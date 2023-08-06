import time
import sys
import getopt
import subprocess
import os

def guess():
    print("--> Analyzing")
    toprint = ""
    files = []
    py = 0
    njs = 0
    other = 0
    for file in os.listdir(os.getcwd()):
        if os.path.isfile(f"{os.getcwd()}/{file}"):
            files.append(file)
            if file.endswith(".py"):
                py += 1
            if file.endswith(".js"):
                njs += 1
            if file.endswith(".js") == False and file.endswith(".py") == False and file != "pyproject.toml" and file != "package.json":
                other += 1
    if "pyproject.toml" in files:
        py += 1
    if "package.json" in files:
        njs += 1
    if py != 0:
        percentage = py / len(files)
        percentage = percentage * 100
        percentage = round(percentage)
        toprint += f"Python: {percentage}%\n"
    if njs != 0:
        percentage = njs / len(files)
        percentage = percentage * 100
        percentage = round(percentage)
        toprint += f"Nodejs: {percentage}%\n"
    percentage = other / len(files)
    percentage = percentage * 100
    percentage = round(percentage)
    toprint += f"Other: {percentage}%\n"
    print(toprint)
    print(f"--> {len(files)} files scanned")

def alz():
    toprint = ""
    files = []
    py = 0
    njs = 0
    for file in os.listdir(os.getcwd()):
        files.append(file)
        if file.endswith(".py"):
            py += 1
        if file.endswith(".js"):
            njs += 1
    if "pyproject.toml" in files:
        py += 1
    if "package.json" in files:
        njs +=1
    if py != 0:
        percentage = (float(py)/float(len(files))) * 100
        percentage = round(percentage)
        toprint += f"Python: {percentage}%\n"
    if njs != 0:
        percentage = (float(njs)/float(len(files))) * 100
        percentage = round(percentage)
        toprint += f"Nodejs: {njs}%\n"
    if py > njs:
        return "python"
    else:
        return "njs"
