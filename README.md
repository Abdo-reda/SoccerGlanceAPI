## Setup 

We recommend to setup virtual environment and install the needed packages using pip. 
You can check the requirements file for the core packages needed.
Also, this was tested on python 3.10

* `python -m venv myEnv`
* `myEnv\Scripts\activate `
* `pip install -r requirements.txt`

## Running the API server

`python manage.py runserver 0.0.0.0:8000`


## To Run with empty database:
1. delete all files in migration folders except __init__.
2. python3 manage.py makemigrations
3. python3manage.py migrate
4. Manually enter the top 5 leagues in the league table. Set another league record to Custom.
5. Create the PremiumPlus SubscriptionType


