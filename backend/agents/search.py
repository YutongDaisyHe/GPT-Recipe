from tavily import TavilyClient
import os
import requests


tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

class SearchAgent:
    def __init__(self):
        pass

    def search_tavily(self, query: str):
        results = tavily_client.search(query=query, max_results=3, include_images=True)
    
        sources = results["results"]
        try:
            image = results["images"][0]
            # Check if the image URL is accessible
            response = requests.get(image)
            if response.status_code != 200:
                image = "https://www.snapfish.com/blog/wp-content/uploads/2018/09/Screenshot_2.jpg"
    
        except:
            image = "https://www.snapfish.com/blog/wp-content/uploads/2018/09/Screenshot_2.jpg"
        return sources, image

    def run(self, recipe: dict):
        res = self.search_tavily(recipe["query"])
        recipe["sources"] = res[0]
        recipe["image"] = res[1]
        return recipe
