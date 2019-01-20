# Usage
##### Subscribe:
```
pipenv run python3 mpi/console.py subscribe \
    --email=c.c@gmail.com \
    --minimum-year=2005 \
    --model=CAR
```

##### Get Subscriptions:
```
pipenv run python3 mpi/console.py subscriptions
+--------------------------------------+---------------+-----------------------------------------------+
|           Subscription ID            |     Email     |                     Search                    |
+--------------------------------------+---------------+-----------------------------------------------+
| 07d570e4-6287-4a22-a728-0ccc7d78b7c1 | c.c@gmail.com | {'model': 'CAR', 'year': {'minimum': '2005'}} |
+--------------------------------------+---------------+-----------------------------------------------+
```

##### Process New Auctions:
```
pipenv run python3 mpi/console.py process
```

##### Start Development Webserver:
```
env FLASK_APP=mpi/web.py FLASK_DEBUG=1 pipenv run flask run
```