import pytest
from db import engine
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import pytest
from httpx import ASGITransport, AsyncClient
from main import app
from models import User, Todo, Base
from users import get_password_hash


@pytest.fixture
def test_client():
    client = TestClient(app)
    return client

@pytest.fixture
def seed_data():
    session = Session(engine)
    user = User(
        id=1,
        username="test_user",
        email="test_user@example.com",
        password_hashed=get_password_hash("test_password"),
        is_active=True
    )

    todo = Todo(
        id=1,
        title="Seed Todo",
        description="Seed Description",
        completed=False,
        priority="Low"
    )

    session.add(user)
    session.add(todo)
    session.commit()

    yield session   

    session.query(User).delete()
    session.query(Todo).delete()
    session.commit()

@pytest.fixture
def fake_context():
    async def fake_get_context(request):
        return {
            "request": request,
            "user": {
                "id": 1,
                "email": "test_user@example.com",
                "is_active": True,
            }
        }

    from main import graphql_app

    old_context_getter = graphql_app.context_getter
    graphql_app.context_getter = fake_get_context

    yield 

    graphql_app.context_getter = old_context_getter


# def test_todos(test_client, seed_data):
#     query = """
#         query {
#             todos {
#                 id
#                 title
#                 description
#                 completed
#                 priority
#             }
#         }
#     """
#     response = test_client.post("/graphql", json={"query": query})
#     assert response.status_code == 200
#     assert response.json().get("data").get("todos") == [
#         {
#             "id": 1,
#             "title": "Seed Todo",
#             "description": "Seed Description",
#             "completed": False,
#             "priority": "Low"
#         }
#     ]  

# def test_todo(test_client, seed_data):
#     query = """
#         query {
#             todo(
#                 todoId: 1
#             ) {
#                 id
#                 title
#                 description
#                 completed
#                 priority
#             }
#         }
#     """
#     response = test_client.post("/graphql", json={"query": query})
#     assert response.status_code == 200
#     assert response.json()["data"]["todo"] == {
#         "id": 1,
#         "title": "Seed Todo",
#         "description": "Seed Description",
#         "completed": False,
#         "priority": "Low"
#     }  
    

# def test_create_todo(test_client, seed_data, fake_context):
#     query = """
#         mutation {
#             createTodo(
#                 title: "Test Todo"
#                 description: "Test Description"
#                 completed: false
#                 priority: "Low"
#             ) {
#                 id
#                 title
#                 description
#                 completed
#                 priority
#             }
#         }
#     """
#     headers = {
#         "Authorization": "Bearer fake_token"
#     }
#     response = test_client.post("/graphql", json={"query": query}, headers=headers)
#     assert response.status_code == 200
#     assert response.json()["data"]["createTodo"] is not None

# def test_update_todo(test_client):
#     query = """
#         mutation {
#             updateTodo(
#                 todoId: 1
#                 title: "Updated Todo"
#                 description: "Updated Description"
#                 completed: true
#                 priority: "High"
#             ) {
#                 id
#                 title
#                 description
#                 completed
#                 priority
#             }
#         }
#     """
#     headers = {
#         "Authorization": "Bearer fake_token"
#     }
#     response = test_client.post("/graphql", json={"query": query}, headers=headers)
#     assert response.status_code == 200
#     assert response.json()["data"]["updateTodo"] is not None    

# def test_delete_todo(test_client):
# #     query = """
# #         mutation {
# #             deleteTodo(
# #                 todoId: 1
# #             ) {
# #                 id
# #             }
# #         }
# #     """
# #     headers = {
# #         "Authorization": "Bearer fake_token"
# #     }
# #     response = test_client.post("/graphql", json={"query": query}, headers=headers)
# #     assert response.status_code == 200
# #     assert response.json()["data"]["deleteTodo"] is not None

# def test_get_users(test_client):
#     query = """
#         query {
#             getUsers {
#                 id
#                 username
#                 email
#                 isActive
#             }
#         }
#     """
#     headers = {
#         "Authorization": "Bearer fake_token"
#     }
#     response = test_client.post("/graphql", json={"query": query}, headers=headers)
#     assert response.status_code == 200
#     assert response.json()["data"]["getUsers"] is not None 

# def test_get_user(test_client, seed_data):
#     query = """
#         query {
#             getUser(
#                 userId: 1
#             ) {
#                 id
#                 username
#                 email
#             }
#         }
#     """
#     headers = {
#         "Authorization": "Bearer fake_token"
#     }
#     response = test_client.post("/graphql", json={"query": query}, headers=headers)
#     assert response.status_code == 200
#     assert response.json()["data"]["getUser"] == {
#         "id": 1,
#         "username": "test_user",
#         "email": "test_user@example.com",
#     }

# def test_create_user(test_client, seed_data):
#     query = """
#         mutation {
#             createUser(
#                 username: "test_u"
#                 email: "test_u@example.com"
#                 password: "test_password"
#                 isActive: true
#             ) {
#                 id
#                 username
#                 email
#                 isActive
#             }
#         }
#     """
#     response = test_client.post("/graphql", json={"query": query})
#     assert response.status_code == 200
#     assert response.json()["data"]["createUser"] is not None   

# def test_update_user(test_client, seed_data):
#     query = """
#         mutation {
#             updateUser(
#                 userId: 1
#                 username: "test_user"
#                 password: "test_password"
#                 isActive: true
#             ) {
#                 id
#                 username
#                 email
#                 isActive
#             }
#         }
#     """
#     response = test_client.post("/graphql", json={"query": query})
#     assert response.status_code == 200
#     assert response.json()["data"]["updateUser"] is not None   

