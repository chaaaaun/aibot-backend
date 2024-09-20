# Setting Up

1. Look through `docker-compose.yml` in the project root and change the database configuration as you see fit
2. Run `docker-compose up -d` to create and set up the MongoDB Docker container
3. Through your preferred project workflow, export the `DB_URI` environment variable with the correct MongoDB connection string for your configuration (e.g. `mongodb://root:admin@localhost:27017`)
4. The `DB_NAME` environment variable is up to you to decide
5. The `API_KEY` environment variable should be a working OpenAPI API key
5. Run in development mode with `fastapi dev src/main.py`

# Testing

1. This project uses `pytest`, check the `test` folder for test files, to modify or add as you see fit
2. Once done, run all tests with `pytest`

# Building for production

1. Ensure environment variables defined in `docker-compose.yml` are up to date
2. Run with `docker-compose up -d` and the server will be available on port 8000 by default