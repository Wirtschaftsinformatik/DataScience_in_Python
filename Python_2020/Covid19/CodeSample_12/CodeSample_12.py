import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State
from plotly.graph_objs import *
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import dash_table
import numpy as np
import pandas as pd
# Dictionary for Missing_Values countryterritoryCode and Population2018 from the Worldbank data :
CountryCode={"AI":("AIA",17422),
             "BQ":("BES",19549),
             "FK":("FLK",3234),
             "ER":("ERI",6050000),
             "EH":("ESH",597339)
             }
# 1- Step : Loading Excel spreadsheet as pandas DataFrame Data will be loaded from Excel spreadsheet as pandas Dataframe.
Coviddaten= pd.read_excel("COVID19.xlsx")
# Show the 20 first Lines of Coviddaten Dataframe.
print("\n ---------------------------The 20 first Lines of Coviddaten :---------------------------\n")
print(Coviddaten.head(20))
# 2- Step : Data Preparation : Show some basic Informations about Features :
print("\n ---------------------------Type of Features---------------------------------------------\n")
print(Coviddaten.info())
# Display the Columns with Missing values
print("\n ---------------------------Columns with True contain Missing-Values:--------------------\n")
print(Coviddaten.isna().any())
print("The Dataframe contains "+str(Coviddaten.isna().any().sum())+" Columns with Missing-Values\n")
print(" The Feature geoId contains "+ str(Coviddaten.geoId.isna().sum())+" Missing Values\n")
print(" The Feature countryterritoryCode contains "+  str(Coviddaten.countryterritoryCode.isna().sum())+" Missing Values\n")
print(" The Feature popData2018 contains "+ str(Coviddaten.popData2018.isna().sum())+" Missing Values\n")
#geoId:alpha2 codes are two-letter country codes
#countryterritoryCode: ISO-3166 alpha3
print("\n ---------------------------Display  of the Missing Values for geoId  :------------------\n")
Missing_ValuegeoId=Coviddaten[Coviddaten["geoId"].isna()]
print(Missing_ValuegeoId.geoId)
#Replace geoId with the appropriate GeoId : NA
print("\n ---------------------------Display of the Missing Values for countriesAndTerritories  :--------\n")
Missing_Value_CoutryCode=pd.DataFrame(Coviddaten[Coviddaten["countryterritoryCode"].isna()])
print(Missing_Value_CoutryCode.head())
print("\n -----------------------------Missing Value per  countriesAndTerritories  :---------------------\n")
print(Missing_Value_CoutryCode["countriesAndTerritories"].value_counts())
print("Anzahl an Missingvalue für countryterritoryCode "+ str(Coviddaten.countryterritoryCode.isna().sum()))
#Features cases and Deaths contains some negativ values: because some countries as Ecuador, Spain , Benin ,United Kingdom have revised the total of cases and deaths.
# those Values will be converted to 0, because the Features Cases and Deaths represent the Daily new cases and not the Total of Cses.
# The Missing Values will be filled with the above created Dictionary:
print("\n Handling the Missing Value and illogical Values using above created dictionary:.......\n")
Coviddaten["geoId"] = np.where(Coviddaten["geoId"].isna(), "NA", Coviddaten["geoId"])
for ind in Coviddaten.index:
        if Coviddaten.iloc[ind,7]=="AI":
            Coviddaten.iloc[ind,8]=CountryCode["AI"][0]
            Coviddaten.iloc[ind,9]=CountryCode["AI"][1]
        if Coviddaten.iloc[ind,7]=="BQ":
            Coviddaten.iloc[ind, 8] = CountryCode["BQ"][0]
            Coviddaten.iloc[ind, 9] = CountryCode["BQ"][1]
        if Coviddaten.iloc[ind, 7] == "FK":
            Coviddaten.iloc[ind, 8] = CountryCode["FK"][0]
            Coviddaten.iloc[ind, 9] = CountryCode["FK"][1]
        if Coviddaten.iloc[ind, 7] == "ER":
            Coviddaten.iloc[ind, 8] = CountryCode["ER"][0]
            Coviddaten.iloc[ind, 9] = CountryCode["ER"][1]
        if Coviddaten.iloc[ind, 7] == "EH":
            Coviddaten.iloc[ind, 8] = CountryCode["EH"][0]
            Coviddaten.iloc[ind, 9] = CountryCode["EH"][1]
        if Coviddaten.iloc[ind,4]<0 :
            Coviddaten.iloc[ind,4]=0
        if Coviddaten.iloc[ind,5]<0:
            Coviddaten.iloc[ind,5]=0
