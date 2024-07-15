from datetime import datetime
from langchain.adapters.openai import convert_openai_messages
from langchain_openai import ChatOpenAI

class CritiqueAgent:
    """
    A class to critique recipes using OpenAI's language model.

    Methods
    -------
    __init__():
        Initializes the CritiqueAgent class.
    
    critique(recipe: dict) -> dict:
        Provides feedback on a given recipe using OpenAI's language model.

    run(recipe: dict) -> dict:
        Runs the critique method and updates the recipe dictionary with the critique.
    """

    def __init__(self):
        """
        Initializes the CritiqueAgent class.
        """
        pass

    def critique(self, recipe: dict) -> dict:
        """
        Provides feedback on a given recipe using OpenAI's language model.

        Parameters
        ----------
        recipe : dict
            A dictionary containing the recipe information.

        Returns
        -------
        dict
            A dictionary with the critique feedback. If no feedback is necessary, 'critique' will be None.
        """
        prompt = [{
            "role": "system",
            "content": "You are a recipe writing critique. Your sole purpose is to provide short feedback on a written "
                       "recipe so the writer will know what to fix.\n "
        }, {
            "role": "user",
            "content": f"{str(recipe)}\n"
                       f"Your task is to provide a really short feedback on the recipe only if necessary.\n"
                       f"If you think the recipe is good, please return None.\n"
                       f"If you noticed the field 'message' in the recipe, it means the writer has revised the recipe"
                       f"based on your previous critique. You can provide feedback on the revised recipe or just "
                       f"return None if you think the recipe is good.\n"
                       f"Please return a string of your critique or None.\n"
        }]

        lc_messages = convert_openai_messages(prompt)
        response = ChatOpenAI(model='gpt-3.5-turbo', max_retries=1).invoke(lc_messages).content
        if response == 'None':
            return {'critique': None}
        else:
            print(f"For recipe: {recipe['title']}")
            print(f"Feedback: {response}\n")
            return {'critique': response, 'message': None}

    def run(self, recipe: dict) -> dict:
        """
        Runs the critique method and updates the recipe dictionary with the critique.

        Parameters
        ----------
        recipe : dict
            A dictionary containing the recipe information.

        Returns
        -------
        dict
            The updated recipe dictionary with the critique feedback.
        """
        recipe.update(self.critique(recipe))
        return recipe
