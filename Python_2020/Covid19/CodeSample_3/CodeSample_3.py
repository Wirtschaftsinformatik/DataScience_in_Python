'''
Auswertung der aktuellen Covid-19 Situation von Marcus Wurster

Kurzer Kommentar zu folgendem Pythonscript:

Die Daten stammen von der ECDC (European Centre for Disease Prevention and Control) und
können unter folgendem Link selbst heruntergeladen werden:
https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide

Alle Darstellungen und Berechnungen beziehen stets die aktuellen Daten mit ein und
sollten somit auch stets tagesaktuell sein. Innerhalb des scripts sind interesannte Printfunktionen
für einzelne Databases und Ergebnisse als Kommentar ergänzt und eingerückt. Sie können durch einfaches
Entfernen des # und der Einrückung mitausgegeben werden. Außerdem ist anzumerken, dass durch eine
eventuell deutlich veränderte Datenlage die Bezeichnungen innerhalb der Grafiken verschoben sein können.
Dies ist aufgrund der Verwendung der stets aktuellen Daten leider nicht zu verhindern.

Die aktuellen Daten werden auch bei der Auswahl der Top10 Länder und dem Land mit den meisten Fällen stets miteinbezogen.
Die betrachteten Länder können sich hiermit auch von Tag zu Tag ändern.

Ab Version Python 3.x sollte das Script ohne Probleme laufen.
'''

# -*- coding: utf-8 -*-

#Notwendige python libraries importieren und plot style setzen

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

plt.style.use('ggplot')


#Daten importieren und als DataFrame speichern

csv_url = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/csv'

df_original = pd.read_csv(csv_url)


#Ursprünglichen DataFrame begutachten (optional)

#print(df_original.head())
#print(df_original.info())
#print(df_original.columns.values)



#Aktuelle weltweite Fallzahen, Todeszahlen und Sterblichkeitsrate berechnen und ausgeben

sum_of_all_cases_worldwide = df_original['cases'].sum()
sum_of_all_deaths_worldwide = df_original['deaths'].sum()
death_rate_worldwide = round(sum_of_all_deaths_worldwide / sum_of_all_cases_worldwide, 5)

lista = ['Weltweite_Fälle', 'Weltweite_Tode', 'Sterblichkeitsrate_weltweit']

listb = [sum_of_all_cases_worldwide, sum_of_all_deaths_worldwide, death_rate_worldwide]

keyvalues_worldwide = dict(zip(lista, listb))

print(keyvalues_worldwide)


#Entwicklung weltweiter Fälle/Tode herausfinden und grafisch darstellen

worldwide_per_day = df_original.groupby(['year', 'month','day'])[['cases', 'deaths']].sum()
#print(worldwide_per_day)

cum_worldwide_per_day_cases = np.cumsum(worldwide_per_day['cases']) #kumulierte Fälle
cum_worldwide_per_day_deaths = np.cumsum(worldwide_per_day['deaths'])
#print(cum_worldwide_per_month)

plt.figure(figsize=(11,6))
cum_worldwide_per_day_cases.plot(x='day', y='cases', kind='line')
cum_worldwide_per_day_deaths.plot(x='day', y='deaths', kind='line')
plt.xticks(rotation=15)
plt.title('Kummulierte weltweite Covid-19 Fälle/Tode', fontsize=14)
str = {'Aktuelle weltweite Fallzahl:', sum_of_all_cases_worldwide}
plt.text(20,3000000,str, fontsize=12)
plt.legend()
plt.show()


#DataFrame bearbeiten und um Merkwürdigkeiten bereinigen

df_original = df_original.drop(['geoId', 'countryterritoryCode', 'dateRep'], axis=1)

df_original = df_original[df_original.continentExp != 'Other']

df_original['countriesAndTerritories'] = df_original['countriesAndTerritories'].replace(
	{'United_States_of_America': 'USA', 'United_Kingdom': 'UK'})


#DataFrame nach Kontinenten aufschlüsseln und als Kuchendiagramm ausgeben
cases_per_continent = df_original.groupby('continentExp', as_index=False)['cases'].sum()
#print(cases_per_continent)

labels = cases_per_continent['continentExp']
sizes = cases_per_continent['cases']
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'black', 'red']
explode = (0, 0, 0, 0.1, 0)

plt.figure(figsize=(11,6))
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
		autopct='%1.1f%%', shadow=True, startangle=140)
plt.xticks(rotation=40)
plt.axis('equal')
plt.title('Prozentualer Anteil der Covid-19 Fälle je Kontinent',fontsize=14)
plt.legend()
plt.show()


#DataFrame nach Länder aufschlüsseln und in absteigender Reihenfolge nach Fällen sortieren
df_per_country = df_original.groupby(['countriesAndTerritories', 'popData2018'],
									 as_index=False)[['cases', 'deaths']].sum()

df_per_country = df_per_country.sort_values(by='cases', ascending=0)


#Sterblichkeitsrate und Fälle/Tode pro 100.000 Einwohner zu cases_per_country hinzufügen

df_per_country['cases100k'] = round(((df_per_country['cases']/
									  df_per_country['popData2018'])*100000))
df_per_country['deaths100k'] = round(((df_per_country['deaths']/
									   df_per_country['popData2018'])*100000))
df_per_country['deathrate'] = round((df_per_country['deaths']/df_per_country['cases']), 4)
#print(cases_per_country)


#Durchschnitt, Max und Min der Fälle & Tode nach Länder ausmachen (wird an anderer Stelle ausgegebe)

