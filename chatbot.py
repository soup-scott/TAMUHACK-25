import os
import requests as rq
from bs4 import BeautifulSoup
from dotenv import load_dotenv
#from llama_index.readers.web import BeautifulSoupWebReader
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.query_pipeline import QueryPipeline, InputComponent
from llama_index.core.prompts import PromptTemplate
from llama_index.llms.openai import OpenAI
from llama_index.postprocessor.colbert_rerank import ColbertRerank
from typing import Any, Dict, List, Optional
from llama_index.core.bridge.pydantic import Field
from llama_index.core.llms import ChatMessage
from llama_index.core.query_pipeline import CustomQueryComponent
from llama_index.core.schema import NodeWithScore
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.readers.json import JSONReader

class NodeMergerComponent(CustomQueryComponent):
    """Custom component to merge node lists from two retrievers"""
    # def _run_component(self, **kwargs):
    #     print(f"Merger inputs: { {k: type(v) for k,v in kwargs.items()} }")
    #     merged = kwargs["rewrite_nodes"] + kwargs["query_nodes"]
    #     print(f"Merged output type: {type(merged)}")
    #     return {"nodes": merged}
    
    @property
    def _input_keys(self) -> set:
        return {"rewrite_nodes", "query_nodes"}

    @property
    def _output_keys(self) -> set:
        return {"nodes"}

    def _run_component(self, rewrite_nodes: List[NodeWithScore], query_nodes: List[NodeWithScore]) -> Dict:
        return {"nodes": rewrite_nodes + query_nodes}


#openAI set up
load_dotenv()
os.environ["OPENAI_API_KEY"] = "add your own key bukko"

# documents stuff to copy over wrote
documents = SimpleDirectoryReader("./data").load_data()

#creating embeddings
index = VectorStoreIndex.from_documents(
    documents,
    embed_model=OpenAIEmbedding(
        model="text-embedding-3-large", embed_batch_size=256 #look at these parameters to see if they fit
    ),
)

def load_files():
    PERSIST_DIR = "./storage"

    if not os.path.exists(PERSIST_DIR):
        #initialize JSONreader and load JSON
        reader = JSONReader(levels_back=0, collapse_length=None, ensure_ascii=False, is_jsonl=False, clean_json=True)
        documents = reader.load_data(input_file="./data/test.json", extra_info={})

        #load pdf docs
        documents += SimpleDirectoryReader("./data").load_data()
        print("With a total of " + str(len(documents)) + " documents")
        #create an index for querying
        index = VectorStoreIndex.from_documents(
            documents,
            embed_model=OpenAIEmbedding(
                model="text-embedding-3-large", embed_batch_size=256 #look at these parameters to see if they fit
            ),
        )

        #store in folder for future use
        index.storage_context.persist(persist_dir=PERSIST_DIR)
    else:
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        index = load_index_from_storage(storage_context)

    return index

#Creating Query Pipeline

#defining default template that responses should follow
input_component = InputComponent()
rewrite = ( #CHANGE THISSSSSSSSSSSSSS AHHHHHHHHHHHHHH
    "Please write a response that prompts the user to buy the best car for them using the current conversation.\n"
    "\n"
    "\n"
    "{chat_history_str}"
    "\n"
    "\n"
    "Latest message: {query_str}\n"
    'Query:"""\n'
)

rewrite_template = PromptTemplate(rewrite)
llm = OpenAI(
    model="gpt-4",
    temperature=0.1, #look at these parameters to see if they fit
    max_tokens=1000,
)

#packing document and format info. Defining prompt manipulation
# argpack_component = ArgPackComponent(
#     partial_dict={},
#     convert_fn=lambda x: x["rewrite_nodes"] + x["query_nodes"]
# )
node_merger = NodeMergerComponent()

# print(argpack_component)

retriever = index.as_retriever(similarity_top_k=6) #double check this

reranker = ColbertRerank(top_n=3) #^


#defining the custom query component
DEFAULT_CONTEXT_PROMPT = (
    "Here is some context that may be relevant:\n"
    "-----\n" #write something here
    "{node_context}\n"
    "-----\n"
    "Please write a response to the following question, using the above context:\n"
    "{query_str}\n"
)

