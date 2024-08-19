from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, jsonify

pong_bp = Blueprint('pong', __name__, template_folder='templates')

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Sample questions
questions = [
    {'question': 'What is the capital of France?', 'options': ['Paris', 'London', 'Berlin', 'Madrid'], 'answer': 'Paris'},
    {'question': 'Who wrote "To Kill a Mockingbird"?', 'options': ['Harper Lee', 'Mark Twain', 'Ernest Hemingway', 'F. Scott Fitzgerald'], 'answer': 'Harper Lee'},
    {'question': 'What is the chemical symbol for water?', 'options': ['H2O', 'O2', 'CO2', 'H2'], 'answer': 'H2O'},
    {'question': 'Which planet is known as the Red Planet?', 'options': ['Mars', 'Jupiter', 'Venus', 'Saturn'], 'answer': 'Mars'},
    {'question': 'What is the largest mammal?', 'options': ['Elephant', 'Blue Whale', 'Giraffe', 'Rhino'], 'answer': 'Blue Whale'},
    {'question': 'Who painted the Mona Lisa?', 'options': ['Leonardo da Vinci', 'Pablo Picasso', 'Vincent van Gogh', 'Claude Monet'], 'answer': 'Leonardo da Vinci'},
    {'question': 'What is the hardest natural substance on Earth?', 'options': ['Gold', 'Iron', 'Diamond', 'Platinum'], 'answer': 'Diamond'},
    {'question': 'Which is the smallest country in the world?', 'options': ['Vatican City', 'Monaco', 'Malta', 'Liechtenstein'], 'answer': 'Vatican City'},
    {'question': 'Who developed the theory of relativity?', 'options': ['Isaac Newton', 'Albert Einstein', 'Nikola Tesla', 'Galileo Galilei'], 'answer': 'Albert Einstein'},
    {'question': 'What is the square root of 64?', 'options': ['6', '8', '10', '12'], 'answer': '8'},
    {'question': 'Which element has the atomic number 1?', 'options': ['Oxygen', 'Hydrogen', 'Carbon', 'Helium'], 'answer': 'Hydrogen'},
    {'question': 'What is the main ingredient in guacamole?', 'options': ['Tomato', 'Avocado', 'Cucumber', 'Pepper'], 'answer': 'Avocado'},
    {'question': 'In which year did the Titanic sink?', 'options': ['1912', '1905', '1920', '1898'], 'answer': '1912'},
    {'question': 'Which ocean is the largest?', 'options': ['Atlantic', 'Indian', 'Arctic', 'Pacific'], 'answer': 'Pacific'},
    {'question': 'Who is known as the father of computers?', 'options': ['Alan Turing', 'Charles Babbage', 'John von Neumann', 'Steve Jobs'], 'answer': 'Charles Babbage'},
    {'question': 'What is the capital of Japan?', 'options': ['Beijing', 'Seoul', 'Tokyo', 'Bangkok'], 'answer': 'Tokyo'},
    {'question': 'Which planet has the most moons?', 'options': ['Earth', 'Mars', 'Saturn', 'Jupiter'], 'answer': 'Jupiter'},
    {'question': 'What is the most spoken language in the world?', 'options': ['English', 'Spanish', 'Mandarin', 'Hindi'], 'answer': 'Mandarin'},
    {'question': 'Which country is the largest by area?', 'options': ['China', 'Canada', 'Russia', 'USA'], 'answer': 'Russia'},
    {'question': 'What is the chemical symbol for gold?', 'options': ['Au', 'Ag', 'Fe', 'Pb'], 'answer': 'Au'},
    {'question': 'Which organ is responsible for pumping blood throughout the body?', 'options': ['Liver', 'Lungs', 'Heart', 'Kidneys'], 'answer': 'Heart'},
    {'question': 'Which is the longest river in the world?', 'options': ['Nile', 'Amazon', 'Yangtze', 'Mississippi'], 'answer': 'Nile'},
    {'question': 'Who was the first man to walk on the moon?', 'options': ['Neil Armstrong', 'Buzz Aldrin', 'Yuri Gagarin', 'Michael Collins'], 'answer': 'Neil Armstrong'},
    {'question': 'What is the freezing point of water?', 'options': ['0°C', '32°F', '100°C', 'Both 0°C and 32°F'], 'answer': 'Both 0°C and 32°F'},
    {'question': 'What is the capital of Australia?', 'options': ['Sydney', 'Melbourne', 'Canberra', 'Perth'], 'answer': 'Canberra'},
]


@pong_bp.route('/pong', methods=['GET', 'POST'])
def index():
    if 'question_index' not in session:
        session['question_index'] = 0
        session['score'] = 0

    if request.method == 'POST':
        selected_option = request.form.get('option')
        correct_answer = questions[session['question_index']]['answer']

        if selected_option == correct_answer:
            session['score'] += 1
        
        session['question_index'] += 1
        
        if session['question_index'] >= len(questions):
            return redirect(url_for('result'))
        
        return redirect(url_for('index'))
    
    current_question = questions[session['question_index']]
    return render_template('pong.html', question=current_question)

@pong_bp.route('/get_next_question', methods=['POST'])
def get_next_question():
    if 'question_index' not in session:
        return jsonify({'error': 'No questions available'}), 400

    session['question_index'] += 1
    
    if session['question_index'] >= len(questions):
        return jsonify({'redirect': url_for('result')})

    current_question = questions[session['question_index']]
    return jsonify({
        'question': current_question['question'],
        'options': current_question['options'],
        'answer': current_question['answer']
    })

@pong_bp.route('/result')
def result():
    score = session.get('score', 0)
    total_questions = len(questions)
    session.pop('question_index', None)
    session.pop('score', None)
    return render_template('pong.html', score=score, total_questions=total_questions)

if __name__ == '__main__':
    app.run(debug=True)