# Rows with Cases_on_an_international_conveyance_Japan will be deleted because it depends on multiple Countries.
# Get names of indexes for which column geoId has value JPG11668
indexNames = Coviddaten[ Coviddaten['geoId'] == "JPG11668" ].index
Coviddaten.drop(indexNames,inplace=True,axis=0)
print(" The Feature geoId contains "+ str(Coviddaten.geoId.isna().sum())+" Missing Values\n")
print(" The Feature countryterritoryCode contains "+  str(Coviddaten.countryterritoryCode.isna().sum())+" Missing Values\n")
print(" The Feature popData2018 contains "+ str(Coviddaten.popData2018.isna().sum())+" Missing Values\n")
#the Dataframe ratedata contains the sum of Cases and Deaths by Country, it will be used to create a new Column Death-Rate.
ratedata=Coviddaten.groupby(["countriesAndTerritories","countryterritoryCode"],as_index=False)[["cases","deaths"]].sum()
ratedata_idx=ratedata.set_index('countriesAndTerritories')
#deathrate is created
ratedata_idx["DeathRate"]=round((ratedata_idx["deaths"]/ratedata_idx["cases"])*100,2)
ratedata_idx["DeathRate"] = np.where(ratedata_idx["DeathRate"].isna(), 0, ratedata_idx["DeathRate"])
# the preprocessed File will be loaded as an Excel sheet and will be saved in the same folder as the Application.
#print("The preprocessed File will be saved in the same folder as the app with the name Coviddaten_prepared.........")
#writer = pd.ExcelWriter('Coviddaten_prepared.xlsx')
# write dataframe to excel
#Coviddaten.to_excel(writer)
#writer.save()
# Here we can use the previous preprocessed File or we can import a new Preprocessed File  .
#Coviddaten = pd.read_excel("Coviddaten_prepared.xlsx", keep_default_na=False)

#2-Step:  Statistical  Analysis:

# For the Data Analysis,i created a  Dashboard as a Web-based analytic apps. i worked with Dash-Python framework.
# The Dashboard will appear in the Web Browser :
#Preparation of the used Dataframes:
#Dataframe with the Statistical Description of numerical Features
Datatable=(pd.DataFrame(Coviddaten.describe()))
#Grouped by Country Data:
df=Coviddaten.groupby(["countriesAndTerritories","countryterritoryCode"],as_index=False).sum()
#set the Index for df to facilate the Filtering od Columns and Rows, with .loc()
df2_idx = df.set_index('countriesAndTerritories')
# Add a new Column Cumul for the cumulative Sum of Cases.
Cumu=Coviddaten.sort_values(by="dateRep",ascending=True)
Cumu["cumul"]=Cumu.groupby("countriesAndTerritories")["cases"].cumsum()
#selecting Data for the Bubble-Map animation.
Cumu_Animation= Cumu[Cumu["dateRep"]>"2020-01-18"]
#selecting Data for the predefined time-series Plot for china and Italy in Tab2
dataChina = Coviddaten[Coviddaten["countriesAndTerritories"] == "China"]
dataItaly = Coviddaten[Coviddaten["countriesAndTerritories"] == "Italy"]
World=["{:,}".format(Coviddaten.cases.sum()),"{:,}".format(Coviddaten.deaths.sum())]
# cor_data contains the Correlation-Values between all the Features.
cor_data = (Coviddaten
            .corr().stack()
            .reset_index()
            .rename(columns={0: 'correlation', 'level_0': 'variable1', 'level_1': 'variable2'})
            )
cor_data['correlation_label'] = cor_data['correlation'].map('{:.2f}'.format)
# the Dash Application will start here....
app = dash.Dash(__name__)
app.title = 'Covid-19 Data Analysis'
server = app.server
# a external sytlesheet is loaded using Bootstrap library
app=dash.Dash(external_stylesheets=[dbc.themes.LUX])
# A Dash application is composed of two parts:
# 1- Layout, and it describes what the application looks like and it contains:
# 1-a The dash_html_components library, where  classes for all of the HTML tags will be provides.
# 1-b The dash_core_components library generates higher-level components like controls and graphs.
#2- The second part describes the interactivity of the application using customized Functions and Callbacks().
# Two Dropdowns will be created to choose the Feature and the country to be visualized in Histogram
inputs = dbc.FormGroup([
    html.Br(),
    html.H4("Select Feature"),
    html.Br(),
    dcc.Dropdown(id="selected_feature", options=[{"label":x,"value":x} for x in Coviddaten.columns], value="dateRep"),
     ])
input=dbc.FormGroup([
    html.Br(),
    html.H4("Select Feature"),
    html.Br(),
dcc.Dropdown(id="country", options=[{"label":x,"value":x} for x in Coviddaten.countriesAndTerritories.unique()], value="Germany"),
    ])
continentD=dbc.FormGroup([
    html.Br(),
    html.H4("Select a Continent"),
    html.Br(),
dcc.Dropdown(id="continentD", options=[{"label":x,"value":x} for x in Coviddaten.continentExp.unique()], value="Europe"),
    ])
