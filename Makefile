
.PHONY:
	test_python
	run_python

pytest: python/test.py
		docker run --rm -u $$(id -u) \
		    -v $(CURDIR)/python:/python \
		    -e DEBUG=1 \
		benlittle6/pytest:3.7 \
		    pytest /python/test.py

run_python: python/test.py
		docker run --rm -u $$(id -u) \
		    -v $(CURDIR)/python:/python \
		python:3.6 \
		    python /python/rps.py

test_rust: rust/src/main.rs
		docker run --rm -u $$(id -u) \
		    -v $(CURDIR)/rust:/rust \
			-w /rust \
		rust:1.39.0 \
		    cargo test
