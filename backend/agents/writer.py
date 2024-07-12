from datetime import datetime
from langchain.adapters.openai import convert_openai_messages
from langchain_openai import ChatOpenAI
import json5 as json

sample_json = """
{
  "title": title of the recipe,
  "date": today's date,
  "paragraphs": [
    "paragraph 1",
    "paragraph 2",
    "paragraph 3",
    "paragraph 4",
    "paragraph 5",
    ],
    "summary": "2 sentences summary of the recipe"
}
"""

sample_revise_json = """
{
    "paragraphs": [
        "paragraph 1",
        "paragraph 2",
        "paragraph 3",
        "paragraph 4",
        "paragraph 5",
    ],
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
            "content": f"Today's date is {datetime.now().strftime('%d/%m/%Y')}\n."
                       f"Query or Topic: {query}"
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

    def revise(self, article: dict):
        prompt = [{
            "role": "system",
            "content": "You are a recipe editor. Your sole purpose is to edit a well-written recipe using a "
                       "list of ingredents based on given critique\n "
        }, {
            "role": "user",
            "content": f"{str(article)}\n"
                        f"Your task is to edit the recipe based on the critique given.\n "
                        f"Please return json format of the 'paragraphs' and a new 'message' field"
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
        print(f"For article: {article['title']}")
        print(f"Writer Revision Message: {response['message']}\n")
        return response

    def run(self, article: dict):
        critique = article.get("critique")
        if critique is not None:
            article.update(self.revise(article))
        else:
            article.update(self.writer(article["query"], article["sources"]))
        return article
