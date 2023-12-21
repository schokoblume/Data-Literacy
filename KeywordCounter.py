import sys

#Aufrufen über Konsole mit folgenden Parametern:
#1. Pfad zur Datei die durchsucht werden soll(.txt)
#2. Pfad zur Datei in der die Ergebnisse gespeichert werden (.txt)
#3. Keyword

def countKeyword(Searchfile, Result, Keyword):
    search_file=Searchfile
    result_file=Result
    Keyword=Keyword
    count = 0
    datafile = open(search_file).readlines()
    for line in datafile:
        if Keyword in line:
                count= count + 1
    file = open(result_file, "a")
    file.write(" \n Das Wort " + Keyword + " wurde " + str(count) + " mal im File " + search_file + " gefunden")
    file.close()





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if len(sys.argv) == 4 :
        countKeyword(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("Invalid Numbers of Arguments. Script will be terminated.")



