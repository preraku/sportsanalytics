import re

class Analysis:
    players = {}
    inpArr = ["Ramsey?K singled to third base (0-1 K).",
              "Wike?T grounded out to 2b (1-1 SB)3a Ramsey?K advanced to third.",
              "Ramsey?K stole second."]

    def analyze(self):
        for action in self.inpArr:
            action = action.replace("; ", ";").replace("3a ", ';')
            for string in action.split(";"):
                name = self.getName(string)
                type = self.getType(string)
                print(type)
                location = self.getLocation(string)
                # if type:
                #     print('good')
                # else:
                #     print('bad')
            # cross reference names against list of players on that team

    def getLocation(self, string):
        return False


    '''
        0 = got on base or run
        1 = got out
        2 = not relevant to us
    '''
    def getType(self, string):
        positiveTypes = ["singled", "doubled", "tripled", "homered", "walked", "stole", "advanced"]
        outs = ["out", "popped", "flied", "lined", "grounded", "struck"]
        for type in positiveTypes:
            if type in string:
                tup = (0, type)
                return tup
        for type in outs:
            if type in string:
                tup = (1, type)
                return tup

        tup = (2, "N/A")
        return tup

    def getName(self, string):
        if string[-1] == '.':
            string = string[:-1]

        string = string.replace(". ", ".").replace("? ", "?")
        name = string.split()[0]

        if '.' in name:
            name = name.split('.')
            name = name[0] + '. ' + name[1].capitalize()
        elif '?' in name:
            name = name.split('?')
            name = name[1][0] + '. ' + name[0].capitalize()
        else:
            name = name.capitalize()

        return name


analysis = Analysis()
analysis.analyze()
