# simplechat

Simple application of a chat server with web client.

## How to set up

In order to set this project on your system it must have docker, git, virtualenv and pip installed, and follow the next steps:

1. clone repo

```
git clone https://github.com/alexandercch/simplechat.git
cd simplechat
```

2. create virtual environment and install dependencies

```
virtualenv -p python3 venv
source venv/bin/activate
cd simplechat
pip install -r requirements.txt
```

3. run migrations, create users, use this command and fill as propted, we suggest create 2 or more users to test

```
./manage.py migrate
./manage.py createsuperuser
```

4. start redis container and celery task, run the celery task in another terminal with the virtual environment activated

```
docker run -p 6379:6379 -d redis:5
celery worker -A simplechat --loglevel=info
```

the docker command may need sudo permission

5. run application and create chat rooms on admin

```
./manage.py runserver
```
on browser go to localhost:8000/admin and create some room objects, use user and password create in step 3

6. chat

on browser go to localhost:8000/chat/
login if not already logged and chat
