import uvicorn
import config

if __name__ == "__main__":
    uvicorn.run(
        host="0.0.0.0",
        app="core.server:app",
        reload=False,
        port=3011,
        workers=1,
    )
