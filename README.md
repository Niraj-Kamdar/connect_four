# Connect 4 REST API

This is a REST API service which allows playing multiple connect 4 games simultaneously. You can try it live on [connect-four-rest.herokuapp.com](https://connect-four-rest.herokuapp.com/).


## Usage

You can see documentation of API in both [swagger](https://connect-four-rest.herokuapp.com/docs) and [redoc](https://connect-four-rest.herokuapp.com/redoc) style.

### How to use it?
- Start a new game by POST request to `/start` endpoint.
- You can see current state of the game by GET request to `/game/{game_id}`.
- You can abort game by DELETE request to `/game/{game_id}`.
- You can throw stone in game at any column by PUT request to `/game/{game_id}`. 

> Note: columns are zero-indexed.
 
## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. If you want to use it in production you can skip to the deployment section.

### Prerequisites

- python 3.8 
- pipenv

### Installing
After cloning/downloading this repository you have to install necessary packages from Pipfile with following command

```console
pipenv install
```

This will install all dependencies needed to run the server.

### Starting server

After installation you just need to run following command to start server.

```console
uvicorn app.main:app
```
> You can stop server by pressing ctrl+c.

## Deployment

If you want to deploy this application. You can do this easily by running following command

```console
docker-compose up
```

This will build docker image and will start all required services to run server. You can visit server on `localhost:80`.
You can see documentation of API on `localhost/docs` or `localhost/redoc`. 
