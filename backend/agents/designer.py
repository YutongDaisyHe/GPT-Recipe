import os
import re

class DesignerAgent:
    """
    A class used to represent a designer agent for generating HTML from recipe data.

    Attributes
    ----------
    output_dir : str
        Directory where the generated HTML files will be saved.

    Methods
    -------
    __init__(output_dir: str):
        Initializes the DesignerAgent class with the specified output directory.
    
    load_html_template() -> str:
        Loads the HTML template from a predefined location.
    
    designer(recipe: dict) -> dict:
        Populates the HTML template with recipe data and updates the recipe dictionary.
    
    save_recipe_html(recipe: dict) -> dict:
        Saves the populated HTML template to a file and updates the recipe dictionary with the file path.
    
    run(recipe: dict) -> dict:
        Runs the designer method to generate and save the HTML file for the given recipe.
    """

    def __init__(self, output_dir):
        """
        Initializes the DesignerAgent class with the specified output directory.

        Parameters
        ----------
        output_dir : str
            Directory where the generated HTML files will be saved.
        """
        self.output_dir = output_dir

    def load_html_template(self) -> str:
        """
        Loads the HTML template from a predefined location.

        Returns
        -------
        str
            The content of the HTML template file.
        """
        relative_path = "../templates/recipe/index.html"
        dir_path = os.path.dirname(os.path.realpath(__file__))
        html_file_path = os.path.join(dir_path, relative_path)
        with open(html_file_path) as f:
            html_template = f.read()
        return html_template

    def designer(self, recipe: dict) -> dict:
        """
        Populates the HTML template with recipe data and updates the recipe dictionary.

        Parameters
        ----------
        recipe : dict
            A dictionary containing the recipe information.

        Returns
        -------
        dict
            The updated recipe dictionary with the generated HTML.
        """
        html_template = self.load_html_template()
        title = recipe["title"]
        image = recipe["image"]
        totaltime = recipe["totaltime"]
        servings = recipe["servings"]
        ingredients = recipe["ingredients"]
        instructions = recipe["instructions"]
        
        # Replace basic placeholders
        html_template = html_template.replace("{{title}}", title)
        html_template = html_template.replace("{{image}}", image)
        html_template = html_template.replace("{{totaltime}}", totaltime)
        html_template = html_template.replace("{{servings}}", str(servings))

        # Create the ingredients list HTML
        ingredients_html = ""
        for ingredient in ingredients:
            if isinstance(ingredient, dict):
                ingredient = f"{ingredient['ingredient']} - {ingredient['amount']}"
            ingredients_html += f"<li>{ingredient}</li>"
    
        # Replace the ingredients placeholder
        html_template = html_template.replace("{{ingredients}}", ingredients_html)

        # Create the instructions list HTML
        instructions_html = ""
        for instruction in instructions:
            instructions_html += f"<li>{instruction.lstrip('0123456789.- ')}</li>"
    
        # Replace the instructions placeholder
        html_template = html_template.replace("{{instructions}}", instructions_html)
       
        recipe["html"] = html_template
        recipe = self.save_recipe_html(recipe)
        return recipe

    def save_recipe_html(self, recipe: dict) -> dict:
        """
        Saves the populated HTML template to a file and updates the recipe dictionary with the file path.

        Parameters
        ----------
        recipe : dict
            A dictionary containing the recipe information.

        Returns
        -------
        dict
            The updated recipe dictionary with the path to the saved HTML file.
        """
        filename = re.sub(r'[\/:*?"<>| ]', '_', recipe['query'])
        filename = f"{filename}.html"
        path = os.path.join(self.output_dir, filename)
        with open(path, 'w') as file:
            file.write(recipe['html'])
        recipe["path"] = filename
        return recipe

    def run(self, recipe: dict) -> dict:
        """
        Runs the designer method to generate and save the HTML file for the given recipe.

        Parameters
        ----------
        recipe : dict
            A dictionary containing the recipe information.

        Returns
        -------
        dict
            The updated recipe dictionary with the generated HTML and file path.
        """
        recipe = self.designer(recipe)
        return recipe
