
import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import argparse

def format_date(issue_date):
    issue_date_as_date = datetime.strptime(issue_date, "%m/01/%Y")
    return issue_date_as_date.strftime("%m/%y").strip()


def format_currency(denom):
    denom = denom.replace("$", "")
    denom = denom.replace(",", "")
    return denom.strip()

"""
Create a CSV with the headers "SerialNumber", "IssueDate", "Denom"
"""
def run(bond_file, redemption_date):
    with open(bond_file, 'r', encoding='utf-8-sig') as bonds_csv:
        bonds_reader = csv.DictReader(bonds_csv)
        driver = webdriver.Firefox()
        driver.get("https://www.treasurydirect.gov/BC/SBCPrice")
        driver.implicitly_wait(30)

        if redemption_date != None:
            send_redemption_date(driver, redemption_date)

        for row in bonds_reader:
            serial_number = row["SerialNumber"]
            issue_date = row["IssueDate"]
            denom = row["Denom"]

            if(len(serial_number.strip()) > 0):
                try:
                    update_denomination(denom, driver)
                    send_serial_number(driver, serial_number)
                    send_issuedate(driver, issue_date)
                    add_bond(driver)
                except ValueError as e:
                    print("Error {1} for value: {0}".format(row, e))

def add_bond(driver):
    driver.find_element_by_name("btnAdd.x").click()

def send_issuedate(driver, issue_date):
    driver.find_element_by_name("IssueDate").clear()
    driver.find_element_by_name("IssueDate").send_keys(format_date(issue_date))


def send_serial_number(driver, serial_number):
    driver.find_element_by_name("SerialNumber").clear()
    driver.find_element_by_name("SerialNumber").send_keys(serial_number)

def update_denomination(denom, driver):
    denom_elem = Select(driver.find_element_by_name("Denomination"))
    denom_elem.select_by_value(format_currency(denom))

def send_redemption_date(driver, redemption_date):
    driver.find_element_by_name("RedemptionDate").clear()
    driver.find_element_by_name("RedemptionDate").send_keys(redemption_date)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--value_as_of', type=str, dest='value_as_of')
    parser.add_argument('--bond_csv', type=str, dest='bond_csv')
    args = parser.parse_args()
    bond_file = args.bond_csv
    value_as_of = args.value_as_of
    run(bond_file, value_as_of)
