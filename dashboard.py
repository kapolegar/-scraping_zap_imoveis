#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from dash import Dash, html, dcc, Input, Output, State, dash_table
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import dash


base = pd.read_csv('dataset.csv')         
            
# Removendo os bairros com apenas um imóvel e definindo a nova base

bairros = pd.DataFrame(base['bairro'].value_counts() == 1).reset_index()
base_bairros = bairros[bairros['bairro'] == True].rename(columns={'index': 'bairro','bairro': 'imovel_unico'})
base_bairros = pd.DataFrame(base_bairros['bairro']).reset_index(drop=True)
lista_bairros = list(base_bairros['bairro'])
base_remocao = base.drop(base[base['bairro'].isin(lista_bairros)].index)

# Definindo as linhas com imóveis sem valor de Aluguel registrado

define_alugueis = base_remocao['aluguel'] == 0
alugueis = pd.DataFrame(define_alugueis)
lista_alugueis = alugueis[alugueis['aluguel'] == True]

# Excluindo do DataFrame as linhas com imóveis sem valor de Aluguel registrado e definindo a nova base

indexalugueis = lista_alugueis.index
base_remocao.drop(indexalugueis, inplace=True)
base_final = base_remocao.reset_index(drop=True)

# Listando os bairros não identificados

define_nao_informado = base_remocao['bairro'] == 'Não Informado'
nao_informado = pd.DataFrame(define_nao_informado)
lista_não_informados = nao_informado[nao_informado['bairro'] == True]

# Removendo do dataset as linhas com bairros não identificados e definindo a nova base

indexabairros = lista_não_informados.index
base_remocao.drop(indexabairros, inplace=True)
base_final = base_remocao.reset_index(drop=True)


# Definindo os quartis e limites

valor = base_final['aluguel']

Q1 = valor.quantile(.25)
Q3 = valor.quantile(.75)
IIQ = Q3 - Q1
limite_inferior = Q1 - 1.5 * IIQ
limite_superior = Q3 + 1.5 * IIQ

# Aplicando a definição dos limites para remoção dos outliers e definindo o novo dataset

selecao = (valor >= limite_inferior) & (valor <= limite_superior)
dataset = base_final[selecao].reset_index(drop=True)

# Definindo os Datasets

media_quartos = dataset.groupby(['quartos']).agg({'total_mensal':'mean'}).sort_values(by='total_mensal', ascending=False).reset_index().round()
media_zonas = dataset.groupby(['zona']).agg({'total_mensal':'mean'}).sort_values(by='total_mensal', ascending=False).reset_index().round()
por_quartos = dataset[['zona', 'total_mensal', 'quartos']].reset_index(drop=True)
por_quartos_zona = por_quartos.groupby(['zona', 'quartos']).agg({'total_mensal':'mean'}).reset_index().round()


# CRIANDO OS GRÁFICOS E LISTAS

# Gráfico 1: Média Total Mensal por número de quartos


media_quartos['Cor'] = np.where(media_quartos["quartos"] == 2, 
                                  px.colors.qualitative.Pastel[0], 
                                  px.colors.qualitative.Pastel[1])

grafico_1 = px.bar(media_quartos, x='quartos', y='total_mensal', 
                   labels={
                   'quartos': ' ',
                   'total_mensal': ' '},
                   barmode="group",
                   title = '<b>Média do Total Mensal por Nº de Quartos<b>', 
                   height = int(300),
                   text_auto = True,
                   template='ygridoff')
grafico_1.update_yaxes(showticklabels=False, visible=False)
grafico_1.update_layout(
          font_family='Calibri',
          title_font_family='Calibri',
          title_font_size = 15,
          font_size = 12,
          title_font_color = '#483D8B')
grafico_1.update_xaxes(
          ticktext=['2 Quartos', '3 Quartos'],
          tickvals=[2, 3])
grafico_1.update_traces(marker_color=media_quartos["Cor"])


# Gráfico 2: Média Total Mensal por zona

grafico_2 = px.bar(media_zonas, x='zona', y='total_mensal', 
                   labels={
                   'zona': ' ',
                   'total_mensal': ' '},
                   barmode="group", 
                   title = '<b>Média do Total Mensal por Zona<b>',
                   height = int(300),
                   text_auto = True,
                   color_discrete_sequence = px.colors.qualitative.Pastel,
                   template='ygridoff')
grafico_2.update_yaxes(showticklabels=False, visible=False)
grafico_2.update_xaxes(type='category')
grafico_2.update_layout(
          font_family='Calibri',
          title_font_family='Calibri',
          title_font_size = 15,
          font_size = 12,
          title_font_color = '#483D8B')


