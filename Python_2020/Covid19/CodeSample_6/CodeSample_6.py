###########################################################################################################
########################################## Python Kurs Projekt ############################################
###########################################################################################################

# Nico Kleinschroth
#
# imports für die Datenbearbeitung...

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# CSV Datei öffnen
# Trennzeichen ";" weil "," in manchen Namen verwendet wird. Erste Spalte mit Datum wird hier als Datum umgewandelt.
data = pd.read_csv("COVID-19-geographic-disbtribution-worldwide.csv", delimiter=";", parse_dates=["dateRep"], date_parser=lambda x: datetime.strptime(x, '%d.%m.%Y'))

# Auffällt, dass es bei "popData2018" 161 fehlende Werte gibt.
# Dies betrifft insgesamt  5 Länder.
# Der vollständigkeitshalber (auch weil ich später mit diesem Wert rechne) wird im Folgenden diesen ein Wert von Google hinzugefügt.
# Alternativ werden diese 5 Länder später nicht berücksichtigt.

if pd.isnull(data[data["countriesAndTerritories"] == "Anguilla" ]["popData2018"].max()):
	data.loc[data.countriesAndTerritories == "Anguilla", "popData2018"] = 15094

if pd.isnull(data[data["countriesAndTerritories"] == "Bonaire, Saint Eustatius and Saba" ]["popData2018"].max()):
	data.loc[data.countriesAndTerritories == "Bonaire, Saint Eustatius and Saba", "popData2018"] = 24548

if pd.isnull(data[data["countriesAndTerritories"] == "Falkland_Islands_(Malvinas)" ]["popData2018"].max()):
	data.loc[data.countriesAndTerritories == "Falkland_Islands_(Malvinas)", "popData2018"] = 2840

if pd.isnull(data[data["countriesAndTerritories"] == "Eritrea" ]["popData2018"].max()):
	data.loc[data.countriesAndTerritories == "Eritrea", "popData2018"] = 3214000

if pd.isnull(data[data["countriesAndTerritories"] == "Western_Sahara" ]["popData2018"].max()):
	data.loc[data.countriesAndTerritories == "Western_Sahara", "popData2018"] = 597000

# Naturlich reagiert dieser Code nicht dynamisch auf zukünftige fehlende Daten (leider).

# Auch bei geoId und countryterritoryCode fehlen Werte, doch ich verwende diese nicht da es bei jedem einen Ländernamen gibt.
# Außerdem sind nicht für jedes Land gleich viele Tage vorhanden. Also wurden nicht bei jedem Land täglich ab dem 31.12 Daten erfasst...

###########################################################################################################
######################################## Aufteilung nach Ländern ##########################################
###########################################################################################################

# Jetzt wird der Datensatz auf die Länder aufgeteilt und dabei die Fall- und Todeszahlen zusammengezählt und in CountryData gespeichert.
# Dabei soll der Name des Landes nicht als index verwendet werden, damit ich später besser mit diesem arbeiten kann.
CountryData = data.groupby(["countriesAndTerritories"], as_index = False)[["deaths","cases"]].sum()

CountryData = CountryData.loc[CountryData["cases"] > 0] # Keine unötigen Daten.

# Ausreßerbehandlung mit Quantilen: Diese werden entfernt.
low = 0.05 # Unteres Quantil Ende
high = 0.7 # Oberes Quantil Ende
CountryData = CountryData.loc[CountryData["cases"] > CountryData["cases"].quantile(q=low)]
CountryData = CountryData.loc[CountryData["cases"] < CountryData["cases"].quantile(q=high)]


# Erstellung von Listen für die folgende Berechnung der jeweiligen Mortalitätsrate,
# Sterberate im Vergleich zur gesamten Bevölkerung und prozentuale Fallzahlen zur Bevölkerung.
deathspercent = []
deathspercentoftotal = []
casepercent = []

