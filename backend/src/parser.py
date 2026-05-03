import requests
import os
from dotenv import load_dotenv
from unidecode import unidecode

load_dotenv()
API_KEY=os.getenv("API_KEY")
BASE_URL = "https://api.challonge.com/v2.1"
BASE_HEADERS = {
    'Content-Type': "application/vnd.api+json",
    'Accept': 'application/json',
    'Authorization-Type': 'v1',
    'Authorization': API_KEY,
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:144.0) Gecko/20100101 Firefox/144.0'
}

def get_matches(tournament_id: str, community_id: str) -> dict:
    
    url = BASE_URL + f"/tournaments/{tournament_id}/matches.json?community_id={community_id}"

    payload={}
    response = requests.request("GET", url, headers=BASE_HEADERS, data=payload)
    matches = response.json()
    return matches

def get_participants(tournament_id: str, community_id: str) -> dict:
    url = BASE_URL + f"/tournaments/{tournament_id}/participants.json?community_id={community_id}&per_page=1000"

    payload={}
    response = requests.request("GET", url, headers=BASE_HEADERS, data=payload)
    participants = response.json()
    return participants 

def parse_participants(participants: dict) -> dict:
    parsed_participants = {}

    for p in participants["data"]:
        parsed_participants[int(p["id"])] = {
            "name": unidecode(p["attributes"]["name"]),
            "final_rank": p["attributes"]["final_rank"],
        }

    return parsed_participants

def parse_matches(matches: dict, parsed_participants: dict) -> list:
    parsed_matches = []
    
    for m in matches["data"]:
        if [] in [p["scores"] for p in m["attributes"]["points_by_participant"]]:
            continue
        parsed_matches.append({
            "participants": [parsed_participants[p["participant_id"]]["name"] for p in m["attributes"]["points_by_participant"]], 
            "score": [p["scores"][0] for p in m["attributes"]["points_by_participant"]], 
            "updated_at": m["attributes"]["timestamps"]["updated_at"],
            "status": m["attributes"]["state"]
        })

    parsed_matches.sort(key=lambda x: x["updated_at"])

    return parsed_matches

def get_tournament_info(tournament_id: str, state: str, community_id: str, time: str) -> dict:
    participants = get_participants(tournament_id, community_id)
    parsed_participants = parse_participants(participants)

    matches = get_matches(tournament_id, community_id)
    parsed_matches = parse_matches(matches, parsed_participants)

    return {"matches": parsed_matches, "participants": parsed_participants, "url": tournament_id, "state": state, "time": time}

def get_tournament_list(community_id: str) -> dict:
    url = BASE_URL + f"/tournaments.json?community_id={community_id}"

    payload={}
    response = requests.request("GET", url, headers=BASE_HEADERS, data=payload)
    tournaments = response.json()
    return tournaments

def parse_tournament_list(tournaments: dict) -> list:
    parsed_tournament_list = []

    for t in tournaments["data"]:
        parsed_tournament_list.append((t["attributes"]["url"], t["attributes"]["state"], t["attributes"]["starts_at"]))

    parsed_tournament_list.sort(key=lambda x: x[2])

    return parsed_tournament_list

def get_all_tournaments_info(communities_id: list) -> list:
    tournaments_info = []
    for community_id in communities_id:
        tournaments = get_tournament_list(community_id)
        parsed_tournament_list = parse_tournament_list(tournaments)
        tournaments_info.extend([get_tournament_info(t[0], t[1], community_id, t[2]) for t in parsed_tournament_list])
    return tournaments_info


if __name__ == "__main__":
    community_id = "a15d0f5c0bca77b6da348af7"
    print(len(get_all_tournaments_info(community_id)[0]["participants"]))
