import streamlit as st
from rag_engine import load_base,ask_rag

# NEW (1): page title and browser tab icon
st.set_page_config(page_title = "ISRO Chatbot",page_icon = "🚀",layout = 'centered')

# NEW (2): main title and captions
st.title("🚀 ISRO Space Assistant")
st.caption("🛰️ Ask anything about ISRO missions, satellites, launch vehicles, and space research...")
st.caption("📚 RAG Pipeline with Multiple Documents")
st.caption("👨‍🚀 Developed by Team Vyoma")

mykey = st.secrets["GROQ_API_KEY"]

@st.cache_resource
def initiate_rag():
  return load_base("ISRO_data_docs")
index,embed_model,chunks = initiate_rag()

if "chat_hist" not in st.session_state:
  st.session_state.chat_hist = []

if "sidebar_view" not in st.session_state:
  st.session_state.sidebar_view = None

# NEW (3): icons for chat messages
avatars = {"user":"🧑‍🚀","assistant":"🛰️"}

with st.sidebar:
  st.header("📌 Menu")
  # NEW (4): icons on the sidebar buttons
  if st.button("⚙️ RAG Pipeline",use_container_width = True):
    st.session_state.sidebar_view = "rag"
  if st.button("ℹ️ Information",use_container_width = True):
    st.session_state.sidebar_view = "info"
  st.divider()

  if st.session_state.sidebar_view == "rag":
    st.subheader("⚙️ RAG Pipeline")
    # NEW (5): icons on each pipeline step
    st.markdown("""
**📄 1. Load PDFs**
Text is read from all ISRO PDFs in the folder using pypdf.

**✂️ 2. Chunking**
Text is split into chunks of 500 characters with 100 overlap.

**🧠 3. Embedding**
Each chunk is converted to a vector using all-MiniLM-L6-v2.

**🗄️ 4. Vector Store**
Vectors are stored in a FAISS index (cosine similarity).

**🔍 5. Retrieval**
Your question is embedded and the top 3 similar chunks are fetched.

**💬 6. Generation**
The chunks and question go to the Groq LLM, which answers only from the documents.
""")

  elif st.session_state.sidebar_view == "info":
    st.subheader("ℹ️ Information")

    # NEW (6): icons on the three topics
    st.markdown("**🚀 1. Project Information**")
    st.write("ISRO Space Assistant is a RAG based chatbot that answers questions about ISRO using the uploaded PDF documents.")

    st.markdown("**📝 2. Description**")
    st.write("The chatbot reads multiple ISRO PDFs, splits them into chunks, converts them to embeddings, and stores them in FAISS. For each question it retrieves the 3 most relevant chunks and sends them to the Groq LLM, which answers only from those documents.")

    st.markdown("**👥 3. Team Members**")
    st.write("🌟 Akshata Ganesh")
    st.write("🌟 Member name 2")
    st.write("🌟 Member name 3")

# NEW (7): avatar added to the chat history display
for qa in   st.session_state.chat_hist :
  with st.chat_message(qa["role"],avatar = avatars[qa["role"]]):
    st.write(qa["content"])

# NEW (8): placeholder updated for ISRO
question = st.chat_input("Ask anything about ISRO....")

if question :
  st.session_state.chat_hist.append(
    {"role":"user","content":question})
  with st.chat_message("user",avatar = avatars["user"]):
    st.write(question)
  with st.chat_message("assistant",avatar = avatars["assistant"]):
    with st.spinner("🛰️ Searching ISRO documents...."):
      answer = ask_rag(question,embed_model,chunks,index,api_key = mykey)
      st.write(answer)
    st.session_state.chat_hist.append(
    {"role":"assistant","content":answer})

# NEW (9): icon on the clear button
if st.button("🗑️ Clear chat"):
  st.session_state.chat_hist = []
  st.rerun()
