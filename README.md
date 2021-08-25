# TomocatDB
* [General info](#general-info)
* [Installation](#installation)
* [Setup](#setup)
* [Usage](#usage)

## General info
This is a pre-made SQLAlchemy/PostgreSQL data model wrapped in a python package. The toold is used within the TomoCAT project at the University of Oslo to store scientific data in a personal Postgres database. The TomocatDB is an ORM data model implemented with SQLAlchemy which provides an easy way of adding database support to other python applications. An example of this is the "BET-Analysis" appliction.

Tomocatdb requires a local Postgres database (this is most easily created and administered with PgAdmin4) as well as configuration of Alembic.

It is important that Alembic is used correctly if you want to alter the data model. For ORM to work the data model (i.e. database tables represeted by python classes) always needs to mirror the current version of the database. This is what Alembic is used for and is analogous to "GIT".

## Installation

1. clone the repository

```
$cd TomocatDB
$pip install .
```

## Setup
### Setting up your database
You should now be able to generate the database tables as per your ORM data model in models.py with alembic.

```
$alembic revision --autogenerate -m 'my first commit'
$alembic upgrade head
```

You can check the database tables using a software like DBeaver.

![image](https://user-images.githubusercontent.com/70808555/130825089-6345a73e-07a6-43d8-833d-02596be9b58b.png)

## Usage
## Interfacing with your database via TomocatDB


