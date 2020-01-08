# Time Tracker Project
This is a sample time tracking project using Django 100%. 

## Basic Setup ##

1. Create and activate a virtualenv (Python 3)
```bash
virtualenv -p python3 venv
source venv/bin/activate
```
2. Install requirements
```bash
pip install -r requirements.txt
```
3. Init database
```bash
./manage.py migrate
```

4. Create admin user
```bash
./manage.py createsuperuser
```

5. Collect static files
```bash
./manage.py collectstatic --noinput
```

6. Run development server (for development only).
```bash
./manage.py runserver
```

## Create a Local Settings File ##
You should create a local_settings.py file in the "timetracker" folder (where settings.py is) and override the default testing config.