# Gráfico 3: Média Total Mensal por zona e número de quartos

grafico_3 = px.histogram(por_quartos_zona, x='zona', y='total_mensal', 
                   color='quartos',
                   histfunc='avg',
                   labels={
                   'zona': ' ',
                   'total_mensal': 'Valor Mensal',
                   'quartos': 'Quartos'},
                   barmode="group", 
                   title = '<b>Média do Total Mensal por Zona e Nº Quartos<b>',
                   height = int(300),
                   text_auto = True,
                   color_discrete_sequence = px.colors.qualitative.Pastel,
                   template='ygridoff')
grafico_3.update_yaxes(showticklabels=False, visible=False)
grafico_3.update_layout(
          font_family='Calibri',
          title_font_family='Calibri',
          title_font_size = 15,
          font_size = 12,
          title_font_color = '#483D8B')


# Definindo as listas de opções

opcoes_quartos = list(dataset['quartos'].unique())
opcoes_zonas = list(dataset['zona'].unique())
opcoes_bairros = list(dataset['bairro'].unique())
opcoes_bairros = list(dataset['endereco'].unique())

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# DEFININDO O LAYOUT DA DASHBOARD


# Cabeçalhos

app.layout =dbc.Container([
                dbc.Row([
                    dbc.Col(
                        html.Div(children=[
                        html.Br(),
                        html.Br(),
                        html.H1('RASTREADOR DE PREÇO MÉDIO DE ALUGUEL + CONDOMÍNIO',
                                style={'textAlign': 'left', 'color': '#191970',
                                       'font-size':'x-large', 'font-family':'Calibri',"font-weight": "bold"}),
                        ]), align='center'
                    ),
                ]),
    
# Gráficos

    dbc.Container([
        dbc.Row([
            
            dbc.Col(
                dcc.Graph(
                    id = 'media_total_quartos',
                    figure = grafico_1,
                ), width=3, align="center",
            ),

            
            
            dbc.Col(
                dcc.Graph(
                    id = 'media_mensal_zona',
                    figure = grafico_2,
                ), width=4, align="center",
            ),
            
            
            
            dbc.Col(
                dcc.Graph(
                    id = 'media_mensal_quartos_zona',
                    figure = grafico_3,
                ), width=5, align="center",
            ),
        ]),
    ]),
    

# Menus de Seleção 
    
    dbc.Container([
        dbc.Row([
            dbc.Col(
    
                
   # Valor Médio Mensal
                
                html.Div([                
                    html.Div([ 
                        html.H4(
                            "Valor Médio Mensal",
                            style={'textAlign': 'center', 'color': '#4682B4', 'font-weight': 'bold',
                                   'font-size':'medium', 'font-family':'Calibri'}),
                        dcc.RangeSlider(
                            id='valor_mensal',
                            min=500,
                            max=7000,
                            value=[500,7000],
                            allowCross=False
                        ),
                        html.Div(id='output_valor_mensal',
                                 style={'textAlign': 'center', 'color': '#DAA520', 'font-size':'medium',
                                        'font-family':'Calibri', 'font-style':'bold'})
                    ]),

                    html.Br(),                
                
                
    # Metragem

                    html.Div([
                        html.H4(
                            "Metragem",
                            style={'textAlign': 'center', 'color': '#4682B4', 'font-weight': 'bold',
                                   'font-size':'medium', 'font-family':'Calibri'}),
                        dcc.RangeSlider(
                            id='metragem',
                            min=10,
                            max=300,
                            value=[10,300],
                            allowCross=False
                        ),
                        html.Div(id='output_metragem',
                                 style={'textAlign': 'center', 'color': '#DAA520', 'font-size':'medium',
                                        'font-family':'Calibri', 'font-style':'bold'})
                    ]),
                    
                    html.Br(),


     #Zona

                    html.Div([
                        html.H5("Zona(s)",
                                style={'textAlign': 'center', 'color': '#4682B4', 'font-weight': 'bold',
                                       'font-size':'medium', 'font-family':'Calibri'}),
                        dcc.Dropdown(opcoes_zonas, id = 'zonas', 
                                     value = ('Centro','Zona Norte'),
                                     multi = True),
                    ]),

                    html.Br(),

                
    # Bairro    
    
                    html.Div([
                        html.H6("Bairro(s)",
                                style={'textAlign': 'center', 'color': '#4682B4', 'font-weight': 'bold',
                                       'font-size':'medium', 'font-family':'Calibri'}),
                        dcc.Dropdown(id = 'bairro',
                                     value = 'Todos',
                                     style={'height': '45%',
                                            'maxHeight': '45%'},
                                     multi = True),
                    ]),
                    ]), width=3, align="center",
            
            ),
            

            
# Gráfico Final
    
            dbc.Col(
                 html.Div([
                     dcc.Graph(
                        id = 'media_aptos',
                        figure = {},
                        style={'border-radius':'15px', 'background-color':'white'},
                        ),
                 ]), width=9,  
            ),
        ], align="left"),
    ]),
    
    html.Br(),
    html.Br(),
    
# Tabela de Imóveis
        
    dbc.Container([
        dbc.Row([
            dbc.Col(
                html.Div(), width=0.5,
            ),
            dbc.Col(
                html.Div([
                    html.H6('APARTAMENTOS',
                            style={'textAlign': 'center', 'color': '#483D8B', 'font-size':'x-large',
                                   "font-weight": "bold", 'font-family':'Calibri', 'margin-left' : '80px'}),
                    dash_table.DataTable(id = 'tabela_aptos',
                                         page_size=10,
                                         page_current=0,
                                         style_table = {"borderRadius": "10px", "overflow": "hidden"},
                                         style_cell_conditional=[
                                             {'if': {'column_id': 'descricao_imovel'},
                                              'textAlign': 'left',
                                              'minWidth': 15,
                                              'maxWidth': 15,
                                              'width': 15,
                                              'fontSize':12, 
                                              'font-family':'calibri',
                                             },
                                             {'if': {'column_id' : 'endereco'},
                                              'minWidth': 10,
                                              'maxWidth': 10,
                                              'width': 10,
                                              'fontSize':12, 
                                              'font-family':'calibri',
                                             },
                                             {'if': {'column_id' : 'bairro'},
                                              'minWidth': 7,
                                              'maxWidth': 7,
                                              'width': 7,
                                              'fontSize':12, 
                                              'font-family':'calibri',
                                             }
                                         ],
                                         style_cell={'minWidth': 4, 'maxWidth': 4, 
                                            'width': 4, 'fontSize':12, 
                                            'font-family':'calibri'},
                                        ),
                ]),
            ),
            dbc.Col(
                html.Div(), width=0.5,
            ),
        ]),
    ]),
    html.Br(),
    html.Br(),
])