# Hier wird der gesamte CountryData Datensatz durchlaufen und jeweils die Raten berechnet und den zugehörigen Listen hinzugefügt.
for i in range(0,len(CountryData)):
	# Mortalitätsrate = Todeszahlen / Fallzahlen
	deathspercent.append(CountryData.iloc[i]["deaths"]/CountryData.iloc[i]["cases"])
	# Mortalitätsrate im Vergleich zur gesamten Bevölkerung (Todezahlen / Bevölkerung)
	deathspercentoftotal.append(CountryData.iloc[i]["deaths"]/data[data["countriesAndTerritories"] == CountryData.iloc[i]["countriesAndTerritories"] ]["popData2018"].max())
	# Wie viel Prozent der Bevölkerung sind infiziert. (Fallzahlen / Bevölkerung)
	casepercent.append(CountryData.iloc[i]["cases"]/data[data["countriesAndTerritories"] == CountryData.iloc[i]["countriesAndTerritories"] ]["popData2018"].max())

# Anschließend werden die Listen dem Datensatz hinzugefügt (Neue Spalten).
CountryData.insert(2, "deathspercent", deathspercent)
CountryData.insert(3, "deathspercentoftotal", deathspercentoftotal)
CountryData.insert(5, "casepercent", casepercent)


# Auch hier werden nochmal extreme Ausreißer herausgenommen.
CountryData = CountryData.loc[CountryData["deathspercentoftotal"] < CountryData["deathspercentoftotal"].quantile(q=0.95)]
CountryData = CountryData.loc[CountryData["casepercent"] < CountryData["casepercent"].quantile(q=0.95)]

# Hier werden die Fallzahlen im verhältnis zur Bevölkerung der Länder in Bins aufgeteilt. 30 Bins
casepercentbins = CountryData
casepercentbins.insert(1,"casepercentbins", pd.cut(casepercentbins["casepercent"], bins=30, right= False))
casepercentbins = casepercentbins.groupby(["casepercentbins"], as_index = False).count()

# Hier wird jetzt noch die Mortalitätsrate gebinned. 10 Bins
deathspercentbins = CountryData
deathspercentbins.insert(1,"deathspercentbins", pd.cut(deathspercentbins["deathspercent"], bins=10, right= False))
deathspercentbins = deathspercentbins.groupby(["deathspercentbins"], as_index = False).count()

# Analog zu den Ländern könnte man dies auch auf Kontinente oder die gesamte Welt anwenden...

############################################# Visualisierung ##############################################

# Mortalitätsraten Bin Graph, klar erkennbare Abflachung
# Logarithmische Verteilung
# Ausreißer sind nicht dabei.
mortality = plt.figure()

# Beschriftungs Liste erstellen
labels = []

# Die Bin Grenzen der x-Achsen Beschriftung hinzufügen, dabei Zeichen ausblenden für ein schöneres Ergebnis
for i in range(0,len(deathspercentbins["deathspercentbins"])):
	labels.append(str(deathspercentbins["deathspercentbins"][i]).replace(",","\n").replace("(","").replace(")","").replace("]","").replace("[",""))

# Die Beschriftungsgröße festlegen.
plt.rc('xtick', labelsize = 8)

# Die Balken für die Mortalitätsraten.
plt.bar(labels, deathspercentbins["deaths"], label="deathspercent")


# Beschriftungen.
plt.title("Mortality rate of countries (10 Bins)")
plt.ylabel("Number of countries")
plt.xlabel("Deaths/Cases")


# Anzeigen des zweiten Graphen
mortality.show()

###########################################################################################################

# Fallzahlen im Verhältnis zur Bevölkerung.
# Diesesmal kein Histogramm, sondern Linie für ein alternative Darstellung.
# Ausreißer sind nicht dabei.
casepercentgraph = plt.figure()

# Neue Beschriftungsliste
labels2 = []

# 6 Beschriftungen sollen angezeigt werden
xtickspos = 6

