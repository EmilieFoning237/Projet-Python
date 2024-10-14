from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# Template HTML
html_template = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tirage au sort - Ligue des Champions</title>
    <style>
        body {
            font-family: Arial, sans-serif;
        }
        h1 {
            text-align: center;
            margin-top: 20px;
        }
        #draw-results {
            width: 50%;
            margin: 20px auto;
            border-collapse: collapse;
        }
        #draw-results td, #draw-results th {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: center;
        }
        button {
            display: block;
            margin: 20px auto;
            padding: 10px 20px;
            font-size: 16px;
        }
    </style>
</head>
<body>

<h1>Tirage au sort - Ligue des Champions</h1>

<button onclick="generateDraw()">Effectuer le tirage au sort</button>

<table id="draw-results">
    <thead>
        <tr>
            <th>Équipe à domicile</th>
            <th>Équipe à l'extérieur</th>
        </tr>
    </thead>
    <tbody id="results-body">
        <!-- Les résultats du tirage apparaîtront ici -->
    </tbody>
</table>

<button onclick="exportPDF()">Exporter en PDF</button>

<script>
    function generateDraw() {
        fetch('/generate_draw')
            .then(response => response.json())
            .then(data => {
                const resultsBody = document.getElementById('results-body');
                resultsBody.innerHTML = ''; // Réinitialiser le tableau

                data.matches.forEach(match => {
                    const row = document.createElement('tr');
                    const homeCell = document.createElement('td');
                    const awayCell = document.createElement('td');

                    homeCell.textContent = match.home;
                    awayCell.textContent = match.away;

                    row.appendChild(homeCell);
                    row.appendChild(awayCell);
                    resultsBody.appendChild(row);
                });
            })
            .catch(error => console.error('Erreur:', error));
    }

    function exportPDF() {
        alert("PDF exporté (logique à compléter) !");
        // Implémentation de l'exportation PDF à ajouter ici
    }
</script>

</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/generate_draw')
def generate_draw():
    # Logique pour générer le tirage au sort
    matches = [
        {'home': 'Équipe A', 'away': 'Équipe B'},
        {'home': 'Équipe C', 'away': 'Équipe D'},
        # Ajoutez d'autres matchs ici
    ]
    return jsonify(matches=matches)

if __name__ == '__main__':
    app.run(debug=True)
