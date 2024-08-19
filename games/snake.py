from flask import Flask, render_template, jsonify, request,Blueprint
import random
snake_bp = Blueprint('snake', __name__ , template_folder='templates')

app = Flask(__name__)

# Game state
snake = [(100, 100)]  # Snake starts with a single segment
food = (200, 200)     # Initial food position
direction = 'right'  # Initial direction
game_width = 500      # Width of the game area
game_height = 500     # Height of the game area
segment_size = 20     # Size of each snake segment

@snake_bp.route('/snake')
def index():
    return render_template('snake.html')

@snake_bp.route('/update_position', methods=['POST'])
def update_position():
    global snake, food, direction
    
    data = request.json
    new_direction = data.get('direction')

    # Update direction if it's a valid change
    if (direction == 'up' and new_direction != 'down') or \
       (direction == 'down' and new_direction != 'up') or \
       (direction == 'left' and new_direction != 'right') or \
       (direction == 'right' and new_direction != 'left'):
        direction = new_direction

    # Move snake
    head_x, head_y = snake[0]
    if direction == 'up':
        head_y -= segment_size
    elif direction == 'down':
        head_y += segment_size
    elif direction == 'left':
        head_x -= segment_size
    elif direction == 'right':
        head_x += segment_size

    # Ensure snake stays within bounds
    head_x = head_x % game_width
    head_y = head_y % game_height

    new_head = (head_x, head_y)
    snake = [new_head] + snake[:-1]  # Add new head and remove the tail

    # Check if snake eats the food
    if new_head == food:
        # Grow the snake by adding a new segment
        snake.append(snake[-1])
        
        # Generate a new food position
        while True:
            food = (random.randint(0, (game_width // segment_size) - 1) * segment_size,
                    random.randint(0, (game_height // segment_size) - 1) * segment_size)
            if food not in snake:
                break

    return jsonify({
        'snake': snake,
        'food': food
    })

if __name__ == '__main__':
    app.run(debug=True)
