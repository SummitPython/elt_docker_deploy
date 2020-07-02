# elt_docker_deploy

This application has two main scripts:

- etl_cron.py : capture of the data
- main_web.py : webapp to visualize the data


The etl_cron.py will run schedulled in the cron of the container. See crontab file.

# Web Application

## Dev

To run the web app locally, first install the requirements:

    pipenv install

After, run the app

    pipenv run python src/main_web.py

## Docker 

To build the docker image, run of the webapp:

    docker build . -t jornada_etl

To run the image:

    docker run --name webapp --rm -p 8000:8000 jornada_etl

To run the application using Nginx, use:

    docker-compose up -d

## Docker hub

You can deploy your image to the docker hub, and copy only the file `docker-compose.yml`
to your server. Then, run only the `docker-compose up` command. 

To update your application, rebuild the image, then update in your server.

### Sending image to docker hub:

1. Login to docker hub

    docker login --username=yourhubusername --email=youremail@company.com
    
2. List your images

    docker images

3. Tag your image (by IMAGE ID) with a name, for example:

    docker tag bb38976d03cf jornadapython/jornada_etl:latest

4. Then, push your image to the hub

    docker push jornadapython/jornada_etl:latest
