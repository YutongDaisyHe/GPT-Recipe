import os
import time
from concurrent.futures import ThreadPoolExecutor
from langgraph.graph import Graph

# Import agent classes
from .agents import SearchAgent, CuratorAgent, WriterAgent, DesignerAgent, EditorAgent, PublisherAgent, CritiqueAgent

class MasterAgent:
    """
    A class used to represent a master agent that coordinates the execution of various agents to generate a recipe book.

    Attributes
    ----------
    output_dir : str
        Directory where the generated files will be saved.

    Methods
    -------
    __init__():
        Initializes the MasterAgent class and creates the output directory.
    
    run(queries: list, layout: str) -> str:
        Executes the workflow for each query and generates a recipe book using the specified layout.
    """

    def __init__(self):
        """
        Initializes the MasterAgent class and creates the output directory.
        """
        self.output_dir = f"outputs/run_{int(time.time())}"
        os.makedirs(self.output_dir, exist_ok=True)

    def run(self, queries: list, layout: str) -> str:
        """
        Executes the workflow for each query and generates a recipe book using the specified layout.

        Parameters
        ----------
        queries : list
            A list of search queries to generate recipes for.
        layout : str
            The layout template file name to be used for the recipe book.

        Returns
        -------
        str
            The path to the generated HTML recipe book file.
        """
        # Initialize agents
        search_agent = SearchAgent()
        curator_agent = CuratorAgent()
        writer_agent = WriterAgent()
        critique_agent = CritiqueAgent()
        designer_agent = DesignerAgent(self.output_dir)
        editor_agent = EditorAgent(layout)
        publisher_agent = PublisherAgent(self.output_dir)

        # Define a Langchain graph
        workflow = Graph()

        # Add nodes for each agent
        workflow.add_node("search", search_agent.run)
        workflow.add_node("curate", curator_agent.run)
        workflow.add_node("write", writer_agent.run)
        workflow.add_node("critique", critique_agent.run)
        workflow.add_node("design", designer_agent.run)

        # Set up edges
        workflow.add_edge('search', 'curate')
        workflow.add_edge('curate', 'write')
        workflow.add_edge('write', 'critique')
        workflow.add_conditional_edges('critique',
                                        lambda x: "accept" if x['critique'] is None else "revise",
                                        {"accept": "design", "revise": "write"})

        # Set up start and end nodes
        workflow.set_entry_point("search")
        workflow.set_finish_point("design")

        # Compile the graph
        chain = workflow.compile()

        # Execute the graph for each query in parallel
        with ThreadPoolExecutor() as executor:
            parallel_results = list(executor.map(lambda q: chain.invoke({"query": q}), queries))

        # Compile the final recipe book
        recipebook_html = editor_agent.run(parallel_results)
        recipebook_path = publisher_agent.run(recipebook_html)

        return recipebook_path
