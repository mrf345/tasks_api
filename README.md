# tasks_api [![status](https://github.com/mrf345/tasks_api/workflows/CI/badge.svg)](https://github.com/mrf345/tasks_api/actions/workflows/main.yml) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

### Setup

- Clone or [download](https://github.com/mrf345/tasks_api/archive/master.zip) this repository
- Make sure you have [`docker`](https://www.docker.com/get-started) and [`docker-compose`](https://docs.docker.com/compose/install/) installed
- From within the project directory run `docker-compose up` and wait for a while, then checkout [`http://0.0.0.0:8000`](http://0.0.0.0:8000)

### Usage

I've included a few useful `make` commands:

---

| Command                           | Description                                              |
| --------------------------------- | -------------------------------------------------------- |
| `make lint`                       | checks if the code adheres to `black` code style         |
| `make format`                     | reformats code that doesn't adhere to `black` code style |
| `make test`                       | runs the test suite, with coverage report                |
| `make manage x='createsuperuser'` | passes `x` content to django's `./manage.py`             |
