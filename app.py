# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 13:39:36 2020

@author: gauravrai
"""


import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import random
from dash.dependencies import Output,Input
import dash_auth
import pathlib

DATA_PATH = pathlib.Path(__file__).parent.joinpath("data").resolve()
data=pd.read_csv(DATA_PATH.joinpath("hr.csv"))

USERNAME_PASSWORD_PAIRS=[['gauravcs08','fvpl@123']]
    




'''--------------------------------Bivariant Analysis-----------------------------------'''
# Department wise number of Employees
k=data.groupby('department',as_index=False).aggregate({'employee_id':'count','is_promoted':'sum'})
k1=data.groupby('education',as_index=False).aggregate({'employee_id':'count','is_promoted':'sum'})
k2=data.groupby('awards_won?',as_index=False).aggregate({'employee_id':'count','is_promoted':'sum'})
k3=data.groupby('KPIs_met >80%',as_index=False).aggregate({'employee_id':'count','is_promoted':'sum'})

'''-------------------------Visualization------------------------------------------------'''
fig_biva=make_subplots(rows=1,cols=4,subplot_titles=("Department Wise Employee Vs Promotee","Education wise Employee Vs Promotee","Relation between Award and Promotion","Relation between KPI and Promotion"))
fig_biva.add_trace(go.Bar(x=k['department'],y=k['employee_id'],name='Total Employees'),row=1,col=1).append_trace(go.Bar(x=k['department'],y=k['is_promoted'],name='Promoted'),row=1,col=1)
fig_biva.add_trace(go.Bar(x=k1['education'],y=k1['employee_id'],name='Total Employees (EDU)'),row=1,col=2).append_trace(go.Bar(x=k1['education'],y=k1['is_promoted'],name='Promoted (EDU)'),row=1,col=2)
fig_biva.add_trace(go.Bar(x=k2['awards_won?'],y=k2['employee_id'],name='Total Employees (Award)'),row=1,col=3).append_trace(go.Bar(x=k2['awards_won?'],y=k2['is_promoted'],name='Promoted (Award)'),row=1,col=3)
fig_biva.update_xaxes(tickvals = [0,1],ticktext=['No Award','Award'],row=1,col=3)
fig_biva.add_trace(go.Bar(x=k3['KPIs_met >80%'],y=k3['employee_id'],name='Total Employees (KPI)'),row=1,col=4).append_trace(go.Bar(x=k3['KPIs_met >80%'],y=k3['is_promoted'],name='Promoted (KPI)'),row=1,col=4)
fig_biva.update_xaxes(tickvals = [0,1],ticktext=['KPI<80','KPI>80'],row=1,col=4)



'''----------------------------Bi-Variant Visualization part2-----------------------------'''

fig_biva1=make_subplots(rows=1,cols=4,subplot_titles=("Department Wise Promotion %","Education wise Promotion %","Promotion Rate after gettion Award","Relation Rate after more the 80% KPI"))
fig_biva1.add_trace(go.Bar(x=k['department'],y=(k['is_promoted']/k['employee_id'])*100,name='Department wise Promotion Percentage'),row=1,col=1)
fig_biva1.add_trace(go.Bar(x=k1['education'],y=(k1['is_promoted']/k1['employee_id'])*100,name='Education wise Promotion %'),row=1,col=2)
fig_biva1.add_trace(go.Bar(x=k2['awards_won?'],y=(k2['is_promoted']/k2['employee_id'])*100,name='Award wise promotion %'),row=1,col=3)
fig_biva1.update_xaxes(tickvals = [0,1],ticktext=['No Award','Award'],row=1,col=3)
fig_biva1.add_trace(go.Bar(x=k3['KPIs_met >80%'],y=(k3['is_promoted']/k3['employee_id'])*100,name='KPI wise promotion %'),row=1,col=4)
fig_biva1.update_xaxes(tickvals = [0,1],ticktext=['KPI<80','KPI>80'],row=1,col=4)

#annotations
fig_biva1.update_traces(texttemplate='%{text:.2s}%',text=(k['is_promoted']/k['employee_id'])*100,textposition='auto',textfont_size=14,row=1,col=1)
fig_biva1.update_traces(texttemplate='%{text:.2s}%',text=(k1['is_promoted']/k1['employee_id'])*100,textposition='auto',textfont_size=14,textfont_color="White",row=1,col=2)
fig_biva1.update_traces(texttemplate='%{text:.2s}%',text=(k2['is_promoted']/k2['employee_id'])*100,textposition='auto',textfont_size=14,textfont_color="White",row=1,col=3)
fig_biva1.update_traces(texttemplate='%{text:.2s}%',text=(k3['is_promoted']/k3['employee_id'])*100,textposition='auto',textfont_size=14,textfont_color="White",row=1,col=4)

#Remove ylabels
fig_biva1.update_yaxes(showticklabels=False,row=1)

for i in fig_biva['layout']['annotations']:
    i['font'] = dict(size=11,color='Blue')

for j in fig_biva1['layout']['annotations']:
    j['font'] = dict(size=11,color='Blue')


'''--------------------Map of Region------------------'''

loc=data['region'].unique()
latitude=[]
longitude=[]
for i in range(len(loc)):
    latitude.append(random.randint(12,34))
    longitude.append(random.randint(74,85))
loc1={"region":loc,"latitude":latitude,"longitude":longitude}
loc=pd.DataFrame(loc1)

#ps.set_mapbox_access_token(open(".mapbox_token").read())
loc_fig = go.Figure(go.Scattermapbox(lat=loc["latitude"], lon=loc["longitude"],text=loc['region'],marker_color ='blue',mode='markers'))

#loc_fig=go.Figure(go.Scattergeo(lat=loc['latitude'],lon=loc['longitude'],text=loc['region'],marker_color ='blue',mode='markers'))
loc_fig.update_layout(
        title = 'Location of office',
        autosize=True,
        mapbox= dict(accesstoken="pk.eyJ1IjoiZ2F1cmF2Y3MwOCIsImEiOiJja2Q1dGFoZ2UwM2d5MnhsZnE3ZmNmZnMwIn0.OZb1Dnh_YdcB8T4gTRAYMQ",
                                
                                bearing=0,
                                pitch=0,
                                zoom=2,
                                center=go.layout.mapbox.Center(lat=20.721319,
                                             lon=110.987130)
                                ),
        hovermode='closest',
    )





'''--------------------------Dashboard Designing Part------------------------------'''
app=dash.Dash(__name__)
server=app.server

auth=dash_auth.BasicAuth(app,USERNAME_PASSWORD_PAIRS)

app.layout=html.Div(children=[
                html.Div(
                html.H1("Capestone Project for HR Analytics"),style={'color': 'white', 'fontSize': 18,'background-color': '#33004d','border':'10px black solid','text-align':'center'}),
                html.Div(html.H2("Univariant analysis of HR Data"),style={'color': 'white','background-color': '#aa00ff','Border':'20px white solid'}),
                html.Div([
                    dcc.Dropdown(id='feat',
                                 options=[{'label':i,'value':i} for i in ['age','no_of_trainings','length_of_service','avg_training_score']],
                                 value='age')
                    ],style={'color': '#33004d', 'fontSize': 14,'background-color': '#33004d','border':'5px black solid','text-align':'left'}),
                html.Div([dcc.Graph(id="univariant")]),
                html.Div(html.H2("Bivariant Analysis of HR Data"),style={'color': 'white','background-color': '#aa00ff'}),
                html.Div([dcc.Graph(id="Bivariant",
                                   figure=fig_biva)
                          ]),
                html.Div(html.H2("Feature wise chance of Promotion"),style={'color': 'white','background-color': '#aa00ff'}),
                html.Div([dcc.Graph(id="Bivariant1",
                                   figure=fig_biva1)
                          ]),
                html.Div(html.H2("Office Locations of Organization"),style={'color': 'white','background-color': '#aa00ff'}),
                html.Div(dcc.Graph(id='location',figure=loc_fig))
                ],style={'background-color': '#aa00ff','Border':'20px white solid'})


@app.callback(Output('univariant','figure'),
              [Input('feat','value')])

def updateunivariant(univ):
    return {'data':[go.Histogram(x=data[univ],nbinsx=10,name=univ,marker_color='#330C73')],
           'layout':go.Layout(title='Univariant Analysis of {}'.format(univ),titlefont={"size": 15,'color':'#33004d'},yaxis={'title':'Distribution of {}'.format(univ)})}

if __name__=='__main__':
    app.run_server(debug='True')
