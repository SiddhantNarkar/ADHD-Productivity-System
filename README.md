# 🧠 ADHD Productivity System

An adaptive AI-powered productivity platform designed for individuals with ADHD. It provides an intelligent and personalized environment to improve focus, manage daily activities, and build productive habits.

### ✨ Key Features

- **Personalized Task Manager:** Create, organize, and manage daily tasks.
- **ADHD Prediction System:** AI-powered ADHD prediction and assessment support.
- **Gamified Assessments:** Interactive assessments and games to make evaluation engaging.
- **Real-Time Messaging:** Communicate with other users through real-time messaging.
- **Reward Mechanism:** Earn points and rewards for completing tasks and activities.
- **AI Chatbot:** An intelligent chatbot that provides motivation, guidance, and productivity support.

---

# 🚀 Project Installation Guide

Follow the steps below to set up and run the project on your local system.

## 📋 Prerequisites

Make sure you have installed the following software:

- Python
- Git
- PyCharm Community Edition (or any preferred code editor)
- Ollama

## ⚙️ Step-by-Step Installation

### Step 1: Clone the Repository

Open Git Bash or PowerShell in the folder where you want to store the project.

Run the following command:

```bash
git clone https://github.com/SiddhantNarkar/ADHD-Productivity-System.git
```

### Step 2: Navigate to the Project Directory

```bash
cd ADHD-Productivity-System
```

### Step 3: Open the Project

Open PyCharm or your preferred code editor and select the cloned project folder.

### Step 4: Create a Virtual Environment

Open the terminal inside the project directory and run:

```bash
python -m venv pyenv
```

### Step 5: Activate the Virtual Environment

For Windows PowerShell:

```powershell
.\pyenv\Scripts\Activate.ps1
```

For Windows Command Prompt:

```cmd
pyenv\Scripts\activate
```

### Step 6: Install Project Dependencies

Install all required Python packages using:

```bash
pip install -r requirements.txt
```

### Step 7: Run the Django Development Server

Start the project using:

```bash
python manage.py runserver
```

Open your browser and visit:

```text
http://127.0.0.1:8000/
```

To stop the development server, press:

```text
Ctrl + C
```

---

# 🤖 Ollama Setup (AI Chatbot)

The project uses Ollama to run the local AI model for chatbot functionality.

### Step 8: Download and Install Ollama

Visit the official Ollama website:

https://ollama.com

Download and install Ollama for your operating system.

### Step 9: Download the Phi-3 Model

Open your terminal and execute:

```bash
ollama pull phi3
```

This downloads the Phi-3 language model to your local system.

### Step 10: Start the Ollama Server

Run the following command:

```bash
ollama serve
```

Keep the Ollama server running while using the AI chatbot.

To stop the server, press:

```text
Ctrl + C
```

---

# 📁 Project Structure

The project contains the following major components:

- `adhd_prediction/` – ADHD prediction, assessments, and related application logic.
- `adhd_productivity_system/` – Main Django project configuration.
- `requirements.txt` – Python dependencies.
- `manage.py` – Django management utility.

---

# 🛠️ Technologies Used

- **Backend:** Python, Django
- **AI/ML:** Machine Learning, Ollama, Phi-3
- **Database:** SQLite (if configured as the project database)
- **Frontend:** HTML, CSS, JavaScript
- **Version Control:** Git and GitHub

---

# 👨‍💻 Author

**Siddhant Narkar**

GitHub: https://github.com/SiddhantNarkar

---

⭐ If you find this project interesting, feel free to explore the repository and share your feedback!
