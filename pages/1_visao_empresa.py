# Librasies 
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go

# importando biblioteca
import pandas as pd
import streamlit as st
from PIL import Image
import folium
from streamlit_folium import folium_static

st.set_page_config( page_title='Visão Empresa', page_icon='📈', layout='wide' )

# --------------------------------------------------#
# Funções 
# --------------------------------------------------#

# Função country_maps
def country_maps( df1 ):
    
    """
    A função country_maps(df1) recebe um objeto DataFrame chamado df1 como parâmetro. O código da função faz o seguinte:

    Cria um novo objeto DataFrame chamado df_aux, que contém as colunas 'City', 'Road_traffic_density', 'Delivery_location_latitude' e 'Delivery_location_longitude' do objeto df1.
    Os dados de df_aux são agrupados por 'City' e 'Road_traffic_density', e calcula-se a mediana das outras colunas.
    Cria um objeto Map do Folium.
    Itera sobre cada linha do objeto df_aux, criando um marcador no mapa Folium para cada ponto de entrega.
    O popup do marcador contém as informações de 'City' e 'Road_traffic_density' para cada ponto de entrega.
    Exibe o mapa usando folium_static.
    Retorna None.

    """
    
    df_aux = ( df1.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']]
              .groupby( ['City', 'Road_traffic_density'] )
              .median()
              .reset_index() )


    map = folium.Map()

    for index, location_info in df_aux.iterrows():
        folium.Marker( [location_info['Delivery_location_latitude'],
                          location_info['Delivery_location_longitude']],
                        popup=location_info[['City', 'Road_traffic_density']] ).add_to( map)

    folium_static(map, width=1024 , height=600 )     
    return None 
#--------------------------------------------------------------#
# Função order_share_by_week

def order_share_by_week( df1 ) :    
# Quantidade de pedidos / numero unico de entregadores 
    df_aux01 = df1.loc[:, ['ID', 'week_of_year']].groupby( 'week_of_year' ).count().reset_index()
    df_aux02 = df1.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby( 'week_of_year' ).nunique().reset_index()
    df_aux = pd.merge( df_aux01, df_aux02, how='inner', on='week_of_year')
    df_aux['order_by_deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']          
    fig = px.line(df_aux, x='week_of_year', y='order_by_deliver')

    return fig 
    """
    A função order_share_by_week(df1) recebe um objeto DataFrame chamado df1 como parâmetro. O código da função faz o seguinte:

    Cria um objeto df_aux01, que contém as colunas 'ID' e 'week_of_year' do objeto df1. Os dados de df_aux01 são agrupados por 'week_of_year',
    contando o número de pedidos feitos em cada semana.
    Cria um objeto df_aux02, que contém as colunas 'Delivery_person_ID' e 'week_of_year' do objeto df1.
    Os dados de df_aux02 são agrupados por 'week_of_year', contando o número de entregadores únicos em cada semana.
    Cria um objeto df_aux que combina as informações de df_aux01 e df_aux02, fazendo um merge interno dos dados em relação à coluna 'week_of_year'.
    Cria uma nova coluna em df_aux chamada 'order_by_deliver', que divide a quantidade de pedidos pelo número de entregadores únicos em cada semana.
    Cria um objeto fig usando a biblioteca Plotly Express.
    O gráfico de linha plotado mostra a evolução da relação entre a quantidade de pedidos e o número de entregadores em cada semana.
    Ao final, a função retorna o objeto fig.
    
    """
    
#---------------------------------------------------------------------------------------------------------------#

# Função order_by_week
def order_by_week( df1 ):
    # criando coluna de semana 
    df1['week_of_year'] = df1['Order_Date'].dt.strftime( '%U' )
    teste = df1.loc[:, ['ID', 'week_of_year']].groupby( 'week_of_year' ).count().reset_index()
    fig = px.line( teste, x='week_of_year', y='ID' )
    return fig

    """
    A função order_by_week(df1) recebe um objeto DataFrame chamado df1 como parâmetro. O código da função faz o seguinte:

    Cria uma nova coluna em df1 chamada 'week_of_year', que contém o número da semana do ano correspondente à data do pedido.
    Cria um objeto teste, que contém as colunas 'ID' e 'week_of_year' do objeto df1.
    Os dados de teste são agrupados por 'week_of_year', contando o número de pedidos feitos em cada semana.
    Cria um objeto fig usando a biblioteca Plotly Express.
    O gráfico de linha plotado mostra a evolução da quantidade de pedidos em cada semana.
    Ao final, a função retorna o objeto fig.
    """