# Die Bin Grenzen werden aufgeteilt und der Beschriftung hinzufügt, dabei Zeichen ausblenden für ein schöneres Ergebnis.
for i in range(0, xtickspos-1):
	labels2.append(str(casepercentbins["casepercentbins"][i * xtickspos]).lstrip("()[].1234567890-e ").replace(",","").replace("(","").replace(")","").replace("]","").replace("[",""))
labels2.append(str(casepercentbins["casepercentbins"].iloc[-1]).lstrip(" ()[].1234567890-e").replace(",","").replace("(","").replace(")","").replace("]","").replace("[",""))


# Die Linie für Fallzahlen im verhältnis zur Bevölkerung.
plt.plot(casepercentbins["cases"])

# Beschriftungen.
plt.title("Cases in proportion to population (30 Bins)")
plt.ylabel("Number of countries")
plt.xticks([0,6,12,18,24,30], labels2)
plt.xlabel("Cases/Population")

# Anzeigen des Graphen
casepercentgraph.show()

# Logarithmisch-Artige Verteilung

###########################################################################################################

# Boxplots mit Statistiken zu den erstellten Werten. Subplots für eine etwas übersichtlichere Darstellung.
# Ausreißer sind nicht dabei.

# Erstellen der Figur mit Subplots.
boxplots, ax = plt.subplots(3,2)

# Die jewiligen Subplots
ax[0][0].boxplot(CountryData["cases"], labels= ["cases"])
ax[0][1].boxplot(CountryData["casepercent"], labels= ["cases in proportion to population"])
ax[1][0].boxplot(CountryData["deaths"], labels= ["deaths"])
ax[1][1].boxplot(CountryData["deathspercent"], labels= ["mortality rate"])
ax[2][0].boxplot(CountryData["deathspercentoftotal"], labels= ["deaths in proportion to population"])


# min, max, mean, std Beschriftung der Werte. (Mit angepassten Nachkommerstellen)
boxplottext1 = ("deaths" +
				"\n" + "min: " + str(format(CountryData["deaths"].min(),".0f")) +
				"  max: " + str(format(CountryData["deaths"].max(),".0f")) +
				"\n" + "mean: " + str(format(CountryData["deaths"].mean(),".2f")) +
				"\n" + "std: " + str(format(CountryData["deaths"].std(),".2f")) +
				"\n" + "\n" + "mortality rate" +
				"\n" + "min: " + str(format(CountryData["deathspercent"].min(),".2f")) +
				"  max: " + str(format(CountryData["deathspercent"].max(),".2f")) +
				"\n" + "mean: " + str(format(CountryData["deathspercent"].mean(),".4f")) +
				"\n" + "std: " + str(format(CountryData["deathspercent"].std(),".4f")) +
				"\n" + "\n" + "deaths/population" +
				"\n" + "min: " + str(format(CountryData["deathspercentoftotal"].min(),".2f")) +
				"  max: " + str(format(CountryData["deathspercentoftotal"].max(),".6f")) +
				"\n" + "mean: " + str(format(CountryData["deathspercentoftotal"].mean(),".8f")) +
				"\n" + "std: " + str(format(CountryData["deathspercentoftotal"].std(),".8f")))

boxplottext2 = ("cases" +
				"\n" + "min: " + str(format(CountryData["cases"].min(),".0f")) +
				"  max: " + str(format(CountryData["cases"].max(),".0f")) +
				"\n" + "mean: " + str(format(CountryData["cases"].mean(),".2f")) +
				"\n" + "std: " + str(format(CountryData["cases"].std(),".2f")) +
				"\n" + "\n" + "cases/population" +
				"\n" + "min: " + str(format(CountryData["casepercent"].min(),".2f")) +
				"  max: " + str(format(CountryData["casepercent"].max(),".4f")) +
				"\n" + "mean: " + str(format(CountryData["casepercent"].mean(),".4f")) +
				"\n" + "std: " + str(format(CountryData["casepercent"].std(),".4f")))

