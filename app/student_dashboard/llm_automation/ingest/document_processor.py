from typing import List
import os 

from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

import glob
import boto3
from dotenv import load_dotenv




load_dotenv()

from llm_automation.ingest.document_loader import DocumentLoader

class DocumentProcessor:   

    def __init__(self, ignored_files, topic):

        self.ignored_files = ignored_files
        self.chunk_size = int(os.environ.get('chunk_size'))
        self.chunk_overlap = int(os.environ.get('chunk_overlap'))
        self.persist_directory = os.environ.get('PERSIST_DIRECTORY') + f"/{topic}"
        self.s3_bucket_name = os.environ.get('bucket_name')
        self.s3 = boto3.client('s3')

    def process_documents(self, source_directory: str, ignored_files: List[str] = []):
        """
        Load documents from S3 and split in chunks
        """
        print(f"Loading documents from {source_directory}")
        document_loader = DocumentLoader(source_directory, ignored_files)
        document_loader.download_files_from_s3()
        documents = document_loader.load_documents()
        if not documents:
            print("No new documents to load")
            return 0
        print(f"Loaded {len(documents)} new documents from {source_directory}")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        texts = text_splitter.split_documents(documents)
        print(f"Split into {len(texts)} chunks of text (max. {self.chunk_size} tokens each)")
        return texts

    def does_vectorstore_exist(self, persist_directory) -> bool:
        """
        Checks if vectorstore exists
        """
        if os.path.exists(os.path.join(persist_directory, 'index')):
            if os.path.exists(os.path.join(persist_directory, 'chroma-collections.parquet')) and os.path.exists(os.path.join(persist_directory, 'chroma-embeddings.parquet')):
                list_index_files = glob.glob(os.path.join(persist_directory, 'index/*.bin'))
                list_index_files += glob.glob(os.path.join(persist_directory, 'index/*.pkl'))
                # At least 3 documents are needed in a working vectorstore
                if len(list_index_files) > 3:
                    return True
        return False
