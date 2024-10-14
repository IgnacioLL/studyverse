from typing import List
import os
from tqdm import tqdm
from multiprocessing import Pool
import glob


from dotenv import load_dotenv

import boto3

from langchain.docstore.document import Document
from langchain.document_loaders import (
    CSVLoader,
    EverNoteLoader,
    PyMuPDFLoader,
    TextLoader,
    UnstructuredEmailLoader,
    UnstructuredEPubLoader,
    UnstructuredHTMLLoader,
    UnstructuredMarkdownLoader,
    UnstructuredODTLoader,
    UnstructuredPowerPointLoader,
    UnstructuredWordDocumentLoader,
)

load_dotenv()


s3_bucket_name = os.environ.get('bucket_name')

# Custom document loaders
class MyElmLoader(UnstructuredEmailLoader):
    """Wrapper to fallback to text/plain when default does not work"""

    def load(self) -> List[Document]:
        """Wrapper adding fallback for elm without html"""
        try:
            try:
                doc = UnstructuredEmailLoader.load(self)
            except ValueError as e:
                if 'text/html content not found in email' in str(e):
                    # Try plain text
                    self.unstructured_kwargs["content_source"]="text/plain"
                    doc = UnstructuredEmailLoader.load(self)
                else:
                    raise
        except Exception as e:
            # Add file_path to exception message
            raise type(e)(f"{self.file_path}: {e}") from e

        return doc





class DocumentLoader:

    LOADER_MAPPING = {
        ".csv": (CSVLoader, {}),
        ".doc": (UnstructuredWordDocumentLoader, {}),
        ".docx": (UnstructuredWordDocumentLoader, {}),
        ".enex": (EverNoteLoader, {}),
        ".eml": (MyElmLoader, {}),
        ".epub": (UnstructuredEPubLoader, {}),
        ".html": (UnstructuredHTMLLoader, {}),
        ".md": (UnstructuredMarkdownLoader, {}),
        ".odt": (UnstructuredODTLoader, {}),
        ".pdf": (PyMuPDFLoader, {}),
        ".ppt": (UnstructuredPowerPointLoader, {}),
        ".pptx": (UnstructuredPowerPointLoader, {}),
        ".ppsx": (UnstructuredPowerPointLoader, {}),
        ".txt": (TextLoader, {"encoding": "utf8"}),
    }

    def __init__(self, source_dir: str, ignored_files: List[str] = []):
        self.source_dir = source_dir
        self.ignored_files = ignored_files
        self.s3_bucket_name = s3_bucket_name
        self.s3 = boto3.client('s3')

        print(f"El origen es {self.source_dir}")


    def download_files_from_s3(self):
        response =  self.s3.list_objects_v2(Bucket=self.s3_bucket_name, Prefix=self.source_dir)

        local_file_path = os.environ.get("temp_media")
        os.makedirs(local_file_path,exist_ok=True)

        for content in response.get('Contents', []):
            key = content['Key']
            # Check if the object is a file (not a directory)
            if not key.endswith('/'):
                # Generate the local file path for the downloaded object
                for ext in self.LOADER_MAPPING:
                    if str(key).endswith(ext):
                        file_path = f"{local_file_path}/{key}"
                        os.makedirs("/".join(str(file_path).split("/")[:-1]),exist_ok=True)
                        self.s3.download_file(self.s3_bucket_name, key, file_path)


    def load_single_document(self, file_path: str) -> List[Document]:
        ext = "." + file_path.rsplit(".", 1)[-1]
        if ext in self.LOADER_MAPPING:
            loader_class, loader_args = self.LOADER_MAPPING[ext]
            loader = loader_class(file_path, **loader_args)
            return loader.load()

        raise ValueError(f"Unsupported file extension '{ext}'")


    def load_documents(self) -> List[Document]:
        """
        Loads all documents from the source documents directory, ignoring specified files
        """
        temp_media = os.environ.get("temp_media")

        all_files = []
        for ext in self.LOADER_MAPPING:
            all_files.extend(
                glob.glob(os.path.join(temp_media, f"**/*{ext}"), recursive=True)
            )

        filtered_files = [file_path for file_path in all_files if file_path not in self.ignored_files]
        filtered_files = [file_path for file_path in all_files if "SVExam" not in file_path]

        results = []
        with tqdm(total=len(filtered_files), desc='Loading new documents', ncols=80) as pbar:
            for file_path in filtered_files:
                docs = self.load_single_document(file_path)

                results.extend(docs)
                pbar.update()
        return results