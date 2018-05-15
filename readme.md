The project is a command line tool with can be used to scrape housing information based on a home address
It requires the following dependancies to run:
1) python 3 (https://www.python.org/downloads/)
2) selnium (http://selenium-python.readthedocs.io/installation.html)
A driver for chrome was included to try and make program installation easier, but if the webdriver provides issues be sure to reinstall to match your operating system setup.

This application allows the user to type in an address and it will scrape all textual and photographic information about a house from
home finder. The user has the option to persistently store the information in an SQLite database for a future session.The tool also allows the user the option to delete any gathered photos, or housing information or display how many photos have been gathered for a given address. Due to inconsistencies between how different pages structure XPaths, it will try all known xPaths for a given field before placing a default value. These default values allow the program to continue without terminating when insufficient information is available about a given page. For instance not all house listings provide information about taxes or the homes cooling system, so in these cases, a value of 0 or n/a might be used to replace an unattained value. 
