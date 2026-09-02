from fastapi import FastAPI

app = FastAPI(title="Cinema Booking API")


@app.get("/health")
def health_check():
    return {"status": "ok"}


# Роутеры будут подключаться сюда по мере готовности, например:
# from app.routers import auth, showtimes, bookings
# app.include_router(auth.router)
