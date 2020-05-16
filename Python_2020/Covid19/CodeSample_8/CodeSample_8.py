#Autor: Sascha Wiedermann
#import der genutzten packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import data / Stand der Daten ist der 03.05.2020
file = pd.read_csv('ETQSJhgp.csv')
df = pd.DataFrame(file)

#Ab hier beginnt der Code für einen 4-Länder-Vergleich. Ziel des Vergleichs soll es sein, einen allgemeinen Überblick über den Ausbruchsverlauf des Virus zu erhalten.
#Zusätzlich sollen Unterschiede über die Ausbrüche in den verschiedenen Ländern offengelegt werden.
#Für eine bessere Darstellung sollte das Fenster maximiert werden.
#Mit df.loc wurden die Daten nach Ländern gefiltert
plt.style.use('ggplot')
plt.figure('4-Länder-Vergleich',figsize=(8,8))

#Graph für Deutschland
ger = df.loc[df['countriesAndTerritories'] == 'Germany']
xger = ger['dateRep']
yger = ger['cases']
gd= round((ger['deaths'].sum() / ger['cases'].sum())*100,2) #Die Sterberate wurde errrechnet mit dem Verhältnis aller Fälle und aller Todesfälle eines Landes über den Betrachtungszeitraum
plt.subplot(2, 2, 1)
drger= round(ger['deaths'].sum() / yger.sum(),4)*100  #Todesrate in deutschland in %
plt.xlim(1, -1) #Ursprünglich starten die Daten vom 03.05. Um aber eine Darstellung ab dem 01.01.2020 zu erhalten musste die x-Achse "gedreht werden" --> Hier mit xlim(1,-1)
plt.xticks(np.arange(1, 90, step=10), rotation=45) #Nur alle 10 Tage wird ein datum auf der x-Achse angezeigt; sonst überlappen sich die insgesamt >100 Daten;zusätzlich wurde der Text um 45 Grad gedreht
plt.plot(xger, yger, color='b', markevery=[67,54,42], marker='o', markersize=3, markerfacecolor='k')
plt.title('Ausbruchsverlauf Deutschland')
plt.xlabel('Zeitverlauf')
plt.ylabel('Fälle in Deutschland')
#Zusätzlich zu dem Diagramm werden hier wichtige Zeitpunkte im Graphen markiert und teilweise mit einem Pfeil hervorgehoben. Dies geschieht analog für die anderen Länder
plt.annotate('Erster Fall 26.02.', ('26/02/2020', 2), xytext=('26/02/2020', 1000), arrowprops=dict(facecolor='black', width=5, headlength=10,shrink=0.05),horizontalalignment='right', verticalalignment='bottom')
plt.annotate('Erster Todesfall 10.03.', ('10/03/2020', 230), xytext=('10/03/2020', 2000), arrowprops=dict(facecolor='black', shrink=0.05),horizontalalignment='right', verticalalignment='bottom')
plt.annotate('Start\nKontaktbeschränkungen\n22.03.', ('22/03/2020', 3280), xytext=('22/03/2020', 1900), arrowprops=dict(facecolor='black', shrink=0.05),horizontalalignment='left', verticalalignment='top')
plt.annotate('Sterberate: ' + str(gd)+ '%',('13/02/2020', 6000) )

#Graph für Italien
it = df.loc[df['countriesAndTerritories'] == 'Italy']
xit = it['dateRep']
yit = it['cases']
id= round((it['deaths'].sum() / it['cases'].sum())*100,2)
plt.subplot(2, 2, 2)
plt.plot(xit, yit, color='g', markevery=[71,70,42], marker='o', markersize=3, markerfacecolor='k')
plt.xlim(1, -1)
plt.xticks(np.arange(1, 90, step=10), rotation=45)
plt.title('Ausbruchsverlauf Italien')
plt.xlabel('Zeitverlauf')
plt.ylabel('Fälle in Italien')
plt.annotate('Erster Fall 22.02.', ('22/02/2020', 2), xytext=('18/02/2020', 1000), arrowprops=dict(facecolor='black', width=5, headlength=10,shrink=0.05),horizontalalignment='right', verticalalignment='bottom')
plt.annotate('Erster Todesfall 23.02.', ('23/02/2020', 23), xytext=('28/02/2020', 1900), arrowprops=dict(facecolor='black', shrink=0.05),horizontalalignment='right', verticalalignment='bottom')
plt.annotate('Start\nKontaktbeschränkungen\n22.03.', ('22/03/2020', 6550), xytext=('22/03/2020', 3000), arrowprops=dict(facecolor='black', shrink=0.05),horizontalalignment='left', verticalalignment='top')
plt.annotate('Sterberate: ' + str(id)+ '%',('13/02/2020', 6000) )

