class Player:
    def __init__(self, name, team):
        self.name = name
        self.team = team
        
class Team:
    def __init__(self, name, players):
        self.name = name
        self.players = players
        
    def add_player(self, player):
        self.players.append(player)
        
    def remove_player(self, player):
        self.players.remove(player)

class Match:
    def __init__(self, team1, team2, division):
        self.team1 = team1
        self.team2 = team2
        self.division = division
        self.winner = ""
        self.is_finished = False

    def get_winner(self):
        if not self.is_finished:
            raise ValueError("A winner can be found after the match ends")
        return self.winner

    def set_winner(self, winner_name):
        if winner_name not in [self.team1, self.team2]:
            raise ValueError("Winner must be one of the teams in the match.")
        self.winner = winner_name
        self.is_finished = True
class Organizer:
    def __init__(self, division):
        self.division = division
        self.matches = []

    def insert_match(self, match):
        self.matches.append(match)

    def remove_match(self, match):
        self.matches.remove(match)

    def advance_to_next_division(self):
        winners = []
        for match in self.matches:
            if not match.is_finished:
                raise ValueError("All matches must be finished to advance to the next division.")
            winners.append(match.get_winner())


        self.division += 1
        next_division_matches = []


        for i in range(0, len(winners), 2):
            if i + 1 < len(winners):
                next_match = Match(winners[i], winners[i + 1], self.division)
                next_division_matches.append(next_match)

        self.matches = next_division_matches

    def declare_tournament_winner(self):
        if len(self.matches) == 1 and self.matches[0].is_finished:
            return self.matches[0].get_winner()
        raise ValueError("Can't declare winner before the Tournament ends")
    

players_team1 = [Player("Jack", "Falcons"), Player("Joshua", "Falcons")]
players_team2 = [Player("Steven", "Hawks"), Player("Chuck", "Hawks")]
players_team3 = [Player("Martin", "Sea"), Player("Carl", "Sea")]
players_team4 = [Player("Gelbert", "Fire"), Player("Harold", "Fire")]
team1 = Team("Team A", players_team1)
team2 = Team("Team B", players_team2)
team3 = Team("Team C", players_team3)
team4 = Team("Team D", players_team4)

# Matches for Division 1
match1 = Match(team1, team2, 1)
match2 = Match(team3, team4, 1)

# Create Organizer and add matches
organizer = Organizer(1)
organizer.insert_match(match1)
organizer.insert_match(match2)

# Get the winners for this division
match1.set_winner(team1)
match2.set_winner(team4)

# Go to the next division
organizer.advance_to_next_division()

# Matches for next division
next_division_matches = organizer.matches
print(f"Next Division ({organizer.division}) Matches:")
for m in next_division_matches:
    print(f"{m.team1.name} vs {m.team2.name}")

# Set winner for the final match
final_match = next_division_matches[0]
final_match.set_winner(team4)

# Declare the tournament winner
tournament_winner = organizer.declare_tournament_winner()
print(f"Tournament Winner: {tournament_winner.name}")