import requests

def get_all_pokemon():
    base_url = "https://pokeapi.co/api/v2/pokemon?limit=1000"  # 'limit' kan worden aangepast afhankelijk van het aantal Pokémon
    response = requests.get(base_url)

    if response.status_code == 200:
        data = response.json()
        return data["results"]
    else:
        return None

def get_pokemon_image(pokemon_url):
    response = requests.get(pokemon_url)

    if response.status_code == 200:
        data = response.json()
        sprite_url = data["sprites"]["front_default"]
        return sprite_url
    else:
        return None

# Ophalen van alle Pokémon
all_pokemon = get_all_pokemon()

if all_pokemon:
    for pokemon in all_pokemon:
        name = pokemon["name"]
        url = pokemon["url"]
        image_url = get_pokemon_image(url)
        
        if image_url:
            print(f"Image URL for {name.capitalize()}: {image_url}")
        else:
            print(f"Failed to get image URL for {name.capitalize()}")
else:
    print("Failed to get the list of Pokémon.")
