from importlib.metadata import version
import yaml


def get_version():
    try:
        with open("gicha-version.yml") as version_file:
            parsed_version_file = yaml.load(version_file, Loader=yaml.FullLoader)
            return parsed_version_file["version"]
    except FileNotFoundError:
        # if no local version file is found
        # then we suppose the call comes from installed package
        # and we just return the installed version
        return version("gicha")
