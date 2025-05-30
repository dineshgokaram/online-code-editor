# 🖥️ Online Code Editor

An online code editor built using **React (frontend)** and **FastAPI (backend)** that allows users to write and execute code in multiple programming languages such as **Python** and **JavaScript**. The frontend is deployed on **Vercel** and the backend is hosted on **Render**.

---

## 🚀 Live Demo

- **Frontend**: [https://online-code-editor-zge3-git-main-dineshgokarams-projects.vercel.app](https://online-code-editor-zge3-git-main-dineshgokarams-projects.vercel.app)  
- **Backend**: [https://online-code-editor-tree-main-backend.onrender.com](https://online-code-editor-tree-main-backend.onrender.com)

---

## 🛠 Tech Stack

### Frontend
- React
- Tailwind CSS (optional, if used)
- Fetch API for backend integration
- Vercel for deployment

### Backend
- FastAPI
- Pydantic
- Subprocess (to execute code safely)
- Render for deployment

---

## ✨ Features

- 🔤 Language selection (e.g., Python, JavaScript)
- 🧑‍💻 Real-time code input
- 🟢 Runs code and displays output
- ⚙️ FastAPI backend with code execution logic
- 🌐 Fully deployed & accessible online

---

## 📁 Project Structure

### `/frontend`
- React app
- Code editor interface
- Language dropdown
- Send code to backend using `POST /run`

### `/backend`
- FastAPI app
- Accepts `POST` request at `/run`
- Executes code in selected language
- Returns stdout and stderr as JSON

---

## 🧪 How to Run Locally

### Frontend
```bash
cd frontend
npm install
npm run dev


Screenshots----------------------------------------------------------------

![Screenshot 2025-05-30 110050](https://github.com/user-attachments/assets/0264d20e-d29c-43ed-a0da-30dc111d4060)
