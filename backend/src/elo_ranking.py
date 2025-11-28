from parser import get_all_tournaments_info
#import matplotlib.pyplot as plt
#from datetime import datetime
#from matplotlib import colors as mcolors
#import random
#import pytz


STARTING_ELO = 1000
ELO_MULTIPLICATIVE_FACTOR = 100
NUMBER_OF_EVAL_GAMES = 5
NUMBER_OF_DAYS_BEFORE_INACTIVE = 15

"""
colors_dict = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
colors = list(colors_dict.values())
random.shuffle(colors)
"""

def calculate_developpement_factor(number_of_games):
    if number_of_games <= NUMBER_OF_EVAL_GAMES:
        return 45 - 5*number_of_games
    
    return 20

def calculate_expected_score_diff(player_1_elo: float, player_2_elo: float) -> float:
    elo_diff = player_1_elo - player_2_elo
    return 1/(1 + 10**(-elo_diff/ELO_MULTIPLICATIVE_FACTOR))

def calculate_elo_update(player_1_elo: float, player_2_elo: float, max_score: int, score_diff: int, number_of_games: float) -> float:
    return calculate_developpement_factor(number_of_games) * (score_diff/(2*max_score) + 1/2 - calculate_expected_score_diff(player_1_elo, player_2_elo))

def update_elo_with_match(match: dict, player_1_current_elo: float, player_2_current_elo: float, number_of_games: dict):
    player_1_name = match["participants"][0]
    player_1_score = match["score"][0]

    player_2_name = match["participants"][1]
    player_2_score = match["score"][1]

    if player_1_score < 0 or player_2_score < 0:
        return player_1_current_elo, player_2_current_elo, False

    max_score = max(player_1_score, player_2_score)
    player_1_elo_diff = calculate_elo_update(player_1_current_elo, player_2_current_elo, max_score, player_1_score - player_2_score, number_of_games[player_1_name])
    player_2_elo_diff = calculate_elo_update(player_2_current_elo, player_1_current_elo, max_score, player_2_score - player_1_score, number_of_games[player_2_name])

    if (number_of_games[player_1_name] >= NUMBER_OF_EVAL_GAMES and number_of_games[player_2_name] >= NUMBER_OF_EVAL_GAMES):
        # Both players are already placed
        new_player_1_elo = player_1_current_elo + player_1_elo_diff
        new_player_2_elo = player_2_current_elo + player_2_elo_diff
    elif (number_of_games[player_1_name] < NUMBER_OF_EVAL_GAMES and number_of_games[player_2_name] < NUMBER_OF_EVAL_GAMES):
        # Both players are in their placement games
        new_player_1_elo = player_1_current_elo + player_1_elo_diff
        new_player_2_elo = player_2_current_elo + player_2_elo_diff
    elif (number_of_games[player_1_name] < NUMBER_OF_EVAL_GAMES):
        # Only player 1 is in his placing games
        new_player_1_elo = player_1_current_elo + player_1_elo_diff
        new_player_2_elo = player_2_current_elo
    else:
        # Only player 2 is in his placing games
        new_player_1_elo = player_1_current_elo 
        new_player_2_elo = player_2_current_elo + player_2_elo_diff


    return new_player_1_elo, new_player_2_elo, True

def group_matches(tournaments: list) -> list:
    matches = []

    for t in tournaments:
        matches.extend(t["matches"])

    matches.sort(key=lambda x: x["updated_at"])

    return matches

