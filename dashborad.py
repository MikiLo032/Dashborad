import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
warnings.filterwarnings('ignore')

app = Dash(__name__)
df = pd.read_csv("C:/Users/user/OneDrive/文件/Dashborad/Weekly_Record.csv")

#######----

app.layout = html.Div([

    html.H1("Progress Report of KANA to MoEngage Migration", style={'text-align': 'center'}),
    html.Br(),

    # dcc.Dropdown(
        # id="Migration_status",
        #          options=[
        #              {"label": "Yet to raise WMR", "value": "Yet to raise WMR"},
        #              {"label": "Raised WMR", "value": "Raised WMR"},
        #              {"label": "Working In Progress", "value": "Working In Progress"},
        #              {"label": "Waiting for sign off", "value": "Waiting for sign off"},
        #           {"label": "Waiting for staging", "value": "Waiting for staging"},
        #          {"label": "Completed", "value": "Completed"}],
        #          multi=False,
        #          value="Yet to raise WMR",
        #          style={'width': "40%"}
        #          ),
dcc.Dropdown(id="Week",
             options=[
                     {"label": "First_Week", "value": "First_Week"},
                     {"label": "Sec_Week", "value": "Sec_Week"},
                     {"label": "Third_Week", "value": "Third_Week"}],
             optionHeight=25,
             multi=False,
             value="First_Week",
             style={'width': "40%"},
             searchable=True,
             clearable=True
                 ),
    # html.Div(id='output_container', children=[]),
    html.Br(),
    html.Div([dcc.Graph(id='our_graph',figure={})]),
    html.Br(),
    dcc.Checklist(
        id="checklist",
        options=["Yet to raise WMR","Raised WMR","Working In Progress","Waiting for sign off","Waiting for staging","Completed","Completed in First pharse"],
        value=["Yet to raise WMR","Raised WMR","Working In Progress","Waiting for sign off","Waiting for staging","Completed","Completed in First pharse"],
        inline=True
    ),
     dcc.Graph(id="graph")
])

### Connecting the Dropdown values to the graph
@app.callback(
    Output(component_id='our_graph', component_property='figure'),
    [Input(component_id='Week', component_property='value')]
)

def build_graph(column_chosen):
    dff=df
    label = ["Yet to raise WMR","Raised WMR","Working In Progress","Waiting for sign off","Waiting for staging","Completed","Completed in First pharse"]
    values = list(dff[column_chosen])
    # values = values.pop(6)
    colours = ['#440154', '#3e4989', '#26828e', '#35b779', '#fde725']
    fig = px.pie(dff,names=label,values=values,color_discrete_sequence=px.colors.sequential.Plasma)
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(title={'text':'Weekly Migration Progress',
                      'font':{'size':28},'x':0.5,'xanchor':'center'})
    return fig

@app.callback(
    Output("graph", "figure"), 
    Input("checklist", "value"))
def update_line_chart(continents):
    dff = df.transpose().copy() # replace with your own data source
    dff.columns = dff.iloc[0]
    dff=dff.drop(dff.index[0])
    fig = px.line(dff, 
        x=[1,2,3], y=continents, labels={'x':'Week','y':'Status'},color_discrete_sequence=px.colors.sequential.Viridis)
    return fig

# @app.callback(
#     Output(component_id='output_data', component_property='children'),
#     [Input(component_id='Week', component_property='search_value')]
# )
# def build_graph(data_chosen):
#     return ('Search value was: " {} "'.format(data_chosen))

if __name__ == '__main__':
    app.run_server(debug=True, port=8067) # or whatever you choose http://127.0.0.1:8050/
