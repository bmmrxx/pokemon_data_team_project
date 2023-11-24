# BitTigers3.0

This Pokemon Dashboard has been developed to allow users to explore detailed information about Pokemon and compare their own Pokemon with others. Below are instructions on how to set up and use the dashboard.

### Table of Contents
1. Installation
2. Usage
    - Page 1: Pokemon Information
    - Page 2: Arena
3. Libraries
4. Developers

### Installation
Before using the dashboard, follow these steps:

1. Install required libraries

pip install requirements.txt

2. Database Configuration
- Ensure you have a working SQL Server.
- Modify the database configuration in the script to connect to the correct database.

3. Add Pokemon API Key
- Register on the Pokemon API website to obtain an API key.
- Add the API key to the script to access Pokemon data.

### Usage

#### Page 1: Pokemon Information
On this page, you will find comprehensive information about various Pokemon.
Use the search function to look up specific Pokemon.
Discover details such as type, height, weight, and more.

#### Page 2: VS Board
Compare your Pokemon with another Pokemon.
Select your Pokemon and enter the name of the other Pokemon.
Receive a comparative analysis based on various statistics.

### Libraries
This project uses the following Python libraries:

- requests: For making HTTP requests to the Pokemon API.
- pyodbc: For database connectivity with SQL Server.