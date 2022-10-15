from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    real_board = game.board
    games[game_id] = game

    return jsonify({"gameId": game_id, "board": real_board})

@app.post("/api/score-word")
def score_word():
    """Receives a JSON object with word input and game id
    Returns a JSON object indicating whether the word is in the
    word list and/or not on the game board.
    """

    response = request.json
    word_guess = response["wordInput"]
    game_id = response["gameId"] 
    curr_game = games[game_id]

    if not curr_game.is_word_in_word_list(word_guess):
        return jsonify({"result": "not-word"})
    if not curr_game.check_word_on_board(word_guess):
        return jsonify({"result": "not-on-board"})
    return jsonify({"result": "ok"})