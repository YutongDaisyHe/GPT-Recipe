from .search import SearchAgent
from .curator import CuratorAgent
from .writer import WriterAgent
from .critique import CritiqueAgent
from .designer import DesignerAgent
from .editor import EditorAgent
from .publisher import PublisherAgent

__all__ = ["SearchAgent", "CuratorAgent", "WriterAgent", "CritiqueAgent", "DesignerAgent", "EditorAgent", "PublisherAgent"]

"""
This module imports various agent classes and makes them available for use.

Classes
-------
SearchAgent
    Seaches the web for the most relevant recipes using Tavily API.
CuratorAgent
    Filters and selects recipes based on users' input keywords.
WriterAgent
    Crafts formatted recipe article.
CritiqueAgent
    Provides feedback on a given recipe using OpenAI's language model.
DesignerAgent
    Responsible for designing and organizing recipe layout.
EditorAgent
    Constructs the recipe book based on produced recipes.
PublisherAgent
    Publishes the recipe book.
"""
