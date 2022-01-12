import aiohttp
import asyncio
from lib import Pokemon

pokedex = []



class Pokemon:
    def __init__(self, id, name, weight, type, attack_move):
        self.id = id
        self.name = name
        self.weight = weight
        self.type = type
        self.attack_move = attack_move

    def __str__(self):
        return f"ID: {self.id} - NAME: {self.name} - WEIGHT: {self.weight} - TYPE: {self.type} - ATTACK-MOVE: {self.attack_move}"

    def attack(self):
        print(f"{self.name} - attacks using {self.attack_move}")
        

async def get_pokemon(session, url):
    try:
        async with session.get(url) as resp:
            print(f"ASYNC Request: {url}")
            pokemon = await resp.json()
            return pokemon
    except aiohttp.ClientConnectionError:
        return {}


async def build_pokedex():
    async with aiohttp.ClientSession() as session:

        tasks = []
        for number in range(1, 151):
            url = f'https://pokeapi.co/api/v2/pokemon/{number}'
            tasks.append(asyncio.ensure_future(get_pokemon(session, url)))

        original_pokemon = await asyncio.gather(*tasks)
        for pokemon_data in filter(None, original_pokemon):
            pokemon = Pokemon(id=pokemon_data["id"], name=pokemon_data["name"], weight=pokemon_data["weight"], type=pokemon_data["types"][0]["type"]["name"], attack_move=pokemon_data["moves"][0]["move"]["name"])
            pokedex.append(pokemon)

if __name__ == "__main__":
    asyncio.run(build_pokedex())
    for pokemon in pokedex:
        print(pokemon)


