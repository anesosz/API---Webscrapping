import uvicorn

from src.app import get_application
from fastapi.responses import RedirectResponse

app = get_application()


@app.get("/")
def root():
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
