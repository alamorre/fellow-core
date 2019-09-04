# fellow-core
Server for fellow interview game.

### Getting Started
Checkout this repo, start a virtualenv, install dependencies, then setup database:

```
# Enter the codebase 
git clone https://github.com/alamorre/fellow-core.git
cd fellow-core

# Start a virtualenv 
python3 -m venv env
source env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up the DB
python manage.py migrate

# Start the server
python manage.py runserver
```
