"""
Generate the app defaults
"""
import platform
import os
import re

from datetime import datetime
from .read_package import read_package_file

# Platform consts
PLATFORM = "python"
PLATFORM_VERSION = platform.python_version()

# Fallbacks
DEFAULT_PACKAGE_NAME = "unknown-app"
DEFAULT_PACKAGE_VERSION = "0.0.0"


def parse_app_name(name):
    env = os.getenv("ENV", os.getenv("PYTHON_ENV", ""))

    if env == "acceptance":
        return re.sub("-acc$", "", name)

    if env == "test":
        return re.sub("-test$", "", name)

    return name


def defaults():
    package = read_package_file()
    app_name = package.get("name", DEFAULT_PACKAGE_NAME)

    return {
        "appName": parse_app_name(app_name),
        "appVersion": package.get("version", DEFAULT_PACKAGE_VERSION),
        "platform": PLATFORM,
        "platformVersion": PLATFORM_VERSION,
        "timestamp": datetime.now().astimezone().isoformat(),
    }
