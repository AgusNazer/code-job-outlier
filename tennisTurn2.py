class Team:
    def __init__(self, name):
        self.name = name
        self.players = []
        self.wins = 0
        self.losses = 0

    def add_player(self, player_name):
        if player_name in self.players:
            print(f"Player {player_name} is already in team {self.name}.")
        else:
            self.players.append(player_name)

    def remove_player(self, player_name):
        if player_name in self.players:
            self.players.remove(player_name)
        else:
            raise ValueError(f"Player {player_name} is not in team {self.name}")

    def __repr__(self) -> str:
        return f"Team(name={self.name}, players={self.players}, wins={self.wins}, losses={self.losses})"


class Match:
    def __init__(self, team1: Team, team2: Team):
        self.team1 = team1
        self.team2 = team2
        self.winner = None

    def get_winner(self) -> Team:
        if self.winner is None:
            raise ValueError(f"Cannot get winner of match between {self.team1.name} and {self.team2.name} because the match has not ended yet.")
        return self.winner

    def set_winner(self, winner: Team):
        if winner not in [self.team1, self.team2]:
            raise ValueError(f"Winner of match between {self.team1.name} and {self.team2.name} must be one of the teams in the match.")
        self.winner = winner
        if winner == self.team1:
            self.team1.wins += 1
            self.team2.losses += 1
        else:
            self.team2.wins += 1
            self.team1.losses += 1

    def __repr__(self) -> str:
        return f"Match({self.team1.name} vs {self.team2.name}, winner={self.winner.name if self.winner else 'None'})"


class Organizer:
    def __init__(self):
        self.teams = []
        self.matches = []

    def add_team(self, team: Team):
        if team in self.teams:
            print(f"Team {team.name} is already in the tournament.")
        else:
            self.teams.append(team)

    def remove_team(self, team: Team):
        if team in self.teams:
            self.teams.remove(team)
        else:
            raise ValueError(f"Team {team.name} is not in the tournament.")

    def insert_match(self, match: Match):
        if match in self.matches:
            print("This match is already exists.")
        else:
            self.matches.append(match)

    def remove_match(self, match: Match):
        self.matches.remove(match)

    def advance_to_next_division(self):
        # Ensure all matches have a winner
        if not all(match.winner is not None for match in self.matches):
            raise ValueError("All matches must be finished to advance to the next division.")
    
        # Check if there are matches to process
        if len(self.matches) == 0:
            raise ValueError("No matches to process for advancing.")
    
        winners = [match.winner for match in self.matches]
        losers = [team for match in self.matches for team in [match.team1, match.team2] if team not in winners]

        # Eliminate teams with 3 losses
        eliminated_teams = [team for team in losers if team.losses >= 3]
        for team in eliminated_teams:
            self.teams.remove(team)
            print(f"Team {team.name} is eliminated.")

        # Create new matches for the next division
        next_division_matches = []
        for i in range(0, len(winners), 2):
            if i + 1 < len(winners):
                next_match = Match(winners[i], winners[i + 1])
                next_division_matches.append(next_match)

        # Create new matches for the losers
        loser_matches = []
        remaining_losers = [team for team in losers if team not in eliminated_teams]
        for i in range(0, len(remaining_losers), 2):
            if i + 1 < len(remaining_losers):
                next_match = Match(remaining_losers[i], remaining_losers[i + 1])
                loser_matches.append(next_match)

        # Handle cases where no new matches can be created
        if len(next_division_matches) == 0 and len(loser_matches) == 0:
            raise ValueError("Not enough teams to create matches for the next division.")

        self.matches = next_division_matches + loser_matches


    def get_most_consistent_team(self):
        if not self.teams:
            raise ValueError("No teams in the tournament.")
        return max(self.teams, key=lambda team: team.wins / (team.wins + team.losses) if team.wins + team.losses > 0 else 0)

    def __repr__(self) -> str:
        return f"Organizer(teams={self.teams}, matches={self.matches})"


# Create teams
team1 = Team("Team A")
team1.add_player("Jack")
team1.add_player("Joshua")

team2 = Team("Team B")
team2.add_player("Steven")
team2.add_player("Chuck")

team3 = Team("Team C")
team3.add_player("Martin")
team3.add_player("Carl")

team4 = Team("Team D")
team4.add_player("Gelbert")
team4.add_player("Harold")

# Create organizer and add teams
organizer = Organizer()
organizer.add_team(team1)
organizer.add_team(team2)
organizer.add_team(team3)
organizer.add_team(team4)

# Create matches
match1 = Match(team1, team2)
match2 = Match(team3, team4)

# Insert matches
organizer.insert_match(match1)
organizer.insert_match(match2)

# Set winners
match1.set_winner(team1)
match2.set_winner(team4)

# Advance to next division
organizer.advance_to_next_division()

# Print next division matches
print("Next Division Matches:")
for match in organizer.matches:
    print(f"{match.team1.name} vs {match.team2.name}")

# Get most consistent team
most_consistent_team = organizer.get_most_consistent_team()
print(f"Most Consistent Team: {most_consistent_team.name}")