#----------------------------------------------------------------------------------------------------------------#

# Função traffic_order_city
def traffic_order_city( df1 ):
            
    test = ( df1.loc[:, ['ID', 'City', 'Road_traffic_density']]
                .groupby( ['City', 'Road_traffic_density'] )
                .count()
                .reset_index() )
    fig = px.scatter( test, x='City', y='Road_traffic_density', size='ID', color='City')

    return fig


    """
    A função traffic_order_city(df1) recebe um objeto DataFrame chamado df1 como parâmetro. O código da função faz o seguinte:

    Cria um objeto test que contém as colunas 'ID', 'City' e 'Road_traffic_density' do objeto df1.
    Os dados de test são agrupados por 'City' e 'Road_traffic_density', contando o número de pedidos feitos em cada combinação de cidade e densidade de tráfego.
    Cria um objeto fig usando a biblioteca Plotly Express.
    O gráfico de dispersão plotado mostra as combinações de cidades e densidades de tráfego,
    com o tamanho de cada ponto representando o número de pedidos em cada combinação e a cor representando a cidade.
    Ao final, a função retorna o objeto fig.
    """
#----------------------------------------------------------------------------------------------------------------#

# Função traffic_order_share
def traffic_order_share( df1 ):
            
    df_aux = df1.loc[:, ['ID', 'Road_traffic_density']].groupby( 'Road_traffic_density' ).count().reset_index() 

    df_aux['entregas_perc'] = df_aux['ID'] / df_aux['ID'].sum()

    px.pie( df_aux, values='entregas_perc', names='Road_traffic_density' )

    fig = px.pie( df_aux, values='entregas_perc', names='Road_traffic_density' )

    return fig



    """
    A função traffic_order_share(df1) recebe um objeto DataFrame chamado df1 como parâmetro. O código da função faz o seguinte:

    Cria um objeto df_aux que contém as colunas 'ID' e 'Road_traffic_density' do objeto df1. Os dados de df_aux são agrupados por 'Road_traffic_density',
    contando o número de pedidos feitos em cada densidade de tráfego.
    Calcula a porcentagem de entregas em cada densidade de tráfego e adiciona essa informação como uma nova coluna chamada 'entregas_perc' no objeto df_aux.
    Cria um gráfico de pizza (pie chart) usando a biblioteca Plotly Express.
    O gráfico mostra a proporção de entregas em cada densidade de tráfego.
    Ao final, a função retorna o objeto fig.
    """
#----------------------------------------------------------------------------------------------------------------#

# Função order_metric
def order_metric( df1 ):
                        
    coluna = ['ID', 'Order_Date']

    #seleção de linhas 
    df_aux = df1.loc[:, coluna].groupby( ['Order_Date'] ).count().reset_index()

    # Desenhar Grafico 
    fig = px.bar( df_aux, x='Order_Date', y='ID')

    return fig

    """
    A função recebe um objeto DataFrame chamado df1 como parâmetro. O código da função faz o seguinte:

    Cria uma lista chamada coluna com as colunas 'ID' e 'Order_Date'.
    Cria um objeto df_aux que contém as colunas especificadas em coluna do objeto df1.
    Os dados de df_aux são agrupados por 'Order_Date', contando o número de pedidos feitos em cada data.
    Cria um gráfico de barras (bar chart) usando a biblioteca Plotly Express.
    O gráfico mostra a quantidade de pedidos feitos em cada data.
    Ao final, a função retorna o objeto fig.
    """
    
#----------------------------------------------------------------------------------------------------------------#

