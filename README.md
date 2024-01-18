Gicha CLI
========

The Python CLI for maintaining a [Gicha stack](https://github.com/hei-school/gicha)... or dozens of them!

## Use cases

### Install gicha and list all possible parameters

```
pip install gicha
python -m gicha --help
```

### Create a completely new project

```
python -m gicha --app-name=gicha-base
```

Those configurations will be automatically saved in [gicha.yml](https://github.com/hei-school/gicha-cli/blob/main/tests/oracles/oracle-gicha-base/gicha.yml) at the end of the creation.

### Upgrade an already existing project

```
pip install gicha --upgrade
python -m gicha --app-name=gicha-base --output-dir=folder-already-created
```
Note the `--upgrade` and the `--output-dir=folder-already-created` flags. The Gicha configuration that was used for the previous generation is saved in `gicha.yml`: it will be updated after the new upgrade.

If you want to do an upgrade without re-specifying each parameter (there are a lot of them!), then gicha conveniently provides de `--gicha-conf` parameter.
Just modify the existing `gicha.yml`
(modify mandatorily the `version` parameter so that it reflects the newly upgraded version,
modify optionally any other parameter depending on your needs), then:
```
pip install gicha --upgrade
cd folder-already-created
python -m gicha --gicha-conf=gicha.yml --output-dir=.
```
