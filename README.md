### Test Automation Documentation ###

Introduction

    


## What is this repository for? ##

* Quick summary:

    This test automation is based on "behave - BDD" to run test. It uses selenium for browser automation and python request for testing api requests. For reporting, it utilizes Allure reporting and behave-html report formatter. Here are some link for further reading. 

* [Learn Markdown]
* https://behave.readthedocs.io/en/latest/
* https://pypi.org/project/allure-behave/
*  https://pypi.org/project/behave-html-formatter/

### How do I get set up? ###

After cloning this repo, you need to create/activate venv

    python3 -m venv venv
    source venv/bin/activate

if needed please install python 3.11 and up

    https://www.python.org/downloads/release/python-3119/

Now you need to install dependencies

    pip install -r requirements.txt

Before run tests, you need to modify your local react repo's RECAPTCHA key to a test key (site key).

Test key can be found here:

    https://developers.google.com/recaptcha/docs/faq

Please make sure you only change REACT_APP_LOCAL_GOOGLE_RECAPTCHA in react repo's .env file. 

## To set your local address or change environment to stage, prod
Copy and paste .env.example file name it based on which environment's it is, such as .env.local. You want to modify "**BASE_URL**" variable so it has your local address or prod url. Default local address may differ from yours.

### Running tests in headless browser
To use headless browser edit "**BROWSER**" value in .env to 'chrome_headless' or 'safari_headless'.

Also please change the **usernames and passwords** in .env file.

Next make sure these brands are Private in your local:
1. https://www.greenrow.com
2. 	https://www.potterybarn.com - Fashionorlove should be in the whitelist 

This brand should be Inactive:
1. https://www.hawaiianairlines.com


## To run tests, You can use behave commands or make commands:
###Run tests and generate allure html reports using make commands

Runs the default test suite (@smoke) using values from:
* Shell environment variables (if set)
* .env file values
* Makefile fallbacks
    
    make run

Override environment, browser, or tags
  
    ENVIRONMENT=stage BROWSER=remote_chrome TAGS=@regression make run
    TAGS=@ui make run
TAGS should be passed without quotes.

Allure Reports

Generate and serve Allure report
After running tests (which generate allure-results/):

    make results

This will:
   * Stop any existing local report server
   * Generate a fresh report under tests/reports/
   * Serve it at: http://localhost:5555/

Stop server and clean results

    make results-stop

This stops the local server and removes:
   * tests/reports/
   * allure-results/

Running Tests using Behave commands (Optional)
    
    behave -t@smoke -f allure -o allure-results
    allure generate allure-results -o tests/reports
### Tags:
To run specific suite of test, please use following tags

Run smoke tests: Build a link form and api on home page, brands page, tools page against Top 5 brands and a brand from remaining networks

    behave -t@smoke

Run build a link test against Top 5 brand plus a brand from remaining networks : Build a link form and api on home page against Top 5 brands and a brand from remaining networks

    behave -t@top5

Run build a link tests on Home Page: Build a link form and api tests on home page against top 30 brands and their category and product pages. 

    behave -t@build_a_link

Run all frontend tests.
  
    behave -t@ui

Run all backend tests.
  
    behave -t@backend
    
Run build a link tests on Tools Page: Build a link form on Tools Page against top 10 brands and their category and product pages. 

    behave -t@build_a_link_tools_page

#### you can find specific tags in each feature file you want to run. Feature files sits in:
    /tests/features

Every feature and scenario are tagged, and you can use that tag to run that specific feature/scenario. You can find these tags in feature files at tests/features. Each feature is organized by function they test. 


### Common Issues ###
Test doesn't run on Safari browser:

  You need to enable Safari driver 
  
    safaridriver --enable
  
Although tests are written to wait for the web elements, sometimes they still cause synchronization issues. if persists let me know. 
