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
    """
    A class used to represent a writer agent for generating and revising recipes.

    Methods
    -------
    __init__():
        Initializes the WriterAgent class.
    
    writer(query: str, sources: list) -> dict:
        Generates a well-written recipe based on the given query and sources.
    
    revise(recipe: dict) -> dict:
        Revises the recipe based on given critique and returns the updated recipe.
    
    run(recipe: dict) -> dict:
        Runs the writer or revise method based on whether a critique is present in the recipe dictionary.
    """

    def __init__(self):
        """
        Initializes the WriterAgent class.
        """
        pass

    def writer(self, query: str, sources: list) -> dict:
        """
        Generates a well-written recipe based on the given query and sources.

        Parameters
        ----------
        query : str
            The search query string.
        sources : list
            A list of source dictionaries.

        Returns
        -------
        dict
            A dictionary containing the generated recipe in JSON format.
        """
        prompt = [{
            "role": "system",
            "content": "You are a recipe writer. Your sole purpose is to write a well-written recipe "
                       "according to a list of recipes using a list of keywords such as ingredients, cuisine types, etc.\n"
        }, {
            "role": "user",
            "content": f"Query or Topic: {query}\n"
                       f"{sources}\n"
                       f"Your task is to write a critically acclaimed recipe for me about the provided query or "
                       f"keywords such as ingredients, cuisine types, etc. based on the sources.\n"
                       f"Please return nothing but a JSON in the following format:\n"
                       f"{sample_json}\n"
        }]

        lc_messages = convert_openai_messages(prompt)
        optional_params = {
            "response_format": {"type": "json_object"}
        }

        response = ChatOpenAI(model='gpt-3.5-turbo', max_retries=1, model_kwargs=optional_params).invoke(lc_messages).content
        return json.loads(response)

    def revise(self, recipe: dict) -> dict:
        """
        Revises the recipe based on given critique and returns the updated recipe.

        Parameters
        ----------
        recipe : dict
            A dictionary containing the recipe information and critique.

        Returns
        -------
        dict
            A dictionary containing the revised recipe in JSON format.
        """
        prompt = [{
            "role": "system",
            "content": "You are a recipe editor. Your sole purpose is to edit a well-written recipe using a "
                       "list of keywords for ingredients, cuisine types, etc. based on given critique.\n"
        }, {
            "role": "user",
            "content": f"{str(recipe)}\n"
                       f"Your task is to edit the recipe based on the critique given.\n"
                       f"Please return JSON format of the 'totaltime', 'servings', 'ingredients',\n"
                       f"'instructions' and a new 'message' field\n"
                       f"to the critique that explains your changes or why you didn't change anything.\n"
                       f"Please return nothing but a JSON in the following format:\n"
                       f"{sample_revise_json}\n"
        }]

        lc_messages = convert_openai_messages(prompt)
        optional_params = {
            "response_format": {"type": "json_object"}
        }

        response = ChatOpenAI(model='gpt-3.5-turbo', max_retries=1, model_kwargs=optional_params).invoke(lc_messages).content

        response = json.loads(response)
        print(f"For recipe: {recipe['title']}")
        print(f"Writer Revision Message: {response['message']}\n")
        return response

    def run(self, recipe: dict) -> dict:
        """
        Runs the writer or revise method based on whether a critique is present in the recipe dictionary.

        Parameters
        ----------
        recipe : dict
            A dictionary containing the recipe information, including the query, sources, and optionally, a critique.

        Returns
        -------
        dict
            The updated recipe dictionary with generated or revised recipe information.
        """
        critique = recipe.get("critique")
        if critique is not None:
            recipe.update(self.revise(recipe))
        else:
            recipe.update(self.writer(recipe["query"], recipe["sources"]))
        return recipe
