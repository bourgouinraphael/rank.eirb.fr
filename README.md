# Ranking system for egh tournaments

This repo contains the code used to calculate and display the results of the egh smash ranking
It's kinda badly written, and was originally planned to be a full blown website (hence the docker compose stack), but I didn't have the time for that
It could enjoy a full rewrite if someone is motivated enough

## Requirements

To run the full stack (with the graphics display), you need to have `docker` and `docker compose` installed

## Get an challonge Api v1 key

You also need to create a `.env` file in the `backend/src` directory, following the example of `.env.example`, and completing with and api key
To get one, go to challonge, in the account settings, in developer API, in manage at connect.challong.com. 
There should be a client named `Migrated APIv1 Key`, click on it and the api key is in the field `API v1 Key`

## Run with docker compose

To run the full stack, the command is
```
docker compose up --build
```

And go to `http://localhost:8080` with a browser
It will be blank for a while because it's fetching and calculating the results
After that, it will show the graphs and current standings according to the pr and elo system

## Changing communities

To change the communities that are analysed by the app, change the list `communities` present in the `./backend/src/app.py` file
This list contains community ids, which can be found inside the link of communities (for example https://challonge.com/communities/2e83a668fc9b0698f4ca2a09 would give `2e83a668fc9b0698f4ca2a09` for season 2)

## Add weights for the PR calculations

Inside the `./backend/src/pr_ranking.py` file, the list `WEIGHT_BY_TOURNAMENT` contains the weight of each tournaments.
The tournaments are designated by their tournament ids, which can be found in their links (for example https://challonge.com/9ug6n3oe would give `9ug6n3oe`)

## Visualisation

The page html code is under `./frontend/index.html`, it uses charts.js
