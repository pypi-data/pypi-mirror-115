from .api import CurseAPI
from curse_app_api.utils import get_driver


class WDCurseAPI(CurseAPI):
    """
    API class that uses webdriver for requests

    Each method has PyDoc with link that leads to api documentation.
    There you can see which parameters and types should be in your request, and type of response
    """

    def __init__(self, wdm_output: bool = False, local_storage: bool = False, debug_output: bool = False):
        self._local_storage = local_storage
        self._wdm_output = wdm_output
        self._debug_output = debug_output
        super().__init__()

    def _init_web(self):
        self._web = get_driver(wdm_output=self._wdm_output, local_storage=self._local_storage,
                               debug_output=self._debug_output)
