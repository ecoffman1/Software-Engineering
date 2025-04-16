import psycopg2
import json

class Database():
    def __init__(self, config = None, config_path = None):
        self.config_path = config_path
        self.conn = None
        self.cursor = None

        if config:
            self.connect_params = config  
        elif config_path:
            # Retrieve database connection params from config file.
            self.connect_params = self.load_config()
        else:
            self.connect_params = {}

        self.db_params = {
            'dbname': self.connect_params.get('dbname'),
            'user': self.connect_params.get('user')
        }

    # Load configuration from a JSON file
    def load_config(self):
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: the file {self.config_path} was not found")
            return {}
        except json.JSONDecodeError:
            print(f"Error: the file {self.config_path} contains invalid JSON")
            return {}

    # Establish connection to database
    def connect(self):
        try:
            if self.db_params:
                self.conn = psycopg2.connect(**self.db_params)
                self.cursor = self.conn.cursor()
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
    def add_player(self, playerID, codename=None):
        if codename:
            query = "INSERT INTO players (id, codename) VALUES (%s, %s)"
            params = (playerID, codename)
            self.execute_query(query, params)
        else:
            print("No codename provided, unable to add.")


    # Update a player's codename in the database
    def update_codename(self, playerID, codename=None):
        # Check if the playerID exists in the db
        query = "SELECT ID FROM players WHERE ID = %s"
        params = (playerID,)
        result = self.execute_query(query, params)
        
        if result and len(result) > 0:
            if codename:
                query = "UPDATE players SET codename = %s WHERE ID = %s"
                params = (codename, playerID)
                self.execute_query(query, params)
                print(f"Codename for player {playerID} updated to {codename}.")
                return True
            else:
                print("No codename provided, unable to update.")
                return False
        else:
            print(f"Player with ID {playerID} does not exist in the database.")
            return False


    # Check if codename exists, if it does, return it.
    def get_codename(self, playerID):
        query = "SELECT codename FROM PLAYERS WHERE ID = %s"
        params = (playerID,)  # Ensure it's passed as a tuple
        result = self.execute_query(query, params)
        
        # If result is not None, we have to check if there are results to return
        if result and len(result) > 0:
            return result[0][0]  # Extract the codename from the tuple of results
        else:
            return None
        
    # Closes the database connection
    def close(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
        except Exception as e:
            print(f"Error closing the database connection: {e}")
