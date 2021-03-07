# tasks_api

### Setup

- Make sure you have [`docker`](https://www.docker.com/get-started) and [`docker-compose`](https://docs.docker.com/compose/install/) installed
- from within the project run `docker-compose up` and wait for a while, then checkout [`http://0.0.0.0:8000`](http://0.0.0.0:8000)

### Usage

I've included a few useful `make` commands:

---

| Command                           | Description                                              |
| --------------------------------- | -------------------------------------------------------- |
| `make lint`                       | checks if the code adheres to `black` code style         |
| `make format`                     | reformats code that doesn't adhere to `black` code style |
| `make test`                       | runs the test suite, with coverage report                |
| `make manage x='createsuperuser'` | passes `x` content to django's `./manage.py`             |
