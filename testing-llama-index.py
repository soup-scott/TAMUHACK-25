import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

load_dotenv()
# os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = "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"
documents = SimpleDirectoryReader("./data").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
print(len(documents))
response = query_engine.query("You are Clara, a toyota agent helping a customer pick a toyata car. Please introduce yourself to the customer, ask them their name and what they are looking for, and provide them with a list of the top 5 that fit their needs. Once the customer has selected a car, provide them with the price and transfer them to billing by saying \"Transferring you to billing now.\"")
print(response)

while response != "Transferring you to billing now.":
    response = query_engine.query(input(response))