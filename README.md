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
$ curl "http://0.0.0.0:5000/api-docs"
```
This request returns you the Open API spec mentioned in the next section.

You can run the script [examples.sh](examples.sh). The script contains some examples of valid requests. You should get success responses to all requests, if no change was made to the database.

If you prefer to use [Postman](https://www.postman.com/), you can import [postman_collection](doc/postman_collection.json) and try the requests there. 

Once you are done, stop the docker containers running:
```
$ docker-compose down
``` 

# API

You can find the full [Open API](https://swagger.io/specification/) documentation in [open-api-spec.json](doc/open-api-spec.json).

It can also be viewed in a nice format in [Swagger Hub](https://app.swaggerhub.com/apis/nunocosta2/Discounterland/0.1.0/).

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
curl --location --request POST 'http://0.0.0.0:5000/consumers/61a22cb797321cee10c8df49/discounts' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0MTI5ODM0OTg5IiwibmFtZSI6IlBhdHJpY2siLCJpYXQiOjE1MTYyMzkwMjJ9.UNxtO1rOKdkMawosiKiaQ3yupcKZWAvev1N0Lb49m28' \
--header 'Content-Type: application/json' \
--data-raw '{
  "promotion_id": "/promotions/9e169116-e3de-41cc-952a-149ed1cc4b40"
}'
```

# Code quality

There are some code quality verifications:
1. linting
1. type checking (as python is an interpreted language, it's possible to run a program even if the type annotations are wrong)
1. unit test
1. test coverage (in this case configured to 100%).

These verifications are preformed by several tools. [Tox](https://tox.readthedocs.io/en/latest/) is used to automate the entire verification pipeline. You can check which tools are used in the [tox configuration](tox.ini)

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

To install `tox` execute:
```
$ pip install tox
```

To be able to run the tests, an instance of MongoDB is needed. For that run:
```
$ docker-compose -f docker-compose-dev.yaml up -d
```

To execute the verifications, run:
```
$ tox
```

For stopping the MongoDB instance (and releasing all the docker resources needed for it), run:
```
$ docker-compose -f docker-file-dev.yaml down
```

# Discussion

Here is some explanation for my choices in this exercise.

## API design

I chose to follow [REST architectural style](https://en.wikipedia.org/wiki/Representational_state_transfer). REST is suitable for the CRUD (Create, Read, Update, Delete) interface described in the requirements, and it positively affects:

* _Performance_ in component interactions.

* _Scalability_ — allowing the support of large numbers of components and interactions among components.

* _Simplicity_ of a uniform interface.

* _Modifiability_ of components to meet changing needs (even while the application is running).

* _Visibility_ of communication between components by service agents.

* _Portability_ of components by moving program code with the data.

* _Reliability_ in the resistance to failure at the system level in the presence of failures within components, connectors, or data.

The operation of reordering tasks is the more challenging to model with the CRUD interface. But if we see the position of a task as part of its status, then reordering is also an update operation. This approach has some important benefits:

1. The uniform interface is preserved. It avoids adding an extra operation whose semantics would be ad-hoc.

1. Adding, removing and moving items with positions has a well-known semantics: the same as the arrays.

1. The front-end can add or remove tasks at any position with a single request. When a task is moved, the front-end only need to track how its position changed. The front-end doesn't need to care about any other task.


## Stack

The stack I chose to use is.
1. python3 
1. [MongoDB](https://www.mongodb.com/)
1. [python eve](https://docs.python-eve.org/en/stable/)

Here are the reasons for the choice.

### python

It's the programming language with which I'm more proficient. It's not as performant as a compiled language. But in a REST back-end mainly concerned with data persistence, it's reasonable to assume that the such difference is not important. The agility of development would be more important. As a high-level language, with powerful abstractions, python makes agility easy to achieve.

## MongoDB

Modeling a RESTful resource as a collection of documents is usually easier than modeling it with a relation (aka table). In the documents case, the mapping is, most of the time, one-to-one. An item of the API with certain fields can be stored as a document with exactly the same fields (including any nesting). 

Consider the following requests.
```
POST /tasks
{
    "summary": "A task.",
    "done": true,
    "type": "simple",
}
```

```

POST /tasks
{
    "summary": "A task.",
    "done": true,
    "type": "custom",
    "custom_fields": {
        "status": "Approved"
    }
}
```

In a MonoDB both items can be created in a collection _tasks_ with exactly the same structure they have in the requests. In this way, there is no need to spend extra time thinking about the DB schema: it is equal to the API schema. There may be cases where the mapping can't be one-to-one. But many times it can. That is the case in the API developed here.

It's possible to argue that the same could be achieved in relational DB as well. The nested `custom_fields` document could be stored as json field. The difference is that Mongo can query for any field of a nested document (e.g. `status`) as efficiently as for any other non-nested field (e.g `summary`). That is not usually the case in a relational DB.

Other more general advantages of MongoDB are:
1. *Flexible document schemas*.

1. *Code native data access* — data can be accessed using native programming language's data structures (e.g. python's dict, JavaScript's associative array, Java's Map). There is no need for ORM or other kind of wrappers.

1. *Change-friendly design* — changing the DB schema doesn't imply any downtime or complex migration process. It is possible to start writing the data in a new format at any time without disruptions. Older data can be migrated to the new format at any time. 

1. *Easy horizontal scale out* — MongoDB is designed to be a distributed database. It is possible to create clusters with real-time replication, and shard large or high-throughput collections across multiple clusters to sustain performance and scaler horizontally.

There are some situations where using MongoDB would not be appropriate. MongoDB violates [ACID](https://en.wikipedia.org/wiki/ACID) (atomicity, consistency, isolation, durability) (see [here](https://en.wikipedia.org/wiki/MongoDB#Transactions)). This means that failed operations (e.g. after power failures) may make the stored data invalid. There are contexts where this is not acceptable (e.g. banking). I assumed that it's not the case in this exercise.

## python eve

[Eve](https://docs.python-eve.org/en/stable/) is a [Flask](https://flask.palletsprojects.com/) extension for building RESTful APIs. It only needs a definition of the resources (see [discounterland/app/settings.py](discounterland/app/settings.py)). Then it provides the CRUD operations for those resources on top of a MongoDB. Most of the time, adding or changing an endpoint is a small change in the definition. In case that such is not possible we can still rely on Flask (see, for example, the login endpoint implemented in [discounterland/app/auth.py](discounterland/app/auth.py)) flexibility. This is why I chose eve. 

With eve we also benefit from the REST constraints without extra work. In particular, some _uniform interface_ constraints that would be laborious to implement:
1. Resource identification in requests
1. Self-descriptive messages
1. Hypermedia as the engine of application state (HATEOAS)

 
# Next steps

