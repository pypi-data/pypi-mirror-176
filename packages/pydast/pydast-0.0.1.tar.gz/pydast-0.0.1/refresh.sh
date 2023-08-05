cd h:/PyDaSt
python setup.py sdist bdist_wheel
pip install ./dist/pydast-0.0.1-py3-none-any.whl --force-reinstall
cd testing
clear