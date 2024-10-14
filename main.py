# Ce module gère le tirage au sort et la génération du PDF des résultats.
from draw import Draw, DrawPDF
import json

# Charger les données des équipes depuis le fichier JSON
try:
    with open("data/teams.json", "r") as file:
        teams_data = json.load(file)
except FileNotFoundError:
    print("Erreur: le fichier teams.json n'a pas été trouvé.")
    exit()
except json.JSONDecodeError:
    print("Erreur: le fichier teams.json n'est pas correctement formaté.")
    exit()

# Créer une instance de la classe Draw pour gérer le tirage au sort
draw = Draw(teams_data)

# Effectuer le tirage au sort
draw.make_draw()

# Sauvegarder les résultats du tirage au format JSON
draw.save_results('tournament_results.json')

# Générer le fichier PDF avec les résultats du tirage
pdf = DrawPDF()
pdf.add_draw(draw.matches)
pdf.output('draw_results.pdf')

print("Le tirage au sort a été effectué et les fichiers JSON et PDF ont été générés.")
