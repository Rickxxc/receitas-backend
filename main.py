from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import random

app = FastAPI()

# Modelo para os dados recebidos
class RecipeRequest(BaseModel):
    ingredients: List[str]
    mode: str  # 'apenas' ou 'contendo'

# Função simulada para gerar receitas
def generate_recipe(ingredients: List[str], strict: bool) -> Dict:
    all_ingredients = ["ovo", "farinha", "margarina", "açúcar", "leite", "fermento", "chocolate"]
    title = "Receita Deliciosa"
    steps = ["Misture os ingredientes.", "Asse por 30 minutos a 180°C.", "Sirva quente."]
    
    if strict:
        # Apenas receitas com os ingredientes fornecidos
        if not set(ingredients).issubset(all_ingredients):
            raise HTTPException(status_code=400, detail="Alguns ingredientes não estão disponíveis.")
        used_ingredients = ingredients
    else:
        # Receitas que contenham os ingredientes fornecidos
        used_ingredients = random.sample(all_ingredients, k=min(len(all_ingredients), len(ingredients) + 2))
    
    return {
        "title": title,
        "ingredients": used_ingredients,
        "steps": steps
    }

@app.post("/generate-recipe/")
async def generate_recipe_endpoint(request: RecipeRequest):
    try:
        recipe = generate_recipe(request.ingredients, request.mode == "apenas")
        return {"recipe": recipe}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
