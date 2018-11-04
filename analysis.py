import re
import csv
import sys
import Webscrape
import os

class Analysis:
    players = {}
    inpArr = []
    team = ""

    def __init__(self, team = "North Carolina"):
        self.scrapeSite(team)
        self.team = team
        location = team.replace(" ", "_") + '_play_by_play.csv'
        self.loadData(location)

    def scrapeSite(self, team):
        scraper = Webscrape.Webscrape(team)
        scraper.createData()

    def makeMyDir(self, name):
        try:
            os.makedirs(name)
        except OSError:
            pass

    def writeToCSV(self):
        fields = ["center", "left", "right", "first", "second", "third", "N/A", "to ss", "to pitcher"]
        rows = ["singled", "doubled", "tripled", "homered", "popped", "lined", "flied", "grounded", "at bat", "walked", "out", "advanced", "scored"]

        self.makeMyDir("./" + self.team.replace(" ", "_"))

        with open("./" + self.team.replace(" ", "_") + "/players.csv", "w", newline='') as f:
            names = csv.writer(f, delimiter=",")
            names.writerow(['Name'])
            for name in self.players:
                names.writerow([name])

        for name in self.players:
            with open("./" + self.team.replace(" ", "_") + "/" + name.replace(". ", "_") + ".csv", "w", newline='') as f:
                writer = csv.writer(f, delimiter=',')
                writer.writerow(["x"] + fields)
                for row in rows:
                    if type(self.players[name][row]) is int:
                        temp = [row, self.players[name][row]]
                    else:
                        temp = [row] + list(self.players[name][row].values())
                    writer.writerow(temp)

    def loadData(self, location):
        f = open(location)
        csv_f = csv.reader(f)

        for row in csv_f:
            self.inpArr.append(row[0])

    def analyze(self):
        nonBats = ["stole", "advanced"]
        for action in self.inpArr:
            action = action.replace("; ", ";").replace("3a ", ';')
            for string in action.split(";"):
                name = self.getName(string)
                typeInt, typeString = self.getType(string)
                location = self.getLocation(string)
                if typeInt is not 2:
                    if name not in self.players:
                        self.players[name] = {"singled":
                                                  {"center": 0, "left": 0, "right": 0, "first": 0, "second": 0, "third": 0, "N/A": 0, "to ss": 0, "to pitcher": 0},
                                              "doubled":
                                                  {"center": 0, "left": 0, "right": 0, "first": 0, "second": 0, "third": 0, "N/A": 0, "to ss": 0, "to pitcher": 0},
                                              "tripled":
                                                  {"center": 0, "left": 0, "right": 0, "first": 0, "second": 0, "third": 0, "N/A": 0, "to ss": 0, "to pitcher": 0},
                                              "homered":
                                                  {"center": 0, "left": 0, "right": 0, "first": 0, "second": 0, "third": 0, "N/A": 0, "to ss": 0, "to pitcher": 0},
                                              "stole":
                                                  {"center": 0, "left": 0, "right": 0, "first": 0, "second": 0, "third": 0, "N/A": 0},
                                              "scored": 0,
                                              "advanced": 0,
                                              "walked": 0,
                                              "out": 0,
                                              "popped":
                                                  {"center": 0, "left": 0, "right": 0, "first": 0, "second": 0, "third": 0, "N/A": 0, "to ss": 0, "to pitcher": 0},
                                              "lined":
                                                  {"center": 0, "left": 0, "right": 0, "first": 0, "second": 0, "third": 0, "N/A": 0, "to ss": 0, "to pitcher": 0},
                                              "flied":
                                                  {"center": 0, "left": 0, "right": 0, "first": 0, "second": 0, "third": 0, "N/A": 0, "to ss": 0, "to pitcher": 0},
                                              "grounded":
                                                  {"center": 0, "left": 0, "right": 0, "first": 0, "second": 0, "third": 0, "N/A": 0, "to ss": 0, "to pitcher": 0},
                                              "at bat": 0}
                    if typeInt == 0:
                        self.players[name][typeString][location] += 1
                    elif typeInt == 1:
                        self.players[name][typeString] += 1
                    if typeString not in nonBats:
                        self.players[name]["at bat"] += 1

            # cross reference names against list of players on that team

    '''
        0 = has location
        1 = doesnt have location
        2 = irrelevant
    '''
    def getType(self, string):
        location = ["singled", "doubled", "tripled", "homered", "popped", "flied", "lined", "grounded", "stole"]
        noLocation = ["scored", "out", "walked", "advanced"]

        for loc in location:
            if loc in string:
                tup = (0, loc)
                return tup
        for no in noLocation:
            if no in string:
                tup = (1, no)
                return tup
        if "hit by" in string:
            tup = (1, "walked")
            return tup

        tup = (2, "N/A")
        return tup

    '''
        0 = center
        1 = left
        2 = right
        3 = infield
        4 = no location given
    '''
    def getLocation(self, string):
        ret = "N/A"
        center = ["centerfield", " c", "center", "cf"]
        left = ["left", "lf"]
        right = ["right", "rf"]
        first = ["first", "1b"]
        second = ["second", "2b"]
        third = ["third", "3b"]
        ss = ['ss']
        top = ["to p"]

        for c in center:
            if c in string:
                return "center"
        for l in left:
            if l in string:
                return "left"
        for r in right:
            if r in string:
                return "right"
        for f in first:
            if f in string:
                return "first"
        for s in second:
            if s in string:
                return "second"
        for t in third:
            if t in string:
                return "third"
        for short in ss:
            if short in string:
                return "to ss"
        for pit in top:
            if pit in string:
                return "to pitcher"
        return ret


    def getName(self, string):
        if string[-1] == '.':
            string = string[:-1]

        string = string.replace(". ", ".").replace("? ", "?")
        name = string.split()[0]

        if '.' in name:
            name = name.split('.')
            name = name[0] + '. ' + name[1].capitalize()
        if '?' in name:
            name = name.split('?')
            name = name[1][0] + '. ' + name[0].capitalize()
        else:
            name = name.capitalize()

        return name

    def printPlayers(self):
        for key in self.players:
            print(key, self.players[key])


team = sys.argv[1]
analysis = Analysis(team)
analysis.analyze()
analysis.writeToCSV()
