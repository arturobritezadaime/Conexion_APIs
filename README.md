📊 U.S. Inflation Analysis
This Python script connects to the FRED API to download and analyze U.S. inflation data (CPIAUCSL). It calculates monthly and annual accumulated inflation for the last three years and exports the results to an Excel file.

📦 Requirements
Install the necessary libraries with:

Bash

pip install -r requirements.txt

⚙️ Setup
Get a free API key from the FRED website.

Create a .env file in the project's root directory.

Add your API key to the .env file:

Fragmento de código

FRED_API_KEY="your_api_key_here"
🚀 How to Run
Execute the script from your terminal:

Bash

python main.py
The script will save the results to inflacion_eeuu.xlsx.