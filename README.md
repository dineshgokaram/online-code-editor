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

![Screenshot 2025-05-28 114929](https://github.com/user-attachments/assets/37d7d40f-432e-4a6b-b367-34b8ce05fe57)
![Screenshot 2025-05-28 193537](https://github.com/user-attachments/assets/98d1ef71-246b-45bf-ab33-aa1142c21240)
![Screenshot 2025-05-29 105241](https://github.com/user-attachments/assets/e1ef840f-ddad-496e-8256-9197b7e5d0fe)
![Screenshot 2025-05-29 112401](https://github.com/user-attachments/assets/f7de852b-c98b-4ccb-a329-0a7bb01b30df)
![Screenshot 2025-05-29 120444](https://github.com/user-attachments/assets/0b70d8a8-8635-43eb-90a9-33d8d3ef1dc6)
![Screenshot 2025-05-29 121029](https://github.com/user-attachments/assets/e478ac85-d14c-493e-8108-f9f3ba2ed87d)
![Screenshot 2025-05-30 110050](https://github.com/user-attachments/assets/cb749ae4-3d67-40ae-872f-0d8dd5fee68a)
![Screenshot 2025-05-30 212230](https://github.com/user-attachments/assets/b2914da1-5d1b-4e99-8ad9-3df6c38acc50)
![Screenshot 2025-05-30 212528](https://github.com/user-attachments/assets/b864a16c-05e5-4621-bab3-d0a9d42b5633)

