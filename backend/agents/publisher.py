import os


class PublisherAgent:
    def __init__(self, output_dir):
        self.output_dir = output_dir

    def save_recipebook_html(self, recipebook_html):
        path = os.path.join(self.output_dir, "recipebook.html")
        with open(path, 'w') as file:
            file.write(recipebook_html)
        return path

    def run(self, recipebook_html: str):
        recipebook_path = self.save_recipebook_html(recipebook_html)
        return recipebook_path
