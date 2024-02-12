# Realtime Quiz Game with Flask and Socket.IO

This project implements a realtime quiz game using Flask for the backend and Socket.IO for real-time communication between clients.

## Features

- Create and join quiz rooms
- Host and player roles
- Real-time updates for player list
- Start game functionality for hosts
- Quiz questions displayed to players in real-time

## Prerequisites

- Python 3.x
- Flask
- Flask-SocketIO

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Austin-Holdheide/realtime-quiz-game.git
   ```

2. Change into the project directory:

   ```bash
   cd realtime-quiz-game
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the Flask application:

   ```bash
   python app.py
   ```

2. Open your web browser and navigate to [http://localhost:5000/](http://localhost:5000/).

3. Create a room or join an existing room to start the quiz.

## Project Structure

- `app.py`: Flask application with Socket.IO integration.
- `templates/`: HTML templates for the frontend.
- `static/`: Static files such as CSS and JavaScript.
- `requirements.txt`: List of Python dependencies.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

This project is licensed under the [MIT License](LICENSE).
