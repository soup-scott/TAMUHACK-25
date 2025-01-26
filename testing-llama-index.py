import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

load_dotenv()
# os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = "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"
documents = SimpleDirectoryReader("./data").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
response = query_engine.query("What is the third article entail?")
print(response)