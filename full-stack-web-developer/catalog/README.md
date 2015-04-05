
Udacity Full stack Web Developer
================================

Catalog Directory Project
-------------------------
Python files for udacity **Full Stack Web Developer** Nano Degree course's Catalog Directory Project

- **requirements.txt** - list of python modules needed to execute this project. you can install all of these using pip

- **db_create.py** - Helper file to create the database and the tables for this project. It uses information 
from models.py creates the table. Use this to create the database and tables before you start the project
- **db_migrate.py** - Helper function to help you update your database when you make changes in your table 
structure in models.py. You would use this if you are developing this project and need to make new database changes
- **db_upgrade.py** - Helper function to upgrade your database to next versions (usually saved by migrate script)
- **db_downgrade.py** - Helper function to downgrade your database to previous versions (usually saved by migrate script)

- **config.py** - collection of configs which will be used by the projects are defined here
- **run.py** - Python script to start the app server

- **app_server** - Files for App server
	- **templates** - HTML template files
		- **base.html** - Base template which will be inherited by other templates. Defines the title & naviagtion of the website
		
		- **login.html** - Portal to login an user. Will used OpenID to add new users as well
		
		- **categories.html** - home page of the project. Will show list of categories and last 10 updated items
		
		- **show_category.html** - Show a categry and the list of items in that category
		- **add_category.html** - template to add a new category
		- **edit_category.html** - template to edit existing category
		- **delete_category.html** - template to delete existing category
		
		- **show_item.html** - Show a description of an item
		- **add_item** - template to add a new item
		- **edit_item** - template to edit existing item
		- **delete_item** - template delete existing item

	- **views.py** - All URL routing and CURD operations are handled in this file
	- **myforms.py** - Defines forms that will be used by views.py for CURD operation
	- **models.py** - This file defines the tables needed for this project. 
	- **schemas.py** - This file defines schemas to generate JSON data for the tables

-----

Creating a virtual environment (Optional)
-----------------------------------------
It is recommended you keep dev and production environment separate to control module versions. These can 
be done using a virtual environment or a separate virtual system up like Vagrant or Docker.

An example is given to create a virtual environment for this project. Install virtualenv using the below command

```
sudo pip install virtualenv
```

You can create a virtual environment for the project now.
Go to the root folder of this project and execute this command to create a virtual environment called flask
 
```
virtualenv flask
```

You will see a new directory *flask* created in your directory

To activate this virtual environment run this command.

```
source flask/bin/activate
```

To install all the needed python modules for this project run this command. 
If not running in virtualenv use sudo to run this command

```
pip install -r requirements.txt
```

Now you should have all the needed python modules. Let us create the needed tables for our project with the command

```
python db_create.py
```
Now you should have all the needed tables in the database for your project

----------
Starting the App Server
-----------------------
After you have installed the needed modules, created the Database & Tables for the project. You can start 
the App Server by running
 
```
./run.py
```

from the root folder. This is launch the App server listening on port 8000 (defined in the file)

-------
JSON Data
---------
This project can also return JSON data with all Categories and its Items. This can be accessed at
http://localhost:8000/catalog.json (You may have to change localhost to your server's IP address)
