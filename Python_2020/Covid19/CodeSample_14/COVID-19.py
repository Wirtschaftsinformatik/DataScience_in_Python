
# coding: utf-8

# # 1.) Importieren der Pakete und einlesen des Datensatzes 

# In[185]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


# In[186]:


file = 'COVID-19.csv'
data = pd.read_csv(file, sep=';', na_values='Nothing')


# # 2.) Preprocessing

# ##  2.1) Sichtung der CSV-Datei

# In[187]:


print(data.head())


# In[188]:


data.info()


# Über verschiedene Befehle können Informationen des Datensatzes eingeholt werden. Im obigen Infobefehl fällt auf,
# dass der Datensatz im hinteren Teil der Attribute weniger Einträge aufweist. Dies könnte auf missing values hinweisen.
# Zudem sind nur die Datentypen Object, int, float vorhanden, obwohl auch ein Datumsformat eingelesen worden sein müsste.

# In[189]:


datarelevant = ['cases','deaths','popData2018']
data[datarelevant].describe()


# In[190]:


data.shape


# Durch die beiden obigen Befehle describe und shape kann eine erste Übersicht über die Ausprägung der Daten gewonnen
# werden. Hier geht es vor allem um eine Gesamtansicht bzw. eine grobe Draufsicht. 
# Dafür wurden nur die relevanten Attribute ausgewählt, da diese Ansicht bei Datumsformaten z.B. keinen Sinn macht.
# Die Werte werden später noch genauer inspiziert. Zudem ist zu sehen, dass der Datensatz 16741 Einträge mit 11
# Ausprägungen enthält.

# In[191]:


data.dtypes


# Wie bereits erwähnt, wird hier noch einmal bestätigt, dass das Datumsformat falsch eingelesen wurde.
# Dies wird im Folgenden behoben.

# ## 2.2) Data Preperation

# ### 2.2.1) Korrektur falsch eingelesener Formate (Datumsformat)

# In[192]:


data['dateRep'] = pd.to_datetime(data['dateRep'])


# In[193]:


data['popData2018'] = data['popData2018']


# In[194]:



NA = data[data['popData2018'] == None]
print(NA)


# In[197]:


data.dtypes


# Nun ist zu sehen, dass die erste Spalte ihr korrektes Datumsformat besitzt. Im Folgenden kann man sich den Kopf
# des Datensatzes nochmals ansehen

# In[198]:


data.head()


# ### 2.2.2) Null-Werte

# Wie bereits zu Beginn vermutet, sind in den Attributen 'geoID','countriesAndTerritories','popData2018' missing values
# enthalten. Dies wird anhand des folgenden Befehls geprüft.

# In[199]:


print(data.isnull().sum())


# Anschließend ist zu klären wie mit diesen Werten umgegangen werden soll. Hierbei bestehen verschiedene Möglichkeiten,
# wie z.B. das Auffüllen anhand vorhandener Daten (Gleichen Wert kopieren, Mittelwerte, letzten Wert usw.) oder mit
# einem "radikalen" Schritt die Daten zu löschen. Da es sich - abgesehen von den Bevölkerungsdaten - bei den fehlenden Werten vor allem um Abkürzungen und Kürzel handelt,
# werden die Missing Values in diesem Fall unverändert belassen, da wichtige Werte wie Todesrate und Fallzahlen weiter
# enthalten sind. Hierbei müsste Python im besten Fall noch gesagt werden wie mit diesen Werten umzugehen ist.

# ### 2.2.3) Korrelationsanalyse

# In[200]:


correlation = data.corr()
correlation


# Zur Beurteilung der Aussagekraft der verschiedenen Attribute (Features) wird eine Korrelationsanalyse durchgeführt. Aufgrund der recht überschaubaren Anzahl an Dimensionen ist dies bei dem vorhandenen Datensatz nicht zwingend notwendig, da mit steigender Anzahl an Attributen auch die Chance steigt, dass zussamenhängende Attribute vorhanden sind, welche den Datensatz unnötigerweise komplex machen. Diese könnten dann z.B. mithilfe einer PCA zu "künstlichen" Attributen zusammengefasst werden, was allerdings auf komplexere Verfahren wie ...... abzielt.
# 
# Dennoch ist eine Korrelationsanalyse hier interessant, da wir sehen, dass erwartungsgemäß die Höhe der Fallzahl stark mit der Zahl der Todesfälle korrelliert. Dies scheint in gewisser Weise offensichtlich, kann aber beispielsweise helfen die Daten zu validieren. Sollte dieser Zusammenhang hier nicht bestehen, müssten wir uns die Frage stellen, woran das liegt und ob unsere Daten ggf. qualitativ hochwertig sind.
# Ebenfalls interessant zu sehen ist, dass weder die Fälle der Erkrankten, noch die Zahl der Todesfälle mit der Bevökerungsanzahl der einzelnen Länder korreliert

