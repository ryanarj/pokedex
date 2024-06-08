from fastapi import FastAPI, status, HTTPException
import json

from pydantic import BaseModel

app = FastAPI()


class Pokemon(BaseModel):
    name: str
    type_1: str
    type_2: str
    total: int
    attack: int
    hp: int
    defense: int
    sp_atk: int
    sp_def: int
    speed: int
    generation: int
    legendary: bool


@app.get("/pokemon/{pokemon_id}", status_code=status.HTTP_200_OK)
async def get_pokemon(pokemon_id: int):
    try:
        with open('apis/pokemon.json', 'r') as f:
            data = json.load(f)
            pokemon = data.get(str(pokemon_id))
            if not pokemon:
                raise HTTPException(status_code=404, detail="Pokemon not found")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Pokemon data file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

    return {"data": pokemon}


@app.post("/pokemon", status_code=201)
async def add_pokemon(pokemon: Pokemon):
    try:
        with open('apis/pokemon.json', 'r+') as f:
            data = json.load(f)
            new_id = max(map(int, data.keys()), default=0) + 1
            pokemon_data = pokemon.dict()
            pokemon_data["Id"] = new_id
            data[new_id] = pokemon_data
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to add Pokemon")

    return {"data": data.get(new_id)}
