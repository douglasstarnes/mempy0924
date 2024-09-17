This demo implements a command line application that manages a portfolio of cryptocurrency investments.
It relies upon four packages listed in the `requirements.txt` file:

 * `click` - provides the command line functionality for parsing commands and options
 * `requests` - makes calling the CoinGecko API to retrieve real-time prices a single line of code
 * `rich` - formats the output of the commands
 * `sqlalchemy` - an ORM so that the application can access a database using Python objects instead of SQL statements

The easiest way to get started with the code is to open it in GitHub Codespaces.  In the repository, click the **Code** button and the **Codespaces** tab.  Then click the **Create codespace on main** button.

![Snag_20f32cd8](https://github.com/user-attachments/assets/8fb01859-bbbf-4b54-bafa-e48f6b928c7e)

In the new Codespace, click the Extension icon on the left side of the window:

![Snag_20f536e1](https://github.com/user-attachments/assets/aabe3f9d-a43a-4baa-9da5-7d1c61190e71)

Search for *python* in the search bar at the top and click the green **Install** button for the extension from Microsoft.

![Snag_20f7194d](https://github.com/user-attachments/assets/1d012204-9b73-493e-b473-a02a1809c497)

Next search for *sqlite* and install the *SQLite Viewer* extension from Florian Klampfer.

![Snag_20f8ab09](https://github.com/user-attachments/assets/798cd0fa-266d-42cf-a719-8f80a7b7ab25)

In the Terminal at the bottom of the window, install the packages in the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

To initialize the database with some investments, execute the `commands.sh` script:
```bash
. ./commands.sh
```

Now you can view the list of investments with the `list-portfolio` command:
```bash
python manager.py list-portfolio
```

Add a buy investment with the `buy-coin` command:
```bash
python manager.py buy-coin bitcoin 1.3
```

Add a sell investment with `sell-coin` command:
```bash
python manager.py sell-coin bitcoin 0.5
```

Lookup the current price of a coin with the `lookup-coin` command:
```bash
python manager.py lookup-coin bitcoin --currency gbp
```
