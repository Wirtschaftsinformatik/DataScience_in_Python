#
# Author: Sebastian Wolf
import pandas as pd                                 #Importieren der notwendigen Bibliotheken
import matplotlib.pyplot as plt

data = pd.read_csv('CoronaDaten.csv')               #Einlesen der Daten aus Excel in ein DataFrame
df = pd.DataFrame(data)

del df['day']                                       #Löschen nicht benötigter Spalten
del df['month']
del df['year']
del df['geoId']

df['dateRep'] = pd.to_datetime(df['dateRep'], dayfirst= True, errors='coerce')  #Transformation des Datums in die Form: year-month-day

df_neu = df.rename(columns={'dateRep':'date', 'popData2018':'population2018' }) #Umbenennen von Spalten

cases_sum = df_neu['cases'].sum()                                   #berechnet Summe der weltweiten Fälle
deaths_sum = df_neu['deaths'].sum()                                 #berechnet Summe der weltweiten Todesfälle
continents = df_neu.groupby('continentExp').sum()                   #berechnet für jeden Kontinent die Summe aller Spalten

share_in_total_number_cases = continents['cases']/cases_sum         #Anteile der Fallzahlen jedes Kontinents an den weltweiten Fallzahlen
share_in_total_number_deaths = continents['deaths']/deaths_sum      #Anteile der Todesfälle jedes Kontinents an den weltweiten Todesfällen
exArray = [0.2, 0.05, 0.05, 0.05, 0.3, 0.5]                         #Array, welcher die Abstände der einzelnen Kreisstücke zum Mittelpunkt enthält

#Für die Visualisierung der anteiligen Fallzahlen der Kontinente an den Fallzahlen weltweit
#ist das Kreisdiagramm sehr gut geeignet.
plt.style.use('bmh')                                                                        #Verwendung des Designs 'bmh'
plt.subplot(1,2,1)                                                                          #Angabe der Stelle, wo erstes Subplot dargestellt werden soll.
plt.pie(share_in_total_number_cases, explode=exArray, shadow=True, radius=1.2)              #Kreisdiagramm wird erstellt. Mit dem Argument explode
plt.title('Verteilung der Fallzahlen\n nach Kontinenten', size=10, fontweight='bold')       #werden die Teilstücke entsprechend ihres vorher definierten
plt.legend(continents.index, bbox_to_anchor=[0.2, 0.1])                                     #Abstandes vom Mittelpunkt des Kreisdiagramms dargestellt.
                                                                                            #Legende hinzufügen, bbox_to_anchor definiert die Position der Legende
#Analog zu dem ersten Kreisdiagramm (Hier: Darstellung der anteiligen Todesfälle)
plt.subplot(1,2,2)                                                                          #Zweites Subplot an Stelle 2
plt.pie(share_in_total_number_deaths, explode=exArray, shadow=True, radius=1.2)             #Zweites Kreisdiagramm wird erstellt
plt.title('Verteilung der Todesfälle\n nach Kontinenten', size=10, fontweight='bold')       #Titel hinzufügen (analog beim ersten Kreisdiagramm)
plt.show()                                                                                  #Erst jetzt Anzeigen der Plots, damit beide im gleichen Plot dargestellt werden.

#Extrahieren der benötigten Daten für Deutschland, Italien, China und die USA
#Deutschland
dataGer = df_neu.loc[df_neu['countriesAndTerritories']=='Germany']                  #Mit loc-Funktion Zugriff auf gewünschte Spalte.
xGer = dataGer['date']                                                              #Durch den Gleichheitsausdruck werden nur die Daten für Deutschland extrahiert.
cases_Ger = dataGer['cases']                                                        #Speichern der Werte für x- und y-Achse in extra Variablen (für spätere Plots hilfreich).
deaths_Ger = dataGer['deaths']
#Italien
dataItaly = df_neu.loc[df_neu['countriesAndTerritories']=='Italy']                  #Analog zu Deutschland
xItaly = dataItaly['date']
cases_Italy = dataItaly['cases']
deaths_Italy = dataItaly['deaths']
#China
dataChina = df_neu.loc[df_neu['countriesAndTerritories']=='China']                  #Analog zu Deutschland
xChina = dataChina['date']
cases_China = dataChina['cases']
deaths_China = dataChina['deaths']
#USA
dataUSA = df_neu.loc[df_neu['countriesAndTerritories']=='United_States_of_America'] #Analog zu Deutschland
xUSA = dataUSA['date']
cases_USA = dataUSA['cases']
deaths_USA = dataUSA['deaths']