# Callbacks e atualização do gráfico com os Menus de Seleção

@app.callback(
    Output('output_valor_mensal', 'children'),
    [Input('valor_mensal', 'value')])

def update_output_valor(value):
    return 'Você selecionou de R$ {} a R$ {}.'.format(value[0], value[1])

@app.callback(
    Output('output_metragem', 'children'),
    [Input('metragem', 'value')])

def update_output_metragem(value):
    return 'Você selecionou {} a {} metros.'.format(value[0], value[1])



@app.callback(
    Output('bairro', 'options'),
    [Input('zonas', 'value'),
     Input('metragem', 'value'),
     Input('valor_mensal','value')])


def update_bairros(zona, metragem, valor_mensal):
    
    # Atualiza o dataset

    dataset_filtrado = dataset[(dataset['zona'].isin(list(zona)))
                               & (dataset['metragem'] >= int(metragem[0]))
                               & (dataset['metragem'] <= int(metragem[1]))
                               & (dataset['total_mensal'] >= int(valor_mensal[0]))
                               & (dataset['total_mensal'] <= int(valor_mensal[1]))]

    opcoes = list(dataset_filtrado['bairro'].unique())
    
    return opcoes



@app.callback(
    [Output('metragem', 'min'),
     Output('metragem', 'max')],
    [Input('zonas', 'value'),
     Input('bairro', 'options'),
     Input('valor_mensal','value')])


def update_metragem(zona, bairro, valor_mensal):
    
    # Atualiza o dataset

    dataset_filtrado = dataset[(dataset['zona'].isin(list(zona)))
                               & (dataset['bairro'].isin(list(bairro)))
                               & (dataset['total_mensal'] >= int(valor_mensal[0]))
                               & (dataset['total_mensal'] <= int(valor_mensal[1]))]
    
    min = min(dataset_filtrado['metragem'])
    max = max(dataset_filtrado['metragem'])
    
    return min, max

                        

@app.callback(
    Output('media_aptos', 'figure'),
    [Input('zonas', 'value'),
     Input('metragem', 'value'),
     Input('bairro', 'value'),
     Input('valor_mensal','value')])

