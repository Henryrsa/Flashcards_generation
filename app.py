from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import pandas as pd
import random
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize database if not exists
def init_db():
    if not os.path.exists('flashcards.db'):
        conn = sqlite3.connect('flashcards.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE flashcards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mistake_type TEXT,
                original_sentence TEXT,
                corrected_sentence TEXT
            )
        ''')
        conn.commit()
        conn.close()

# Load CSV data into database
def load_csv_to_db():
    df = pd.read_csv('student_mistakes.csv')
    conn = sqlite3.connect('flashcards.db')
    df.to_sql('flashcards', conn, if_exists='replace', index=False)
    conn.commit()
    conn.close()

# Fetch random flashcard for user quiz
def get_random_flashcard():
    conn = sqlite3.connect('flashcards.db')
    c = conn.cursor()
    c.execute('SELECT * FROM flashcards ORDER BY RANDOM() LIMIT 1')
    flashcard = c.fetchone()
    conn.close()
    return flashcard

# Store user answers for review
user_answers = []
answered_questions = set()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    flashcard = get_random_flashcard()
    
    # Calculate total number of questions
    conn = sqlite3.connect('flashcards.db')
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM flashcards')
    total_questions = c.fetchone()[0]
    conn.close()

    if request.method == 'POST':
        user_answer = request.form['user_answer'].strip().lower()  # Clean user input
        correct_answer = request.form['correct_answer'].strip().lower()  # Clean correct answer
        question_id = request.form['question_id']  # Fetch question ID from hidden field

        # Store user input and correct answer
        user_answers.append({
            'id': question_id,  # Flashcard ID
            'mistake_type': request.form['mistake_type'],  # Mistake type
            'original_sentence': request.form['original_sentence'],  # Original sentence
            'user_input': user_answer,  # User's input
            'corrected_sentence': correct_answer  # Correct answer
        })
        answered_questions.add(question_id)

        if user_answer == correct_answer:
            flash('Correct!', 'success')
        else:
            flash(f'Incorrect! The correct answer is: {correct_answer.capitalize()}', 'danger')

        return redirect(url_for('quiz'))

    # Calculate current question index
    current_question_index = len(user_answers) + 1  # 1-based index

    return render_template('quiz.html', flashcard=flashcard, total_questions=total_questions, current_question_index=current_question_index)

@app.route('/flashcards')
def flashcards_review():
    return render_template('flashcards.html', flashcards=user_answers, answered_questions=answered_questions)

if __name__ == '__main__':
    init_db()
    load_csv_to_db()
    app.run(debug=True)
