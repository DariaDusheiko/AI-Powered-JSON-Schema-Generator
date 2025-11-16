import uvicorn
from backend.src.config import settings

def main():

    uvicorn.run(
        "backend.src.presentation.api.main:app",
        host=settings.app.host,
        port=settings.app.port,
        reload=settings.app.reload,
    )

if __name__ == "__main__":
    main()