# Kanban v1

Kanban is an application built in Flask for managing tasks in a project.

## Run Locally (cmd)

Go to the project directory

Create a virtual environment

```cmd
  py -3 -m venv env
```

Activate the virtual environment

```cmd
  env\Scripts\activate.bat
```

Install dependencies

```cmd
  pip install -r requirements.txt
```

Start the server

```cmd
  python main.py
```

## Run Locally (bash)

Extract the .zip file

Go to the project directory

Create a virtual environment

```cmd
  python -m venv env
```

Activate the virtual environment

```cmd
  . env/Scripts/activate
```

Install dependencies

```cmd
  pip install -r requirements.txt
```

Start the server

```cmd
  python main.py
```

## Folder Structure

- `app` - Application code is present in this folder.
- `static` - Default `static` files folder. It serves at '/static' path. More about it is [here](https://flask.palletsprojects.com/en/2.0.x/tutorial/static/).
- `templates` - Default flask templates folder.
- `kanban_db.sqlite3` - Application database file.
- `main.py` - The main entry-point of the app to setup and initialize.
- `README.md` - A readme file that explains how to run the code.
- `requirements.txt` - Contains the project dependencies.

## Author

- Vaibhav Kesharwani (vaibhav.vk2128@gmail.com)
