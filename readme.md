The project is a command line tool with can be used to scrape housing information based on a home address
It requires the following dependancies to run:
1) python 3
2) selnium 

This applicaiton allows the user to type in an address and it will scrape all textual and photgraphic information about a house 
from home finder. The user has the option to persistently store the information in an sqlite database for a future session.
The tool also allows the user the option to delete any gathered photos, or housing information or display how many photos have been 
gathered for a given house. Due to inconsistancies between how different pages structure xpaths, it will try all known xPaths for a given
field before placing a default value. These default values allow the program to continue without terminating when insufficient 
information is available about a given page. 
