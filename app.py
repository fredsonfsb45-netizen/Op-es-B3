import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

#Configuração da página para visualização Mobile
#(importante para o seu trabalho de campo em Belém)
st.set_page_config(page_title="Expert Scanner B3", layout="wide", initial_sidebar_state="collapsed")

st.title("🎯 Scanner Expert: Opções B3")
st.subheader("Foco: Compra a Seco (Call e Put)")
st.markdown("---")

#Painel Lateral para Gestão de Risco
with st.sidebar:
st.header("💰 Gestão de Banca")
banca_input = st.number_input("Sua Banca Total (R$`)", value=0.0)

def identificar_letra(tipo, mes):
letras_call = "ABCDEFGHIJKL"
letras_put = "MNOPQRSTUVWX"
return letras_call[mes-1] if tipo == 'CALL' else letras_put[mes-1]

#Lista de ativos com alta liquidez na B3
lista_ativos = ["PETR4.SA", "VALE3.SA", "ITUB4.SA", "BBDC4.SA", "BBAS3.SA", "ELET3.SA"]

if st.button('🔄 Atualizar Análise do Mercado'):
hoje = datetime.date.today()
mes_venc = hoje.month + 1 if hoje.day > 15 else hoje.month
if mes_venc > 12:
mes_venc = 1

cols = st.columns(3)

for i, ticker in enumerate(lista_ativos):
try:
dados = yf.download(ticker, period="60d", interval="1d", progress=False)
if dados.empty:
continue

dados['MA9'] = dados['Close'].rolling(window=9).mean()
dados['MA20'] = dados['Close'].rolling(window=20).mean()
dados['Vol_Avg'] = dados['Volume'].rolling(window=20).mean()

p_atual = dados['Close'].iloc[-1]
ma9_atual = dados['MA9'].iloc[-1]
ma20_atual = dados['MA20'].iloc[-1]
vol_confirmado = dados['Volume'].iloc[-1] > dados['Vol_Avg'].iloc[-1]

nome_limpo = ticker.replace(".SA", "")

with cols[i % 3]:
st.info(f"{nome_limpo}")
st.metric("Preço Atual", f"R`$ {p_atual:.2f}")

if p_atual > ma9_atual and ma9_atual > ma20_atual and vol_confirmado:
l = identificar_letra('CALL', mes_venc)
st.success(f"🚀 CALL: {nome_limpo}{l}{round(p_atual)}")

elif p_atual < ma9_atual and ma9_atual < ma20_atual and vol_confirmado:
l = identificar_letra('PUT', mes_venc)
st.error(f"📉 PUT: {nome_limpo}{l}{round(p_atual)}")

else:
st.warning("⚖️ Neutro")

except:
continue