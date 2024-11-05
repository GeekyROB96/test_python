import sqlite3
from sqlite3 import Error
import os
class FictionalChocoHouse:
    def __init__(self,db_file="chocolate.db"):
        self.db_file=os.path.join(os.path.dirname(os.path.abspath(__file__)),db_file)
        
    def connection(self):
        """Create a database connection"""
        try:
            conn=sqlite3.connect(self.db_file)
            return conn
        except Error as e:
            print(f"There's an Error connecting to the database:{e}")
            return None 
    
    def init_db(self):
        conn = self.connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS flavours (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        description TEXT,
                        is_seasonal BOOLEAN,
                        season TEXT
                    )
                """)
                conn.commit()
            except Error as e:
                print(f"Error initializing database: {e}")
            finally:
                conn.close()
        
#----ADD FLAVOUR----
    def add_flavour(self,name,description,is_seasonal=False,season=None):
        """Add a new flavour to DB"""
        sql="""INSERT INTO flavours(name,description,is_seasonal,season) VALUES(?,?,?,?)"""
        conn=self.connection()
        try:
            cursor=conn.cursor()
            cursor.execute(sql,(name,description,is_seasonal,season))
            conn.commit()
            print("Successfully added flavour:{name}")
        except Error as e:
            print(f"Oops! error adding the flavour:{e}")
            return None
        finally:
            conn.close()
    
    #RETRIVE FLAVOURS FROM DB      
    def get_all_flavours(self):
        """Retrieve all flavours from DB"""
        sql="""SELECT * FROM flavours"""
        conn=self.connection()
        try:
            cursor=conn.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
        except Error as e:
            print(f"Oops! error retrieving flavours from DB:{e}")
            return []
        finally:
            conn.close()
        
    def get_flavour_by_name(self,name):
        """Retrieve flavour by name from DB"""
        sql="""SELECT * FROM flavours WHERE name=?"""
        conn=self.connection()
        try:
            cursor=conn.cursor()
            cursor.execute(sql,(name,))
            return cursor.fetchone()
        except Error as e:
            print(f"Error retrieving flavour:{e}")
            return None
        finally:
            conn.close()
            
            
    #------ADDING THE INGREDIENT------
    def add_ingredient(self,name,qunatity,unit,allergen_info=None):
        """Add a new ingredient to the DB"""
        sql="""INSERT INTO ingredients(name,quantity,unit,allergen_info) VALUES(?,?,?,?)"""
        conn=self.connection()
        try:
            cursor=conn.cursor()
            cursor.execute(sql,(name,qunatity,unit,allergen_info))
            conn.commit()
            print(f"Successfully added ingredient:{name}")
            return cursor.lastrowid
        except Error as e:
            print(f"Error adding ingredients:{e}")
            return None
        finally:
            conn.close()
            
    def update_ingredient_quantity(self,ingredient_id,new_quant):
        """Update the quantity of an ingredient"""
        sql="""UPDATE ingredients SET quantity=? WHERE id=?"""
        conn=self.connection()
        try:
            cursor=conn.cursor()
            cursor.execute(sql,(new_quant,ingredient_id))
            conn.commit()
            print(f"Successfully updated quantity of ingredient:{ingredient_id}")
            return True
        except Error as e:
            print(f"Error updating ingredient quantity:{e}")
            return False
        finally:
            conn.close()
    
    def get_all_ingredients(self):
        """Retrieve all ingredients from DB"""
        sql="""SELECT * FROM ingredients"""
        conn=self.connection()
        try:
            cursor=conn.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
        except Error as e:
            print(f"Error retrieving ingredients:{e}")
            return []
        finally:   
            conn.close()
            
    #---FLAVOUR INGREDIENT------#
    def link_flavour_ingredient(self,ingredient_id,flavour_id):
        """Link a flavour to an ingredient"""
        sql="""INSERT INTO flavour_ingredients(ingredient_id,flavour_id) VALUES(?,?)"""
        conn=self.connection()
        try:
            cursor=conn.cursor()
            cursor.execute(sql,(ingredient_id,flavour_id))
            conn.commit()
            print(f"Successfully linked flavour{flavour_id} with ingredient:{ingredient_id}")
            return True
        except Error as e:
            print(f"Error linking flavour ingredient:{e}")
            return False
        finally:
            conn.close()
            
    def get_flavour_ingredients(self,flavour_id):
        """Retrieve all ingredients for a specific flavour"""
        sql="""
        SELECT i.* From ingredients i
        JOIN flavour_ingredients fi ON i.id = fi.ingredient_id
        WHERE fi.flavour_id = ?
        """
        # all the values should passed in the query should be in tuple
        conn=self.connection()
        try:
            cursor=conn.cursor()
            cursor.execute(sql,(flavour_id))
            return cursor.fetchall()
        except Error as e:
            print(f"Error retrieving flavour ingredients:{e}")
            return []
        finally:
            conn.close()
            
    #----CUSTOMER SUGGESTION OPERATION----#
    def add_suggestion(self,flavour_name,description,allergen_concerns=None):
        """Add a new customer suggestion"""
        sql="""INSERT INTO suggestions(flavour_name,description,allergen_concerns) VALUES(?,?,?)"""
        conn=self.connection()
        try:
            cursor=conn.cursor()
            cursor.execute(sql,(flavour_name,description,allergen_concerns))
            conn.commit()
            print(f"Successfully added suggestion:{flavour_name}")
            return cursor.lastrowid
        
        except Error as e:
            print(f"Error adding suggestion:{e}")
            return None
        
        finally:
            conn.close()
            
            
    def get_all_suggestions(self):
        """Retrieve all customer suggestions"""
        sql="""SELECT * FROM suggestions"""
        conn=self.connection()
        try:
            cursor=conn.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
        except Error as e:
            print(f"Error retrieving suggestions:{e}")
            return []
        finally:
            conn.close()
            
    def update_suggestion_status(self,suggestion_id,new_status):
        """Update the status of a customer suggestion"""
        sql="""UPDATE suggestions SET status=? WHERE id=?"""
        conn=self.connection()
        try:
            cursor=conn.cursor()
            cursor.execute(sql,(new_status,suggestion_id))
            conn.commit()
            print(f"Successfully updated suggestion status:{suggestion_id}")
            return True
        except Error as e:
            print(f"Error updating suggestion status:{e}")
            return False
        finally:
            conn.close()
            

    
            

        
        
    
    
    
    