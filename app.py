import streamlit as st
from rag_engine import load_base,ask_rag
st.set_page_config(page_title = "SIET_multi_Chatbot",layout = 'centered')
st.title("Explore SIET with Chatbot")
st.caption("Ask anything about college information,Courses,Placements,FAQs,Rules and regulation...")
st.caption("RAG Pipeline with Multiple files")
st.caption("Developed by Akshata Ganesh")

mykey = st.secrets["GROQ_API_KEY"]

@st.cache_resource
def initiate_rag():
  return load_base("ISRO_data_docs")
index,embed_model,chunks = initiate_rag()

if "chat_hist" not in st.session_state:
  st.session_state.chat_hist = []

# NEW (1): remember which sidebar button was clicked
if "sidebar_view" not in st.session_state:
  st.session_state.sidebar_view = None

# NEW (2): sidebar with two buttons
with st.sidebar:
  st.header("Menu")
  if st.button("RAG Pipeline",use_container_width = True):
    st.session_state.sidebar_view = "rag"
  if st.button("Information",use_container_width = True):
    st.session_state.sidebar_view = "info"
  st.divider()

  # NEW (3): content shown when "RAG Pipeline" is clicked
  if st.session_state.sidebar_view == "rag":
    st.subheader("RAG Pipeline")
    st.markdown("""
**1. Load PDFs**
Text is read from all PDFs in the folder using pypdf.

**2. Chunking**
Text is split into chunks of 500 characters with 100 overlap.

**3. Embedding**
Each chunk is converted to a vector using all-MiniLM-L6-v2.

**4. Vector Store**
Vectors are stored in a FAISS index (cosine similarity).

**5. Retrieval**
Your question is embedded and the top 3 similar chunks are fetched.

**6. Generation**
The chunks and question go to the Groq LLM, which answers only from the documents.
""")

  # NEW (4): content shown when "Information" is clicked
  elif st.session_state.sidebar_view == "info":
    st.subheader("Information")
    st.markdown("""
**Topic 1** : (will add)

**Topic 2** : (will add)

**Topic 3** : (will add)
""")

for qa in   st.session_state.chat_hist :
  with st.chat_message(qa["role"]):
    st.write(qa["content"])

question = st.chat_input("Ask anything about SIET college....")

if question :
  st.session_state.chat_hist.append(
    {"role":"user","content":question})
  with st.chat_message("user"):
    st.write(question)
  with st.chat_message("assistant"):
    with st.spinner("Asking RAG for Answer...."):
      answer = ask_rag(question,embed_model,chunks,index,api_key = mykey)
      st.write(answer)
    st.session_state.chat_hist.append(
    {"role":"assistant","content":answer})

if st.button("Clear chat"):
  st.session_state.chat_hist = []
  st.rerun()
