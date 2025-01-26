from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.readers.json import JSONReader
import os
from llama_index.llms.openai import OpenAI


os.environ["OPENAI_API_KEY"] = "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"
llm = OpenAI(temperature=0.1, model="gpt-4o", max_tokens=512, api_key="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")
# Function to load and index JSON data
def load_and_index_json():
    reader = JSONReader(
        levels_back=0,             # Set levels back as needed
        collapse_length=None,      # Set collapse length as needed
        ensure_ascii=False,        # ASCII encoding option
        is_jsonl=False,            # Set if input is JSON Lines format
        clean_json=True            # Clean up formatting-only lines
    )

    # Find all JSON files in the specified directory
    # json_files = glob.glob(os.path.join(directory_path, "*.json"))

    # Load the data from each JSON file
    # documents = []
    # for json_file in json_files:
        # documents.extend(reader.load_data(input_file=json_file, extra_info={}))
    
    documents = reader.load_data(input_file="./data/test.json", extra_info={})

    # Create an index for querying
    index = VectorStoreIndex.from_documents(documents)
    return index

# Specify the directory containing your JSON files
json_directory = "./data"

# Load JSON and create an index
index = load_and_index_json()
print("Indexing completed!")

# Query the index
def query_index(index, query):
    query_engine = index.as_query_engine()
    response = query_engine.query(query)
    return response

# Example query
user_query = "What are the specs of the Rav4 2025 model?"
response = query_index(index, user_query)
print(f"Response: {response}")