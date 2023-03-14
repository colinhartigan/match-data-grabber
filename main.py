import json

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from valclient.client import Client

client = Client()
client.activate()

def fetch_matches(client) -> list:
    print("fetching matches one sec")
    matches = client.fetch_match_history()["History"]
    choices = []
    for match in matches:
        match_data = client.fetch_match_details(match["MatchID"])

        me = next(player for player in match_data["players"] if player["subject"] == client.puuid)
        my_team = next(team for team in match_data["teams"] if team["teamId"] == me["teamId"])
        other_team = next(team for team in match_data["teams"] if team["teamId"] != me["teamId"])

        queue = match_data["matchInfo"]["queueID"]
        if queue == " " or queue == "":
            queue = "custom"
        match_id = match_data["matchInfo"]["matchId"]
        score = f"{my_team['roundsWon']}-{other_team['roundsWon']}"

        string = f"[{score}] {queue} ({match_id})"
        choices.append(Choice(match_id, string))

    return choices

if __name__ == "__main__":
    choices = fetch_matches(client)
    match_id = inquirer.select("pick a match:", choices).execute()
    with open(f"{match_id}.json", "w") as f:
        f.write(json.dumps(client.fetch_match_details(match_id)))
    print("done")