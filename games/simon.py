from flask import Flask, render_template, session,Blueprint
import random
simon_bp = Blueprint('simon', __name__ , template_folder='templates')

app = Flask(__name__)
app.secret_key = 'simon_says_secret_key'

@simon_bp.route('/simon')
def index():
    session.clear()  # Clear session data to reset the game
    return render_template('simon.html')

@simon_bp.route('/next_sequence')
def next_sequence():
    if 'sequence' not in session:
        session['sequence'] = []

    colors = ['red', 'green', 'blue', 'yellow']
    next_color = random.choice(colors)
    session['sequence'].append(next_color)

    return {'sequence': session['sequence']}

@simon_bp.route('/reset_game')
def reset_game():
    session.clear()
    return {'status': 'Game reset'}

if __name__ == '__main__':
    app.run(debug=True)
