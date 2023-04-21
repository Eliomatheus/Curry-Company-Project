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

st.set_page_config( page_title='Visão Entregadores', page_icon='🚚', layout='wide' )

# --------------------------------------------------#
# Funções 
# --------------------------------------------------#

# Função top_delivers
def top_delivers( df1, top_asc ):
    df2 = ( df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']]
               .groupby( ['City', 'Delivery_person_ID'])
               .mean()
               .sort_values( ['City', 'Time_taken(min)'], ascending=top_asc)
               .reset_index() )

    df_aux01 = df2.loc[df2[ 'City'] == 'Metropolitian', :].head(10)
    df_aux02 = df2.loc[df2[ 'City'] == 'Urban', :].head(10)
    df_aux03 = df2.loc[df2[ 'City'] == 'Semi-Urban', :].head(10)

    df3 = pd.concat( [df_aux01, df_aux02, df_aux03] ).reset_index( drop=True)

    return df3 

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

# Clean dataset
df1 = clean_code( df )


# Visão - Empresa 
# ==========================================================================
# Barra Lateral 
# ==========================================================================
st.header( 'Marketplace - Visão Entregadores' )

#image_path = '/Users/eliom/Documents/repos/ftc_ds/cury.jpg'
image = Image.open( 'cury.jpg' )
st.sidebar.image( image, width=120 )

st.sidebar.markdown( '# Cury Company' )
st.sidebar.markdown( '## Fastest Delivery in Town' )
st.sidebar.markdown( """___""" )

st.sidebar.markdown( '## Selecione uma data limite ' )
date_slider = st.sidebar.slider(
    'Até qual valor?',
    value=pd.datetime( 2022, 4, 13 ),
    min_value=pd.datetime( 2022, 2, 11 ),
    max_value=pd.datetime( 2022, 4, 6 ),
    format='DD-MM-YYYY' )


st.sidebar.markdown( """___""" )


traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito',
    ['Low', 'Medium', 'High', 'Jam'],
    default=['Low', 'Medium', 'High', 'Jam'] )

st.sidebar.markdown( """___""" )


Weatherconditions = st.sidebar.multiselect(
    'Quais as condições Climaticas',
    ['conditions Cloudy', 'conditions Fog', 'conditions Sandstorms', 'conditions Stormy', 'conditions Sunny', 'conditions Windy'],
    default=['conditions Cloudy', 'conditions Fog', 'conditions Sandstorms', 'conditions Stormy', 'conditions Sunny', 'conditions Windy'] )

st.sidebar.markdown( """___""" )
st.sidebar.markdown( '### Powered by Comunidade DS' )

# Filtro de Data 
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de Transito 
linhas_selecionadas = df1['Road_traffic_density'].isin( traffic_options )
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de Clima
linhas_selecionadas = df1['Weatherconditions'].isin( Weatherconditions )
df1 = df1.loc[linhas_selecionadas, :]

# ==========================================================================
# Layout no Streamlit
# ==========================================================================

tab= st.tabs( ['Visão Gerencial'] )

with st.container():
    st.title( ' Overall Metrics' )
    col1, col2, col3, col4 = st.columns( 4, gap='large' )
    with col1:
        # A Maior idade dos entregadores 
        maior_idade = df1.loc[:, 'Delivery_person_Age'].max() 
        col1.metric( 'Maior idade', maior_idade )

    with col2: 
        # A menor idade dos entregadores 
        menor_idade = df1.loc[:, 'Delivery_person_Age'].min() 
        col2.metric( 'Menor idade', menor_idade )
            
    with col3:
        # A pior e a melhor condição de veículos.
        melhor_condicao = df1.loc[:, 'Vehicle_condition'].max()
        col3.metric( 'Melhor condição', melhor_condicao )

            
    with col4:
        pior_condicao = df1.loc[:, 'Vehicle_condition'].min() 
        col4.metric( 'Pior condição', pior_condicao )
            
with st.container():
        
    st.markdown( """___""" )
    st.title( 'Avaliacoes' )
        
    col1, col2 = st.columns( 2 )
    with col1:
        st.markdown( '##### Avaliacao medias por entregador' )
        media_por_entregador = ( df1.loc[:, ['Delivery_person_ID', 'Delivery_person_Ratings']]
                                    .groupby( 'Delivery_person_ID')
                                    .mean()
                                    .reset_index() )
        st.dataframe( media_por_entregador,  use_container_width=True )
            
    with col2:
        st.markdown( '##### Avaliacao media por transito' )
        df_avg_rating_by_traffic = ( df1.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']]
                                        .groupby( 'Road_traffic_density' )
                                        .agg( {'Delivery_person_Ratings' : ['mean', 'std'] } ) )

        #mudança de nomes das colunas 
        df_avg_rating_by_traffic.columns = ['delivery_mean', 'delivery_std' ]

        #reset do index
        df_avg_rating_by_traffic.reset_index()
        st.dataframe( df_avg_rating_by_traffic,  use_container_width=True )
            
            
        st.markdown( '##### Avaliacao media por clima' )
        df_avg_rating_by_weather = ( df1.loc[:, ['Delivery_person_Ratings', 'Weatherconditions']]
                                        .groupby( 'Weatherconditions' )
                                        .agg( {'Delivery_person_Ratings' : ['mean', 'std'] } ) )

        #mudança de nomes das colunas 
        df_avg_rating_by_weather.columns = ['delivery_mean', 'delivery_std' ]

        #reset do index
        df_avg_rating_by_weather = df_avg_rating_by_weather.reset_index()
        st.dataframe( df_avg_rating_by_weather,  use_container_width=True )
            
            
with st.container():
    st.markdown( """___""" )
    st.title( 'Velocidade de Entrega' )
            
    col1, col2 = st.columns( 2 )
        
    with col1:
        st.markdown( '##### Top Entregadores mais rapidos' )
        df3 = top_delivers( df1, top_asc=True )
        st.dataframe( df3,  use_container_width=True ) 
                
    with col2:
        st.markdown( '##### Top Entregadores mais lentos' )
        df3 = top_delivers( df1, top_asc=False )
        st.dataframe( df3,  use_container_width=True )
                    