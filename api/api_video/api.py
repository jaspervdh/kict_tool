from flask import Flask, render_template, jsonify, request
from dartspel import DartVragenSpel

app = Flask(__name__)
spel = DartVragenSpel("vragenlijst.csv")

@app.route('/')
def home():
    """Laadt de HTML-pagina wanneer de server draait."""
    return render_template('index.html')

@app.route('/vraag', methods=['GET'])
def geef_vraag():
    try:
        score = int(request.args.get('nummer'))
        perspectief, vraag = spel.kies_vraag_voor_score(score)
        if perspectief and vraag:
            return jsonify({'perspectief': perspectief, 'vraag': vraag})
        else:
            return jsonify({'error': 'Ongeldig vraagnummer'}), 400

    
    except ValueError:
        return jsonify({'error': 'Vraagnummer moet een integer zijn'}), 400
    

if __name__ == '__main__':
    app.run(debug=True)