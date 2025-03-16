# Import necessary libraries
import streamlit as st  # For building the web-based user interface
import sqlite3  # For database operations to store student progress
import random  # For selecting random questions
import pandas as pd  # For handling data in tables
import matplotlib.pyplot as plt  # For plotting performance charts
import speech_recognition as sr  # For speech-to-text functionality
import sounddevice as sd  # For capturing audio input instead of PyAudio
import numpy as np  # For processing audio data


# --------------------------- INITIALIZE SESSION STATE --------------------------- #
# Streamlit session state variables store data across interactions

if "correct" not in st.session_state:
    st.session_state.correct = 0  # Tracks the number of correct answers

if "incorrect" not in st.session_state:
    st.session_state.incorrect = 0  # Tracks the number of incorrect answers

if "question" not in st.session_state:
    st.session_state.question = None  # Stores the current question being asked

# --------------------------- DATABASE FUNCTIONS --------------------------- #
# The database stores user progress, so the system remembers performance between sessions

def init_db():
    """Initialize the database and create the 'progress' table if it does not exist."""
    conn = sqlite3.connect("student_progress.db")  # Connect to SQLite database
    c = conn.cursor()  # Create a cursor to execute SQL commands
    # Create a table to store user progress if it does not already exist
    c.execute('''CREATE TABLE IF NOT EXISTS progress (
                    id INTEGER PRIMARY KEY, 
                    correct INTEGER, 
                    incorrect INTEGER)''')
    # Insert default values if there is no existing progress record
    c.execute("INSERT OR IGNORE INTO progress (id, correct, incorrect) VALUES (1, 0, 0)")
    conn.commit()  # Save changes to the database
    conn.close()  # Close the database connection

def update_db():
    """Update the user's progress (correct and incorrect answers) in the database."""
    conn = sqlite3.connect("student_progress.db")
    c = conn.cursor()
    c.execute("UPDATE progress SET correct = ?, incorrect = ? WHERE id = 1",
              (st.session_state.correct, st.session_state.incorrect))  # Update values
    conn.commit()
    conn.close()

def get_progress():
    """Retrieve the user's progress from the database."""
    conn = sqlite3.connect("student_progress.db")
    c = conn.cursor()
    c.execute("SELECT correct, incorrect FROM progress WHERE id = 1")  # Get stored progress
    data = c.fetchone()  # Fetch the result
    conn.close()
    return data if data else (0, 0)  # Return progress or default values

# --------------------------- QUESTION GENERATION --------------------------- #
# The system selects an appropriate question based on user performance

def get_next_question():
    """Selects a new question based on the user's progress."""
    easy_questions = [
        {"question": "5 + 3 =", "answer": 8},
        {"question": "12 - 4 =", "answer": 8},
    ]
    
    hard_questions = [
        {"question": "8 x 6 =", "answer": 48},
        {"question": "36 ÷ 6 =", "answer": 6},
    ]
    
    multiple_choice = [
        {"question": "What is 9 + 5?", "choices": ["12", "14", "15", "16"], "answer": "14"},
        {"question": "What is 7 x 3?", "choices": ["21", "24", "18", "27"], "answer": "21"}
    ]
    
    # If user has more correct answers, provide harder questions
    if st.session_state.correct > st.session_state.incorrect:
        return random.choice(hard_questions)
    else:
        return random.choice(easy_questions + multiple_choice)

# --------------------------- SPEECH RECOGNITION --------------------------- #
# Allows users to speak their answers instead of typing



def recognize_speech():
    """Capture audio using Sounddevice and process it with SpeechRecognition."""
    recognizer = sr.Recognizer()
    
    duration = 5  # Record for 5 seconds
    sample_rate = 44100  # Audio sample rate
    st.write("Listening...")

    try:
        # Record audio using Sounddevice
        audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype=np.int16)
        sd.wait()  # Wait for recording to complete

        # Convert numpy array to SpeechRecognition format
        audio = sr.AudioData(audio_data.tobytes(), sample_rate, 2)
        return recognizer.recognize_google(audio)
    
    except sr.UnknownValueError:
        return "Could not understand. Please try again."
    
    except sr.RequestError:
        return "Speech recognition service unavailable."


# --------------------------- MAIN APPLICATION (STREAMLIT UI) --------------------------- #

def main():
    """Main function to run the Streamlit-based tutoring system."""
    
    st.title("Intelligent Tutoring System")  # Display the app title
    
    init_db()  # Ensure the database is set up before starting
    
    # --------------------------- SIDEBAR: PERFORMANCE ANALYTICS --------------------------- #
    st.sidebar.header("Performance Analytics")  # Sidebar title
    
    # Fetch user's progress from the database
    correct, incorrect = get_progress()
    
    # Create a data frame for the performance chart
    df = pd.DataFrame({"Category": ["Correct", "Incorrect"], "Count": [correct, incorrect]})
    
    # Display bar chart to visualize correct vs incorrect answers
    st.sidebar.bar_chart(df.set_index("Category"))
    
    # Show the user's progress as text
    st.sidebar.write(f"✅ Correct Answers: {correct}")
    st.sidebar.write(f"❌ Incorrect Answers: {incorrect}")
    
    # --------------------------- ASKING QUESTIONS --------------------------- #
    
    # If no question is stored in session state, generate a new one
    if st.session_state.question is None:
        st.session_state.question = get_next_question()

    # Display the question
    st.write(st.session_state.question["question"])
    
    # Check if the question has multiple-choice options
    if "choices" in st.session_state.question:
        user_answer = st.radio("Choose an answer:", st.session_state.question["choices"])  # Multiple-choice input
    else:
        user_answer = st.text_input("Your Answer:", "")  # Open-ended answer input
    
    # --------------------------- SPEECH-TO-TEXT INPUT --------------------------- #
    
    if st.button("Use Speech-to-Text"):
        user_answer = recognize_speech()  # Capture spoken answer
        st.text(f"You said: {user_answer}")  # Display recognized speech

    # --------------------------- SUBMIT ANSWER & PROVIDE FEEDBACK --------------------------- #
    
    if st.button("Submit"):
        correct_answer = st.session_state.question["answer"]  # Get the correct answer
        
        # Compare user response with correct answer
        if str(user_answer) == str(correct_answer):
            st.success("Correct!")  # Display success message
            st.session_state.correct += 1  # Update correct answer count
        else:
            st.error(f"Incorrect! The correct answer is {correct_answer}")  # Show correct answer
            st.session_state.incorrect += 1  # Update incorrect answer count

        # Update database with new progress
        update_db()
        
        # Load the next question
        st.session_state.question = get_next_question()
        
        # Refresh the Streamlit UI
        st.rerun()
    
    # --------------------------- DISPLAY SCORE --------------------------- #
    
    st.write(f"Score: {st.session_state.correct} correct, {st.session_state.incorrect} incorrect")

# Run the application
if __name__ == "__main__":
    main()
