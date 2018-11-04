from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
import csv
from datetime import datetime as dt
import sys

class Webscrape:
    # browser = webdriver.Firefox()
    options = Options()
    options.set_headless(headless=True)
    browser = webdriver.Firefox(firefox_options=options, executable_path=r'C:/Users/com93/Desktop/geckodriver.exe') #C Change executable_path in order to use geckodriver
    url = 'http://stats.ncaa.org/teams/312390'

    browser.get(url)
    browser.maximize_window()

    # date = dt.today().strftime("%m/%d/%Y")
    opponent = ""

    def __init__(self, opponent = "North Carolina"):
        self.opponent = opponent

    # Get last 15 games window
    def getPlayByPlayData(self, elementNum, opp_win):
        for game in range(elementNum - 15, elementNum):
            element = self.browser.find_element_by_xpath("//*[@id=\"contentarea\"]/table/tbody/tr/td[1]/table/tbody/tr[" + str(game) + "]/td[1]")
            currDate = element.text
            element = self.browser.find_element_by_xpath("//*[@id=\"contentarea\"]/table/tbody/tr/td[1]/table/tbody/tr[" + str(game) + "]/td[3]/a")
            element.send_keys(Keys.SHIFT + Keys.RETURN)
            sleep(5)
            self.browser.switch_to_window([win for win in self.browser.window_handles if win !=opp_win][0]) # switch to new window

            #Do scraping here
            element = self.browser.find_element_by_xpath("//*[@id=\"root\"]/li[3]/a") # play by play element
            element.click()
            sleep(3)

            # whether the opponent attributes are on the left side or the right side
            element = self.browser.find_element_by_xpath("//*[@id=\"contentarea\"]/table[6]/tbody/tr[1]/td[1]")
            num = 1
            if (element.text != self.opponent):
                num = 3

            element = self.browser.find_elements_by_xpath("//*[@id=\"contentarea\"]/table[1]/tbody/tr[1]/td") # to find how many innings

            # get play by play strings for the opponent
            for inning in range(0, (len(element) - 4) * 2 + 1, 2):
                element = self.browser.find_elements_by_xpath("//*[@id=\"contentarea\"]/table[" + str(6 + inning) + "]/tbody/tr")

                for e in element:
                    if e.get_attribute("class") != "grey_heading":
                        tdText = e.find_element_by_xpath(".//td[" + str(num) + "]").text
                        if tdText != "":
                            # print(tdText)
                            with open(self.opponent.replace(" ", "_") + '_play_by_play.csv', 'a', encoding='UTF-8', newline = '') as outfile:
                                w = csv.writer(outfile)
                                w.writerow({tdText.replace(",", "?")}) # need to replace commas with spaces because it's csv

            self.browser.close() # close new window
            self.browser.switch_to_window(opp_win) # switch back to main window

    # Get opponent's team stats - hitting
    def getOverallHittingStat(self):
        with open(self.opponent.replace(" ", "_") + '_team_stats_hitting.csv', 'a', encoding='UTF-8', newline = '') as outfile:
            w = csv.writer(outfile)
            w.writerow(["Jersey", "Player", "Yr", "Pos", "GP", "GS", "GS", "G", "BA", "OBPct", "SlgPct", "AB", "R", "H", "2B", "3B", "TB", "HR", "IBB", "BB", "HBP", "RBI", "SF", "SH",  "K", "KL", "DP", "GDP", "TP", "SB", "CS", "Picked", "GO", "FO", "WOBA"])

        element = self.browser.find_element_by_xpath("//*[@id=\"contentarea\"]/table/tbody/tr/td[2]/table[2]/tbody/tr[13]/td/a")
        element.click()
        sleep(3)

        element = self.browser.find_elements_by_xpath("//*[@id=\"stat_grid\"]/tbody/tr")
        for row in element:
            if row.find_element_by_xpath(".//td[12]/div").text != "":
                column = row.find_elements_by_xpath(".//td")
                values = []
                for c in column:
                    values.append(c.text)

                slug = row.find_element_by_xpath(".//td[11]/div").text
                obp = row.find_element_by_xpath(".//td[10]/div").text
                if slug != "" and obp != "":
                    values.append("%.3f" % ((float(slug)+(float(obp)*2))/3))
                else:
                    values.append("")

                with open(self.opponent.replace(" ", "_") + '_team_stats_hitting.csv', 'a', encoding='UTF-8', newline = '') as outfile:
                    w = csv.writer(outfile)
                    w.writerow(values)

    # Get stats vs. LHP
    def getLHPHittingStat(self):
        with open(self.opponent.replace(" ", "_") + '_team_stats_hitting_LHP.csv', 'a', encoding='UTF-8', newline = '') as outfile:
            w = csv.writer(outfile)
            w.writerow(["Jersey", "Player", "Yr", "Pos", "GP", "GS", "GS", "G", "BA", "OBPct", "SlgPct", "AB", "R", "H", "2B", "3B", "TB", "HR", "IBB", "BB", "HBP", "RBI", "SF", "SH",  "K", "KL", "DP", "GDP", "TP", "SB", "CS", "Picked", "GO", "FO", "WOBA"])

        element = self.browser.find_element_by_xpath("//*[@id=\"available_stat_id\"]/option[4]")
        element.click()
        sleep(3)

        element = self.browser.find_elements_by_xpath("//*[@id=\"stat_grid\"]/tbody/tr")
        for row in element:
            column = row.find_elements_by_xpath(".//td")
            values = []
            for c in column:
                values.append(c.text)

            slug = row.find_element_by_xpath(".//td[11]/div").text
            obp = row.find_element_by_xpath(".//td[10]/div").text
            if slug != "" and obp != "":
                values.append("%.3f" % ((float(slug)+(float(obp)*2))/3))

            with open(self.opponent.replace(" ", "_") + '_team_stats_hitting_LHP.csv', 'a', encoding='UTF-8', newline = '') as outfile:
                w = csv.writer(outfile)
                w.writerow(values)

    # Get stats vs. RHP
    def getRHPHittingStat(self):
        with open(self.opponent.replace(" ", "_") + '_team_stats_hitting_RHP.csv', 'a', encoding='UTF-8', newline = '') as outfile:
            w = csv.writer(outfile)
            w.writerow(["Jersey", "Player", "Yr", "Pos", "GP", "GS", "GS", "G", "BA", "OBPct", "SlgPct", "AB", "R", "H", "2B", "3B", "TB", "HR", "IBB", "BB", "HBP", "RBI", "SF", "SH",  "K", "KL", "DP", "GDP", "TP", "SB", "CS", "Picked", "GO", "FO", "WOBA"])

        element = self.browser.find_element_by_xpath("//*[@id=\"available_stat_id\"]/option[5]")
        element.click()
        sleep(3)

        element = self.browser.find_elements_by_xpath("//*[@id=\"stat_grid\"]/tbody/tr")
        for row in element:
            column = row.find_elements_by_xpath(".//td")
            values = []
            for c in column:
                values.append(c.text)

            slug = row.find_element_by_xpath(".//td[11]/div").text
            obp = row.find_element_by_xpath(".//td[10]/div").text
            if slug != "" and obp != "":
                values.append("%.3f" % ((float(slug)+(float(obp)*2))/3))

            with open(self.opponent.replace(" ", "_") + '_team_stats_hitting_RHP.csv', 'a', encoding='UTF-8', newline = '') as outfile:
                w = csv.writer(outfile)
                w.writerow(values)

    # Get opponent's team stats - pitching
    def getOverallPitchingStat(self):
        with open(self.opponent.replace(" ", "_") + '_team_stats_pitching.csv', 'a', encoding='UTF-8', newline = '') as outfile:
            w = csv.writer(outfile)
            w.writerow(["Jersey", "Player", "Yr", "Pos", "GP", "GS", "ERA", "IP", "HA", "R", "ER", "BB", "SO", "SHO", "BF", "P-OAB", "2B-A", "3B-A", "HR-A", "CSO", "WP", "BK", "HB", "KL", "IBB", "CG", "Inh Run", "Inh Run Score", "SHA", "SFA", "CIA", "GO", "FO", "W", "L", "SV"])

        element = self.browser.find_element_by_xpath("//*[@id=\"stats_div\"]/table[1]/tbody/tr/td[2]/a")
        element.click()
        sleep(3)

        element = self.browser.find_elements_by_xpath("//*[@id=\"stat_grid\"]/tbody/tr")
        for row in element:
            if row.find_element_by_xpath(".//td[7]/div").text != "":
                column = row.find_elements_by_xpath(".//td")
                values = []
                for c in column:
                    values.append(c.text)
                with open(self.opponent.replace(" ", "_") + '_team_stats_pitching.csv', 'a', encoding='UTF-8', newline = '') as outfile:
                    w = csv.writer(outfile)
                    w.writerow(values)

    def getLHBPitchingStat(self):
        # Get stats vs. LHB
        with open(self.opponent.replace(" ", "_") + '_team_stats_pitching_LHB.csv', 'a', encoding='UTF-8', newline = '') as outfile:
            w = csv.writer(outfile)
            w.writerow(["Jersey", "Player", "Yr", "Pos", "GP", "GS", "App", "GS", "ERA", "IP", "HA", "R", "ER", "BB", "SO", "SHO", "BF", "P-OAB", "2B-A", "3B-A", "HR-A", "CSO", "WP", "BK", "HB", "KL", "IBB", "CG", "Inh Run", "Inh Run Score", "SHA", "SFA", "CIA", "GO", "FO", "W", "L", "SV"])

        element = self.browser.find_element_by_xpath("//*[@id=\"available_stat_id\"]/option[4]")
        element.click()
        sleep(3)

        element = self.browser.find_elements_by_xpath("//*[@id=\"stat_grid\"]/tbody/tr")
        for row in element:
            column = row.find_elements_by_xpath(".//td")
            values = []
            for c in column:
                values.append(c.text)
            with open(self.opponent.replace(" ", "_") + '_team_stats_pitching_LHB.csv', 'a', encoding='UTF-8', newline = '') as outfile:
                w = csv.writer(outfile)
                w.writerow(values)

    def getRHBPitchingStat(self):
        # Get stats vs. RHB
        with open(self.opponent.replace(" ", "_") + '_team_stats_pitching_RHB.csv', 'a', encoding='UTF-8', newline = '') as outfile:
            w = csv.writer(outfile)
            w.writerow(["Jersey", "Player", "Yr", "Pos", "GP", "GS", "App", "GS", "ERA", "IP", "HA", "R", "ER", "BB", "SO", "SHO", "BF", "P-OAB", "2B-A", "3B-A", "HR-A", "CSO", "WP", "BK", "HB", "KL", "IBB", "CG", "Inh Run", "Inh Run Score", "SHA", "SFA", "CIA", "GO", "FO", "W", "L", "SV"])

        element = self.browser.find_element_by_xpath("//*[@id=\"available_stat_id\"]/option[11]")
        element.click()
        sleep(3)

        element = self.browser.find_elements_by_xpath("//*[@id=\"stat_grid\"]/tbody/tr")
        for row in element:
            column = row.find_elements_by_xpath(".//td")
            values = []
            for c in column:
                values.append(c.text)
            with open(self.opponent.replace(" ", "_") + '_team_stats_pitching_RHB.csv', 'a', encoding='UTF-8', newline = '') as outfile:
                w = csv.writer(outfile)
                w.writerow(values)

    # Get opponent's team stats - fielding
    def getFieldingStat(self):
        with open(self.opponent.replace(" ", "_") + '_team_stats_fielding.csv', 'a', encoding='UTF-8', newline = '') as outfile:
            w = csv.writer(outfile)
            w.writerow(["Jersey", "Player", "Yr", "Pos", "GP", "GS", "GS", "PO", "A", "E", "FldPct", "CI", "PB", "SBA", "CSB", "TC", "IDP", "ITP"])

        element = self.browser.find_element_by_xpath("//*[@id=\"stats_div\"]/table[1]/tbody/tr/td[3]/a")
        element.click()
        sleep(3)

        element = self.browser.find_elements_by_xpath("//*[@id=\"stat_grid\"]/tbody/tr")
        for row in element:
            column = row.find_elements_by_xpath(".//td")
            values = []
            for c in column:
                values.append(c.text)
            with open(self.opponent.replace(" ", "_") + '_team_stats_fielding.csv', 'a', encoding='UTF-8', newline = '') as outfile:
                w = csv.writer(outfile)
                w.writerow(values)

    def createData(self):
        try:
            # Input data
            date = dt.strptime("04/05/2018", "%m/%d/%Y") # will be today's date
            currDate = dt.strptime("01/01/1970", "%m/%d/%Y")
            # Find the game that matches desired date
            elementFromText = ""
            elementNum = 2
            while date > currDate or self.opponent != elementFromText:
                elementNum += 1
                element = self.browser.find_element_by_xpath("//*[@id=\"contentarea\"]/table/tbody/tr/td[1]/table/tbody/tr[" + str(elementNum) + "]/td[1]")
                currDate = dt.strptime(element.text, "%m/%d/%Y")
                elementFromText = self.browser.find_element_by_xpath("//*[@id=\"contentarea\"]/table/tbody/tr/td[1]/table/tbody/tr[" + str(elementNum) + "]/td[2]/a").text
                elementFromText, nextLine, neutralLocation = elementFromText.partition('\n')
                elementFromText = elementFromText.replace("@ ", "")

            date = currDate
            # # Open the self.opponent team's webpage
            element = self.browser.find_element_by_xpath("//*[@id=\"contentarea\"]/table/tbody/tr/td[1]/table/tbody/tr[" + str(elementNum) + "]/td[2]/a")
            # self.opponent = element.text
            # self.opponent, nextLine, neutralLocation = element.text.partition('\n')
            # self.opponent = self.opponent.replace("@ ", "")

            element.click()
            sleep(3)

            opp_win = self.browser.current_window_handle # Opponent window

            # Find past 15 games played by the opponent
            currDate = dt.strptime("01/01/1970", "%m/%d/%Y")
            # Find the game that matches desired date
            elementNum = 2
            while date > currDate:
                elementNum += 1
                element = self.browser.find_element_by_xpath("//*[@id=\"contentarea\"]/table/tbody/tr/td[1]/table/tbody/tr[" + str(elementNum) + "]/td[1]")
                currDate = dt.strptime(element.text, "%m/%d/%Y")

            self.getPlayByPlayData(elementNum, opp_win)

            self.getOverallHittingStat()

            self.getLHPHittingStat()

            self.getRHPHittingStat()

            self.getOverallPitchingStat()

            self.getLHBPitchingStat()

            self.getRHBPitchingStat()

            self.getFieldingStat()

        except Exception as e:
            print(e)
            self.browser.quit()
        self.browser.quit()