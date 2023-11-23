import requests
import pyodbc

# Connecting to the database
try:
    conn = pyodbc.connect("Driver={ODBC Driver 18 for SQL Server};Server=tcp:jarvis-cloud-verzamelen-joram.database.windows.net,1433;Database=BitAcademyDB;Uid=152791@student.horizoncollege.nl;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;Authentication=ActiveDirectoryInteractive")
    cursor = conn.cursor()

except pyodbc.Error as e:
    print(f"Fout bij het verbinden met de database: {e}")

# Function that creates the move data table
def create_moves_table():
    table_name = '[move data]'

    # Commit changes before dropping the table
    conn.commit()

    # Drop the table if it exists
    drop_table_query = f"IF OBJECT_ID('{table_name}', 'U') IS NOT NULL DROP TABLE {table_name}"
    cursor.execute(drop_table_query)

    # Create the new table
    create_table_query = f'''
    CREATE TABLE {table_name} (
        MoveId INT PRIMARY KEY,
        Name NVARCHAR(255),
        Type NVARCHAR(255),
        Power INT,
        PP INT,
        Accuracy INT,
        Priority INT,
        DamageClass NVARCHAR(255),
        Effect NVARCHAR(MAX)
    )
    '''
    cursor.execute(create_table_query)
    conn.commit()

# Function to insert move data into the database
def insert_move_data(move_data):
    insert_query = '''
    INSERT INTO [move data] (MoveId, Name, Type, Power, PP, Accuracy, Priority, DamageClass, Effect)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''

    # Check if the record with the same MoveId already exists
    check_query = f"SELECT MoveId FROM [move data] WHERE MoveId = {move_data['id']}"
    existing_record = cursor.execute(check_query).fetchone()

    if existing_record:
        print(f"Record with MoveId {move_data['id']} already exists. Skipping insertion.")
    else:
        cursor.execute(insert_query, (
            move_data['id'],
            move_data['name'],
            move_data['type']['name'],
            move_data['power'],
            move_data['pp'],
            move_data['accuracy'],
            move_data['priority'],
            move_data['damage_class']['name'],
            move_data['effect_entries'][0]['effect'] if move_data['effect_entries'] else None
        ))
        conn.commit()

# Function to get move data from the PokeAPI
def get_move_data(move_id):
    url = f"https://pokeapi.co/api/v2/move/{move_id}/"
    response = requests.get(url)

    if response.status_code == 200:
        move_data = response.json()
        return move_data
    else:
        print(f"Failed to fetch data for Move with ID {move_id}")
        return None

# Function to loop through all moves and save them to the database
def get_and_save_all_moves(num_moves):
    create_moves_table()

    for move_id in range(1, num_moves + 1):
        print(f"Processing Move ID: {move_id}")
        move_data = get_move_data(move_id)
        if move_data:
            try:
                insert_move_data(move_data)
            except Exception as e:
                print(f"Error inserting data for Move with ID {move_id}: {e}")

if __name__ == "__main__":
    num_moves = 922 
    get_and_save_all_moves(num_moves)
