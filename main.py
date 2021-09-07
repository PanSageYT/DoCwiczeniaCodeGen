import random
import threading
import time
import math

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import psutil

class bcolors:
    OK = '\033[92m' #GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR

url = "https://docwiczenia.pl/kod/"

fail = 0
success = 0
threadfail = 0
repeattext = 0
testedcodes = []
closing = False

allowedthreads = 4

timeunix = time.time()
timelocal = time.gmtime(timeunix)
timehour = timelocal.tm_hour
timeminute = timelocal.tm_min
timeday = timelocal.tm_mday
timemonth = timelocal.tm_mon

def GetRandomCode():
    global repeattext
    RandomCode = ''.join((random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890') for x in range(6)))
    if RandomCode in testedcodes:
        GetRandomCode()
        repeattext = repeattext + 1
    testedcodes.append(RandomCode)
    return RandomCode

def CreateStatFile():
    statFileNum = str(timehour + timeminute + timeday + timemonth) + GetRandomCode()
    statFile = open("stats\\Statistics" + statFileNum + ".txt", 'w+')
    print(f"{bcolors.WARNING}Statis: Stworzono plik: Statistics" + statFileNum + f".txt{bcolors.RESET}")
    statFile.close()

def UpdateStats():
    global fail, success, threadfail, repeattext

    failstr = str(fail)
    successstr = str(success)
    threadfailstr = str(threadfail)
    repeattextstr = str(repeattext)

    statFileNum = str(timehour + timeminute + timeday + timemonth) + GetRandomCode()
    statFile = open("stats\\Statistics" + statFileNum + ".txt", 'w+')
    print(f"{bcolors.OK}Statis: Zaaktualizowano statystyki.")
    print("        Potwierdzone kody: " + successstr)
    print("        Odrzucone kody   : " + failstr)
    print("        Odrzucono wątków : " + threadfailstr)
    print("        Powtórzone kody  : " + repeattextstr + f"{bcolors.RESET}")
    statFile.write(str(timehour) + ":" + str(timeminute) + " dnia " + str(timeday) + "." + str(timemonth) + "\n"
                   "--- SPAMMER KODOW DOCWICZENIA --- \n" +
                   "Potwierdzone kody: " + successstr + "\n" +
                   "Odrzucone kody: " + failstr + "\n"
                   "Odrzucono wątków: " + threadfailstr + "\n"
                   "Powtórzone kody: " + repeattextstr)
    statFile.close()
    time.sleep(20)
    UpdateStats()

def CheckCode():
    global fail, success, threadfail, closing, testedcodes, repeattext, repeattextstr
    global timehour, timeminute, timeday, timemonth
    timehour = str(timehour)
    timeminute = str(timeminute)
    timeday = str(timeday)
    timemonth = str(timemonth)

    codeToCheck = GetRandomCode()
    chromeoptions = Options()
    chromeoptions.add_argument("--headless")
    driver = webdriver.Firefox(options=chromeoptions)
    driver.get(url + codeToCheck)

    try:
        if(len(driver.find_elements_by_class_name("not-found")) != 0):
            for err in driver.find_elements_by_class_name("not-found"):
                if(err.text == "Kod nie istnieje."):
                    failFile = open("NoCode.txt", 'a')
                    failFile.write("Kod " + codeToCheck + " nie działa \n")
                    failFile.close()
                    print(f"{bcolors.FAIL}Fail  : " + codeToCheck + f" nie działa{bcolors.RESET}")
                    fail = fail + 1
                    driver.close()
                    driver.quit()
        if (len(driver.find_elements_by_class_name("code-audio")) != 0):
            for checkifcode in driver.find_elements_by_class_name("code-audio"):
                    whatisthis = driver.find_element_by_class_name("page-info").text
                    successFile = open("YesCode.txt", 'a')
                    successFile.write(codeToCheck + " - " + whatisthis + "\n")
                    successFile.close()
                    print(f"{bcolors.OK}Succes: " + codeToCheck + " - " + whatisthis + f"{bcolors.RESET}")
                    success = success + 1
                    driver.close()
                    driver.quit()
    except:
        return time.sleep(0)

    #try:
    #    os.mknod("C:/Users/Patryk Kursa/PycharmProjects/Stats/Statistics" + str(timehour) + str(timeminute) + ".txt")
    #except:
    #    print("")


def updateThreads():
    while(3 > 2):
        global allowedthreads
        allowedthreads = (math.ceil((math.ceil(((psutil.virtual_memory().available / 25) + ((psutil.cpu_percent(percpu=False, interval=1) * -1) / 69)) * math.pi)) / (15000000 * math.pi))) + math.ceil(threading.activeCount() / 5)
        print(f"{bcolors.WARNING}Thread: Zmieniono dozwolone thready na " + str(allowedthreads) + f"{bcolors.RESET}")
        print(f"{bcolors.WARNING}Thread: Uruchomione thready: " + str(threading.activeCount()) + f"{bcolors.RESET}")
        print(f"{bcolors.OK}CPURAM: Użycie CPU " + str(psutil.cpu_percent(percpu=False, interval=1)) + f"%{bcolors.RESET}")
        print(f"{bcolors.OK}CPURAM: Dostępny RAM " + str(psutil.virtual_memory().available) + f"b / " + str(math.ceil(psutil.virtual_memory().available / 1000000000)) + f"gb{bcolors.RESET}")
        time.sleep(allowedthreads * (math.pi / 2))

if __name__ == '__main__':
    print(" ")
    print(f"{bcolors.OK}START : Uruchamianie generatora kodów do strony {bcolors.RESET}{bcolors.WARNING}DoCwiczenia.pl{bcolors.RESET}")
    print(" ")
    CreateStatFile()

    x = threading.Thread(target=updateThreads, args=())
    x.start()

    x = threading.Thread(target=UpdateStats, args=())
    x.start()

    while(3 > 2):
        time.sleep(1)
        if(threading.activeCount() <= allowedthreads):
            if (threading.activeCount() > allowedthreads):
                threadfail = threadfail + 1
                break
            x = threading.Thread(target=CheckCode, args=())
            x.daemon = True
            x.start()
        else:
            threadfail = threadfail + 1
