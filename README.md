# Fellow Core
Server for fellow interview game.

### Before Starting
Make sure you have a virtual environment set up. Choose one of the two options

#### 1. Create with default (python default should NOT be 2.7)
```
python3 -m venv env
source env/bin/activate
```

#### 2. Create with Conda
```
conda create -n fellenv python=3
source activate fellenv
```

### Getting Started
Checkout this repo, start a virtualenv, install dependencies, then setup database:

```
# Enter the codebase 
git clone https://github.com/alamorre/fellow-core.git
cd fellow-core

# Install dependencies
pip install -r requirements.txt

# Set up the DB
python manage.py migrate

# Start the server
python manage.py runserver
```
