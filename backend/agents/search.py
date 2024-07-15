from tavily import TavilyClient
import os
import requests

# Initialize TavilyClient with API key from environment variable
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

class SearchAgent:
    """
    A class used to represent a search agent for querying the Tavily API.

    Methods
    -------
    search_tavily(query: str):
        Searches the Tavily API for the given query and returns sources and an image URL.
    
    run(recipe: dict) -> dict:
        Runs the search_tavily method and updates the recipe dictionary with the search results.
    """

    def __init__(self):
        """
        Initializes the SearchAgent class.
        """
        pass

    def search_tavily(self, query: str):
        """
        Searches the Tavily API for the given query and returns sources and an image URL.

        Parameters
        ----------
        query : str
            The search query string.

        Returns
        -------
        tuple
            A tuple containing the search results (sources) and an image URL.
        """
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

    def run(self, recipe: dict) -> dict:
        """
        Runs the search_tavily method and updates the recipe dictionary with the search results.

        Parameters
        ----------
        recipe : dict
            A dictionary containing the recipe information, including the search query.

        Returns
        -------
        dict
            The updated recipe dictionary with the search results and image URL.
        """
        res = self.search_tavily(recipe["query"])
        recipe["sources"] = res[0]
        recipe["image"] = res[1]
        return recipe