#The Start of the Layout
app.layout = html.Div(
    [
        dbc.Alert("Covid-19 Data Analysis",color="primary"),
        #The Dashboard is composed of two Tabs :
        dbc.Tabs(
        [
        #The first Tab contains the Statistical Analysis of Features, where Histograms, Scatters, Heatmap will be showed
            # in function of the selected Feature and country.
        dbc.Tab(
            html.Div([
        dbc.Container(children=[
            dbc.Row([
                # Panel where descriptive Infomration(min, max, count))about the Features will be showed.
                dbc.Col(md=3,children=[
                    html.Br(),html.Br(),html.Br(),html.Br(),
                    inputs,
                    html.Br(),
                    html.Div(id="output-panel",style={"margin-top":"5"})
                ]),
                #Second part contains a 3 different Tabs for 3 different Graphics: Histogram, Scatter, Heatmap
                dbc.Col(md=9,children=[
                    html.Br(),html.Br(),
                    dbc.Col(html.H4("Feature Distribution"), width={"size": 6, "offset": 3}),
                    html.Br(),
                    dbc.Tabs(children=[
#1.Tab contains a Graph dash Component, where a histogram will be displayed
                        dbc.Tab(children=[dcc.Graph(id="Histogram"),html.Div(id="Comment")],label="Histogram"),
#2.Tab contains two Dropdown for the selection of Features and a Graph dash Component, where a Scatter will be displayed
                        dbc.Tab(children=[
                            html.Br(),
                            html.H6("Select two Features"),
                            dbc.Row(children=[
#Dropdown with the LIST OF Features
                                dbc.Col(children=dcc.Dropdown(id='my-dropdown1',
                                         options=[{"label": i, "value": i} for i in ["dateRep","cases","deaths","continentExp","popData2018","countryterritoryCode"]],#Coviddaten.columns],
                                         value='cases'
                                         ),width=5
                                        ),
                                dbc.Col(dcc.Dropdown(id='my-dropdown2',
                                         options=[{"label": i, "value": i} for i in Coviddaten.columns],
                                         value='dateRep'
                                         ),width=5
                                        )
                            ]),
                            #the Dash Component Graph contains a Scatter
                            dcc.Graph(id="Scatter",
                                      figure={'layout':{'title': "Dash Data Visualization","margin-right":"40px"}
                                              }
                                      ),
                            dbc.Container(id="ScatComment")],label="Scatter",
                        ),
                            #the Dash Component Graph contains a Scatter
                            dbc.Tab(children=[dcc.Graph(id="Heatmap",
                                          figure={"data":[go.Heatmap(
                                                                      z=cor_data["correlation_label"].tolist(),
                                                                      x=cor_data["variable1"].tolist(),
                                                                      y=cor_data["variable2"].tolist(),
                                                                       colorscale="Sunset"
                                                                    )
                                          ],
                                              "layout":{"xaxis":dict(title ="variable1"),"yaxis":dict(title="variable2"),
                                                        "width":"950","height":"500","title":"Correlation-Matrix"}
                                          }

                            ), dbc.Card(dbc.CardBody(children=[
                                html.P("- This chart displays a heat map of the correlation matrix."),
                                html.P("- The Correlation Matrix is a table showing correlation coefficient between all numerical variables."),
                                html.P("- Each cell in the table shows the correlation between two variables."),
                                html.P("- This plot allows to discover various subsets of the variables that seem to be highly correlated within the subset."),
                                html.P(" -In this dataset, we can see that cases and deaths seem to be highly related. Similarly,year and month seem to be related.")]),style={"padding-left":"100px","border":"None"})],label="Heatmap")
                            ])
                ])
            ])
        ]),
            ]),label="Statistical Analysis"
        ),
            #  2-Tab contains the Covid-19 TRACKER
        dbc.Tab(html.Div(
            dbc.Container(children=[
            #TopBar with the Daily-Status for each selected Country
                dbc.Row([
                    dbc.Col(children=[input],width=3),
                    dbc.Col(
                        html.Div(id="daily-stats"),
                    ),
                ]),
                # CHART 1:
                # Add a Chart with a line(Deaths) and bar(Cases) plot for the Exploration of the Relation btw the Deaths and Cases evolution.
                dbc.Row(
                    dbc.Col(
                        html.Div(
                            dbc.Row(children=[
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.Div(
                                                    id="confirmed-cases-chart-title",
                                                    className="bottom-chart-h1-title",
                                                ),
                                                html.Div(
                                                    "Daily new confirmed COVID-19 cases vs deaths",
                                                ),
                                                html.Div(
                                                    dcc.Loading(
                                                        dcc.Graph(
                                                            id="confirmed-cases-timeline",
                                                            # figure=cases_chart(),
                                                            config={"responsive": False},
                                                            style={"height": "300px"},
                                                        ),
                                                    ),
                                                    id="chart-container1",
                                                ),
                                            ]
                                        )
                                    ), width=6,
                                ),

                                # CHART 2:
                                # Add a chart with a Comparison between 2 predefined countries, and a selected Country

                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.Div(
                                                    id="infection-trajectory-title",
                                                    # "Infection Trajectory",
                                                    className="bottom-chart-h1-title",
                                                ),
                                                html.Div(
                                                    "Comparison of the Confirmed Cases between 3 Countries ",
                                                    className="bottom-chart-h2-title",
                                                ),
                                                html.Div(
                                                    dcc.Loading(
                                                        dcc.Graph(
                                                            id="infection-trajectory-chart",

                                                            config={"responsive": False},
                                                            style={"height": "300px"},

                                                        ),
                                                        style={"padding-top": "8px","padding-bottom":"20px"},
                                                        color="#19202A",
                                                    ),
                                                    id="chart-container3",
                                                ),
                                            ]
                                        ),
                                    ),
                                    className="top-bottom-right-chart",
                                    width=6,
                                ),
                            ], no_gutters=True,

                            )
                        ,style={"padding-bottom":"50px"})
                    )
                ),
                dbc.Row(children=[
                    dbc.Col(children=[continentD,
                                html.Div(id="Continent_Bar",style={"margin-top":"5"})

                    ],width=3),
                    dbc.Col(dcc.Graph(id="Horizbarchart"),width=9)
                ]),
                # Add a Table as a ListView with the latest Sum of Cases and Deaths for each Country
                dbc.Row(children=[

                    #Add a animated Map-Chart with the Evolution of the Total of cases per Country, the size is defined by the Sum of Cases and the color by the Continent.
                    dbc.Col( children=[dbc.Row(html.Div(html.P("The figure below is an interactive map,it shows the coronavirus spread, the map allows you to see which parts of the world are impacted the most by it.At least "+World[1]+" people globally have died from COVID-19 and "+World[0]+" have been infected by the novel coronavirus that causes it, following an outbreak that started in Wuhan, China, in December."),style={"padding-top":"50px","padding-left":"50px"})),
                        dcc.Graph(id="Map_country",
                                  figure = px.scatter_geo(Cumu_Animation,
                                                          title="Tracking the spread of the novel coronavirus",
                                                          locations="countryterritoryCode",
                                                          hover_name="countriesAndTerritories",
                                                          size="cumul",
                                                          animation_frame=Cumu_Animation.dateRep.astype(str),
                                                          projection="equirectangular", width=1000,
                                                          height=650,
                                                          scope="world",
                                                          size_max=100,
                                                          color="continentExp",
                                                           ),
                                                      )],style={"margin":"center"})
                ]),

                ])
        ),label="COVID-19 Tracker"),
            html.Br(),html.Br()
]
            )
])
########    Functions Part

