import pytest
from app.services.seo_service import get_home_seo, SeoData


def test_home_seo_data():
    """Тест создания SEO данных для главной"""
    seo = get_home_seo()

    assert isinstance(seo, SeoData)
    assert seo.title is not None
    assert seo.description is not None
    assert len(seo.title) > 10
    assert len(seo.description) > 20


def test_seo_meta_tags():
    """Тест генерации мета-тегов"""
    seo = get_home_seo()

    # Создаём мок-запрос
    class MockRequest:
        url = type('obj', (), {'path': '/'})()

    request = MockRequest()
    meta = seo.get_meta_tags(request)

    assert "title" in meta
    assert "description" in meta
    assert "og_title" in meta
    assert "og_image" in meta
    assert "canonical" in meta


def test_seo_data_defaults():
    """Тест значений по умолчанию"""
    seo = SeoData(
        title="Test",
        description="Test description"
    )

    assert seo.og_title == seo.title
    assert seo.og_description == seo.description
    assert seo.canonical == "/"
    assert seo.og_type == "website"
    assert seo.robots == "index, follow"