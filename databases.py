import sqlite3

def init_db():
    conn = sqlite3.connect('rifas.db')
    c = conn.cursor()
    
    # Crear tabla de rifas
    c.execute('''CREATE TABLE IF NOT EXISTS rifas
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  nombre TEXT NOT NULL,
                  descripcion TEXT,
                  total_boletos INTEGER NOT NULL,
                  boletos_vendidos INTEGER DEFAULT 0)''')
    
    # Crear tabla de participantes
    c.execute('''CREATE TABLE IF NOT EXISTS participantes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  rifa_id INTEGER NOT NULL,
                  nombre TEXT NOT NULL,
                  boleto INTEGER NOT NULL,
                  FOREIGN KEY(rifa_id) REFERENCES rifas(id))''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
