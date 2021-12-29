import os

from dotenv import load_dotenv
from sec_api import FullTextSearchApi, RenderApi

load_dotenv()

_SEC_API_KEY: str = os.environ.get("QUERY_API_KEY")
SEC_FULL_TEXT_SEARCH_API = (FullTextSearchApi(api_key=_SEC_API_KEY))
SEC_RENDER_API = RenderApi(api_key=_SEC_API_KEY)

INTRINIO_API_KEY: str = os.environ.get("INTRINIO_API_KEY")

EMAIL_PASSWORD: str = os.environ.get('EMAIL_PASSWORD')
