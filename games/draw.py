from flask import Flask, render_template,Blueprint
draw_bp = Blueprint('draw', __name__ , template_folder='templates')

app = Flask(__name__)

@draw_bp.route('/draw')
def index():
    return render_template('draw.html')

@draw_bp.route('/multiplayer')
def multiplayer():
    return render_template('multiplayer.html')

if __name__ == '__main__':
    app.run(debug=True)
