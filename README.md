# CO3095-Group9
# Film Reccomendation System
GitHub Link: https://github.com/angharadMark/CO3095-Group9.git

## 1. Project Description
We have created a Film Recommendation System with a registration, login, personal watchlist, and more.

## 2. Setup Instructions
### a. Uncompress the Project
Locate the .zip file.
Extract All...

### b. Loading into PyCharm
In Pycharm, go to File > Open then navigate to our folder.

### c. Install Dependencies
In the terminal please enter:
pip install bcrypt fuzzywuzzy coverage beautifulsoup4 pynguin pytest-mock typing-extensions pytest

## 3. Run Application
Run it normally via the main.py or in the terminal:
python main.py

## 4. Testing
### To run AM1460's random blackbox and whitebox testing input into terminal:
python -m coverage run -p -m pytest am1460/test/blackbox/random_based/test_logic_user_settings.py

python -m coverage run -p -m unittest discover am1460/test/blackbox/specification_based/

python -m coverage run -p am1460/test/whitebox/statement_testing/test_objects.py

python -m coverage run -p am1460/test/whitebox/statement_testing/test_keyword_search_statements.py

python -m coverage run -p am1460/test/whitebox/branch_testing/test_object_logic.py

python -m coverage run -p am1460/test/whitebox/branch_testing/test_keyword_search_branches.py

### Combine: 
python -m coverage combine

### Report: 
python -m coverage report -m

## 5. Usage Guidelines:
**Registration:** Passwords for registration must be atleast 6 characters.
**Admin:** Admin can be accessed by the username 'admin' and password 'admins'.

## 6. Contributors
Contributions can be seen in the user stories or the report.

