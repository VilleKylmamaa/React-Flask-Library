import click
from flask.cli import with_appcontext
from api import db


class Book(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=True)
    author = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=True)
    
    @staticmethod
    def get_schema():
        schema = {
            "type": "object",
            "required": ["title"],
        }
        props = schema["properties"] = {}
        props["book_id"] = {
            "description": "Identifier of the book",
            "type": "integer"
        }
        props["title"] = {
            "description": "Title of the book",
            "type": "string"
        }
        props["author"] = {
            "description": "Author of the book",
            "type": "string"
        }
        props["description"] = {
            "description": "Description of the book",
            "type": "string"
        }
        return schema



#
# CLI commands for generating test data, deleting tables and creating tables
#

# Inserts books to the database
@click.command("testgen")
@with_appcontext
def insert_initial_data(*args, **kwargs):
    db.session.add(Book(
        title="Harry Potter and the Philosopher's Stone",
        author="J. K. Rowling",
        description="Young wizard with a bad-ass scar fights against a bad guy with a weird nose.",
        ))
    db.session.add(Book(
        title="Lord of the Rings",
        author="J. R. R. Tolkien",
        description="Young hobbit gets a cool ring but he has to throw it in a volcano because there's a bad guy who is actually just a tower.",
        ))
    db.session.add(Book(
        title="The Lion, the Witch and the Wardrobe",
        author="C. S. Lewis",
        description="Seven kids go inside their wardrobe to talk to animals and fight against an evil witch.",
        ))

    db.session.commit()


# Deletes the database
@click.command("delete-db")
@with_appcontext
def delete_db_command():
    db.drop_all()

# Initializes the database
@click.command("init-db")
@with_appcontext
def init_db_command():
    db.create_all()
