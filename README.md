# 🐞 BugBase

### AI-Powered Software Bug Retrieval & Solution Recommendation System

BugBase is an **Information Retrieval (IR)-based system** that helps programmers find relevant solutions to software bugs using a structured knowledge base.

Instead of relying only on exact keyword matching, BugBase processes the user's query, expands relevant terms, retrieves candidate bugs, calculates similarity, and ranks the most relevant solutions.

---

## ✨ Features

- 🔎 Natural-language bug search
- 🧹 Text preprocessing
- 🔄 Query expansion
- 📚 Inverted index
- 📊 TF-IDF retrieval
- 📐 Cosine similarity
- 🏆 Relevance-based ranking
- 💡 Best solution recommendation
- 🤖 AI-assisted bug explanation
- 📈 Retrieval evaluation
- 💻 Interactive Streamlit UI

---

## 🧠 How It Works

User Query
    ↓
Text Preprocessing
    ↓
Query Expansion
    ↓
Inverted Index
    ↓
Candidate Retrieval
    ↓
TF-IDF
    ↓
Cosine Similarity
    ↓
Relevance Ranking
    ↓
Recommended Solution
    ↓
AI Assistant


📚 Dataset

BugBase currently contains 150 software bug records covering programming errors across languages such as:
Java
Python
C
C++
Web Development

Each record contains information such as:
BugID | ErrorName | Language | Description | Cause | Solution | Keywords

Dataset:
data/bugs.csv

🛠️ Tech Stack
Python
Streamlit
SQLite
Pandas
Scikit-learn
Information Retrieval
Git & GitHub


📁 Project Structure
BugBase/
│
├── app.py
├── ai_assistant.py
├── preprocessing.py
├── database.py
├── inverted_index.py
├── query_expansion.py
├── retrieval.py
├── evaluation.py
├── requirements.txt
│
├── data/
│   └── bugs.csv
│
└── database/
    └── bugs.db

🚀 Run Locally
1. Clone
git clone https://github.com/Ananyanaik24/BugBase.git
cd BugBase
2. Install dependencies
pip install -r requirements.txt
3. Run
streamlit run app.py

🔬 Research Direction
BugBase can be extended into a research project by comparing different retrieval approaches such as:

TF-IDF
   ↓
TF-IDF + Query Expansion
   ↓
Semantic Retrieval
   ↓
Hybrid Retrieval
These approaches can be evaluated using metrics such as Precision, Recall, F1-score, MRR, and Precision@K.

👩‍💻 Author
Ananya Naik
Computer Engineering
