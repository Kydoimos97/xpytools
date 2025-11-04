import base64
from io import BytesIO

import pytest

PIL = pytest.importorskip("PIL", reason="PIL required for img tests")
from PIL import Image


@pytest.fixture
def sample_image_bytes():
    """Create a simple test img as bytes"""
    img = Image.new('RGB', (100, 100), color='red')
    buf = BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()


@pytest.fixture
def sample_image():
    """Create a simple test PIL Image"""
    return Image.new('RGB', (100, 100), color='blue')


@pytest.fixture
def sample_base64(sample_image_bytes):
    """Create a base64-encoded img string"""
    return base64.b64encode(sample_image_bytes).decode('utf-8')


class TestConversions:
    """Tests for img conversions"""

    def test_to_bytes(self, sample_image):
        from xpytools.xtool.img import to_bytes

        result = to_bytes(sample_image)
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_from_bytes(self, sample_image_bytes):
        from xpytools.xtool.img import from_bytes

        result = from_bytes(sample_image_bytes)
        assert isinstance(result, Image.Image)
        assert result.size == (100, 100)

    def test_to_base64(self, sample_image):
        from xpytools.xtool.img import to_base64

        result = to_base64(sample_image)
        assert isinstance(result, str)
        assert len(result) > 0
        # Should be valid base64
        try:
            base64.b64decode(result)
        except Exception:
            pytest.fail("Invalid base64 output")

    def test_from_base64(self, sample_base64):
        from xpytools.xtool.img import from_base64

        result = from_base64(sample_base64)
        assert isinstance(result, Image.Image)

    def test_from_base64_with_data_uri(self, sample_base64):
        from xpytools.xtool.img import from_base64

        data_uri = f"data:img/png;base64,{sample_base64}"
        result = from_base64(data_uri)
        assert isinstance(result, Image.Image)

    def test_base64_to_bytes(self, sample_base64):
        from xpytools.xtool.img import base64_to_bytes

        result = base64_to_bytes(sample_base64)
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_roundtrip_bytes(self, sample_image):
        from xpytools.xtool.img import to_bytes, from_bytes

        img_bytes = to_bytes(sample_image)
        restored = from_bytes(img_bytes)
        assert restored.size == sample_image.size
        assert restored.mode == sample_image.mode

    def test_roundtrip_base64(self, sample_image):
        from xpytools.xtool.img import to_base64, from_base64

        b64 = to_base64(sample_image)
        restored = from_base64(b64)
        assert restored.size == sample_image.size


class TestLoad:
    """Tests for img loading"""

    def test_load_from_bytes(self, sample_image_bytes):
        from xpytools.xtool.img import load

        result = load(sample_image_bytes, rtype="bytes")
        assert result == sample_image_bytes

    def test_load_from_bytes_as_pil(self, sample_image_bytes):
        from xpytools.xtool.img import load

        result = load(sample_image_bytes, rtype="pil.img")
        assert isinstance(result, Image.Image)

    def test_load_from_bytes_as_base64(self, sample_image_bytes):
        from xpytools.xtool.img import load

        result = load(sample_image_bytes, rtype="base64")
        assert isinstance(result, str)
        # Verify it's valid base64
        decoded = base64.b64decode(result)
        assert decoded == sample_image_bytes

    def test_load_from_base64(self, sample_base64):
        from xpytools.xtool.img import load

        result = load(sample_base64, rtype="pil.img")
        assert isinstance(result, Image.Image)

    def test_load_from_path(self, tmp_path, sample_image_bytes):
        from xpytools.xtool.img import load

        # Create temp img file
        img_path = tmp_path / "test.png"
        img_path.write_bytes(sample_image_bytes)

        result = load(str(img_path), rtype="pil.img")
        assert isinstance(result, Image.Image)

    def test_load_from_path_object(self, tmp_path, sample_image_bytes):
        from xpytools.xtool.img import load

        img_path = tmp_path / "test.png"
        img_path.write_bytes(sample_image_bytes)

        result = load(img_path, rtype="bytes")
        assert result == sample_image_bytes

    def test_load_invalid_rtype(self, sample_image_bytes):
        from xpytools.xtool.img import load

        with pytest.raises(ValueError, match="Invalid rtype"):
            load(sample_image_bytes, rtype="invalid")

    def test_load_nonexistent_file(self):
        from xpytools.xtool.img import load

        with pytest.raises(FileNotFoundError):
            load("/nonexistent/file.png")

    @pytest.mark.skipif(
            not pytest.importorskip("requests", reason="requests not installed"),
            reason="requests not available"
            )
    def test_load_from_url_mock(self, sample_image_bytes, monkeypatch):
        from xpytools.xtool.img import load
        import requests

        class MockResponse:
            content = sample_image_bytes

            def raise_for_status(self):
                pass

        def mock_get(*args, **kwargs):
            return MockResponse()

        monkeypatch.setattr(requests, "get", mock_get)

        result = load("https://example.com/image.png", rtype="bytes")
        assert result == sample_image_bytes


class TestTransform:
    """Tests for img transformations"""

    def test_create_thumbnail(self, sample_image_bytes):
        from xpytools.xtool.img import create_thumbnail

        result = create_thumbnail(sample_image_bytes, size=(50, 50))
        assert isinstance(result, bytes)

        # Verify thumbnail is smaller
        thumb_img = Image.open(BytesIO(result))
        assert thumb_img.size[0] <= 50
        assert thumb_img.size[1] <= 50

    def test_create_thumbnail_preserves_aspect(self, sample_image_bytes):
        from xpytools.xtool.img import create_thumbnail

        # Create non-square img
        img = Image.new('RGB', (200, 100), color='green')
        buf = BytesIO()
        img.save(buf, format='PNG')
        img_bytes = buf.getvalue()

        result = create_thumbnail(img_bytes, size=(50, 50))
        thumb_img = Image.open(BytesIO(result))

        # Should maintain aspect ratio (2:1)
        assert thumb_img.size[0] == 50
        assert thumb_img.size[1] == 25

    def test_resize_exact(self, sample_image_bytes):
        from xpytools.xtool.img import resize

        result = resize(sample_image_bytes, size=(200, 150), keep_aspect=False)
        resized_img = Image.open(BytesIO(result))
        assert resized_img.size == (200, 150)

    def test_resize_keep_aspect(self, sample_image_bytes):
        from xpytools.xtool.img import resize

        result = resize(sample_image_bytes, size=(200, 200), keep_aspect=True)
        resized_img = Image.open(BytesIO(result))
        # Should fit within 200x200 but maintain aspect
        assert resized_img.size[0] <= 200
        assert resized_img.size[1] <= 200

    def test_resize_custom_format(self, sample_image_bytes):
        from xpytools.xtool.img import resize

        result = resize(sample_image_bytes, size=(50, 50), format="JPEG")
        # Should still work (no exception)
        assert isinstance(result, bytes)
