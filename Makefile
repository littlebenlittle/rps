
.PHONY:
	test_python
	run_python
	venv_install

python/venv:
		docker run --rm -u $$(id -u) \
		    -v $(CURDIR)/python:/python \
		python:3.7 \
			python -m venv /python/venv

venv_install:
		docker run --rm -u $$(id -u) \
		    -v $(CURDIR)/python:/python \
		python:3.7 \
			/python/venv/bin/pip install -r /python/requirements.txt --no-cache

venv: python/venv venv_install

pytest: python/test.py
		docker run --rm -u $$(id -u) \
		    -v $(CURDIR)/python:/python \
		    -e DEBUG=1 \
		benlittle6/pytest:3.7 \
		    /python/venv/bin/pytest /python/test.py

run_python: python/test.py
		docker run --rm -u $$(id -u) \
		    -v $(CURDIR)/python:/python \
		python:3.7 \
		    python /python/rps.py

test_rust: rust/src/main.rs
		docker run --rm -u $$(id -u) \
		    -v $(CURDIR)/rust:/rust \
			-w /rust \
		rust:1.39.0 \
		    cargo test