# Function to create and display Histogram after choosing a Feature:
@app.callback(Output("Histogram","figure"), [Input("selected_feature","value")])
def Hist_Draw(selected_feature):
    if selected_feature=="None":
       selected_feature="dateRep"
# With the marginal keyword, a subplot is drawn alongside the histogram, visualizing the distribution.
    fig=px.histogram(Coviddaten,x=selected_feature,color="continentExp",marginal="box",hover_data=df.columns,title='Combined representations of statistical distributions of '+str(selected_feature),
                     width=950,height=500,nbins=70)
    if selected_feature in ("cases","deaths"):
        fig = px.bar(Coviddaten, x="dateRep", y=selected_feature, color="continentExp",
                           title='Combined representations of statistical distributions of ' + str(selected_feature),
                           width=950, height=500)

    fig.update_layout(
            margin={"r": 0, "t": 100, "l": 0, "b": 1},
            template="plotly_white",
            autosize=False,
            showlegend=True,
            legend_orientation="h",
            paper_bgcolor="rgba(0,0,0,0)",
            hoverlabel={"font": {"color": "black"}},
            xaxis_showgrid=False,
            yaxis_showgrid=False,
            font=dict(family="Julius Sans One, sans-serif", size=12, color="black"),
            yaxis_title="Sum of cases",
            xaxis_title="Date",
        )
    if selected_feature=="year":
            fig.update_layout(xaxis=dict(
                tickmode='array',
                tickvals=[2019, 2020],
                ticktext=['2019', "2020"]))
    elif selected_feature=="month":
            fig.update_layout(xaxis=dict(
                tickmode='array',
                tickvals=[1,2,3,4,5,6,7,8,9,10,11,12],
                ticktext=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
            )
    return fig

#Function to create Scatter, two Features have to be selected
@app.callback(Output("Scatter","figure"),
             [Input("my-dropdown1","value"),
              Input("my-dropdown2","value")])

def Scatter_Draw(selected_value1,selected_value2):
    if (selected_value1 == "cases" and selected_value2 == "deaths") or (
            selected_value1 == "deaths" and selected_value2 == "cases"):
           fig=px.scatter(Coviddaten, x=selected_value1, y=selected_value2, color="continentExp",width=950,height=500,title="Scatter-Plot",trendline="ols")
        #   fig.update_layout(plot_bgcolor='White', autosize=False, width=800, height=550)
    else:
            fig=px.scatter(Coviddaten, x=selected_value1, y=selected_value2, color="continentExp",width=950,height=500,title="Scatter-Plot")

    fig.update_layout(
                margin={"r": 0, "t": 50, "l": 0, "b": 1},
                template="plotly_white",
                autosize=False,
                showlegend=True,
                legend_orientation="h",
                paper_bgcolor="rgba(0,0,0,0)",
                hoverlabel={"font": {"color": "black"}},
                xaxis_showgrid=False,
                yaxis_showgrid=False,
                font=dict(family="Roboto, sans-serif", size=10, color="black"),
                yaxis_title=selected_value2,
                xaxis_title=selected_value1,
                plot_bgcolor='White')
    return fig
#Function to display the Panel with Information about Features.
@app.callback(Output("output-panel", "children"),
              [Input("selected_feature", "value")])
def render_output_panel(selected_feature):
    if selected_feature in ("day","month","cases","deaths","popData2018","year"):
        panel = html.Div([
        html.H4(selected_feature),
        dbc.Card(body=True, className="text-white bg-primary", children=[
            html.H6("Count of values :", style={"color": "white"}),
            html.H3("{:,.0f}".format(Datatable.loc["count",selected_feature]), style={"color": "white"}),
            html.H6("Mean of values :", style={"color": "white"}),
            html.H3("{:,.0f}".format(Datatable.loc["mean", selected_feature]), style={"color": "white"}),
            html.H6("Minmum of values :", style={"color": "white"}),
            html.H3("{:,.0f}".format(Datatable.loc["min", selected_feature]), style={"color": "white"}),
            html.H6("Maximum of values :", style={"color": "white"}),
            html.H3("{:,.0f}".format(Datatable.loc["max", selected_feature]), style={"color": "white"})
        ])
    ])
    elif selected_feature=="dateRep":
        panel = html.Div([
        html.H4(selected_feature),
        dbc.Card(body=True, className="text-white bg-primary", children=[
        html.H5("First Apparition of the Virus :", style={"color": "white","font":"bold"}),
        html.H6((Coviddaten[selected_feature].min()).date(), style={"color": "white"}),
        html.H5("Insights", style={"color": "white"}),
        html.P("- The count of different Dates is present in the Dataset",style={"color": "white"}),
            html.P(              "- The most of values are in:",style={"color": "white"}),
            html.P("   * Asia: From 17-02-2020 to 23-04-2020 ",style={"color": "white"}),
            html.P("   * Europe: From 20-02-2020 to 29-04-2020",style={"color": "white"}),
            html.P("   * America: From 29-03-2020 to 08-05-2020",style={"color": "white"}),
            html.P("   * Africa:From 02-04-2020 to 10-05-2020",style={"color": "white"}),
            html.P("   * Australia:From 23-03-2020 to 06-05-2020",style={"color": "white"})

            ]),
        ])
    elif selected_feature in("countriesAndTerritories","geoId","countryterritoryCode","continentExp") :
        k = Coviddaten["dateRep"].min()
        data=Coviddaten[(Coviddaten["dateRep"] ==k) & (Coviddaten["cases"] > 0)]
        panel = html.Div([
            html.H4(selected_feature,style={"fontSize":12}),
            dbc.Card(body=True, className="text-white bg-primary", children=[
                html.Br(),
                html.H6("Number of Affected Countries with Covid-19  :", style={"color": "white"}),
                html.H3(Coviddaten.countryterritoryCode.nunique(), style={"color": "white"}),
                html.Br(),
                html.H6("The first Affected Country with Covid-19 :", style={"color": "white"}),
                html.H6(data.countriesAndTerritories, style={"color": "white"}),
                html.H6("Continent :", style={"color": "white"}),
                html.H6(data.continentExp, style={"color": "white"}),
            ])])
    else:
        panel = html.Div([
            html.H4(selected_feature)])
    return panel
# Function to fill the Daily Status in the top Bar
@app.callback(Output("daily-stats", "children"), [Input("country", "value")])
def render_daily_state(country):
    df2_idx = df.set_index('countriesAndTerritories')
   # first_card = dbc.Card(
    #    dbc.CardBody(html.H5(country,style={"margin": "center","font-size":"12px"})),style={"border":"None","padding-top":"55px"}
    #)
    cases_Card=dbc.Card(
        dbc.CardBody( children=[
            html.H5("Confirmed",style={"color":"#F4B000"}),
            html.H6("{:,.0f}".format(df2_idx.loc[country, "cases"]),style={"color":"Orange"})]
        ),style={"border":"None","padding-top":"55px"})
    deaths_Card=dbc.Card(
        dbc.CardBody(children=[
            html.H5("Deaths",style={"color":"#E55465"}),
            html.H6("{:,.0f}".format(df2_idx.loc[country, "deaths"]),style={"color":"Red"})]
        ),style={"border":"None","padding-top":"55px"})
    ratio_Crads = dbc.Card(
        dbc.CardBody(children=[
            html.H5("Death Rate",style={"color":"#DD1E34"}),
            html.H6("{:,.0f}".format(ratedata_idx.loc[country, "DeathRate"])+"%")]
        ),style={"border":"None","padding-top":"55px"})
    cards = dbc.Row([ dbc.Col(cases_Card, md=3),dbc.Col(deaths_Card, md=3),dbc.Col(ratio_Crads, md=3)])
    return cards

#@app.callback(Output("country-table", "children"), [Input("country", "value")])
#Function to fill the DataTable in the left side
def stats_table(country):
    data = df.sort_values(by=["cases"], ascending=False)
    data = data.rename(
        columns={
            "countriesAndTerritories":"Country",
            "cases": "Confirmed",
            "deaths": "Deaths",
        }
    )
    table=dash_table.DataTable(
        data=data.to_dict("records"),
        columns=[
            {"name": "Country", "id": "Country" },
            {
                "name": "Confirmed",
                "id": "Confirmed",
                "type": "numeric"
            },
            {
                "name": "Deaths",
                "id": "Deaths",
                "type": "numeric",
            }
        ],
        style_table={
            "width": "100%",
            "height": "100vh",
        },
        style_header=
        {
            "font": "Lato, sans-serif",
            "height": "2vw",
            'border': 'thin lightgrey solid',
            "textAlign":"center",
            'width': '150px',
            'minWidth': '180px',
            'maxWidth': '180px',
        },
        style_cell={
            'textAlign': 'left',
            'whiteSpace': 'no-wrap',
            "font-size": "12px",
            "font-family": "Lato, sans-serif",
            "border-bottom": "0.01rem solid #313841",
            "height": "2.75vw",
        },
        style_data_conditional=[
            {
                'if': {'column_id': 'Country'},
                'color': 'black',
                'fontWeight': 'bold',
                'textAlign': 'center',
                'width': '150px',
                'minWidth': '180px',
                'maxWidth': '180px',
            },
            {
                "if": {"column_id": "Confirmed"},
                "color": "#F4B000",
            },
            {
                "if": {"column_id": "Deaths"},
                "color": "#E55465",
            }
            ],
        fixed_rows={'headers': True, 'data': 0},
        style_as_list_view=True,
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
    )
    return table
#Function to draw the combined Graph for confirmed Cases and Deaths
@app.callback(Output("confirmed-cases-timeline", "figure"), [Input("country", "value")])
def graph_country(country):
    dataCountry=Coviddaten[Coviddaten["countriesAndTerritories"]==country]
    print(dataCountry["cases"])
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=dataCountry.dateRep.astype(str),
            y=dataCountry["cases"],
            name="Total Confirmed Cases",
            line={"color": "#F4B000"},
            mode="lines",
        ),

    ),
    fig.add_trace(
        go.Bar(
            x=dataCountry.dateRep.astype(str),
            y=dataCountry["deaths"],
            name="Total deaths ",
            marker={"color": "Red"},
            #mode="lines",

        ),
    ),
    fig.add_trace(
        go.Bar(
            x=dataCountry["dateRep"],
            y=dataCountry["cases"],
            name="New Cases Added",
            marker={"color": "#F4B000"},
        )
    )
    fig.update_layout(
        margin={"r": 0, "t": 30, "l": 0, "b": 1},
        template="plotly_white",
        autosize=True,
        showlegend=True,
        #legend_orientation="h",
        paper_bgcolor="rgba(0,0,0,0)",
        hoverlabel={"font": {"color": "black"}},
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        xaxis={"tickformat": "%m/%d"},
        font=dict(family="Roboto, sans-serif", size=10, color="black"),
        yaxis_title="Number of cases",
        title=country + ". Confirmed Cases vs Deaths",
        barmode='overlay',
    ),
    fig.update_traces(opacity=0.5)
    return  fig
