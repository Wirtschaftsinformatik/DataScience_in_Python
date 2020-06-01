#!/usr/bin/python
# -*- coding: latin-1 -*-

#------------Workshop Python_Jendrik Weber------------------------------------
#-----------------------------------------------------------------------------
#Das Programm liest die Daten zur Corona ausbreitung ein und werden verarbeitet, 
# um sie vergleichbar zu machen.
#Es wird eine statistische Analyse der Daten durchgef�hr. Zus�tzlich werden die Ergebnisse Visualisiert. 

#--------------------------------------------------------------------------
#import der n�tigen Packages-----------------------------------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#liest Daten direkt aus dem Web ein
Daten=pd.read_csv('https://opendata.ecdc.europa.eu/covid19/casedistribution/csv')
# Sortiert die Daten und filtert nach n�tigsten Spalten aus 
SortDaten=Daten[['dateRep','cases' , 'deaths', 'countriesAndTerritories','continentExp']]

#gibt einmal die Daten aus
print('Es wird einmal die Datei ausgegeben, wegen der unsch�nen Ausgabe wird im Folgenden darauf verzichtet:')
print(SortDaten)
#------------------------------------------------------------------------

#--------------------------------------------------------------------------
#Es soll nun ein Array erstellt werden, dass alle Kontinente beinhaltet, ohne Duplikate
#Dazu etwas an Vorbereitung:
Kontinente=SortDaten.copy()   #Kopie der Datei
Liste=[]                      #Erstellung einer leeren Liste
a1=Kontinente.continentExp    #Erstellung einer neuen Datei, die nur noch die Spalte der Kontinente beinhaltet
#Eingehen einer Schleife, die jede Zeile durchgeht
for L in range(len(a1.index)):
    x=a1.values[L]
    if x not in Liste:     # und den Kontinent in die Liste hinzuf�gt, vorausgesetz er ist noch nicht bereits drinne
        Liste += [ str(x) ]
        
#print(Liste) ergibt: ['Asia', 'Europe', 'Africa', 'America', 'Oceania', 'Other']
print()   #Leerzeichen
#-----------------------------------------------------------------------------
#---------------------------Statistische Analyse der Kontinente---------------
#--------------------------Gesamte Tote nach Kontinenten
print('Wie viele Tote gab es in den jeweiligen Kontinenten und welcher Kontinent hatte die meisten Toten?')
GesamteTote=[] #Vorbereitung: Erstellung eines leeren Arrays f�r die Totenzahlen
GesamteInfizierte=[]  # Erstellung eines Arrays f�r die Infiziertenzahlen
# nun wird ein das Array Gesamte Tote gef�llt:
for i in range (len(Liste)):
    #Die Datei werd nach den einzelnen Kontinenten , welche in der Liste vorher gespeichert wurden, gefiltert.
    k=Kontinente[Kontinente.continentExp == Liste[i]]    
    d=np.sum(k.deaths) # Es wird die Summe der Toten in dem Kontinent ausgerechnet 
    j=np.sum(k.cases) # Es wird die Summe der Infizierten in jedem Kontinent ausgerechnet
    GesamteTote += [d] # und in dem Array gespeichert
    GesamteInfizierte += [j] #Die Summe der Infizierten wird ebenfalls in einem Array gespeichert!
    print(str(Liste[i])+': Tote:' + str(d) + '; Infizierte: ' + str(j) ) #Es wird ausgegeben, welches Land die h�chste Anzahl an Toten hatte
#----------------------------------------------
print()
#------Wer hat die meisten Toten?-----
#Es wird ein neues np.Array erstellt, welches die Anzahl der gesamten Toten drinne hat
e=np.array(GesamteTote)
m=np.array(GesamteInfizierte)
#hier wird die Stelle des Maximums ausgegeben
Maximum= e.argmax()
#ausgegeben wird das maximum des Array GesamteTote (identisch mit Array e)
#und die Stelle des Maximums in der Liste der L�nder, damit das dazugeh�rigeLand ausgegeben wird!
print('Die meisten Toten (' + str(max(GesamteTote)) +') gab es in "'+ str(Liste[Maximum]) + '".')
print('Die meisten Infizierten (' + str(max(GesamteInfizierte)) + ') gab es in "' + str(Liste[m.argmax()]) + '".')


