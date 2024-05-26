import streamlit as st
import pandas as pd
import altair as alt

@st.cache_data
def load_data():
    return pd.read_csv('dados.csv')

data = load_data()
data = data[["Qual seu nome?","Qual sua idade?","Qual estilo de corte você usa?","Horário de preferência para cortar:","Dia de preferência:","Média de cortes por mês:"]]

st.title("Análise de Dados da Barbearia")

st.sidebar.header("Barbershop Board")
st.sidebar.subheader("Filtros")

idade_min = int(data['Qual sua idade?'].min())
idade_max = int(data['Qual sua idade?'].max())
idade = st.sidebar.slider(
    'Idade', idade_min, idade_max, (idade_min, idade_max))

estilos = data['Qual estilo de corte você usa?'].unique()
estilo_corte = st.sidebar.multiselect('Estilo de Corte', estilos, estilos)

dias = data['Dia de preferência:'].unique()
dia_preferencia = st.sidebar.multiselect('Dia de Preferência', dias, dias)

filtered_data = data[
    (data['Qual sua idade?'] >= idade[0]) &
    (data['Qual sua idade?'] <= idade[1])
]

if estilo_corte:
    filtered_data = filtered_data[filtered_data['Qual estilo de corte você usa?'].isin(
        estilo_corte)]

if dia_preferencia:
    filtered_data = filtered_data[filtered_data['Dia de preferência:'].isin(
        dia_preferencia)]

st.subheader("Estilo de Corte por Faixa Etária")
corte_faixa_etaria = filtered_data.groupby(
    ['Qual estilo de corte você usa?', 'Qual sua idade?']).size().reset_index(name='counts')
corte_faixa_etaria_chart = alt.Chart(corte_faixa_etaria).mark_bar().encode(
    x='Qual sua idade?:O',
    y='counts:Q',
    color='Qual estilo de corte você usa?:N',
    tooltip=['Qual sua idade?', 'counts', 'Qual estilo de corte você usa?']
).interactive()
st.altair_chart(corte_faixa_etaria_chart, use_container_width=True)

st.subheader("Dias da Semana com Maior Frequência de Cortes")
frequencia_dia = filtered_data['Dia de preferência:'].value_counts(
).reset_index()
frequencia_dia.columns = ['Dia de preferência', 'counts']
frequencia_dia_chart = alt.Chart(frequencia_dia).mark_bar().encode(
    x='Dia de preferência:N',
    y='counts:Q',
    tooltip=['Dia de preferência', 'counts']
).interactive()
st.altair_chart(frequencia_dia_chart, use_container_width=True)

st.subheader("Média de Cortes por Mês")
media_cortes_mes = filtered_data.groupby(
    'Qual seu nome?')['Média de cortes por mês:'].mean().reset_index()
media_cortes_mes.columns = ['Cliente', 'Média de cortes por mês']
media_cortes_mes_chart = alt.Chart(media_cortes_mes).mark_bar().encode(
    x='Cliente:N',
    y='Média de cortes por mês:Q',
    tooltip=['Cliente', 'Média de cortes por mês']
).interactive()
st.altair_chart(media_cortes_mes_chart, use_container_width=True)

st.subheader("Horários de Preferência para Cortar Cabelo")
horario_preferencia = filtered_data['Horário de preferência para cortar:'].value_counts(
).reset_index()
horario_preferencia.columns = ['Horário de preferência', 'counts']
horario_preferencia_chart = alt.Chart(horario_preferencia).mark_bar().encode(
    x='Horário de preferência:N',
    y='counts:Q',
    tooltip=['Horário de preferência', 'counts']
).interactive()
st.altair_chart(horario_preferencia_chart, use_container_width=True)

st.subheader("Dados Filtrados")
st.write(filtered_data)
