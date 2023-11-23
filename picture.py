import requests
import pyodbc

# Probeer een verbinding tot stand te brengen
try:
    conn = pyodbc.connect("Driver={ODBC Driver 18 for SQL Server};Server=tcp:jarvis-cloud-verzamelen-joram.database.windows.net,1433;Database=BitAcademyDB;Uid=152791@student.horizoncollege.nl;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;Authentication=ActiveDirectoryInteractive")
    cursor = conn.cursor()

except pyodbc.Error as e:
    print(f"Fout bij het verbinden met de database: {e}")

def create_pokemon_pictures_table():
    table_name = 'pokemon_pictures'

    # Commit changes before dropping the table
    conn.commit()

    # Drop the table if it exists
    drop_table_query = f"IF OBJECT_ID('{table_name}', 'U') IS NOT NULL DROP TABLE {table_name}"
    cursor.execute(drop_table_query)

    # Create the new table
    create_table_query = '''
    CREATE TABLE pokemon_pictures (
        Id INT PRIMARY KEY,
        Name NVARCHAR(255),
        ImageURL NVARCHAR(255)
    )
    '''
    cursor.execute(create_table_query)
    conn.commit()

def insert_pokemon_picture_data(pokemon_id, name, image_url):
    insert_query = '''
    INSERT INTO pokemon_pictures (Id, Name, ImageURL)
    VALUES (?, ?, ?)
    '''

    cursor.execute(insert_query, (pokemon_id, name, image_url))
    conn.commit()

def get_pokemon_image(pokemon_url):
    response = requests.get(pokemon_url)

    if response.status_code == 200:
        data = response.json()
        sprite_url = data["sprites"]["front_default"]
        return sprite_url
    else:
        return None

def get_and_save_pokemon_pictures():
    create_pokemon_pictures_table()

    base_url = "https://pokeapi.co/api/v2/pokemon?limit=1017"
    response = requests.get(base_url)

    if response.status_code == 200:
        data = response.json()
        pokemon_list = data["results"]

        for pokemon in pokemon_list:
            name = pokemon["name"]
            url = pokemon["url"]
            image_url = get_pokemon_image(url)

            if image_url:
                # Insert data into the pokemon_pictures table
                try:
                    insert_pokemon_picture_data(int(url.split('/')[-2]), name, image_url)
                    print(f"Inserted data for {name.capitalize()} with ID {int(url.split('/')[-2])}")
                except Exception as e:
                    print(f"Error inserting data for {name.capitalize()}: {e}")
            else:
                print(f"Failed to get image URL for {name.capitalize()}")
    else:
        print("Failed to get the list of Pokémon.")

if __name__ == "__main__":
    get_and_save_pokemon_pictures()
