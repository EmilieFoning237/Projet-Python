# Ce module contient les instances de vos classes back-end et front-end
from draw import Draw, DrawPDF
import json

# Charger les équipes depuis le fichier JSON
with open("data/teams.json", "r") as file:
    teams = json.load(file)

# Créer une instance de la classe Draw pour gérer le tirage au sort
draw = Draw(teams)

# Effectuer le tirage au sort
draw.make_draw()

# Sauvegarder les résultats du tirage au format JSON
draw.save_results('tournament_results.json')

# Générer le fichier PDF avec les résultats du tirage
pdf = DrawPDF()
pdf.add_draw(draw.matches)
pdf.output('draw_results.pdf')

print("Le tirage au sort a été effectué et les fichiers JSON et PDF ont été générés.")
