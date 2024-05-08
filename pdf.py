import os
from llama_index import StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.readers import PDFReader
import pandas as pd
from llama_index.query_engine import PandasQueryEngine

def get_index(data, index_name):
    index = None
    if not os.path.exists(index_name):
        print("building index", index_name)
        index = VectorStoreIndex.from_documents(data, show_progress=True)
        index.storage_context.persist(persist_dir=index_name)
    else:
        index = load_index_from_storage(
            StorageContext.from_defaults(persist_dir=index_name)
        )

    return index


pdf_path = os.path.join("data", "Texas_holdem_poker_pt.pdf")
poker_pdf = PDFReader().load_data(file=pdf_path)
poker_index = get_index(poker_pdf, "poker")
poker_engine = poker_index.as_query_engine()


note_path = os.path.join("data", "notas.txt")

# Lista para armazenar as linhas de notas
notas = []

# Leitura do arquivo de notas linha por linha
with open(note_path, "r") as file:
    nota_atual = {}
    for line in file:
        line = line.strip()
        if line.startswith("Notas do dia:"):
            if nota_atual:
                notas.append(nota_atual)
                nota_atual = {}
            nota_atual["data"] = line.split(":")[1].strip()
        elif line.startswith("Nota :"):
            if nota_atual:
                notas.append(nota_atual)
                nota_atual = {}
            info = line.split(":")
            if len(info) > 1:
                numero_hora = info[0].split()
                if len(numero_hora) > 1:
                    nota_atual["numero"] = int(numero_hora[1])
                    nota_atual["hora"] = info[1].split("(")[0].strip()
        elif line.startswith("Nota:"):
            nota_atual["conteudo"] = line.split(":")[1].strip()
        elif line.startswith("Pensamento do agente:"):
            nota_atual["pensamento"] = line.split(":")[1].strip()

# Adicionando a última nota à lista
if nota_atual:
    notas.append(nota_atual)

# Criando o DataFrame Pandas com as notas
notas_df = pd.DataFrame(notas)


# Em vez disso, você pode usar diretamente o conteúdo do arquivo de notas
notas_engine = PandasQueryEngine(df=notas_df, verbose=True)



