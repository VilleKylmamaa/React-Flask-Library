# React-Flask-Library

Small full stack project.

Frontend: React

Backend: Flask


<br />


# Installation and Running


**1. If not already installed, install** [**NodeJs**](https://nodejs.org/en/download/), [**Python**](https://www.python.org/downloads/) **and** [**Pip**](https://pypi.org/project/pip/). If you encounter problems with installation and running, try updating these 3 to the latest versions.


**2. (Optional) Use** [**virtual environment**](https://docs.python.org/3/tutorial/venv.html).

A virtual environment is a private copy of the Python interpreter onto which you can install packages privately, without affecting the global Python interpreter installed in your system. In the root folder, to create the virtual environment, run the command:

```
python -m venv venv
```

Then start using the virtual enviroment with the command:

in Windows:

```
venv\Scripts\activate.bat
```

in Mac or Linux:

```
source venv/bin/activate
```


**3. Install the project and required libraries (Flask, Flask-RESTful, SQLAlchemy, Flask-SQLAlchemy, etc.).**

In the root folder, where the requirements.txt file is located, run the following command in command prompt:
 
 ```
 pip install -r requirements.txt
 ```
 
 This alone should also install the project through setup.py. If not, try updating pip to the newest version.
 

**4. Install React for the project:**

```
npm install
```


**5. Run the Flask backend and React frontend in localhost with a single command:**

```
npm run start-all
```


**6. To reset the database with the default values, run:**

```
npm run init-db
```


**6. The API is now running in localhost:5000.**

The Flask API will be running in: 

>http://localhost:5000/api/

The React client (opens automatically) will be running in:

>http://localhost:3000/


<br />


# Running tests

1. Project and the required libraries should be installed. If not, see above in the installment section.

2. To run the tests for the database and the API, run:

```
npm run test-api
```

Frontend tests are not implemented.


