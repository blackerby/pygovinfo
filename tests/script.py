import os
from pprint import pprint

from govinfo import GovInfo

api_key = os.getenv("GPO_API_KEY")
govinfo = GovInfo(api_key=api_key)
start_date = "2025-06-20T00:00:00Z"
collections = govinfo.collections("bills", start_date=start_date)

pprint(list(collections))
