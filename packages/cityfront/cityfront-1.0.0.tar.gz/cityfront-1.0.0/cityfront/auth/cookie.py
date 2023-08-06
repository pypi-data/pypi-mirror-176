"""Create a Cookie Auth that can act as the base for both the JWT and Token Auth strategies"""


from dataclasses import dataclass
from typing import TYPE_CHECKING, Generator
from diskcache import Cache
import httpx
from loguru import logger as log
from .base import BaseAuthStrategy
from ..utils import CookieCache
if TYPE_CHECKING:
    from cityfront import AppWrite

cookie_cache = CookieCache()
COOKIE_KEY = "cookie-store"




def cookies_to_dict(cookies: httpx.Cookies) -> dict:
    """Convert the cookies to a dict"""
    cookie_dicts = []
    if not len(cookies):
        return cookie_dicts
    for cookie in cookies.jar:
        cookie_dicts.append({"name": cookie.name, "value": cookie.value, "domain": cookie.domain, "path": cookie.path})
    return cookie_dicts

def dict_to_cookies(cookies: list[dict]) -> httpx.Cookies:
    """Convert the dict to a cookies object"""
    cookie_bin = httpx.Cookies()
    if not len(cookies):
        return cookie_bin
    for cookie in cookies:
        cookie_bin.set(cookie["name"], cookie["value"], domain=cookie["domain"], path=cookie["path"])
    return cookie_bin


@dataclass(slots=True)
class CookieAuth(httpx.Auth):
    """Admin Access Key Authentication Hook"""


    # def __init__(self):
    #     self.jwt_token = jwt_token

    def auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        request = self.load_cookies(request)
        
        
        # request.headers["X-Appwrite-Jwt"] = f"{self.jwt_token}"
        response = yield request
        self.update_cookies_if_exists(response)
    
    def load_cookies(self, request: httpx.Request) -> httpx.Cookies | None:
        """Load the cookies from the local cache if they exist"""
        unset_cookie = self.check_local_cookies()
        unset_cookie.set_cookie_header(request)
        request.cookies = unset_cookie
        return request
    
    def check_local_cookies(self) -> httpx.Cookies | None:
        """Check if the there's saved cookie code. """
        request_cookies = httpx.Cookies()
        
        if COOKIE_KEY in cookie_cache:
            
            
            stored = cookie_cache[COOKIE_KEY]
            match stored:
                case httpx.Cookies() as prior_cookie:
                    request_cookies = httpx.Cookies(prior_cookie)
                case dict() as cookie:
                    request_cookies.set(cookie["name"], cookie["value"], domain=str(cookie["domain"]).strip("."))
                case list() as cookies_list:
                    for cookie in cookies_list:
                        request_cookies.set(cookie["name"], cookie["value"], domain=str(cookie["domain"]).strip("."))
                case _:
                    log.info("No cookies to update")
        return request_cookies
    
    def update_cookies_if_exists(self, response: httpx.Response):
        """Update the local cookie store if it exists"""
        local_cookies = httpx.Cookies()
        
        
        local_cookies.extract_cookies(response)
        if len(local_cookies):
            
            cookie_dict = cookies_to_dict(local_cookies)
            # ! TODO: Might need to merge the cache with the new cookies. Will test on prototype environment.
            if cookie_dict:
                cookie_cache[COOKIE_KEY] = cookie_dict
            # cookie_cache[COOKIE_KEY] = cookie_dict

            
        

@dataclass(slots=True)
class CookieAuthStrategy(BaseAuthStrategy):
    """Personal Access Token Authentication"""

    # jwt_token: str

    def get_auth_flow(self, appwrite: "AppWrite") -> httpx.Auth:
        return CookieAuth()
