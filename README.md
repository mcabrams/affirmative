# Affirmative

## Getting started
Copy and rename `web.env.example` to `web.env` with necessary
secrets/configured environment variables.

`docker-compose -f docker-compose.test.yml build`
`docker-compose -f docker-compose.test.yml up -d`
`docker-compose exec web bash`


## Notes
You may need to create `/Volumes/dst` in docker container. Then try running
```
./manage.py shell
>>> from trigger import tasks
>>> tasks.watch_for_new_file('.')
```

Then outside the container run
```
touch foo.txt
```

Check your email.