#Darstellung der Entwicklung der Fallzahlen der vier Länder in einem Liniediagramm.
#Ein Liniendiagramm ist dafür besonders geeignet, weil dadurch Anstiege/Abstiege gut nachvollziehbar sind.
#Außerdem lassen sich die Entwicklungen mehrerer Länder gleichzeitig darstellen, ohne dass das Diagramm an Übersichtlichkeit verliert.
plt.style.use(i)
plt.plot(xGer, cases_Ger, color='red', label='Germany')                         #Erstellung der vier Liniendiagramme
plt.plot(xItaly, cases_Italy, color='green', label='Italy')
plt.plot(xChina, cases_China, color='orangered', label='China')
plt.plot(xUSA, cases_USA, color='blue', label='USA')
plt.title('Gegenüberstellung der Fallzahlen', fontweight='bold')
plt.xticks(rotation=45)                                                         #Rotiert das Datum um 45 Grad um Überlagerungen zu vermeiden.
plt.legend()
plt.show()

plt.style.use('bmh')
plt.plot(xGer, deaths_Ger, color='red', label='Germany')                        #Analog zum vorherigen Liniendiagramm.
plt.plot(xItaly, deaths_Italy, color='green', label='Italy')                    #Hier werden die Verläufe der Todesfälle dargestellt.
plt.plot(xChina, deaths_China, color='orangered', label='China')
plt.plot(xUSA, deaths_USA, color='blue', label='USA')
plt.title('Gegenüberstellung der Todeszahlen', fontweight='bold')
plt.xticks(rotation=45)
plt.legend()
plt.show()

#Extrahieren der Daten für Frankreich und Russland
#Frankreich
dataFrance = df_neu.loc[df_neu['countriesAndTerritories']=='France']
xFrance = dataFrance['date']
cases_France = dataFrance['cases']
deaths_France = dataFrance['deaths']
#Russland
dataRussia = df_neu.loc[df_neu['countriesAndTerritories']=='Russia']
xRussia = dataRussia['date']
cases_Russia = dataRussia['cases']
deaths_Russia = dataRussia['deaths']

#Herausfinden, wie hoch das Maximum der Todesfälle über den gesamten Zeitraum der Datenerhebung für die sechs ausgewählten Länder ist.
max_deaths_Ger = max(deaths_Ger)
max_deaths_Italy = max(deaths_Italy)
max_deaths_China = max(deaths_China)
max_deaths_USA = max(deaths_USA)
max_deaths_France = max(deaths_France)
max_deaths_Russia = max(deaths_Russia)

#Listenerstellung für die x und y Argumente des Histogramms.
max_deaths = [max_deaths_Ger, max_deaths_Italy, max_deaths_China, max_deaths_USA, max_deaths_France, max_deaths_Russia]
countryID = ['DEU', 'ITA', 'CHN', 'USA', 'FRA', 'RUS']

#Gegenüberstellung der Maxima der Todesfälle der sechs Länder in einem Histogramm.
#Statistisch ist dieses Diagramm nicht sonderlich aussagekräftige, aber es zeigt eine weitere Variante der Visualisierung, die mit Matplotlib möglich ist.
plt.bar(countryID, max_deaths, color='darkred')
plt.title('Höchste Anzahl Todesopfer an einem Tag', size=14, fontweight='bold')
plt.show()