# Function to draw the Comparison Graph for 3 Countries
@app.callback(Output("infection-trajectory-chart", "figure"), [Input("country", "value")])
def trajectory_comparison(country):
    dataCountry = Coviddaten[Coviddaten["countriesAndTerritories"] == country]
    fig = go.Figure()
    fig.add_trace(
            go.Scatter(
            x=dataCountry.dateRep.astype(str),
            y=dataCountry["cases"],
            name="Total Cases in "+country,
            line={"color":"red"},
            mode="lines",
            hovertext=country,
        ),
    )
    fig.add_trace(
            go.Scatter(
            x=dataChina.dateRep.astype(str),
            y=dataChina["cases"],
            name="Total Cases in China",
            line={"color":"green"},
            mode="lines",
            hovertext="China",

        ),
    )
    fig.add_trace(
        go.Scatter(
            x=dataItaly.dateRep.astype(str),
            y=dataItaly["cases"],
            name="Total Cases in Italy",
            line={"color": "grey"},
            mode="lines",
            hovertext="Italy"
        ),
    )

    fig.update_layout(
        margin={"r": 0, "t": 30, "l": 0, "b": 1},
        template="plotly_white",
        # annotations=annotations,
        autosize=True,
        showlegend=True,
        #   legend_orientation="h",
        paper_bgcolor="rgba(0,0,0,0)",
        hoverlabel={"font": {"color": "black"}},
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        xaxis={"tickformat": "%m/%d"},
        font=dict(family="Lato, sans-serif", size=10, color="black"),
        yaxis_title="Number of cases",
        title=country + " Trajectory"
    )
    return fig
