install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

format:	
	black *.py 

lint:
	pylint --disable=R,C,locally-disabled --ignore-patterns=test_.*?py *.py

test:
	python3 -m pytest -vv --cov=main test_*.py
		
all: install format lint test  