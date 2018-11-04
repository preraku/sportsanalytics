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
                playType = self.getType(string)
                location = self.getLocation(string)
                print(name + ' ' + playType[1] + ' ' + location[1])
            # cross reference names against list of players on that team

    '''
            0 = center
            1 = left
            2 = right
            3 = infield
            4 = no location given
        '''
    def getLocation(self, string):
        tup = (4, "N/A")
        center = ["centerfield", " c", "center", "cf"]
        left = ["left", "lf"]
        right = ["right", "rf"]
        other = ["third", "second", "first", "ss", "3b", "2b", "1b", " p"]

        for c in center:
            if c in string:
                tup = (0, c)
                return tup
        for l in left:
            if l in string:
                tup = (1, l)
                return tup
        for r in right:
            if r in string:
                tup = (2, r)
                return tup
        for o in other:
            if o in string:
                tup = (3, o)
                return tup

        return False


    '''
        0 = got on base or run
        1 = got out
        2 = not relevant to us
    '''
    def getType(self, string):
        positiveTypes = ["singled", "doubled", "tripled", "homered", "walked", "stole", "advanced"]
        outs = ["out", "popped", "flied", "lined", "grounded", "struck"]
        for hit in positiveTypes:
            if hit in string:
                tup = (0, hit)
                return tup
        for out in outs:
            if out in string:
                tup = (1, out)
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
