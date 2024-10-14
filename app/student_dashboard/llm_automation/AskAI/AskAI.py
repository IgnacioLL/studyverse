import os 
from dotenv import load_dotenv

from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings

from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

from fpdf import FPDF
from datetime import datetime

import re

import time 

import random

load_dotenv()

class AskAI:

    def __init__(self, persist_directory, CHROMA_SETTINGS, idioma, topic):
        self.persist_directory = persist_directory
        self.CHROMA_SETTINGS = CHROMA_SETTINGS
        self.idioma = idioma
        self.topic = topic
        self.openai_key = os.environ.get('OPENAI_API_KEY')
        self.model_n_batch = int(os.environ.get('MODEL_N_BATCH',8))
        self.target_source_chunks = int(os.environ.get('TARGET_SOURCE_CHUNKS',4))

    def get_retriever(self):
        embeddings = OpenAIEmbeddings(openai_api_key=self.openai_key)
        db = Chroma(
            persist_directory=self.persist_directory, 
            embedding_function=embeddings, 
            client_settings=self.CHROMA_SETTINGS
            )
        
        self.retriever = db.as_retriever(search_kwargs={"k": self.target_source_chunks})
        return self


    def get_qa_model(self):

        chat_model = ChatOpenAI(
            model_name = "gpt-3.5-turbo-16k",
            temperature=1, 
            max_tokens=300
            )
        
        self.qa = RetrievalQA.from_chain_type(
            llm=chat_model, 
            chain_type="stuff", 
            retriever=self.retriever, 
            return_source_documents= True
            )
        return self 

    def create_answer(self, query = None):
        
        if query is None:
            if self.idioma == "English":
                query = input(f"Write your question about {self.topic}: ")
            elif self.idioma == "Español":
                query = input(f"Escribe tu pregunta acerca de {self.topic}: ")

        start = time.time()
        res = self.qa(query)
        end = time.time()

        return res['result'], round(end - start, 2), res['source_documents']

    def print_sources(self, fuentes):
        for document in fuentes:
            print("\n> " + document.metadata["source"] + ":")
            print(document.page_content)

    def create_exam(self, printSources = False):
        if self.idioma == "English":
            query = f"Create 20 questions about {self.topic}:\n Sure here are the questions:"
        elif self.idioma == "Español":
            query = f"Hazme 20 preguntas acerca de {self.topic}\n Claro esta son las preguntas:"

        answer, time_spend, fuentes = self.create_answer(query)
        if printSources:
            self.print_sources(fuentes)
        answer = re.sub(r'^\d+\.\s*', '', answer) 

        examen = answer.split("\n")[:-1]
        examen = [re.sub('^\d+\.\s*', '', answer) for answer in examen]

        print(examen)
        self.new_exam = random.sample(examen, 4)
        return self, time_spend
        

    def create_exam_pdf(self, output):
        pdf = FPDF()

        # Add a page
        pdf.add_page()

        # Set font
        pdf.set_font("Arial", 'B', size = 12)

        # Add 'StudyVerse' at the top right
        pdf.cell(0, 10, txt='StudyVerse', ln=True, align='R')

        # Add the date of creation just below 'StudyVerse'
        today_date = datetime.today().strftime("%Y-%m-%d")
        pdf.cell(0, 10, txt=today_date, ln=True, align='R')

        # Set font for exam title (slightly bigger than the other text)
        pdf.set_font("Arial", 'B', size=16)
        
        # Line breaks 
        pdf.ln(10)
        
        # Add topic in the center
        pdf.cell(0, 10, txt = f"Examen de {self.topic}", ln=True, align='C')

        # Set font for questions
        pdf.set_font("Arial", size = 12)

        # Line break between the topic and questions
        pdf.ln(10)

        # Add questions
        # Four lines between questions
        for i, question in enumerate(self.new_exam, 1):
            pdf.cell(0, 10, txt = f"{i}. {question}", ln = True, align = 'L')
            pdf.ln(30)

        # Save the pdf with name .pdf
        pdf.output(output)
