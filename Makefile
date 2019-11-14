
.PHONY:
	test_python
	run_python

test_python: python/test.py
		docker run --rm -u $$(id -u) \
		    -v $(CURDIR)/python:/python \
		python:3.6 \
		    python /python/test.py

run_python: python/test.py
		docker run --rm -u $$(id -u) \
		    -v $(CURDIR)/python:/python \
		python:3.6 \
		    python /python/rps.py
