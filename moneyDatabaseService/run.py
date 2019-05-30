##### RESTful API using Flask
import os
import sys
sys.path.insert(0, os.path.realpath(__file__).replace('run.py', '') + 'src')
from database_management import app

app.run(host='127.0.0.1', port=8077, debug=True)