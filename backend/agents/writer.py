from datetime import datetime
from langchain.adapters.openai import convert_openai_messages
from langchain_openai import ChatOpenAI
import json5 as json

sample_json = """
{
  "title": title of the recipe,
  "totaltime": total cooking time,
  "servings": amount of servings,
  "ingredients": list of ingredients and amount,
  "instructions": list of cooking steps,
  "summary": "2 sentences summary of the recipe"
}
"""

sample_revise_json = """
{
    "totaltime": total cooking time,
    "servings": amount of servings,
    "ingredients": list of ingredients and amount,
    "instructions": list of cooking steps,
    "message": "message to the critique"
}
"""


class WriterAgent:
    def __init__(self):
        pass

    def writer(self, query: str, sources: list):

        prompt = [{
            "role": "system",
            "content": "You are a recipe writer. Your sole purpose is to write a well-written recipe "
                       "according to a list of recipes using a list of ingredients.\n "
        }, {
            "role": "user",
            "content": f"Query or Topic: {query}"
                       f"{sources}\n"
                       f"Your task is to write a critically acclaimed recipe for me about the provided query or "
                       f"ingredients based on the sources.\n "
                       f"Please return nothing but a JSON in the following format:\n"
                       f"{sample_json}\n "

        }]

        lc_messages = convert_openai_messages(prompt)
        optional_params = {
            "response_format": {"type": "json_object"}
        }

        # response = ChatOpenAI(model='gpt-4-0125-preview', max_retries=1, model_kwargs=optional_params).invoke(lc_messages).content
        response = ChatOpenAI(model='gpt-3.5-turbo', max_retries=1, model_kwargs=optional_params).invoke(lc_messages).content
        return json.loads(response)

    def revise(self, recipe: dict):
        prompt = [{
            "role": "system",
            "content": "You are a recipe editor. Your sole purpose is to edit a well-written recipe using a "
                       "list of ingredents based on given critique\n "
        }, {
            "role": "user",
            "content": f"{str(recipe)}\n"
                        f"Your task is to edit the recipe based on the critique given.\n "
                        f"Please return json format of the 'totaltime', 'servings', 'ingredients',\n" 
                        f"'instructions' and a new 'message' field\n"
                        f"to the critique that explain your changes or why you didn't change anything.\n"
                        f"please return nothing but a JSON in the following format:\n"
                        f"{sample_revise_json}\n "

        }]

        lc_messages = convert_openai_messages(prompt)
        optional_params = {
            "response_format": {"type": "json_object"}
        }

        # response = ChatOpenAI(model='gpt-4-0125-preview', max_retries=1, model_kwargs=optional_params).invoke(lc_messages).content
        response = ChatOpenAI(model='gpt-3.5-turbo', max_retries=1, model_kwargs=optional_params).invoke(lc_messages).content

        response = json.loads(response)
        print(f"For recipe: {recipe['title']}")
        print(f"Writer Revision Message: {response['message']}\n")
        return response

    def run(self, recipe: dict):
        critique = recipe.get("critique")
        if critique is not None:
            recipe.update(self.revise(recipe))
        else:
            recipe.update(self.writer(recipe["query"], recipe["sources"]))
        return recipe
