import zipfile
import os, sys
root = os.getcwd()
sys.path.append(os.path.join(root, "modules"))
sys.path.append(os.path.join(root, "modules", "colorama"))
os.environ["PATH"] = os.path.join(root, "modules", "winrar")
import rarfile
from colorama import init, Fore, Style
from termcolor import colored
from progress.bar import Bar

init(convert=True)

zipEndTypes = [".zip", ".cbz"]
rarEndTypes = [".rar", ".cbr"]

errorsCount = 0
errors = []

while True:
    bookPartsDir = input("Enter folder name with files to merge (in input folder): ")
    bookPath = os.path.join(root, "input", bookPartsDir)
    if (bookPartsDir == ""):
        print(colored("Folder name is empty", "red"))
    elif (os.path.exists(bookPath) and len(os.listdir(bookPath)) == 0):
        print(colored("Folder is empty", "red"))
    elif (not os.path.exists(bookPath)):
        print(colored("Folder \"{0}\" does not exist".format(bookPartsDir), "red"))
    else:
        break

overwrite = 0

while True:
    endName = input("Enter merged file name with file type (.cbz, .zip, .rar, .cbr support. <name of the input folder>.cbr by default): ") or "{0}.cbr".format(bookPartsDir)
    if (endName in os.listdir(os.path.join(root, "output"))):
        print(colored("Name \"{0}\" already existed.".format(endName), "red"))
        while True:
            overwriteInput = input("Overwrite it? y/n: ")
            if overwriteInput.upper() == "Y":
                overwrite = 1
                break
            elif overwriteInput.upper() == "N":
                overwrite = 0
                break
            else:
                print(colored("Please use Y or N.", "red"))
        if (not overwrite):
            continue
    endType = endName[endName.rfind("."):]
    if (endType in zipEndTypes):
        endTypeMode = "zip"
        break
    elif (endType in rarEndTypes):
        endTypeMode = "rar"
        break
    else:
        print(colored("Unsupported file type \"{0}\"".format(endType), "red"))

if ("output" not in os.listdir()):
    os.mkdir("output")
if ("temp" not in os.listdir()):
    os.mkdir("temp")
if ("input" not in os.listdir()):
    os.mkdir("input")

bookPartsList = os.listdir(bookPath)

progressBar = Bar('Processing', max=len(bookPartsList))
progressBar.update()

filesCount = 1
chapterCount = 1
if (endTypeMode == "zip"):
    endFile = zipfile.ZipFile(os.path.join("output", endName), "w", allowZip64 = True)

    for part in bookPartsList:
        partPath = os.path.join(bookPath, part)

        if os.path.isdir(partPath):
            filesList = os.listdir(partPath)
            for i in range(len(filesList)):
                item = open(os.path.join(partPath, filesList[i]), "rb")
                itemData = item.read()
                fileType = filesList[i][filesList[i].rfind("."):]
                formatFilesCount = str(filesCount).zfill(3)
                formatChapterCount = str(chapterCount).zfill(3)
                endFile.writestr(formatChapterCount + "-" + formatFilesCount + fileType, itemData)
                item.close()
                filesCount += 1
            progressBar.next()
            chapterCount += 1
            filesCount = 1

        elif zipfile.is_zipfile(partPath):
            arhive = zipfile.ZipFile(partPath, "r")
            filesList = arhive.namelist()
            for i in range(len(filesList)):
                fileType = filesList[i][filesList[i].rfind("."):]
                itemData = arhive.read(filesList[i])
                formatFilesCount = str(filesCount).zfill(3)
                formatChapterCount = str(chapterCount).zfill(3)
                endFile.writestr(formatChapterCount + "-" + formatFilesCount + fileType, itemData)
                filesCount += 1
            arhive.close()
            progressBar.next()
            chapterCount += 1
            filesCount = 1

        elif rarfile.is_rarfile(partPath):
            arhive = rarfile.RarFile(partPath, "r")
            filesList = arhive.namelist()
            for i in range(len(filesList)):
                fileType = filesList[i][filesList[i].rfind("."):]
                itemData = arhive.read(filesList[i])
                formatFilesCount = str(filesCount).zfill(3)
                formatChapterCount = str(chapterCount).zfill(3)
                endFile.writestr(formatChapterCount + "-" + formatFilesCount + fileType, itemData)
                filesCount += 1
            arhive.close()
            progressBar.next()
            chapterCount += 1
            filesCount = 1

        else:
            errorsCount += 1
            errors.append(part)
    endFile.close()

elif (endTypeMode == "rar"):

    

    endFile = os.path.join(root, "output", endName + endType)

    for part in bookPartsList:
        partPath = os.path.join(bookPath, part)
        if os.path.isdir(partPath):
            filesList = os.listdir(partPath)
            for i in range(len(filesList)):#copy with change names
                fileType = filesList[i][filesList[i].rfind("."):]
                item = open(os.path.join(partPath, filesList[i]), "rb")
                itemData = item.read()
                formatFilesCount = str(filesCount).zfill(3)
                formatChapterCount = str(chapterCount).zfill(3)
                tempFile = open(os.path.join("temp", "{0}-{1}".format(formatChapterCount, formatFilesCount) + fileType), "wb")
                tempFile.write(itemData)
                tempFile.close()
                item.close()
                filesCount += 1
            progressBar.next()
            chapterCount += 1
            filesCount = 1

        elif zipfile.is_zipfile(partPath):
            arhive = zipfile.ZipFile(partPath, "r")
            filesList = arhive.namelist()
            for i in range(len(filesList)):
                fileType = filesList[i][filesList[i].rfind("."):]
                itemData = arhive.read(filesList[i])
                formatFilesCount = str(filesCount).zfill(3)
                formatChapterCount = str(chapterCount).zfill(3)
                tempFile = open(os.path.join("temp", "{0}-{1}".format(formatChapterCount, formatFilesCount) + fileType), "wb")
                tempFile.write(itemData)
                tempFile.close()
                filesCount += 1
            arhive.close()
            progressBar.next()
            chapterCount += 1
            filesCount = 1

        elif rarfile.is_rarfile(partPath):
            arhive = rarfile.RarFile(partPath, "r")
            filesList = arhive.namelist()
            for i in range(len(filesList)):
                fileType = filesList[i][filesList[i].rfind("."):]
                itemData = arhive.read(filesList[i])
                formatFilesCount = str(filesCount).zfill(3)
                formatChapterCount = str(chapterCount).zfill(3)
                tempFile = open(os.path.join("temp", "{0}-{1}".format(formatChapterCount, formatFilesCount) + fileType), "wb")
                tempFile.write(itemData)
                tempFile.close()
                filesCount += 1
            arhive.close()
            progressBar.next()
            chapterCount += 1
            filesCount = 1

        else:
            errorsCount += 1
            errors.append(part)
    
    arhivePath = os.path.join("output", endName)
    filePath = "temp"
    if overwrite:
        os.system("@echo off & rar d {0}>Nul".format(arhivePath))
    
    os.system("@echo off & rar m -ep \"{0}\" {1}>Nul".format(arhivePath, filePath))

progressBar.finish()

if (errorsCount > 0):
    print(colored("Unsupported files: {0}".format(errorsCount), "yellow"))
    print(colored("\n".join(errors), "yellow"))

print(colored("Done", "green"))
input()