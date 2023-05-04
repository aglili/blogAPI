from fastapi.testclient import TestClient
from main import app
from datetime import datetime

client = TestClient(app=app)

def test_create_post():
    data = {
        "title": "How To Create A RESTFUL API",
        "content": "You First Learn A Framework",
        "created_at": datetime.utcnow().isoformat()
    }

    response = client.post("/blog",json=data)

    assert response.status_code == 200
    print(response.json())
    assert response.json()["title"] == "How To Create A RESTFUL API"
    assert response.json()["content"] == "You First Learn A Framework"


def test_get_posts():
    response = client.get('/posts/')

    assert response.status_code == 200

    assert isinstance(response.json()["posts"],list)

    assert len(response.json()["posts"]) == 5