# Hinzufügen der Beschriftung zum letzten Graphen und ausblenden der Achsen.
plt.text(0, 1, boxplottext1, fontsize = 7, verticalalignment = "top")
plt.text(0.5, 1, boxplottext2, fontsize = 7, verticalalignment = "top")
plt.axis('off')

# Die Figur enger machen, damit Zahlen nicht in andere Graphen überlappen.
boxplots.tight_layout()

# Anzeigen der Boxplots
boxplots.show()

###########################################################################################################
######################### Gesamte Fallzahlen zu Fallzahlen vergangener Woche ##############################
###########################################################################################################

# Hier wird nun eine neues Dataframe erzeugt mit allen Ländern und deren Fallzahlen aufsummiert. (Ohne Ausreißerbehandlung)
PastWeek = data.groupby(["countriesAndTerritories"], as_index = False)[["cases"]].sum()

# Neue Liste für die Fallzahlen von letzter Woche
caseslastweek = []

# Alle Länder im Dataframe werden durchlaufen.
for i in range(0,len(PastWeek)):
	# Neues platzhalter Dataframe wird für das jeweils gerade "aktive" Land erstellt.
	placeholderdata = data.loc[data["countriesAndTerritories"] == PastWeek["countriesAndTerritories"][i]]
	# Dem ph Dataframe wird nun anhand der Spalte "dateRep" also einem Datum eine neue Spalte "weekday" mit dem jeweiligen Wochentag hinzugefügt.
	# 0 = Montag, 1= Dienstag usw.
	placeholderdata.insert(1,"weekday",placeholderdata["dateRep"].dt.dayofweek)
	# Zur Sicherheit nochmal nach dem Datum sortiert.
	placeholderdata = placeholderdata.sort_values(["dateRep"])
	# Jetzt wird auch nochmal zur Sicherheit überprüft ob eine ganze Woche überhaupt vorhanden ist. (0,1,2,3,4,5,6 = 21)
	# Zu bemerken ist, dass Pandas das Datum so sortiert, dass das neuste an letzter Stelle steht daher .tail statt .head
	if placeholderdata["weekday"].tail(7).sum() == 21:
		# Nun wird der Wert der Liste hinzugefügt.
		caseslastweek.append(placeholderdata["cases"].tail(7).sum())
	else:
		# Keine ganze Woche vorhanden -100000000000 um es eindeutig zu erkennen.
		caseslastweek.append([-100000000000])

	# Nun wird die Liste dem Dataframe hinzugefügt als neue Spalte "caseslastweek"
PastWeek.insert(2, "caseslastweek", caseslastweek)

# Alle Länder ohne ganze Woche werden entfernt.
PastWeek = PastWeek.loc[PastWeek["caseslastweek"] != -100000000000]

# Hier wird der Verlauf von Deutschland in der gesamten Corona Krise nochmal berechnet.
# Neues Dataframe
germanycurve =  data.loc[data["countriesAndTerritories"] == "Germany"]

# Listen der jeweiligen gesamt Fälle und Fälle der letzten Woche für jeden Tag
TrendWeekCases = []
TrendTotalCases =[]

# Durchlauf der gesamten Daten (jeden Tag)
for i in range(0,len(germanycurve)):
	# Die Tage an denen es noch kein Corona in DE gab herausgenommen.
	if germanycurve["cases"].sum() > 1:
		# Die jeweilige gesamt Fallzahl
		TrendTotalCases.append(germanycurve["cases"].sum())
		# Die letzten 7 Tage
		TrendWeekCases.append(germanycurve["cases"].head(7).sum())
	# Der Tag, der gerade in der For-Schleife behandelt wurde, wird nun entfernt.
	germanycurve = germanycurve.tail(-1)

############################################# Visualisierung ##############################################

# Gesamt Fallzahlen im vergleich zu Fallzahlen vergangener Woche Graph.