#---------------------------------------------------------------------------------------------------
#-Analyse Europa und Länder
#Ausgeben der Fragestellungen und Instruktionen
print()
print('Welches sind die L�nder mit den meisten Toten in Europa?:')
print('Es werden nur L�nder angezeigt, die im Vgl. zu den anderen europ�ischen L�ndern eine �berdurchschnittliche Totenzahl aufweist:')
print('Zudem werden noch andere statistische Gr��en von jenen L�ndern angezeigt.')
#Europa wird als neue Variable gespeicvhert, welche die Datei nach dem Kontinent Europa filtert
print()
#Die Datei wird kopiert und als Variable gespeichert und nach Europa gefiltert
Europa=SortDaten.copy()
Europa=SortDaten[SortDaten.continentExp == 'Europe']
print()
#print(Europa)
#-------------------------------------------------------------------------------
#Es wird nun ein Array erstellt, dass alle Länder von Europa beinhaltet---------
#Erstellt ein leeres Array
Laender=[]
#a wird definiert als Europa und nur nach den Ländern gefiltert!
a=Europa.countriesAndTerritories
#Es wird ein Array erstellt, welches alle Länder von Europa ausgibt. 
for i in range(len(a.index)):
    z=a.values[i]
    if z not in Laender:
        Laender += [ str(z) ]
#print(Laender) w�rde folgende Ausgabe geben
#['Albania', 'Andorra', 'Armenia', 'Austria', 'Azerbaijan', 'Belarus', 'Belgium', 'Bosnia_and_Herzegovina', 'Bulgaria', 'Croatia', 'Cyprus', 'Czechia', 'Denmark', 'Estonia', 'Faroe_Islands', 'Finland', 'France', 'Georgia', 'Germany', 'Gibraltar', 'Greece', 'Guernsey', 'Holy_See', 'Hungary', 'Iceland', 'Ireland', 'Isle_of_Man', 'Italy', 'Jersey', 'Kosovo', 'Latvia', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Malta', 'Moldova', 'Monaco', 'Montenegro', 'Netherlands', 'North_Macedonia', 'Norway', 'Poland', 'Portugal', 'Romania', 'Russia', 'San_Marino', 'Serbia', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Ukraine', 'United_Kingdom']
#------------------------------------------------------------------------------

#Nun zu den Fragestellungen, dazu wieder etwas Vorbereitung
#Tote insgesamt
ToteLaender=[]    #Leere Liste, welche mit der Summe der Toten der L�nder gef�llt wird
Summe=np.sum(Europa.deaths)  #Summer aller Toten in Europa
InfizierteLaender=[] # Liste der Infizierten der L�nder

#Wird nun eine schleife durchlaufen, wobei jedes einzelne Land aus der Laenderliste einmal angesprochen wird
for l in range (len(Laender)):
    b=Europa[Europa.countriesAndTerritories == Laender[l]]    #Die Europaliste wird nach den einzelnen L�ndern gefiltert
    c=np.sum(b.deaths)                                        #und jeweils wird die Summe der Toten gespeichert
    Mittelwert=np.mean(b.deaths)     # Es wird der Mittelwert der einzelnen L�nder gespeichert
    Standardabweichung=np.std(b.deaths)    # Standardabweichung
    ToteLaender += [c]    # Die Anzahl wird in die Liste hinzugef�gt
    Infizierte=np.sum(b.cases)   #Das selbe bei den Infizierten
    InfizierteLaender += [Infizierte]
    # Da es zuviele L�nder gibt, werden nur jene ausgegeben, welche eine gr��ere Totenzahl als die durchschnittliche Totenzahl in Europa haben!
    if c > Summe/len(Laender):
        #F�r diese L�nder werden die oben bestimmten Daten ausgegeben.
        print(str(Laender[l])+': Tote=' + str(c) + ';  Mittelwert= ' + str(round(Mittelwert,2)) + '; Std: ' + str(round(Standardabweichung,2)) 
              +'\n'+ '-'*(len(Laender[l]))+'> '+ 'Infizierte: ' + str(Infizierte)
              +'\n'+ '-'*(len(Laender[l]))+'> ' + 'Prozentual sind somit ' + str(round(c/Infizierte,2)) + ' gestorben.'
              )

