# DATA APP — PREVISÃO DE HOMICÍDIOS MUNDIAIS (UNODC)
# Tópicos Especiais em Computação I
#
# Este Data App permite visualizar os dados históricos de
# homicídios por país e prever os valores para 2023–2026
# usando Regressão Linear.
#
# Fonte dos dados: UNODC
# https://dataunodc.un.org/dp-intentional-homicide-victims
#
# Para instalar as dependências:
# pip install streamlit pandas numpy scikit-learn plotly openpyxl
#
# Para rodar:
# streamlit run dataapp.py
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, max_error

st.set_page_config(
    page_title='Homicídios Mundiais — Previsão',
    page_icon='🌍',
    layout='wide'
)

# CARREGAMENTO DOS DADOS

@st.cache_data
def carregar_dados():
    df = pd.read_excel('data_cts_intentional_homicide.xlsx', sheet_name=0)

    df_total = df[
        (df['Indicator']            == 'Victims of intentional homicide') &
        (df['Dimension']            == 'Total') &
        (df['Category']             == 'Total') &
        (df['Unit of measurement']  == 'Counts') &
        (df['Age']                  == 'Total') &
        (df['Sex']                  == 'Total')
    ].copy().reset_index(drop=True)

    return df_total


@st.cache_resource
def treinar_modelo(pais, df):
    dados = df[df['Country'] == pais][['Year', 'VALUE']].sort_values('Year').dropna()

    if len(dados) < 5:
        return None

    X = dados[['Year']].values
    y = dados['VALUE'].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=0
    )

    modelo = LinearRegression()
    modelo.fit(X_train, y_train)
    previsoes_test = modelo.predict(X_test)

    metricas = {
        'R²':          round(modelo.score(X, y), 4),
        'MAE':         round(mean_absolute_error(y_test, previsoes_test), 2),
        'RMSE':        round(mean_squared_error(y_test, previsoes_test) ** 0.5, 2),
        'Erro Máximo': round(max_error(y_test, previsoes_test), 2),
    }

    anos_futuros = np.array([[2023], [2024], [2025], [2026]])
    valores_futuros = modelo.predict(anos_futuros)
    previsoes = {
        ano: max(0, round(val))
        for ano, val in zip([2023, 2024, 2025, 2026], valores_futuros)
    }

    return {
        'modelo':    modelo,
        'dados':     dados,
        'metricas':  metricas,
        'previsoes': previsoes,
    }

# CARREGANDO OS DADOS

df_total = carregar_dados()

# Lista de países com dados suficientes (>= 5 anos)
contagem = df_total.groupby('Country')['Year'].count()
paises_validos = sorted(contagem[contagem >= 5].index.tolist())

st.title('🌍 Homicídios Mundiais — Análise e Previsão')
st.write(
    'Visualize os dados históricos de homicídios por país (2013–2022) '
    'e acompanhe a previsão para **2023–2026** gerada por Regressão Linear.'
)
st.write('**Fonte:** Escritório das Nações Unidas sobre Drogas e Crime (UNODC)')
st.divider()

# SELEÇÃO DO PAÍS
st.sidebar.header('⚙️ Configurações')
st.sidebar.write('Selecione um país para analisar:')

pais_selecionado = st.sidebar.selectbox(
    'País',
    options=paises_validos,
    index=paises_validos.index('Brazil') if 'Brazil' in paises_validos else 0
)

st.sidebar.divider()
st.sidebar.write('**Comparativo entre países:**')
paises_comparar = st.sidebar.multiselect(
    'Selecione até 5 países',
    options=paises_validos,
    default=['Brazil', 'Mexico', 'India', 'South Africa', 'Colombia'],
    max_selections=5
)

# REGRESSÃO DO PAÍS SELECIONADO
resultado = treinar_modelo(pais_selecionado, df_total)

if resultado is None:
    st.warning(f'Dados insuficientes para {pais_selecionado}.')
    st.stop()

dados       = resultado['dados']
metricas    = resultado['metricas']
previsoes   = resultado['previsoes']
modelo      = resultado['modelo']

