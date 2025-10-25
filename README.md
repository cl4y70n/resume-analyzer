# 🧠 Resume Analyzer – AI-Powered Resume Ranking System

## 📄 Overview

**Resume Analyzer** is an intelligent system that analyzes and ranks resumes based on relevance, skills, and job fit.
It leverages **Hugging Face**, **LangChain**, and **LangGraph** to extract and evaluate key competencies, providing an automatic ranking and exporting the results into a spreadsheet for HR teams.

---

## 🚀 Key Features

* ⚙️ **Automatic Resume Ranking** – Scores resumes based on alignment with the job description.
* 🧩 **Skill Extraction (NER)** – Identifies key competencies, experience levels, and relevant entities.
* 📊 **Export to Spreadsheet** – Automatically exports results in `.xlsx` format.
* 🧠 **AI Integration** – Uses pre-trained NLP models for semantic understanding of resumes.
* 🧾 **Job Queue with Celery** – Handles heavy processing asynchronously.
* 🔐 **API Authentication** – Secure endpoints using API keys.
* 🐳 **Dockerized Setup** – Ready for deployment via Docker & Docker Compose.

---

## 🏗️ Project Architecture

```
resume-analyzer/
│
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI entry point
│   ├── models.py               # Data models and schema definitions
│   ├── utils/
│   │   ├── ranker.py           # Resume ranking logic
│   │   ├── skill_extractor.py  # Skill extraction using NER
│   │   ├── exporter.py         # Excel export logic
│   │   └── config.py           # Environment and model configuration
│   ├── routes/
│   │   └── resumes.py          # API endpoints
│   └── celery_worker.py        # Celery background task handler
│
├── data/                       # Test resumes and output exports
│   ├── resumes/
│   └── results/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── README.md
└── tests/
    └── test_api.py
```

---

## ⚙️ Technologies

| Category             | Stack                                           |
| -------------------- | ----------------------------------------------- |
| **Backend**          | FastAPI                                         |
| **AI Models**        | Hugging Face Transformers, LangChain, LangGraph |
| **Async Processing** | Celery + Redis                                  |
| **Export**           | Pandas, OpenPyXL                                |
| **Containerization** | Docker, Docker Compose                          |
| **Auth**             | API Key middleware                              |

---

## 🧠 How It Works

1. **Upload resumes** (PDF, DOCX, or TXT).
2. The system extracts **entities and skills** using NLP (Named Entity Recognition).
3. It compares the extracted skills with the **job description** or required skills list.
4. Each resume receives a **relevance score**.
5. Results are **ranked** and **exported** to a spreadsheet for easy review.

---

## 🧩 Setup and Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/resume-analyzer.git
cd resume-analyzer
```

### 2️⃣ Configure environment variables

Create a `.env` file:

```bash
API_KEY=your_api_key_here
HF_MODEL=neuralmind/bert-base-portuguese-cased
REDIS_URL=redis://redis:6379/0
```

### 3️⃣ Build and run the project

```bash
docker-compose up --build
```

The API will be available at:
👉 `http://localhost:8000/docs`

---

## 🧾 API Endpoints

| Method | Endpoint               | Description                               |
| ------ | ---------------------- | ----------------------------------------- |
| `POST` | `/api/resumes/upload`  | Upload resumes (5–10 test samples)        |
| `POST` | `/api/resumes/analyze` | Start asynchronous resume analysis        |
| `GET`  | `/api/resumes/results` | Retrieve ranked resumes                   |
| `GET`  | `/api/export`          | Download ranked results in `.xlsx` format |

---

## 🔑 Authentication

Include the following header in every request:

```
x-api-key: your_api_key_here
```

---

## 🔧 Example Request

```bash
curl -X POST "http://localhost:8000/api/resumes/analyze" \
-H "x-api-key: your_api_key_here" \
-F "files=@data/resumes/candidate1.pdf" \
-F "files=@data/resumes/candidate2.pdf"
```

---

## 📊 Example Output (Excel)

| Candidate  | Score | Matched Skills       | Missing Skills |
| ---------- | ----- | -------------------- | -------------- |
| John Doe   | 92%   | Python, NLP, FastAPI | None           |
| Jane Smith | 78%   | Machine Learning     | LangChain      |

---

## 🧪 Testing

Run the test suite:

```bash
pytest -v
```

---

## ☁️ Deployment Options

* GitHub + DockerHub (CI/CD)
* AWS ECS / Google Cloud Run / Railway.app
* Can be extended with a React or Next.js frontend

---

## 🧭 Future Improvements

* 🔍 Add multilingual support (EN, PT, ES)
* 🤖 Train a fine-tuned NER model for resumes
* 🗃️ Add vector database (ChromaDB/Pinecone) for semantic search
* 📈 Dashboard with analytics and filtering
* 🔐 OAuth2 / JWT authentication

---

## 🧑‍💼 Author

**Developed by:** AI Engineer Clayton
**Tech Stack:** Python · FastAPI · LangChain · Hugging Face · Docker

