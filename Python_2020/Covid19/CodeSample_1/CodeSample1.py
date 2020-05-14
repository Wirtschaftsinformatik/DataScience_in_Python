#Anbei der Python Code zur Covid 19 Analyse von
#Julian Gerhardt(Matrikelnr:185648)
#Forschungsfrage des Projekt: Analyse von Covid 19 auf den verschiedenen Kontinenten
#Der Code wurde mit Sypder(Anaconda) geschrieben und beinhaltet die packages
#'pandas', 'matplotlib' und 'numpy', welche in den Workshopvideos bei Data Camp vorgestellt wurden

#.........................................
#1.Daten einlesen (Daten habe ich mir vorher von Excel als .csv Datenpaket umgewandelt)
import pandas as pd #package 'pandas' einlesen für die Daten aus Excel bzw. csv. (Die Vorgehensweise hatte ich aus Data Camp)
data= pd.read_csv("COVID-19-Daten.csv", delimiter= ';') #Die Trennstriche sind ';'
print(data) # einlesen der Daten(Achtung: von meinem PC) und anzeigen
print(data.head()) #Zum Test, ob die Daten alles berücksichtigen
#.........................................
#2. Daten bearbeiten, um vergleichbar zu machen
data_new= data[["dateRep","cases","deaths","countriesAndTerritories","continentExp"]]
print(data_new) #Es werden nur die wichtigsten Spalten für die Analyse gebraucht, den Rest lasse ich weg
print(data_new.head())#Zum Test, ob die Daten alles berücksichtigen
#..................
#nach einzelnen Kontinenten Teiltabellen definieren (ohne "Other")
#im Projekt möchte ich die Entwicklung auf den jeweiligen Kontinenten analysieren,
#deswegen muss die gesamte Tabelle im data.frame in Einzeltabellen nach den Kontinenten 'zerlegt' werden
Asia= data_new.copy() #ich lege eine Kopie an, damit sich aus den ursprünglichen Daten nichts "versehentlich" ändert
Asia= data_new[(data_new.continentExp == "Asia")] # Der Befehl gleicht die Spalte'continentExp" nach den einzelnen Kontinenten ab
Asia= Asia.sort_values(["dateRep"]) #wichtig, das Datum sortieren (leider wird der 31.12.19 an das Ende gepackt. Habe leider nicht herausgefunden, wie sich das ändern lässt....)
print(Asia) # Teiltabelle ausgeben
#....................
Africa= data_new.copy() # gleiches vorgehen für die anderen Kontinente
Africa= data_new[(data_new.continentExp == "Africa")]
Afirca= Africa.sort_values(["dateRep"])
print(Africa)
#...................
America= data_new.copy()
America= data_new[(data_new.continentExp == "America")]
America= America.sort_values(["dateRep"])
print(America)
#..................
Europe= data_new.copy()
Europe= data_new[(data_new.continentExp == "Europe")]
Europe= Europe.sort_values(["dateRep"])
print(Europe)
#...........
Oceania= data_new.copy()
Oceania= data_new[(data_new.continentExp == "Oceania")]
Oceania= Oceania.sort_values(["dateRep"])
print(Oceania)
#für alle Kontinente Teiltabellen für die Analyse erstellt, Daten sind aufbereitet
#...........
#3.Statistischer Vergleich zwischen den Kontinenten auf Basis von Lageparametern
import numpy as np #für statistische Analyse package 'numpy'
#Toteszahlen vergleichen
print("\n") #Das schafft einen Zeilenumbruch im Output (Quelle:https://www.python-forum.de/viewtopic.php?t=41566)
print("Übersicht über die Todeszahlen:")
Asien_deaths= [[np.mean(Asia.deaths)],[np.max(Asia.deaths)],[np.min(Asia.deaths)],[np.sum(Asia.deaths)]] #Verschiedene Lageparameter für die Analyse auswählen (hier Beispiel Asien)
print("Tote in Asien:","Mittelwert:",Asien_deaths[0],"Maximum:",Asien_deaths[1],"Minimum:"
	  ,Asien_deaths[2],"Gesamt:",Asien_deaths[-1]) #Zur Ausgabe kommentieren, [] greigt jeweils auf den Index zu