#Berechnung der durchschnittlichen Fallzahlen und Todesfällen der sechs Länder und speichern in jeweils einer Liste.
mean_cases = [cases_Ger.mean(), cases_Italy.mean(), cases_China.mean(), cases_USA.mean(), cases_France.mean(), cases_Russia.mean()]
mean_deaths = [deaths_Ger.mean(), deaths_Italy.mean(), deaths_China.mean(), deaths_USA.mean(), deaths_France.mean(), deaths_Russia.mean()]
#Berechnungen der Todesraten der sechs Länder.
mean_deathrate_Ger = round((mean_deaths[0]/mean_cases[0]).mean()*100, 1)
mean_deathrate_Italy = round(mean_deaths[1]/mean_cases[1].mean()*100, 1)
mean_deathrate_China = round(mean_deaths[2]/mean_cases[2].mean()*100, 1)
mean_deathrate_USA = round(mean_deaths[3]/mean_cases[3].mean()*100, 1)
mean_deathrate_France = round(mean_deaths[4]/mean_cases[4].mean()*100, 1)
mean_deathrate_Russia = round(mean_deaths[5]/mean_cases[5].mean()*100, 1)

#Darstellung der durchschnittlichen Fallzahlen nach Land.
#Und Darstellung der durchscnittlichen Todesfälle nach Land in der gleichen Säule.
#Diese Darstellung dient der Veranschaulichung des Anteils der Todesfälle an den gesamten Fallzahlen für jedes der sechs Länder.
plt.bar(['Germany', 'Italy', 'China', 'USA', 'France', 'Russia'], height=mean_cases, label='cases', color='darkcyan')
plt.bar(['Germany', 'Italy', 'China', 'USA', 'France', 'Russia'], height=mean_deaths, label='deaths', color='darkred')
plt.title('Mittlere Fallzahlen und anteilige mittlere Todesfälle\n (Mittlere Todesraten in Prozent)', fontweight='bold')
plt.annotate('deathrates:', ('Germany', 10500), size=10, fontweight='bold')            #Zusätzlich ist in diesem Histogramm eine Übersicht
plt.annotate('Germany: ' + str(mean_deathrate_Ger)+ '%', ('Germany', 9500))            #der Todesraten der sechs Länder enthalten.
plt.annotate('Italy: ' + str(mean_deathrate_Italy)+ '%', ('Germany', 8500))            #Mit plt.annotate kann man ganz einfach einen Print
plt.annotate('China: ' + str(mean_deathrate_China)+ '%', ('Germany', 7500))            #in das Diagramm einfügen.
plt.annotate('USA: ' + str(mean_deathrate_USA)+ '%', ('Germany', 6500))
plt.annotate('France: ' + str(mean_deathrate_France)+ '%', ('Germany', 5500))
plt.annotate('Russia: ' + str(mean_deathrate_Russia)+ '%', ('Germany', 4500))
plt.legend()
plt.show()

#Um einen Überblick über den erkrankten Anteil der Bevölkerung zu erhalten, wurden im folgenden Code die mittleren
#Bevölkerungszahlen der sechs Länder in Variablen abgespeichert.
popGer = dataGer['population2018'].mean()
popItaly = dataItaly['population2018'].mean()
popChina = dataChina['population2018'].mean()
popUSA = dataUSA['population2018'].mean()
popFrance = dataFrance['population2018'].mean()
popRussia = dataRussia['population2018'].mean()
#Anschließend wurden die Anteile der Bevölkerung, die erkrankt sind, in Prozent mittels Print ausgegeben.
print('\nInfected population:')
inf_pop_Germany = round(cases_Ger.sum()/popGer*100, 2)
print('Germany: '+ str(inf_pop_Germany) + '%')
inf_pop_Italy = round(cases_Italy.sum()/popItaly*100, 2)
print('Italy: '+ str(inf_pop_Italy) + '%')
inf_pop_China = round(cases_China.sum()/popChina*100, 2)
print('China: '+ str(inf_pop_China) + '%')
inf_pop_USA = round(cases_USA.sum()/popUSA*100, 2)
print('USA: '+ str(inf_pop_USA) + '%')
inf_pop_France = round(cases_France.sum()/popFrance*100, 2)
print('France: '+ str(inf_pop_France) + '%')
inf_pop_Russia = round(cases_Russia.sum()/popRussia*100, 2)
print('Russia: '+ str(inf_pop_Russia) + '%')