@app.callback(Output("Comment","children"),
             [Input("selected_feature","value"),
             # Input("selected_country","value")
              ])
def commen(selected_feature):
    if selected_feature=="dateRep":
       comment= dbc.Card(dbc.CardBody(children=[html.P("- The plot is based on a single Variable and show the frequency of uniques values of the variable dateRep."),
                                      html.P("- We can see that the count of different date present in the dataset are presented in the Histogram."),
                                    html.P("- The Boxplot shows, that the continents Oceania,America and Africa have a normal distributed Data because the median is splitting the Boxplot into two even pieces."),
                        html.P("- The rest of the continent have a negative skew.")]),style={"padding-left":"30px","border":"None"})
       return comment
    elif selected_feature == "cases":
        comment = dbc.Card(dbc.CardBody(children=[html.P("- The Bar chart above shows the Daily number of confirmed cases in different Continents."),
                                        html.P("-It can be seen that the chart have an extreme left skew what usually means that the distribution has a large range and an important standard deviation."),
                                  html.P("- The feature contains an important number of Outliers. ")]),style={"padding-left":"100px","border":"None"})
        return comment
    elif selected_feature == "deaths":
        comment = dbc.Card(dbc.CardBody(children=[html.P("- The Bar chart above shows the Daily number of confirmed deaths in different Continents."),
                                    html.P("- It can be seen that the chart have an less extreme left skew comparatively to the variable Cases, what usually means that the distribution has a large range and an important standard deviation."),
                                    html.P("- The feature contains an important number of Outliers. "),
                                    html.P("- Most deaths range is situated in Europe and America. ")]),style={"padding-left":"100px","border":"None"})
        return comment

