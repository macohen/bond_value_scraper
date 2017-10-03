# Bond Value Scraper

I wish there was a way to bulk upload a spreadsheet of bond serial numbers to https://www.treasurydirect.gov/BC/SBCPrice. There isn't. So I wrote a python script with Selenium Webdriver to parse a CSV containing the info needed to fill out the form and run it automatically.

Then, you just need to click save and copy and paste the table back into a spreadsheet for fiddling.

## Run
1. Use Python 3.2+
1. pip install -r requirements.txt
1. Install [geckodriver](https://github.com/mozilla/geckodriver) on your PATH for Firefox support
1. copy your bonds.csv file to the root. don't add it to git, please. I don't want to know
1. python bond_scraper.py --value_as_of=&lt;month and year you want to calculate the value for&gt; --bond_csv=&lt;the file with the list of bonds to calculate&gt;
    * --value_as_of=11/2017
    * --bond_csv=sample_bonds.csv (see included sample_bonds.csv for reference format) 
1. Once the script is done, you should be able to go to the Firefox instance that Selenium opened and save the results as a file