# Bei komplexeren Datensätzen können die Zusammenhangsmaße zudem mithilfe einer Heatmap visualisiert und somit leichter
# ausfindig gemacht werden:

# In[204]:


fig, ax = plt.subplots(figsize=(15,15))

sns.heatmap(correlation,
xticklabels=correlation.columns,
yticklabels=correlation.columns,
ax=ax)


# # 3.) Analyse des Datensatzes

# In der folgenden Analyse des Datensatzes wird nun zum einen eine Zeitpunktbetrachtung durchgeführt, die den aktuellen
# Stand (hier 15.05.2020) der einzelnen Länder in der Covid-19-Krise wiedergibt (Um den Zeitpunkt auf einen aktuelleren
# Tag zu updaten, einfach den aktuellen Datensatz herunterladen, einlesen und das heutige Datum ändern).
# 
# Zum Anderen findet nachfolgend eine Zeitreihenanalyse statt, die die Entwicklung einzelner Gebiete darstellt.

# ## 3.1) Zeitpunktbetrachtung

# Der Filterung des Datensatzes zur Zeitpunktbetrachtung sieht wie folgt aus:

# In[206]:


today = data[data['dateRep'] == '2020-05-13']
todaysum_continent = data.groupby('continentExp').sum()
todaysum_country = data.groupby('countriesAndTerritories').sum()
today.head()


# Anhand des oben gezeigten Datensatzes könnte nun untersucht werden, wie sich die Fallzahlen am "heutigen" Tag
# verändert haben.
# 
# Uns interessieren jedoch vielmehr die aggregierten Fallzahlen bis zum "heutigen" Tag, weshalb wir die Daten kontinent- bzw. länderweise aufsummieren.

# In[207]:


todaysum_continent.head()


# In[208]:


todaysum_country.head()


# Zur genaueren Untersuchung des Datensatzes werden folgend grundlegende Lage- und Streuparamter untersucht:

# In[209]:


todaysum_country['cases'].mean()


# In[210]:


todaysum_country['cases'].median()


# In[211]:


todaysum_country['cases'].std()


# In[212]:


todaysum_country['cases'].max()


# In[213]:


todaysum_country['deaths'].mean()


# In[214]:


todaysum_country['deaths'].median()


# In[215]:


todaysum_country['deaths'].std()


# In[216]:


todaysum_country['deaths'].max()


# Auffällig hierbei ist, dass Mittelwert und Median vor allem bei den Erkrankungszahlen deutlich voneinander abweichen, 
# was möglicherweise für die Anwesenheit von Ausreißern spricht. Um dies genauer zu untersuchen, wird ein Boxplot erstellt:

# In[217]:


cols = ['deaths','cases']
todaysum_country[cols].plot(kind='box', subplots=True)


# Sowohl Fallzahlen als auch Todesfälle enthalten starke Ausreißer nach oben, was bedeutet, dass es vor allem einige
# wenige, stark betroffende Länder gibt. Dies zeigen ebenfalls die Maximalzahlen an.
# 
# Daher folgt nun eine Wertesortierung mit den Top10-Ländern der höchsten Fall- bzw. Todeszahlen:

# In[218]:


today_cases = todaysum_country[['cases','deaths','popData2018']]
today_deaths = todaysum_country[['deaths','cases','popData2018']]


# In[219]:


today_cases.sort_values(by=['cases'], ascending=False)[0:10]


# In[220]:


today_deaths.sort_values(by=['deaths'], ascending=False)[0:10]


# In[221]:


plt.plot(todaysum_country[['deaths']])
plt.title('Deaths per Country')


# In[222]:


todaysum_country.plot(kind='scatter', y='deaths', x='popData2018')


# Zu sehen ist hier, dass Fall- und Todeszahlen vor allem in großen Ländern besonders hoch sind. Wie wir vorhin
# gesehen haben, korrelieren diese Zahlen aber nicht zwingend mit der Einwohnerzahl. Für einen besseren Überblick,
# schauen wir uns daher noch die Top10 der Fallzahlen pro Einwohner an. 

# In[223]:


todaysum_country['casesperpop'] = todaysum_country['cases']/todaysum_country['popData2018']
today_casesbypop = todaysum_country[['casesperpop','deaths','cases','popData2018']]
today_casesbypop.sort_values(by=['deaths'], ascending=False)[0:10]


# Unter den am stärksten betroffenden Ländern der Covid19-Krise pro Einwohnerzahl sind nach den USA vor allem viele
# europäische Länder. Ob dies der Realität entspricht oder an mangelnder Intransparenz der Länder liegt, muss an anderer
# Stelle geklärt werden.

# ## 3.2) Zeitreihenbetrachtung 

# In[225]:


todaysum_date = data.groupby(['dateRep','countriesAndTerritories']).sum()
todaysum_month = data.groupby(['month','countriesAndTerritories']).sum()
todaysum_month.head()

