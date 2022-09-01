from flask import Flask, request, redirect, render_template, flash, session, jsonify
from boggle import Boggle

# from flask_debugtoolbar import DebugToolbarExtension

boggle_game = Boggle()
statistics = {
    'times_played' : 0,
    'high_score' : 0
}

app = Flask(__name__)
app.config['SECRET_KEY'] = "sdklfjno9023u4"

# debug = DebugToolbarExtension(app)

@app.route("/")
def display_board():
    """begin a new game, create a new game-board, display HTML"""
    board_list = boggle_game.make_board()
    session['board'] = board_list
    session['statistics'] = statistics
    times_played = statistics['times_played']
    high_score = statistics['high_score']

    return render_template("boggle_board.html", board_list=board_list, times_played=times_played, high_score=high_score)


@app.route("/guess")
def check_word():
    """checks user input again word database, return JSON response"""
    word = request.args['guess']    
    response = boggle_game.check_valid_word(session['board'], word)
    json_response = jsonify({"result": response})

    return json_response


@app.route("/times_played", methods=["POST"])
def update_play_count():
    """updated the play count on game timeout"""
    old = statistics["times_played"]
    new = old + 1
    statistics["times_played"] = new
    return "updated"

    
@app.route("/high_score", methods=["POST"])
def update_high_score():
    """interpret post request with score data, if score is a new high, reset score in memory"""
    req = request.get_json()
    new_score = int(req['high_score'])
    if new_score > statistics.get('high_score'):
        statistics['high_score'] = new_score
    
    return "updated"

