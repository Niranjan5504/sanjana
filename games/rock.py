from flask import Flask, render_template, request, session, redirect, url_for,Blueprint
import random
rock_bp = Blueprint('rock', __name__ , template_folder='templates')

app = Flask(__name__)
app.secret_key = 'a_very_secure_and_random_key_1234'  # Replace with a strong secret key

@rock_bp.route('/rock')
def index():
    # Initialize scores if not already set
    if 'player1_score' not in session:
        session['player1_score'] = 0
    if 'player2_score' not in session:
        session['player2_score'] = 0

    return render_template('paper.html', 
                           player1_score=session['player1_score'], 
                           player2_score=session['player2_score'])

@rock_bp.route('/play', methods=['POST'])
def play():
    mode = request.form.get('mode')
    player1_choice = request.form.get('player1_choice')

    if mode == 'single':
        choices = ['rock', 'paper', 'scissors']
        computer_choice = random.choice(choices)
        result = get_winner(player1_choice, computer_choice)

        if result == 'player1':
            session['player1_score'] += 1
        elif result == 'player2':
            session['player2_score'] += 1
        
        return render_template('paper.html', 
                               player1_choice=player1_choice, 
                               player2_choice=computer_choice, 
                               result=result, 
                               player1_score=session['player1_score'], 
                               player2_score=session['player2_score'], 
                               mode=mode)

    elif mode == 'multi':
        player2_choice = request.form.get('player2_choice')
        result = get_winner(player1_choice, player2_choice)

        if result == 'player1':
            session['player1_score'] += 1
        elif result == 'player2':
            session['player2_score'] += 1
        
        return render_template('paper.html', 
                               player1_choice=player1_choice, 
                               player2_choice=player2_choice, 
                               result=result, 
                               player1_score=session['player1_score'], 
                               player2_score=session['player2_score'], 
                               mode=mode)

def get_winner(choice1, choice2):
    if choice1 == choice2:
        return 'draw'
    elif (choice1 == 'rock' and choice2 == 'scissors') or \
         (choice1 == 'scissors' and choice2 == 'paper') or \
         (choice1 == 'paper' and choice2 == 'rock'):
        return 'player1'
    else:
        return 'player2'

@rock_bp.route('/reset1')
def reset():
    session['player1_score'] = 0
    session['player2_score'] = 0
    return redirect(url_for('rock.index'))

if __name__ == '__main__':
    app.run(debug=True)
