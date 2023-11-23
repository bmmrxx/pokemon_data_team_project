import requests
import pyodbc

# Connecting to database
try:
    conn = pyodbc.connect("Driver={ODBC Driver 18 for SQL Server};Server=tcp:jarvis-cloud-verzamelen-joram.database.windows.net,1433;Database=BitAcademyDB;Uid=152791@student.horizoncollege.nl;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;Authentication=ActiveDirectoryInteractive")
    cursor = conn.cursor()

except pyodbc.Error as e:
    print(f"Fout bij het verbinden met de database: {e}")

def get_pokemon_data(pokemon_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}/"
    response = requests.get(url)
    
    if response.status_code == 200:
        pokemon_data = response.json()
        return pokemon_data
    else:
        print(f"Failed to fetch data for Pokemon with ID {pokemon_id}")
        return None

# Function that creates our database table
def create_pokemon_table():
    table_name = '[base ability data]'

    # Commit changes before dropping the table
    conn.commit()

    # Drop the table if it exists
    drop_table_query = f"IF OBJECT_ID('{table_name}', 'U') IS NOT NULL DROP TABLE {table_name}"
    cursor.execute(drop_table_query)

    # Create the new table
    create_table_query = f'''
    CREATE TABLE {table_name} (
        Id INT PRIMARY KEY,
        Name NVARCHAR(255),
        Type NVARCHAR(255),
        Ability NVARCHAR(255),
        Hp INT,
        Attack INT,
        Defense INT,
        SpecialAttack INT,
        SpecialDefense INT,
        Speed INT,
        DoubleDamageTo NVARCHAR(255),
        HalfDamageTo NVARCHAR(255),
        NoDamageTo NVARCHAR(255),
        DoubleDamageFrom NVARCHAR(255),
        HalfDamageFrom NVARCHAR(255),
        NoDamageFrom NVARCHAR(255)
    )
    '''
    cursor.execute(create_table_query)
    conn.commit()


# Function to import pokemon data to database
def insert_pokemon_data(pokemon_data):
    insert_query = '''
    INSERT INTO [base ability data] (Id, Name, Type, Ability, Hp, Attack, Defense, SpecialAttack, SpecialDefense, Speed,
        DoubleDamageTo, HalfDamageTo, NoDamageTo, DoubleDamageFrom, HalfDamageFrom, NoDamageFrom)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''

    # Check if the record with the same Id already exists
    check_query = f"SELECT Id FROM [base ability data] WHERE Id = {pokemon_data['id']}"
    existing_record = cursor.execute(check_query).fetchone()

    if existing_record:
        print(f"Record with Id {pokemon_data['id']} already exists. Skipping insertion.")
    else:
        for damage_relation in pokemon_data['types']:
            type_name = damage_relation['type']['name']
            type_url = damage_relation['type']['url']
            type_info = requests.get(type_url).json()

            double_damage_to = [type['name'] for type in type_info['damage_relations']['double_damage_to']]
            half_damage_to = [type['name'] for type in type_info['damage_relations']['half_damage_to']]
            no_damage_to = [type['name'] for type in type_info['damage_relations']['no_damage_to']]

            double_damage_from = [type['name'] for type in type_info['damage_relations']['double_damage_from']]
            half_damage_from = [type['name'] for type in type_info['damage_relations']['half_damage_from']]
            no_damage_from = [type['name'] for type in type_info['damage_relations']['no_damage_from']]

            cursor.execute(insert_query, (
                pokemon_data['id'],
                pokemon_data['name'],
                ', '.join([type_info['type']['name'] for type_info in pokemon_data['types']]),
                ', '.join([ability['ability']['name'] for ability in pokemon_data['abilities']]),
                pokemon_data['stats'][0]['base_stat'],  # Hp
                pokemon_data['stats'][1]['base_stat'],  # Attack
                pokemon_data['stats'][2]['base_stat'],  # Defense
                pokemon_data['stats'][3]['base_stat'],  # SpecialAttack
                pokemon_data['stats'][4]['base_stat'],  # SpecialDefense
                pokemon_data['stats'][5]['base_stat'],  # Speed
                ', '.join(double_damage_to),
                ', '.join(half_damage_to),
                ', '.join(no_damage_to),
                ', '.join(double_damage_from),
                ', '.join(half_damage_from),
                ', '.join(no_damage_from)
            ))
            conn.commit()
# Loop trough all pokemon in the pokemon data
def get_and_save_all_pokemons(num_pokemons):
    create_pokemon_table()

    for pokemon_id in range(num_pokemons + 1):
        print(f"Processing Pokemon ID: {pokemon_id}")
        pokemon_data = get_pokemon_data(pokemon_id)
        if pokemon_data:
            try:
                insert_pokemon_data(pokemon_data)
            except Exception as e:
                print(f"Error inserting data for Pokemon with ID {pokemon_id}: {e}")

# We gather 
if __name__ == "__main__":
    num_pokemons = 1017
    get_and_save_all_pokemons( num_pokemons)