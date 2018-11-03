from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
import csv

# browser = webdriver.Firefox()
options = Options()
options.set_headless(headless=False)
browser = webdriver.Firefox(firefox_options=options, executable_path=r'C:/Users/com93/Desktop/geckodriver.exe')
url = 'http://stats.ncaa.org/teams/312390'

try:
    browser.get(url)
    browser.maximize_window()

    date = "05/10/2018"
    currDate = ""
    # Find the game that matches desired date
    elementNum = 2
    while date != currDate:
        elementNum += 1
        element = browser.find_element_by_xpath("//*[@id=\"contentarea\"]/table/tbody/tr/td[1]/table/tbody/tr[" + str(elementNum) + "]/td[1]")
        currDate = element.text

    # Open the opponent team's webpage
    element = browser.find_element_by_xpath("//*[@id=\"contentarea\"]/table/tbody/tr/td[1]/table/tbody/tr[" + str(elementNum) + "]/td[2]/a")
    element.click()
    sleep(15)

    # Find past 15 games played by the opponent
    date = "05/10/2018"
    currDate = ""
    # Find the game that matches desired date
    elementNum = 2
    while date != currDate:
        elementNum += 1
        element = browser.find_element_by_xpath("//*[@id=\"contentarea\"]/table/tbody/tr/td[1]/table/tbody/tr[" + str(elementNum) + "]/td[1]")
        currDate = element.text

    # Get last 15 games window
    for game in range(elementNum - 15, elementNum):
        element = browser.find_element_by_xpath("//*[@id=\"contentarea\"]/table/tbody/tr/td[1]/table/tbody/tr[" + str(game) + "]/td[1]")
        currDate = element.text
        opp_win = browser.current_window_handle # Opponent window
        element = browser.find_element_by_xpath("//*[@id=\"contentarea\"]/table/tbody/tr/td[1]/table/tbody/tr[" + str(game) + "]/td[3]/a")
        element.send_keys(Keys.SHIFT + Keys.RETURN)
        sleep(5)
        browser.switch_to_window([win for win in browser.window_handles if win !=opp_win][0]) # switch to new window

        browser.close() # close new window
        browser.switch_to_window(opp_win) # switch back to main window

except Exception as e:
    print(e)
    browser.quit()
browser.quit()