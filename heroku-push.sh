#!/bin/bash

heroku container:login
docker build -t registry.heroku.com/pytoys-api/web .
docker push registry.heroku.com/pytoys-api/web
heroku container:release -a pytoys-api web