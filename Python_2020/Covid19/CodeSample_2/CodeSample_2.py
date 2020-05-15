'''
- Bearbeiter: André Bötticher
- notwendige Packages:
    pandas
    numpy
    matplotlib.pyplot
    xlrd

1. Import der Daten
2. Daten Vorbereitung
    a) Index neu setzen
3. Daten untersuchen
    a) FRAGE: gibt es mehrere 'countryterritoryCodes' zu einer 'geoId'?
    b) FRAGE: ist für jedes Land der gleiche Zeitraum abgebildet?
    c) Vergleich von Infektions- und Todeszahlen Kontinente übergreifend
    d) tiefergreifende Analyse bezüglich Europa und europ. Länder - Infektionsraten über die Zeit

'''

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xlrd

# *******************************************************************************************************************************************
# 1. Import der Daten

# Quellpfad bestimmen in Variable: file
file = "COVID-19-geographic-disbtribution-worldwide.xlsx"

# lade excel datei in Variable: xls
xls = pd.ExcelFile(file)

# erstelle Tabelle aus xls: covid
covid = xls.parse()

# zeige die Spaltennamen, die ersten 5 Zeilen und den shape aus covid
print(covid.keys())
print(covid.head())
print("Zeilen, Spalten: " + str(np.shape(covid)))

# *******************************************************************************************************************************************
# 2. Daten Vorbereitung

# a) Index neu setzen
# zeige den Index von covid
print("-->Index DataFrame covid: ")
print(covid.index)
# ->Index von covid ist eine Zahlen-Folge von 0-13221

# Setze hierarchischen Index von Tabelle covid auf 'continentExp' und 'countriesAndTerritories'
covid = covid.set_index(['continentExp', 'countriesAndTerritories'])

# sortiere den MultiIndex: covid
covid = covid.sort_index()

# Zeige das Ergebnis
print("-->DataFrame covid_new mit neuem Index: ")
print(covid.head())

# *******************************************************************************************************************************************
# 3. Daten deskriptiv untersuchen

# a) FRAGE: gibt es mehrere 'countryterritoryCodes' zu einer 'geoId'?:
# Subset der zu untersuchenden Features bilden in Variable: geo_ctc
geo_ctc = covid.loc[:, ['geoId', 'countryterritoryCode']]

# gruppieren von geo_ctc nach 'geoId' und 'countryterritoryCode'; aggregatfunktion erstellt ein Index-Array
by_geoId = geo_ctc.groupby(['geoId','countryterritoryCode']).count()
print("--> by_geoId: ")
print(by_geoId)
#Ergebnis: ein Index-Array, das Wertepaare von 'geoId' und 'countryterritoryCode' enthält

# Index-Array 'by_geoId' zu DataFrame umwandeln
non_index_geoId = by_geoId.reset_index()
print(non_index_geoId)

# Häufigkeiten der Werte aus dem Feature 'geoId' in dictionary speichern: dict_geoId
dict_geoId = non_index_geoId['geoId'].value_counts().to_dict()

# wenn ein Value von geoId öfter als 1x vorkommt wird eine Fehlermeldung gegeben; ansonsten OK
# Zähler "Probe" zeigt Anzahl der verarbeiteten Ergebnisse an. Sollte 201 betragen
Probe=0
for i in dict_geoId.keys():
	if dict_geoId[i] > 1:
		print('ERROR: Mehrere countryterritoryCodes für ',i)
		Probe = Probe+1
	else:
		print('OK: ',i)
		Probe = Probe+1
print("Verarbeitete Fälle: ",Probe)
# ERGEBNIS: jeder countryterritoryCode ist für jede geoId einzigartig.

# 'geoId', 'countryterritoryCode' und 'countriesAndTerritories' enthalten redundante Infos (betrachtetes Land)
# löschen von 'geoId' und 'countryterritoryCode'
covid_new = covid.drop(columns = ['geoId', 'countryterritoryCode'])

