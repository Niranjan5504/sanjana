from flask import Blueprint, render_template, jsonify, request
import random

hang_bp = Blueprint('hang', __name__ , template_folder='templates')

# List of potential words
word_pool = [
    "python", "flask", "hangman", "challenge", "programming", 
    "computer", "algorithm", "function", "variable", "syntax"
]

# Game state
game_state = {
    "word": "",
    "display_word": "",
    "clues": [],
    "guesses": [],
    "attempts_left": 6,
    "game_over": False,
    "win": False
}

# Function to generate clues based on the word
def generate_clues(word):
    clues = [
        f"It starts with '{word[0].upper()}' and ends with '{word[-1].upper()}'.",
        f"It has {len(word)} letters.",
        f"It contains the letter '{random.choice(word)}'.",
        f"It is related to technology.",
        f"It rhymes with '{generate_rhyme(word)}'."
    ]
    return clues

# Simple function to generate a rhyme (this is just a placeholder and may not create actual rhymes)
def generate_rhyme(word):
    if len(word) > 2:
        return word[-2:] + random.choice('abcdefghijklmnopqrstuvwxyz')
    return word + random.choice('abcdefghijklmnopqrstuvwxyz')

def new_game():
    word = random.choice(word_pool)
    game_state["word"] = word
    game_state["display_word"] = "_" * len(word)
    game_state["clues"] = generate_clues(word)  # Generate clues automatically
    game_state["guesses"] = []
    game_state["attempts_left"] = 6
    game_state["game_over"] = False
    game_state["win"] = False

@hang_bp.route('/hang')
def index():
    new_game()
    return render_template('hang.html', game_state=game_state)

@hang_bp.route('/guess', methods=['POST'])
def guess():
    if game_state["game_over"]:
        return jsonify(game_state)

    data = request.json
    letter = data.get('letter').lower()

    if letter in game_state["guesses"]:
        return jsonify(game_state)

    game_state["guesses"].append(letter)

    if letter in game_state["word"]:
        display_word = list(game_state["display_word"])
        for i, char in enumerate(game_state["word"]):
            if char == letter:
                display_word[i] = letter
        game_state["display_word"] = "".join(display_word)

        if "_" not in game_state["display_word"]:
            game_state["win"] = True
            game_state["game_over"] = True
    else:
        game_state["attempts_left"] -= 1
        if game_state["attempts_left"] <= 0:
            game_state["game_over"] = True

    return jsonify(game_state=game_state)

@hang_bp.route('/clue', methods=['GET'])
def clue():
    if game_state["game_over"]:
        return jsonify({"clue": ""})

    # Provide the next clue in the list
    clue = game_state["clues"].pop(0) if game_state["clues"] else "No more clues available."
    return jsonify({"clue": clue})


if __name__ == '__main__':
    app.run(debug=True)