@app.callback(Output("ScatComment","children"),
             [Input("my-dropdown1","value"),Input("my-dropdown2","value")])

def ScatCo(selected_value1,selected_value2):
    if (selected_value1 == "cases" and selected_value2 == "deaths") or (selected_value1 == "deaths" and selected_value2 == "cases"):
        a=dbc.Card(dbc.CardBody(children=[html.P("- The Scatter plot is used to find a relation between two variables and to find how the value of one variable change the value of another variable."),
                                html.P("- This chart illustrates the relationship between the variables cases and deaths, it shows a  moderate linear positive relationship."),
                                html.P("- The increase of confirmed cases leads to a high number of deaths.")]),style={"padding-left":"100px","border":"None"})
    else:
        a=""
    return a
@app.callback(Output("Horizbarchart","figure"),
             [Input("continentD","value")])

def Continent_Histo(continent):
    Cont = Coviddaten.groupby(["continentExp", "countriesAndTerritories"], as_index=False)[["cases", "deaths"]].sum()
    data=Cont[Cont["continentExp"]==continent]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=data["cases"],y=data["countriesAndTerritories"],orientation="h",marker_color="rgb(255, 204, 0)",name='Total cases',hovertext=data["cases"])),
    fig.add_trace(go.Bar(x=data["deaths"], y=data["countriesAndTerritories"], orientation="h", marker_color="rgb(255, 0, 0)",name='Total deaths',hovertext=["deaths"])),
    fig.update_layout(
        margin={"r": 0, "t": 30, "l": 0, "b": 1},
        xaxis_tickfont_size=14,
        template="plotly_white",
        height=600,
        width=950,
        title="Total confirmed Cases deaths in"+ str(continent),
        #barmode="group",
        bargap=0.25,  # gap between bars of adjacent location coordinates.
        bargroupgap=0.5,  # gap between bars of the same location coordinate.
        showlegend=True
    )
    return fig
@app.callback(Output("Continent_Bar","children"),
             [Input("continentD","value")])