# Erstellen einer neuen Figur.
covid19 = plt.figure()

# Scatterplot für alle Länder für den letzten Stand.
plt.scatter(PastWeek["cases"],PastWeek["caseslastweek"], alpha=0.5 , label="other Countries")
# Scatterplot nur für DE und US für den letzten Stand. Damit man diese besser erkennt.
plt.scatter(PastWeek[PastWeek["countriesAndTerritories"] == "Germany" ]["cases"],PastWeek[PastWeek["countriesAndTerritories"] == "Germany" ]["caseslastweek"], label= "Germany", color="green")
plt.scatter(PastWeek[PastWeek["countriesAndTerritories"] == "United_States_of_America" ]["cases"],PastWeek[PastWeek["countriesAndTerritories"] == "United_States_of_America" ]["caseslastweek"], label= "USA")

# Hilfslinie
plt.plot([1,PastWeek["cases"].max()],[1,PastWeek["cases"].max()],'r--' , alpha=0.5)

# Der Verlauf von DE mit den zwei Listen als Werte.
plt.plot(TrendTotalCases, TrendWeekCases, color= "green", label="Trend of Germany", alpha=0.8)

# logarithmische skala damit alle Länder besser dargestellt werden.
plt.xscale('log')
plt.yscale('log')
# Beschriftungen
plt.title("Countries COVID-19 " + "(" + str(data.sort_values(["dateRep"], ascending=False,).iloc[0]["dateRep"]).rstrip("0:") + ")")
plt.ylabel("New Cases in the Past Week")
plt.xlabel("Total Cases")
plt.legend()

# Anzeigen der Figur
covid19.show()

###########################################################################################################
############################## Prozentuale Fallzahlen im Zeitverlauf ######################################
###########################################################################################################

# Zwei neue Listen für die Zahlen der zwei Länder.
casesagg = []
casesagg2 = []

# Alle Tage von DE nach Datum sortiert.
placeholderdata = data[data["countriesAndTerritories"] == "Germany" ]
placeholderdata = placeholderdata.sort_values(["dateRep"])
# Aggregierter Wert wird der Liste hinzugefügt.
for i in range(1,len(placeholderdata) + 1):
	casesagg.append(placeholderdata["cases"].head(i).sum())

# Umwandlung in numpy array und durch Bevölkerung teilen, um Werte vergleichbar zu machen zwischen den Ländern.
casesagg = np.array(casesagg)
casesagg = casesagg / data[data["countriesAndTerritories"] == "Germany" ]["popData2018"].max()

# Analog für die USA.
placeholderdata = data[data["countriesAndTerritories"] == "United_States_of_America" ]
placeholderdata = placeholderdata.sort_values(["dateRep"])
for i in range(1,len(placeholderdata) + 1):
	casesagg2.append(placeholderdata["cases"].head(i).sum())

casesagg2 = np.array(casesagg2)
casesagg2 = casesagg2 / data[data["countriesAndTerritories"] == "United_States_of_America" ]["popData2018"].max()

############################################# Visualisierung ##############################################

# Erstellen der Figur
casesovertime = plt.subplots()

# Sortierung nach Datum damit es gleich richtig angezeigt wird.
data = data.sort_values("dateRep")

# Die zwei Linien für die Länder
plt.plot(data[data["countriesAndTerritories"] == "Germany" ]["dateRep"],casesagg, label= "Germany")
plt.plot(data[data["countriesAndTerritories"] == "United_States_of_America" ]["dateRep"],casesagg2 , label = "United States of America")

# Beschriftungen.
plt.title("Percentage of cases over time")
plt.ylabel("cases/population")
plt.legend()

# X-Achse erst ab März
plt.xlim(left =datetime.strptime("01.03.2020", '%d.%m.%Y'))

# X-Achsen Beschriftung rotieren
plt.xticks(rotation=45)
plt.tight_layout()

# Anzeigen des Graphen
plt.show()

###########################################################################################################