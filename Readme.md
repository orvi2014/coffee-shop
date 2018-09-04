# Coffeeshop

A RESTful backend for a Coffee Shop application. This backend will contain API endpoints for user registration, login, place order, update order and cancel order.

## Getting Started

You need some Prerequisites First to run this application

### Prerequisites

```
pip
Python3.6+
VirtualEnv
Django1.11
DRF
```

### Installing

## From Local Machine

First, we will create a virturalenv in our local machine. Name it `venv`

```
Virtualenv venv
```
Next, cd in it : `cd venv`
Activate your venv.

For Linux `source activate venv`
For Windows `venv\Scripts\activate`

Clone this app using `git clone url coffeeshop`
go to the directory `cd coffeshop`
Run following command for installing dependencies `pip install -r requirements.txt`
Migrate the database

```
python manage.py makemigrations
python mange.py migrate
```

Now run the application `python manage.py runserver`

## From Docker

You can use it from docker too.

You have to install docker in your local machine first.

First clone the repo and cd it.

`git clone url coffeeshop && cd coffeshop`

Then run `docker-compose build`
Now make it up by running `docker-compose up`





## Running the tests

For running testcase run: `python manage.py test`

## Deployment

You can check the live version here : http://coffeeshopbd.herokuapp.com

## API Documentation

Check the link
