# 🔮 EduVision AI: Advanced Multi-Agent Multimodal Education System

**EduVision AI** is a state-of-the-art educational platform built with **Agentic AI** principles. It uses a swarm of specialized agents to research, write, visualize, and assess any topic in real-time.

![EduVision Banner](https://img.shields.io/badge/Agentic%20AI-Multimodal-purple?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-121212?style=for-the-badge&logo=Chainlink&logoColor=white)

## 🚀 Key Features
- **🕵️ Agentic Research**: Real-time web searching via DuckDuckGo to provide current data.
- **🎴 Multimodal Flashcards**: Generates high-quality AI images for every concept using **Pollinations AI**.
- **⚡ Parallel Processing**: Generates 5+ images simultaneously, reducing response time by 5x.
- **☁️ Cloud Semantic Memory**: Uses **Upstash Vector DB** to store and retrieve knowledge globally.
- **🧠 Automated Assessments**: Logic-based quizzes with instant feedback for better learning.
- **🌌 Premium Nebula UI**: A sleek, dark-themed interface with purple glow aesthetics.

---

## 🛠️ Tech Stack
- **AI Orchestration**: LangChain
- **LLM**: Llama 3.3 70B (via Groq Cloud)
- **Vector Database**: Upstash Vector (Cloud)
- **Frontend**: Streamlit
- **Image Generation**: Pollinations AI (Stable Diffusion)
- **Local DB**: TinyDB (for session history)

---

## 💻 Setup Instructions (For Friends)

If you want to run this project on your own machine, follow these steps:

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/EduAgent-AI.git
cd EduAgent-AI
```

### 2. Create a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
Create a file named `.env` in the root directory and add your API keys:
```env
GROQ_API_KEY=your_groq_api_key
HF_TOKEN=your_huggingface_token

# Upstash Vector DB (Create a free index on Upstash)
UPSTASH_VECTOR_REST_URL=your_upstash_url
UPSTASH_VECTOR_REST_TOKEN=your_upstash_token
```

### 5. Run the Application
```bash
streamlit run app.py
```

---

## 📁 Project Structure
- `app.py`: Main Streamlit application and UI logic.
- `education_agent/`: Core AI engine.
  - `agents/`: Researcher, Writer, Flashcard, and Quiz agents.
  - `utils/`: Image generation and parallel processing logic.
- `database.py`: Logic for Cloud Vector DB and local history.
- `auth.py`: User authentication system.


---

**Developed for Medicaps University – Datagami Skill Based Course (2026)**