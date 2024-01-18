import gicha.mygit as mygit
import shutil
import gicha.sed as sed
from gicha.myrich import print_title, print_normal, print_banner, print_warn
from gicha.version import get_version
import yaml
from yaml.loader import BaseLoader
import os
from gicha.myos import cd_then_exec

GIT_URL = "https://github.com/hei-school/gicha"
GIT_TAG_OR_COMMIT = "b8e60aa"


def gen(
    gicha_conf=None,
    app_name=None,
    region="eu-west-3",
    custom_python_requirements=None,
    custom_python_requirements_dev=None,
    custom_python_env_vars_prod=None,
    custom_python_env_vars_preprod=None,
    output_dir=None,
    pytest_min_coverage="90",
    memory=256,
):
    if gicha_conf is not None:
        with open(gicha_conf, "r") as conf_strem:
            conf = yaml.load(conf_strem, Loader=BaseLoader)
            if get_version() != conf["cli_version"]:
                raise Exception(
                    "You must use the gicha version defined in your conf file. Forgot to upgrade?"
                )
            print_warn(
                "Only --gicha-conf will be taken into account: all other arguments will be ignored!"
            )
            print_warn(
                "No default value will be used: explicit everything in your conf file!!"
            )
            app_name = conf["app_name"]
            region = conf["region"]
            custom_python_requirements = conf["custom_python_requirements"]
            custom_python_requirements_dev = conf["custom_python_requirements_dev"]
            custom_python_env_vars_prod = conf["custom_python_env_vars_prod"]
            custom_python_env_vars_preprod = conf["custom_python_env_vars_preprod"]
            pytest_min_coverage = conf["pytest_min_coverage"]
            memory = int(conf["memory"])

    if app_name is None:
        raise Exception(
            "app_name in conf file (or --app-name as argument) must be defined"
        )

    if output_dir is None:
        output_dir = app_name

    print_banner("gicha v" + get_version())

    print_title("Checkout base repository...")
    print_normal(f"git_url={GIT_URL}")
    print_normal(f"git_tag={GIT_TAG_OR_COMMIT}")
    tmp_dir = mygit.checkout(GIT_URL, GIT_TAG_OR_COMMIT, no_git=True)
    print_normal(f"tmp_dir={tmp_dir}")

    print_title("Rm project-specific files...")
    print_normal("README.md")
    os.remove(tmp_dir + "/README.md")
    print_normal("README.md")
    shutil.rmtree(tmp_dir + "/mascot")

    print_title("Handle arguments...")
    exclude = "*.pyc"
    print_normal("region")
    sed.find_replace(tmp_dir, "<?aws-region>", region, exclude)

    print_normal("memory")
    sed.find_replace(tmp_dir, "<?memory>", str(memory), exclude)

    print_normal("custom_python_requirements")
    python_requirements = replace_with_file_content(
        tmp_dir, "<?python-requirements>", custom_python_requirements, exclude
    )

    print_normal("custom_python_requirements_dev")
    python_requirements_dev = replace_with_file_content(
        tmp_dir, "<?python-requirements-dev>", custom_python_requirements_dev, exclude
    )

    print_normal("custom_python_env_vars_prod")
    python_env_vars_prod = replace_with_file_content(
        tmp_dir,
        "<?env-vars-prod>",
        custom_python_env_vars_prod,
        exclude,
    )

    print_normal("custom_python_env_vars_preprod")
    python_env_vars_preprod = replace_with_file_content(
        tmp_dir,
        "<?env-vars-preprod>",
        custom_python_env_vars_preprod,
        exclude,
    )

    print_normal("app_name")
    sed.find_replace(tmp_dir, "<?app-name>", app_name, exclude)

    print_normal("pytest_min_coverage")
    sed.find_replace(
        tmp_dir, "<?pytest-min-coverage>", str(pytest_min_coverage), exclude
    )

    print_title("Save conf...")
    save_conf(
        tmp_dir,
        app_name,
        region,
        python_requirements,
        python_requirements_dev,
        python_env_vars_prod,
        python_env_vars_preprod,
        pytest_min_coverage,
        memory,
    )
    print_normal("gicha.yml")

    print_title("Format...")
    format_cmd = "pip install black && black --exclude tests/oracles --check ."
    cd_then_exec(tmp_dir, format_cmd, format_cmd)

    print_title("Copy to output dir...")
    shutil.copytree(tmp_dir, output_dir, dirs_exist_ok=True)

    print_title("... all done!")


def save_conf(
    tmp_dir,
    app_name,
    region,
    python_requirements,
    python_requirements_dev,
    python_env_vars_prod,
    python_env_vars_preprod,
    pytest_min_coverage,
    memory,
):
    custom_python_requirements_filename = "gicha-custom-python-requirements.txt"
    custom_python_requirements_dev_filename = "gicha-custom-python-requirements-dev.txt"
    custom_python_env_vars_prod_filename = "gicha-custom-python-env-vars-prod.txt"
    custom_python_env_vars_preprod_filename = "gicha-custom-python-env-vars-preprod.txt"
    conf = {
        "cli_version": get_version(),
        "app_name": app_name,
        "region": region,
        "custom_python_requirements": custom_python_requirements_filename,
        "custom_python_requirements_dev": custom_python_requirements_dev_filename,
        "custom_python_env_vars_prod": custom_python_env_vars_prod_filename,
        "custom_python_env_vars_preprod": custom_python_env_vars_preprod_filename,
        "pytest_min_coverage": pytest_min_coverage,
        "memory": memory,
    }
    with open(tmp_dir + "/gicha.yml", "w") as conf_file:
        yaml.dump(conf, conf_file)

    print_normal(custom_python_requirements_filename)
    with open(
        f"{tmp_dir}/{custom_python_requirements_filename}", "w"
    ) as custom_python_requirements_file:
        custom_python_requirements_file.write(python_requirements)

    print_normal(custom_python_requirements_dev_filename)
    with open(
        f"{tmp_dir}/{custom_python_requirements_dev_filename}", "w"
    ) as custom_python_requirements_dev_file:
        custom_python_requirements_dev_file.write(python_requirements_dev)

    print_normal(custom_python_env_vars_prod_filename)
    with open(
        f"{tmp_dir}/{custom_python_env_vars_prod_filename}", "w"
    ) as custom_python_env_vars_prod_file:
        custom_python_env_vars_prod_file.write(
            "\n".join([s.strip() for s in python_env_vars_prod.split("\n")])
        )

    print_normal(custom_python_env_vars_preprod_filename)
    with open(
        f"{tmp_dir}/{custom_python_env_vars_preprod_filename}", "w"
    ) as custom_python_env_vars_preprod_file:
        custom_python_env_vars_preprod_file.write(
            "\n".join([s.strip() for s in python_env_vars_preprod.split("\n")])
        )


def replace_with_file_content(
    project_dir, to_replace, replacement_filepath, exclude, joiner=""
):
    if replacement_filepath is None:
        content = ""
    else:
        file = open(replacement_filepath, "r")
        content = joiner.join(file.readlines())
    sed.find_replace(project_dir, to_replace, content, exclude)
    return content
