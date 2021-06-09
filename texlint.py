#!/usr/bin/env python
import sys

farg = sys.argv[1]

texFile = open(farg,'r')
doc = texFile.readlines()

def db():
    print("here")

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
    commands = ["\\section","\\subsection", "\\subsubsection"]
    beginStack = []
    beginIndent = 0
    commandIndent = 0
    lastIndex = 0
    keep = 0
    for line in lines:
        keep = 0
        for command in commands:
            if command in line:
                index = commands.index(command)
                if index > lastIndex:
                    commandIndent += 1
                elif index < lastIndex: 
                    commandIndent -= 1
                # commandIndent = commands.index(command) + 1
                lastIndex = index
                keep = 1
                break

        # If there is a begin command
        if "\\begin" in line:
            beginStack.append(commandIndent)
            commandIndent += 1
            keep = 1
        # If there is an end command
        if "\\end" in line:
            commandIndent = beginStack.pop()

        # Dont indent commands other than \item
        if"\\" in line and not "\\item" in line:
            keep = 1

        indt = ""
        for i in range(commandIndent - keep):
            indt += '\t'
        out.append( indt+ line)
    return out
    
doc = indent(doc)



outFile = sys.argv[2]
l = open(outFile,"w")
l.writelines(doc)
l.close()