# b) FRAGE: ist für jedes Land der gleiche Zeitraum abgebildet?; eignet sich das Datum als Index-Feature?
# Subset der zu untersuchenden Features bilden in Variable: date
date = covid.loc[:, ['dateRep', 'countryterritoryCode']]

# gruppieren von date nach 'countryterritoryCode';
# 'last' Zeigt letzten Eintrag (Beginn der Datenerhebung) eines Landes
beginn_Aufzeichnung = date.groupby(['countryterritoryCode']).last()
print("-->Beginn Aufzeichnung: ")
print(beginn_Aufzeichnung)

# 'first' Zeigt letzten Eintrag (Ende der Datenerhebung) eines Landes
ende_Aufzeichnung = date.groupby(['countryterritoryCode']).first()
print("-->Ende Aufzeichnung: ")
print(ende_Aufzeichnung)
# ERGEBNIS: Die Länder beginnen zu unterschiedlichen Zeitpunkten mit der Erhebung von Daten.
#           --> Datum als weiterer Index für DataFrame 'covid' scheidet aus
#           --> daraus resultierende "fehlende Werte" werden nicht weiter berücksichtigt, da
#               diese sowieso gelöscht oder mit 0 erstetzt würden

# c) Vergleich von Infektions- und Todeszahlen Kontinentübergreifend
# summiere die verstorbenen Patienten pro Kontinent: deaths_continent
deaths_continent = covid_new.deaths.groupby(['continentExp']).sum()

# kumuliere die Infektionen pro Kontinent: infected_continent
infected_continent = covid_new.cases.groupby(['continentExp']).sum()

# errechne das Verhältnis zwischen Infektionen und Todesfällen
ratio = []
for i in range(len(deaths_continent)):
	ratio.insert(i, ((deaths_continent[i] / infected_continent[i])*100))

# visualisiere die Zahlen
# linker Plot (Infektionen)
plt.subplot(2, 2, 1)
# Anzahl der Kontinente
N = 6

# erstelle array mit Zahlen von 1-6
x = np.arange(N)

# Barchart mit Beschriftungen erstellen
p1 = plt.bar(x, height=infected_continent)
plt.ylabel('Infektionen')
plt.title('Infektionen pro Kontinent (in mio.)')
plt.xticks(x, ('Africa', 'America', 'Asia', 'Europe', 'Oceania','Other'))

# mittlerer Plot (Todeszahlen)
plt.subplot(2, 2, 2)
N = 6
x = np.arange(N)
p1 = plt.bar(x, height=deaths_continent)
plt.ylabel('Todesfälle')
plt.title('Todesfälle pro Kontinent')
plt.xticks(x, ('Africa', 'America', 'Asia', 'Europe', 'Oceania','Other'))

# rechter Plot (Verhältnis von Toden zu Infektionen)
plt.subplot(2, 2, 3)
N = 6
x = np.arange(N)
p1 = plt.bar(x, height=ratio)
plt.ylabel('Sterberate in %')
plt.title('Sterberate')
plt.xticks(x, ('Africa', 'America', 'Asia', 'Europe', 'Oceania','Other'))

# Plots ausrichten und ausgeben
plt.tight_layout()
plt.show()
# ERGEBNIS: Von allen Kontinenten hat Europa die höchste Sterberate -
# weitere Analysen beziehen sich auf Europa!

# d) tiefergreifende Analyse bezüglich Europa und europ. Länder - Infektionsraten über die Zeit
# Vergleich der Länder bezüglich Neu-Infizierter über Datenerhebungszeitraum
# Filtern von covid_neu nach Europa in: covid_europ
covid_europ = covid_new.loc['Europe',('dateRep', 'cases')]

# FRAGE: welche 20% der Länder weisen (mindestens) 80% der Europäischen Corona Fälle auf?
# aggregieren von covid_europ um Anzahl der Fälle pro Land zu finden
twy_perc_nonIndex = covid_europ.groupby('countriesAndTerritories').sum().reset_index()

# wie viele Länder sind 20% der europ. Länder?
perc_land = ((len(twy_perc_nonIndex.countriesAndTerritories)*0.2))
print ("zu betrachtende Zahl der Länder (20%): ", np.trunc(perc_land))

