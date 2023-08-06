# sinai

This is a library for developing monitoring applications that encourages rapid development and clean, pragmatic design.

What your application monitors is up to you. It could be online data sources, the state of a business application, data integrity, anything you want.

For a high-level overview, please read [Creating a monitoring application with sinai](INTRO.md)

## Usage

To develop a monitoring application with sinai, you install it and import it like any other Python library. 

See the [interactive tutorials](./docs/tutorial/README.md) for how to use it.

See [a simple usage example](example.py).

### Install

There are no required dependencies, but optional dependencies are required for the relevant features:

* `requests` to use API sources and stores, and the Slack store
* `pymongo` to use MongoDB sources and stores
* `boto3` to use the CloudWatch store

To install via pip:

```bash
pip install sinai
```

To install via setup tools:

```bash
$ git clone git@github.com:SinAI-monitoring/sinai.git
$ cd sinai
$ python setup.py install
```

## Contributing

To develop sinai itself, use the following commands to create a development environment. These assume you have [pipenv](https://pipenv.pypa.io/en/latest/) installed.

```bash
$ git clone git@github.com:SinAI-monitoring/sinai.git
$ cd sinai
$ pipenv install --dev
$ pipenv shell
$ pre-commit install
```

Check the pre-commit hooks are working with:

```bash
$ pre-commit run -a
```

Run the unit tests with:

```bash
$ pytest
```
