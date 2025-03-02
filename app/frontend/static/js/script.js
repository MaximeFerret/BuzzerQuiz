document.addEventListener("DOMContentLoaded", function () {
    const socket = io(); // Connexion WebSocket
    const buzzerButton = document.getElementById("buzzer-btn");
    const result = document.getElementById("result");

    buzzerButton.addEventListener("click", function () {
        buzzerButton.classList.add("pressed");
        socket.emit("buzz", { username: currentUser });// Envoi du signal au serveur
        setTimeout(() => {
            buzzerButton.classList.remove("pressed");
        }, 200);
    });

    // Réception de l'info sur qui a buzzé en premier
    socket.on("buzzer_response", function (data) {
        result.innerHTML = `<h2>🏆 ${data.winner} a buzzé en premier !</h2>`;
        buzzerButton.disabled = true;
    });

    // Réinitialisation du buzzer
   
    socket.on("buzzer_reset", function () {
        result.innerHTML = "";
        buzzerButton.disabled = false;
    });
});
