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
    "cpcpl0ng": 2.25,  #PKF7
    "spvaky9d": 2.25, #PKF8
    "rwwddc57": 4, # PKF9
    #============== Saison 2 =============
    "xlyc40s7": 1.5,
    "z8fmjkuk": 8,
    "u6d0larl": 2,
    "ckyh7n6m": 3,
    "ky8z1ukw": 1.5,
    "9ug6n3oe": 4,
    "2g64tkut": 1.5,
    "cdm8qmgw": 4,
    "v5gmufc8": 1.5
}

def ranking_formula(tournaments_propreties: list) -> float:
    return sum(w*POINT_GAINED[r] for _, w, r in tournaments_propreties)/(1 + 0.22*sum(w for _, w, _ in tournaments_propreties)**0.8)

def calculate_pr_scores(tournaments_info: list) -> dict:
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