def calculate_elo_scores(tournaments: list) -> list:
    elo_scores_dict = {}
    number_of_games = {}

    matches = group_matches(tournaments)
    for m in matches:
        player_1_name = m["participants"][0]
        player_2_name = m["participants"][1]

        if elo_scores_dict.get(player_1_name, None) is None:
            elo_scores_dict[player_1_name] = STARTING_ELO
            number_of_games[player_1_name] = 0

        if elo_scores_dict.get(player_2_name, None) is None:
            elo_scores_dict[player_2_name] = STARTING_ELO
            number_of_games[player_2_name] = 0
        
        player_1_new_score, player_2_new_score, match_played = update_elo_with_match(m, elo_scores_dict[player_1_name], elo_scores_dict[player_2_name], number_of_games)

        if match_played:
            elo_scores_dict[player_1_name] = player_1_new_score
            elo_scores_dict[player_2_name] = player_2_new_score
            number_of_games[player_1_name] += 1
            number_of_games[player_2_name] += 1

    elo_scores = [(participant, score) for participant, score in elo_scores_dict.items() if number_of_games[participant] >= NUMBER_OF_EVAL_GAMES]
    elo_scores.sort(key=lambda x: x[1])

    if elo_scores is None:
        raise Exception

    return elo_scores

def calculate_elo_scores_to_graph(tournaments: list) -> list:
    elo_scores_dict = {}
    number_of_games = {}
    times = {}

    matches = group_matches(tournaments)
    for m in matches:
        player_1_name = m["participants"][0]
        player_2_name = m["participants"][1]

        if elo_scores_dict.get(player_1_name, None) is None:
            elo_scores_dict[player_1_name] = [STARTING_ELO]
            number_of_games[player_1_name] = 0
            times[player_1_name] = []

        if elo_scores_dict.get(player_2_name, None) is None:
            elo_scores_dict[player_2_name] = [STARTING_ELO]
            number_of_games[player_2_name] = 0
            times[player_2_name] = []
        
        player_1_new_score, player_2_new_score, match_played = update_elo_with_match(m, elo_scores_dict[player_1_name][-1], elo_scores_dict[player_2_name][-1], number_of_games)

        if match_played:
            elo_scores_dict[player_1_name].append(player_1_new_score)
            elo_scores_dict[player_2_name].append(player_2_new_score)
            times[player_1_name].append(m["updated_at"])
            times[player_2_name].append(m["updated_at"])
            number_of_games[player_1_name] += 1
            number_of_games[player_2_name] += 1

    elo_scores = [(participant, score, times[participant]) for participant, score in elo_scores_dict.items()]
    elo_scores.sort(key=lambda x: x[1][-1], reverse=True)

    if elo_scores is None:
        raise Exception

    return elo_scores

"""
def plot_elo_scores(elo_scores: list):

    max_number_of_games = max(len(s) for _, s, _ in elo_scores)
    i = 0

    for participant, scores, _ in elo_scores:
        if len(scores) < NUMBER_OF_EVAL_GAMES + 1:
            continue
        plt.plot(range(len(scores)), scores, label=participant, color=colors[i])
        plt.scatter([max_number_of_games], [scores[-1]], color=colors[i])

        i += 1

    plt.legend(loc = "upper left")
    plt.show()

def plot_elo_scores_by_time(elo_scores: list):

    now = datetime.now()
    timezone = pytz.timezone("Europe/Paris")
    aware = timezone.localize(now)
    offset = aware.utcoffset()
    i = 0
    for participant, scores, times in elo_scores:
        if len(scores) < NUMBER_OF_EVAL_GAMES + 1:
            continue
        converted_times = [datetime.strptime(t, "%Y-%m-%dT%H:%M:%S.%fZ") + offset for t in times]
        if (datetime.now() - converted_times[-1]).total_seconds() >= NUMBER_OF_DAYS_BEFORE_INACTIVE*24*3600:
            continue
        plt.step(converted_times + [datetime.now()], scores[1:] + [scores[-1]], label=participant, where='post', color=colors[i])
        i += 1

    plt.legend(loc = "upper left")
    plt.show()
"""

if __name__ == "__main__":
    community_id = "a15d0f5c0bca77b6da348af7"
    tournaments_info = get_all_tournaments_info(community_id)
    elo_scores = calculate_elo_scores(tournaments_info)
    for participant, score in elo_scores:
        print(f"{participant}: {score}")

    elo_scores_hist = calculate_elo_scores_to_graph(tournaments_info)
    #plot_elo_scores(elo_scores_hist)
    #plot_elo_scores_by_time(elo_scores_hist)

    