avg_cases = round(df_per_country['cases'].mean())
max_cases = df_per_country['cases'].max()
avg_deaths = round(df_per_country['deaths'].mean())
max_deaths = df_per_country['deaths'].max()
avg_deathrate = df_per_country['deathrate'].mean()
max_deathrate = df_per_country['deathrate'].max()

kpis = [max_cases, avg_cases, max_deaths, avg_deaths, max_deathrate, avg_deathrate]
title = ['Max Fälle pro Land', 'Durschn.Fallzahl pro Land',
		 'Max Tode pro Land', 'Durchschn. Todeszahl pro Land',
		 'Max Sterblichkeitsrate pro Land',
		 'Durschschn. Sterblichkeitsrate pro Land']

numbers_country = pd.DataFrame({'Covid-19_Kennzahl': title, 'Ausprägung': kpis })
#print(numbers_country)


#Top10 der Länder mit größter Anzahl an Fällen(mit Fällen pro 100000Einwohner) in einem Balkendiagramm darstellen

df_pc_top10 = df_per_country.nlargest(10, ['cases']) #selektiert n größte Werte in Spalte cases
#print(cpc_top10)

plt.figure(figsize=(11,6))
plt.subplot(2,1,1)
plt.bar(df_pc_top10['countriesAndTerritories'],df_pc_top10['cases'],color='blue',edgecolor='black')
plt.title('Covid-19 Fälle je Land der 10 Länder mit den meisten Fällen',fontsize=14)
plt.subplots_adjust(hspace=0.3)

plt.subplot(2,1,2)
plt.bar(df_pc_top10['countriesAndTerritories'],df_pc_top10['cases100k'],
		color='blue',edgecolor='black')
plt.title('Covid-19 Fälle pro 100.000 Einwohner je Land',fontsize=14)
plt.show()


#Top10 der Länder nach Fällen pro 100.000 Einwohner darstellen

df_pc_top10_100k = df_per_country.nlargest(10, ['cases100k']) #selektiert n größte Werte in Spalte cases
#print(cpc_top10)

plt.figure(figsize=(11,6))
plt.subplot(2,1,1)
plt.bar(df_pc_top10_100k['countriesAndTerritories'],df_pc_top10_100k['cases'],
		color='blue',edgecolor='black')
plt.title('Covid-19 Fälle je Land der 10 Länder mit den meisten Fällen je 100.000 Einwohner',fontsize=14)
plt.subplots_adjust(hspace=0.3)

plt.subplot(2,1,2)
plt.bar(df_pc_top10_100k['countriesAndTerritories'],df_pc_top10_100k['cases100k'],
		color='blue',edgecolor='black')
plt.title('Covid-19 Fälle pro 100.000 Einwohner je Land',fontsize=14)
plt.show()


#Land mit den meisten Fällen ausmachen und DataFrame nach diesem Land filtern

df_pc_top1 = df_original.nlargest(1, ['cases'])

pc_top1 = df_pc_top1['countriesAndTerritories'].values

df_pc_top1 = df_original[df_original.countriesAndTerritories.isin(pc_top1)]
#print(df_pc_top1)

top1_per_day = df_pc_top1.groupby(['year', 'month','day'])[['cases', 'deaths']].sum()

cum_top1_per_day_cases = np.cumsum(top1_per_day['cases'])
cum_top1_per_day_deaths = np.cumsum(top1_per_day['deaths'])


#DataFrame nach Deutschland filtern und kummulierte Töde/Fälle ausmachen

is_germany = df_original['countriesAndTerritories'] == 'Germany'

df_germany = df_original[is_germany]
##print(df_germany)

germany_per_day = df_germany.groupby(['year', 'month','day'])[['cases', 'deaths']].sum()
#print(germany_per_day)

cum_germany_per_day_cases = np.cumsum(germany_per_day['cases'])
cum_germany_per_day_deaths = np.cumsum(germany_per_day['deaths'])


#Top1 Land mit Deutschland nach Fällen und Toden vergleichen (Diagramme zeichnen)

plt.figure(figsize=(11,6))
cum_top1_per_day_cases.plot(x='day', y='cases', kind='line')
plt.title('Kummulierte Covid-19 Fälle des Landes mit den meisten Fällen und Deutschland, aktuell:' + pc_top1, fontsize=14)
plt.xlabel(None)
cum_germany_per_day_cases.plot(x='day', y='cases', kind='line')
plt.legend([pc_top1,'Deutschland'], fontsize=12)
plt.show()

plt.figure(figsize=(11,6))
cum_top1_per_day_deaths.plot(x='day', y='deaths', kind='line')
plt.title('Kummulierte Covid-19 Tode des Landes mit den meisten Fällen und Deutschland, aktuell:' + pc_top1, fontsize=14)
plt.xlabel(None)
cum_germany_per_day_deaths.plot(x='day', y='deaths', kind='line')
plt.legend([pc_top1,'Deutschland'], fontsize=12)
plt.show()

#Standardmäßig ausgegebene Tabelle um dazugehörige Länder ergänzen
df_pd_top1 = df_original.nlargest(1, ['deaths'])
pd_top1 = df_pd_top1['countriesAndTerritories'].values

df_pdr_top1 = df_per_country.nlargest(1, ['deathrate'])
pdr_top1 = df_pdr_top1['countriesAndTerritories'].values

countries = [pc_top1, '-', pd_top1,'-', pdr_top1, '-' ]

numbers_country['Zugehöriges_Land'] = countries

#Printbefehle zur schöneren Ausgabe in Konsole

print('______________________________')
print('')
print(numbers_country)


