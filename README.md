# GPT Recipe

Welcome to the GPT Recipe project, an innovative autonomous agent designed to create personalized recipe books tailored to user preferences. GPT Recipe revolutionizes the way we discover and enjoy recipes by leveraging the power of AI to curate, write, design, and edit content based on individual tastes and interests.

## 🔍 Overview

GPT Recipe consists of seven specialized sub-agents in LangChain's new [LangGraph Library](https://github.com/langchain-ai/langgraph):

1. **Search Agent**: Scours the web for the latest and most relevant recipes.
2. **Curator Agent**: Filters and selects recipes based on user-defined preferences and interests.
3. **Writer Agent**: Crafts engaging and reader-friendly recipes.
4. **Critique Agent**: Provides feedback to the writer until the recipe is approved.
5. **Designer Agent**: Layouts and designs the recipes for an aesthetically pleasing reading experience.
6. **Editor Agent**: Constructs the recipe book based on the produced recipes.
7. **Publisher Agent**: Publishes the recipe book to the frontend or desired service.

Each agent plays a critical role in delivering a unique and personalized recipe book experience.

<div align="center">
<img align="center" height="500" src="https://example.com/gpt-recipe-architecture.png" alt="GPT Recipe Architecture">
</div>

## Demo
[Check out our demo video here](https://example.com/gpt-recipe-demo)

## 🌟 Features

- **Personalized Content**: Get recipes that align with your tastes and preferences.
- **Diverse Sources**: Aggregates recipes from a wide range of reputable sources.
- **Engaging Design**: Enjoy a visually appealing layout and design.
- **Quality Assurance**: Rigorous editing ensures reliable and accurate recipe instructions.
- **User-Friendly Interface**: Easy-to-use platform for setting preferences and receiving your recipe book.

## 🛠️ How It Works

1. **Setting Preferences**: Users input their interests, preferred ingredients, and cuisine types.
2. **Automated Curation**: The Search and Curator Agents find and select recipes.
3. **Content Creation**: The Writer Agent drafts recipes, which are then designed by the Designer Agent.
4. **Recipe Book Design**: The Editor Agent reviews and finalizes the content.
5. **Delivery**: Users receive their personalized recipe book in their mailbox.

## 🚀 Getting Started

### Prerequisites

- Tavily API Key - [Sign Up](https://tavily.com/)
- OpenAI API Key - [Sign Up](https://platform.openai.com/)

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/yourusername/gpt-recipe.git

2. Export your API Keys
   ```sh
    export TAVILY_API_KEY=<YOUR_TAVILY_API_KEY>
    export OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>

3. Install Requirements
    ```sh
    pip install -r requirements.txt

4. Run the app
    ```sh
    python app.py

5. Open the app in your browser
    ```sh
    http://localhost:5000/
    
6. Have fun searching for recipes and enjoying your meals!

## 🛡️ Disclaimer

GPT Recipe is an experimental project and is provided "as-is" without any warranty. It is intended for personal use and not as a replacement for professional recipe books or culinary advice.


