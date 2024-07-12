from tavily import TavilyClient
import os
import logging
logging.basicConfig(level=logging.DEBUG)

# tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
tavily_client = TavilyClient(api_key="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")

class SearchAgent:
    def __init__(self):
        pass

    def search_tavily(self, query: str):
        print("test1")
        print(query)
        # No topic="recipes"
        results = tavily_client.search(query=query, max_results=3, include_images=True)
        
        # results = tavily_client.search(query=query, topic="recipes", max_results=3, include_images=True)
        # results = tavily_client.search(query='test')
        logging.debug(f"Received results: {results}")

        print("test2")
        sources = results["results"]
        try:
            image = results["images"][0]
        except:
            image = "https://www.snapfish.com/blog/wp-content/uploads/2018/09/Screenshot_2.jpg"
        return sources, image

    def run(self, recipe: dict):
        res = self.search_tavily(recipe["query"])
        recipe["sources"] = res[0]
        recipe["image"] = res[1]
        return recipe
