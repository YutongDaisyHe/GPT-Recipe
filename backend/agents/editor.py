import os

recipe_templates = {
    "layout_1.html": """
    <div class="recipe">
        <a href="{{path}}" target="_blank"><h2>{{title}}</h2></a>
        <img src="{{image}}" alt="Recipe Image">
        <p>{{summary}}</p>
    </div>
    """,
    "layout_2.html": """
    <div class="recipe">
        <img src="{{image}}" alt="Recipe Image">
        <div>
            <a href="{{path}}" target="_blank"><h2>{{title}}</h2></a>
            <p>{{summary}}</p>
        </div>
    </div>
    """,
    "layout_3.html": """
    <div class="recipe">
        <a href="{{path}}" target="_blank"><h2>{{title}}</h2></a>
        <img src="{{image}}" alt="Recipe Image">
        <p>{{summary}}</p>
    </div>
    """,
}

class EditorAgent:
    def __init__(self, layout):
        self.layout = layout

    def load_html_template(self):
        template_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'recipebook', 'layouts', self.layout)
        with open(template_path) as f:
            return f.read()

    def editor(self, recipes):
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
        # html_template = html_template.replace("{{date}}", recipes[0]["date"])
        recipebook_html = html_template.replace("{{recipes}}", recipes_html)
        return recipebook_html

    def run(self, recipes):
        res = self.editor(recipes)
        return res
