#!/bin/sh

if [ ! -d migrations ]; then
  flask --app oso_demo db init
fi

flask --app oso_demo db migrate
flask --app oso_demo db upgrade
flask run --debug