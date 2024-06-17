from unittest.mock import MagicMock

import mysql.connector
import pytest

from core import settings
from webpage.utils import create_database


@pytest.fixture
def mock_db():
    return MagicMock(spec=mysql.connector.MySQLConnection)


@pytest.fixture
def mock_cursor():
    return MagicMock(spec=mysql.connector.cursor.MySQLCursor)


def test_create_database(mock_db, mock_cursor, monkeypatch):
    monkeypatch.setattr("mysql.connector.connect", MagicMock(return_value=mock_db))
    mock_db.cursor.return_value = mock_cursor

    create_database()

    mock_db.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with(f"CREATE DATABASE {settings.DB_NAME}")
