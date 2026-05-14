import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

# Configuração da página
st.set_page_config(page_title="Expert Scanner B3", layout="wide")

st.title("🎯 Scanner Expert: Opções B3")
st.markdown("---")

# Gestão de Risco na barra lateral
st.sidebar.header("💰 Gestão de Banca")
banca_total = st.sidebar.number_input("Sua Banca (R {banca_total * (risco_op/100):.2f}")

# Lista de ativos
lista_ativos = ["PETR4.SA", "VALE3.SA", "ITUB4.SA", "BBDC4.SA", "BBAS3.SA", "ELET3.SA"]

if st.button('🔄 Atualizar Análise'):
hoje = datetime.date.today()
mes_venc = hoje.month + 1 if hoje.day > 15 else hoje.month
if mes_venc > 12: mes_venc = 1

# Mapeamento de letras sem usar função (mais seguro para celular)
letras_c = "ABCDEFGHIJKL"
letras_p = "MNOPQRSTUVWX"
letra_call = letras_c[mes_venc-1]
letra_put = letras_p[mes_venc-1]

cols = st.columns(3)

for i, ticker in enumerate(lista_ativos):
try:
df = yf.download(ticker, period="60d", interval="1d", progress=False)
if df.empty: continue

df['MA9'] = df['Close'].rolling(window=9).mean()
df['MA20'] = df['Close'].rolling(window=20).mean()
df['V_Avg'] = df['Volume'].rolling(window=20).mean()

p = df['Close'].iloc[-1]
m9 = df['MA9'].iloc[-1]
m20 = df['MA20'].iloc[-1]
v_ok = df['Volume'].iloc[-1] > df['V_Avg'].iloc[-1]

nome = ticker.replace(".SA", "")
with cols[i % 3]:
st.info(f"{nome}")
st.metric("Preço", f"R$ {p:.2f}")

if p > m9 and m9 > m20 and v_ok:
st.success(f"🚀 CALL: {nome}{letra_call}{round(p)}")
elif p < m9 and m9 < m20 and v_ok:
st.error(f"📉 PUT: {nome}{letra_put}{round(p)}")
else:
st.warning("⚖️ Neutro")
except:
continue