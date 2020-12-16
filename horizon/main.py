from fastapi import FastAPI

from horizon.server.api import router as proxy_router
from horizon.enforcer.api import router as enforcer_router
from horizon.policy.api import router as policy_router
from horizon.server.middleware import configure_middleware
from horizon.logger import logger
from horizon.policy.updater import policy_updater
from horizon.enforcer.runner import opa_runner

app = FastAPI(title="Horizon Sidecar", version="0.1.0")
configure_middleware(app)

# include the api routes
app.include_router(proxy_router)
app.include_router(enforcer_router)
app.include_router(policy_router)

@app.get("/healthcheck", include_in_schema=False)
@app.get("/", include_in_schema=False)
def healthcheck():
    return {"status": "ok"}

@app.on_event("startup")
async def startup_event():
    policy_updater.start()
    opa_runner.start()

@app.on_event("shutdown")
async def shutdown_event():
    opa_runner.stop()
    policy_updater.stop()