def update_grafico(zona, metragem, bairro, valor_mensal):
    
    dataset = base_final[selecao].reset_index(drop=True)    
    dataset_filtrado = dataset[(dataset['zona'].isin(list(zona)))
                                & (dataset['metragem'] >= int(metragem[0]))
                                & (dataset['metragem'] <= int(metragem[1]))
                                & (dataset['total_mensal'] >= int(valor_mensal[0]))
                                & (dataset['total_mensal'] <= int(valor_mensal[1]))]
        
    dataset_filtrado_end = dataset[(dataset['zona'].isin(list(zona)))
                                & (dataset['metragem'] >= int(metragem[0]))
                                & (dataset['metragem'] <= int(metragem[1]))
                                & (dataset['total_mensal'] >= int(valor_mensal[0]))
                                & (dataset['total_mensal'] <= int(valor_mensal[1]))
                                & (dataset['bairro'].isin(list(bairro)))]
    
    
        
    if (bairro == ('Todos')) or ((len(bairro) == 0) == True):
        
        grafico_final = px.histogram(dataset_filtrado,
                                     x='bairro', y='total_mensal',
                                     labels={'bairro': ' ',
                                             'quartos': 'Nº de Quartos'},
                                     color='quartos',
                                     barmode="group", 
                                     histfunc='avg',
                                     height = int(450),
                                     title = '<b>Valor Médio de Aluguel e Condomínio<b>',
                                     text_auto = True,
                                     color_discrete_sequence = [px.colors.qualitative.Pastel[0], 
                                                                px.colors.qualitative.Pastel[1]],
                                     category_orders={"quartos": [2,3]},
                                     template='ygridoff')
        grafico_final.update_yaxes(showticklabels=False, visible=False)
        grafico_final.update_layout(font_family='Calibri', title_font_family='Calibri',
                                    title_font_size = 20,font_size = 12, title_font_color = '#483D8B')
        grafico_final.update_layout(margin=dict(b=120))
        
    else:
        
        grafico_final = px.histogram(dataset_filtrado_end,
                                     x='endereco', y='total_mensal',
                                     labels={'endereco': ' ',
                                             'quartos': 'Nº de Quartos'},
                                     color='quartos',
                                     barmode="group", 
                                     histfunc='avg',
                                     height = int(450),
                                     title = '<b>Valor Médio de Aluguel e Condomínio<b>',
                                     text_auto = True,
                                     color_discrete_sequence = [px.colors.qualitative.Pastel[0], 
                                                                px.colors.qualitative.Pastel[1]],
                                     category_orders={"quartos": [2,3]},
                                     template='ygridoff')
        grafico_final.update_yaxes(showticklabels=False, visible=False)
        grafico_final.update_layout(font_family='Calibri', title_font_family='Calibri',
                                    title_font_size = 20,font_size = 12, title_font_color = '#483D8B')
        grafico_final.update_layout(margin=dict(b=120))
        
    return grafico_final



@app.callback(
    [Output('tabela_aptos', 'data'),
     Output('tabela_aptos', 'columns')],
    [Input('zonas', 'value'),
     Input('metragem', 'value'),
     Input('bairro', 'value'),
     Input('valor_mensal','value')])

def update_tabela(zona, metragem, bairro, valor_mensal):
    
    dataset = base_final[selecao].reset_index(drop=True)    
    dataset_filtrado = dataset[(dataset['zona'].isin(list(zona)))
                                & (dataset['metragem'] >= int(metragem[0]))
                                & (dataset['metragem'] <= int(metragem[1]))
                                & (dataset['total_mensal'] >= int(valor_mensal[0]))
                                & (dataset['total_mensal'] <= int(valor_mensal[1]))]
        
    dataset_filtrado_end = dataset[(dataset['zona'].isin(list(zona)))
                                & (dataset['metragem'] >= int(metragem[0]))
                                & (dataset['metragem'] <= int(metragem[1]))
                                & (dataset['total_mensal'] >= int(valor_mensal[0]))
                                & (dataset['total_mensal'] <= int(valor_mensal[1]))
                                & (dataset['bairro'].isin(list(bairro)))]    
    
        
    if (bairro == ('Todos')) or ((len(bairro) == 0) == True):

        data = dataset_filtrado.to_dict('records')
        
        columns = [{"name": i, "id": i, "deletable": True,
                    "selectable": True, "hideable": True}
                   if i == "iptu" or i == "cidade" or i == "zona" or i == "garagem"
                   else {"name": i, "id": i, "deletable": True, "selectable": True}
                   for i in dataset_filtrado.columns]
        
    else:
        
        data = dataset_filtrado_end.to_dict('records')
        
        columns = [{"name": i, "id": i, "deletable": True,
                    "selectable": True, "hideable": True}
                   if i == "iptu" or i == "cidade" or i == "zona" or i == "garagem"
                   else {"name": i, "id": i, "deletable": True, "selectable": True}
                   for i in dataset_filtrado_end.columns]
        
                
    return data, columns



if __name__ == '__main__':
    app.run_server(debug=False)


# In[ ]:





# In[ ]:




