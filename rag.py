import lancedb
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector
from dotenv import load_dotenv
from google import genai
from google.genai import types
from langchain_text_splitters import RecursiveCharacterTextSplitter
from llama_index.core import SimpleDirectoryReader

# load GEMINI API KEY
load_dotenv()

# create gemini client
client = genai.Client()

# connect to lancedb
db = lancedb.connect("./embeddings")
# set sentence-transformers model from registry
model = get_registry().get("sentence-transformers").create()

class DataStore(LanceModel):
    text: str = model.SourceField()
    vector: Vector(model.ndims()) = model.VectorField()

# create or get lancedb table, overwrite if exists
table = db.create_table("rag_test", schema=DataStore, mode="overwrite")

# load pdf documents from data_source folder
documents = SimpleDirectoryReader("./data_source").load_data()

# create text splitter
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
chunk_size=100, chunk_overlap=10,
)

# insert to lancedb table with auto-vectorization
for doc in documents:
    if doc.text:
        chunks = text_splitter.split_text(doc.text)
        # Prepare chunks for insertion
        data_list = [{"text": chunk} for chunk in chunks]
        table. add(data_list)

# command loop for chat stimulation
while True:
    query = input(": ")
    if query.lower() in ("stop","exit"):
        break
    
    relevant_context = table.search(query).limit(2).to_list()
    # create a single string from the relevant context
    context_joined = ','.join(context["text"] for context in relevant_context)
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
        system_instruction="You are an AI Assistant.Only Answer from given Context"),
        contents=f"""User : {query} 
                     Context:
                     {context_joined}
                     Answer : 
                 """
    )
    print(response.text)