Africa_deaths= [[np.mean(Africa.deaths)],[np.max(Africa.deaths)],[np.min(Africa.deaths)],[np.sum(Africa.deaths)]] #gleiches Vorgehen bei den anderen Kontinenten
print("Tote in Afrika:","Mittelwert:",Africa_deaths[0],"Maximum:",Africa_deaths[1],"Minimum:"
	  ,Africa_deaths[2],"Gesamt:",Africa_deaths[-1])
America_deaths= [[np.mean(America.deaths)],[np.max(America.deaths)],[np.min(America.deaths)],[np.sum(America.deaths)]]
print("Tote in Amerika:","Mittelwert:",America_deaths[0],"Maximum:",America_deaths[1],"Minimum:"
	  ,America_deaths[2],"Gesamt:",America_deaths[-1])
Europe_deaths= [[np.mean(Europe.deaths)],[np.max(Europe.deaths)],[np.min(Europe.deaths)],[np.sum(Europe.deaths)]]
print("Tote in Europa:","Mittelwert:",Europe_deaths[0],"Maximum:",Europe_deaths[1],"Minimum:"
	  ,Europe_deaths[2],"Gesamt:",Europe_deaths[-1])
Oceania_deaths= [[np.mean(Oceania.deaths)],[np.max(Oceania.deaths)],[np.min(Oceania.deaths)],[np.sum(Oceania.deaths)]]
print("Tote in Ozeanien:","Mittelwert:",Oceania_deaths[0],"Maximum:",Oceania_deaths[1],"Minimum:"
	  ,Oceania_deaths[2],"Gesamt:",Oceania_deaths[-1])
#Vergleich zwischen den Paramertern mithilfe von if und Relationszeichen (Vorgehen wie in Data Camp Video gezeigt)
#Vergleich zwischen den Todezahlen an einem Tag
print("Vergleich zwischen den Todeszahlen:")
if np.max(America.deaths) > np.max(Africa.deaths) | np.max(Asia.deaths) | np.max(Europe.deaths) | np.max(Oceania.deaths) : print("Die meisten Toten an einem Tag gab es in Amerika!") # gibt dann jeweils eine Variante aus
if np.max(Africa.deaths) > np.max(America.deaths) | np.max(Asia.deaths) | np.max(Europe.deaths) | np.max(Oceania.deaths) : print("Die meisten Toten an einem Tag gab es in Afrika!")
if np.max(Asia.deaths) > np.max(Africa.deaths) | np.max(America.deaths) | np.max(Europe.deaths) | np.max(Oceania.deaths) : print("Die meisten Toten an einem Tag gab es in Asien!")
if np.max(Europe.deaths) > np.max(Africa.deaths) | np.max(Asia.deaths) | np.max(America.deaths) | np.max(Oceania.deaths) : print("Die meisten Toten an einem Tag gab es in Europa!")
if np.max(Oceania.deaths) > np.max(Africa.deaths) | np.max(Asia.deaths) | np.max(Europe.deaths) | np.max(America.deaths) : print("Die meisten Toten an einem Tag gab es in Ozeanien!")
#Vergleich zwischen den Todezahlen insgesamt, simultanes Vorgehen wie oben
if np.sum(America.deaths) > np.sum(Africa.deaths) | np.sum(Asia.deaths) | np.sum(Europe.deaths) | np.sum(Oceania.deaths) : print("Die meisten Toten insgesamt gab es in Amerika!")
if np.sum(Africa.deaths) > np.sum(America.deaths) | np.sum(Asia.deaths) | np.sum(Europe.deaths) | np.sum(Oceania.deaths) : print("Die meisten Toten insgesamt gab es in Afrika!")
if np.sum(Asia.deaths) > np.sum(Africa.deaths) | np.sum(America.deaths) | np.sum(Europe.deaths) | np.sum(Oceania.deaths) : print("Die meisten Toten insgesamt gab es in Asien!")
if np.sum(Europe.deaths) > np.sum(Africa.deaths) | np.sum(Asia.deaths) | np.sum(America.deaths) | np.sum(Oceania.deaths) : print("Die meisten Toten insgesamt gab es in Europa!")
if np.sum(Oceania.deaths) > np.sum(Africa.deaths) | np.sum(Asia.deaths) | np.sum(Europe.deaths) | np.sum(America.deaths) : print("Die meisten Toten insgesamt gab es in Ozeanien!")
#...............
#Infiziertenfälle vergleichen, Simultanes Vorgehen wie oben, nur andere Spalte
print("\n")
print("Übersicht über die Infiziertenzahlen:")
Asien_cases= [[np.mean(Asia.cases)],[np.max(Asia.cases)],[np.min(Asia.cases)],[np.sum(Asia.cases)]]
print("Fälle in Asien:","Mittelwert:",Asien_cases[0],"Maximum:",Asien_cases[1],"Minimum:"
	  ,Asien_cases[2],"Gesamt:",Asien_cases[-1])
