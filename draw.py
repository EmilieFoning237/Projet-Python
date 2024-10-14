import random
import json
from fpdf import FPDF

class Team:
    """Classe représentant une équipe."""
    def __init__(self, name, country, league, pot):
        self.name = name
        self.country = country
        self.league = league
        self.pot = pot

class Draw:
    """Classe principale pour gérer le tirage au sort."""
    def __init__(self, teams_data):
        self.teams = self.load_teams(teams_data)
        self.groups = []
        self.matches = {}

    def load_teams(self, teams_data):
        """Charge les équipes à partir de la donnée JSON et crée des objets Team."""
        teams = []
        for team_data in teams_data:
            team = Team(team_data['nom'], team_data['pays'], team_data['championnat'], team_data['chapeau'])
            teams.append(team)
        return teams

    def make_draw(self):
        """Effectue le tirage en respectant les règles des chapeaux et championnats."""
        # Répartir les équipes par chapeau
        pots = self.group_teams_by_pot()
        
        # Mélanger les équipes à l'intérieur de chaque chapeau
        for pot in pots:
            random.shuffle(pots[pot])

        # Assigner 2 équipes de chaque chapeau, respecter les règles de championnat
        for team in self.teams:
            home_matches, away_matches = self.assign_opponents(team, pots)
            self.matches[team.name] = {
                'chapeau': team.pot,
                'league': team.league,
                'home': [{'name': opponent.name, 'pot': opponent.pot, 'league': opponent.league} for opponent in home_matches],
                'away': [{'name': opponent.name, 'pot': opponent.pot, 'league': opponent.league} for opponent in away_matches]
            }
    
    def group_teams_by_pot(self):
        """Regroupe les équipes par chapeau."""
        pots = {1: [], 2: [], 3: [], 4: []}
        for team in self.teams:
            pots[team.pot].append(team)
        return pots

    def assign_opponents(self, team, pots):
        """Assigne 8 adversaires (2 par chapeau) à une équipe en respectant les règles."""
        home_matches = []
        away_matches = []
        league_count = {}

        # Pour chaque chapeau, choisir 2 adversaires
        for pot in pots:
            available_teams = [t for t in pots[pot] if t != team and t.league != team.league]
            random.shuffle(available_teams)
            assigned_teams = available_teams[:2]

            # Répartir entre domicile et extérieur
            for i, opponent in enumerate(assigned_teams):
                if len(home_matches) < 4:
                    home_matches.append(opponent)
                else:
                    away_matches.append(opponent)

                # Compter le nombre d'équipes du même championnat déjà assignées
                league_count[opponent.league] = league_count.get(opponent.league, 0) + 1
                if league_count[opponent.league] > 2:
                    assigned_teams.remove(opponent)

        return home_matches, away_matches

    def save_results(self, filename):
        """Sauvegarde les résultats du tirage dans un fichier JSON."""
        results = {'matches': self.matches}
        with open(filename, 'w') as file:
            json.dump(results, file, indent=4)
        print(f"Results saved to {filename}")

class DrawPDF(FPDF):
    """Classe pour générer le PDF avec les résultats du tirage au sort."""
    
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
    
    def header(self):
        """En-tête du document PDF."""
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Tirage au sort - Ligue des Champions', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        """Pied de page du document PDF."""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_draw(self, matches):
        """Ajoute les résultats du tirage au document PDF."""
        self.add_page()
        self.set_font('Arial', '', 12)
        for team, details in matches.items():
            self.cell(0, 10, f'{team} (Chapeau {details["chapeau"]}, Ligue: {details["league"]})', ln=True)
            self.cell(0, 10, 'Matchs à domicile:', ln=True)
            for opponent in details['home']:
                self.cell(0, 10, f'  - {opponent["name"]} (Chapeau {opponent["pot"]}, Ligue: {opponent["league"]})', ln=True)
            self.cell(0, 10, 'Matchs à l\'extérieur:', ln=True)
            for opponent in details['away']:
                self.cell(0, 10, f'  - {opponent["name"]} (Chapeau {opponent["pot"]}, Ligue: {opponent["league"]})', ln=True)
            self.ln(10)

# Exemple d'utilisation
if __name__ == "__main__":
    with open("data/teams.json", "r") as file:
        teams_data = json.load(file)

    draw = Draw(teams_data)
    draw.make_draw()
    draw.save_results('tournament_results.json')

    # Générer le PDF
    pdf = DrawPDF()
    pdf.add_draw(draw.matches)
    pdf.output('draw_results.pdf')
