import uvicorn

from src.app import get_application
from fastapi.responses import RedirectResponse

app = get_application()


@app.get("/")
def root():
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    uvicorn.run("main:app", debug=True, reload=True, port=8080)
