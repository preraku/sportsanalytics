from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
import csv

# browser = webdriver.Firefox()
options = Options()
options.set_headless(headless=True)
browser = webdriver.Firefox(firefox_options=options, executable_path=r'C:/Users/com93/Desktop/geckodriver.exe') #C Change executable_path in order to use geckodriver
url = 'http://stats.ncaa.org/teams/312390'

try:
    browser.get(url)
    browser.maximize_window()

    # Input data
    opponent = "Boston College"
    date = "05/04/2018"
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
    sleep(8)

    opp_win = browser.current_window_handle # Opponent window

    # Find past 15 games played by the opponent
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
        element = browser.find_element_by_xpath("//*[@id=\"contentarea\"]/table/tbody/tr/td[1]/table/tbody/tr[" + str(game) + "]/td[3]/a")
        element.send_keys(Keys.SHIFT + Keys.RETURN)
        sleep(5)
        browser.switch_to_window([win for win in browser.window_handles if win !=opp_win][0]) # switch to new window

        #Do scraping here
        element = browser.find_element_by_xpath("//*[@id=\"root\"]/li[3]/a") # play by play element
        element.click()
        sleep(3)

        # whether the opponent attributes are on the left side or the right side
        element = browser.find_element_by_xpath("//*[@id=\"contentarea\"]/table[6]/tbody/tr[1]/td[1]")
        num = 1
        if (element.text != opponent):
            num = 3

        element = browser.find_elements_by_xpath("//*[@id=\"contentarea\"]/table[1]/tbody/tr[1]/td") # to find how many innings

        # get play by play strings for the opponent
        for inning in range(0, (len(element) - 4) * 2 + 1, 2):
            element = browser.find_elements_by_xpath("//*[@id=\"contentarea\"]/table[" + str(6 + inning) + "]/tbody/tr")

            for e in element:
                if e.get_attribute("class") != "grey_heading":
                    tdText = e.find_element_by_xpath(".//td[" + str(num) + "]").text
                    if tdText != "":
                        # print(tdText)
                        with open(opponent.replace(" ", "_") + '_play_by_play.csv', 'a', encoding='UTF-8', newline = '') as outfile:
                            w = csv.writer(outfile)
                            w.writerow({tdText.replace(",", "?")}) # need to replace commas with spaces because it's csv

        browser.close() # close new window
        browser.switch_to_window(opp_win) # switch back to main window

    # Get opponent's team stats - hitting
    with open(opponent.replace(" ", "_") + '_team_stats_hitting.csv', 'a', encoding='UTF-8', newline = '') as outfile:
        w = csv.writer(outfile)
        w.writerow(["Jersey", "Player", "Yr", "Pos", "GP", "GS", "GS", "G", "BA", "OBPct", "SlgPct", "AB", "R", "H", "2B", "3B", "TB", "HR", "IBB", "BB", "HBP", "RBI", "SF", "SH",  "K", "KL", "DP", "GDP", "TP", "SB", "CS", "Picked", "GO", "FO"])

    element = browser.find_element_by_xpath("//*[@id=\"contentarea\"]/table/tbody/tr/td[2]/table[2]/tbody/tr[13]/td/a")
    element.click()
    sleep(3)

    element = browser.find_elements_by_xpath("//*[@id=\"stat_grid\"]/tbody/tr")
    for row in element:
        if row.find_element_by_xpath(".//td[12]/div").text != "":
            column = row.find_elements_by_xpath(".//td")
            values = []
            for c in column:
                values.append(c.text)
            with open(opponent.replace(" ", "_") + '_team_stats_hitting.csv', 'a', encoding='UTF-8', newline = '') as outfile:
                w = csv.writer(outfile)
                w.writerow(values)

    # Get opponent's team stats - pitching
    with open(opponent.replace(" ", "_") + '_team_stats_pitching.csv', 'a', encoding='UTF-8', newline = '') as outfile:
        w = csv.writer(outfile)
        w.writerow(["Jersey", "Player", "Yr", "Pos", "GP", "GS", "ERA", "IP", "HA", "R", "ER", "BB", "SO", "SHO", "BF", "P-OAB", "2B-A", "3B-A", "HR-A", "CSO", "WP", "BK", "HB", "KL", "IBB", "CG", "Inh Run", "Inh Run Score", "SHA", "SFA", "CIA", "GO", "FO", "W", "L", "SV"])

    element = browser.find_element_by_xpath("//*[@id=\"stats_div\"]/table[1]/tbody/tr/td[2]/a")
    element.click()
    sleep(3)

    element = browser.find_elements_by_xpath("//*[@id=\"stat_grid\"]/tbody/tr")
    for row in element:
        if row.find_element_by_xpath(".//td[7]/div").text != "":
            column = row.find_elements_by_xpath(".//td")
            values = []
            for c in column:
                values.append(c.text)
            with open(opponent.replace(" ", "_") + '_team_stats_pitching.csv', 'a', encoding='UTF-8', newline = '') as outfile:
                w = csv.writer(outfile)
                w.writerow(values)

    # Get opponent's team stats - fielding
    with open(opponent.replace(" ", "_") + '_team_stats_fielding.csv', 'a', encoding='UTF-8', newline = '') as outfile:
        w = csv.writer(outfile)
        w.writerow(["Jersey", "Player", "Yr", "Pos", "GP", "GS", "GS", "PO", "A", "E", "FldPct", "CI", "PB", "SBA", "CSB", "TC", "IDP", "ITP"])

    element = browser.find_element_by_xpath("//*[@id=\"stats_div\"]/table[1]/tbody/tr/td[3]/a")
    element.click()
    sleep(3)

    element = browser.find_elements_by_xpath("//*[@id=\"stat_grid\"]/tbody/tr")
    for row in element:
        column = row.find_elements_by_xpath(".//td")
        values = []
        for c in column:
            values.append(c.text)
        with open(opponent.replace(" ", "_") + '_team_stats_fielding.csv', 'a', encoding='UTF-8', newline = '') as outfile:
            w = csv.writer(outfile)
            w.writerow(values)

except Exception as e:
    print(e)
    browser.quit()
browser.quit()