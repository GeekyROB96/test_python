import sqlite3
from sqlite3 import Error
import os
curr_dir=os.path.dirname(os.path.abspath(__file__))
DB_PATH=os.path.join(curr_dir,'chocolate.db')
def create_conn():
    """ create a database connection to the SQLite database"""
    conn = None
    try:
        conn=sqlite3.connect(DB_PATH)
        print("Successfully connected!")
        return conn
    except Error as e:
        print(f"Error connecting to database:{e}")
    return conn

def create_tables(conn):
    """CREATING THE TABLES"""
    
    create_flavours_table = """
    CREATE TABLE IF NOT EXISTS flavours(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        description TEXT,
        is_seasonal INTEGER,
        season TEXT
    );
    """
    
    create_ingredients_table="""
    CREATE TABLE IF NOT EXISTS ingredients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        quantity INTEGER DEFAULT 0,
        unit TEXT,
        allergen_info TEXT
    );
    """
    
    create_flavours_ingredients_table="""
    CREATE TABLE IF NOT EXISTS flavour_ingredients(
        flavour_id INTEGER,
        ingredient_id INTEGER,
        PRIMARY KEY(flavour_id,ingredient_id),
        FOREIGN KEY(flavour_id) REFERENCES flavours(id),
        FOREIGN KEY(ingredient_id) REFERENCES ingredients(id)
    );
    """
    
    create_suggestions_table="""
    CREATE TABLE IF NOT EXISTS suggestions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        flavour_name TEXT NOT NULL,
        description TEXT,
        allergen_concerns TEXT,
        status TEXT DEFAULT 'pending'
    );
    """
    
    try:
        cursor=conn.cursor()
        cursor.execute(create_flavours_table)
        cursor.execute(create_ingredients_table)
        cursor.execute(create_flavours_ingredients_table)
        cursor.execute(create_suggestions_table)
        conn.commit()
        print("Successfully created the tables!")
    except Error as e:
        print(f"Error creating tables: {e}")
        
def init_db():
    """"Initializing the database"""
    conn=create_conn()
    if conn is not None:
        create_tables(conn)
        conn.close()
        
    else:
        print("Error connecting to the database")
        
if __name__ =="__main__":
    init_db()
        
    