# app.py
from flask import Flask, render_template, request
from solver import sokoban_solver

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    solution = None
    if request.method == "POST":
        board_input = request.form["board"]
        raw_board = board_input.strip().split("\n")
        max_width = max(len(row) for row in raw_board)
        raw_board = [row.ljust(max_width) for row in raw_board]
        solution = sokoban_solver(raw_board)
    return render_template("index.html", solution=solution)

if __name__ == "__main__":
    app.run(debug=True)
