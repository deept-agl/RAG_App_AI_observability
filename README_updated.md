# Snowflake AI Observability for Agentic Applications

Build an agentic RAG application in Snowflake, evaluate its quality, and use TruLens to observe and improve it before production.

## Project Goal

A working AI application is not automatically production ready.

This project demonstrates a simple production-readiness flow:

**Build → Observe → Evaluate → Compare → Improve → Deploy**

The use case is a clinical study RAG application built on RECOVERY trial documents.

---

## Part 1: Build the Agentic Application

The source documents are uploaded to Snowflake, parsed, chunked, indexed with Cortex Search, and used by the RAG application.

```text
Clinical Study PDFs
        ↓
Snowflake Stage
        ↓
PARSE_DOCUMENT
        ↓
Chunking
        ↓
Cortex Search
        ↓
Cortex LLM
        ↓
Agentic RAG Application
```

A curated evaluation dataset containing `QUERY` and `GROUND_TRUTH_RESPONSE` is also prepared for testing the application.

---

## Part 2: AI Observability with TruLens

The same application is instrumented with TruLens and evaluated across two versions:

```text
baseline_v1
top_k = 3
Basic prompt
```

```text
grounded_v2
top_k = 4
Strict grounding prompt
```

We inspect execution traces and compare the application using the RAG Triad:

- **Context Relevance**: Did retrieval find the right information?
- **Groundedness**: Is the answer supported by the retrieved context?
- **Answer Relevance**: Does the response answer the user's question?

---

## Repository Structure

```text
RAG_App_AI_observability/
│
├── .snowflake/
│   ├── .folder
│   └── settings.json
│
├── 00_setup/
│   ├── .folder
│   └── setup.sql
│
├── 01_AI_Observability/
│   ├── .folder
│   ├── CLINICAL_STUDY_OBSERVABILITY.ipynb
│   └── requirements.txt
│
├── STREAMLIT_APP/
│   ├── .streamlit/
│   ├── .folder
│   ├── 03_STREAMLIT_APP.py
│   ├── pyproject.toml
│   └── snowflake.yml
│
├── source files/
│   └── Clinical_study pdf files/
│
├── Eval_dataset_recovery_clinical_study.csv
├── cleanup_rag_app.sql
└── README.md
```

---

## Run the Project

### 1. Setup Snowflake Objects

Run:

```text
00_setup/setup.sql
```

This creates the required database, schemas, warehouse, stages, parsed-document objects, chunks, Cortex Search service, and evaluation table.

### 2. Upload Source Documents

Upload the clinical study PDFs from:

```text
source files/Clinical_study pdf files/
```

to the Snowflake document stage created by the setup script.

### 3. Load the Evaluation Dataset

Use:

```text
Eval_dataset_recovery_clinical_study.csv
```

to populate the evaluation table used by the observability runs.

### 4. Run AI Observability Notebook

Open and run:

```text
01_AI_Observability/CLINICAL_STUDY_OBSERVABILITY.ipynb
```

The notebook:

- Builds baseline and grounded application versions
- Adds TruLens instrumentation
- Registers application versions
- Runs the evaluation dataset
- Captures retrieval and generation traces
- Computes RAG Triad metrics
- Compares application quality

### 5. Run the Streamlit Application

The Streamlit files are available under:

```text
STREAMLIT_APP/
```

Main application:

```text
STREAMLIT_APP/03_STREAMLIT_APP.py
```

### 6. Review Evaluations

In Snowsight, navigate to:

```text
AI & ML → Evaluations
```

Review:

- Application versions
- Evaluation runs
- Execution traces
- Retrieved context
- Generated responses
- RAG Triad metrics
- Version comparisons

### 7. Cleanup

To remove the project objects, run:

```text
cleanup_rag_app.sql
```

---

## Tech Stack

- Snowflake
- Snowflake Cortex AI
- Cortex Search
- `PARSE_DOCUMENT`
- Snowpark Python
- TruLens
- Snowflake AI Observability
- Streamlit

---

## Key Takeaway

Instead of:

```text
Build → Demo → Deploy
```

Use:

```text
Build → Observe → Evaluate → Improve → Deploy
```

The goal is to understand and improve an AI application before taking it to production.

---

## Video Series

**Part 1:** Build the Agentic Application  
YouTube: `[ADD PART 1 LINK]`

**Part 2:** AI Observability with TruLens  
YouTube: `[ADD PART 2 LINK]`

---

## Connect

YouTube: https://youtube.com/@DeeptiBuilds  
LinkedIn: https://linkedin.com/in/deeptiagrawal29  
GitHub: https://github.com/deept-agl  
Medium: https://medium.com/@deepti.agl2912

---

## Disclaimer

This project is for learning and demonstration purposes only. The clinical study content should not be used for medical advice or clinical decision-making.
