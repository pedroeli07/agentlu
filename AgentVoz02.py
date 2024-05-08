import asyncio
import shutil
import boto3 
import subprocess
import time
import streamlit as st

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains import LLMChain
from apikeys import get_api_keys
from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
    Microphone,
)

def ManagerAgent():

    class Manager:
        def __init__(self):
            groq_key, deepgram_key, openai_key, aws_access_key_id, aws_secret_access_key, aws_region = get_api_keys()

            self.llm = ChatOpenAI(temperature=0, model_name="gpt-4-0125-preview", openai_api_key=openai_key)
            self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
            with open('system_prompt.txt', 'r') as file:
                system_prompt = file.read().strip()
            self.prompt = ChatPromptTemplate.from_messages([
                SystemMessagePromptTemplate.from_template(system_prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template("{text}")
            ])
            self.conversation = LLMChain(
                llm=self.llm,
                prompt=self.prompt,
                memory=self.memory
            )

        def process(self, text):
            self.memory.chat_memory.add_user_message(text)
            start_time = time.time()
            response = self.conversation.invoke({"text": text})
            end_time = time.time()
            self.memory.chat_memory.add_ai_message(response['text'])
            elapsed_time = int((end_time - start_time) * 1000)
            print(f"LLM ({elapsed_time}ms): {response['text']}")
            return response['text']

    class TextToSpeech:
        @staticmethod
        def is_installed(lib_name: str) -> bool:
            lib = shutil.which(lib_name)
            return lib is not None
        
        def speak(self, text):
            print("Text to be synthesized:", text)
            polly_client = boto3.client('polly', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)
            if not self.is_installed("ffplay"):
                raise ValueError("ffplay not found, necessary to stream audio.")
            response = polly_client.synthesize_speech(
                Text=text,
                OutputFormat='mp3',
                VoiceId='Vitoria'
            )
            with open('output.mp3', 'wb') as file:
                file.write(response['AudioStream'].read())
            print("Audio file generated successfully.")
            subprocess.run(['ffplay', '-nodisp', 'output.mp3', '-autoexit'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    class TranscriptCollector:
        def __init__(self):
            self.transcript_parts = []
        def reset(self):
            self.transcript_parts = []
        def add_part(self, part):
            self.transcript_parts.append(part)
        def get_full_transcript(self):
            return ' '.join(self.transcript_parts)

    transcript_collector = TranscriptCollector()

    async def get_transcript(callback):
        transcription_complete = asyncio.Event()
        activation_phrase = "Nina"
        activated = False
        try:
            config = DeepgramClientOptions(options={"keepalive": "true"})
            deepgram: DeepgramClient = DeepgramClient("", config)
            dg_connection = deepgram.listen.asynclive.v("1")
            st.write("Aguardando o comando de ativação...")
            st.write("Meu comando de ativação é ' Nina ' ...")
            st.write("Basta dizer isso para começarmos a interagir")
            tts = TextToSpeech()
            async def on_message(self, result, **kwargs):
                nonlocal activated
                sentence = result.channel.alternatives[0].transcript
                if activation_phrase.lower() in sentence.lower() and not activated:
                    st.write("AI Agent (Nina) ativada. Aguardando comandos...")
                    activated = True
                    tts.speak("Nina Ativada. Olá Avelange, como posso te ajudar?")
                    callback("Nina Ativada. Olá Avelange, como posso te ajudar?")
                    manager.start_voice_agent()  # Ativa o agente de voz quando 'Nina' é detectado
                    return

                if not activated:
                    return
                if "parar" in sentence.lower() or "sair" in sentence.lower():
                    st.write("Nina desativada.")
                    activated = False
                    transcription_complete.set()
                    return
                if result.speech_final and sentence.strip():
                    transcript_collector.add_part(sentence)
                    full_sentence = transcript_collector.get_full_transcript()
                    if len(full_sentence.strip()) > 0:
                        full_sentence = full_sentence.strip()
                        st.write(f"Você disse: {full_sentence}")
                        llm_response = manager.llm.process(full_sentence)
                        st.write(f"Nina respondeu: {llm_response}")
                        tts.speak(llm_response)
                        callback(full_sentence)
                        transcript_collector.reset()
            dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
            options = LiveOptions(
                model="nova-2",
                punctuate=True,
                language="pt-BR",
                encoding="linear16",
                channels=1,
                sample_rate=16000,
                endpointing=300,
                smart_format=True,
            )
            await dg_connection.start(options)
            microphone = Microphone(dg_connection.send)
            microphone.start()
            await transcription_complete.wait()
            microphone.finish()
            await dg_connection.finish()
        except Exception as e:
            st.write(f"Could not open socket: {e}")
            return

    class ConversationManager:
        def __init__(self):
            self.transcription_response = ""
            self.llm = Manager()

        async def main(self):
            def handle_full_sentence(full_sentence):
                self.transcription_response = full_sentence

            st.title("Agente de Voz")

            # Caixa de texto para entrada do usuário
            user_input = st.text_area("Digite aqui:", height=100)

            if st.button("Enviar"):
                # Exibir mensagem do usuário em uma caixa de texto formatada
                st.text_area("Você disse:", value=user_input, height=100)

                # Obter e exibir a resposta do agente de voz
                agent_response = self.llm.process(user_input)
                st.text_area("Nina:", value=agent_response, height=100, key="agent_response")


                # Chamada para o método handle_full_sentence com a mensagem do usuário
                handle_full_sentence(user_input)

        def start_voice_agent(self):
            self.active = True
            st.write("Aguardando o comando de ativação...")
            st.write("Meu comando de ativação é ' Nina ' ...")
            st.write("Basta dizer isso para começarmos a interagir")
            asyncio.run(self.main())


    manager = ConversationManager()
    manager.start_voice_agent()
