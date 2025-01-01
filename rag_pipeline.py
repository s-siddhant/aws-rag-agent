from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter, SemanticSplitterNodeParser
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import SummaryIndex, VectorStoreIndex
from llama_index.core.tools import QueryEngineTool
from llama_index.core.query_engine.router_query_engine import RouterQueryEngine
import os
import shutil

def initialize_query_engine(file_path: str, openai_key: str, parser_type='semantic'):
    """Initialize and return a router query engine with OpenAI models."""
    if not openai_key:
        raise ValueError("OpenAI API key is required.")

    # Set OpenAI API key
    os.environ["OPENAI_API_KEY"] = openai_key

    # Initialize models with OpenAI
    llm = OpenAI(model="gpt-3.5-turbo")
    embedding_model = OpenAIEmbedding(model="text-embedding-ada-002")

    # Load and process documents
    nodes = load_and_process_documents(file_path, embedding_model, parser_type)

    # Create query engines and tools
    vector_tool, summarizer_tool = create_query_engines(nodes, llm, embedding_model)

    # Configure and return the query engine
    query_engine = RouterQueryEngine.from_defaults(
        [vector_tool, summarizer_tool],
        select_multi=True,
        verbose=True
    )
    return query_engine

def load_and_process_documents(file_path: str, embedding_model, parser_type='semantic'):
    """Load documents and process them into nodes."""
    documents = SimpleDirectoryReader(input_files=[file_path]).load_data()

    if parser_type == 'semantic':
        parser = SemanticSplitterNodeParser(
            buffer_size=1,
            breakpoint_percentile_threshold=97,
            embed_model=embedding_model
        )
    elif parser_type == 'sentence':
        parser = SentenceSplitter(chunk_size=1024)
    else:
        raise ValueError(f"Invalid parser_type: {parser_type}. Choose 'semantic' or 'sentence'.")

    nodes = parser.get_nodes_from_documents(documents)
    return nodes

def create_query_engines(nodes, llm, embedding_model):
    """Create vector and summarizer query engines."""
    vector_index = VectorStoreIndex(nodes, embed_model=embedding_model)
    summary_index = SummaryIndex(nodes)

    vector_query_engine = vector_index.as_query_engine(llm=llm)
    summary_query_engine = summary_index.as_query_engine(
        response_mode="tree_summarize",
        use_async=True,
        llm=llm
    )

    vector_tool = QueryEngineTool.from_defaults(
        query_engine=vector_query_engine,
        description="Retrieves specific context from the documents."
    )

    summarizer_tool = QueryEngineTool.from_defaults(
        query_engine=summary_query_engine,
        description="Provides document summarization."
    )

    return vector_tool, summarizer_tool

def clean_temp_directory(session_id):
    """Clean up the temporary directory for a session."""
    temp_dir = f"./temp/{session_id}"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
