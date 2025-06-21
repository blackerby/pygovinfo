import os
from pprint import pprint

from govinfo import GovInfo

api_key = os.getenv("GPO_API_KEY")
govinfo = GovInfo(api_key=api_key)
collections = govinfo.collections()

pprint(list(collections))
