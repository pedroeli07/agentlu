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
import sounddevice as sd
import soundfile as sf
import os

def Manager():
    # Import the API keys using the function from apikeys.py
    groq_key, deepgram_key, openai_key, aws_access_key_id, aws_secret_access_key, aws_region = get_api_keys()

    class LanguageModelProcessor:
        def __init__(self):
            self.llm = ChatOpenAI(temperature=0, model_name="gpt-4-0125-preview", openai_api_key=openai_key)
            self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

            # Load the system prompt from a file
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
            self.memory.chat_memory.add_user_message(text)  # Add user message to memory

            start_time = time.time()

            # Go get the response from the LLM
            response = self.conversation.invoke({"text": text})
            end_time = time.time()

            self.memory.chat_memory.add_ai_message(response['text'])  # Add AI response to memory

            elapsed_time = int((end_time - start_time) * 1000)
            print(f"LLM ({elapsed_time}ms): {response['text']}")
            return response['text']  # Remove a conversão de codificação aqui
    class TextToSpeech:
        @staticmethod
        def is_installed(lib_name: str) -> bool:
            lib = shutil.which(lib_name)
            return lib is not None
    
        def speak(self, text):
            print("Text to be synthesized:", text)  # Debugging: Print the text to be synthesized
            # Ensure UTF-8 encoding for text
            text_utf8 = text.encode('utf-8')
            # Inicializa o cliente do Polly
            polly_client = boto3.client('polly',
                                        aws_access_key_id=aws_access_key_id,
                                        aws_secret_access_key=aws_secret_access_key,
                                        region_name=aws_region)
            if not self.is_installed("ffplay"):
                raise ValueError("ffplay not found, necessary to stream audio.")
            
            # Explicitly specify UTF-8 encoding in Polly request
            response = polly_client.synthesize_speech(
                Text=text_utf8.decode('utf-8'),  # Decode back to string for API call
                OutputFormat='mp3',
                VoiceId='Vitoria'  # Choose the desired voice
            )   
            with open('output.mp3', 'wb') as file:
                file.write(response['AudioStream'].read())

            print("Audio file generated successfully.")  # Debugging: Print a message indicating successful audio file generation

            # Reproduz o áudio usando o sounddevice
            data, fs = sf.read('output.mp3', dtype='float32')
            sd.play(data, fs)
            sd.wait()  # Espera a reprodução do áudio terminar

            # Remove o arquivo de áudio gerado
            os.remove('output.mp3')

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
        transcription_complete = asyncio.Event()  # Event to signal transcription completion
        activation_phrase = "Nina"  # Modifique a frase de ativação conforme necessário
        activated = False

        try:
            # Configuração do cliente Deepgram
            config = DeepgramClientOptions(options={"keepalive": "true"})
            deepgram: DeepgramClient = DeepgramClient("", config)

            dg_connection = deepgram.listen.asynclive.v("1")
        
            tts = TextToSpeech()  # Defina tts fora da função on_message
        
            async def on_message(self, result, **kwargs):
                nonlocal activated

                sentence = result.channel.alternatives[0].transcript

                # Check if activation phrase is detected and agent is not already activated
                if activation_phrase.lower() in sentence.lower() and not activated:
                    st.write("AI Agent (Nina) ativada. Aguardando comandos...")
                    activated = True
                    # Say the activation phrase
                #   tts = TextToSpeech()
                    tts.speak("Nina Ativada. Olá Avelange, como posso te ajudar?")
                    # Add activation phrase to conversation history
                    callback("Nina Ativada. Olá Avelange, como posso te ajudar?")
                    return

                # If agent is not activated, we don't process further
                if not activated:
                    return

                # Check if stop command is given
                if "parar" in sentence.lower() or "sair" in sentence.lower():
                    st.write("Nina desativada.")
                    activated = False
                    transcription_complete.set()
                    return

                # Process further only if speech is finalized and transcription is not empty
                if result.speech_final and sentence.strip():
                    transcript_collector.add_part(sentence)
                    full_sentence = transcript_collector.get_full_transcript()
                    # Check if the full_sentence is not empty before printing
                    if len(full_sentence.strip()) > 0:
                        full_sentence = full_sentence.strip()
                        # Print the question before processing the agent's response
                        st.write(f"Você disse: {full_sentence}")
                        # Get AI response
                        llm_response = manager.llm.process(full_sentence)
                        # Show AI response
                        st.write(f"Nina respondeu : {llm_response}")
                        tts.speak(llm_response)  # Fale a resposta do IA
                        callback(full_sentence)  # Chame o retorno de chamada com full_sentence
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

            # Open a microphone stream on the default input device
            microphone = Microphone(dg_connection.send)
            microphone.start()

            await transcription_complete.wait()  # Wait for the transcription to complete instead of looping indefinitely

            # Wait for the microphone to close
            microphone.finish()

            # Indicate that we've finished
            await dg_connection.finish()

        except Exception as e:
            st.write(f"Could not open socket: {e}")
            return

    class ConversationManager:
        def __init__(self):
            self.transcription_response = ""
            self.llm = LanguageModelProcessor()

        async def main(self):
            def handle_full_sentence(full_sentence):
                self.transcription_response = full_sentence

            # Loop indefinitely until "goodbye" is detected
            while True:
                await get_transcript(handle_full_sentence)
                
                # Check for "goodbye" to exit the loop
                if "Nina Desativar" in self.transcription_response.lower():
                    break
                
                llm_response = self.llm.process(self.transcription_response)

                tts = TextToSpeech()
                tts.speak(llm_response)

                # Reset transcription_response for the next loop iteration
                self.transcription_response = ""

        def start_voice_agent(self):
            self.active = True
            asyncio.run(self.main())  # Inicia o loop de conversa em uma nova thread


    #if __name__ == "__main__":
    manager = ConversationManager()
    asyncio.run(manager.main())



