# CO3095-Group9
# Film Reccomendation System

## Installions before running
Please install these packages before running:
- fuzzywuzzy
- coverage
- beautifulsoup4
- pynguin
- pip install pytest-mock
- pip install typing-extensions

you can install these by simply doing:

pip install (name of library)

## For Testing
### To run AM1460's random blackbox and whitebox testing input into terminal:
python -m coverage run -p -m pytest am1460/test/blackbox/random_based/test_logic_user_settings.py

python -m coverage run -p -m unittest discover am1460/test/blackbox/specification_based/

python -m coverage run -p am1460/test/whitebox/statement_testing/test_objects.py

python -m coverage run -p am1460/test/whitebox/statement_testing/test_keyword_search_statements.py

python -m coverage run -p am1460/test/whitebox/branch_testing/test_object_logic.py

python -m coverage run -p am1460/test/whitebox/branch_testing/test_keyword_search_branches.py

python -m coverage run -p -m pytest am1460/test/blackbox/random_based/test_logic_user_settings.py


### Combine: 
python -m coverage combine

### Report: 
python -m coverage report -m
## Descripion

## Usage

## Contributors

