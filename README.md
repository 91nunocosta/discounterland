# How to run locally

To run the application locally you will need:
- [docker](https://docs.docker.com/engine/install/)
- [docker-compose](https://docs.docker.com/compose/install/)

Clone this repository to some directory of your choice:

```bash
$ git clone git@github.com:91nunocosta/discounterland.git
```

Go inside the project:

```bash
$ cd discounterland
```

Run docker-compose to build and run the required docker containers:
```bash
$ docker-compose up -d
```

Do your requests:
```bash
$ curl "http://0.0.0.0:5000/"
```
This request returns you the available endpoints.

You can run the script [examples.sh](examples.sh). The script contains some examples of valid requests. You should get success responses to all requests, if no change was made to the database.

If you prefer to use [Postman](https://www.postman.com/), you can import [postman_collection](doc/postman_collection.json) and try the requests there.

Once you are done, stop the docker containers running:
```
$ docker-compose down
```

# API

You can find the full [Open API](https://swagger.io/specification/) documentation [here](./.optic/generated/openapi.yaml).

It can also be viewed in a nice format in [Swagger Hub](https://app.swaggerhub.com/apis/nunocosta2/Discounterland/0.2.0/).

Here are some examples of requests from [examples.sh](examples.sh).

## Create promotion

```bash
curl --location --request POST 'http://0.0.0.0:5000/brands/61a22c8f43cf71b9933afdd7/promotions' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI5MW51bm9jb3N0YUBnbWFpbC5jb20iLCJpYXQiOjE2MTY2MTY5NjN9.tMQoy_6ROA_sxWR1exWVeRZZZFR4qvMbO2Szos_XIMI' \
--header 'Content-Type: application/json' \
--data-raw '{
  "expiration_date": "2022-11-25T16:51:02.003Z",
  "product": {
    "name": "Nutella",
    "images": [
      "https://images.jumpseller.com/store/hercules-it-llc/10188702/Nutella.jpg?1623999446"
    ]
  },
  "discounts_quantity": 10
}'
```

## Create discount

```bash
curl --location --request POST 'http://0.0.0.0:5000/consumers/61a2d3be596808c5d69dd11b/discounts' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI5MW51bm9jb3N0YUBnbWFpbC5jb20iLCJpYXQiOjE2MTY2MTY5NjN9.tMQoy_6ROA_sxWR1exWVeRZZZFR4qvMbO2Szos_XIMI' \
--header 'Content-Type: application/json' \
--data-raw '{
  "promotion_id": "61a2d5606ac07b74c824f1a9"
}'

```

# Code quality

There are some code quality verifications:
1. linting
1. type checking (as python is an interpreted language, it's possible to run a program even if the type annotations are wrong)
1. unit test
1. test coverage (in this case configured to 100%).

These verifications are preformed by several tools. [pre-commit](https://pre-commit.com/) is used to automate the entire verification pipeline. You can check which tools are used in the [pre-commit configuration](.pre-commit-config.yaml)

To run the code quality verifications in your machine you will need:
- python3
- pip
- [docker](https://docs.docker.com/engine/install/)
- [docker-compose](https://docs.docker.com/compose/install/)

Clone this repository to some directory of your choice:

```bash
$ git clone git@github.com:91nunocosta/discounterland.git
```

Go inside the project:

```bash
$ cd discounterland
```

To install `pre-commit` execute:
```
$ pip install pre-commit
```

To be able to run the tests, an instance of MongoDB is needed. For that run:
```
$ docker-compose -f docker-compose-dev.yaml up -d
```

To execute the verifications, run:
```
$ pre-commit run --all-files
```

For stopping the MongoDB instance (and releasing all the docker resources needed for it), run:
```
$ docker-compose -f docker-file-dev.yaml down
```

## Functional Tests

You can run the tests againts a real server instance.

Follow the tests above replacing `pre-commit run --all-files` by:

```bash
./functional_tests.sh
```
