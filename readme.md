# Doc-to-Action Assistant
### Grounded Document Q&A and Workflow Tooling using Gemini

Doc-to-Action Assistant is a command-line tool that ingests documents (PDFs), retrieves relevant sections, and uses a Gemini model to generate grounded answers and actionable outputs.

The system demonstrates a practical **ML engineering workflow**, including document ingestion, retrieval-augmented generation (RAG), and tool-based automation such as extracting requirements, generating checklists, and producing structured issue payloads.

The goal of the project is to explore how LLM-based systems can help convert unstructured documents into actionable insights while maintaining **traceability and grounded responses**.

---

# Key Features

### Document Ingestion
- Extracts text from PDFs
- Splits content into manageable chunks
- Stores chunks for retrieval

### Retrieval-Augmented Generation (RAG)

Instead of allowing the model to answer freely, the assistant:

1. Retrieves relevant document chunks
2. Sends those chunks as context to the model
3. Forces answers to cite document sources

This approach helps reduce hallucinations and improves explainability.

---

### Grounded Question Answering

Users can ask questions about the document and receive answers that reference specific document sections.

Example:

```
ask summarize the responsibilities described in this document
```

Example Output:

```
The document outlines several responsibilities including maintaining compliance with internal policies, submitting required documentation within specified timelines, and cooperating with internal review procedures [chunk-3][chunk-5].

Sources:
chunk-3
chunk-5
```

---

### Tool-Based Actions

The assistant includes specialized tools powered by the LLM.

#### Extract Requirements

```
extract reporting requirements
```

Returns structured bullet points of requirements identified in the document.

---

#### Generate Checklist

```
checklist onboarding steps
```

Converts document requirements into a structured checklist.

---

#### Create Issue Payload

```
issue create a high priority issue for unclear approval requirements
```

Returns a structured JSON issue payload.

Example:

```json
{
  "title": "Ambiguous approval process in document",
  "priority": "High",
  "summary": "The document references approval requirements but does not clearly define responsible parties.",
  "acceptance_criteria": [
    "Clarify approval authority in the document",
    "Define approval workflow steps",
    "Update documentation to remove ambiguity"
  ],
  "citations": ["chunk-4"]
}
```

---

# Architecture

```
PDF Document
     │
     ▼
Text Extraction (pypdf)
     │
     ▼
Chunking
     │
     ▼
Vectorization (TF-IDF)
     │
     ▼
Retrieval Engine
     │
     ▼
Gemini LLM
     │
     ▼
Grounded Answer or Tool Action
```

---

# Main Components

| Component | Responsibility |
|-----------|---------------|
| `pdf.py` | Extract text from PDF |
| `text.py` | Chunk documents |
| `store.py` | Vector store using TF-IDF |
| `retrieve.py` | Retrieve relevant chunks |
| `gemini_client.py` | Gemini API interaction |
| `tools/` | Document-driven automation tools |
| `main.py` | CLI interface |

---

# Installation

Clone the repository.

```
git clone <repository-url>
cd doc-to-action-assistant
```

Create a virtual environment.

```
python -m venv .venv
```

Activate the environment.

Windows

```
.venv\Scripts\activate
```

Mac/Linux

```
source .venv/bin/activate
```

Install dependencies.

```
pip install -r requirements.txt
```

---

# Configuration

Create a `.env` file.

```
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=models/gemini-2.5-flash
```

---

# Running the Assistant

```
python -m app.main
```

You will be prompted to provide a PDF path.

Example:

```
Enter PDF path: data/sample.pdf
```

---

# CLI Commands

| Command | Description |
|--------|-------------|
| `ask <question>` | Ask a grounded question about the document |
| `extract <topic>` | Extract requirements related to a topic |
| `checklist <topic>` | Generate a checklist |
| `issue <request>` | Create a structured issue payload |
| `help` | Show available commands |
| `exit` | Exit the assistant |

Example session:

```
doc-assistant> ask summarize the obligations described in this document
doc-assistant> extract compliance requirements
doc-assistant> checklist compliance steps
doc-assistant> issue create issue for missing documentation guidance
```

---

# Example Use Cases

Although this project is domain-agnostic, it can support workflows such as:

- analyzing policies or contracts
- extracting compliance obligations
- summarizing technical documentation
- generating operational checklists
- identifying potential documentation gaps
- creating issue tickets based on document findings

---

# Design Considerations

### Grounded Responses
The system requires the model to answer using only retrieved document content.

### Retrieval First
All queries retrieve relevant document chunks before invoking the model.

### Tool-Driven Automation
The assistant supports structured workflows beyond simple question answering.

### Explainability
Answers include citations so users can trace results back to the source text.

---

# Potential Production Improvements

If deployed as a production system, the following improvements could be implemented:

- authentication and access control
- document versioning
- persistent vector database storage
- automated evaluation datasets
- hallucination detection
- PII redaction
- embedding caching
- latency monitoring
- rate limiting
- multi-document retrieval

---

# Technologies Used

- Python
- Gemini API
- Scikit-learn
- TF-IDF vectorization
- PyPDF
- dotenv

---

# Project Motivation

This project was created to explore **practical ML engineering patterns**, including:

- Retrieval-Augmented Generation
- grounded LLM responses
- tool orchestration
- transforming unstructured documents into actionable insights

The focus is not just using an LLM, but building **reliable systems around models** that support real operational workflows.

---

# License

This project is provided for educational and demonstration purposes.