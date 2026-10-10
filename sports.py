# Sports Tournament Management System
# Python 3.6 compatible command-line prototype.
# Run: python3 sports_tournament.py
# Records are saved in sports_data.json in the same folder.

import json
import os

DATA_FILE = "sports_data.json"


def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                data = json.load(file)
                return data
        except (ValueError, IOError):
            pass
    return {"teams": [], "players": [], "matches": [],
            "next_team_id": 1, "next_player_id": 1, "next_match_id": 1}


def save_data():
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


data = load_data()


def find_team(team_id):
    for team in data["teams"]:
        if team["id"] == team_id:
            return team
    return None


def team_name(team_id):
    team = find_team(team_id)
    return team["name"] if team else "Unknown team"


def read_int(prompt, minimum=0):
    while True:
        try:
            value = int(input(prompt))
            if value < minimum:
                print("Enter a number greater than or equal to {}.".format(minimum))
            else:
                return value
        except ValueError:
            print("Please enter a whole number.")


def add_team():
    name = input("Team name: ").strip()
    sport = input("Sport: ").strip()
    captain = input("Captain name: ").strip()
    city = input("City/college: ").strip()
    if not name:
        print("Team name cannot be empty.")
        return
    team = {"id": data["next_team_id"], "name": name, "sport": sport,
            "captain": captain, "city": city}
    data["teams"].append(team)
    data["next_team_id"] += 1
    save_data()
    print("Team added successfully. Team ID:", team["id"])


def list_teams():
    if not data["teams"]:
        print("No teams registered.")
        return
    print("\n--- REGISTERED TEAMS ---")
    for team in data["teams"]:
        print("ID: {id} | {name} | {sport} | Captain: {captain} | {city}".format(**team))


def add_player():
    list_teams()
    if not data["teams"]:
        return
    team_id = read_int("Enter the team ID for this player: ", 1)
    if not find_team(team_id):
        print("Team ID not found.")
        return
    name = input("Player name: ").strip()
    age = read_int("Player age: ", 1)
    role = input("Player role/position: ").strip()
    player = {"id": data["next_player_id"], "name": name, "age": age,
              "role": role, "team_id": team_id}
    data["players"].append(player)
    data["next_player_id"] += 1
    save_data()
    print("Player registered successfully.")


def list_players():
    if not data["players"]:
        print("No players registered.")
        return
    print("\n--- PLAYER ROSTER ---")
    for player in data["players"]:
        print("ID: {} | {} | Age: {} | Role: {} | Team: {}".format(
            player["id"], player["name"], player["age"], player["role"],
            team_name(player["team_id"])))


def schedule_match():
    list_teams()
    if len(data["teams"]) < 2:
        print("Register at least two teams before scheduling a match.")
        return
    home_id = read_int("Team A ID: ", 1)
    away_id = read_int("Team B ID: ", 1)
    if not find_team(home_id) or not find_team(away_id):
        print("One or both team IDs do not exist.")
        return
    if home_id == away_id:
        print("A team cannot play against itself.")
        return
    date = input("Match date (YYYY-MM-DD): ").strip()
    venue = input("Venue: ").strip()
    match = {"id": data["next_match_id"], "home_id": home_id,
             "away_id": away_id, "date": date, "venue": venue,
             "status": "Scheduled", "home_score": None, "away_score": None}
    data["matches"].append(match)
    data["next_match_id"] += 1
    save_data()
    print("Match scheduled successfully. Match ID:", match["id"])


def list_matches():
    if not data["matches"]:
        print("No matches scheduled.")
        return
    print("\n--- MATCH FIXTURES ---")
    for match in data["matches"]:
        if match["status"] == "Completed":
            score = "{} - {}".format(match["home_score"], match["away_score"])
        else:
            score = "vs"
        print("ID: {} | {} {} {} | Date: {} | Venue: {} | {}".format(
            match["id"], team_name(match["home_id"]), score,
            team_name(match["away_id"]), match["date"], match["venue"],
            match["status"]))


def update_score():
    list_matches()
    if not data["matches"]:
        return
    match_id = read_int("Enter match ID to update: ", 1)
    match = None
    for item in data["matches"]:
        if item["id"] == match_id:
            match = item
            break
    if not match:
        print("Match ID not found.")
        return
    match["home_score"] = read_int("Score for {}: ".format(team_name(match["home_id"])))
    match["away_score"] = read_int("Score for {}: ".format(team_name(match["away_id"])))
    match["status"] = "Completed"
    save_data()
    print("Score updated successfully.")


def standings():
    table = {}
    for team in data["teams"]:
        table[team["id"]] = {"name": team["name"], "played": 0, "won": 0,
                             "lost": 0, "draw": 0, "points": 0}
    for match in data["matches"]:
        if match["status"] != "Completed":
            continue
        home_id = match["home_id"]
        away_id = match["away_id"]
        if home_id not in table or away_id not in table:
            continue
        home = table[home_id]
        away = table[away_id]
        home["played"] += 1
        away["played"] += 1
        if match["home_score"] > match["away_score"]:
            home["won"] += 1
            home["points"] += 3
            away["lost"] += 1
        elif match["home_score"] < match["away_score"]:
            away["won"] += 1
            away["points"] += 3
            home["lost"] += 1
        else:
            home["draw"] += 1
            away["draw"] += 1
            home["points"] += 1
            away["points"] += 1
    ordered = sorted(table.values(),
                     key=lambda row: (-row["points"], -row["won"], row["name"].lower()))
    print("\n--- TOURNAMENT STANDINGS ---")
    if not ordered:
        print("No teams registered.")
    for rank, row in enumerate(ordered, 1):
        print("{}. {} | Played: {} | Won: {} | Lost: {} | Draw: {} | Points: {}".format(
            rank, row["name"], row["played"], row["won"], row["lost"],
            row["draw"], row["points"]))


def delete_match():
    list_matches()
    if not data["matches"]:
        return
    match_id = read_int("Enter match ID to delete: ", 1)
    for index, match in enumerate(data["matches"]):
        if match["id"] == match_id:
            del data["matches"][index]
            save_data()
            print("Match deleted.")
            return
    print("Match ID not found.")


def main():
    while True:
        print("\n========== SPORTS TOURNAMENT MANAGER ==========")
        print("1. Add team")
        print("2. View teams")
        print("3. Register player")
        print("4. View players")
        print("5. Schedule match")
        print("6. View matches")
        print("7. Enter/update match score")
        print("8. View tournament standings")
        print("9. Delete match")
        print("0. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            add_team()
        elif choice == "2":
            list_teams()
        elif choice == "3":
            add_player()
        elif choice == "4":
            list_players()
        elif choice == "5":
            schedule_match()
        elif choice == "6":
            list_matches()
        elif choice == "7":
            update_score()
        elif choice == "8":
            standings()
        elif choice == "9":
            delete_match()
        elif choice == "0":
            print("Thank you for using Sports Tournament Manager!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
