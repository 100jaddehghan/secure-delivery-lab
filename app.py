from fastapi import FastAPI

app = FastAPI(title="Secure Delivery Lab")


@app.get("/healthz")
def health() -> dict[str, str]:
    return {"status": "ok"}
