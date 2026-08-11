import os
import sqlite3


# =========================
# DATABASE CONFIG
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, "database")
DB = os.path.join(DATABASE_DIR, "shop.db")


# =========================
# CONNECTION
# =========================

def conn():
    os.makedirs(DATABASE_DIR, exist_ok=True)

    return sqlite3.connect(DB)


# =========================
# INITIALIZE DATABASE
# =========================

def init_db():

    c = conn()
    cur = c.cursor()

    # =========================
    # PRODUCTS TABLE
    # =========================

    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT DEFAULT '',
            price INTEGER NOT NULL,
            stock INTEGER DEFAULT 0,
            category TEXT DEFAULT 'Umum'
        )
    """)

    # =========================
    # ORDERS TABLE
    # =========================

    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            username TEXT,
            items TEXT NOT NULL,
            total INTEGER NOT NULL,
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # =========================
    # DEMO PRODUCTS
    # =========================

    product_count = cur.execute(
        "SELECT COUNT(*) FROM products"
    ).fetchone()[0]

    if product_count == 0:

        cur.executemany(
            """
            INSERT INTO products
            (name, description, price, stock, category)
            VALUES (?, ?, ?, ?, ?)
            """,
            [
                (
                    "Produk Demo 1",
                    "Contoh produk toko.",
                    10000,
                    10,
                    "Umum"
                ),
                (
                    "Produk Demo 2",
                    "Contoh produk lainnya.",
                    25000,
                    5,
                    "Umum"
                )
            ]
        )

    c.commit()
    c.close()


# =========================
# GET PRODUCTS
# =========================

def products():

    c = conn()

    rows = c.execute(
        """
        SELECT
            id,
            name,
            description,
            price,
            stock,
            category
        FROM products
        ORDER BY id DESC
        """
    ).fetchall()

    c.close()

    return rows


# =========================
# ADD PRODUCT
# =========================

def add_product(
    name,
    description,
    price,
    stock,
    category="Umum"
):

    c = conn()

    c.execute(
        """
        INSERT INTO products
        (name, description, price, stock, category)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            name,
            description,
            price,
            stock,
            category
        )
    )

    c.commit()
    c.close()


# =========================
# DELETE PRODUCT
# =========================

def delete_product(product_id):

    c = conn()

    c.execute(
        "DELETE FROM products WHERE id = ?",
        (product_id,)
    )

    c.commit()
    c.close()


# =========================
# ADD ORDER
# =========================

def add_order(
    user_id,
    username,
    items,
    total
):

    c = conn()

    cursor = c.execute(
        """
        INSERT INTO orders
        (user_id, username, items, total)
        VALUES (?, ?, ?, ?)
        """,
        (
            user_id,
            username,
            items,
            total
        )
    )

    order_id = cursor.lastrowid

    c.commit()
    c.close()

    return order_id


# =========================
# GET ORDERS
# =========================

def orders():

    c = conn()

    rows = c.execute(
        """
        SELECT
            id,
            user_id,
            username,
            items,
            total,
            status,
            created_at
        FROM orders
        ORDER BY id DESC
        """
    ).fetchall()

    c.close()

    return rows
