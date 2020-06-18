# TheatreManagement

This project is submitted as part of course requirements for CS254, DBMS lab.

This project was done by:

Feyaz Baker  - 181CO119

Nihar KG Rai - 181CO235

# Setup instructions

Run

```
python3 -m pip install -r requirements.txt
```

to install all requirements needed.

## If you want to run mysql version on linux:

Go into dbms/settings.py, and uncomment lines 80 - 89, and comment out lines 91 - 96.

Open Mysql, and create a user 'dbms_proj_user', and a database named 'dbms_project'. Supply the password into the corresponding password field in the curly braces. 

Refer https://www.digitalocean.com/community/tutorials/how-to-create-a-django-app-and-connect-it-to-a-database for a more detailed process, using a separate file for the login credentials.

# Running the project

Run

```
python3 manage.py makemigrations

python3 manage.py migrate

python3 manage.py createsuperuser

python3 manage.py runserver
```

Note step #3, createsuperuser, is to make a super user that can access the admin panel. It is not possible to add another user as admin without accessing the admin panel, and it is not possible to access the admin panel without being an admin.

## Comments

For ease of testing, we have made a database that you can use to view the complete product.

The admin username is 
`
feyaz
`
and the password is 
`
pass
`
.

To delete all this data, simply delete db.sqlite3 file present in this directory.

