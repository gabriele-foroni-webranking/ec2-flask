import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Recupera le configurazioni passate da Docker Compose (con fallback se vuote)
MYSQL_HOST = os.environ.get('MYSQL_HOST')
MYSQL_USER = os.environ.get('MYSQL_USER')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE')

# Stringa di connessione SQLALCHEMY corretto per pymysql
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:3306/{MYSQL_DATABASE}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modello del Database (La tabella verrà creata su MySQL)
class Elemento(db.Model):
    __tablename__ = 'elementi' # Nome della tabella su MySQL
    id = db.Column(db.Integer, primary_key=True)
    chiave = db.Column(db.String(100), nullable=False)
    valore = db.Column(db.String(200), nullable=False)

# Crea la tabella su MySQL all'avvio se non esiste
with app.app_context():
    db.create_all()

# Rotta principale: Legge dal database MySQL
@app.route('/', methods=['GET'])
def index():
    elementi = Elemento.query.all()
    return render_template('index.html', elementi=elementi)

# Rotta per inserire una nuova coppia chiave:valore
@app.route('/aggiungi', methods=['POST'])
def aggiungi():
    chiave = request.form.get('chiave')
    valore = request.form.get('valore')
    
    if chiave and valore:
        nuovo_elemento = Elemento(chiave=chiave, valore=valore)
        db.session.add(nuovo_elemento)
        db.session.commit()
    
    return redirect(url_for('index'))

# Rotta per eliminare un elemento uno ad uno
@app.route('/elimina/<int:id>', methods=['DELETE'])
def elimina(id):
    elemento_da_cancellare = Elemento.query.get_or_404(id)
    db.session.delete(elemento_da_cancellare)
    db.session.commit()
    
    # Ritorna una stringa vuota e il codice HTTP 200 (Successo)
    return '', 200

if __name__ == '__main__':
    app.run()