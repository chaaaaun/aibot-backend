# Setting Up

1. Look through `docker-compose.yml` in the project root and change the database configuration as you see fit
2. Run `docker-compose up -d` to create and set up the MongoDB Docker container
3. Through your preferred project workflow, export the `DB_URI` environment variable with the correct MongoDB connection string for your configuration (e.g. `mongodb://root:admin@localhost:27017/admin`)
4. Run in development mode with `fastapi dev main.py` in the `src` directory