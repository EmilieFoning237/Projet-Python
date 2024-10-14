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
        self.groups = self.create_groups()
        self.matches = {}

    def load_teams(self, teams_data):
        """Charge les équipes à partir de la donnée JSON et crée des objets Team."""
        teams = []
        for team_data in teams_data:
            team = Team(team_data['nom'], team_data['pays'], team_data['championnat'], team_data['chapeau'])
            teams.append(team)
        return teams

    def create_groups(self):
        """Crée les groupes de matches."""
        groups = [[] for _ in range(8)]  # 8 groupes de matches
        return groups

    def make_draw(self):
        """Effectue le tirage en respectant les règles des chapeaux et championnats."""
        pots = self.group_teams_by_pot()

        # Mélanger les équipes à l'intérieur de chaque chapeau
        for pot in pots:
            random.shuffle(pots[pot])

        # Assigner une équipe de chaque chapeau à chaque groupe, en respectant les règles de championnat
        for i in range(8):
            for pot in range(1, 5):
                available_teams = [t for t in pots[pot] if t not in self.groups[i] and (len(self.groups[i]) == 0 or t.league != self.groups[i][0].league)]
                if available_teams:
                    team = random.choice(available_teams)
                    self.groups[i].append(team)
                    self.assign_opponents(team)

    def group_teams_by_pot(self):
        """Regroupe les équipes par chapeau."""
        return {pot: [team for team in self.teams if team.pot == pot] for pot in range(1, 5)}

    def assign_opponents(self, team):
        """Assigne les adversaires à une équipe en respectant les règles."""
        group = self.groups[self.groups.index(team)]
        home_matches = []
        away_matches = []
        league_count = {}

        # Pour chaque chapeau, choisir 2 adversaires
        for pot in range(1, 5):
            available_teams = [t for t in self.groups[self.groups.index(team)] if t != team and t.pot == pot and t.league != team.league]
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

        self.matches[team.name] = {
            'chapeau': team.pot,
            'league': team.league,
            'home': [{'name': opponent.name, 'pot': opponent.pot, 'league': opponent.league} for opponent in home_matches],
            'away': [{'name': opponent.name, 'pot': opponent.pot, 'league': opponent.league} for opponent in away_matches]
        }

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
        self.add_page()
        self.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)  # Assurez-vous que 'DejaVuSans.ttf' est dans votre projet
        self.set_font('DejaVu', '', 12)

    def header(self):
        """En-tête du document PDF."""
        self.set_font('DejaVu', 'B', 12)
        self.cell(0, 10, 'Tirage au sort - Ligue des Champions', 0, 1, 'C')
        self.ln(10)

    def generate_pdf(self, matches):
        """Génère le corps du document PDF."""
        for team, match_data in matches.items():
            self.set_font('DejaVu', 'B', 14)
            self.cell(0, 10, team, 0, 1, 'L')
            self.set_font('DejaVu', '', 12)
            self.cell(0, 5, f"Chapeau {match_data['chapeau']} - {match_data['league']}", 0, 1, 'L')

            self.cell(0, 5, "Matchs à domicile:", 0, 1, 'L')
            for opponent in match_data['home']:
                self.cell(0, 5, f"- {opponent['name']} (Chapeau {opponent['pot']} - {opponent['league']})", 0, 1, 'L')

            self.cell(0, 5, "Matchs à l'extérieur:", 0, 1, 'L')
            for opponent in match_data['away']:
                self.cell(0, 5, f"- {opponent['name']} (Chapeau {opponent['pot']} - {opponent['league']})", 0, 1, 'L')

            self.ln(10)

# Chargement des données des équipes
with open('teams.json', 'r') as f:
    teams_data = json.load(f)

# Création de l'objet Draw
draw = Draw(teams_data)

# Exécution du tirage au sort
draw.make_draw()

# Sauvegarde des résultats dans un fichier JSON
draw.save_results('results.json')

# Génération du PDF
pdf = DrawPDF()
pdf.header()
pdf.generate_pdf(draw.matches)
pdf.output('draw_results.pdf')
