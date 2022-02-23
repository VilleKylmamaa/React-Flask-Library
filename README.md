# React-Flask-Library

Small full stack project.

Frontend: React

Backend: Flask


<br />


# Installation


**1. If not already installed, install** [**NodeJs**](https://nodejs.org/en/download/), [**Python**](https://www.python.org/downloads/) **and** [**Pip**](https://pypi.org/project/pip/). If you encounter problems with installation or running, try updating these 3 to the latest versions.


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


**3. Install the required libraries for the Flask backend.**

In the root folder, where the requirements.txt file is located, run the following in command prompt:
 
 ```
 pip install -r requirements.txt
 ```
 
This should also setup the project through setup.py (in the api folder). If not, try updating pip to the newest version and running the command again.


**4. Install React for the project in the frontend folder:**

```
cd frontend // or open a new command prompt in the frontend folder
npm install
```


<br />


# Running

**1. Run the application (both frontend and backend) in localhost with a single command:**

```
.\start-all.bat
```

The React client (opens automatically) will be running in:

>http://localhost:3000/

The Flask API will be running in: 

>http://localhost:5000/api/


**2. If you with to reset the database with the default values, run:**

```
.\init-db.bat
```

<br />


# Tests

**1. The project and the required libraries should be installed. If not, see above in the installment section.**

**2. To run the tests for the API, run:**

```
.\run-backend-tests.bat
```

Tests for the frontend are not implemented.


