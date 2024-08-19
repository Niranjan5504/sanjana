from flask import Flask, render_template
from games.hang import hang_bp
from games.snake import snake_bp
from games.tic import tic_bp
from games.simon import simon_bp
from games.rock import rock_bp
from games.pong import pong_bp
from games.draw import draw_bp
from games.piano import piano_bp


app = Flask(__name__)
app.secret_key = 'your_unique_secret_key'

# Register Blueprints
app.register_blueprint(hang_bp)
app.register_blueprint(snake_bp)
app.register_blueprint(tic_bp)
app.register_blueprint(simon_bp)
app.register_blueprint(rock_bp)
app.register_blueprint(pong_bp)
app.register_blueprint(draw_bp)
app.register_blueprint(piano_bp)


@app.route('/')
def index():
    return render_template('index1.html')

if __name__ == '__main__':
    app.run(debug=True)
