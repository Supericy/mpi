# Usage
##### Subscribe:
```
bin/console subscribe \
    --email=c.c@gmail.com \
    --minimum-year=2005 \
    --model=CAR
```

##### Get Subscriptions:
```
bin/console subscriptions
+--------------------------------------+---------------+-----------------------------------------------+
|           Subscription ID            |     Email     |                     Search                    |
+--------------------------------------+---------------+-----------------------------------------------+
| 07d570e4-6287-4a22-a728-0ccc7d78b7c1 | c.c@gmail.com | {'model': 'CAR', 'year': {'minimum': '2005'}} |
+--------------------------------------+---------------+-----------------------------------------------+
```

##### Process New Auctions:
```
bin/console process
```

##### Start Local Development Server:
```
make server
```

##### Deploy
```
make deploy
```
