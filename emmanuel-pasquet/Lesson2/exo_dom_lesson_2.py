import requests
from bs4 import BeautifulSoup

url = "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=2010"

def dataPerYear(year):
url = "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=" + str(year)
r = requests.get(url)
soup = BeautifulSoup(r.text,"html.parser")
return retrieveEuros(soup)

def getSpecifyLineData(soup,index):
return soup.find_all(class_ = "montantpetit G")[index].text.replace('\xa0','')

def retrieveEuros(soup):
dico = {}
dico['eurosparhabitantA'] = getSpecifyLineData(soup,1)
dico['eurosparstrateA'] = getSpecifyLineData(soup,2)
dico['eurosparhabitantB'] = getSpecifyLineData(soup,4)
dico['eurosparstrateB'] = getSpecifyLineData(soup,5)
dico['eurosparhabitantC'] = getSpecifyLineData(soup,10)
dico['eurosparstrateC'] = getSpecifyLineData(soup,11)
dico['eurosparhabitantD'] = getSpecifyLineData(soup,13)
dico['eurosparstrateD'] = getSpecifyLineData(soup,14)

return dico

def printData(dico):
print("Euros par habitant A : " + dico['eurosparhabitantA'] + " -- Moyenne de la strate A : " + dico['eurosparstrateA'])
print("Euros par habitant B : " + dico['eurosparhabitantB'] + " -- Moyenne de la strate B : " + dico['eurosparstrateB'])
print("Euros par habitant C : " + dico['eurosparhabitantC'] + " -- Moyenne de la strate C : " + dico['eurosparstrateC'])
print("Euros par habitant D : " + dico['eurosparhabitantD'] + " -- Moyenne de la strate D : " + dico['eurosparstrateD'])

for year in range(2010,2014):
dico = dataPerYear(year)
print("-----" + str(year) + "-----")
printData(dico)
