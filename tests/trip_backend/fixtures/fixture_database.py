import pytest
import sqlalchemy as sa
from app.core.config import settings
from app.core.database import async_session_maker


@pytest.fixture(scope="session", autouse=True)
async def prepare_database(request):
    assert settings.MODE == "TEST"

    reuse_db = request.config.getoption("--reuse-db", False)
    sql_dump_file = "../tests/trip_backend/fixtures/fixture_data_test_db.sql"

    if not reuse_db:
        print("Deleting and recreating the database.")
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

        async with async_session_maker() as session:
            await session.execute(sa.text(drop_all_tables_sql))
            with open(sql_dump_file, "r") as file:
                sql_statements = file.read().split(";")
                for statement in sql_statements:
                    clean_statement = statement.strip()
                    if clean_statement:
                        try:
                            await session.execute(sa.text(clean_statement))
                        except Exception as e:
                            print(f"Error executing statement: {clean_statement}")
                            raise e
            await session.commit()
    yield


@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session
