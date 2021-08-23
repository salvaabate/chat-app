import json
import os
import random
import string
import subprocess


def random_key():
    return ''.join([random.SystemRandom().choice("{}{}{}".format(
        string.ascii_letters, string.digits, string.punctuation)) for i in range(50)])


CONFIGS = {
    'FLASK_SECRET_KEY': random_key(),
}

# Check if configuration file exist, if not, create it
CURRPATH = os.getcwd()
PATH = CURRPATH + '/instance/'
CONFIG_FILE = 'configs.json'

if not os.path.exists(PATH + CONFIG_FILE):
    # Check if directory exists
    if not os.path.exists(PATH):
        os.makedirs(PATH, exist_ok=True)

    with open(PATH + CONFIG_FILE, 'w+') as conf_file:
        json.dump(CONFIGS, conf_file)

os.system("flask init-db")
