from govinfo import Govinfo


def test_govinfo_default_api_key():
    govinfo = Govinfo()
    assert govinfo._api_key == "DEMO_KEY"


def test_govinfo_user_supplied_api_key():
    govinfo = Govinfo(api_key="dummy key")
    assert govinfo._api_key == "dummy key"


def test_govinfo_base_url():
    govinfo = Govinfo()
    assert govinfo.url == "https://api.govinfo.gov"


def test_govinfo_repr():
    govinfo = Govinfo()
    assert str(govinfo) == "Govinfo(url='https://api.govinfo.gov', api_key='DEMO_KEY')"
    govinfo = Govinfo(api_key="dummy key")
    assert (
        str(govinfo)
        == "Govinfo(url='https://api.govinfo.gov', api_key='user supplied')"
    )


def test_govinfo_endpoint_starts_as_none():
    govinfo = Govinfo()
    assert govinfo.endpoint is None
