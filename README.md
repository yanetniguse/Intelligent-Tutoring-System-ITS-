# Intelligent Tutoring System (ITS)

## 📌 Project Overview
The **Intelligent Tutoring System (ITS)** is an AI-powered learning platform that adapts to user performance. It provides personalized learning experiences using **adaptive difficulty**, **speech-to-text input**, and **real-time analytics**. The system tracks student progress and offers insights for improvement.

## 🚀 Features
✅ **Adaptive Learning** – Adjusts question difficulty based on user performance.  
✅ **Speech-to-Text Integration** – Users can answer using their voice.  
✅ **Multiple-Choice & Open-Ended Questions** – Supports different question types.  
✅ **Real-Time Performance Analytics** – Displays progress with interactive charts.  
✅ **Database Storage** – Saves student progress for future sessions.  
✅ **Web-Based Interface** – Runs on **Streamlit** for an intuitive experience.  

## 🛠️ Technologies Used
- **Python 3.13**
- **Streamlit** – Frontend UI
- **SQLite** – Database for storing student progress
- **SpeechRecognition & PyAudio** – Speech-to-text functionality
- **Matplotlib & Pandas** – Data visualization

## 📥 Installation Guide
### 1️⃣ Install Dependencies
Run the following command to install required libraries:
```bash
pip install streamlit sqlite3 pandas matplotlib speechrecognition pyaudio pipwin
pipwin install pyaudio
```

### 2️⃣ Run the Application
Start the tutor system using Streamlit:
```bash
streamlit run its-tutor.py
```

## 🖥️ How to Use
1. **Start the application** – The system will display a math question.
2. **Answer the question** – You can either:
   - **Type your answer** in the text input field.
   - **Use voice input** by clicking **"Use Speech-to-Text"**.
3. **Receive feedback** – The system will inform you if your answer is correct or incorrect.
4. **Track your performance** – View analytics on the sidebar.
5. **Continue answering questions** – The system will adjust difficulty based on your performance.

## 📊 Performance Analytics
- Your **correct and incorrect answers** are stored in a **SQLite database**.
- A **progress bar and analytics chart** provide real-time feedback on your learning.

## 🛠️ Troubleshooting
**Problem:** "Could not find PyAudio"
- Run: `pipwin install pyaudio`
- Restart your computer and try again.

**Problem:** "Speech-to-Text is not working"
- Ensure your **microphone is enabled** and **set as default**.
- Try typing the answer instead.

## 👥 Contributors
- **Your Name** - Developer
- **Professor/Group Name** (if applicable)

## 📜 License
This project is **open-source** under the MIT License.

## ⭐ Acknowledgments
Special thanks to **Austin Odera** for guidance and support!

