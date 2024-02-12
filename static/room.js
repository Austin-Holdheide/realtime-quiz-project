// static/quiz.js
document.addEventListener('DOMContentLoaded', () => {
    const socket = io.connect(window.location.origin);

    socket.on('connect', () => {
        socket.emit('connect');
    });

    // Customize the following function to handle quiz display
    function displayQuiz(questions) {
        const quizContainer = document.getElementById('quiz-container');

        // Clear previous content
        quizContainer.innerHTML = '';

        // Display each question and options
        questions.forEach((question, index) => {
            const questionDiv = document.createElement('div');
            questionDiv.innerHTML = `
                <h3>${index + 1}. ${question.question}</h3>
                <ul>
                    ${question.options.map(option => `<li>${option}</li>`).join('')}
                </ul>
            `;
            quizContainer.appendChild(questionDiv);
        });
    }

    // Listen for quiz data from the server
    socket.on('quiz_data', (data) => {
        displayQuiz(data.questions);
    });
});
