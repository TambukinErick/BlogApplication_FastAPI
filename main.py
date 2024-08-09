from fastapi import FastAPI

from .models import comment_model, interaction_model, post_model, user_model

from .database import engine
from .routers import comment_router, interaction_router, post_router, user_router

comment_model.Base.metadata.create_all(bind=engine)
interaction_model.Base.metadata.create_all(bind=engine)
post_model.Base.metadata.create_all(bind=engine)
user_model.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Blog App"
)
post_router.router.include_router(comment_router.router)
post_router.router.include_router(interaction_router.router)
# app.include_router(comment_router.router)
# app.include_router(interaction_router.router)
app.include_router(post_router.router)
app.include_router(user_router.router)

@app.get("/Home/")
async def root():
    return {"message": "Hello World"}










