from datetime import datetime
from langchain.adapters.openai import convert_openai_messages
from langchain_openai import ChatOpenAI


class CuratorAgent:
    def __init__(self):
        pass

    def curate_sources(self, query: str, sources: list):
        """
        Curate relevant sources for a query
        :param input:
        :return:
        """
        prompt = [{
            "role": "system",
            "content": "You are a personal recipe creator. Your sole purpose is to choose 2 most relevant recipes "
                       "for me to read from a list of recipes.\n "
        }, {
            "role": "user",
            "content": f"Topic or Query: {query}\n"
                       f"Your task is to return the 2 most relevant recipes for me to cook for the provided keywords or "
                       f"query such as ingredients, cuisine types, etc.\n "
                       f"Here is a list of recipes:\n"
                       f"{sources}\n"
                       f"Please return nothing but a list of the strings of the URLs in this structure: ['url1',"
                       f"'url2','url3', 'url4', 'url5'].\n "
        }]

        lc_messages = convert_openai_messages(prompt)
        response = ChatOpenAI(model='gpt-3.5-turbo', max_retries=1).invoke(lc_messages).content
        chosen_sources = response
        for i in sources:
            if i["url"] not in chosen_sources:
                sources.remove(i)
        return sources

    def run(self, article: dict):
        article["sources"] = self.curate_sources(article["query"], article["sources"])
        return article