# Es wird ein np array erstellt, damit man die Stelle der maximalen Anzahl finden kann und das dazugeh�rige Land ermitteln kann
f=np.array(ToteLaender)
h=np.array(InfizierteLaender)
print()
#Es werden die wichtigsten Ergebnisse ausgegeben!
print('Durchschnittliche Totenanzahl pro Land betr�gt: ' + str(round(Summe/len(Laender),2)) )
print('Das Land mit den meisten Toten (' + str(max(ToteLaender)) + ') ist "' + str(Laender[np.argmax(f)]) + '". Dieses Land hat ' + str(InfizierteLaender[np.argmax(f)]) + ' Infizierte. ')
print('Das Land mit den meisten Infizierten (' + str(max(InfizierteLaender)) +  ') ist "' + str(Laender[np.argmax(h)]) + '". Dieses Land hat ' + str(ToteLaender[np.argmax(h)]) + ' Tote.'  )

#----------------------------------------------------------------------------
#--------Keine Toten
print()
print('Wie viele und welche L�nder haben bisher noch keine Toten?')
print()
#- Es wird wieder eine Liste durchlaufen, Vorbereitung �hnlich wie oben 
KeineToten=[]
KEINETOTENLAENDER=[]
for i in range(len(ToteLaender)):
    #Wenn die die Anzahl der Toten gleich null ergibt
    if ToteLaender[i]==0:
        #Weird dieses Land in eine Liste hinzugef�gt und die 0 wird ebenfalls einer Liste hinzugef�gt, um zu erfahren wie viele L�nder keine Toten haben
        KeineToten += [i]
        KEINETOTENLAENDER += [Laender[i]]
#Ausgabe der Anzahl der L�nder (L�nge der Liste mit 0 drinne) und Ausgabe der L�nderliste mit Null Toten. 
print('Bisher haben ' + str(len(KeineToten)) + ' L�nder in Europa noch keine Toten zu beklagen. Dies betrifft folgende L�nder: ' + str(KEINETOTENLAENDER))

print()


#Grafische Darstellung:
#------------------------------------------------------------------------------
#Anzahl der Toten in den einzelnen Kontinenten------------
## Die Kontinente und die Gesamtzahl der Toten werden geplottet
plt.plot(Liste, GesamteTote, 'red')
#Titel
plt.title('Anzahl der Tote in den Kontinenten')
# y-Achsenbeschriftung
plt.ylabel('Tote')
#x- Achsenbeschriftung
plt.xlabel('Kontinente')
#Ausf�hrung d. Grafik
plt.show()
#-----------------------------------------------------------------------------
#--- Kontinente- Infiziertenzahl und Totenzahl
plt.plot(Liste, GesamteTote, 'red', label='Tote')
plt.plot(Liste, GesamteInfizierte, 'blue', label='Infizierte')
plt.legend()
plt.title('Tote und Infizierte in den Kontinenten')
plt.xlabel('Kontinente')
plt.ylabel('Anzahl')
plt.show()

#-----------------------------------------------------------------------------
#L�nder Infizierte und Tote
plt.plot(Laender, ToteLaender, 'yellow', label='Tote')
plt.plot(Laender, InfizierteLaender, 'green', label='Infizierte')
plt.xticks(rotation='vertical')
plt.legend()
plt.title('Tote und Infizierte in den L�ndern in Europa')
plt.xlabel('L�nder')
plt.ylabel('Anzahl')
plt.show()


#---Folgend zeige ich, was das Programm ausgibt(au�er die Grafiken):

