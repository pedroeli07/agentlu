
import streamlit as st
import os
from llama_index.tools import FunctionTool
from datetime import datetime



note_dir = "data"
note_file = os.path.join(note_dir, "notas.txt")  
hoje = datetime.now().strftime("%d/%m/%Y")

def salvar_nota(nota, agent_thought):
    global hoje
    if not os.path.exists(note_dir):
        os.makedirs(note_dir)

    # Determinar se é a primeira nota do dia
    primeira_nota = False
    if not os.path.exists(note_file):
        primeira_nota = True
    else:
        with open(note_file, "r", encoding="utf-8") as f:
            primeira_linha = f.readline().strip()
            hoje = datetime.now().strftime("%d/%m/%Y")
            if primeira_linha.startswith("Notas do dia") and primeira_linha.endswith(hoje):
                primeira_nota = False
            else:
                primeira_nota = True
    
    # Construir a nota com as informações de horário, data e identificação da nota
    hora_data = datetime.now().strftime("%H:%M")
    if primeira_nota:
        num_notas = 1
        with open(note_file, "a", encoding="utf-8") as f:
            f.write(f'Notas do dia: {hoje}\n')  # Write the header first
    else:
        with open(note_file, "r", encoding="utf-8") as f:
            existing_notes = [line.strip() for line in f if line.strip().startswith("Nota : ")]
            num_notas = len(existing_notes) + 1  # Count existing notes and increment

    # Reorganizar a ordem para exibir primeiro a nota e depois o pensamento do agente
    nota_final = f"Nota : {num_notas} ({hoje} - {hora_data}):\n\nNota: {nota}\n\nPensamento do agente: {agent_thought}\n\n"

    with open(note_file, "a", encoding="utf-8") as f:
        f.write(nota_final)

    return "Nota salva com sucesso!"

def exibir_notas_salvas():
    note_dir = "data"
    note_file = os.path.join(note_dir, "notas.txt")
    
    if os.path.exists(note_file):
        with open(note_file, "r", encoding="utf-8") as f:
            notas = f.read().split("\n\n")  # Dividir as notas com base em duas quebras de linha
            st.subheader("Notas Salvas")
            for i, nota in enumerate(notas, start=1):
               # st.write(f"Nota {i}:", font="Arial, ", fontsize=26)
                st.write(nota, font="Arial", fontsize=26)  # Exibir cada nota em uma nova linha
    else:
        st.subheader("Notas Salvas")
        st.write("Nenhuma nota foi encontrada.")



note_engine = FunctionTool.from_defaults(
    fn=salvar_nota,
    name="salvador_de_notas",
    description="""Esta ferramenta salva uma nota de texto em um arquivo para o usuário. 
                 As notas são organizadas de forma a incluir a data e hora de cada nota, 
                 e são numeradas sequencialmente, começando com '1ª Nota' para a primeira nota do dia,
                 '2ª Nota' para a segunda nota do dia e assim sucessivamente. Se tiver 30 notas no dia, 
                 vai terminar em '30ª Nota'.""",
)
