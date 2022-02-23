import os
import pytest
import tempfile
from sqlalchemy.exc import IntegrityError
from api import create_app, db
from api.models import *

# Based on http://flask.pocoo.org/docs/1.0/testing/
@pytest.fixture
def app():
    db_fd, db_fname = tempfile.mkstemp()
    config = {
        "SQLALCHEMY_DATABASE_URI": "sqlite:///" + db_fname,
        "TESTING": True
    }
    
    app = create_app(config)

    with app.app_context():
        db.create_all()

    yield app
    
    os.close(db_fd)
    os.unlink(db_fname)

    
def _get_book():
    return Book(
        book_id=1,
        title="Harry Potter and the Philosopher's Stone",
        author="J. K. Rowling",
        description="Young wizard with a bad-ass scar fights against a bad guy with a weird nose."
    )

def test_create_instances(app):
    """
    Tests that we can create one instance of each model and save them to the
    database using valid values for all columns.
    """
    
    with app.app_context():
        db.session.add(_get_book())
        db.session.commit()
        assert Book.query.count() == 1


def test_book_columns(app):
    """
    Tests book columns' non-nullable and unique restrictions
    """
    
    with app.app_context():
        # Tests that book_id is unique
        book_1 = _get_book()
        book_2 = _get_book()
        db.session.add(book_1)
        db.session.add(book_2)
        with pytest.raises(IntegrityError):
            db.session.commit()
        
        db.session.rollback()

        # Tests that nullable columns are nullable
        book = _get_book()
        book.title = None
        book.author = None
        book.description = None
        db.session.add(book)  
        assert Book.query.first() == book

def test_cli_init(app):
    """
    Tests that init_db_command exists
    """
    runner = app.test_cli_runner()
    result = runner.invoke(init_db_command)
    assert result

def test_cli_delete(app):
    """
    Tests that delete_db_command exists
    """
    runner = app.test_cli_runner()
    result = runner.invoke(delete_db_command)
    assert result

def test_cli_testgen(app):
    """
    Tests that insert_initial_data exists
    """
    runner = app.test_cli_runner()
    result = runner.invoke(insert_initial_data)
    assert result