'use strict';

const apiUrl = "/api"
refresh_state()

async function start() {
    try {
        const response = await fetch(`${apiUrl}/manage`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                method: 'start'
            })

        });
        const data = await response.json();
        console.log(data)
        localStorage.setItem("game_id", data.game_id);
        document.getElementById("status").textContent = `Current turn: Purple`
        set_board(data.board)
    } catch (error) {
        console.error("Error starting the game:", error);
    }
}

async function stop() {
    try {
        const gameId = localStorage.getItem("game_id")
        const response = await fetch(`${apiUrl}/manage`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                method: 'stop',
                game_id: gameId
            })
        });
        if (response.ok) {
            localStorage.removeItem("game_id")
            document.getElementById("status").textContent = "Shishima game"
            set_board([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])
        }
    } catch (error) {
        console.error("Error starting the game:", error);
    }
}

async function refresh_state() {
    try {
        const gameId = localStorage.getItem("game_id")
        const response = await fetch(`${apiUrl}/${gameId}/board`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            }
        });
        const data = await response.json();
        console.log(data)
        set_board(data.board)
        if (data.game_over) {
            const winner = data.current_player === "X" ? "Purple" : "Blue"
            document.getElementById("status").textContent = `${winner} wins!`
        } else {
            const turn = data.current_player === "X" ? "Purple" : "Blue"
            document.getElementById("status").textContent = `${turn}'s turn!`
        }
    } catch (error) {
        console.error("Error starting the game:", error);
    }
}

const set_board = function (board) {
    for (let i = 0; i < board.length; i++) {
        const cell = document.getElementById(`cell${i}`);
        if (board[i] === "X") {
            cell.setAttribute("state", "self");
        } else if (board[i] === "O") {
            cell.setAttribute("state", "enemy");
        } else {
            cell.setAttribute("state", "empty");
        }
    }
}

async function makeMove(moveFrom, moveTo) {
    const gameId = localStorage.getItem("game_id");
    try {
        const response = await fetch(`${apiUrl}/${gameId}/move`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                move_from: moveFrom,
                move_to: moveTo
            })
        });
        const data = await response.json();
        console.log(data)
    } catch (error) {
        console.error("Error making the move:", error);
    }
}


let move_from = null;
document.getElementById("start").addEventListener("click", start);
document.getElementById("reset").addEventListener("click", stop);
document.querySelectorAll(".cell").forEach((item) =>
    item.addEventListener("click", (e) => {
        if (move_from === null) {
            move_from = e.target.getAttribute("data-id")
            console.log(move_from)
        } else {
            makeMove(move_from, e.target.getAttribute("data-id"))
            refresh_state()
            move_from = null;
        }
    })
);