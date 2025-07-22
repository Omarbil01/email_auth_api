from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from . import models
from .database import engine
from .api import router as api_router


models.Base.metadata.create_all(bind=engine)


limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="User Login API with OTP")


app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    if request.url.path == "/api/request-otp":
        try:
            await limiter.check(request)
        except RateLimitExceeded as e:
            return _rate_limit_exceeded_handler(request, e)
    response = await call_next(request)
    return response

r
app.include_router(api_router, prefix="/api", tags=["authentication"])

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the OTP Authentication API"}