# MÉTRICAS PRINCIPAIS
st.subheader(f'📊 {pais_selecionado} — Resultado do Modelo')

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric('R²', f"{metricas['R²']:.4f}")
with col2:
    st.metric('MAE', f"{metricas['MAE']:,.0f}")
with col3:
    st.metric('RMSE', f"{metricas['RMSE']:,.0f}")
with col4:
    st.metric('Erro Máximo', f"{metricas['Erro Máximo']:,.0f}")

# GRÁFICO PRINCIPAL
st.subheader('📈 Dados Históricos e Previsão (2023–2026)')

anos_hist  = dados['Year'].tolist()
vals_hist  = dados['VALUE'].tolist()
y_regressao = modelo.predict(dados[['Year']].values).tolist()

anos_prev  = list(previsoes.keys())
vals_prev  = list(previsoes.values())

fig = go.Figure()

# Dados reais
fig.add_trace(go.Scatter(
    x=anos_hist, y=vals_hist,
    mode='lines+markers',
    name='Dados reais (2013–2022)',
    line=dict(color='steelblue', width=2),
    marker=dict(size=8)
))

# Linha de regressão
fig.add_trace(go.Scatter(
    x=anos_hist, y=y_regressao,
    mode='lines',
    name='Linha de regressão',
    line=dict(color='gray', dash='dash', width=1.5)
))

# Previsão
fig.add_trace(go.Scatter(
    x=anos_prev, y=vals_prev,
    mode='lines+markers+text',
    name='Previsão (2023–2026)',
    line=dict(color='red', dash='dash', width=2),
    marker=dict(size=10, symbol='square'),
    text=[f'{v:,}' for v in vals_prev],
    textposition='top center'
))

# Linha separando histórico da previsão
fig.add_vline(x=2022.5, line_dash='dot', line_color='black', opacity=0.5)

fig.update_layout(
    xaxis_title='Ano',
    yaxis_title='Número de Homicídios',
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
    height=450
)

st.plotly_chart(fig, use_container_width=True)

# TABELA DE PREVISÕES
col_a, col_b = st.columns(2)

with col_a:
    st.subheader('📋 Previsões Numéricas')
    df_prev = pd.DataFrame({
        'Ano': list(previsoes.keys()),
        'Homicídios Previstos': list(previsoes.values())
    })
    st.dataframe(df_prev, use_container_width=True, hide_index=True)

with col_b:
    st.subheader('📋 Dados Históricos')
    df_hist = dados.copy()
    df_hist.columns = ['Ano', 'Homicídios']
    df_hist['Homicídios'] = df_hist['Homicídios'].astype(int)
    st.dataframe(df_hist.reset_index(drop=True), use_container_width=True, hide_index=True)

st.divider()

# COMPARATIVO ENTRE PAÍSES
st.subheader('🔀 Comparativo entre Países — Previsão 2023–2026')

if paises_comparar:
    tabela_comp = []

    for pais in paises_comparar:
        res = treinar_modelo(pais, df_total)
        if res:
            linha = {'País': pais, 'R²': res['metricas']['R²']}
            linha.update(res['previsoes'])
            tabela_comp.append(linha)

    df_comp = pd.DataFrame(tabela_comp)

    # Gráfico de linhas comparativo
    fig_comp = go.Figure()

    for _, row in df_comp.iterrows():
        fig_comp.add_trace(go.Scatter(
            x=[2023, 2024, 2025, 2026],
            y=[row[2023], row[2024], row[2025], row[2026]],
            mode='lines+markers',
            name=row['País']
        ))

    fig_comp.update_layout(
        xaxis_title='Ano',
        yaxis_title='Homicídios Previstos',
        height=400
    )

    st.plotly_chart(fig_comp, use_container_width=True)

    # Tabela comparativa
    df_comp[[2023, 2024, 2025, 2026]] = df_comp[[2023, 2024, 2025, 2026]].astype(int)
    st.dataframe(df_comp, use_container_width=True, hide_index=True)

else:
    st.info('Selecione ao menos um país na barra lateral para ver o comparativo.')
