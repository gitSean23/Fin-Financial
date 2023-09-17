# pdf code
from api import open_api_key
from api import pinecone_api_key
from api import pinecone_env
import openai
import os
import getpass
import langchain
import pinecone
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone

os.environ["OPENAI_API_KEY"] = open_api_key
os.environ["PINECONE_API_KEY"] = pinecone_api_key
os.environ["PINECONE_ENV"] = pinecone_env


def create_qa_bot(query):
    # Load
    # loader = PyPDFLoader("pdf/Vanguard_guide_to_financial_wellness.pdf")
    # rawDocs = loader.load()

    # # Splitting
    # text_splitter = RecursiveCharacterTextSplitter(
    #         chunk_size = 1000,
    #         chunk_overlap = 200,
    # )
    # docs = text_splitter.split_documents(rawDocs)

    # Bring in the embedding API
    embeddings = OpenAIEmbeddings()

    # Initialize the pinecone api and environment
    pinecone.init(
        api_key=os.getenv("PINECONE_API_KEY"),  # find at app.pinecone.io
        environment=os.getenv("PINECONE_ENV"),  # next to api key in console
    )

    # Create the index if needed.
    # The OpenAI embedding model `text-embedding-ada-002 uses 1536 dimensions`
    index_name = "vanguard-guide"
    # if index_name not in pinecone.list_indexes():
    #     # we create a new index
    #     pinecone.create_index(
    #     name=index_name,
    #     metric='cosine',
    #     dimension=1536  
    # )

    # Find the doc from the index.
    docsearch = Pinecone.from_existing_index(index_name, embeddings)
    relevent_docs = docsearch.similarity_search(query)

    # Langchain to answer the query with the relevant docs.
    llm = ChatOpenAI(temperature=0, openai_api_key=open_api_key, model_name='gpt-4')
    chain = load_qa_chain(llm, chain_type="stuff")
    relevent_docs = docsearch.similarity_search(query)
    answer = chain.run(input_documents=relevent_docs, question=query)

    # Answer plaintext is returned.
    return answer

