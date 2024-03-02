from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, emit
import random

app = Flask(__name__)
socketio = SocketIO(app)

# Store information about active games
active_games = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_game', methods=['POST'])
def create_game():
    game_id = str(random.randint(1000, 9999))
    active_games[game_id] = {'questions': ['Question 1', 'Question 2', 'Question 3'], 'answers': [2, 1, 3], 'current_question': 0, 'answered': 0, 'players': []}
    return redirect(url_for('host', game_id=game_id))

@app.route('/join_game', methods=['POST'])
def join_game():
    username = request.form['username']
    game_id = request.form['game_id']
    return render_template('player.html', username=username, game_id=game_id)

@app.route('/host/<game_id>')
def host(game_id):
    return render_template('host.html', game_id=game_id)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('join_room')
def handle_join_room(data):
    username = data['username']
    game_id = data['game_id']
    join_room(game_id)
    active_games[game_id]['players'].append(username)
    emit('update_players', {'players': active_games[game_id]['players']}, room=game_id)

@socketio.on('start_game')
def handle_start_game(data):
    game_id = data['game_id']
    emit('game_started', room=game_id)

@socketio.on('answer_question')
def handle_answer_question(data):
    game_id = data['game_id']
    active_games[game_id]['answered'] += 1
    emit('update_answers', {'answered': active_games[game_id]['answered']}, room=game_id)

if __name__ == '__main__':
    socketio.run(app, debug=True)
