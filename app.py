import pandas as pd
import plotly.express as px
import streamlit as st

## Gerando títulos
st.set_page_config(page_title="Análise Exploratória", layout="wide")
st.title("Anúncios para vendas de carros")

## Função para carregar os dados
#
@st.cache_data
def load_data(url):
    """ Carrega o dataframe em cache e realiza alguns tratamentos nas colunas
    """
    ## Carregando dados
    #
    df_vehicles = pd.read_csv(url, dtype='str')

    ## Tratando colunas
    #
    df_vehicles['model_year'] = df_vehicles['model_year'].fillna('unknown').str.replace('.0','')
    df_vehicles['cylinders'] = df_vehicles['cylinders'].fillna('unknown')
    df_vehicles['paint_color'] = df_vehicles['paint_color'].fillna('unknown')
    df_vehicles['price'] = df_vehicles['price'].astype('float')
    df_vehicles['odometer'] = df_vehicles['odometer'].astype('float')
    df_vehicles['is_4wd'] = df_vehicles['is_4wd'].fillna(0).astype('bool')
    df_vehicles['days_listed'] = df_vehicles['days_listed'].fillna(0).astype('int')
    df_vehicles['date_posted'] = pd.to_datetime(df_vehicles['date_posted'],format='%Y-%m-%d')
    

    return df_vehicles

## Inicia os dados
#
dados = load_data('./assets/vehicles.csv')

## Gerando um sidebar na página
#
with st.sidebar:
    st.header("Escolha os tipos de gráficos:")

    # Checkbox
    graficos = {
        'histogram': st.checkbox('Histogram', value=True),
        'scatter': st.checkbox('Scatter', value=True),                                               
    }

    # Button
    hist_button = st.button('Gerar Gráficos')


## Verificando se existe um checkbox ativo
#
if graficos['histogram'] or graficos['scatter']:
                
    ## Verifica se o botão foi clicado
    #
    if hist_button: 
        
        
        ## Verifica se o histogram foi selecionado
        #
        if graficos['histogram']:
            st.write('Histograma da distância percorrida por um veículo.')
            fig = px.histogram(dados, x="odometer")
            st.plotly_chart(fig, use_container_width=True)

        ## Verifica se o scatter foi selecionado
        # 
        if graficos['scatter']:
            st.write('Disperção da distância percorrida x Preço.')
            fig2 = px.scatter(dados, x="odometer", y="price")
            st.plotly_chart(fig2, use_container_width=True)

        ## Exibe uma tabela com os dados de origem
        st.write('Tabela de dados:')
        st.write(dados)

else:
    st.error("Erro. Seleciono ao menos um tipo de gráfico.")