from datetime import datetime
from langchain.adapters.openai import convert_openai_messages
from langchain_openai import ChatOpenAI

class CuratorAgent:
    """
    A class used to represent a curator agent for selecting the most relevant sources.

    Methods
    -------
    __init__():
        Initializes the CuratorAgent class.
    
    curate_sources(query: str, sources: list) -> list:
        Curates the most relevant sources based on the given query.
    
    run(recipe: dict) -> dict:
        Runs the curate_sources method and updates the recipe dictionary with the curated sources.
    """

    def __init__(self):
        """
        Initializes the CuratorAgent class.
        """
        pass

    def curate_sources(self, query: str, sources: list) -> list:
        """
        Curates the most relevant sources based on the given query.

        Parameters
        ----------
        query : str
            The search query string.
        sources : list
            A list of source dictionaries, each containing a 'url' key.

        Returns
        -------
        list
            A list of curated source dictionaries.
        """
        prompt = [{
            "role": "system",
            "content": "You are a personal recipe creator. Your sole purpose is to choose the 2 most relevant recipes "
                       "for me to read from a list of recipes.\n"
        }, {
            "role": "user",
            "content": f"Topic or Query: {query}\n"
                       f"Your task is to return the 2 most relevant recipes for me to cook for the provided keywords or "
                       f"query such as ingredients, cuisine types, etc.\n"
                       f"Here is a list of recipes:\n"
                       f"{sources}\n"
                       f"Please return nothing but a list of the strings of the URLs in this structure: ['url1', "
                       f"'url2', 'url3', 'url4', 'url5'].\n"
        }]

        lc_messages = convert_openai_messages(prompt)
        response = ChatOpenAI(model='gpt-3.5-turbo', max_retries=1).invoke(lc_messages).content
        chosen_sources = eval(response)  # Assuming response is a string representation of a list
        sources = [source for source in sources if source["url"] in chosen_sources]
        return sources

    def run(self, recipe: dict) -> dict:
        """
        Runs the curate_sources method and updates the recipe dictionary with the curated sources.

        Parameters
        ----------
        recipe : dict
            A dictionary containing the recipe information, including the query and sources.

        Returns
        -------
        dict
            The updated recipe dictionary with the curated sources.
        """
        recipe["sources"] = self.curate_sources(recipe["query"], recipe["sources"])
        return recipe
