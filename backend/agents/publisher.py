import os

class PublisherAgent:
    """
    A class used to represent a publisher agent for saving HTML recipe books to a specified directory.

    Attributes
    ----------
    output_dir : str
        Directory where the generated HTML recipe book file will be saved.

    Methods
    -------
    __init__(output_dir: str):
        Initializes the PublisherAgent class with the specified output directory.
    
    save_recipebook_html(recipebook_html: str) -> str:
        Saves the generated HTML recipe book to a file in the output directory.
    
    run(recipebook_html: str) -> str:
        Runs the save_recipebook_html method to save the HTML recipe book and returns the file path.
    """

    def __init__(self, output_dir):
        """
        Initializes the PublisherAgent class with the specified output directory.

        Parameters
        ----------
        output_dir : str
            Directory where the generated HTML recipe book file will be saved.
        """
        self.output_dir = output_dir

    def save_recipebook_html(self, recipebook_html: str) -> str:
        """
        Saves the generated HTML recipe book to a file in the output directory.

        Parameters
        ----------
        recipebook_html : str
            The HTML content of the recipe book.

        Returns
        -------
        str
            The path to the saved HTML recipe book file.
        """
        path = os.path.join(self.output_dir, "recipebook.html")
        with open(path, 'w') as file:
            file.write(recipebook_html)
        return path

    def run(self, recipebook_html: str) -> str:
        """
        Runs the save_recipebook_html method to save the HTML recipe book and returns the file path.

        Parameters
        ----------
        recipebook_html : str
            The HTML content of the recipe book.

        Returns
        -------
        str
            The path to the saved HTML recipe book file.
        """
        recipebook_path = self.save_recipebook_html(recipebook_html)
        return recipebook_path
