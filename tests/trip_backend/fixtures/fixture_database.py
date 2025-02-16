import os
import subprocess

import pytest
import sqlalchemy as sa
from app.core.config import settings
from app.core.database import async_session_maker
from dotenv import load_dotenv


SQL_DUMP_PATH = "../tests/trip_backend/fixtures/fixture_data_test_db.sql"
DB_USER = os.getenv("DB_USER")


@pytest.fixture(scope="session", autouse=True)
async def prepare_database(request):
    """Runs once per test session to reset the database."""

    assert settings.MODE == "TEST"

    reuse_db = request.config.getoption("--reuse-db", False)
    if not reuse_db:
        print("Deleting and recreating the database.")
        async with async_session_maker() as session:
            # delete all existings tables
            drop_all_tables_sql = """
            DO $$ DECLARE
                r RECORD;
            BEGIN
                -- Loop through all table names in the current schema, excluding 'spatial_' prefixed tables
                FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public' AND tablename NOT LIKE 'spatial_%') LOOP
                    EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
                END LOOP;
            END $$;
            """
            await session.execute(sa.text(drop_all_tables_sql))

            # load django dump
            with open(SQL_DUMP_PATH, "r") as file:
                sql_statements = file.read().replace("DB_USER", DB_USER).split(";")
                for statement in sql_statements:
                    clean_statement = statement.strip()
                    if clean_statement:
                        try:
                            await session.execute(sa.text(clean_statement))
                        except Exception as e:
                            print(f"Error executing statement: {clean_statement}")
                            raise e
            await session.commit()

        # make fast-api migrations
        subprocess.run(["alembic", "upgrade", "head"], check=False)
    yield


@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session
