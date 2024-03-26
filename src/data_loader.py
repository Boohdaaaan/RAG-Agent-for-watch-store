import os
import json
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveJsonSplitter, RecursiveCharacterTextSplitter


def load_data(root_dir: str = 'data', chunk_size: int = 1000, chunk_overlap: int = 100):
    # Get list of documents in the specified directory
    documents_list = os.listdir(root_dir)

    # Loop through each document in the directory
    for doc in documents_list:
        try:
            # Check if the document is a text file
            if '.txt' in doc:
                # Load the text document and split it into chunks
                loader = TextLoader(os.path.join(root_dir, doc), encoding='utf-8')
                documents = loader.load()

                # Split each document into chunks
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
                docs = text_splitter.split_documents(documents)

                # Create the open-source embedding function
                embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

                # Load documents into Chroma
                db = Chroma.from_documents(docs, embedding_function)

            # Check if the document is a JSON file
            elif '.json' in doc:
                # Load JSON data from the file
                with open(os.path.join(root_dir, doc), 'r', encoding='utf-8') as f:
                    json_data = json.load(f)

                # Split JSON data into chunks
                splitter = RecursiveJsonSplitter(max_chunk_size=300)
                # The splitter can also output documents
                docs = splitter.create_documents(texts=[json_data])

                # Create the open-source embedding function
                embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

                # Load documents into Chroma
                db = Chroma.from_documents(docs, embedding_function)

        except Exception as e:
            # If there's an error loading a document, print the error
            print("Error loading the document:", e)

    return db


# Call the load_data function with specified parameters
db = load_data('./data/', 1000, 100)