# Função clean_code
def clean_code( df1 ):
    """ Esta função tem a responsabilidade de limpar o dataframe
        
        Tipos de limpeza:
        1. Remoção dos dados NaN
        2. Mudança do tipo da coluna 
        3. Remoção dos espaços das variáveis de texto
        4. Formatação da coluna de datas 
        5. Limpeza da coluna de tempo ( remoção do texto da variável númerica )
        
        Input: Dataframe
        Output: Dataframe
    
    
    """
    
    ## Limpeza dos dados 
    # 1. convertendo a coluna Age do texto para numero 
    linha_selecionada = (df1['Delivery_person_Age' ] != 'NaN ')
    df1 = df1.loc[linha_selecionada, :].copy()

    linha_selecionada = (df1['Road_traffic_density' ] != 'NaN ')
    df1 = df1.loc[linha_selecionada, :].copy()

    linha_selecionada = (df1['City' ] != 'NaN ')
    df1 = df1.loc[linha_selecionada, :].copy()

    linha_selecionada = (df1['Festival' ] != 'NaN ')
    df1 = df1.loc[linha_selecionada, :].copy()

    df1[ 'Delivery_person_Age'] = df1[ 'Delivery_person_Age' ].astype( int )

    # 2. convertendo a coluna Ratings de texto para numero decimal ( float )
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype( float )

    # 3. convertendo a coluna order_date de texto para data
    df1['Order_Date'] = pd.to_datetime( df1['Order_Date' ], format='%d-%m-%Y' )

    # 4. convertendo multiple_deliveries de texto para numero inteiro ( int )
    linha_selecionada = (df1['multiple_deliveries'] != 'NaN ')
    df1 = df1.loc[linha_selecionada, :].copy()
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype( int )

    # 5. Removendo os espaços dentro de strings/testos/object
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()

    # 6. Limpando a coluna de Time taken(min)
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply( lambda x: x.split( '(min)')[1] )
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype( int )

    return df1


#-------------------------- Inicio da Estrutura lógica do código------------------------
#---------------------------------------------------------------------------------------
# importando dataset
df = pd.read_csv( 'dataset/train.csv' )

df1 = clean_code( df )


    
# Visão - Empresa 
# ==========================================================================
# Barra Lateral 
# ==========================================================================
st.header( 'Marketplace - Visão Cliente' )

#image_path = '/Users/eliom/Documents/repos/ftc_ds/cury.jpg'
image = Image.open( 'cury.jpg' )
st.sidebar.image( image, width=120 )

st.sidebar.markdown( '# Cury Company' )
st.sidebar.markdown( '## Fastest Delivery in Town' )
st.sidebar.markdown( """___""" )

st.sidebar.markdown( '## Selecione uma data limite ' )

import datetime

date_value = pd.Timestamp(2022, 4, 13)
date_timestamp = int(date_value.timestamp())

date_datetime = datetime.datetime.fromtimestamp(date_timestamp)

date_slider = st.sidebar.slider(
    "Até qual valor?",
    value=date_datetime,
    min_value=datetime.datetime(2022, 2, 11),
    max_value=datetime.datetime(2022, 4, 6),
    format='YYYY-MM-DD'
)

st.sidebar.markdown( """___""" )


traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito',
    ['Low', 'Medium', 'High', 'Jam'],
    default=['Low', 'Medium', 'High', 'Jam'] )

st.sidebar.markdown( """___""" )
st.sidebar.markdown( '### Powered by Comunidade DS' )

# Filtro de Data 
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de Transito 
linhas_selecionadas = df1['Road_traffic_density'].isin( traffic_options )
df1 = df1.loc[linhas_selecionadas, :]
# ==========================================================================
# Layout no Streamlit
# ==========================================================================
tab1, tab2, tab3 = st.tabs( ['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'] )

with tab1:
    with st.container():
        # Order Matric
        fig = order_metric( df1 )
        st.markdown( '# Orders By Day' )
        st.plotly_chart(fig, use_container_width=True )
        
        
        
    with st.container():
        col1, col2 = st.columns( 2 )
        
        with col1:
            fig = traffic_order_share( df1 )
            st.header( "Traffic Order Share" )
            st.plotly_chart(fig, use_container_width=True )
            
            
        with col2:
            st.header( "Traffic Order City" )
            fig = traffic_order_city( df1 )
            st.plotly_chart( fig, use_container=True )

            
            
with tab2:
    with st.container():
        st.markdown("# Order By Week" )
        fig = order_by_week( df1 )
        st.plotly_chart(fig, use_container_width=True )
        
    with st.container():
        st.markdown("# Order Share by Week" )
        fig = order_share_by_week( df1 )
        st.plotly_chart(fig, use_container_width=True )
    

with tab3:
    st.markdown( "# Country Maps" )
    country_maps( df1 )
    
    

