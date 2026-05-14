import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

1. Configuração da página
st.set_page_config(page_title="Expert Scanner B3", layout="wide")

st.title("🎯 Scanner Expert: Opções B3")
st.markdown("---")

2. Gestão de Risco Simplificada
st.sidebar.header("💰 Gestão de Banca")
banca = st.sidebar.number_input("Sua Banca (R {banca * (risco/100):.2f}")

3. Lógica de Data e Letras (Fora de blocos para evitar erros)
hoje = datetime.date.today()
mes_venc = hoje.month + 1 if hoje.day > 15 else hoje.month
if mes_venc > 12: mes_venc = 1

letras_c = "ABCDEFGHIJKL"
letras_p = "MNOPQRSTUVWX"
l_call = letras_c[mes_venc-1]
l_put = letras_p[mes_venc-1]

4. Lista de Ativos
ativos = ["PETR4.SA", "VALE3.SA", "ITUB4.SA", "BBDC4.SA", "BBAS3.SA", "ELET3.SA"]

st.write(f"Análise atualizada em: {hoje.strftime('%d/%m/%Y %H:%M')}")
cols = st.columns(3)

5. Loop de Análise
for i, ticker in enumerate(ativos):
try:
df = yf.download(ticker, period="60d", interval="1d", progress=False)
if df.empty: continue

# Médias e Volume
df['M9'] = df['Close'].rolling(window=9).mean()
df['M20'] = df['Close'].rolling(window=20).mean()
df['V_Avg'] = df['Volume'].rolling(window=20).mean()

p = df['Close'].iloc[-1]
m9 = df['M9'].iloc[-1]
m20 = df['M20'].iloc[-1]
v_ok = df['Volume'].iloc[-1] > df['V_Avg'].iloc[-1]

nome = ticker.replace(".SA", "")
with cols[i % 3]:
st.info(f"{nome}")
st.metric("Preço", f"R$ {p:.2f}")

# Sinais
if p > m9 and m9 > m20 and v_ok:
st.success(f"🚀 CALL: {nome}{l_call}{round(p)}")
elif p < m9 and m9 < m20 and v_ok:
st.error(f"📉 PUT: {nome}{l_put}{round(p)}")
else:
st.warning("⚖️ Neutro")
except:
continue