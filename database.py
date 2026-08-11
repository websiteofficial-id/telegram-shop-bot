import sqlite3

DB="database/shop.db"

def conn():
    return sqlite3.connect(DB)

def init_db():
    c=conn()
    cur=c.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT DEFAULT '',
        price INTEGER NOT NULL,
        stock INTEGER DEFAULT 0,
        category TEXT DEFAULT 'Umum'
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        username TEXT,
        items TEXT NOT NULL,
        total INTEGER NOT NULL,
        status TEXT DEFAULT 'Pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    if cur.execute("SELECT COUNT(*) FROM products").fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO products(name,description,price,stock,category) VALUES(?,?,?,?,?)",
            [
                ("Produk Demo 1","Contoh produk toko.",10000,10,"Umum"),
                ("Produk Demo 2","Contoh produk lainnya.",25000,5,"Umum"),
            ]
        )
    c.commit()
    c.close()

def products():
    c=conn()
    rows=c.execute("SELECT id,name,description,price,stock,category FROM products ORDER BY id DESC").fetchall()
    c.close()
    return rows

def add_product(name, description, price, stock, category="Umum"):
    c=conn()
    c.execute("INSERT INTO products(name,description,price,stock,category) VALUES(?,?,?,?,?)",
              (name,description,price,stock,category))
    c.commit(); c.close()

def delete_product(pid):
    c=conn()
    c.execute("DELETE FROM products WHERE id=?", (pid,))
    c.commit(); c.close()

def add_order(user_id, username, items, total):
    c=conn()
    cur=c.execute("INSERT INTO orders(user_id,username,items,total) VALUES(?,?,?,?)",
                  (user_id,username,items,total))
    oid=cur.lastrowid
    c.commit(); c.close()
    return oid

def orders():
    c=conn()
    rows=c.execute("SELECT id,user_id,username,items,total,status,created_at FROM orders ORDER BY id DESC").fetchall()
    c.close()
    return rows