def ScatCo(continent):
    Cont = Coviddaten.groupby(["continentExp", "countriesAndTerritories"], as_index=False)["cases", "deaths"].sum()
    data = Cont[Cont["continentExp"] == continent]
    max_Cases= data[data["cases"]==data["cases"].max()]
    max_deaths=data[data["deaths"]==data["deaths"].max()]
    min_Cases = data[data["cases"] == data["cases"].min()]
    min_deaths = data[data["deaths"] == data["deaths"].min()]

    if continent == "Asia":
        panel = html.Div([
            html.H4(continent),
            dbc.Card(body=True, className="text-white bg-primary", children=[
                html.H6(" The maximum Confirmed COVID-19 cases is detected in : ", style={"color": "white"}),
                html.H6(max_Cases["countriesAndTerritories"] + ":" + max_Cases["cases"].to_string(index=False),
                        style={"color": "orange"}),
                html.Br(),
                html.H6(" The minimum Confirmed COVID-19 cases is detected in :", style={"color": "white"}),
                html.H6(min_Cases["countriesAndTerritories"] + ":" + min_Cases["cases"].to_string(index=False),
                        style={"color": "orange"}),
                html.Br(),
                html.H6(" The maximum COVID-19 deaths is detected in : ", style={"color": "white"}),
                html.H6(max_deaths["countriesAndTerritories"] + ":" + max_deaths["deaths"].to_string(index=False),
                        style={"color": "red"}),
                html.Br(),

            ])])
    elif continent == "Africa":
        panel = html.Div([
            html.H4(continent),
            dbc.Card(body=True, className="text-white bg-primary", children=[
                html.H6(" The maximum Confirmed COVID-19 cases is detected in : ", style={"color": "white"}),
                html.H6(max_Cases["countriesAndTerritories"] + ":" + max_Cases["cases"].to_string(index=False),style={"color": "orange"}),
                html.Br(),
                html.H6(" The minimum Confirmed COVID-19 cases is detected in :", style={"color": "white"}),
                html.H6(min_Cases[ "countriesAndTerritories"]+":"+ min_Cases[ "cases"].to_string(index=False), style={"color": "orange"}),
                html.Br(),
                html.H6(" The maximum COVID-19 deaths is detected in : ", style={"color": "white"}),
                html.H6(max_deaths["countriesAndTerritories"] + ":" + max_deaths["deaths"].to_string(index=False), style={"color": "red"}),
                html.Br(),
                html.H6("The minimum COVID-19 cases is detected in :", style={"color": "white"}),
                html.H6(min_deaths["countriesAndTerritories"] , style={"color": "red","font-size":"14px"}),
            ])])
    elif continent == "Europe":
        panel = html.Div([
            html.H4(continent),
            dbc.Card(body=True, className="text-white bg-primary", children=[
                html.H6(" The maximum Confirmed COVID-19 cases is detected in : ", style={"color": "white"}),
                html.H6(max_Cases["countriesAndTerritories"] + ":" + max_Cases["cases"].to_string(index=False),style={"color": "orange"}),
                html.Br(),
                html.H6(" The minimum Confirmed COVID-19 cases is detected in :", style={"color": "white"}),
                html.H6(min_Cases["countriesAndTerritories"] + ":" + min_Cases["cases"].to_string(index=False),style={"color": "orange"}),
                html.Br(),
                html.H6(" The maximum COVID-19 deaths is detected in : ", style={"color": "white"}),
                html.H6(max_deaths["countriesAndTerritories"] + ":" + max_deaths["deaths"].to_string(index=False),style={"color": "red"}),
                html.Br(),
                html.H6("The minimum COVID-19 cases is detected in :", style={"color": "white"}),
                html.H6(min_deaths["countriesAndTerritories"] ,style={"color": "red"}),
            ])])
    elif continent == "America":
        panel = html.Div([
            html.H4(continent),
            dbc.Card(body=True, className="text-white bg-primary", children=[
                html.H6(" The maximum Confirmed COVID-19 cases is detected in : ", style={"color": "white"}),
                html.H6(max_Cases["countriesAndTerritories"] + ":" + max_Cases["cases"].to_string(index=False),
                        style={"color": "Orange"}),
                html.Br(),
                html.H6(" The minimum Confirmed COVID-19 cases is detected in :", style={"color": "white"}),
                html.H6(min_Cases["countriesAndTerritories"] + ":" + min_Cases["cases"].to_string(index=False),
                        style={"color": "Orange"}),
                html.Br(),
                html.H6(" The maximum  COVID-19 deaths is detected in : ", style={"color": "white"}),
                html.H6(max_deaths["countriesAndTerritories"] + ":" + max_deaths["deaths"].to_string(index=False),
                        style={"color": "red"}),
                html.Br(),
                html.H6("The minimum COVID-19 cases is detected in :", style={"color": "white"}),
                html.H6(min_deaths["countriesAndTerritories"],style={"color": "red","font-size":"14px"}),
            ])])
    else:
        panel = html.Div([
            html.H4(continent),
            dbc.Card(body=True, className="text-white bg-primary", children=[
                html.H6(" The maximum Confirmed COVID-19 cases is detected in : ", style={"color": "white"}),
                html.H6(max_Cases["countriesAndTerritories"] + ":" + max_Cases["cases"].to_string(index=False),
                        style={"color": "orange"}),
                html.Br(),
                html.H6(" The minimum Confirmed COVID-19 cases is detected in :", style={"color": "white"}),
                html.H6(min_Cases["countriesAndTerritories"] + ":" + min_Cases["cases"].to_string(index=False),
                        style={"color": "orange"}),
                html.Br(),
                html.H6(" The maximum COVID-19 deaths is detected in : ", style={"color": "white"}),
                html.H6(max_deaths["countriesAndTerritories"] + ":" + max_deaths["deaths"].to_string(index=False),
                        style={"color": "red"}),
                html.Br(),

            ])])
    return panel
#Run the app with
#and visit http://127.0.0.1:8050/ in your web browser. You should see the  app.
print("Please open the address://127.0.0.1:8050")
if __name__ == '__main__':
    app.run_server(debug=True)