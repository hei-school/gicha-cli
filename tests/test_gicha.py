import platform
import gicha
from gicha.myos import cd_then_exec
from filecmp import dircmp
import shutil
from tempfile import TemporaryDirectory
import os.path
from pytest import raises


def oracle_rel_path(oracle_dir_name):
    return f"tests/oracles/{oracle_dir_name}"


def test_app_name_must_be_defined():
    with raises(Exception) as e:
        gicha.gen()
    assert (
        str(e.value)
        == "app_name in conf file (or --app-name as argument) must be defined"
    )


def test_gicha_conf_must_use_proper_version():
    with raises(Exception) as e:
        gicha.gen(gicha_conf=oracle_rel_path("gicha-conf-bad-version.yml"))
    assert (
        str(e.value)
        == "You must use the gicha version defined in your conf file. Forgot to upgrade?"
    )


def test_base():
    output_dir = "test-gicha-base"
    gicha.gen(app_name="gicha-base", output_dir=output_dir)
    assert is_dir_superset_of(oracle_rel_path("oracle-gicha-base"), output_dir)


def are_dir_equals(dir1, dir2):
    return is_dir_superset_of(dir1, dir2) and is_dir_superset_of(dir2, dir1)


def is_dir_superset_of(superset_dir, subset_dir):
    compared = dircmp(superset_dir, subset_dir)
    print(
        "superset_only=%s, subset_only=%s, both=%s, incomparables=%s"
        % (
            compared.left_only,
            compared.right_only,
            compared.diff_files,
            compared.funny_files,
        ),
    )
    if compared.right_only or compared.diff_files or compared.funny_files:
        return False
    for subdir in compared.common_dirs:
        if not is_dir_superset_of(
            os.path.join(superset_dir, subdir), os.path.join(subset_dir, subdir)
        ):
            return False
    return True


def oracle_tests_are_passing(oracle_dir):
    if "Windows" in platform.system():
        return True
    gradlew_file = f"{oracle_dir}/gradlew"
    os.system(f"chmod +x {gradlew_file}")

    aws_env = "AWS_ACCESS_KEY_ID=dummy AWS_SECRET_ACCESS_KEY=dummy AWS_REGION=dummy"
    test_return_code = os.system(f"cd {oracle_dir} && {aws_env} ./gradlew test")

    return test_return_code == 0