# def test_delete_user(test_client, seed_data):
#     query = """
#         mutation {
#             deleteUser(
#                 userId: 1
#             ) {
#                 id
#             }
#         }
#     """
#     response = test_client.post("/graphql", json={"query": query})
#     assert response.status_code == 200
#     assert response.json()["data"]["deleteUser"] is not None   

# def test_login_for_access_token(test_client, seed_data):
#     query = """
#         mutation {
#             loginForAccessToken(
#                 email: "test_user@example.com"
#                 password: "test_password"
#             ) {
#                 accessToken
#                 tokenType
#             }
#         }
#     """
#     response = test_client.post("/graphql", json={"query": query})
#     assert response.status_code == 200
#     assert response.json()["data"]["loginForAccessToken"] is not None


@pytest.mark.anyio
async def test_todos(seed_data):
    query = """
        query {
            todos {
                id
                title
                description
                completed
                priority
            }
        }
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post("/graphql", json={"query": query})
    assert response.status_code == 200
    assert response.json().get("data").get("todos") == [
        {
            "id": 1,
            "title": "Seed Todo",
            "description": "Seed Description",
            "completed": False,
            "priority": "Low"
        }
    ]  

@pytest.mark.anyio
async def test_todo(seed_data):
    query = """
        query {
            todo(
                todoId: 1
            ) {
                id
                title
                description
                completed
                priority
            }
        }
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post("/graphql", json={"query": query})
    assert response.status_code == 200
    assert response.json()["data"]["todo"] == {
        "id": 1,
        "title": "Seed Todo",
        "description": "Seed Description",
        "completed": False,
        "priority": "Low"
    }  
    

# def test_create_todo(test_client, seed_data, fake_context):
#     query = """
#         mutation {
#             createTodo(
#                 title: "Test Todo"
#                 description: "Test Description"
#                 completed: false
#                 priority: "Low"
#             ) {
#                 id
#                 title
#                 description
#                 completed
#                 priority
#             }
#         }
#     """
#     headers = {
#         "Authorization": "Bearer fake_token"
#     }
#     response = test_client.post("/graphql", json={"query": query}, headers=headers)
#     assert response.status_code == 200
#     assert response.json()["data"]["createTodo"] is not None

# def test_update_todo(test_client):
#     query = """
#         mutation {
#             updateTodo(
#                 todoId: 1
#                 title: "Updated Todo"
#                 description: "Updated Description"
#                 completed: true
#                 priority: "High"
#             ) {
#                 id
#                 title
#                 description
#                 completed
#                 priority
#             }
#         }
#     """
#     headers = {
#         "Authorization": "Bearer fake_token"
#     }
#     response = test_client.post("/graphql", json={"query": query}, headers=headers)
#     assert response.status_code == 200
#     assert response.json()["data"]["updateTodo"] is not None    

# def test_delete_todo(test_client):
#     query = """
#         mutation {
#             deleteTodo(
#                 todoId: 1
#             ) {
#                 id
#             }
#         }
#     """
#     headers = {
#         "Authorization": "Bearer fake_token"
#     }
#     response = test_client.post("/graphql", json={"query": query}, headers=headers)
#     assert response.status_code == 200
#     assert response.json()["data"]["deleteTodo"] is not None

@pytest.mark.aanyio
async def test_get_users(seed_data):
    query = """
        query {
            getUsers {
                id
                username
                email
                isActive
            }
        }
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post("/graphql", json={"query": query})
    assert response.status_code == 200
    assert response.json()["data"]["getUsers"] is not None 

@pytest.mark.aanyio
async def test_get_user( seed_data):
    query = """
        query {
            getUser(
                userId: 1
            ) {
                id
                username
                email
            }
        }
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post("/graphql", json={"query": query})
    assert response.status_code == 200
    assert response.json()["data"]["getUser"] == {
        "id": 1,
        "username": "test_user",
        "email": "test_user@example.com",
    }

@pytest.mark.aanyio
async def test_create_user( seed_data):
    query = """
        mutation {
            createUser(
                username: "test_u"
                email: "test_u@example.com"
                password: "test_password"
                isActive: true
            ) {
                id
                username
                email
                isActive
            }
        }
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post("/graphql", json={"query": query})
    assert response.status_code == 200
    assert response.json()["data"]["createUser"] is not None   

@pytest.mark.aanyio
async def test_update_user( seed_data):
    query = """
        mutation {
            updateUser(
                userId: 1
                username: "test_user"
                password: "test_password"
                isActive: true
            ) {
                id
                username
                email
                isActive
            }
        }
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post("/graphql", json={"query": query})
    assert response.status_code == 200
    assert response.json()["data"]["updateUser"] is not None   

@pytest.mark.aanyio
async def test_delete_user( seed_data):
    query = """
        mutation {
            deleteUser(
                userId: 1
            ) {
                id
            }
        }
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post("/graphql", json={"query": query})
    assert response.status_code == 200
    assert response.json()["data"]["deleteUser"] is not None   

@pytest.mark.aanyio
async def test_login_for_access_token( seed_data):
    query = """
        mutation {
            loginForAccessToken(
                email: "test_user@example.com"
                password: "test_password"
            ) {
                accessToken
                tokenType
            }
        }
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post("/graphql", json={"query": query})
    assert response.status_code == 200
    assert response.json()["data"]["loginForAccessToken"] is not None


