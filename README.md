# Two Pydantic-AI Agents for Website Data Extraction

This project demonstrates a simple example of scraping product data from web pages using two Pydantic-AI agents. It explores techniques for improving AI model performance by cleaning HTML content to reduce context and token usage.

## 1. Installation

First, make the installation and execution scripts executable:

sudo chmod +x install.sh<br>
sudo chmod +x run.sh



Then, run the install.sh script to create a virtual environment and install the necessary dependencies:<br>
./install.sh<br>
**Important**: Set your API key for the AI provider of your choice in the .env file.<br>

## 2. Usage
You can run the script in two ways:

**Method 1:** Command Line Argument

Provide the URL directly as a command-line argument:

./run.sh https://www.shop.com/product/43536 

**Method 2:** Interactive Mode

Run the script without arguments, and it will prompt you for the URL:

./run.sh

Paste the URL when prompted.

## 3. Code Examples
scrap.py: A basic example of direct web scraping using BeautifulSoup.<br>
scrap_clean.py: An experimental script testing HTML cleaning techniques to reduce context and token usage for improved AI model performance. The goal is to provide the AI with a more concise and relevant input.

## 4. Experimental Code
The trash directory contains incomplete and experimental code that was not fully implemented. Feel free to explore it, but be aware that it may not be functional.
