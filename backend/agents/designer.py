import os
import re

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
        date = recipe["date"]
        image = recipe["image"]
        paragraphs = recipe["paragraphs"]
        html_template = html_template.replace("{{title}}", title)
        html_template = html_template.replace("{{image}}", image)
        html_template = html_template.replace("{{date}}", date)
        for i in range(5):
            html_template = html_template.replace(f"{{paragraph{i + 1}}}", paragraphs[i])
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
