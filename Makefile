all: pip

venv3:
	[ -e venv/bin/pip ] || pyvenv-3.3 venv
	wget http://python-distribute.org/distribute_setup.py
	./venv/bin/python distribute_setup.py
	./venv/local/bin/easy_install pip

venv:
	[ -e venv/bin/pip ] || virtualenv venv

pip: venv
	./venv/bin/pip install -r requirements.txt

