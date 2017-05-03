# Voice Assist Backend Service and Web App
A smart nursing request system built 


## Setup Database
1. [Download PostgreSQL](https://www.postgresql.org/download/)
2. Open the client and make sure it's running locally
3. Run the setup_tables.sql script in the psql console

## Connect to IBM Watson
1. Setup an instance of [IBM Watson's Natural Language Understanding](https://console.ng.bluemix.net/catalog/services/natural-language-understanding) service
2. Get the service credentials from the service and fill in the username and password in app.py

## Setup Server
1. Install requirements `pip install -r requirements.txt`
2. Set environment variable `export FLASK_APP=app.py`
3. Run server 'flask run'
4. Go to <localhost:5000>

## To deploy onto Heroku
1. The app is currently setup to be deployed on Heroku, [follow instructions here](https://devcenter.heroku.com/articles/getting-started-with-python#introduction)
2. Provision a PostgreSQL add-on onto the Heroku server, [follow instructions here](https://devcenter.heroku.com/articles/heroku-postgresql#provisioning-the-add-on)
