// static/index.js
document.addEventListener('DOMContentLoaded', () => {
    const socket = io.connect(window.location.origin);

    socket.on('connect', () => {
        socket.emit('connect');
    });

    socket.on('notification', (data) => {
        console.log(data.message);
    });
});
