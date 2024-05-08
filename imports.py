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
from time import sleep
from apikeys import get_api_keys
from Contatos import mostrar_contatos
from Agent import configure_agent
from note_engine import exibir_notas_salvas
from AgentNota import configure_agent02
from Home import home
from custom_theme import hide_menu, hide_share_icon, hide_top_right_icons
from AgentVoz import Manager
import os
import pandas as pd
from llama_index.core.query_engine import PandasQueryEngine
from prompts import new_prompt, instruction_str, context
from note_engine import note_engine
from llama_index.tools import QueryEngineTool, ToolMetadata
from llama_index.agent import ReActAgent
from llama_index.llms import OpenAI
from pdf import poker_engine, notas_engine
from llama_index import PromptTemplate
from llama_index.tools import FunctionTool
from datetime import datetime
from llama_index import StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.readers import PDFReader
from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
    Microphone,
)