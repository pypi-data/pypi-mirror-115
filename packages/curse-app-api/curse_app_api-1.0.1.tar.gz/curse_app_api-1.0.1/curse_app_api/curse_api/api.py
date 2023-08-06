from curse_app_api.utils import get_query, InvalidArgumentError, check_response, headers
from requests import session, Response
from typing import List, Dict, Optional, Union


class CurseAPI:
    """
    Base API class. Uses requests.Session() for doing requests


    Each method has PyDoc with link that leads to api documentation.
    There you can see which parameters and types should be in your request, and type of response
    """

    def __init__(self):
        self._base_link = "https://addons-ecs.forgesvc.net/api/v2"
        self._last_query_link = ""
        self._last_response = None
        self._web = None
        self._init_web()

    def _init_web(self):
        self._web = session()
        self._web.headers = headers

    def search_addon(self, params: Optional[Dict[str, Union[int, str]]] = None, **kwargs):
        """
        params and kwargs will be merged, from duplicates from params and kwargs the highest priority is on kwargs
        Note: not all parameters required for request, but more parameters will lead to more accurate result

        https://curseforgeapi.docs.apiary.io/#/reference/0/curseforge-addon-search
        """
        attr = {"categoryid": int, "gameid": int, "gameversion": str, "index": int, "pagesize": int,
                "searchfilter": str, "sectionid": int, "sort": int}
        if params is None:
            params = {}
        if type(params) != dict:
            raise InvalidArgumentError("'params' should be a dict object")
        search_params = f"/addon/search?"
        query = get_query(attr, params, kwargs)
        search_params += "&".join(f"{key}={value}" for key, value in query.items())
        self._last_query_link = self._base_link + search_params
        self._last_response = self._web.request("GET", self._last_query_link)
        return check_response(self._last_response)

    def search_by_fingerprint(self, fingerprint: int):
        """
        https://curseforgeapi.docs.apiary.io/#/reference/0/get-addon-by-fingerprint
        """
        self._last_query_link = self._base_link + "/fingerprint"
        self._last_response = self._web.request("POST", self._last_query_link, json=[fingerprint])
        return check_response(self._last_response)

    def get_addon_description(self, addonID: int):
        """
        https://curseforgeapi.docs.apiary.io/#/reference/0/get-addon-description
        """
        params = f"/addon/{addonID}/description"
        self._last_query_link = self._base_link + params
        self._last_response = self._web.request("GET", self._last_query_link)
        return check_response(self._last_response, "text")

    def get_addon_file_changelog(self, addonID: int, fileID: int):
        """
        https://curseforgeapi.docs.apiary.io/#/reference/0/get-addon-file-changelog/get-addon-file-changelog
        """
        params = f"/addon/{addonID}/file/{fileID}/changelog"
        self._last_query_link = self._base_link + params
        self._last_response = self._web.request("GET", self._last_query_link)
        return check_response(self._last_response, "text")

    def get_addon_file_download_url(self, addonID: int, fileID: int):
        """
        https://curseforgeapi.docs.apiary.io/#/reference/0/get-addon-file-download-url
        """
        params = f"/addon/{addonID}/file/{fileID}/download-url"
        self._last_query_link = self._base_link + params
        self._last_response = self._web.request("GET", self._last_query_link)
        return check_response(self._last_response, "text")

    def get_addon_file_information(self, addonID: int, fileID: int):
        """
        https://curseforgeapi.docs.apiary.io/#/reference/0/get-addon-file-information
        """
        params = f"/addon/{addonID}/file/{fileID}"
        self._last_query_link = self._base_link + params
        self._last_response = self._web.request("GET", self._last_query_link)
        return check_response(self._last_response)

    def get_addon_info(self, addonID: int):
        """
        https://curseforgeapi.docs.apiary.io/#/reference/0/get-addon-info
        """
        param = f"/addon/{addonID}"
        self._last_query_link = self._base_link + param
        self._last_response = self._web.request("GET", self._last_query_link)
        return check_response(self._last_response)

    def get_addons_database_timestamp(self):
        """
        https://curseforgeapi.docs.apiary.io/#/reference/0/get-addons-database-timestamp
        """
        self._last_query_link = self._base_link + "/addon/timestamp"
        self._last_response = self._web.request("GET", self._last_query_link)
        return self._last_response.json(strict=False)

    def get_category_info(self, CategoryID: int):
        """
        https://curseforgeapi.docs.apiary.io/#/reference/0/get-category-info
        """
        param = f"/category/{CategoryID}"
        self._last_query_link = self._base_link + param
        self._last_response = self._web.request("GET", self._last_query_link)
        return check_response(self._last_response)

    def get_category_list(self):
        """
        https://curseforgeapi.docs.apiary.io/#/reference/0/get-category-list
        """
        self._last_query_link = self._base_link + "/category"
        self._last_response = self._web.request("GET", self._last_query_link)
        return self._last_response.json(strict=False)

    def get_category_section_info(self, SectionID: int):
        """
        https://curseforgeapi.docs.apiary.io/#/reference/0/get-category-section-info
        """
        param = f"/category/section/{SectionID}"
        self._last_query_link = self._base_link + param
        self._last_response = self._web.request("GET", self._last_query_link)
        return check_response(self._last_response)

    def get_category_timestamp(self):
        """
        https://curseforgeapi.docs.apiary.io/#/reference/0/get-category-timestamp
        """
        self._last_query_link = self._base_link + "/category/timestamp"
        self._last_response = self._web.request("GET", self._last_query_link)
        return self._last_response.json(strict=False)

    def get_featured_addons(self, params: Optional[Dict] = None, **kwargs):
        """
        params and kwargs will be merged, from duplicates from params and kwargs the highest priority is on kwargs
        Note: not all parameters required for request, but more parameters will lead to more accurate result

        https://curseforgeapi.docs.apiary.io/#/reference/0/get-featured-addons
        """
        attr = {"gameid": int, "addonids": List[int], "featuredcount": int, "popularcount": int, "updatedcount": int}
        if params is None:
            params = {}
        if type(params) != dict:
            raise InvalidArgumentError("params should be in a dictionary with keys:\n" +
                                       "\n".join("\'" + key + "\' with value of type: \'" + str(value) + "\'"
                                                 for key, value in attr.items()))
        query = get_query(attr, params, kwargs)
        self._last_query_link = self._base_link + "/addon/featured"
        return self._web.request("POST", self._last_query_link, json=query).json(strict=False)

    def get_game_info(self, GameID: int):
        """
        https://curseforgeapi.docs.apiary.io/#/reference/0/get-game-info
        """
        self._last_query_link = self._base_link + f"/game/{GameID}"
        self._last_response = self._web.request("GET", self._last_query_link)
        return check_response(self._last_response)

    def get_game_timestamp(self):
        """
        https://curseforgeapi.docs.apiary.io/#/reference/0/get-game-timestamp
        """
        self._last_query_link = self._base_link + "/game/timestamp"
        self._last_response = self._web.request("GET", self._last_query_link)
        return self._last_response.json(strict=False)

    def get_games_list(self, supportsAddons: Optional[bool] = None):
        """
        https://curseforgeapi.docs.apiary.io/#/reference/0/get-games-list
        """
        self._last_query_link = self._base_link + "/game"
        if supportsAddons is not None:
            self._last_query_link += f"?supportsAddons={supportsAddons}"
        self._last_response = self._web.request("GET", self._last_query_link)
        return check_response(self._last_response)

    def get_minecraft_version_info(self, VersionString: str):
        """

        https://curseforgeapi.docs.apiary.io/#/reference/0/get-minecraft-version-info

        Returns minecraft version info by given it's version in 'str' object

        Note: works on RELEASES only.
        :param VersionString: ex. "1.12.2"
        :return: dict with info about {VersionString} version of minecraft
        """
        param = f"/minecraft/version/{VersionString}"
        self._last_query_link = self._base_link + param
        self._last_response = self._web.request("GET", self._last_query_link)
        return check_response(self._last_response)

    def get_minecraft_version_list(self) -> Union[List[Dict[str, Union[int, str]]], str]:
        """
        https://curseforgeapi.docs.apiary.io/#/reference/0/get-minecraft-version-list
        """
        self._last_query_link = self._base_link + "/minecraft/version"
        self._last_response = self._web.request("GET", self._last_query_link)
        return self._last_response.json(strict=False)

    def get_minecraft_version_timestamp(self):
        """
        https://curseforgeapi.docs.apiary.io/#/reference/0/get-minecraft-version-timestamp
        """
        self._last_query_link = self._base_link + "/minecraft/version/timestamp"
        self._last_response = self._web.request("GET", self._last_query_link)
        return self._last_response.json(strict=False)

    def get_modloader_info(self, VersionName: str):
        """
        https://curseforgeapi.docs.apiary.io/#/reference/0/get-modloader-info
        """
        param = f"/minecraft/modloader/{VersionName}"
        self._last_query_link = self._base_link + param
        self._last_response = self._web.request("GET", self._last_query_link)
        return check_response(self._last_response)

    def get_modloader_list(self):
        """
        https://curseforgeapi.docs.apiary.io/#/reference/0/get-modloader-list
        """
        self._last_query_link = self._base_link + "/minecraft/modloader"
        self._last_response = self._web.request("GET", self._last_query_link)
        return self._last_response.json(strict=False)

    def get_modloader_timestamp(self):
        """
        https://curseforgeapi.docs.apiary.io/#/reference/0/get-modloader-timestamp
        """
        self._last_query_link = self._base_link + "/minecraft/modloader/timestamp"
        self._last_response = self._web.request("GET", self._last_query_link)
        return self._last_response.json(strict=False)

    def get_multiple_addons(self, params: Optional[List[int]] = None, *args):
        """
        params and args will be merged and will be prepared to send unique IDs (set)
        https://curseforgeapi.docs.apiary.io/#/reference/0/get-multiple-addons
        """
        if params is None:
            params = []
        query = list(set(params + list(args)))
        for e in query:
            if type(e) != int:
                raise InvalidArgumentError("parameters should be integer values.")
        self._last_query_link = self._base_link + "/addon"
        self._last_response = self._web.request("POST", self._last_query_link, json=query)
        return check_response(self._last_response)

    @property
    def last_query_link(self) -> str:
        return self._last_query_link

    @property
    def last_response(self) -> Response:
        return self._last_response
