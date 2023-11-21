import requests

def get_pokemon_data(pokemon_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}/"
    response = requests.get(url)
    
    if response.status_code == 200:
        pokemon_data = response.json()
        return pokemon_data
    else:
        print(f"Failed to fetch data for Pokemon with ID {pokemon_id}")
        return None

def print_pokemon_info(pokemon_data):
    if pokemon_data:
        print(f"Name: {pokemon_data['name'].capitalize()}")
        print(f"ID: {pokemon_data['id']}")
        print("Types:", ', '.join([type_info['type']['name'] for type_info in pokemon_data['types']]))
        print("Abilities:", ', '.join([ability['ability']['name'] for ability in pokemon_data['abilities']]))
        print("Stats:")
        for stat in pokemon_data['stats']:
            print(f"  {stat['stat']['name'].capitalize()}: {stat['base_stat']}")
        print("\n")

def main():
    num_pokemons = 100  # You can change this number based on how many Pokémon you want to retrieve

    for pokemon_id in range(1, num_pokemons + 1):
        pokemon_data = get_pokemon_data(pokemon_id)
        print_pokemon_info(pokemon_data)

if __name__ == "__main__":
    main()
