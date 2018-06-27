del /f/s/q dist
del /f/s/q build
del /f/s/q OpenDataTools.egg-info
git pull
python setup.py sdist
python setup.py bdist_wheel
twine upload dist/*
pause