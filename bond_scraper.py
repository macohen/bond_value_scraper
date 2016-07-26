
import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import Select

def format_date(issue_date):
    issue_date_as_date = datetime.strptime(issue_date, "%b-%y")
    return issue_date_as_date.strftime("%m/%y").strip()


def format_currency(denom):
    denom = denom.replace("$", "")
    denom = denom.replace(",", "")
    return denom.strip()

"""
Create a CSV with the headers "SerialNumber", "IssueDate", "Denom"
"""
def run(bond_file, redemption_date):
    with open(bond_file, 'r', encoding='utf-8') as bonds_csv:
        bonds_reader = csv.DictReader(bonds_csv)
        browser = webdriver.Firefox()
        browser.get("https://www.treasurydirect.gov/BC/SBCPrice")
        browser.implicitly_wait(3)

        for idx, row in enumerate(bonds_reader):
            serial_number = row["SerialNumber"]
            issue_date = row["IssueDate"]
            denom = row["Denom"]
            print(row)

            if(len(serial_number.strip()) > 0):
                # does the $ need to be replaced by %?
                browser.find_element_by_name("SBCForm")
                browser.find_element_by_name("SerialNumber").clear()
                browser.find_element_by_name("SerialNumber").send_keys(serial_number)
                browser.find_element_by_name("IssueDate").clear()
                browser.find_element_by_name("IssueDate").send_keys(format_date(issue_date))
                browser.find_element_by_name("RedemptionDate").clear()
                browser.find_element_by_name("RedemptionDate").send_keys(redemption_date)
                Select(browser.find_element_by_name("Denomination")).select_by_value(format_currency(denom))
                browser.find_element_by_name("btnAdd.x").click()

if __name__ == '__main__':
    bond_file = "bonds.csv"
    redemption_date = "11/2016"
    run(bond_file, redemption_date)
