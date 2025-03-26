import os
from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine


def create_database(
    database_url: str | None = None,
    database_path: str | Path | None = None,
    logging: bool = False,
):
    """Create a leaflock database from EITHER a url or path.

    :param database_url: SQLAlchemy url of a database, defaults to None
    :type database_url: str | None, optional
    :param database_path: File path of a database, will create if it does not exist, defaults to None.
    Takes precedence over `database_url`
    :param logging: To log to console - can mess with other logging setups, set to False.
    :type logging: bool
    :type database_path: str | Path | None, optional
    """
    upgrade_database(
        database_path=database_path,
        database_url=database_url,
        logging=logging,
    )


def upgrade_database(
    database_url: str | None = None,
    database_path: str | Path | None = None,
    alembic_cfg_path: str | Path | None = None,
    alembic_migration_path: str | Path | None = None,
    alembic_revision: str = "head",
    logging: bool = False,
):
    """Upgrades a leaflock database to the newest revision by default.
    Requires env var "LEAFLOCK_DB_URL", or `database_url` or `database_path`.

    :param database_url: SQLAlchemy database url.
    :type database_url: str | None
    :param database_path: SQLite database path, takes precedence over `database_url`.
    :type database_path: str | Path | None
    :param alembic_cfg_path: Path to alternative alembic config.
    :type alembic_cfg_path: str | None
    :param alembic_revision: Revision to upgrade to, defaults to "head"
    :type alembic_revision: str
    :param logging: To log to console - can mess with other logging setups, set to False.
    :type logging: bool
    :raises ValueError: If neither database url or path is provided, and environment var "LEAFLOCK_DB_URL" is unset.
    """
    if database_path is not None:
        database_url = f"sqlite:///{database_path}"

    if database_url is None:
        database_url = os.environ.get("LEAFLOCK_DB_URL", None)

        if database_url is None:
            raise ValueError("Missing environment variable LEAFLOCK_DB_URL!")

    if alembic_cfg_path is None:
        alembic_cfg_path = os.environ.get("LEAFLOCK_ALEMBIC_CONFIG_PATH", None)

        if alembic_cfg_path is None:
            alembic_cfg_path = (Path(__file__).parent / "alembic/alembic.ini").resolve()

            if alembic_cfg_path.exists() and alembic_cfg_path.is_file():
                alembic_cfg_path = str(alembic_cfg_path)
            else:
                raise ValueError("Could not identify an alembic.ini file!")

    if alembic_migration_path is None:
        alembic_migration_path = os.environ.get("LEAFLOCK_ALEMBIC_MIGRATION_PATH", None)

        if alembic_migration_path is None:
            alembic_migration_path = (Path(__file__).parent / "alembic").resolve()

            if alembic_migration_path.exists() and alembic_migration_path.is_dir():
                alembic_migration_path = str(alembic_migration_path)
            else:
                raise ValueError("Could not identify an alembic migration directory!")

    alembic_cfg = Config(file_=alembic_cfg_path)

    engine = create_engine(database_url)

    with engine.begin() as connection:
        alembic_cfg.attributes["connection"] = connection
        alembic_cfg.attributes["logging"] = logging
        alembic_cfg.set_main_option("script_location", str(alembic_migration_path))
        command.upgrade(alembic_cfg, alembic_revision)
