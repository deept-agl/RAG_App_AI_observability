import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.core import Root
from snowflake.cortex import Complete

DB = "CLINICAL_STUDY_AI_DB"
SCHEMA = "RAG"
SEARCH_SERVICE = "CLINICAL_STUDY_SEARCH_SERVICE"
MODEL = "mistral-large2"
TOP_K = 4

session = get_active_session()
root = Root(session)

st.set_page_config(page_title="Clinical Study Assistant", page_icon="🧪", layout="wide")
st.title("🧪 Clinical Study Information Assistant")
st.caption(
    "Answers are grounded only in the selected RECOVERY trial documents. "
    "This app provides study information and does not provide medical advice."
)

@st.cache_resource
def get_search_service():
    return (
        root.databases[DB]
        .schemas[SCHEMA]
        .cortex_search_services[SEARCH_SERVICE]
    )

def retrieve_context(question):
    response = get_search_service().search(
        query=question,
        columns=["CHUNK", "FILE_NAME", "DOCUMENT_TYPE", "CHUNK_INDEX"],
        limit=TOP_K
    )
    return response.results or []

def generate_answer(question, results):
    context = "\n\n".join(
        f"[Source {i+1}: {r.get('FILE_NAME', 'Unknown')}]\n{r.get('CHUNK', '')}"
        for i, r in enumerate(results)
    )
    prompt = f"""
You are a clinical study information assistant.

Use only the supplied RECOVERY trial document context.
Do not use outside medical knowledge.
Do not provide medical advice.
If the answer is unsupported, respond:
"I could not find this information in the selected study documents."

Give a concise answer and end with the relevant source file names.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""
    return Complete(MODEL, prompt, session=session)

with st.sidebar:
    st.subheader("Configuration")
    st.write("**Dataset:** RECOVERY clinical study")
    st.write("**Documents:** 5 PDFs")
    st.write(f"**Model:** {MODEL}")
    st.write(f"**Retrieved chunks:** {TOP_K}")
    show_context = st.toggle("Show retrieved context", value=True)

question = st.text_input(
    "Ask a question about the clinical study",
    placeholder="What conditions must a patient meet to participate?"
)

if st.button("Ask", type="primary", use_container_width=True, disabled=not question.strip()):
    with st.spinner("Searching documents..."):
        results = retrieve_context(question.strip())

    if not results:
        st.warning("No relevant context was found.")
    else:
        with st.spinner("Generating grounded response..."):
            answer = generate_answer(question.strip(), results)

        st.subheader("Answer")
        st.write(answer)

        if show_context:
            st.subheader("Retrieved evidence")
            for i, result in enumerate(results, 1):
                with st.expander(
                    f"{i}. {result.get('FILE_NAME', 'Unknown')} — "
                    f"{result.get('DOCUMENT_TYPE', 'Unknown')} — "
                    f"chunk {result.get('CHUNK_INDEX', '')}"
                ):
                    st.write(result.get("CHUNK", ""))