# nach Fallzahlen geordnete Ausgabe der europ. Länder
Land_sort = twy_perc_nonIndex.sort_values(by = 'cases', ascending=False)
print(Land_sort)

#füge neue Spalte mit Index für sortierte Länder ein: idx
N = len(Land_sort)
Land_sort['idx'] = np.arange(N)

# Setze  Index von Tabelle Land_sort auf 'idx'
Land_sort = Land_sort.set_index(['idx'])
print(Land_sort)

# Gesamtinfektionen für Europe in Variable speichern: total
total = infected_continent['Europe']

# welchen Anteil der Gesamtinfektionen machen die 10 ersten Länder der sortierten Liste aus?
ratio_europe = 0
for i in range(10):
	ratio_europe = ratio_europe + Land_sort.loc[i,'cases']

# Speichern der 10 Meistinfizierten Länder in Tupel: twty_perc
twty_perc = []
for i in range(10):
	twty_perc.insert(i, Land_sort.loc[i, 'countriesAndTerritories'])
print("Die 10 Meistinfizierten Länder machen ",(ratio_europe/total)*100,"% der Infektionen in Europa aus.")
# ERGEBNIS: 86% der Infektionen in Europa lassen sich auf 10 Länder zurückführen

# Für diese 10 Länder werden deskriptive Statistiken bezügl. der täglichen Neuinfektionen ausgegeben
for i in twty_perc:
	slice = covid_europ.loc[i, 'cases']
	summarize_case = pd.DataFrame.describe(slice)
	print(i,": ",summarize_case)
# ERGEBNIS: Spanien und Portugal haben negatives minimum für Neuinfektionen -> unmöglich, min===0
#           --> negatives Value wird durch Mittelwert des vor- und nachgelagerten Wertes ersetzt

# Falsche (negative) Werte ersetzen
# Index von covid_europ zurücksetzen -> automatischer Index wird erstellt
covid_eu_NonIndex = covid_europ.reset_index()

# neue, leere Liste erstellen: cases_new
cases_new=[]

# cases_new ausfüllen
for i in range(len(covid_eu_NonIndex)):

	# einzelnen Wert aus Tabelle covid_eu_NonIndex abspeichern in: Value
	Value = covid_eu_NonIndex.loc[i, 'cases']

	# wenn dieser Wert kleiner null:
	if Value < 0:

		#Ersatzwert errechnen
		summand1 = covid_eu_NonIndex.loc[i - 1, 'cases']
		summand2 = covid_eu_NonIndex.loc[i + 1, 'cases']
		Ersatzwert = (summand1+summand2)/2

		# Value durch Ersatzwert ersetzen
		zu_ersetzender_Wert = Value
		Value = Ersatzwert

		# ersetzten Wert in 'cases_new' speichern
		cases_new.append(Value)
		print("Ersetzter Wert: ", zu_ersetzender_Wert, " durch: ", Value)

	# wenn dieser Wert größer null:
	else:

		# Wert in 'cases_new' speichern
		cases_new.append(Value)

# Liste 'cases_new' zu Dataframe 'covid_eu_NonIndex' hinzufügen
covid_eu_NonIndex['cases_new'] = cases_new

# Index auf 'countriesAndTerritories' setzen in neuer Dataframe: covid_eu
covid_eu = covid_eu_NonIndex.set_index('countriesAndTerritories')

# Plotte die 10 Länder in einem Diagramm
for i in twty_perc:
	# X-Achse ist der Tag
	X = covid_eu.loc[i,'dateRep']

	#Y-Achse ist die Fallzahl am Tag
	Y = covid_eu.loc[i,'cases_new']
	plt.plot(X,Y, label=i)

# Legende dazu
plt.legend(loc='upper left')

# x-Ticks ausrichten und plot ausgeben
spain = covid_europ.loc['Spain'] #SPAIN NACHSCHAUEN
print(spain.loc[spain['dateRep'] > '2020-04-10'])

plt.xticks(rotation=60)
plt.show()
# *******************************************************************************************************************************************