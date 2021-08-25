# TomocatDB

This is a pre-made SQLAlchemy/PostgreSQL data model wrapped in a python package. The toold is used within the TomoCAT project at the University of Oslo. 
The data model for storing simple scientific data in a postgres database. The ORM datamodel implemented with SQLAlchemy provides an easy way of adding database support to other python applications. An example of this is the "BET-Analysis" appliction.

Tomocatdb requires a local Postgres database (this is most easily created and administered with PgAdmin4) as well as configuration of Alembic.

It is important that Alembic is used correctly if you want to alter the data model. For ORM to work the data model (i.e. database tables represeted by python classes) always needs to mirror the current version of the database. This is what Alembic is used for and is analogous to "GIT".

## To install.

1. clone the repository

```
$cd TomocatDB
$pip install .
```

## Setting up your database.

You should now be able to generate the database tables detailed by your data model with alembic.

```
$alembic revision --autogenerate -m 'my first commit'
$alembic upgrade head
```

You can check the database tables using a software like DBeaver.
