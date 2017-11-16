# You Talkin' To Me?

An AI chatbot *Arnold Schwarzenatter* trained using movie quotes

[![Build Status](https://travis-ci.org/jhole89/you-talkin-to-me.svg?branch=master)](https://travis-ci.org/jhole89/you-talkin-to-me)
[![Coverage Status](https://coveralls.io/repos/github/jhole89/you-talkin-to-me/badge.svg?branch=master)](https://coveralls.io/github/jhole89/you-talkin-to-me?branch=master)

## Getting Started

### Prerequisites

* [Python 3.6+](https://www.python.org/downloads/)

### Installation

1. Install Python 3.6 on your Operating System as per the Python Docs.
Continuum's Anaconda distribution is recommended.

2. Checkout the repo:
`git clone https://github.com/jhole89/you-talkin-to-me.git`

3. Setup the project dependencies:
```
$ cd you-talking-to-me
$ export PYTHONPATH=$PYTHONPATH:$(pwd)
$ pip install -r requirements.txt
```

### Execution

1. From the project root run the webserver, it will be available at `localhost:5000`
(*Note: if you receive a python module not found error, ensure your python
path is set correctly*):
```
$ python app/run.py
List Trainer: [####################] 100%
List Trainer: [####################] 100%
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

2. By default the chatbot only knows a couple of responses pre-training,
e.g. `GET /question/who%20are%you` or `http://127.0.0.1:5000/question/whow%20are%20you`
should respond with the raw HTML 'Arnold Schwartzenatter'. We need to train the chatbot
on the Cornell Movie Corpus provided. This is done by sending a POST request to
`/admin/retrain/` with a json object of `{"conversation_length": <int>, "stop_short": <int>}`.
Due to limitations on the default database (sqlite) used to store the statement and responses,
it is recommended to use default values of `{"conversation_length": 5, "stop_short": 10000}`.
Conversation_length values below this will result in the chatbot learning many short and simple
conversations, while stop_short values above this will cause the chatbot to learn too many
conversations for a timely and effective lookup when later querying the sqlite database for a response.
**WARNING:** Training can take a few minutes, but progress can be monitored from the terminal.
If trained correctly we would receive a respond of
`Retrained with parameters: {'conversation_length': 5, 'stop_short': 1000}`.

3. With the chatbot now trained we can send GET requests to /question/ to receive a trained
response, for example:
 * [QUESTION:](http://127.0.0.1:5000/question/what%20do%20you%20want)
  What do you want? --- RESPONSE: came by to check on you.
 * [QUESTION:](http://127.0.0.1:5000/question/how%20are%20you%20feeling%20today)
   How are you feeling today? --- RESPONSE: confused. i'm not sure what to do now. i'm not sure what he wants for me.
 * [QUESTION:](http://127.0.0.1:5000/question/where%20are%20we%20going)
   Where are we going? --- RESPONSE: if you ask me, we're heading straight for those mountains.

4. Repeated training can be done but is discouraged due to the increased lookup times for GET requests.
Each time we train we do take a random sample so the Examples above are unlikely to result in the same
answers in user implementations.

## Test Coverage and Coding Style

This project uses [Travis-CI](https://travis-ci.org/jhole89/you-talkin-to-me) for our CI/CD
and runs test coverage (pytest) and style checks (pep8) against every commit and against the
nightly CPython build to ensure we are always aligned with the latest CPython dev builds.
Build status is shown at the top of this README.

## Architecture and Design

This project was designed to be a simple PoC implementation of a chatbot trained on movie quotes.
As such it did not make sense to use more complex methods such as Recurrent Neural Networks for an
initial PoC, however that is likely to provide a better model in a larger production setting.
Instead we have made use of the Chatterbot API which performs the Levenshtein distance between all
strings loaded into the database (hence the increasing delay for GET requests with a larger training
set). With the current architecture there is the issue of limitations of the database.  This defaults
to a simple sqlite instance which can safely be deleted between runs of the application (retrain will
then be required). There are some optimisations we can make to the sqlite database such as indexes
on the primary keys, however this has not currently been implemented as the database is not distributed
with the repository.  It could also prove beneficial to move the database from sqlite to mongoDB instead,
however this requires the user to have an instance of mongoDB already running and as such has not been
implemented at this stage.

## Acknowledgments

* *Arnold Schwarzenatter* is trained on the [Cornell Movie-Quotes Corpus v1.0](https://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html#lexicon)
by Cristian Danescu-Niculescu-Mizil, Justin Cheng, Jon Kleinberg and Lillian Lee -
*You had me at Hello: How phrasing affects memorability (ACL 2012)*