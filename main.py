from fastapi import FastAPI
from users import user_router
from strawberry.fastapi import GraphQLRouter
from graphql_schema import schema, get_context


graphql_app = GraphQLRouter(schema, context_getter=get_context)


app = FastAPI()
app.include_router(router=user_router)
app.include_router(graphql_app, prefix="/graphql")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)