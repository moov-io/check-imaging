import os
import subprocess
import json
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.v1.image_controller import router as image_router
from core.config import TEMP_DIR_PATH


@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs(TEMP_DIR_PATH, mode=777, exist_ok=True)

    # Startup event: Start Ollama server
    print("Starting Ollama server...")
    # You might need to adjust the command based on your Ollama installation
    ollama_process = subprocess.Popen(["ollama", "serve"])
    print("Ollama server started.")

    yield
    print("Stopping Ollama server...")
    ollama_process.terminate() # or ollama_process.kill() if terminate isn't enough
    ollama_process.wait() # Wait for the process to terminate
    print("Ollama server stopped.")


# Create the FastAPI app instance
app = FastAPI(lifespan=lifespan)

app.include_router(image_router)

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    if isinstance(exc.detail, str):
        return JSONResponse(status_code=exc.status_code, content={ 'message': exc.detail })
    return JSONResponse(status_code=exc.status_code, content=exc.detail)

@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    return JSONResponse(status_code=500, content={"message": "Internal Server Error"})

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.get('/health', tags=["Other"])
def health():
    '''
        Check API health status.
    '''
    return {"status": "OK"}


def custom_openapi():
    '''
        Define custom openapi.
    '''
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title='Moov Check API',
        version='1.0.0',
        description="This is the API document for moov check.",
        servers=[{'url': 'http://localhost:8000' }],
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://moov.io/favicon.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

def generate_openapi():
    with open("openapi.json", "w") as f:
        jsonContent = app.openapi()

        path_keys = jsonContent['paths'].keys()
        for path_key in path_keys:
            path = jsonContent['paths'][path_key]
            method_keys = path.keys()
            for method_key in method_keys:
                if 'parameters' in path[method_key]:
                    del jsonContent['paths'][path_key][method_key]['parameters']
        json.dump(jsonContent, f, indent=2)

if __name__ == "__main__":
    generate_openapi()
