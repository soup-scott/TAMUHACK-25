import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

os.environ["OPENAI_API_KEY"] = "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"

documents = SimpleDirectoryReader("./data").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
response = query_engine.query("What is the third article entail?")
print(response)