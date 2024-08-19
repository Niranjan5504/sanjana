from flask import Flask, render_template, request, redirect, url_for, session,Blueprint
import random
tic_bp = Blueprint('tic', __name__ , template_folder='templates')

app = Flask(__name__)
app.secret_key = 'a_very_secure_and_random_key_123345678905678'

# Initialize the game board
def init_board():
    return ['' for _ in range(9)]

# Check for a winner or draw
def check_winner(board):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for condition in win_conditions:
        a, b, c = condition
        if board[a] == board[b] == board[c] and board[a] != '':
            return board[a]
    if '' not in board:
        return 'Draw'
    return None

# Computer move (simple AI)
def computer_move(board):
    available_moves = [i for i, spot in enumerate(board) if spot == '']
    return random.choice(available_moves)

@tic_bp.route('/tic', methods=['GET', 'POST'])  # Fixed line 32
def index():
    if request.method == 'POST':
        session['player_symbol'] = request.form['symbol']
        session['computer_symbol'] = 'O' if session['player_symbol'] == 'X' else 'X'
        session['mode'] = request.form['mode']
        session['board'] = init_board()
        session['turn'] = 'X'
        return redirect(url_for('tic.game'))

    return render_template('tic.html')

@tic_bp.route('/game1', methods=['GET', 'POST'])
def game():
    if request.method == 'POST':
        index = int(request.form['index'])
        mode = session.get('mode')

        if session['board'][index] == '':
            session['board'][index] = session['turn']
            winner = check_winner(session['board'])

            if winner:
                return render_template('game1.html', board=session['board'], turn=session['turn'], winner=winner, mode=mode)

            # Switch turns
            session['turn'] = 'O' if session['turn'] == 'X' else 'X'

            # If single-player and it's now the computer's turn, make the computer move
            if mode == 'single' and session['turn'] == session['computer_symbol']:
                computer_index = computer_move(session['board'])
                session['board'][computer_index] = session['computer_symbol']
                winner = check_winner(session['board'])

                if winner:
                    return render_template('game1.html', board=session['board'], turn=session['turn'], winner=winner, mode=mode)

                # Switch back to player's turn
                session['turn'] = session['player_symbol']

    return render_template('game1.html', board=session['board'], turn=session['turn'], mode=session['mode'])

@tic_bp.route('/reset')
def reset():
    session['board'] = init_board()
    session['turn'] = 'X'
    return redirect(url_for('tic.index'))


if __name__ == '__main__':
    app.run(debug=True)
