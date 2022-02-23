import json
import os
import pytest
import tempfile
from jsonschema import validate

from api import create_app, db
from api.models import Book


# Based on http://flask.pocoo.org/docs/1.0/testing/
@pytest.fixture
def client():
    db_fd, db_fname = tempfile.mkstemp()
    config = {
        "SQLALCHEMY_DATABASE_URI": "sqlite:///" + db_fname,
        "TESTING": True
    }
    
    app = create_app(config)
    
    with app.app_context():
        db.create_all()
        _populate_db()
        
    yield app.test_client()
    
    db.session.remove()
    os.close(db_fd)
    os.unlink(db_fname)


def _populate_db():
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


def _get_book_json():
    """
    Creates a valid book JSON object to be used for PUT and POST tests.
    """
    
    return {
            "book_id": 4,
            "title": "Harry Potter and the Philosopher's Stone",
            "author": "J. K. Rowling",
            "description": "Young wizard with a bad-ass scar fights against a bad guy with a weird nose."
            }

def _check_control_get_method(ctrl, client, obj):
    """
    Checks a GET type control from a JSON object be it root document or an item
    in a collection. Also checks that the URL of the control can be accessed.
    """
    
    href = obj["@controls"][ctrl]["href"]
    resp = client.get(href)
    assert resp.status_code == 200
    
def _check_control_delete_method(ctrl, client, obj):
    """
    Checks a DELETE type control from a JSON object be it root document or an
    item in a collection. Checks the contrl's method in addition to its "href".
    Also checks that using the control results in the correct status code of 204.
    """
    
    href = obj["@controls"][ctrl]["href"]
    method = obj["@controls"][ctrl]["method"].lower()
    assert method == "delete"
    resp = client.delete(href)
    assert resp.status_code == 204
    
def _check_control_put_method(ctrl, client, obj):
    """
    Checks a PUT type control from a JSON object be it root document or an item
    in a collection. In addition to checking the "href" attribute, also checks
    that method, encoding and schema can be found from the control. Also
    validates a valid resource against the schema of the control to ensure that
    they match. Finally checks that using the control results in the correct
    status code of 204.
    """
    
    ctrl_obj = obj["@controls"][ctrl]
    href = ctrl_obj["href"]
    method = ctrl_obj["method"].lower()
    encoding = ctrl_obj["encoding"].lower()
    schema = ctrl_obj["schema"]
    assert method == "put"
    assert encoding == "json"
    
    body = _get_book_json()
    body["book_id"] = obj["book_id"]
    validate(body, schema)
    resp = client.put(href, json=body)
    assert resp.status_code == 204
    
def _check_control_post_method(ctrl, client, obj):
    """
    Checks a POST type control from a JSON object be it root document or an item
    in a collection. In addition to checking the "href" attribute, also checks
    that method, encoding and schema can be found from the control. Also
    validates a valid resource against the schema of the control to ensure that
    they match. Finally checks that using the control results in the correct
    status code of 201.
    """
    
    ctrl_obj = obj["@controls"][ctrl]
    href = ctrl_obj["href"]
    method = ctrl_obj["method"].lower()
    encoding = ctrl_obj["encoding"].lower()
    schema = ctrl_obj["schema"]
    assert method == "post"
    assert encoding == "json"
    
    body = _get_book_json()
    validate(body, schema)
    resp = client.post(href, json=body)
    assert resp.status_code == 201



class TestApiEntry(object):
    
    RESOURCE_URL = "/api/"

    # test that API entry point exists
    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200


class TestBookCollection(object):
    
    RESOURCE_URL = "/api/books/"

    # test GET method and that all methods exist
    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        
        body = json.loads(resp.data)
        _check_control_post_method("library:add-book", client, body)
        assert len(body["items"]) == 3
        
        for item in body["items"]:
            _check_control_get_method("self", client, item)

    # test POST method
    def test_post(self, client):
        valid = _get_book_json()
        
        # test with valid and see that it exists afterward
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 201
        
        # test location header
        assert resp.headers["Location"].endswith(self.RESOURCE_URL + "4/")
        resp = client.get(resp.headers["Location"])
        assert resp.status_code == 200
        
        # test with wrong content type
        resp = client.post(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415
        
        # test with an invalid type (title should be a string)
        valid["title"] = []
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

   
class TestBookItem(object):
    
    RESOURCE_URL = "/api/books/1/"
    INVALID_URL = "/api/books/999/"
    
    # test GET method and that all methods exist
    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        _check_control_get_method("collection", client, body)
        _check_control_put_method("edit", client, body)
        _check_control_delete_method("library:delete", client, body)

        # test get with invalid url
        resp = client.get(self.INVALID_URL)
        assert resp.status_code == 404

    # test PUT method
    def test_put(self, client):
        valid = _get_book_json()
        
        # test with valid
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 204
        
        # test with wrong content type
        resp = client.put(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415
        
        # test with an invalid URL
        resp = client.put(self.INVALID_URL, json=valid)
        assert resp.status_code == 404
        
        # test with an invalid type (title should be a string)
        valid["title"] = []
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400
        
        
    # test DELETE method
    def test_delete(self, client):
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 204
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 404
        resp = client.delete(self.INVALID_URL)
        assert resp.status_code == 404

