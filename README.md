# Academic CS Assistant (Study Hub)

An advanced, AI-powered web application specifically designed to assist B.Tech Computer Science students with academic queries, quizzes, and coding tasks. This application leverages the ultra-fast **Groq API** and features a modern, **Grid-based Glassmorphism UI**.

The project implements a clean separation of concerns between the FastAPI backend and the Vanilla JS frontend, ensuring high performance and a professional user experience.

---

## 🚀 Key Features

### 🎓 Academic Chat Engine
Context-aware conversational AI with dedicated study modes:
*   **Detailed Study**: Comprehensive explanations of CS concepts with real-world examples and analogies.
*   **Quick Review**: Precise summaries for last-minute revisions and core concept recaps.
*   **Exam Practice**: Mock questions, strategic answer structures, and critical thinking exercises.

### 📝 Quiz Master (Assessment Engine)
Dynamic generator that creates high-quality assessments tailored to your syllabus:
*   **Types**: Multiple Choice (MCQ), Theoretical (Open-ended), and Coding Challenges.
*   **Difficulty**: Introductory (Easy), Intermediate (Medium), and Advanced (Hard).
*   **Customization**: Specify topics (e.g., "CPU Scheduling") and question counts.

### 💻 Code Helper
A specialized software engineering assistant for generating, debugging, and optimizing code:
*   **Broad Support**: Supports 15+ languages including Python, JavaScript, TypeScript, Java, C++, Go, Rust, SQL, Bash, and more.
*   **Use Cases**: Algorithm implementation, boilerplate generation, and logic optimization.

### 💾 Persistent Sessions & History
*   **Session Management**: Automatically saves chat history using an **SQLite** database.
*   **Continuity**: Resume past conversations from the sidebar, synced via `localStorage`.

### 📄 Professional PDF Export
*   **High Contrast**: Specially designed "PDF Mode" ensures clean, black-and-white exports perfect for printing or offline study.
*   **Panel Export**: Export chat logs, quizzes, or code snippets independently.

### 🌓 Theme & UI
*   **Modern Aesthetic**: A sleek, grid-based layout with zero rounded corners for a professional, technical look.
*   **Dark Mode**: Native support for a seamless dark/light mode toggle with persistent theme settings.

---

## 📁 Project Structure

```text
INT428-Chatbot-Project/
│
├── backend/                  # FastAPI Backend Server
│   ├── main.py               # API endpoints and entry point (Uvicorn)
│   ├── database.py           # SQLite models and session persistence
│   ├── groq_client.py        # Groq API integration (LLM Inference)
│   ├── prompts.py            # Specialized System Prompts (Academic, Quiz, Code)
│   └── chats.db              # SQLite Database (auto-generated)
│
├── frontend/                 # Vanilla HTML/JS/CSS Frontend
│   └── index.html            # Single-page Application UI
│
├── .env                      # Environment Variables (API Keys)
├── requirements.txt          # Python dependencies
├── package.json              # Project Metadata
└── README.md                 # Project Documentation
```

---

## 🛠️ Tech Stack

### Frontend
*   **HTML5 / CSS3**: Responsive layout with a grid-based minimalist aesthetic.
*   **JavaScript (ES6+)**: Vanilla JS for state management and DOM manipulation.
*   **[marked.js](https://marked.js.org/)**: Renders AI-generated Markdown with precision.
*   **[html2pdf.js](https://ekoopmans.github.io/html2pdf.js/)**: Handles high-fidelity PDF generation.

### Backend
*   **Python 3.10+**: Core backend logic.
*   **[FastAPI](https://fastapi.tiangolo.com/)**: High-performance REST framework.
*   **[Groq SDK](https://groq.com/)**: Blazing-fast LLM inference (Llama 3 / Mixtral).
*   **SQLite**: Lightweight relational database for persistent chat logs.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/chat` | Standard academic conversation based on study mode. |
| `POST` | `/quiz` | Generates a structured quiz based on syllabus and type. |
| `POST` | `/code` | Generates programming solutions for a specific task. |
| `GET` | `/sessions` | Fetches a list of all historical chat sessions. |
| `GET` | `/sessions/{id}` | Retrieves full message history for a specific session. |

---

## ⚙️ Installation & Setup

### 1. Prerequisites
*   **Python 3.8+** installed.
*   A **Groq API Key** (Get one at [console.groq.com](https://console.groq.com/)).

### 2. Clone & Install
```bash
git clone https://github.com/Tanvi566/INT428-Chatbot-Project.git
cd INT428-Chatbot-Project
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=gsk_your_key_here
```
> [!NOTE]
> Alternatively, you can paste your key directly into `backend/main.py` at **line 30**.

### 4. Run the Application
**Start the Backend:**
```bash
cd backend
python main.py
```
*The API will be live at `http://localhost:8000`.*

**Launch the Frontend:**
Simply open `frontend/index.html` in your browser.

---

## 📖 Usage Tips
*   **New Session**: Use the "+ New Session" button to start a fresh topic and keep your history organized.
*   **Mode Switching**: Switch to "Exam Practice" before tests for harder, assessment-style responses.
*   **PDF Formatting**: Use the "PDF" button at the top right of each panel for a professional export.

---

## 👤 Author
**Tanvi (CSE)**