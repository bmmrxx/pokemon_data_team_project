import requests
import pyodbc

# Probeer een verbinding tot stand te brengen
try:
    conn = pyodbc.connect("Driver={ODBC Driver 18 for SQL Server};Server=tcp:jarvis-cloud-verzamelen-joram.database.windows.net,1433;Database=BitAcademyDB;Uid=152791@student.horizoncollege.nl;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;Authentication=ActiveDirectoryInteractive")
    cursor = conn.cursor()

except pyodbc.Error as e:
    print(f"Fout bij het verbinden met de database: {e}")

def create_evolution_table():
    table_name = '[evolution_data]'

    # Commit changes before dropping the table
    conn.commit()

    # Drop the table if it exists
    drop_table_query = f"IF OBJECT_ID('{table_name}', 'U') IS NOT NULL DROP TABLE {table_name}"
    cursor.execute(drop_table_query)

    # Create the new table
    create_table_query = f'''
CREATE TABLE {table_name} (
    EvolutionId INT PRIMARY KEY IDENTITY(1,1),
    PokemonName NVARCHAR(255),
    Evolution1 NVARCHAR(255),
    Evolution2 NVARCHAR(255),
    Evolution3 NVARCHAR(255)
    )
'''

    cursor.execute(create_table_query)
    conn.commit()

def insert_evolution_data(pokemon_name, evolutions):
    # Ensure that the length of evolutions does not exceed 3
    evolutions = evolutions[:3]

    insert_query = '''
    INSERT INTO [evolution_data] (PokemonName, Evolution1, Evolution2, Evolution3)
    VALUES (?, ?, ?, ?)
    '''

    # Pad the evolutions list with None if needed
    evolutions += [None] * (3 - len(evolutions))

    cursor.execute(insert_query, (pokemon_name, *evolutions))
    conn.commit()

def get_and_save_all_pokemon_evolutions():
    create_evolution_table()

    url = 'https://pokeapi.co/api/v2/pokemon?limit=1017'
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Fout bij het ophalen van Pokémon-lijst. Statuscode: {response.status_code}")
        return
    
    pokemon_list = response.json()['results']
    
    for pokemon in pokemon_list:
        pokemon_name = pokemon['name']
        evolution_chain = get_pokemon_evolution_chain(pokemon_name)

        if evolution_chain:
            print(f"\n{'='*30}\nPokémon: {pokemon_name.capitalize()}")
            evolutions = display_and_get_evolution_chain(evolution_chain)
            insert_evolution_data(pokemon_name, evolutions)

def get_pokemon_evolution_chain(pokemon_name):
    url = f'https://pokeapi.co/api/v2/pokemon-species/{pokemon_name.lower()}/'
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Fout bij het ophalen van Pokémon-informatie. Statuscode: {response.status_code}")
        return None
    
    pokemon_data = response.json()
    
    evolution_chain_url = pokemon_data['evolution_chain']['url']
    evolution_chain_response = requests.get(evolution_chain_url)
    
    if evolution_chain_response.status_code != 200:
        print(f"Fout bij het ophalen van evolutieketen. Statuscode: {evolution_chain_response.status_code}")
        return None
    
    evolution_chain_data = evolution_chain_response.json()
    return evolution_chain_data['chain']


def display_and_get_evolution_chain(chain, level=0, max_evolutions=3):
    evolutions = []

    if level < max_evolutions:
        evolutions.append(chain['species']['name'])

    if chain['evolves_to']:
        for child in chain['evolves_to']:
            evolutions.extend(display_and_get_evolution_chain(child, level + 1, max_evolutions))

    return evolutions

if __name__ == "__main__":
    get_and_save_all_pokemon_evolutions()