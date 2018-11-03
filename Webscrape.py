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
        # print(currDate)

    # Open a new browser for opponent team
    cur_win = browser.current_window_handle # Georgia Tech window
    element = browser.find_element_by_xpath("//*[@id=\"contentarea\"]/table/tbody/tr/td[1]/table/tbody/tr[" + str(elementNum) + "]/td[2]/a")
    element.send_keys(Keys.SHIFT + Keys.RETURN)
    sleep(15)
    browser.switch_to_window([win for win in browser.window_handles if win !=cur_win][0]) # switch to new window

    # Find past 15 games played by the opponent
    date = "05/10/2018"
    currDate = ""
    # Find the game that matches desired date
    elementNum = 2
    while date != currDate:
        elementNum += 1
        element = browser.find_element_by_xpath("//*[@id=\"contentarea\"]/table/tbody/tr/td[1]/table/tbody/tr[" + str(elementNum) + "]/td[1]")
        currDate = element.text

    # Get last 15 games
    for game in range(elementNum - 15, elementNum):
        element = browser.find_element_by_xpath("//*[@id=\"contentarea\"]/table/tbody/tr/td[1]/table/tbody/tr[" + str(game) + "]/td[1]")
        currDate = element.text



    # numMatch = 0

    # for year in range(1, 3):
    #     element = browser.find_element_by_xpath("//*[@id=\"date-config\"]")
    #     # element.click()
    #     browser.execute_script("arguments[0].click();", element)

    #     element = browser.find_element_by_xpath("//*[@id=\"date-config\"]/div[1]/div/table/tbody/tr/td[1]/div/table/tbody/tr[" + str(year) + "]/td")
    #     # element.click()
    #     browser.execute_script("arguments[0].click();", element)

    #     for month in range(1, 6):
    #         if year == 1 and month == 1:
    #             element = browser.find_element_by_xpath("//*[@id=\"date-config\"]/div[1]/div/table/tbody/tr/td[2]/div/table/tbody/tr[2]/td[4]")
    #             # element.click()
    #             browser.execute_script("arguments[0].click();", element)
    #         elif year == 1:
    #             element = browser.find_element_by_xpath("//*[@id=\"date-config\"]/div[1]/div/table/tbody/tr/td[2]/div/table/tbody/tr[3]/td[" + str(month-1) +"]")
    #             # element.click()
    #             browser.execute_script("arguments[0].click();", element)
    #         elif year == 2 and month != 5:
    #             element = browser.find_element_by_xpath("//*[@id=\"date-config\"]/div[1]/div/table/tbody/tr/td[2]/div/table/tbody/tr[1]/td[" + str(month) + "]")
    #             # element.click()
    #             browser.execute_script("arguments[0].click();", element)
    #         else:
    #             element = browser.find_element_by_xpath("//*[@id=\"date-config\"]/div[1]/div/table/tbody/tr/td[2]/div/table/tbody/tr[2]/td[1]")
    #             # element.click()
    #             browser.execute_script("arguments[0].click();", element)

    #         sleep(3)
    #         currMatches = browser.find_elements_by_class_name("result")

    #         cur_win = browser.current_window_handle # get current/main window

    #         for match in currMatches:

    #             matchLink = match.find_elements_by_tag_name("a")
    #             for link in matchLink:
    #                 # link.click()
    #                 link.send_keys(Keys.SHIFT + Keys.RETURN)
    #                 sleep(10)
    #             # Open the link in a new window by sending key strokes on the element
    #             # match.send_keys(Keys.COMMAND + 't')

    #             # Get windows list and put focus on new window (which is on the 1st index in the list)
    #             # windows = browser.window_handles
    #             # browser.switch_to.window(windows[1])

    #             browser.switch_to_window([win for win in browser.window_handles if win !=cur_win][0]) # switch to new window

    #             element = browser.find_element_by_xpath("//*[@id=\"live-match-options\"]/li[3]/a")
    #             browser.execute_script("arguments[0].click();", element)
    #             # time.sleep(5)

    #             home = {};
    #             away = {};

    #             search =  browser.find_element_by_xpath("//*[@id=\"match-centre-header\"]/div[1]/div[2]/a") # home name
    #             home['Name'] = search.text

    #             search =  browser.find_element_by_xpath("//*[@id=\"match-centre-header\"]/div[1]/div[2]/div[3]") # home formation
    #             home['Formation'] = search.text

    #             search =  browser.find_element_by_xpath("//*[@id=\"match-centre-header\"]/div[3]/div[2]/a") # away name
    #             away['Name'] = search.text

    #             search =  browser.find_element_by_xpath("//*[@id=\"match-centre-header\"]/div[3]/div[2]/div[3]") # away formation
    #             away['Formation'] = search.text

    #             for i in range(1, 17):
    #                 element = browser.find_element_by_xpath("//*[@id=\"event-type-filters\"]/li[" + str(i) + "]")
    #                 browser.execute_script("arguments[0].click();", element)

    #                 title = browser.find_element_by_xpath("//*[@id=\"event-type-filters\"]/li[" + str(i) + "]/a/h4") # title
    #                 search = browser.find_element_by_xpath("//*[@id=\"event-type-filters\"]/li[" + str(i) + "]/a/div/span[1]") # home attribute
    #                 home[title.text] = search.text

    #                 search = browser.find_element_by_xpath("//*[@id=\"event-type-filters\"]/li[" + str(i) + "]/a/div/span[3]") # away attribute
    #                 away[title.text] = search.text

    #                 if i == 1:
    #                     home["Goals"] = browser.find_element_by_xpath("//*[@id=\"chalkboard\"]/div[2]/div[1]/div[2]/div[2]/span[1]").text
    #                     home["Shots on Target"] = browser.find_element_by_xpath("//*[@id=\"chalkboard\"]/div[2]/div[1]/div[2]/div[3]/span[1]").text

    #                     away["Goals"] = browser.find_element_by_xpath("//*[@id=\"chalkboard\"]/div[2]/div[1]/div[2]/div[2]/span[2]").text
    #                     away["Shots on Target"] = browser.find_element_by_xpath("//*[@id=\"chalkboard\"]/div[2]/div[1]/div[2]/div[3]/span[2]").text

    #                     if int(home["Goals"]) > int(away["Goals"]):
    #                         home["Result"] = 3
    #                         away["Result"] = 0
    #                     elif int(home["Goals"]) < int(away["Goals"]):
    #                         home["Result"] = 0
    #                         away["Result"] = 3
    #                     else:
    #                         home["Result"] = 1
    #                         away["Result"] = 1
    #         # //*[@id="chalkboard-timeline"]/div[1]/div[2]/div
    #         # //*[@id="chalkboard-timeline"]/div[1]/div[3]/div[1]
    #         # //*[@id="chalkboard-timeline"]/div[1]/div[3]/div[2]
    #                 # search = browser.find_element_by_xpath("//*[@id=\"chalkboard-timeline\"]/div[3]/div[1]/div")
    #                 # print(search.get_attribute('data-minute'))

    #             print(home)
    #             print(away)
    #             with open('epl1718.csv', 'a', newline = '') as outfile:
    #                 w = csv.writer(outfile)
    #                 if numMatch == 0:
    #                     w.writerow(home.keys())
    #                 w.writerow(home.values())
    #                 w.writerow(away.values())

    #             numMatch = numMatch + 1
    #             browser.close() # close new window
    #             browser.switch_to_window(cur_win) # switch back to main window

except Exception as e:
    print(e)
    browser.quit()
browser.quit()