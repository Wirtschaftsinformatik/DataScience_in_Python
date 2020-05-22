# package import
import matplotlib.pyplot as plt
import pandas as pd

# data import
data = pd.read_csv("covid_data_2.csv")

# change to datetime format
data["dateRep"] = pd.to_datetime(data["dateRep"], dayfirst=True)

# todo: find out cases per continent as flow over time
# group data
data2 = data.iloc[:, [0, 4, 5, 10]]
data2 = data.groupby(["continentExp", "dateRep"]).sum()
data2 = data2.iloc[:, [3, 4]]
df2 = data2.reset_index(level="continentExp")

# visualize
fig, ax = plt.subplots()
for key, grp in df2.groupby(["continentExp"]):
	ax = grp.plot(ax=ax, kind="line", y="cases", label=key)
plt.title("Cases per Continent and Day")
plt.xlabel("Date")
plt.ylabel("Cases")
plt.show()
# todo: find out, if death cases correlate with avg age (visually)
# import file for median age
popage = pd.read_csv("popagedata.csv")

# sort data
data_2 = data.iloc[:, [4, 5, 6, 10]]
data_2 = data_2.groupby(["countriesAndTerritories"]).sum()

# rewrite continent to grouped list
helpframe = data.iloc[:, [6, 10]]
helpframe = helpframe.drop_duplicates(subset="countriesAndTerritories", keep='first', inplace=False)
data_2 = pd.merge(data_2, helpframe, how="left", on="countriesAndTerritories")

# merge lists of age and covid data
popage = popage.rename(index=str, columns={"Place": "countriesAndTerritories"})
mlist = pd.merge(popage, data_2, how="left", on="countriesAndTerritories")

# calc. deathrate
mlist["deathrate"] = (mlist["deaths"] / mlist["cases"])
mlist.dropna()

# visualize
# vislist = mlist.iloc[:, [-2, 4, 1, -1]]
vislist = mlist.iloc[:, [-2, 4, 1, -1, 0]]
fig, ax = plt.subplots()
colors = {"Africa": "red", "Europe": "blue", "America": "green", "Asia": "black", "Oceania": "yellow"}
grouped = vislist.groupby("continentExp")
for key, group in grouped:
    group.plot(ax=ax, kind="scatter", x="deathrate", y="Median", label=key, color=colors[key],s=vislist["cases"] / 1000)
    temp = group[group['cases'] == group['cases'].max()]
    text = '{}: {}'.format(temp.iloc[0]['countriesAndTerritories'], temp.iloc[0]['cases'])
    x=temp.iloc[0]['deathrate']
    y=temp.iloc[0]['Median']
    plt.annotate(s=text, xy=(x, y))
plt.savefig('sven')
plt.show()
