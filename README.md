# Data engineering task

<img
  alt="Tests"
  src="https://github.com/mart-mihkel/deng-task/actions/workflows/pytest.yml/badge.svg"
/>

## Run

To start the production server simply run:
```bash
docker compose up
```
This will serve iris data on [endpoints](#endpoints).

## Dev

The only required dependencies are docker and [astral-uv](https://docs.astral.sh/uv/),
latter of which can be installed with `curl -LsSf https://astral.sh/uv/install.sh | sh`.

To install project dependencies you can run `uv sync` or `make setup`.

To run the development server you need to have running a postgres database:
```bash
docker compose -f compose.dev.yml up
```

After which you can initialize the database and start the flask server with:
```bash
uv run flask --app flaskr --debug init-db
uv run flask --app flaskr --debug run
```

This will serve iris data on `http://localhost:5000/iris/`

### Endpoints

```bash
# get the whole dataset in json
curl http://localhost:8080/iris/
```

```bash
# get aggregated means of flower attributes grouped by species
curl http://localhost:8080/iris/mean
```

```bash
# upload new observations
curl -X POST http://localhost:8080/iris/ \
  -H "Content-Type: application/json" \
  -d '[
    {
      "petal_length": 14,
      "petal_width": 0.2,
      "sepal_length": 5.1,
      "sepal_width": 3.5,
      "species": "setosa"
    }
  ]'
```

### Commands

Run `make help` for a rundown of development commands including tests and formatting.