#Es wird einmal die Datei ausgegeben, wegen der unsch�nen Ausgabe wird im Folgenden darauf verzichtet:
#          dateRep  cases  deaths countriesAndTerritories continentExp
#0      27/05/2020    658       1             Afghanistan         Asia
#1      26/05/2020    591       1             Afghanistan         Asia
#2      25/05/2020    584       2             Afghanistan         Asia
#3      24/05/2020    782      11             Afghanistan         Asia
#4      23/05/2020    540      12             Afghanistan         Asia
#          ...    ...     ...                     ...          ...
#19661  25/03/2020      0       0                Zimbabwe       Africa
#19662  24/03/2020      0       1                Zimbabwe       Africa
#19663  23/03/2020      0       0                Zimbabwe       Africa
#19664  22/03/2020      1       0                Zimbabwe       Africa
#19665  21/03/2020      1       0                Zimbabwe       Africa

#[19666 rows x 5 columns]

#Wie viele Tote gab es in den jeweiligen Kontinenten und welcher Kontinent hatte die meisten Toten?
#Asia: Tote:28077; Infizierte: 992377
#Europe: Tote:169385; Infizierte: 1862304
#Africa: Tote:3590; Infizierte: 119775
#America: Tote:149023; Infizierte: 2571974
#Oceania: Tote:130; Infizierte: 8582
#Other: Tote:7; Infizierte: 696
#
#Die meisten Toten (169385) gab es in "Europe".
#Die meisten Infizierten (2571974) gab es in "America".
#
#Welches sind die L�nder mit den meisten Toten in Europa?:
#Es werden nur L�nder angezeigt, die im Vgl. zu den anderen europ�ischen L�ndern eine �berdurchschnittliche Totenzahl aufweist:
#Zudem werden noch andere statistische Gr��en von jenen L�ndern angezeigt.


#Belgium: Tote=9334;  Mittelwert= 62.64; Std: 101.4
#-------> Infizierte: 57455
#-------> Prozentual sind somit 0.16 gestorben.
#France: Tote=28530;  Mittelwert= 191.48; Std: 323.78
#------> Infizierte: 145555
#------> Prozentual sind somit 0.2 gestorben.
#Germany: Tote=8349;  Mittelwert= 56.03; Std: 82.61
#-------> Infizierte: 179364
#-------> Prozentual sind somit 0.05 gestorben.
#Italy: Tote=32955;  Mittelwert= 221.17; Std: 263.85
#-----> Infizierte: 230555
#-----> Prozentual sind somit 0.14 gestorben.
#Netherlands: Tote=5856;  Mittelwert= 39.3; Std: 55.37
#-----------> Infizierte: 45578
#-----------> Prozentual sind somit 0.13 gestorben.
#Russia: Tote=3807;  Mittelwert= 25.55; Std: 42.61
#------> Infizierte: 362342
#------> Prozentual sind somit 0.01 gestorben.
#Spain: Tote=27117;  Mittelwert= 183.22; Std: 325.07
#-----> Infizierte: 236259
#-----> Prozentual sind somit 0.11 gestorben.
#Sweden: Tote=4125;  Mittelwert= 27.68; Std: 43.81
#------> Infizierte: 34440
#------> Prozentual sind somit 0.12 gestorben.
#United_Kingdom: Tote=37048;  Mittelwert= 248.64; Std: 343.09
#--------------> Infizierte: 265227
#--------------> Prozentual sind somit 0.14 gestorben.

#Durchschnittliche Totenanzahl pro Land betr�gt: 3136.76
#Das Land mit den meisten Toten (37048) ist "United_Kingdom". Dieses Land hat 265227 Infizierte. 
#Das Land mit den meisten Infizierten (362342) ist "Russia". Dieses Land hat 3807 Tote.

#Wie viele und welche L�nder haben bisher noch keine Toten?

#Bisher haben 3 L�nder in Europa noch keine Toten zu beklagen. Dies betrifft folgende L�nder: ['Faroe_Islands', 'Gibraltar', 'Holy_See']

    
