# importing user agent
from .helpers import __user_agent

# importing webdrivers and options

from seleniumrequests import RequestMixin, Chrome as ChromeRequests, Opera as OperaRequests, \
    Safari as SafariRequests, Firefox as FirefoxRequests
from selenium.webdriver import ChromeOptions
from selenium.webdriver.opera.options import Options as OperaOptions  # , AndroidOptions as OperaAndroidOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from msedge.selenium_tools.webdriver import WebDriver as Edge
from msedge.selenium_tools.options import Options as EdgeOptions

# importing managers
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.opera import OperaDriverManager
from webdriver_manager.firefox import GeckoDriverManager

import os
import sys


class WebDriverNotFoundError(BaseException):
    pass


def prepare_universal_options(options):
    options.add_argument("--headless")
    options.add_argument("start-maximized")
    options.add_argument("--disable-logging")
    options.add_argument("--log-level=0")
    options.add_argument("disable-gpu")
    options.add_argument(__user_agent)
    return options


def prepare_chromium_type_driver_options(options):
    options = prepare_universal_options(options)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    return options


def prepare_edge_options(options: EdgeOptions):
    options.use_chromium = True
    return prepare_chromium_type_driver_options(options)


# def prepare_android_chromium_options(options):
#     options.add_experimental_option('androidPackage', 'com.android.chrome')
#     return prepare_chromium_type_driver_options(options)


def prepare_firefox_options(options: FirefoxOptions):
    options.headless = True
    options = prepare_universal_options(options)
    return options


class EdgeRequests(Edge, RequestMixin):
    pass


def get_driver(wdm_output: bool = False, local_storage: bool = False, debug_output: bool = False):
    """
    Returns optimal webdriver for usage.
    :return: web_driver object for doing requests
    """
    if not wdm_output:
        os.environ['WDM_PRINT_FIRST_LINE'] = 'False'
        os.environ['WDM_LOG_LEVEL'] = '0'
    if local_storage:
        os.environ['WDM_LOCAL'] = '1'  # to storage web drivers not far from sources (in project root)
    drivers = {
        "chrome": {"driver": ChromeRequests, "manager": ChromeDriverManager,
                   "options": prepare_chromium_type_driver_options(ChromeOptions())},
        "edge": {"driver": EdgeRequests, "manager": EdgeChromiumDriverManager,
                 "options": prepare_edge_options(EdgeOptions())},
        "opera": {"driver": OperaRequests, "manager": OperaDriverManager,
                  "options": prepare_chromium_type_driver_options(OperaOptions())},
        "firefox": {"driver": FirefoxRequests, "manager": GeckoDriverManager,
                    "options": prepare_firefox_options(FirefoxOptions())},
        "safari": {"driver": SafariRequests},
        # "chrome-android": {"driver": ChromeRequests, "path": "./chromedriver",
        #                    "options": prepare_android_chromium_options(ChromeOptions())},
        # "opera-android": {"driver": OperaRequests, "manager": OperaDriverManager,
        #                   "options": prepare_chromium_type_driver_options(OperaAndroidOptions())},
    }
    for name, info in drivers.items():
        try:
            if debug_output:
                print(f"trying to get {name} driver:", file=sys.stderr)
            options = info.get("options", None)
            if info.get("manager", None) is not None:
                driver = info["driver"](executable_path=info["manager"]().install(), options=options)
            # elif info.get("path", None) is not None:
            #     driver = info["driver"](executable_path=info["path"], options=option)
            else:
                driver = info["driver"]()
            if driver is not None:
                if debug_output:
                    print(f"Using driver: {name}", file=sys.stderr)
                return driver
        except Exception as e:
            if debug_output:
                print(f"Some exception occurred:\n{e}", file=sys.stderr)
    raise WebDriverNotFoundError("Unable to find webdriver for your OS")
