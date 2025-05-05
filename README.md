# Oso Demo: Flask

A simple shopping cart application to demonstrate the features of Oso

## Run

to get started:

```
# install oso cloud cli
curl -L https://cloud.osohq.com/install.sh | bash

# setup local-dev environment for oso-cloud cli testing
export OSO_URL=http://localhost:9090
export OSO_AUTH=e_0123456789_12345_osotesttoken01xiIn

# in another window run docker
docker compose up --build

# test it out -> should return 80 lines
oso-cloud get | wc -l

# test it out -> should return 5 lines
oso-cloud query allow User:_ "update" Shop:_
```

### about the dev environment

The system is built using docker compose:
1. oso dev server: 
   1. uses `public.ecr.aws/osohq/dev-server:latest`
   2. maps volume to ./authorization and ./.oso for data
   3. maps default 8080 to localhost 9090
   4. `docker exec -it oso-flask-app-1 sh`
2. postgres database
   1. uses `postgres:17-alpine`
   2. `postgres/postgres` as username and password
   3. maps `localhost:5444` to `5432`
   4. `docker exec -it oso-flask`
   5. `oso_cart` is the database
   6. `psql -U postgres oso_cart` on docker
   7. `psql -p 5444 -h localhost -U postgres oso_cart` on localhost
3. Python flask
   1. uses `Dockerfile.app` with `python:3.12-alpine` image
   2. exposes 5000 to localhost

## References
1. [Oso Overview](https://www.osohq.com/docs/what-is-oso-cloud)
2. [Oso Cli](https://www.osohq.com/docs/app-integration/client-apis/cli)
3. [Oso Dev Server](https://www.osohq.com/docs/development/oso-dev-server)
4. [Oso Python Api](https://www.osohq.com/docs/app-integration/client-apis/python)

## erd diagram

![erd for application](erd.png)
