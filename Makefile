all: pip

venv:
	[ -e venv/bin/pip ] || pyvenv-3.3 venv
	wget http://python-distribute.org/distribute_setup.py
	./venv/bin/python distribute_setup.py
	./venv/local/bin/easy_install pip

pip: venv
	./venv/local/bin/pip install -r requirements.txt

