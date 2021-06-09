#!/usr/bin/env python
import sys

farg = sys.argv[1]

texFile = open(farg,'r')
doc = texFile.readlines()

# What I want to do:
#     I want to make a tool that:
#     splits up paragraps based off of sentences
#     Indents the inside of chapters, sections, subsections, etc

# This removes all leading whitespace
def rmWs(lines):
    out = []
    for line in lines:
        while line[0] == " " or line[0] =="\t":
            line = line[1:]
        out.append(line)
    return out

doc = rmWs(doc)

# This removes all double spaces
def rmDs(lines):
    out = ['']
    for line in lines:
        if line != "\n" or out[-1] != "\n":
            out.append(line)
    return out[1:]

doc = rmDs(doc)


def indent(lines):
    out = []
    currentLevel = ''
    commands = ["\\section","\\subsection", "\\subsubsection"]
    indentLevel = 0
    beginStack = []
    for line in lines:
        # First indent
        indt = ""
        for i in range(indentLevel):
            indt += "\t"
        out.append(indt + line)
        
        # Then check how we should indent next line
        for i in range(len(commands)):
            res = line.find(commands[i])
            # If there is an indent command
            if res != -1:
                currentLevel = commands[res]
                indentLevel = i+1
                break
            
        # If there is a begin command
        if "begin" in line:
            beginStack.append(indentLevel)
            indentLevel += 1
        # If there is an end command
        if "\\end" in line:
            indentLevel = beginStack.pop()
            out.pop()
            indt = ""
            for i in range(indentLevel):
                indt += "\t"
            out.append(indt +line)
    return out
    
doc = indent(doc)



outFile = sys.argv[2]
l = open(outFile,"w")
l.writelines(doc)
l.close()

