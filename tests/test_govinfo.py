from govinfo import GovInfo
from govinfo.config import OFFSET_DEFAULT, PAGE_DEFAULT


def test_govinfo_default_api_key():
    govinfo = GovInfo()
    assert govinfo._api_key == "DEMO_KEY"


def test_govinfo_user_supplied_api_key():
    govinfo = GovInfo(api_key="dummy key")
    assert govinfo._api_key == "dummy key"


def test_govinfo_repr():
    govinfo = GovInfo()
    assert str(govinfo) == "GovInfo(url='https://api.govinfo.gov', api_key='DEMO_KEY')"
    govinfo = GovInfo(api_key="dummy key")
    assert (
        str(govinfo)
        == "GovInfo(url='https://api.govinfo.gov', api_key='user supplied')"
    )


def test_build_default_collections_request():
    govinfo = GovInfo()
    govinfo._build_request(endpoint="collections")
    assert govinfo._path == "collections"
    assert govinfo._params == {"offsetMark": OFFSET_DEFAULT, "pageSize": PAGE_DEFAULT}


def test_build_collections_request_with_args():
    govinfo = GovInfo()
    govinfo._build_request(
        endpoint="collections",
        collection="bills",
        start_date="2025-06-16T00:00:00Z",
        page_size=10,
        offset_mark="something",
    )
    assert govinfo._path == "collections/bills/2025-06-16T00:00:00Z"
    assert govinfo._params == {"offsetMark": "something", "pageSize": 10}


def test_build_default_packages_granules_request():
    govinfo = GovInfo()
    govinfo._build_request(endpoint="packages", package_id="CREC-2018-01-04")
    assert govinfo._path == "packages/CREC-2018-01-04/granules"
    assert govinfo._params == {"offsetMark": OFFSET_DEFAULT, "pageSize": PAGE_DEFAULT}


def test_build_packages_granules_request_with_args():
    govinfo = GovInfo()
    govinfo._build_request(
        endpoint="packages",
        package_id="CREC-2018-01-04",
        granule_class="something",
        md5="something",
    )
    assert govinfo._path == "packages/CREC-2018-01-04/granules"
    assert govinfo._params == {
        "offsetMark": OFFSET_DEFAULT,
        "pageSize": PAGE_DEFAULT,
        "granuleClass": "something",
        "md5": "something",
    }


def test_build_default_published_request():
    govinfo = GovInfo()
    govinfo._build_request(
        endpoint="published", collection="bills", start_date="2025-06-20"
    )
    assert govinfo._path == "published/2025-06-20"
    assert govinfo._params == {
        "offsetMark": OFFSET_DEFAULT,
        "pageSize": PAGE_DEFAULT,
        "collection": "bills",
    }
