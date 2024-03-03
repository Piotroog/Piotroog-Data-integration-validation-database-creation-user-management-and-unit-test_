## Data integration, validation, database creation, user management and unit test 

### Summary 
This project is designed to demonstrate expertise in Python programming, particularly in data processing and management.
The task involved several challenging components:
- Data Integration: A script was developed to merge and process data from various file formats, including JSON, CSV, and 
XML. This enabled the creation of a comprehensive and unified database from diverse data sources.
- Data Validation: A vital part of the project was to implement a script for stringent data validation. This script was 
tailored to the specific requirements of the task, encompassing the validation of email addresses, formatting of
telephone numbers, and the identification and removal of duplicate records.
- Database Creation: The project included the development of a script to establish an SQLite database. This database was
utilized for storing all the validated records, thus creating a robust foundation for the subsequent data operations.
- User Management CLI Script: A significant feature of the project was the creation of a Command Line Interface (CLI) 
program. This script was designed to facilitate various operations on the database, in line with the task requirements.
Key functionalities included displaying user account information, grouping children by age, and other specific features 
for user and admin roles.
- Unit Testing: To ensure the reliability and correctness of the program's methods, a comprehensive set of unit tests 
was developed. These tests were executed using a test database, covering all the critical functionalities of the program.

## Manual of using 

### Clone the repository
`git clone https://github.com/Piotroog/Piotroog-Data-integration-validation-database-creation-user-management-and-unit-test_ `
### Create environment
`python -m venv (env_name)`

### Activate environment
`.\env_name\Scripts\activate`
or
`source env_name/bin/activate`

### Install pandas on local environment
`pip install pandas`

### Run data_marge script
`python data_merge.py`
That script merges data from different types of file (JSON, XML and CSV) in one JSON file.

### Run data_validation script
`python data_validation.py`
That script validates data in merged file (corrects data and deletes duplicated records)

### Run database_creator script
`python database_creator.py`
That script creates database according to validated data in the  JSON file

### Run main script file
There is possibility to log in with 2 options: with admin login and password or as a user. 
Admin can: 
1. Print The Number of All Valid Accounts (used example login and password from database)
`python user_manager.py --login lowerykimberly@example.net --password '6mKY!nP^+y' --command print-all-accounts`
2. Print The Longest Existing Account (used example login and password from database)
`python user_manager.py --login lowerykimberly@example.net --password '6mKY!nP^+y' --command print-oldest-account`
3. Group Children by Age (used example login and password from database)
`python user_manager.py --login lowerykimberly@example.net --password '6mKY!nP^+y' --command group-by-age`
User can:
1. Print Children (used example login and password from database)
`python user_manager.py --login lowerykimberly@example.net --password '6mKY!nP^+y' --command print-children`
2. Find Users with Children of Same Age (used example login and password from database)
`python user_manager.py --login lowerykimberly@example.net --password '6mKY!nP^+y' --command find-similar-children-by-age`

### Unit test script file
There is possibility to check if the main functions from files are correct with unit test script. 
It allows to create test database and test functionality of user_manager.py script
`python test.py`