Africa_cases= [[np.mean(Africa.cases)],[np.max(Africa.cases)],[np.min(Africa.cases)],[np.sum(Africa.cases)]]
print("Fälle in Afrika:","Mittelwert:",Africa_cases[0],"Maximum:",Africa_cases[1],"Minimum:"
	  ,Africa_cases[2],"Gesamt:",Africa_cases[-1])
America_cases= [[np.mean(America.cases)],[np.max(America.cases)],[np.min(America.cases)],[np.sum(America.cases)]]
print("Fälle in Amerika:","Mittelwert:",America_cases[0],"Maximum:",America_cases[1],"Minimum:"
	  ,America_cases[2],"Gesamt:",America_cases[-1])
Europe_cases= [[np.mean(Europe.cases)],[np.max(Europe.cases)],[np.min(Europe.cases)],[np.sum(Europe.cases)]]
print("Fälle in Europa:","Mittelwert:",Europe_cases[0],"Maximum:",Europe_cases[1],"Minimum:"
	  ,Europe_cases[2],"Gesamt:",Europe_cases[-1])
Oceania_cases= [[np.mean(Oceania.cases)],[np.max(Oceania.cases)],[np.min(Oceania.cases)],[np.sum(Oceania.cases)]]
print("Fälle in Ozeanien:","Mittelwert:",Oceania_cases[0],"Maximum:",Oceania_cases[1],"Minimum:"
	  ,Oceania_cases[2],"Gesamt:",Oceania_cases[-1])
