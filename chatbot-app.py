import os
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.readers.json import JSONReader
from llama_index.llms.openai import OpenAI

#env loader
os.environ["OPENAI_API_KEY"] = "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"

#llm loader
# , api_key="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"
llm = OpenAI(temperature=0.1, model="gpt-4o", max_tokens=512)

def load_files():
    #initialize JSONreader and load JSON
    reader = JSONReader(levels_back=0, collapse_length=None, ensure_ascii=False, is_jsonl=False, clean_json=True)
    documents = reader.load_data(input_file="./data/test.json", extra_info={})

    #load pdf docs
    documents += SimpleDirectoryReader("./data").load_data()
    print("With a total of " + str(len(documents)) + " documents")
    #create an index for querying
    index = VectorStoreIndex.from_documents(documents)
    return index

def query_index(index, query):
    query_engine = index.as_query_engine()
    response = query_engine.query(query)
    return response

index = load_files()
print("Indexing completed!")

user_query = "What are the specs of the Rav4 2025 model? I also want to consider the price and mileage. Also give me the image link."
response = query_index(index, user_query)
print(f"Response: {response}")
