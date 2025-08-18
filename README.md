# Check Imaging API

Get information from your check image.

## Installation (Docker)

### 1. Build the Image

From the project root (where your `Dockerfile` lives):

```bash
docker build -t check-imaging:latest .
```

> **Note on Dependencies:**
>
> - If your processing pipeline needs ImageMagick 7+ or the MICR font inside the container, make sure your `Dockerfile` installs them (e.g., `apt-get update && apt-get install -y imagemagick fonts-...`).
> - If you want the Ollama CLI available in the container, add the following to your `Dockerfile`:
>   ```dockerfile
>   RUN curl -fsSL https://ollama.com/install.sh | sh
>   ```
> - Optionally, to add the Python client for Ollama:
>   ```dockerfile
>   RUN conda install -c conda-forge ollama-python -y
>   ```

### 2. Run the API

Expose the FastAPI app on port 8000:

```bash
docker run --rm -p 8000:8000 check-imaging:latest
```

Your API will be available at `http://localhost:8000`.

## API Usage

### Endpoint

```
POST /check-image
```

### How to Send Input

You can either upload a file or provide an image URL via `multipart/form-data`.

-   **Upload a file:** Put the file in the `image_file` form field.
-   **Provide an image URL:** Put the URL string in the `image_url` form field.

> **Important:** Only send one of `image_file` or `image_url` per request.

### Optional Fields

You may support the following optional fields in the form data:

-   `threshold` (float): e.g., `0.67`

### Examples

#### cURL

##### Upload a file

```bash
curl -X POST http://localhost:8000/check-image \
  -F "image_file=@tests/check_front.jpg" \
  -F "threshold=0.67" \
  -o check_front.tiff
```

This will save the converted TIFF to `check_front.tiff`.

##### Use a remote image URL

```bash
curl -X POST http://localhost:8000/check-image \
  -F "image_url=https://example.com/path/to/check_front.jpg" \
  -F "threshold=0.67" \
  -o check_front.tiff
```

#### Python (`requests`)

##### Upload a file

```python
import requests

url = "http://localhost:8000/check-image"
files = {"image_file": open("tests/check_front.jpg", "rb")}
resp = requests.post(url, files=files)
print(resp.text)
```

##### Use a remote image URL

```python
import requests

url = "http://localhost:8000/check-image"
data = {
    "image_url": "https://example.com/path/to/check_front.jpg",
}
resp = requests.post(url, data=data)
print(resp.text)
```