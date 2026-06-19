import os
import time
import sqlalchemy.exc
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

MYSQL_HOST = os.environ.get('MYSQL_HOST')
MYSQL_USER = os.environ.get('MYSQL_USER')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:3306/{MYSQL_DATABASE}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Elemento(db.Model):
    __tablename__ = 'elementi'
    id = db.Column(db.Integer, primary_key=True)
    chiave = db.Column(db.String(100), nullable=False)
    valore = db.Column(db.String(200), nullable=False)


with app.app_context():
    for i in range(10):
        try:
            db.create_all()
            print("Connessione al database riuscita e tabelle verificate!")
            break
        except sqlalchemy.exc.OperationalError:
            print(f"Database non ancora pronto. Tentativo {i+1}/10. Riprovo tra 3 secondi...")
            time.sleep(3)
    else:
        raise RuntimeError("Impossibile connettersi al database dopo 10 tentativi.")


@app.route('/', methods=['GET'])
def index():
    elementi = Elemento.query.all()
    return render_template('index.html', elementi=elementi)


@app.route('/aggiungi', methods=['POST'])
def aggiungi():
    chiave = request.form.get('chiave')
    valore = request.form.get('valore')
    if chiave and valore:
        nuovo_elemento = Elemento(chiave=chiave, valore=valore)
        db.session.add(nuovo_elemento)
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/elimina/<int:id>', methods=['DELETE'])
def elimina(id):
    elemento = Elemento.query.get_or_404(id)
    db.session.delete(elemento)
    db.session.commit()
    return {"success": True}, 200


if __name__ == '__main__':
    app.run()