#Graph für China: Das Ende der Kontaktbeschränkungen ist hier markiert. Es soll veranschaulichen, dass die chinesische Regierung abgewartet hat, bis sich die Lage in China nicht nur kurzfristig wieder gebessert hat,
#sondern sich nach längerer Zeit erst für die Lockerung der Maßnahmen entschieden hat. Dies soll als möglicher Ausblick für die anderen Länder dienen.
ch = df.loc[df['countriesAndTerritories'] == 'China']
xch = ch['dateRep']
ych = ch['cases']
cd= round((ch['deaths'].sum() / ch['cases'].sum())*100,2)
plt.subplot(2, 2, 3)
plt.plot(xch, ych, color='y', markevery=[121,113,25],marker='o', markersize=3, markerfacecolor='k')
plt.xlim(1, -1)
plt.xticks(np.arange(20, 135, step=10), rotation=45)
plt.title('Ausbruchsverlauf China')
plt.xlabel('Zeitverlauf')
plt.ylabel('Fälle in China')
plt.annotate('Erster Fall 03.01.', ('03/01/2020', 20), xytext=('03/01/2020', 1000), arrowprops=dict(facecolor='black', width=5, headlength=10,shrink=0.05),horizontalalignment='right', verticalalignment='bottom')
plt.annotate('Erster Todesfall 11.01.', ('11/01/2020', 5), xytext=('11/01/2020', 3500), arrowprops=dict(facecolor='black', shrink=0.05),horizontalalignment='right', verticalalignment='bottom')
plt.annotate('Ende\nKontaktbeschränkungen\n08.04.', ('08/04/2020', 0), xytext=('08/04/2020', 3000), arrowprops=dict(facecolor='black', shrink=0.05),horizontalalignment='right', verticalalignment='bottom')
plt.annotate('Sterberate: ' + str(cd)+ '%',('31/12/2020', 14500))

#Graph für USA
USA = df.loc[df['countriesAndTerritories'] == 'United_States_of_America']
xusa = USA['dateRep']
yusa = USA['cases']
ud = round((USA['deaths'].sum() / USA['cases'].sum())*100,2)
plt.subplot(2, 2, 4)
plt.plot(xusa, yusa, color='r', markevery=[63,41],marker='o', markersize=3, markerfacecolor='k')
plt.xlim(1, -1)
plt.xticks(np.arange(1, 90, step=10), rotation=45)
plt.title('Ausbruchsverlauf USA')
plt.xlabel('Zeitverlauf')
plt.ylabel('Fälle in USA')
plt.annotate('Erster Fall 21.01.', ('15/02/2020', 40000))
plt.annotate('Erster Todesfall 01.03.', ('01/03/2020', 230), xytext=('01/03/2020', 6000), arrowprops=dict(facecolor='black', shrink=0.05),horizontalalignment='right', verticalalignment='bottom')
plt.annotate('Start\nKontaktbeschränkungen\nca.23.03.', ('23/03/2020', 8470), xytext=('13/03/2020', 29000), arrowprops=dict(facecolor='black', shrink=0.05),horizontalalignment='right', verticalalignment='top')
plt.annotate('Sterberate: ' + str(ud)+ '%',('15/02/2020', 45000))
plt.tight_layout()
plt.show()
#4-Länder-Vergleich endet hier. Um den nächsten Vergleich (Pie-Chart) zu öffnen, muss das aktuelle Fenster geschlossen werden)

#Als zusätzlichen Bestandteil des Projektes wird hier ein Pie-Chart implementiert, das die Anzahl der Todesfälle über alle Kontinente miteinander vergleicht
#Dies soll dem Zweck dienen, einen globalen Vergleich der von Corona verursachten Todesfälle zu erhalten.(Ozeanien und Other sind bei 0 Prozent)
continent = df.groupby('continentExp').sum()
todeszahlen = continent['deaths']
explode = (0.1, 0.1, 0.1, 0.1, 0.3, 0.55)
plt.figure('Pie-Chart Kontinente')
plt.pie(todeszahlen, explode= explode, autopct='%1.1f%%', shadow=True,wedgeprops = {'linewidth': 1})
plt.legend(continent.index, loc='lower right')
plt.title('Vergleich Anzahl Todesfälle über Kontinente')
plt.tight_layout()
plt.show()
#PS: Ursprünglich habe ich eine zusätzliche CSV Datei herangezogen, die alle Länder zu den Kontinenten zuordnet. Mit einem Merge habe ich dann die beiden Datensätze miteinander verbunden.
#Leider wurde die Originaldatei mit der Zeit um die Kontinente erweitert und mein Merge wurde überflüssig.