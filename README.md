# Chat App

Simple chat app created using Python. 
This application allows several users to log in and talk in a chatroom and also to get stock quotes
from an API using a specific command.

## Design 
The chatapp consists of two independent packages or modules which should be executed as different processes. The packages are:
  chatapp/
  bot/

'chatapp' holds most of the functionality of the application. Handles user interaction, like messaging each other in the chatroom, as well as handling user input directed towards the bot. These messages directed towards the bot are handled by RabbitMQ on a separate thread as to not hold the webserver while awaiting for a reply.

'bot' is a simple container for a bot that is spawned and listens for commands given by users through the chat. The bot receives a message through the RabbitMQ queue designated for this and replies back to the waiting process.

Currently the project is simple enough for a SQLite database. Secret stuff like the `FLASK_SECRET_KEY` should be placed in a separated file at `<project directory>/chatapp/configs.json`. To test the project easily, the `setup` script will autogenerate a configuration file for you as well as initialize the database.

## Installation
The project requires the following Python packages to be installed:

* Flask
* Flask-SocketIO
* pika
* requests
* pytest

Remember to initialize your virtual environment before installing these packages. You can do this by doing 'python -m venv venv/' from the project's parent directory

All are installed via 'pip', and a 'requirements.txt' file is provided for easi installation via:
 
 pip install -r requirements.txt
 
Addiotionally, it is necessary to install the following:
  
  * rabbitMQ (see [this](https://www.rabbitmq.com/download.html) to install)

After installing and enabling the services head to the project's parent directory and run the following command to set the flask environment (depending on your OS):

  * Windows (cmd): 'set FLASK_APP=chatapp'
  * Windows (powershell): '$env:FLASK_APP = "chatapp"
  * Unic-based (bash): export FLASK_APP=chatapp

After completing this you can run the 'setup' script from the project's parent directory using the following command:

  python setup.py
  
This will generate a config file and auto-generato a secret key for flask session handling. You can find the config file in the 'instance' subdirectory. The setup will also initialzie the database for you.

## Running the webserver

Now that all the setup has been completed, it is time to start up our server. Simply execute the following command from inside the project's parent directory in your terminal of choice:

  python main.py
  
This will boot up the server and now we are ready to start chatting. Using your favorite browser, navigate to '127.0.0.1:5000' or 'localhost:5000' and you are ready. Register an account and log in to begin chatting.

To use bot commands, it is necessary to boot up the bot. On a separate terminal, initialize th bot by executing the following commmand from the 'bot' subdirectory in the project.

  python stock_bot.py
    
## Notes/Known issues

Currently there is no graceful way to terminate a bot after it has been initialized. Simply end execution by using a command line keyboard interrupt (ctrl + c for windows)
