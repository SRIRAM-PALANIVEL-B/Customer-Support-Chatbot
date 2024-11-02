# Customer-Support-Chatbot

# Customer Support Chatbot Application

This project implements a customer support chatbot that leverages web scraping and OpenAI's GPT model to provide users with relevant information based on the content of a specified website. The application is built using Streamlit and allows users to input a URL, scrape content from the website, and interact with the chatbot to get support.

## Features
- **Web Scraping**: Extracts relevant text content from a given website using BeautifulSoup.
- **Interactive Chatbot**: Users can chat with the bot, which generates responses based on the scraped content.
- **Conversation History**: Keeps track of user interactions for contextually relevant responses.
- **User-Friendly Interface**: Built with Streamlit for easy access and interaction.

## Technologies Used
- **Python**: The main programming language for the application.
- **Streamlit**: Framework used to create the web application.
- **OpenAI API**: Utilized for generating responses from the chatbot using the GPT model.
- **BeautifulSoup**: Library for web scraping to extract content from HTML.
- **dotenv**: Manages environment variables for secure configuration.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/customer-support-chatbot.git
   cd customer-support-chatbot

# Create a virtual environment (optional but recommended):

    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    
# Install the required packages:

    pip install -r requirements.txt
    
# Create a .env file in the root directory and add your OpenAI API key:

    OPENAI_API_KEY=your_api_key_here

# Usage
To run the application, execute the following command:

    streamlit run app.py
Open your web browser and navigate to http://localhost:8501 to access the Customer Support Chatbot application.

# How It Works
  - The user enters a website URL to scrape content from.
  - The application fetches and processes the text content of the website, saving it to a file.
  - The user can then interact with the chatbot by asking questions.
  - The chatbot formulates responses based on the scraped content and the conversation history.
    
#Environment Variables

To use the OpenAI API, you need to set the following environment variable:

  - OPENAI_API_KEY: Your OpenAI API key.
    
Make sure to keep this key private and secure.



![Project Logo](logo.png)
