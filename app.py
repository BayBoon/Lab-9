from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Game {self.game} ({self.year})>'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        game_name = request.form['game']
        game_year = request.form['year']
        
        try:
            game_year = int(game_year)
            if game_year > datetime.now().year:
                raise ValueError
        except ValueError:
            return render_template('index.html', games=Game.query.all(), error="Please enter a valid year")
        
        new_game = Game(game=game_name, year=game_year)
        db.session.add(new_game)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('index.html', games=Game.query.all())

@app.route('/clear', methods=['POST'])
def clear():
    db.session.query(Game).delete()
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=1234)