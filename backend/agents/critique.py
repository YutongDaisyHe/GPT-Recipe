from datetime import datetime
from langchain.adapters.openai import convert_openai_messages
from langchain_openai import ChatOpenAI

class CritiqueAgent:
    def __init__(self):
        pass

    def critique(self, recipe: dict):
        prompt = [{
            "role": "system",
            "content": "You are a recipe writing critique. Your sole purpose is to provide short feedback on a written "
                       "recipe so the writer will know what to fix.\n "
        }, {
            "role": "user",
            "content": f"{str(recipe)}\n"
                       f"Your task is to provide a really short feedback on the recipe only if necessary.\n"
                       f"if you think the recipe is good, please return None.\n"
                       f"if you noticed the field 'message' in the recipe, it means the writer has revised the recipe"
                       f"based on your previous critique. you can provide feedback on the revised recipe or just "
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

    def run(self, recipe: dict):
        recipe.update(self.critique(recipe))
        return recipe