#Das zweite und dritte Diagramm stellt die Entwicklungen der Fallzahlen und der Todesfälle der vier Länder (Deutschland, Italien, China und USA) dar.
#Alternativ könnte man die Entwicklung für jedes der vier Länder auch in einem Subplot darstellen
#und die vier Subplots in einem gemeinsamen "großen" Plot.
#Aufgrund der unterschiedlichen Dimensionen der Ordinatenachsen ist die Darstellung in Subplots in diesem Fall nicht zu empfehlen.
#Dennoch soll mit den zwei folgenden Plots die Möglichkeit, die Matplotlib bietet unterstrichen werden.

#Es folgen die vier Subplots für die Entwicklung der Fallzahlen in den vier Ländern.
plt.style.use('bmh')
plt.subplot(2,2,1)
plt.plot(xGer, cases_Ger, color='darkcyan')
plt.tight_layout()
plt.title('Entwicklung der Fallzahlen\n in Deutschland', size=10, fontweight='bold')
plt.xlabel('Day')
plt.ylabel('Cases')
plt.xticks(rotation=45)

plt.subplot(2,2,2)
plt.plot(xItaly, cases_Italy, color='darkcyan')
plt.tight_layout()
plt.title('Entwicklung der Fallzahlen\n in Italien', size=10, fontweight='bold')
plt.xlabel('Day')
plt.ylabel('Cases')
plt.xticks(rotation=45)

plt.subplot(2,2,3)
plt.plot(xChina, cases_China, color='darkcyan')
plt.title('Entwicklung der Fallzahlen\n in China', size=10, fontweight='bold')
plt.xlabel('Day')
plt.ylabel('Cases')
plt.xticks(rotation=45)

plt.subplot(2,2,4)
plt.plot(xUSA, cases_USA, color='darkcyan')
plt.title('Entwicklung der Fallzahlen\n in den USA', size=10, fontweight='bold')
plt.xlabel('Day')
plt.ylabel('Cases')
plt.xticks(rotation=45)
plt.show()

#Es folgen die vier Subplots für die Entwicklung der Todesfälle in den vier Ländern.
plt.style.use('bmh')
plt.subplot(2,2,1)
plt.plot(xGer, deaths_Ger, color='darkred')
plt.tight_layout()
plt.title('Entwicklung der Todesfälle\n in Deutschland', size=10, fontweight='bold')
plt.xlabel('Day')
plt.ylabel('Deaths')
plt.xticks(rotation=45)

plt.subplot(2,2,2)
plt.plot(xItaly, deaths_Italy, color='darkred')
plt.tight_layout()
plt.title('Entwicklung der Todesfälle\n in Italien', size=10, fontweight='bold')
plt.xlabel('Day')
plt.ylabel('Deaths')
plt.xticks(rotation=45)

plt.subplot(2,2,3)
plt.plot(xChina, deaths_China, color='darkred')
plt.title('Entwicklung der Todesfälle\n in China', size=10, fontweight='bold')
plt.xlabel('Day')
plt.ylabel('Deaths')
plt.xticks(rotation=45)

plt.subplot(2,2,4)
plt.plot(xUSA, deaths_USA, color='darkred')
plt.title('Entwicklung der Todesfälle\n in den USA', size=10, fontweight='bold')
plt.xlabel('Day')
plt.ylabel('Deaths')
plt.xticks(rotation=45)
plt.show()


#Um einen bestimmten Abschnitt des Entwicklungsverlaufes abzuschneiden (z.B. lässt sich in Deutschland vor dem 1. März 2020
#keine Entwicklung im Diagramm ablesen, da die Fallzahlen und die Todesfälle entweder nahe oder gänzlich bei Null liegen) kann
#man folgendes machen:

dataGer_new = dataGer.loc[dataGer['date']>= '2020-03-01']
xGer_new = dataGer_new['date']
cases_Ger_new = dataGer_new['cases']
plt.plot(xGer_new, cases_Ger_new, color='darkcyan')
plt.xlabel('Day')
plt.ylabel('Cases')
plt.show()
