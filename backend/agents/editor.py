import os

recipe_templates = {
    "layout_1.html": """
    <div class="recipe">
        <a href="{{path}}" target="_blank"><h2>{{title}}</h2></a>
        <img src="{{image}}" alt="Recipe Image">
        <p>{{summary}}</p>
    </div>
    """
}

class EditorAgent:
    """
    A class used to represent an editor agent for generating an HTML recipe book from multiple recipes.

    Attributes
    ----------
    layout : str
        The layout template file name to be used for the recipe book.

    Methods
    -------
    __init__(layout: str):
        Initializes the EditorAgent class with the specified layout template.
    
    load_html_template() -> str:
        Loads the HTML layout template from a predefined location.
    
    editor(recipes: list) -> str:
        Generates an HTML recipe book from a list of recipes using the specified layout.
    
    run(recipes: list) -> str:
        Runs the editor method to generate the HTML recipe book.
    """

    def __init__(self, layout):
        """
        Initializes the EditorAgent class with the specified layout template.

        Parameters
        ----------
        layout : str
            The layout template file name to be used for the recipe book.
        """
        self.layout = layout

    def load_html_template(self) -> str:
        """
        Loads the HTML layout template from a predefined location.

        Returns
        -------
        str
            The content of the HTML layout template file.
        """
        template_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'recipebook', 'layouts', self.layout)
        with open(template_path) as f:
            return f.read()

    def editor(self, recipes: list) -> str:
        """
        Generates an HTML recipe book from a list of recipes using the specified layout.

        Parameters
        ----------
        recipes : list
            A list of dictionaries, each containing the recipe information.

        Returns
        -------
        str
            The generated HTML content for the recipe book.
        """
        html_template = self.load_html_template()

        # Recipe template
        recipe_template = recipe_templates[self.layout]

        # Generate recipes HTML
        recipes_html = ""
        for recipe in recipes:
            recipe_html = recipe_template.replace("{{title}}", recipe["title"])
            recipe_html = recipe_html.replace("{{image}}", recipe["image"])
            recipe_html = recipe_html.replace("{{summary}}", recipe["summary"])
            recipe_html = recipe_html.replace("{{path}}", recipe["path"])
            recipes_html += recipe_html

        # Replace placeholders in template
        recipebook_html = html_template.replace("{{recipes}}", recipes_html)
        return recipebook_html

    def run(self, recipes: list) -> str:
        """
        Runs the editor method to generate the HTML recipe book.

        Parameters
        ----------
        recipes : list
            A list of dictionaries, each containing the recipe information.

        Returns
        -------
        str
            The generated HTML content for the recipe book.
        """
        res = self.editor(recipes)
        return res