#Vergleich zwischen den geringsten Infiziertenzahlen
print("Vergleich zwischen den Infiziertenzahlen:")
if np.sum(America.cases) > np.sum(Africa.cases) | np.sum(Asia.cases) | np.sum(Europe.cases) | np.sum(Oceania.cases) : print("Die meisten Infektionsfälle insgesamt gab es in Amerika!")
if np.sum(Africa.cases) > np.sum(America.cases) | np.sum(Asia.cases) | np.sum(Europe.cases) | np.sum(Oceania.cases) : print("Die meisten Infektionsfälle insgesamt gab es in Afrika!")
if np.sum(Asia.cases) > np.sum(Africa.cases) | np.sum(America.cases) | np.sum(Europe.cases) | np.sum(Oceania.cases) : print("Die meisten Infektionsfälle insgesamt gab es in Asien!")
if np.sum(Europe.cases) > np.sum(Africa.cases) | np.sum(Asia.cases) | np.sum(America.cases) | np.sum(Oceania.cases) : print("Die meisten Infektionsfälle insgesamt gab es in Europa!")
if np.sum(Oceania.cases) > np.sum(Africa.cases) | np.sum(Asia.cases) | np.sum(Europe.cases) | np.sum(America.cases) : print("Die meisten Infektionsfälle insgesamt gab es in Ozeanien!")
#..................
#Korrelation zwischen Fällen und Tote nach Kontinent und insgesamt mithilfe von np.corrcoef, als interessante Kennzahl
print("\n")
print("(Linearer) Zusammenhang zwischen Todefällen und Infiziertenzahlen:")
Asien_correl=np.corrcoef(Asia.deaths,Asia.cases) #den von numpy Methode genutzten Befehl corrcoef (Quelle:https://benalexkeen.com/correlation-in-python/)
Asien_correl= np.round(Asien_correl, 2) #Den Korrelationskoeffizient auf zwei Kommastellen runden
print("Die Korrelation zwischen Toten und Fällen in Asien ist:",Asien_correl[0,1])
Africa_correl=np.corrcoef(Africa.deaths,Africa.cases) #gleiches Vorgehen bei den anderen
Africa_correl=np.round(Africa_correl, 2)
print("Die Korrelation zwischen Toten und Fällen in Afrika ist:",Africa_correl[0,1])
America_correl=np.corrcoef(America.deaths,America.cases)
America_correl= np.round(America_correl, 2)
print("Die Korrelation zwischen Toten und Fällen in Amerika ist:",America_correl[0,1])
Europe_correl=np.corrcoef(Europe.deaths,Europe.cases)
Europe_correl= np.round(Europe_correl, 2)
print("Die Korrelation zwischen Toten und Fällen in Europa ist:",Europe_correl[0,1])
Oceania_correl=np.corrcoef(Oceania.deaths,Oceania.cases)
Oceania_correl= np.round(Oceania_correl, 2)
print("Die Korrelation zwischen Toten und Fällen in Ozeanien ist:",Oceania_correl[0,1])
world_correl=np.corrcoef(data_new.deaths,data_new.cases)
world_correl= np.round(world_correl, 2)
print("Die Korrelation zwischen Toten und Fällen auf der Welt ist:",world_correl[0,1])
#Ordnen der Korrelationskoeffizienten für die Reihenfolgebeziehung, durch die Funktion sorted (Quelle:https://www.geeksforgeeks.org/python-sort-python-dictionaries-by-key-or-value/)
print("Die geordneten Korrelationen sind aufsteigend:")
Liste_correl= ([ Asien_correl[0,1],Africa_correl[0,1], America_correl[0,1], Europe_correl[0,1], Oceania_correl[0,1] ])
Liste_correl= sorted(Liste_correl)
print(sorted(Liste_correl))
#....................
#4.Gaphische Abbildungen
#Diese habe ich, wie im Video gezeigt, mit package "matplotlib.pyplot" gestaltet
#Graphische Darstellung der Korrelation
import matplotlib.pyplot as plt
#import matplotlib als alternatives package hier nicht gebraucht
plt.scatter(Asia.deaths,Asia.cases, edgecolors="red") #dabei habe ich die Ränder mit rot eingefärbt
plt.xlabel("Todesfälle Asien") # siehe Kommentierungen der Axen
plt.ylabel("Infiziertenzahl Asien")
plt.show()
plt.scatter(Africa.deaths,Africa.cases, edgecolors="green")
plt.xlabel("Todesfälle Afrika")
plt.ylabel("Infiziertenzahl Afrika")
plt.show()
plt.scatter(America.deaths,America.cases, edgecolors="yellow")
plt.xlabel("Todesfälle Amerika")
plt.ylabel("Infiziertenzahl Amerika")
plt.show()
plt.scatter(Europe.deaths,Europe.cases, edgecolors="blue")
plt.xlabel("Todesfälle Europa")
plt.ylabel("Infiziertenzahl Europa")
plt.show()
plt.scatter(Oceania.deaths,Oceania.cases, edgecolors="black")
plt.xlabel("Todesfälle Ozeanien")
plt.ylabel("Infiziertenzahl Ozeanien")
plt.show()
plt.scatter(data_new.deaths,data_new.cases, edgecolors="purple")
plt.xlabel("Todesfälle weltweit" )
plt.ylabel("Infiziertenzahl weltweit")
plt.show()
#...................
#Graphische Darstellung der Entwicklung der Todeszahlen
#Asien vs.Africa
plt.plot(Asia.dateRep,Asia.deaths,'red', label='Asien') # durch die 'label' Funktion lässt sich eine Legende erstellen(wie im Data Camp Video gezeigt)
plt.plot(Africa.dateRep,Africa.deaths,'blue',label='Afrika')
plt.legend()
plt.ylabel("Todesfälle Afrika und Asien")
plt.xlabel("Entwicklung zwischen Januar und April 2020") # die Skalierung ist nicht ganz so schön geworden ...
plt.show()
#.............................
#gleiches Vorgehen wie oben
#Asien vs.Africa vs.Amerika
plt.plot(Asia.dateRep,Asia.deaths,'red', label='Asien')
plt.plot(Africa.dateRep,Africa.deaths,'blue',label='Afrika')
plt.plot(America.dateRep,America.deaths,"green", label="Amerika")
plt.legend()
plt.ylabel("Todesfälle Afrika,Asien und Amerika")
plt.xlabel("Entwicklung zwischen Januar und April 2020")
plt.show()
#..........................
#Welt
plt.plot(Asia.dateRep,Asia.deaths,'red', label='Asien')
plt.plot(Africa.dateRep,Africa.deaths,'blue',label='Afrika')
plt.plot(America.dateRep,America.deaths,"green", label="Amerika")
plt.plot(Europe.dateRep,Europe.deaths,"yellow", label="Europa")
plt.plot(Oceania.dateRep,Oceania.deaths,"black", label="Ozeanien")
plt.legend()
plt.ylabel("Todesfälle weltweit")
plt.xlabel("Entwicklung zwischen Januar und April 2020")
plt.show()
#............................
#Graphische Darstellung der Entwicklung der Fallzahlen
#Asien vs.Africa
plt.plot(Asia.dateRep,Asia.cases,'red', label='Asien')
plt.plot(Africa.dateRep,Africa.cases,'blue',label='Afrika')
plt.legend()
plt.ylabel("Infiziertenfälle Afrika und Asien")
plt.xlabel("Entwicklung zwischen Januar und April 2020")
plt.show()
#.............................
#wieder gleiches Vorgehen,nur andere Variable
#Asien vs.Africa vs.Amerika
plt.plot(Asia.dateRep,Asia.cases,'red', label='Asien')
plt.plot(Africa.dateRep,Africa.cases,'blue',label='Afrika')
plt.plot(America.dateRep,America.cases,"green", label="Amerika")
plt.legend()
plt.ylabel("Infiziertenfälle Afrika,Asien und Amerika")
plt.xlabel("Entwicklung zwischen Januar und April 2020")
plt.show()
#..........................
#Welt
plt.plot(Asia.dateRep,Asia.cases,'red', label='Asien')
plt.plot(Africa.dateRep,Africa.cases,'blue',label='Afrika')
plt.plot(America.dateRep,America.cases,"green", label="Amerika")
plt.plot(Europe.dateRep,Europe.cases,"yellow", label="Europa")
plt.plot(Oceania.dateRep,Oceania.cases,"black", label="Ozeanien")
plt.legend()
plt.title('Entwicklung der Infiziertenfälle weltweit') #der Graphik eine Überschrift geben
plt.ylabel("Infiziertenfälle weltweit")
plt.xlabel("Entwicklung zwischen Januar und April 2020")
plt.show()
print("\n")
#.............................
print("Vielen Dank für den Python-Workshop und die Videos bei DataCamp! Dadurch konnte ich einen tollen,ersten Einblick in Data Science für Python gewinnen!")
print("Beste Grüße, Julian Gerhardt.")

