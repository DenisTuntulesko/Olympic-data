import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import urllib.request 
from PIL import Image
import plotly.graph_objects as go
import plotly.express as px
from dash import Input, Output

df = pd.read_csv('https://raw.githubusercontent.com/DenisTuntulesko/Olympic-data/main/athlete_events.csv')
df_summer = df[df.Season == 'Summer']
df_winter = df[df.Season == 'Winter']

year = np.arange(1896,2017,4)
amount = []
for y in year:
    amount.append(df_summer[df_summer.Year == y].shape[0])
year = pd.Series(year, name = 'Year')
amount = pd.Series(amount, name = 'Amount')
games=[]
for y in year:
    games.append("Summer games")
games = pd.Series(games,name = 'Season')
year_am_sum = pd.concat([year,amount,games],axis=1)
    
year_1 = np.arange(1924,1993,4)
year_2 = np.arange(1994,2015,4)
year_1 = np.concatenate((year_1,year_2))
amount_1 = []
for y in year_1:
    amount_1.append(df_winter[df_winter.Year == y].shape[0])
year_1 = pd.Series(year_1, name = 'Year')
amount_1 = pd.Series(amount_1, name = 'Amount')
games_1=[]
for y in year_1:
    games_1.append("Winter games")
games_1 = pd.Series(games_1,name = 'Season')
year_am_win = pd.concat([year_1,amount_1,games_1],axis=1)


year_am = pd.concat([year_am_win,year_am_sum], axis = 0,ignore_index = True)
year_am.sort_values(by=['Year'],inplace = True)    

winter_medal = df_winter[df_winter['Medal'].notna()]
w_m_list = winter_medal.Sport.unique()
medal_amount = []
for s in w_m_list:
    medal_amount.append(winter_medal[winter_medal.Sport == s].shape[0])

summer_medal = df_summer[df_summer['Medal'].notna()]
s_m_list = summer_medal.Sport.unique()
medal_amount_1 = []
for s in s_m_list:
    medal_amount_1.append(summer_medal[summer_medal.Sport == s].shape[0])
s_m_list = pd.Series(s_m_list,name = 'Sport')
medal_amount_1 = pd.Series(medal_amount_1, name = 'Amount')
s_m = pd.concat([s_m_list,medal_amount_1], axis = 1)
s_m.sort_values(by=['Amount'],inplace = True)
s_m = s_m[s_m.Amount > 200]

sum_names = ['Michael Fred Phelps, II','Larysa Semenivna Latynina (Diriy-)','Nikolay Yefimovich Andrianov',
            'Borys Anfiyanovych Shakhlin','Takashi Ono','Edoardo Mangiarotti','Paavo Johannes Nurmi','Birgit Fischer-Schmidt',
            'Jennifer Elisabeth "Jenny" Thompson (-Cumpelik)','Sawao Kato']
med = []
g_m = []
for s in sum_names:
    med.append(summer_medal[summer_medal.Name == s].shape[0])
    g_m.append(summer_medal[(summer_medal.Name == s) & (summer_medal.Medal == 'Gold')].shape[0])
med = pd.Series(med,name='Medals')
g_m = pd.Series(g_m,name='Gold medals')
sum_names = pd.Series(sum_names,name = 'Name')
sum_sm = pd.concat([sum_names,med,g_m], axis = 1)
    
    
win_names = ['Ole Einar Bjrndalen','Raisa Petrovna Smetanina','Stefania Belmondo','Yang Yang','Marit Bjrgen',
            'Ursula "Uschi" Disl','Edy Sixten Jernberg','Claudia Pechstein',
             'Lyubov Ivanovna Yegorova','Gunda Niemann-Stirnemann-Kleemann']
med_1 = []
g_m_1 = []
for s in win_names:
    med_1.append(winter_medal[winter_medal.Name == s].shape[0])
    g_m_1.append(winter_medal[(winter_medal.Name == s) & (winter_medal.Medal == 'Gold')].shape[0])
med_1 = pd.Series(med_1,name='Medals')
g_m_1 = pd.Series(g_m_1,name='Gold medals')
win_names = pd.Series(win_names,name = 'Name')
win_sm = pd.concat([win_names,med_1,g_m_1], axis = 1)

urllib.request.urlretrieve('https://raw.githubusercontent.com/DenisTuntulesko/Olympic-data/main/images/ol_logo.png',"ol_logo.png")
img = Image.open("ol_logo.png")
 
app = dash.Dash(__name__)

app.title = "Olympic games data"

app.layout = html.Div(
   children = [
        html.Div(children=[html.Img(src = img),
                           "Данные по олимпийским играм с 1896 по 2016 год"], style={"fontSize": "36px","text-align": "center" },className="header"),
        
       
        dcc.Graph(
            figure=px.bar(year_am[-10:],x="Year",y="Amount",color='Season',title="Число участников на последних (из датасета) 5 зимних и летних Олимпийских игрх"),
        ),

        html.P(children = "Сезон:"),  
        
        dcc.Dropdown(['Зимние игры','Летние игры'],value = 'Зимние игры',id='season-dropdown'),
        html.Div(children = [dcc.Graph(figure={}, id = 'amount',style={'width' : '50%', 'display' : 'inline-block'}),
                 dcc.Graph(figure={}, id = 'age',style={'width' : '50%', 'display' : 'inline-block'})]),
        html.Div(children = [dcc.Graph(figure={}, id = 'pie',style={'width' : '50%', 'display' : 'inline-block'}),
                             dcc.Graph(figure={}, id = 'medals',style={'width' : '50%', 'display' : 'inline-block'})])] 
   
    
)   

@app.callback(
    Output(component_id = 'amount', component_property='figure'),
    Input(component_id='season-dropdown', component_property='value')
)
def update_graph_1(column):
    if(column == 'Зимние игры'):
        fig = px.line(year_am_win, x = 'Year',y='Amount',title='Количество участников зимних игр по годам')
    else:
        fig = px.line(year_am_sum, x = 'Year',y='Amount',title='Количество участников летних игр по годам',color_discrete_sequence=['orange'])
    return fig

@app.callback(
    Output(component_id = 'age', component_property='figure'),
    Input(component_id='season-dropdown', component_property='value')
)
def update_graph_2(column):
    if(column == 'Зимние игры'):
        fig = px.histogram(df_winter, x = 'Age',title='Распределение возрастов участников зимних игр')
    else:
        fig = px.histogram(df_summer, x = 'Age',title='Распределение возрастов участников летних игр',color_discrete_sequence=['orange'])
    return fig

@app.callback(
    Output(component_id = 'pie', component_property='figure'),
    Input(component_id='season-dropdown', component_property='value')
)
def update_graph_3(column):
    if(column == 'Зимние игры'):
        fig = px.pie(values=medal_amount, names=w_m_list,title = 'Доля всех медалей на каждый вид спорта')
    else:
        fig = px.pie(s_m,values='Amount', names='Sport',title = 'Доля всех медалей на каждый вид спорта')
    return fig

@app.callback(
    Output(component_id = 'medals', component_property='figure'),
    Input(component_id='season-dropdown', component_property='value')
)
def update_graph_4(column):
    if(column == 'Зимние игры'):
        fig = px.scatter(win_sm,x='Medals',y='Gold medals',hover_name="Name",title="Самые успешные спортсмены зимних игр")
    else:
        fig = px.scatter(sum_sm,x='Medals',y='Gold medals',hover_name="Name",title="Самые успешные спортсмены летних игр")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)