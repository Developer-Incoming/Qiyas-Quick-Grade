from http.client import HTTPSConnection
from bs4 import BeautifulSoup
import pyautogui # user manipulation
import webbrowser
import time

phoneNumber = "966xxxxxxxxx"
whatsappURL = f"https://web.whatsapp.com/send/?phone={phoneNumber}&text="

conn = HTTPSConnection("e-services.qiyas.sa")

cookies = {
    "ASP.NET_SessionId": "",
    "OClmoOot": "",
    "etec_co": "",
    "TS01fdea90": ""
}
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Cookie": f"OClmoOot={cookies['OClmoOot']}; etec_co={cookies['etec_co']}; TS01fdea90={cookies['TS01fdea90']}; ASP.NET_SessionId={cookies['ASP.NET_SessionId']}",
}

# Repeats checking for a test type's results until there's a change whether its positive or not.
def checkTestResults(testType: int):
    conn.request("POST", "/Qiyas.TRAS.Web.Internet/Home/_TestsResult", f"testType={str(testType)}", headers) # testType=1 = qudurat, 2 = tahsili
    response = conn.getresponse().read().decode("utf-8")
    soup = BeautifulSoup(response, "html.parser")

    # error = len(str(soup.find("head"))) <= 40
    # print(len(str(soup.find("head"))))
    # print(soup.find("head"))
    # input()

    results = []
    for x in soup.find_all("div", {"class": "panel"}):
        labels = x.find_all("label")
        smalls = x.find_all("small")
        results.append(f'''{labels[0].text.strip()} - {labels[1].text.strip()}{smalls[0].text.strip()} - {labels[2].text.strip()}{smalls[1].text.strip()}''')
    
    # print(results)
    # input()
    return results

# Repeats checking available tests until there's a change whether its positive or not.
# CONCEPT - not working, and I don't have any "test subject" to test it on.
def checkAvailableTests():
    conn.request("POST", "/Qiyas.TRAS.Web.Internet/Home/_AvailableTest_Candidate", "isVisibleActions=True", headers)
    response = conn.getresponse().read().decode("utf-8")
    soup = BeautifulSoup(response, "html.parser")

    # error = len(str(soup.find("head"))) <= 40
    print(len(str(soup.find("head"))))
    print(soup.find("head"))
    input()

    results = []
    
    print(results)
    input()
    return results

def sendMessage(message: str):
        open(f"{whatsappURL}{message}")
        time.sleep(10)
        pyautogui.click()
        time.sleep(1)
        pyautogui.typewrite(["enter"])


# Main
firstCheck = True
responseLength = newLength = -1

while True:
    firstCheck = responseLength == -1 # False if responseLength == -1 else True
    
    results = checkTestResults(1)
    newLength = len(results)

    print("\nresults:", results)
    print(not firstCheck, len(results) == 0, newLength > responseLength and responseLength != -1)

    if not firstCheck and len(results) == 0:
        sendMessage("it broke lol")
        break

    if (not firstCheck or len(results) == 0) and newLength > responseLength and responseLength != -1:
        sendMessage(f"{str(results if not len(results) == 0 else 'broke')}")
        break

    responseLength = newLength
    
    time.sleep(3)
