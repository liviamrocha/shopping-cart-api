from fastapi import FastAPI
from shopping_cart.routers import api_router
from shopping_cart.core.settings import get_environment_variables
from shopping_cart.server.database import connect_db, close_conn_db

env = get_environment_variables()
app = FastAPI(
    title=env.APP_NAME,
    version=1.0
)

# Add conection database
app.add_event_handler('startup', connect_db)
app.add_event_handler('shutdown', close_conn_db)

# Add API routes
app.include_router(api_router)