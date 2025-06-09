from govinfo import Govinfo


def test_govinfo_default_api_key():
    govinfo = Govinfo()
    assert govinfo._api_key == "DEMO_KEY"


def test_govinfo_base_url():
    govinfo = Govinfo()
    assert govinfo._url == "https://api.govinfo.gov"
