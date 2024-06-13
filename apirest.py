from flask import Flask, request, jsonify, abort, g
import sqlite3

app = Flask(__name__)

# Função para conectar ao banco de dados
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('database.db')
        g.db.row_factory = sqlite3.Row
    return g.db

# Função para fechar a conexão com o banco de dados
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()

# Código para criar o banco de dados e a tabela, se não existirem
def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trips (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                destination TEXT NOT NULL,
                start_date TEXT,
                end_date TEXT
            )
        ''')
        db.commit()
        cursor.close()

@app.route('/add_trip', methods=['POST'])
def add_trip():
    if not request.json or not 'destination' in request.json:
        abort(400)
    trip_data = (request.json['destination'], request.json.get('start_date', ""), request.json.get('end_date', ""))
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO trips (destination, start_date, end_date) VALUES (?, ?, ?)', trip_data)
    db.commit()
    trip_id = cursor.lastrowid
    cursor.close()
    return jsonify({"id": trip_id}), 201

# Rota para obter todas as viagens
@app.route('/trips', methods=['GET'])
def get_trips():
    db = get_db()
    trips_data = db.execute('SELECT * FROM trips').fetchall()
    trips = [dict(trip) for trip in trips_data]
    return jsonify(trips)

# Rota para obter uma viagem específica
@app.route('/trips/<int:trip_id>', methods=['GET'])
def get_trip(trip_id):
    db = get_db()
    trip_data = db.execute('SELECT * FROM trips WHERE id = ?', (trip_id,)).fetchone()
    if trip_data is None:
        abort(404)
    trip = dict(trip_data)
    return jsonify(trip)

# Rota para adicionar uma nova viagem 
@app.route('/trips', methods=['POST'])
def create_trip():
    if not request.json or not 'destination' in request.json:
        abort(400)
    trip_data = (request.json['destination'], request.json.get('start_date', ""), request.json.get('end_date', ""))
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO trips (destination, start_date, end_date) VALUES (?, ?, ?)', trip_data)
    db.commit()
    trip_id = cursor.lastrowid
    cursor.close()
    return jsonify({"id": trip_id}), 201

# Rota para atualizar uma viagem existente
@app.route('/trips/<int:trip_id>', methods=['PUT'])
def update_trip(trip_id):
    trip_data = (request.json.get('destination'), request.json.get('start_date'), request.json.get('end_date'), trip_id)
    db = get_db()
    cursor = db.cursor()
    cursor.execute('UPDATE trips SET destination = ?, start_date = ?, end_date = ? WHERE id = ?', trip_data)
    db.commit()
    cursor.close()
    return '', 204

# Rota para excluir uma viagem
@app.route('/trips/<int:trip_id>', methods=['DELETE'])
def delete_trip(trip_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM trips WHERE id = ?', (trip_id,))
    db.commit()
    cursor.close()
    return '', 204

# Rota padrão
@app.route('/')
def index():
    return 'PARA VER AS VIAGENS JA LISTADAS, adicione "/trips" ao seu link'

# Inicializar o banco de dados ao iniciar a aplicação
init_db()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
