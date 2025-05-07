#!/usr/bin/env bash

echo "This command will recreate all the files and database of the project. Do you want to continue? (y/N)"
read answer

if [[ $answer != "y" && $answer != "Y" ]]; then
  echo "See you another time."
  exit 1
fi

# Get absolute path to script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Deleting existing files..."
# Don't delete directories, only delete files except the script itself
find . -type f -not -name "set_up_hylo_wagtail_project.sh" -delete
# Also remove directories
find . -type d -not -path "." -exec rm -rf {} +

echo "Creating and activating virtual environment..."
# Check if venv exists, if not create it
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi
source "$SCRIPT_DIR/venv/bin/activate"

echo "Installing Wagtail..."
pip install wagtail

echo "Creating a Wagtail project from the template..."
wagtail start --template=https://github.com/hyperlocalhq/hylo-wagtail-project-template/archive/refs/heads/main.zip myproject .

echo "Installing pip dependencies..."
if [ -f "requirements.txt" ]; then
  pip install -r requirements.txt
else
  echo "Warning: requirements.txt not found"
fi

echo "Creating the default database..."
if [ -f "Makefile" ]; then
  make load-data
else
  echo "Warning: Makefile not found, trying direct commands..."
  if [ -f "manage.py" ]; then
    python manage.py createcachetable
    python manage.py migrate
    python manage.py load_initial_data
    python manage.py collectstatic --noinput
  else
    echo "Error: manage.py not found"
  fi
fi

echo "Starting the local server..."
if [ -f "Makefile" ]; then
  make start
else
  echo "Warning: Makefile not found, trying direct command..."
  if [ -f "manage.py" ]; then
    python manage.py runserver
  else
    echo "Error: manage.py not found"
  fi
fi