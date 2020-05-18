# Python Projekt - SoSe 2020
# Maximilian Goebel - Stand: 16.05.20
# -*- coding: utf-8 -*-
# Import notwendiger Packages

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Setzen von Optionen zur Anzeigeskalierung
pd.set_option('display.max_rows',20)
pd.set_option('display.max_columns',20)
pd.set_option('display.width', 1000)


'''Import der CSV und Speicherung in df_quelldatei 
Als URL, um die tÃ€glichen Updates einzubeziehen, ansonsten waere immer wieder 
lokales Updaten der Datei notwendig '''
csv_pfad = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/csv'
df_quelle = pd.read_csv(csv_pfad)

# Uebersichtsartige Inspektion der Daten
print('============================================================================================================================================')
print(df_quelle.head(10))
print('============================================================================================================================================')
print(df_quelle.info())
print('============================================================================================================================================')

# Ausgabe der aktuellen Kennzahlen Gesamtfaelle, Gesamttode und Lethalitaet in einem Dictionary
# Ermittlung der Kennzahlen
faelle_ges = df_quelle['cases'].sum()
tode_ges = df_quelle['deaths'].sum()
leth = round(tode_ges/faelle_ges,4)*100

# Anlegen des Dictionary und Ausgabe
liste_kennzahlen = ['Gesamte Fälle weltweit','Gesamte Todeszahl weltweit','Lethalitaet des Virus weltweit']
liste_kennzahlwerte = [faelle_ges,tode_ges,"{:.2f}".format(leth)+"%"]
dict_kennzahlen = dict(zip(liste_kennzahlen,liste_kennzahlwerte))
print(dict_kennzahlen)
print('============================================================================================================================================')

# Generierung Plot 1: Balkendiagramm der Kennzahlen
# Daten ermitteln und zuweisen
bar_werte = [faelle_ges,tode_ges]
bar_kennzahlen = ('Faelle', 'Tode')

# Formatierung und Anzeige
y_pos = np.arange(len(bar_werte))
plt.bar(y_pos, bar_werte)
plt.xticks(y_pos, bar_kennzahlen)
plt.title('Gesamtfaelle und -todeszahlen Weltweit')
plt.ylabel('Anzahl Personen')
plt.show()

# Generierung Plot 2: Entwicklung der Fall- und Todeszahlen über die Monate hinweg, nicht kumuliert
# Aggregieren der Fallzahlen nach Jahr,Monat und Plotten
df_faelle_monat = df_quelle.groupby(['year','month'])['cases'].sum()
df_faelle_monat.plot(x='month',y='cases',label='Fallzahlen')

# Aggregieren der Todeszahlen nach Jahr,Monat und Plotten
df_tode_monat = df_quelle.groupby(['year','month'])['deaths'].sum()
df_tode_monat.plot(x='month',y='cases',label='Todeszahlen')

# Formatierung und Anzeige
plt.xlabel('Jahr, Monat')
plt.ylabel('Anzahl Fälle')
plt.title('Entwicklung der Fall- und Todeszahlen je Monat, nicht kumuliert')
plt.legend()
plt.show()

# Generierung Plot 3: Entwicklung der Fall- und Todeszahlen über die Monate hinweg, kumuliert
# Kumulieren der Fallzahlen nach Jahr,Monat und Plotten
df_faelle_kum = df_quelle.groupby(['year','month'])['cases'].sum().groupby(['year']).cumsum()
df_faelle_kum.plot(x='month',y='cases',label='Fallzahlen')

# Kumulieren der Todeszahlen nach Jahr,Monat und Plotten
df_tode_kum = df_quelle.groupby(['year','month'])['deaths'].sum().groupby(['year']).cumsum()
df_tode_kum.plot(x='month',y='cases',label='Todeszahlen')

# Formatierung und Anzeige
plt.xlabel('Jahr, Monat')
plt.ylabel('Anzahl Personen')
plt.title('Entwicklung der Fall- und Todeszahlen je Monat, kumuliert')
plt.legend()
plt.show()

# Generierung Plot 4: Entwicklung der Fallzahlen je Kontinent
# Aggregieren der Fallzahlen nach Kontinent,Jahr,Monat und Plotten
df_faelle_kontinent = df_quelle.groupby(['continentExp','year','month'])['cases'].sum()
df_faelle_kontinent['Africa'].plot(x='month',y='cases',label='Afrika')
df_faelle_kontinent['America'].plot(x='month',y='cases',label='Amerika')
df_faelle_kontinent['Asia'].plot(x='month',y='cases',label='Asien')
df_faelle_kontinent['Europe'].plot(x='month',y='cases',label='Europa')
df_faelle_kontinent['Oceania'].plot(x='month',y='cases',label='Ozeanien')

# Formatierung und Anzeige
plt.xlabel('Jahr, Monat')
plt.ylabel('Anzahl Personen')
plt.title('Entwicklung der Fallzahlen je Kontinent, nicht kumuliert')
plt.legend()
plt.show()

# Generierung Plot 5: Entwicklung der Todeszahlen je Kontinent
# Aggregieren der Todeszahlen nach Kontinent,Jahr,Monat und Plotten
df_tode_kontinent = df_quelle.groupby(['continentExp','year','month'])['deaths'].sum()
df_tode_kontinent['Africa'].plot(x='month',y='deaths',label='Afrika')
df_tode_kontinent['America'].plot(x='month',y='deaths',label='Amerika')
df_tode_kontinent['Asia'].plot(x='month',y='deaths',label='Asien')
df_tode_kontinent['Europe'].plot(x='month',y='deaths',label='Europa')
df_tode_kontinent['Oceania'].plot(x='month',y='deaths',label='Ozeanien')

# Formatierung und Anzeige
plt.xlabel('Jahr, Monat')
plt.ylabel('Anzahl Personen')
plt.title('Entwicklung der Todeszahlen je Kontinent, nicht kumuliert')
plt.legend()
plt.show()

# Genierung Plot 5: Gegenüberstellung Fallzahlen und Bevoelkerungsgroeße der Laender
# Zur Abtrennung: Slicing der Datenquelle um Data Frame mit Laendern, Faellen und Bevoelkerung zu erhalten
df_pop = df_quelle.loc[:,['countriesAndTerritories','cases','popData2018']]
df_pop['popData2018']=df_pop['popData2018'].apply(lambda x: x/1000000) # Darstellung von Anzahl in Millionen

# Aggregieren der Fallzahlen nach Landesgroeße: cases:sum erzeugt Summe der Faelle, popData2018:first weist Land die Bevoelkerung zu (sonst: Problem von Duplikaten)
df_pop_sum = df_pop.groupby('countriesAndTerritories').agg({'cases':'sum', 'popData2018':'first'}).reset_index()

# Plotten, Formatierung und Anzeige
scatter_pop = plt.scatter(df_pop_sum.popData2018,df_pop_sum.cases)
plt.xlabel('Bevoelkerung der Laender in Millionen')
plt.ylabel('Anzahl Faelle')
plt.title('Fallzahlen gegenueber den Groeßen der Laender, gemessen an deren Bevoelkerung')
plt.show()