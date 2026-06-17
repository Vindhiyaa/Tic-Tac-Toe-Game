from flask import Flask, render_template, request, redirect, session
import random

app = Flask(__name__)
app.secret_key = "game"

board = [""] * 9
current_player = "X"
game_over = False
winner = None
win_cells = []

score = {"X": 0, "O": 0}


def check_winner():
    global win_cells

    win_conditions = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]

    for a,b,c in win_conditions:
        if board[a] == board[b] == board[c] and board[a] != "":
            win_cells = [a,b,c]
            return board[a]

    if "" not in board:
        return "Draw"

    return None


@app.route("/")
def login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def do_login():
    session["mode"] = request.form["mode"]

    if session["mode"] == "pvp":
        session["p1"] = request.form["player1"]
        session["p2"] = request.form["player2"]
    else:
        session["p1"] = request.form["player1"]
        session["p2"] = "Computer"

    return redirect("/game")


@app.route("/game")
def game():
    if "p1" not in session:
        return redirect("/")

    return render_template(
        "game.html",
        board=board,
        player=current_player,
        winner=winner,
        score=score,
        win_cells=win_cells,
        p1=session["p1"],
        p2=session["p2"]
    )


@app.route("/move/<int:index>")
def move(index):
    global current_player, game_over, winner

    if board[index] == "" and not game_over:
        board[index] = current_player

        result = check_winner()

        if result:
            game_over = True
            winner = result
            if winner != "Draw":
                score[winner] += 1
        else:
            current_player = "O" if current_player == "X" else "X"

            # Computer move
            if session.get("mode") == "cpu" and current_player == "O":
                empty = [i for i in range(9) if board[i] == ""]
                if empty:
                    comp_move = random.choice(empty)
                    board[comp_move] = "O"

                    result = check_winner()
                    if result:
                        game_over = True
                        winner = result
                        if winner != "Draw":
                            score[winner] += 1
                    else:
                        current_player = "X"

    return redirect("/game")


@app.route("/reset")
def reset():
    global board, current_player, game_over, winner, win_cells

    board = [""] * 9
    current_player = "X"
    game_over = False
    winner = None
    win_cells = []

    return redirect("/game")


@app.route("/logout")
def logout():
    global board, current_player, game_over, winner, win_cells

    session.clear()

    board = [""] * 9
    current_player = "X"
    game_over = False
    winner = None
    win_cells = []

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)