from flask import Flask, request
from pr_ranking import calculate_pr_scores
from elo_ranking import calculate_elo_scores
from parser import get_all_tournaments_info

app = Flask(__name__)
communities = ["a15d0f5c0bca77b6da348af7", "2e83a668fc9b0698f4ca2a09"]

@app.route('/get_pr_ranking')
def get_pr_ranking():
    tournaments = get_all_tournaments_info(communities[-1:])
    return calculate_pr_scores(tournaments)

@app.route('/get_elo_ranking')
def get_elo_ranking():
    tournaments = get_all_tournaments_info(communities)
    return calculate_elo_scores(tournaments)
