from flask import Flask, request
from pr_ranking import calculate_scores
from parser import get_all_tournaments_info

app = Flask(__name__)
community_id = "a15d0f5c0bca77b6da348af7"

@app.route('/get_pr_ranking')
def get_pr_ranking():
    tournaments = get_all_tournaments_info(community_id)
    return calculate_scores(tournaments)
