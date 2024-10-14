#!/usr/bin/env python3
import os
import glob
from typing import List
from dotenv import load_dotenv
from multiprocessing import Pool
from tqdm import tqdm

import random




from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings

from llm_automation.AskAI.AskAI import AskAI

import sys

from chromadb.config import Settings

from llm_automation.ingest.document_processor import DocumentProcessor 
import boto3


import shutil
# Define the folder for storing database


# Define the Chroma settings
load_dotenv()

def delete_local(source_directory,persist_directory, temp_media, temp_exam):
        shutil.rmtree(f"{persist_directory}{source_directory}")
        shutil.rmtree(f"{temp_media}{source_directory}")
        try:
            shutil.rmtree(f"{temp_exam}{source_directory}")
        except: 
            pass

        return 

def delete_s3_folder(bucket_name, folder_prefix):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)

    # List objects with the specified prefix
    objects_to_delete = bucket.objects.filter(Prefix=folder_prefix)

    # Delete each object
    for s3_object in objects_to_delete:
        s3_object.delete()


PERSIST_DIRECTORY = os.environ.get("PERSIST_DIRECTORY")
s3_bucket_name = os.environ.get("bucket_name")
s3 = boto3.client('s3')
temp_exam = os.environ.get('temp_exam')
temp_media= os.environ.get('temp_media')



def main(source_directory,topic,idioma, chat=None):

    assert idioma in ['English','Español'], "Este idioma no esta contemplado"


    openai_key = os.environ.get('OPENAI_API_KEY')
    persist_directory = f"{PERSIST_DIRECTORY}{source_directory}" 

    CHROMA_SETTINGS = Settings(
        chroma_db_impl='duckdb+parquet',
        persist_directory=persist_directory,
        anonymized_telemetry=False
    )   



    # Create embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=openai_key)
    document_processor = DocumentProcessor(ignored_files=[], topic=topic)

    

    if document_processor.does_vectorstore_exist(persist_directory):
        response =  s3.list_objects_v2(Bucket=s3_bucket_name, Prefix="db/" + source_directory)

        temp_db = persist_directory
        os.makedirs(temp_db,exist_ok=True)

        for content in response.get('Contents', []):
            key = content['Key']
            # Check if the object is a file (not a directory)
            if not key.endswith('/'):
                # Generate the local file path for the downloaded object
                file_path = f"{temp_db}/{key}"
                os.makedirs("/".join(str(file_path).split("/")[:-1]),exist_ok=True)
                s3.download_file(s3_bucket_name, key, file_path)

        # Update and store locally vectorstore
        print(f"Appending to existing vectorstore at {persist_directory}")
        db = Chroma(persist_directory=persist_directory, embedding_function=embeddings, client_settings=CHROMA_SETTINGS)

        collection = db.get()

        
        texts_not_repeat = [metadata['source'] for metadata in collection['metadatas']]

        texts = document_processor.process_documents(source_directory, texts_not_repeat)
        if texts == 0:
            pass
        else:
            delete_s3_folder(s3_bucket_name, f"db/{source_directory}")
            print(f"Creating embeddings. May take some minutes...")
            db.add_documents(texts)
            db.persist()


    else:
        
        # Create and store locally vectorstore
        print("Creating new vectorstore")
        texts = document_processor.process_documents(source_directory)
        print(f"Creating embeddings. May take some minutes...")
        db = Chroma.from_documents(texts, embeddings, persist_directory=persist_directory, client_settings=CHROMA_SETTINGS)
        db.persist()

    db = None
    print(f"Ingestion complete!")


    if chat is None:
        model = AskAI(persist_directory, CHROMA_SETTINGS, idioma, topic)

        model = model.get_retriever().get_qa_model()

        model, _ = model.create_exam()
        os.makedirs(f"temp_exam/{source_directory}", exist_ok=True)
        nombre_examen = f"SVExam_{topic}.pdf"
        exam_path = f"temp_exam/{source_directory}/{nombre_examen}"
        model = model.create_exam_pdf(exam_path)

        for root, dirs, files in os.walk(os.environ.get('PERSIST_DIRECTORY')):
            for file in files:
                file_path = os.path.join(root, file)
                s3.upload_file(exam_path, s3_bucket_name, f"{source_directory}/{nombre_examen}")


        return 0

    else:
        model = AskAI(persist_directory, CHROMA_SETTINGS, idioma, topic)

        model = model.get_retriever().get_qa_model()

        answer, time_spend, fuentes = model.create_answer(chat)

        return answer, time_spend, fuentes

if __name__ == "__main__":
    main("/home/ubuntu/one/app/student_dashboard/media/1/79","toxicologia","Español")
