import os
from urllib.parse import urlparse, parse_qs

import pytest

from integrations.hubspot import HubSpotIntegration
from integrations.notion import NotionIntegration
from integrations.airtable import AirtableIntegration


@pytest.fixture
def hubspot():
    os.environ["HUBSPOT_CLIENT_ID"] = "test-hubspot-client"
    os.environ["HUBSPOT_CLIENT_SECRET"] = "test-hubspot-secret"
    os.environ["BACKEND_URL"] = "http://localhost:8000"

    return HubSpotIntegration()


@pytest.fixture
def notion():
    os.environ["NOTION_CLIENT_ID"] = "test-notion-client"
    os.environ["NOTION_CLIENT_SECRET"] = "test-notion-secret"
    os.environ["BACKEND_URL"] = "http://localhost:8000"

    return NotionIntegration()


@pytest.fixture
def airtable():
    os.environ["AIRTABLE_CLIENT_ID"] = "test-airtable-client"
    os.environ["AIRTABLE_CLIENT_SECRET"] = "test-airtable-secret"
    os.environ["BACKEND_URL"] = "http://localhost:8000"

    return AirtableIntegration()


def test_hubspot_auth_url(hubspot):
    url = hubspot.get_auth_url()

    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    assert parsed.scheme == "https"
    assert parsed.netloc == "app.hubspot.com"
    assert parsed.path == "/oauth/authorize"

    assert params["client_id"][0] == "test-hubspot-client"
    assert params["redirect_uri"][0] == (
        "http://localhost:8000/integrations/hubspot/oauth2callback"
    )
    assert "state" in params
    assert "oauth" in params["scope"][0]


def test_notion_auth_url(notion):
    url = notion.get_auth_url()

    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    assert parsed.scheme == "https"
    assert parsed.netloc == "api.notion.com"
    assert parsed.path == "/v1/oauth/authorize"

    assert params["client_id"][0] == "test-notion-client"
    assert params["redirect_uri"][0] == (
        "http://localhost:8000/integrations/notion/oauth2callback"
    )
    assert params["response_type"][0] == "code"
    assert params["owner"][0] == "user"
    assert "state" in params


def test_airtable_auth_url(airtable):
    url = airtable.get_auth_url()

    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    assert parsed.scheme == "https"
    assert parsed.netloc == "airtable.com"
    assert parsed.path == "/oauth2/v1/authorize"

    assert params["client_id"][0] == "test-airtable-client"
    assert params["redirect_uri"][0] == (
        "http://localhost:8000/integrations/airtable/oauth2callback"
    )
    assert params["response_type"][0] == "code"

    assert "state" in params
    assert "code_challenge" in params
    assert params["code_challenge_method"][0] == "S256"


def test_hubspot_missing_credentials(monkeypatch):
    monkeypatch.delenv("HUBSPOT_CLIENT_ID", raising=False)
    monkeypatch.delenv("HUBSPOT_CLIENT_SECRET", raising=False)

    with pytest.raises(ValueError):
        HubSpotIntegration()


def test_notion_missing_credentials(monkeypatch):
    monkeypatch.delenv("NOTION_CLIENT_ID", raising=False)
    monkeypatch.delenv("NOTION_CLIENT_SECRET", raising=False)

    with pytest.raises(ValueError):
        NotionIntegration()


def test_airtable_missing_credentials(monkeypatch):
    monkeypatch.delenv("AIRTABLE_CLIENT_ID", raising=False)
    monkeypatch.delenv("AIRTABLE_CLIENT_SECRET", raising=False)

    with pytest.raises(ValueError):
        AirtableIntegration()