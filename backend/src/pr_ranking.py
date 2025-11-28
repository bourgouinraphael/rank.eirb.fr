#from parser import get_all_tournaments_info
#import matplotlib.pyplot as plt
#from datetime import datetime
#import pytz
#from matplotlib import colors as mcolors
#import random

"""
colors_dict = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
colors = list(colors_dict.values())
random.shuffle(colors)
"""

POINT_GAINED = {
    1: 75,
    2: 60,
    3: 50,
    4: 40,
    5: 53,
    7: 30,
    9: 25,
    13: 20,
    17: 15,
    25: 10
}

WEIGHT_BY_TOURNAMENT = {
    "ey5d6c0e": 7, # WEES 2025
    "3da4jzp9": 2, # PK1
    "dptt9cfz": 2, # PK2
    "jldmeplm": 1.5, # PK3
    "b2ncwzb1": 1.25, # PK4
    "s8qpjgaz": 7, # PKT1
    "5vx9rv0b": 2.25, #PKF5
    "ohnm2yke": 2.25, #PKF6
    "cpcpl0ng": 2.25  #PKF7
}

def ranking_formula(tournaments_propreties: list) -> float:
    return sum(w*POINT_GAINED[r] for _, w, r in tournaments_propreties)/(1 + 0.22*sum(w for _, w, _ in tournaments_propreties)**0.8)

def calculate_scores(tournaments_info: list) -> dict:
    rankings_per_participants = {}

    for tournament in tournaments_info:
        tournament_time = tournament["time"]
        rankings = {p["name"]: p["final_rank"] for p in tournament["participants"].values()}
        weight = WEIGHT_BY_TOURNAMENT.get(tournament["url"], 0)
        for name, rank in rankings.items():
            if rankings_per_participants.get(name, None) is None:
                rankings_per_participants[name] = [(tournament_time, weight, rank)]
            else:
                rankings_per_participants[name].append((tournament_time, weight, rank))

    for name in rankings_per_participants.keys():
        rankings_per_participants[name].sort(key=lambda x: x[0])
    
    score_per_participant = {}
    for name, ranks in rankings_per_participants.items():
        score_per_participant[name] = [(ranks[i][0], ranking_formula(ranks[:i+1])) for i in range(len(ranks))]

    return score_per_participant

"""
def plot_scores_on_time(scores: dict):
    
    now = datetime.now()
    timezone = pytz.timezone("Europe/Paris")
    aware = timezone.localize(now)
    offset = aware.utcoffset()
    i = 0
    for participant, s in scores.items():
        times = [t[0] for t in s]
        participant_scores = [t[1] for t in s]
        plt.step([datetime.strptime(t.split("+")[0], "%Y-%m-%dT%H:%M:%S.%f") + offset for t in times] + [datetime.now()], participant_scores + [participant_scores[-1]], label=participant, where='post', color=colors[i])
        i += 1

    plt.legend(loc = "upper left", ncol=3)
    plt.show()

if __name__ == "__main__":
    community_id = "a15d0f5c0bca77b6da348af7"
    tournaments_info = get_all_tournaments_info(community_id)
    complete_score = calculate_scores(tournaments_info)

    for i in range(len(tournaments_info)):
        final_scores = [(participant, max((s[1] for s in scores if s[0] <= tournaments_info[i]["time"]), default=-1)) for participant, scores in complete_score.items()]
        final_scores = [f for f in final_scores if f[1] != -1]
        final_scores.sort(key=lambda x: x[1])
        j = len(final_scores)
        for participant, score in final_scores:
            print(f"{j} {participant}: {score}")
            j -= 1

        input()

    #plot_scores_on_time(complete_score)

"""
