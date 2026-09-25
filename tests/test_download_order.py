import sys
import types


def _stub(name, **attrs):
    module = types.ModuleType(name)
    for key, value in attrs.items():
        setattr(module, key, value)
    sys.modules[name] = module
    return module


_stub("pillow_avif")
_image = _stub("PIL.Image", Image=object, open=lambda *args, **kwargs: None)
_stub("PIL")
sys.modules["PIL"].Image = _image
_stub("PIL.ImageOps", exif_transpose=lambda image: image)
_stub("pillow_heif", register_heif_opener=lambda: None)
_stub("requests", get=lambda *args, **kwargs: None)


class _HTTPException(Exception):
    def __init__(self, status_code=0, detail=""):
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail


_stub("fastapi", HTTPException=_HTTPException)
_stub("ollama")
_stub("schemas")
_stub("schemas.schemas", Check=type("Check", (), {}))

from helpers.helpers import image_upload_decorator  # noqa: E402


def test_url_is_downloaded_to_the_local_path():
    seen = {}

    def fake_download(url, output_path):
        seen["url"] = url
        seen["path"] = output_path
        return True

    import helpers.helpers as helpers

    helpers.download_file_from_url = fake_download
    helpers.url_to_image = lambda url: object()

    @image_upload_decorator(image_required=True)
    async def endpoint(**kwargs):
        return kwargs

    import asyncio

    asyncio.run(endpoint(image_url="https://example.test/check.png"))

    assert seen["url"] == "https://example.test/check.png"
    assert seen["path"].endswith(".png")
    assert "example.test" not in seen["path"]
