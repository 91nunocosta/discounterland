# Discounterland

RESTful web service for generating discount codes.

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Code Coverage](coverage.svg)

## Installation

### From source

1. Install the required tools:

   1. Install [docker](https://docs.docker.com/get-docker/).

   2. Install [docker-compose](https://docs.docker.com/compose/install/).

2. Clone the repository.

   ```bash
   git clone git@github.com:91nunocosta/discounterland.git
   ```

3. Open the project directory.

   ```bash
   cd discounterland
   ```

4. Start docker containers with MongoDB and the web server:

   ```bash
   docker-compose up -d
   ```

5. Stop the dockers once you are done.

    ```bash
    docker-compose down
    ```

## Usage

You can find the full [Open API](https://swagger.io/specification/) documentation
[here](./.optic/generated/openapi.yaml).

It can also be viewed in a nice format in [Swagger Hub](https://app.swaggerhub.com/apis/nunocosta2/Discounterland/0.2.0/).

### Examples

The following sections exemplify how you can interact with the API using the _curl_.

You can execute the examples by running the script [examples.sh](examples.sh).
If you prefer to use [Postman](https://www.postman.com/),
you can import [postman_collection](doc/postman_collection.json) and
try the requests there.

Before executing the following examples, set the environment variable `TOKEN` with:

```bash
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI5MW51bm9jb3N0YUBnbWFpbC5jb20iLCJpYXQiOjE2MTY2MTY5NjN9.tMQoy_6ROA_sxWR1exWVeRZZZFR4qvMbO2Szos_XIMI
```

#### Get available resources

Get the available endpoints (the format is not Open API).

```bash
curl "http://0.0.0.0:5000/"

```

#### Create promotion

A brand's manager creates a promotion with _10_ discount codes available.

```bash
curl --location
     --request POST \
     'http://0.0.0.0:5000/brands/61a22c8f43cf71b9933afdd7/promotions' \
     --header "Authorization: Bearer ${TOKEN}" \
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

#### Create discount

A consumer generates a new discout code for himself/herself for the promotion created above.

```bash
curl --location \
     --request POST \
     'http://0.0.0.0:5000/consumers/61a2d3be596808c5d69dd11b/discounts' \
     --header "Authorization: Bearer ${TOKEN}" \
     --header 'Content-Type: application/json' \
     --data-raw '{
       "promotion_id": "61a2d5606ac07b74c824f1a9"
     }'
```

## Contributing

### How to prepare the development environment

1. Install the required tools:

   1. Install [_poetry_](https://python-poetry.org/) _package and dependency manager_.
   Follow the [poetry installation guide](https://python-poetry.org/docs/#installation).
   Chose the method that is more convenient to you, for example:

      ```bash
      curl -sSL\
           https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py \
         | python -
      ```

   2. Install [docker](https://docs.docker.com/get-docker/).

   3. Install [docker-compose](https://docs.docker.com/compose/install/).

2. Clone the repository.

   ```bash
   git clone git@github.com:91nunocosta/discounterland.git
   ```

3. Open the project directory.

   ```bash
   cd discounterland
   ```

4. Create a new virtual environment (managed by _poetry_) with the project dependencies.

   ```bash
   poetry install
   ```

5. Enter the virtual environment.

   ```bash
   poetry shell
   ```

6. Start docker containers with MongoDB:

   ```bash
   docker-compose -f ./docker-compose-dev.yaml up -d
   ```

7. Stop the docker once you are done.

    ```bash
    docker-compose -f ./docker-compose-dev.yaml down
    ```

### How to check code quality

1. Prepare the development environment, as described in
[**How to prepare the development environment**](#how-to-prepare-the-development-environment).

2. Lint and test code

     ```bash
     pre-commit run --all-files
     ```

### How to run  the functional tests

You can run all tests against a real server instance.

1. Run the script [functional_tests](./funtional_test.sh)

```bash
./funtional_test.sh
```
