import pandas as pd
from itertools import combinations
import re

class CSP:
    def __init__(self):
        self.domain = []
        self.nodes = []
        self.constraints = []
        self.goal = None

    def findNode(self, name):
        for n in self.nodes:
            if n.name == name:
                return n
            
    def getAllNodeNames(self):
        res = []
        for n in self.nodes:
            res.append(n.name)
        return res

class Node:
    def __init__(self):
        self.value = -1
        self.name = None

class Constraint:
    def __init__(self):
        self.NodeA = None
        self.NodeB = None
        self.type = None
        self.isValue = -1
    
    def toStr(self):
        res = self.type + " " + self.NodeA.name
        if self.NodeB is not None:
            res += " " + self.NodeB.name
        if self.isValue != -1:
            res += " (value: " +  str(self.isValue) + ")"
        return res

class PuzzleParser:

    def parsePuzzle(self, puzzle):
        csp = CSP()
        #preprocessing
        puzzle = puzzle.lower()
        replacers = [("jan ", "january "), ("feb ", "february "), ("sep ", "september "), ("dec ", "december "), ("swedish ", "swede ")]
        for r in replacers:
            puzzle = puzzle.replace(r[0], r[1])


        months = ("january|february|march|april|may|june|july|august|september|october|november|december")
        puzzle = re.sub(rf"\bin\s+(?=({months})\b)", "", puzzle) # remove 'in' before months 
        #parse domains
        splits = puzzle.split("## clues:\n")[0].split('\n')
        splits.pop(0)
        for split in splits:
            nodes = []
            subsplit = split.split('`')
            for i in range(len(subsplit)):
                if(i % 2 == 1 and subsplit[i] != ''):
                    new = Node()
                    new.name = subsplit[i]
                    nodes.append(new)
                    csp.nodes.append(new)
            pairs = list(combinations(nodes, 2))
            for p in pairs:
                c = Constraint()
                c.NodeA = p[0]
                c.NodeB = p[1]
                c.type = "NOT_EQUAL"
                csp.constraints.append(c)
        #parse clues
        clues = puzzle.split("## clues:\n")[1].split('\n')
        for clue in clues:
            if clue == '':
                continue
            targets = []
            indexFound = []
            for n in csp.nodes:
                if findKeyInClue(clue, n.name) != -1:     #----------------
                    targets.append(n)
                    indexFound.append(findKeyInClue(clue, n.name))
            if len(indexFound) > 1 and indexFound[1] < indexFound[0]:
                l = targets[1]
                targets[1] = targets[0]
                targets[0] = l

            #build constraint

            if clue.find(" is directly left ") != -1:
                if len(targets) < 2:
                    print(f"Could not parse dirLeft clue ({clue}) from tergets {targets}")
                    continue
                c = Constraint()
                c.NodeA = targets[0]
                c.NodeB = targets[1]
                c.type = "DIR_LEFT"
                csp.constraints.append(c)
            elif clue.find(" is somewhere to the left ") != -1:
                if len(targets) < 2:
                    print(f"Could not parse somLeft clue ({clue}) from tergets {targets}")
                    continue
                c = Constraint()
                c.NodeA = targets[0]
                c.NodeB = targets[1]
                c.type = "SOM_LEFT"
                csp.constraints.append(c)
            
            elif clue.find(" is directly right ") != -1:
                if len(targets) < 2:
                    print(f"Could not parse dirRight clue ({clue}) from tergets {targets}")
                    continue
                c = Constraint()
                c.NodeA = targets[0]
                c.NodeB = targets[1]
                c.type = "DIR_RIGHT"
                csp.constraints.append(c)
            
            elif clue.find(" is somewhere to the right ") != -1:
                if len(targets) < 2:
                    print(f"Could not parse somRight clue ({clue}) from tergets {targets}")
                    continue
                c = Constraint()
                c.NodeA = targets[0]
                c.NodeB = targets[1]
                c.type = "SOM_RIGHT"
                csp.constraints.append(c)
            
            elif clue.find(" is in ") != -1:
                if len(targets) < 1:
                    print(f"Could not parse isIn clue ({clue}) from tergets {targets}")
                    continue
                c = Constraint()
                c.NodeA = targets[0]
                c.type = "IS_IN"
                c.isValue = self.findNumber(clue)
                csp.constraints.append(c)
            
            elif clue.find(" is not in ") != -1:
                if len(targets) < 1:
                    print(f"Could not parse isNotIn clue ({clue}) from tergets {targets}")
                    continue
                c = Constraint()
                c.NodeA = targets[0]
                c.type = "IS_NOT_IN"
                c.isValue = self.findNumber(clue)
                csp.constraints.append(c)

            elif clue.find(" next to ") != -1:
                if len(targets) < 2:
                    print(f"Could not parse Distance1 clue ({clue}) from tergets {targets}")
                    continue
                c = Constraint()
                c.NodeA = targets[0]
                c.NodeB = targets[1]
                c.type = "DISTANCE_1"
                csp.constraints.append(c)

            elif clue.find(" are two houses between ") != -1:
                if len(targets) < 2:
                    print(f"Could not parse Distance3 clue ({clue}) from tergets {targets}")
                    continue
                c = Constraint()
                c.NodeA = targets[0]
                c.NodeB = targets[1]
                c.type = "DISTANCE_3"
                csp.constraints.append(c)

            elif clue.find(" is one house between ") != -1:
                if len(targets) < 2:
                    print(f"Could not parse Distance2 clue ({clue}) from tergets {targets}")
                    continue
                c = Constraint()
                c.NodeA = targets[0]
                c.NodeB = targets[1]
                c.type = "DISTANCE_2"
                csp.constraints.append(c)

            elif clue.find(" is not ") != -1:
                if len(targets) < 2:
                    print(f"Could not parse isNot clue: {clue}")
                    continue
                c = Constraint()
                c.NodeA = targets[0]
                c.NodeB = targets[1]
                c.type = "IS_NOT"
                csp.constraints.append(c)
            
            elif clue.find(" is ") != -1:
                if len(targets) < 2:
                    print(f"Could not parse IS clue: {clue}")
                    continue
                c = Constraint()
                c.NodeA = targets[0]
                c.NodeB = targets[1]
                c.type = "IS"
                csp.constraints.append(c)
            else:
                print(f"Could not classify clue: {clue}")
            
        return csp

    def findNumber(self, clue):
        if clue.find(" first house") != -1:
            return 1        
        elif clue.find(" second house") != -1:
            return 2
        elif clue.find(" third house") != -1:
            return 3
        elif clue.find(" fourth house") != -1:
            return 4
        elif clue.find(" fifth house") != -1:
            return 5
        elif clue.find(" sixth house") != -1:
            return 6
        else:
            print(f"Can't find number in clue: {clue}")
            return -1

def findKeyInClue(clue, key):
    l = clue.find(key)
    if l != -1:
        return l
    l = clue.find(key.replace("-", ""))
    if l != -1:
        return l
    l = clue.find(key.replace("-", " "))
    if l != -1:
        return l
    l=clue.replace("-", "").find(key)
    if l != -1:
        return l
    l=clue.replace("-", " ").find(key)
    if l != -1:
        return l
    keyWithoutS = re.sub(r"s\b", "", key)
    l=clue.find(keyWithoutS)
    if l != -1:
        return l
    keyWithoutIng = re.sub(r"ing\b", "", key)
    l=clue.find(keyWithoutIng)
    if l != -1:
        return l

    return -1