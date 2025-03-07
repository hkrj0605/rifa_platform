from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Ruta principal
@app.route('/')
def index():
    conn = sqlite3.connect('rifas.db')
    c = conn.cursor()
    c.execute("SELECT * FROM rifas")
    rifas = c.fetchall()
    conn.close()
    return render_template('index.html', rifas=rifas)

# Ruta para crear una nueva rifa
@app.route('/crear_rifa', methods=['GET', 'POST'])
def crear_rifa():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        total_boletos = int(request.form['total_boletos'])
        
        conn = sqlite3.connect('rifas.db')
        c = conn.cursor()
        c.execute("INSERT INTO rifas (nombre, descripcion, total_boletos) VALUES (?, ?, ?)",
                  (nombre, descripcion, total_boletos))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('crear_rifa.html')

# Ruta para participar en una rifa
@app.route('/participar/<int:rifa_id>', methods=['GET', 'POST'])
def participar(rifa_id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        boleto = int(request.form['boleto'])
        
        conn = sqlite3.connect('rifas.db')
        c = conn.cursor()
        
        # Verificar si el boleto ya está vendido
        c.execute("SELECT * FROM participantes WHERE rifa_id = ? AND boleto = ?", (rifa_id, boleto))
        if c.fetchone():
            return "Este boleto ya está vendido."
        
        # Registrar participante
        c.execute("INSERT INTO participantes (rifa_id, nombre, boleto) VALUES (?, ?, ?)",
                  (rifa_id, nombre, boleto))
        
        # Actualizar boletos vendidos
        c.execute("UPDATE rifas SET boletos_vendidos = boletos_vendidos + 1 WHERE id = ?", (rifa_id,))
        
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    return render_template('participar.html', rifa_id=rifa_id)

# Ruta para realizar el sorteo
@app.route('/sorteo/<int:rifa_id>')
def sorteo(rifa_id):
    conn = sqlite3.connect('rifas.db')
    c = conn.cursor()
    
    # Obtener todos los boletos vendidos
    c.execute("SELECT boleto FROM participantes WHERE rifa_id = ?", (rifa_id,))
    boletos = c.fetchall()
    
    # Seleccionar un ganador al azar
    import random
    ganador = random.choice(boletos)[0]
    
    conn.close()
    return render_template('sorteo.html', ganador=ganador)

if __name__ == "__main__":
    app.run(debug=True)
