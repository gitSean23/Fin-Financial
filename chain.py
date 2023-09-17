# pdf code
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
from dotenv import load_dotenv

# OPENAI_API_KEY = config('OPENAI_API_KEY')
# PINECONE_API_KEY = config('PINECONE_API_KEY')
# PINECONE_ENV = config('PINECONE_ENV')

load_dotenv()


def create_qa_bot(query):

    # Bring in the embedding API
    embeddings = OpenAIEmbeddings()

    # Initialize the pinecone api and environment
    pinecone.init(
        api_key=os.environ['PINECONE_API_KEY'],  # find at app.pinecone.io
        environment=os.environ['PINECONE_ENV'],  # next to api key in console
    )

    # The OpenAI embedding model `text-embedding-ada-002 uses 1536 dimensions`
    index_name = "vanguard-guide"

    # Find the doc from the index.
    docsearch = Pinecone.from_existing_index(index_name, embeddings)
    relevent_docs = docsearch.similarity_search(query)

    # Langchain to answer the query with the relevant docs.
    llm = ChatOpenAI(temperature=0, openai_api_key=os.environ['OPENAI_API_KEY'], model_name='gpt-4')
    chain = load_qa_chain(llm, chain_type="stuff")
    relevent_docs = docsearch.similarity_search(query)
    answer = chain.run(input_documents=relevent_docs, question=query)
    # Answer plaintext is returned.
    return answer

