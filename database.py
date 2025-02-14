import psycopg2
import json

class Database():
    def __init__(self, config_file='UDP/config.json'):
        self.config_file = config_file
        self.conn = None
        self.cursor = None

        # Retrieve database connection params from config file.
        self.connect_params = self.load_config()
        self.db_params = {
            'dbname': self.connect_params.get('dbname'),
            'user': self.connect_params.get('user')
        }

    # Load configuration from a JSON file
    def load_config(self):
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: the file {self.config_file} was not found")
            return {}
        except json.JSONDecodeError:
            print(f"Error: the file {self.config_file} contains invalid JSON")
            return {}

    # Establish connection to database
    def connect(self):
        try:
            if self.db_params:
                self.conn = psycopg2.connect(**self.db_params)
                self.cursor = self.conn.cursor()
                print("Database connection established.")
            else:
                print("Failed to load database connection parameters")
        except psycopg2.Error as e:
            print(f"Database connection failed: {e}")
    
    # Executes the given query
    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            # returns select query results
            if query.strip().lower().startswith("select"):
                return self.cursor.fetchall() 
            # Commit changes for non-SELECT queries
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"Failed to run query: {e}")
            return None
    
    # Add new player into the database
    def add_player(self, name, codename=None):
        query = "INSERT INTO players (id, codename) VALUES (%s, %s)"
        params = (name, codename)
        self.execute_query(query, params)
        
    # Closes the database connection
    def close(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
        except Exception as e:
            print(f"Error closing the database connection: {e}")