class ResponseWithChatHistory(CustomQueryComponent):
    llm: OpenAI = Field(..., description="OpenAI LLM") #this is supposed to have ellipses
    system_prompt: Optional[str] = Field( #Not giving a system prompt now - gives later
        default=None, description="System prompt to use for the LLM"
    )
    context_prompt: str = Field( #feed the context prompt
        default=DEFAULT_CONTEXT_PROMPT,
        description="Context prompt to use for the LLM",
    )

    def _validate_component_inputs( #I don't understand this
        self, input: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate component inputs during run_component."""
        # NOTE: this is OPTIONAL but we show you where to do validation as an example
        return input

    @property
    def _input_keys(self) -> set: #figure out how to define this - AJJ
        """Input keys dict."""
        # NOTE: These are required inputs. If you have optional inputs please override
        # `optional_input_keys_dict`
        return {"chat_history", "nodes", "query_str"}

    @property
    def _output_keys(self) -> set:
        return {"response"}

    def _prepare_context(
        self,
        chat_history: List[ChatMessage],
        nodes: List[NodeWithScore],
        query_str: str,
    ) -> List[ChatMessage]:
        node_context = ""
        for idx, node in enumerate(nodes):
            node_text = node.get_content(metadata_mode="llm")
            node_context += f"Context Chunk {idx}:\n{node_text}\n\n"

        formatted_context = self.context_prompt.format(
            node_context=node_context, query_str=query_str
        )
        user_message = ChatMessage(role="user", content=formatted_context)

        chat_history.append(user_message)

        if self.system_prompt is not None:
            chat_history = [
                ChatMessage(role="system", content=self.system_prompt)
            ] + chat_history

        return chat_history

    def _run_component(self, **kwargs) -> Dict[str, Any]:
        """Run the component."""
        chat_history = kwargs["chat_history"]
        nodes = kwargs["nodes"]
        query_str = kwargs["query_str"]

        prepared_context = self._prepare_context(
            chat_history, nodes, query_str
        )

        response = llm.chat(prepared_context)

        return {"response": response}

    # async def _arun_component(self, **kwargs: Any) -> Dict[str, Any]:
    #     """Run the component asynchronously."""
    #     # NOTE: Optional, but async LLM calls are easy to implement
    #     chat_history = kwargs["chat_history"]
    #     nodes = kwargs["nodes"]
    #     query_str = kwargs["query_str"]

    #     prepared_context = self._prepare_context(
    #         chat_history, nodes, query_str
    #     )

    #     response = await llm.achat(prepared_context)

    #     return {"response": response}

response_component = ResponseWithChatHistory(
    llm=llm,
    system_prompt=( #REWRITE AHHHHHHHHHHHHHHH
        "You are a toyota support representative, helping a user pick a car. You will be provided with the previous chat history, "
        "as well as possibly relevant context, to assist in answering a user message."
    ),
)

pipeline = QueryPipeline(
    modules={
        "input": input_component,
        "rewrite_template": rewrite_template,
        "llm": llm,
        "rewrite_retriever": retriever,
        "query_retriever": retriever,
        "join": node_merger,
        "reranker": reranker,
        "response_component": response_component,
    },
    verbose=False,
)
# print(pipeline)
# run both retrievers -- once with the hallucinated query, once with the real query
pipeline.add_link(
    "input", "rewrite_template", src_key="query_str", dest_key="query_str"
)
pipeline.add_link(
    "input",
    "rewrite_template",
    src_key="chat_history_str",
    dest_key="chat_history_str",
)
pipeline.add_link("rewrite_template", "llm")
pipeline.add_link("llm", "rewrite_retriever")
pipeline.add_link("input", "query_retriever", src_key="query_str")

# each input to the argpack component needs a dest key -- it can be anything
# then, the argpack component will pack all the inputs into a single list 

#Links from original

# pipeline.add_link("rewrite_retriever", "join", dest_key="rewrite_nodes")
# pipeline.add_link("query_retriever", "join", dest_key="query_nodes")

# # reranker needs the packed nodes and the query string
# pipeline.add_link("join", "reranker", dest_key="nodes")

pipeline.add_link("rewrite_retriever", "join", dest_key="rewrite_nodes")
pipeline.add_link("query_retriever", "join", dest_key="query_nodes")
pipeline.add_link("join", "reranker", dest_key="nodes")
pipeline.add_link(
    "input", "reranker", src_key="query_str", dest_key="query_str"
)

# synthesizer needs the reranked nodes and query str
pipeline.add_link("reranker", "response_component", dest_key="nodes")
pipeline.add_link(
    "input", "response_component", src_key="query_str", dest_key="query_str"
)
pipeline.add_link(
    "input",
    "response_component",
    src_key="chat_history",
    dest_key="chat_history",
)


pipeline_memory = ChatMemoryBuffer.from_defaults(token_limit=8000)

# user_inputs = [
#     "Hello!",
#     "I'd like to get a car with a high gas milage, but I'm scared of hybrid cars?",
#     "Do any of those come in yellow?",
#     "Thanks, that what I needed to know!",
# ]
user_inputs = ["Hello!"]

# test_nodes1 = retriever.retrieve("test query")
# test_nodes2 = retriever.retrieve("another query")
# print(type(test_nodes1)) 

for j, msg in enumerate(user_inputs):
    
    # get memory
    chat_history = pipeline_memory.get()

    # prepare inputs
    chat_history_str = "\n".join([str(x) for x in chat_history])

    #print(pipeline)
    # run pipeline
    response = pipeline.run(
        query_str=msg,
        chat_history=chat_history,
        chat_history_str=chat_history_str,
    )
    
    # update memory
    user_msg = ChatMessage(role="user", content=msg)
    pipeline_memory.put(user_msg)
    print("User Message:")
    if j >0:
        print(str(user_msg))

    pipeline_memory.put(response.message)
    print("Response:")
    print(str(response.message))
    print()
    
    user_inputs.append(input())

