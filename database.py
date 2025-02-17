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
    def add_player(self, playerId, codename=None):
        if codename:
            query = "INSERT INTO players (id, codename) VALUES (%s, %s)"
            params = (playerId, codename)
            self.execute_query(query, params)
        else:
            print("No codename provided, unable to add.")
            

    # Update a player's codename in the database
    def update_codename(self, playerId, codename=None):
        # Check if the playerId exists in the db
        query = "SELECT ID FROM players WHERE ID = %s"
        params = (playerId,)
        result = self.execute_query(query, params)
        
        if result and len(result) > 0:
            if codename:
                query = "UPDATE players SET codename = %s WHERE ID = %s"
                params = (codename, playerId)
                self.execute_query(query, params)
                print(f"Codename for player {playerId} updated to {codename}.")
            else:
                print("No codename provided, unable to update.")
        else:
            print(f"Player with ID {playerId} does not exist in the database.")


    # Check if codename exists, if it does, return it.
    def get_codename(self, equipmentId):
        query = "SELECT codename FROM PLAYERS WHERE ID = %s"
        params = (equipmentId,)  # Ensure it's passed as a tuple
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
