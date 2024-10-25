import importlib.metadata
import requests

def get_latest_package_version(package_name):
    response = requests.get(f'https://pypi.org/pypi/{package_name}/json')
    return response.json()['info']['version']

def get_versions(package_name:str = "gitco"):
    current_version = importlib.metadata.version(package_name)
    latest_version = get_latest_package_version(package_name)
    return current_version, latest_version

def get_version(): # get_it: bool):
    # if get_it:
    current_version, latest_version = get_versions()
    print(f"Current version: {current_version} || Latest version: {latest_version}")

def warn_latest():
    current_version, latest_version = get_versions()

    # The versions needs to be in the format x.x.x
    # because 1 and 1.0 aren't the same in the following approach

    c_version = tuple(map(int, (current_version.split("."))))
    l_version = tuple(map(int, (latest_version.split("."))))

    if l_version > c_version:
        print(f"A new version of the `gitco` package is available. (Current version: {current_version} || Latest version: {latest_version})")
    else:
        print("Your version is the latest")
