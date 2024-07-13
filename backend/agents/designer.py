import os
import re
import logging

class DesignerAgent:
    def __init__(self, output_dir):
        self.output_dir = output_dir


    def load_html_template(self):
        relative_path = "../templates/recipe/index.html"
        dir_path = os.path.dirname(os.path.realpath(__file__))
        html_file_path = os.path.join(dir_path, relative_path)
        with open(html_file_path) as f:
            html_template = f.read()
        return html_template

    def designer(self, recipe):
        html_template = self.load_html_template()
        title = recipe["title"]
        # date = recipe["date"]
        image = recipe["image"]
        totaltime = recipe["totaltime"]
        servings = recipe["servings"]
        ingredients = recipe["ingredients"]
        instructions = recipe["instructions"]

        # logging.debug(f"Recipe title: {title}")
        # logging.debug(f"Recipe image: {image}")
        # logging.debug(f"Recipe servings: {servings}")
        # logging.debug(f"Recipe ingredients: {ingredients}")
        
        # Replace basic placeholders
        html_template = html_template.replace("{{title}}", title)
        html_template = html_template.replace("{{image}}", image)
        html_template = html_template.replace("{{totaltime}}", totaltime)
        html_template = html_template.replace("{{servings}}", str(servings))
        # Create the ingredients list HTML
        ingredients_html = ""
        for ingredient in ingredients:
            ingredients_html += f"<li>{ingredient}</li>"
    
        # Replace the ingredients placeholder
        html_template = html_template.replace("{{ingredients}}", ingredients_html)

        # html_template = html_template.replace("{{date}}", date)
        # Create the instructions list HTML
        instructions_html = ""
        for instruction in instructions:
            instructions_html += f"<li>{instruction}</li>"
    
        # Replace the instructions placeholder
        html_template = html_template.replace("{{instructions}}", instructions_html)
       
        recipe["html"] = html_template
        recipe = self.save_recipe_html(recipe)
        return recipe

    def save_recipe_html(self, recipe):
        filename = re.sub(r'[\/:*?"<>| ]', '_', recipe['query'])
        filename = f"{filename}.html"
        path = os.path.join(self.output_dir, filename)
        with open(path, 'w') as file:
            file.write(recipe['html'])
        recipe["path"] = filename
        return recipe

    def run(self, recipe: dict):
        recipe = self.designer(recipe)
        return recipe
