# Affirmative

## Getting started
Add paths to your src and dst directory volumes in the docker-compose.yml file:
```
    volumes:
      - "SOME_PATH:/Volumes/src/"
      - "SOME_PATH:/Volumes/dst/"
```

Copy and rename `web.env.example` to `web.env` with necessary
secrets/configured environment variables.

`docker-compose -f docker-compose.test.yml build`
`docker-compose -f docker-compose.test.yml up -d`
`docker-compose exec web bash`

Then run in the container
```
./manage.py migrate
```


## Notes
You may need to create `/Volumes/dst/` in docker container. Then try running
```
./manage.py shell
>>> from trigger import tasks
>>> tasks.watch_for_new_file('/Volumes/src/')
```

Then outside the container run in directory you previously mapped to
`/Volumes/src/`
```
touch foo.txt
```

Check your email.
