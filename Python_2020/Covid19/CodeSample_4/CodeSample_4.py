###Corona-Projekt Paulina Schindler
#Erste Programmierung in Python
#Testen verschiedener verbreiteter Packages


##Import der Packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
#außerdem installiert zum Lesen der Excel-Datei: xlrd


##Datensatz laden (xlsx direkt gewählt, um Trennzeichen-Verwirrungen zu vermeiden)
df = pd.read_excel('COVID-19-geographic-disbtribution-worldwide.xlsx')


###--Data Understanding:-- (Auskommentiert, da nur zu Analyse nötig)
#print(type(df)) - der Datensatz ist ein DataFrame

#print(df.dtypes) - Formate der Daten
#dateRep: datetime = Datum der Messung (nicht jedes Land ist schon gleich lang in der Liste vertreten)
#day, month, year, cases, deaths: int = Datum der Messung getrennt + aktuelle Fall- und Todeszahlen (nicht kumuliert - bei cases handelt es sich vermutlich wie bei deaths um tägliche Neuerkrankungen - wäre sonst extrem schnelle Genesung ohne Tode)
#countriesAndTerritories, geoId, dountryterritoryCode: object = Identifikation des betrachteten Landes (für jedes Land gibt es einen Eintrag pro Tag)
#popData2018: float = Größe der Population des Landes 2018

#day, month und year wiederholen die Information aus dateRep; ebenso drücken countriesAndTerritories, geoId und countryterritoryCode das gleiche aus

##welche und wie viele Länder sind betroffen:
#print(df['countriesAndTerritories'].unique())
#print(len(df['countriesAndTerritories'].unique()))

#print(df.describe()) # zeigt mean, std, min und max an

##Auf mögliche Korrelation prüfen - keine unerwartete Korrelation
#print(df.corr())




###--Data Preparation--


##Redundanzen abbauen, ausreichend ist countriesAndTerritories
del df['geoId']
del df['countryterritoryCode']


##jeweiliger Anteil der Cases bzw. der Tode an der Gesamtbevölkerung
df['casesPercentage'] =  (df['cases'] / df['popData2018'] ) * 100
df['deathsPercentage'] =  (df['deaths'] / df['popData2018'] ) * 100


##Kumulieren und Gruppieren der aufgetretenen Fall- und Todeszahlen (da es keine Information über Genesung gibt, können keine genaueren Aussagen getroffen werden)
cum_cases_country = df.groupby('countriesAndTerritories')['cases','deaths','casesPercentage','deathsPercentage'].sum()
print(cum_cases_country)

cum_cases_date = df.groupby('dateRep')['cases','deaths'].sum()
print(cum_cases_date)


##Fälle und Tode pro Land
max_cases_country = df.groupby('countriesAndTerritories')['cases','deaths'].max()
print(max_cases_country)

max_cases_date = df.groupby('dateRep')['cases','deaths'].max()
print(max_cases_date)


##Datum mit den meisten Fällen ausgeben
date_max = max_cases_date['cases'].idxmax()
print(date_max)


##Dataframe, der nur Tage enthält, an denen über 10 Fälle registriert wurden
zehn = df[df['cases']>=10]
print(zehn.count())
#Fälle in Deutschland genauer betrachten
print(zehn[zehn['countriesAndTerritories']=='Germany'])


##Pivot-Table
summe = df.groupby('countriesAndTerritories').agg({'deaths':np.sum,'cases':np.sum}).reset_index()
print(summe)





###--Modeling--

#Fälle je Land anzeigen
df['countriesAndTerritories'].value_counts().plot(kind='bar',figsize=(20,10))
plt.title("Bisher aufgetretene Fälle je Land")
plt.xlabel("Länder")
plt.ylabel("Fälle")
plt.show()

#Fälle je Land in Prozent anzeigen
df['countriesAndTerritories'].value_counts().plot.pie(autopct="%1.1f%%")
plt.title("Fälle je Land - in Prozent")
plt.show()


##Plot des Verlaufs aller täglichen Neuerkrankungen drei ausgewählter, interessanter Länder
fig, ax = plt.subplots()

gruppe = df.groupby('countriesAndTerritories')
#Als betrachtete Länder ausgewählt: Deutschland, Italien, USA
for k, v in gruppe:
	if k == 'Germany' or k == 'Italy' or k == 'United_States_of_America':
		v.plot(x='dateRep', y='cases', label=k, alpha=.75, ax=ax)
ax.legend()

plt.title("Verlauf der Neuerkrankungen je Land")
plt.xlabel("Länder")
plt.ylabel("Neuerkrankungen")

plt.show()


##Gesamte Fälle und Tode im Zeitvergleich
df2 = df #kopieren des Datarframes
ts = df2.set_index('dateRep')
df_by_date = ts.groupby(['dateRep']).sum().reset_index(drop=None)
df_by_date[['cases', 'deaths']].plot(kind='line',figsize=(20,10))
plt.title("Alle Fälle und Tode im Zeitverlauf")
plt.xlabel("Zeit")
plt.ylabel("Anzahl")
plt.show()


##Vergleich aller Länder: Darstellung von Infizierten und Todesfällen, was zeigt, das das Verhältnis nicht in jedem Land gleich ist

plot_daten = df.groupby(['countriesAndTerritories'], as_index=False).sum()[['countriesAndTerritories', 'cases', 'deaths']]
def plot_bar_horizontal(data=plot_daten, sort=True):

	fig = go.Figure()

	#Fälle hinzufügen
	fig.add_trace(go.Bar(
		y=data['cases'],
		x=data['countriesAndTerritories'],
		orientation='v',
		name='Infizierte',
		marker_color='green'))

	#Tode hinzufügen
	fig.add_trace(go.Bar(
		y=data['deaths'],
		x=data['countriesAndTerritories'],
		orientation='v',
		name='Tote',
		marker_color='red'))

	fig.update_layout(barmode='group')
	fig.update_layout(title="Infizierte und Todesfälle der Länder")
	fig.update_layout(uniformtext_minsize=10, uniformtext_mode='show')

	fig.show()

plot_bar_horizontal()


##Boxplot-Diagramm
#Um Varianz zu reduzieren, werden nur die fallstärksten Einträge gespeichert (15 Länder)
plot_daten_top_cases = plot_daten.sort_values('cases', ascending=False).head(15)
plot_daten_top_deaths = plot_daten.sort_values('deaths', ascending=False).head(15)

def plot_boxplot(plot_value, data=plot_daten, width=500):
	fig = px.box(data, y=plot_value, points="all", hover_name="countriesAndTerritories",
				 color_discrete_sequence = px.colors.colorbrewer.Paired, width=width)
	fig.show()

#Boxplot der Infiziertenfälle
plot_boxplot(plot_value='cases', data=plot_daten_top_cases)

#Boxplot der Todesfälle
plot_boxplot(plot_value='deaths', data=plot_daten_top_deaths)

#Boxplot des Verhältnisses von Infizierten zu Todesfällen (hier alle Länder einbezogen)
plot_daten['ratio'] = plot_daten['deaths'] / plot_daten['cases'] * 100
plot_boxplot(plot_value='ratio')