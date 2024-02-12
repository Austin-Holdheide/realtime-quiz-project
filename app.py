# app.py
from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
socketio = SocketIO(app)

questions = [
    {'question': 'What is the capital of France?', 'options': ['Paris', 'Berlin', 'Rome', 'Madrid'], 'correct_answer': 'Paris'},
    {'question': 'Which planet is known as the Red Planet?', 'options': ['Earth', 'Mars', 'Jupiter', 'Venus'], 'correct_answer': 'Mars'},
    # Add more questions as needed
]

active_rooms = {}

def update_player_list(room):
    player_list = active_rooms.get(room, {}).get('players', [])
    emit('player_list_update', {'players': player_list}, room=room)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/join', methods=['POST'])
def join():
    username = request.form['username']
    room = request.form['room']
    session['username'] = username
    session['room'] = room

    if room not in active_rooms:
        # Handle the case where the room does not exist
        return redirect(url_for('index'))

    join_room(room)
    active_rooms[room]['players'].append(username)
    emit('notification', {'message': f'{username} has joined the room'}, room=room)
    update_player_list(room)

    return redirect(url_for('player_room'))

@app.route('/create', methods=['POST'])
def create():
    username = request.form['username']
    room = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
    session['username'] = username
    session['room'] = room
    join_room(room)
    active_rooms[room] = {'host': username, 'players': [username]}
    emit('notification', {'message': f'{username} has created and joined the room'}, room=room)
    update_player_list(room)
    return redirect(url_for('host_room'))

@app.route('/host-room')
def host_room():
    username = session.get('username', 'Anonymous')
    room = session.get('room', '')
    return render_template('host_room.html', username=username, room=room)

@app.route('/player-room')
def player_room():
    username = session.get('username', 'Anonymous')
    room = session.get('room', '')

    # Ensure the user is in a valid room before allowing access to the quiz
    if room not in active_rooms or username not in active_rooms[room]['players']:
        return redirect(url_for('index'))

    return render_template('player_room.html', username=username, room=room)

@app.route('/quiz')
def quiz():
    username = session.get('username', 'Anonymous')
    room = session.get('room', '')

    # Ensure the user is in a valid room before allowing access to the quiz
    if room not in active_rooms or username not in active_rooms[room]['players']:
        return redirect(url_for('index'))

    # Get quiz data (questions and options) - Replace this with your quiz data
    quiz_data = {'questions': questions}
    
    # Emit quiz data to clients in the room
    socketio.emit('quiz_data', quiz_data, room=room)

    return render_template('quiz.html')

@socketio.on('connect')
def handle_connect():
    username = session.get('username', 'Anonymous')
    room = session.get('room', '')

    if room not in active_rooms:
        # Handle the case where the room does not exist
        return

    join_room(room)
    active_rooms[room]['players'].append(username)
    update_player_list(room)

@socketio.on('start_game')
def handle_start_game():
    username = session.get('username', 'Anonymous')
    room = session.get('room', '')
    if username == active_rooms.get(room, {}).get('host'):
        emit('game_started', room=room, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)
