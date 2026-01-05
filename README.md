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

### To run EU20's random blackbox and whitebox testing input into terminal
python -m coverage run -p -m pytest eu20/test/blackbox/random_based

python -m coverage run -p -m pytest eu20/test/blackbox/specification_based

python -m coverage run -p -m pytest eu20/test/whitebox/statement_testing/test_user_statement.py

python -m coverage run -p -m pytest eu20/test/whitebox/branch_testing/test_database_loader_branch.py

python -m coverage run -p -m pytest eu20/test/whitebox/branch_testing/test_database_filter_branch.py

python -m coverage run -p -m pytest eu20/test/whitebox/branch_testing/test_film_branch.py

python -m coverage run -p -m pytest eu20/test/whitebox/branch_testing/test_user_auth_branch.py

python -m coverage run -p -m pytest eu20/test/whitebox/branch_testing/test_user_auth_branch.py

### To run CW536 Whitebox and Blackbox testing input into terminal:

python -m coverage run -p -m pytest cw536/test/Blackbox/Random_Testing/test_actor_helper.py
python -m coverage run -p -m pytest cw536/test/Blackbox/Random_Testing/test_Data_writer_helper.py

python -m coverage run -p -m pytest "cw536/test/Blackbox/Category Partition/Database_load_test.py"
python -m coverage run -p -m pytest "cw536/test/Blackbox/Category Partition/Film_recco_tests.py"
python -m coverage run -p -m pytest "cw536/test/Blackbox/Category Partition/Popular_test.py"
python -m coverage run -p -m pytest "cw536/test/Blackbox/Category Partition/Profanity_test.py"

python -m coverage run -p -m pytest "cw536/test/Whitebox/Branch Testing/Main_test.py"
python -m coverage run -p -m pytest "cw536/test/Whitebox/Statement Testing/User_test.py"
python -m coverage run -p -m pytest "cw536/test/Whitebox/Statement Testing/Film_test.py"


### Combine: 
python -m coverage combine

### Report: 
python -m coverage report -m

## 5. Usage Guidelines:
**Registration:** Passwords for registration must be atleast 6 characters.

**Admin:** Admin can be accessed by registering with the username 'admin'.

## 6. Contributors
Contributions can be seen in the user stories or the report.

