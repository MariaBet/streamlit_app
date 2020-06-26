# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from os import system


st.markdown(" ## ** Viveiro Florestal em Unidades de Conservação ** ")
st.image("image1.png", width=700)

if st.checkbox("Saber Mais"):
    st.markdown(''' ### O que é uma unidade de conservação?
    É uma área de proteção ambiental. As unidades de conservação
    (UCs) são legalmente instituídas pelo poder público, nas suas três
    esferas (municipal, estadual e federal). Elas são reguladas pela
    Lei no. 9.985, de 2000, que institui
    o Sistema Nacional de Unidades de Conservação (SNUC)''')

st.markdown(" ### ** Ánalise de Dados sobre a produção de mudas florestais ** ")

def main():

    name_file = 'viveiro.csv'
    df = pd.read_csv(name_file, sep=';')
    if st.checkbox("Deseja saber as quais mudas são desenvolvidas neste espaço? Clique "):
        st.dataframe(df.especie)


    add_selectbox = st.sidebar.selectbox(
    "Selecione sua ánalise",
    ("Índice", "Visualização do Arquivo CSV", "Número de linhas",
    "Número de colunas", "Contagem de dados em branco", "Descrever CSV" )
    )

    if add_selectbox == "Visualização do Arquivo CSV":
        st.markdown('### **Ánalise dos Dados presentes no Dataset  ** ')
        slider = st.slider('Selecione o número de linhas', 1, 50)
        st.dataframe(df.head(slider))


    if add_selectbox == "Número de linhas":
        st.markdown(' ### ** Informação presente no Dataset sobre o número de Linhas **')
        st.markdown(df.shape[0])

    if add_selectbox == 'Número de colunas':
        st.markdown(' ### ** Informação presente no Dataset sobre o número de Colunas **')
        st.markdown(df.shape[1])

    if add_selectbox == "Contagem de dados em branco":
        st.markdown(' ### ** Informação presente no Dataset sobre dados Nulos **')
        st.dataframe(df.isna().sum())

    if add_selectbox == "Descrever CSV":
        st.markdown('### **Ánalise descritiva dos Dados presentes no Dataset  ** ')
        st.dataframe(df.describe())

    aux = pd.DataFrame({"colunas": df.columns, 'tipos': df.dtypes})
    colunas_numericas = list(aux[aux['tipos'] != 'object']['colunas'])
    colunas_object = list(aux[aux['tipos'] == 'object']['colunas'])
    colunas = list(df.columns)

    add_selectbox2 = st.sidebar.selectbox(
    "Selecione a estatítica descritiva",
    ("Índice", "Média", "Mediana",
    "Desvio Padrão")
    )

    if add_selectbox2 == "Média":
        col = st.selectbox('Selecione a coluna :', colunas_numericas)
        st.text('Média')
        st.markdown(df[col].mean())

    if add_selectbox2 == "Mediana":
        col = st.selectbox('Selecione a coluna :', colunas_numericas)
        st.text('Mediana')
        st.markdown(df[col].median())

    if add_selectbox2 == "Desvio Padrão":
        col = st.selectbox('Selecione a coluna :', colunas_numericas)
        st.markdown(df[col].std())

    add_selectbox3 = st.sidebar.selectbox(
        " Produção do viveiro",
        ("Índice" , "Espécie mais cultivada", "Porcentagem de Germinação",
        "Mudas Produzidas")
        )

    if add_selectbox3 == "Espécie mais cultivada":
        st.markdown(' ### Espécie de árvore ')
        st.dataframe(df.groupby('especie')['germinacao'].median().reset_index().sort_values('germinacao', ascending = False))


    if add_selectbox3 == "Porcentagem de Germinação":
        st.dataframe(df['germinacao']*100/df['semeadura'])

    if add_selectbox3 == "Mudas Produzidas":
        st.markdown(' ### Mudas disponíveis ')
        st.dataframe(df['mudas_prontas'])
        st.markdown(' ### Quantidade disponível ')
        st.dataframe(df['producao'])

    # graficos

    add_selectbox4 = st.sidebar.selectbox(
        " Gráficos",
        ("Índice" , "Gráfico de Barras", "Gráfico de Linhas",
        "Histograma", "Correlação")
        )
    # st.bar_chart(df['especies'],df['germinacao'])

    def criar_barras(coluna_num, coluna_cat, df):
        bars = alt.Chart(df, width = 700).mark_bar().encode(
        x=alt.X(coluna_num, stack='zero'),
        y=alt.Y(coluna_cat),
        tooltip=[coluna_cat, coluna_num]
        ).interactive()
        return bars


    if add_selectbox4 == "Gráfico de Barras":
        col_num_barras = st.selectbox('Selecione a coluna numerica: ', colunas_numericas, key = 'unique')
        col_cat_barras = st.selectbox('Selecione uma coluna categorica : ', colunas_object, key = 'unique')
        st.markdown(' Gráfico de barras da ' + str(col_cat_barras) + ' e a ' + col_num_barras)
        st.write(criar_barras(col_num_barras, col_cat_barras, df))

    if add_selectbox4 == "Gráfico de Linhas":
        st.markdown(' ### Este grafico de linhas é fictício foi exclusivamente para a base de teste no streamlit')
        chart_data = pd.DataFrame(
            np.random.randn(100, 3),
            columns=['Germinacao', 'Producao', 'Semeadura'])
        st.line_chart(chart_data)


    def criar_histograma(coluna, df):
        chart = alt.Chart(df, width=700).mark_bar().encode(
        alt.X(coluna, bin=True),
        y='count()', tooltip=[coluna, 'count()']
        ).interactive()
        return chart

    if add_selectbox4 == "Histograma":
        col_num = st.selectbox('Selecione a Coluna Numerica: ', colunas_numericas,key = 'unique')
        st.markdown('### Histograma de  ' + str(col_num))
        st.write(criar_histograma(col_num, df))


    def cria_correlationplot(df, colunas_numericas):
        cor_data = (df[colunas_numericas]).corr().stack().reset_index().rename(columns={0: 'correlation', 'level_0': 'variable', 'level_1': 'variable2'})
        cor_data['correlation_label'] = cor_data['correlation'].map('{:.2f}'.format)  # Round to 2 decimal
        base = alt.Chart(cor_data, width=700, height=600).encode( x = 'variable2:O', y = 'variable:O')
        text = base.mark_text().encode(text = 'correlation_label',color = alt.condition(alt.datum.correlation > 0.5,alt.value('white'),
        alt.value('black')))

        cor_plot = base.mark_rect().encode(
        color = 'correlation:Q')

        return cor_plot + text

    if add_selectbox4 == "Correlação":
        st.markdown(' ### Gráfico de Correlação ')
        st.write(cria_correlationplot(df, colunas_numericas))


    st.sidebar.markdown(' ## Sobre a autora')
    st.sidebar.image('enviar.jpg', width=90)
    add_markdown2 = st.sidebar.markdown(' ### Maria Betânia Honorio')
    add_markdown3 = st.sidebar.markdown(''' Monitora ambiental em Unidade
                                        de Conservação de Minas Gerais, Formada em
                                        Ánalise e Desenvolvimento de Sistemas e
                                        Estudanete em Ciências de dados, pela
                                        Codenation, IGTI e QODA''')
    st.sidebar.markdown('## Linkedin')
    st.sidebar.markdown('https://www.linkedin.com/in/maria-betania-honorio/')

if __name__ == '__main__':
    main()
