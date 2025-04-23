#!/bin/sh

if [ ! -d migrations/versions ]; then
  flask --app oso_demo db init
fi

flask --app oso_demo db migrate
flask --app oso_demo db upgrade
python ./seed.py
flask run --debug