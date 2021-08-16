import zipfile
import os, sys
import time
root = os.getcwd()
sys.path.append(os.path.join(root, "modules"))
sys.path.append(os.path.join(root, "modules", "colorama"))
os.environ["PATH"] = os.path.join(root, "modules", "winrar")
import rarfile
from colorama import init, Fore, Style
from termcolor import colored
from progress.bar import Bar

init(convert=True)

endTypes = [".zip", ".cbz"]

errorsCount = 0
errors = []

while True:
    bookPartsDir = input("Enter folder name with files to merge: ")
    bookPath = os.path.join(root, bookPartsDir)
    if (bookPartsDir == ""):
        print(colored("folder name is empty", "red"))
    elif (os.path.exists(bookPath) and not bookPartsDir == ""):
        break
    else:
        print(colored("folder \"{0}\" does not exist".format(bookPartsDir), "red"))

while True:
    endName = input("Enter merged file name with file type (.cbz or .zip, <name of the input folder>.cbz by default): ") or "{0}.cbz".format(bookPartsDir)
    endType = endName[endName.rfind("."):]
    if endType in endTypes:
        break
    else:
        print(colored("unsupported file type \"{0}\"".format(endType), "red"))

if ("output" not in os.listdir()):
    os.mkdir("output")

endFile = zipfile.ZipFile(os.path.join("output", endName), "w")

bookPartsList = os.listdir(bookPath)

progressBar = Bar('Processing', max=len(bookPartsList))
progressBar.update()

filesCount = 1
for part in bookPartsList:
    partPath = os.path.join(bookPath, part)

    if os.path.isdir(partPath):
        filesList = os.listdir(partPath)
        for i in range(len(filesList)):
            item = open(os.path.join(partPath, filesList[i]), "rb")
            itemData = item.read()
            fileType = filesList[i][filesList[i].rfind("."):]
            endFile.writestr(str(filesCount) + fileType, itemData)
            filesCount += 1
        progressBar.next()

    elif zipfile.is_zipfile(partPath):
        arhive = zipfile.ZipFile(partPath, "r")
        filesList = arhive.namelist()
        for i in range(len(filesList)):
            fileType = filesList[i][filesList[i].rfind("."):]
            endFile.writestr(str(filesCount) + fileType, arhive.read(filesList[i]))
            filesCount += 1
        arhive.close()
        progressBar.next()

    elif rarfile.is_rarfile(partPath):
        arhive = rarfile.RarFile(partPath, "r")
        filesList = arhive.namelist()
        for i in range(len(filesList)):
            fileType = filesList[i][filesList[i].rfind("."):]
            endFile.writestr(str(filesCount) + fileType, arhive.read(filesList[i]))
            filesCount += 1
        arhive.close()
        progressBar.next()

    else:
        errorsCount += 1
        errors.append(part)


endFile.close()
progressBar.finish()
if (errorsCount > 0):
    print(colored("Unsupported files: {0}".format(errorsCount), "yellow"))
    print(colored("\n".join(errors), "yellow"))
print(Fore.GREEN + "Done " + Style.RESET_ALL)
time.sleep(3)