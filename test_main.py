from users import create_access_token
import pytest
import pytest_asyncio
from db import engine
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from httpx import ASGITransport, AsyncClient
from main import app
from models import User, Todo, Base
from users import get_password_hash


@pytest.fixture
def test_client():
    client = TestClient(app)
    return client

@pytest.fixture
def user():
    session = Session(engine)
    user = User(
        id=1,
        username="test_user",
        email="test_user@example.com",
        password_hashed=get_password_hash("test_password"),
        is_active=True
    )
    session.add(user)
    session.commit()
    yield user
    session.query(User).delete()
    session.commit()

@pytest.fixture
def user_authorization_header(user):
    token = create_access_token(data={"sub": user.email})
    return {
        "Authorization": f"Bearer {token}"
    }

@pytest.fixture
def todo():
    session = Session(engine)
    todo = Todo(
        id=1,
        title="Test Todo",
        description="Test Description",
        completed=False,
        priority="Low"
    )
    session.add(todo)
    session.commit()
    yield todo
    session.query(Todo).delete()
    session.commit()    

@pytest.fixture
def todos():
    session = Session(engine)
    todos = [
        Todo(
            id=2,
            title="Test Todo 2",
            description="Test Description 2",
            completed=False,
            priority="Low"
        ),
        Todo(
            id=3,
            title="Test Todo 3",
            description="Test Description 3",
            completed=False,
            priority="Low"
        )
    ]
    session.add_all(todos)
    session.commit()
    yield todos
    session.query(Todo).delete()
    session.commit()

@pytest.fixture
def seed_data(user, todo, todos):
    session = Session(engine)
    yield session   



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


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://",
    ) as ac:
        yield ac




async def test_todos(client, seed_data):
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
    response = await client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    assert response.json().get("data").get("todos") == [
        {
            "id": 1,
            "title": "Test Todo",
            "description": "Test Description",
            "completed": False,
            "priority": "Low"
        },
        {
            "id": 2,
            "title": "Test Todo 2",
            "description": "Test Description 2",
            "completed": False,
            "priority": "Low"
        },
        {
            "id": 3,
            "title": "Test Todo 3",
            "description": "Test Description 3",
            "completed": False,
            "priority": "Low"
        }
    ]  


async def test_todo(client, seed_data):
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
    response = await client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    assert response.json()["data"]["todo"] == {
        "id": 1,
        "title": "Test Todo",
        "description": "Test Description",
        "completed": False,
        "priority": "Low"
    }  
    

async def test_create_todo(client,user_authorization_header,seed_data):
    query = """
        mutation {
            createTodo(
                title: "Test Todo"
                description: "Test Description"
                completed: false
                priority: "Low"
            ) {
                id
                title
                description
                completed
                priority
            }
        }
    """
    response = await client.post("/graphql", json={"query": query}, headers=user_authorization_header)
    assert response.status_code == 200
    assert response.json()["data"]["createTodo"] is not None


async def test_update_todo(client,user_authorization_header,seed_data):
    query = """
        mutation {
            updateTodo(
                todoId: 1
                title: "Updated Todo"
                description: "Updated Description"
                completed: true
                priority: "High"
            ) {
                id
                title
                description
                completed
                priority
            }
        }
    """
    response = await client.post("/graphql", json={"query": query}, headers=user_authorization_header)
    assert response.status_code == 200
    assert response.json()["data"]["updateTodo"] is not None    


async def test_delete_todo(client,user_authorization_header,seed_data):
    query = """
        mutation {
            deleteTodo(
                todoId: 1
            ) {
                id
            }
        }
    """
    response = await client.post("/graphql", json={"query": query}, headers=user_authorization_header)
    assert response.status_code == 200
    assert response.json()["data"]["deleteTodo"] is not None


async def test_get_users(client, seed_data):
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
    response = await client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    assert response.json()["data"]["getUsers"] is not None 


async def test_get_user(client, seed_data):
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
    response = await client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    assert response.json()["data"]["getUser"] == {
        "id": 1,
        "username": "test_user",
        "email": "test_user@example.com",
    }


async def test_create_user(client, seed_data):
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
    response = await client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    assert response.json()["data"]["createUser"] is not None   


async def test_update_user(client, seed_data):
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
    response = await client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    assert response.json()["data"]["updateUser"] is not None   


async def test_delete_user(client, seed_data):
    query = """
        mutation {
            deleteUser(
                userId: 1
            ) {
                id
            }
        }
    """
    response = await client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    assert response.json()["data"]["deleteUser"] is not None   


async def test_login_for_access_token(client, seed_data):
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
    response = await client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    assert response.json()["data"]["loginForAccessToken"] is not None


