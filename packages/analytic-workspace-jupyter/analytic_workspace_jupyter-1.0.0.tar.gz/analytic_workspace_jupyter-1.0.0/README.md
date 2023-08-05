# aw_jupyter

Сборка проекта и выкладывание в pypi

Перед запуском команды - изменить версию в setup.py

```sh
$ python setup.py sdist
$ twine upload --username %user% --password %pass% --repository pypi dist/*
```