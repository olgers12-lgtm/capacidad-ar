import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Datos base
recetas = pd.DataFrame({
    "Receta": ["Sapphire", "Prevencia", "Rock", "Super Hidrofobico"],
    "Participacion": [50.24, 21.47, 4.25, 24.04],  # %
    "Tiempo_h": [1.6, 1.2, 1.6, 1.1]  # horas por cámara
})

LENTES_CAMARA = 56
JOBS_CAMARA = 28

def calcular_capacidad(num_maquinas=2, horas_dia=16, oee=0.85, 
                      sapphire=50.24, prevencia=21.47, rock=4.25, superh=24.04):
    mix = pd.DataFrame({
        "Receta": ["Sapphire", "Prevencia", "Rock", "Super Hidrofobico"],
        "Participacion": [sapphire, prevencia, rock, superh],
        "Tiempo_h": [1.6, 1.2, 1.6, 1.1]
    })
    mix["Peso"] = mix["Participacion"] / 100
    tiempo_prom = (mix["Peso"] * mix["Tiempo_h"]).sum()
    camaras_maquina = (horas_dia * oee) / tiempo_prom
    camaras_totales = camaras_maquina * num_maquinas
    lentes_dia = camaras_totales * LENTES_CAMARA
    jobs_dia = camaras_totales * JOBS_CAMARA
    return tiempo_prom, camaras_totales, lentes_dia, jobs_dia

def grafico_3d(num_maquinas):
    horas = np.arange(8, 25, 1)
    oees = np.arange(0.6, 1.01, 0.05)
    H, O = np.meshgrid(horas, oees)
    Z = np.zeros_like(H)
    for i in range(H.shape[0]):
        for j in range(H.shape[1]):
            _, _, lentes, _ = calcular_capacidad(num_maquinas, H[i, j], O[i, j])
            Z[i, j] = lentes
    fig = go.Figure(data=[go.Surface(z=Z, x=H, y=O)])
    fig.update_layout(
        title=f"Capacidad de Lentes/día (con {num_maquinas} máquinas)",
        scene=dict(
            xaxis_title='Horas por día',
            yaxis_title='OEE',
            zaxis_title='Lentes por día'
        ),
        autosize=True, height=600
    )
    return fig

st.title("📌 Modelo de capacidad AR - Interactivo y 3D")

num_maquinas = st.slider("Máquinas", min_value=1, max_value=5, value=2, step=1)
horas_dia = st.slider("Horas/día", min_value=8, max_value=24, value=16, step=1)
oee = st.slider("OEE", min_value=0.6, max_value=1.0, value=0.85, step=0.05)
sapphire = st.slider("Sapphire %", min_value=0.0, max_value=100.0, value=50.24, step=1.0)
prevencia = st.slider("Prevencia %", min_value=0.0, max_value=100.0, value=21.47, step=1.0)
rock = st.slider("Rock %", min_value=0.0, max_value=100.0, value=4.25, step=1.0)
superh = st.slider("SuperH %", min_value=0.0, max_value=100.0, value=24.04, step=1.0)

tiempo_prom, camaras, lentes, jobs = calcular_capacidad(
    num_maquinas, horas_dia, oee, sapphire, prevencia, rock, superh
)

st.markdown(f"**📊 Tiempo promedio por cámara:** {tiempo_prom:.2f} h")
st.markdown(f"**🏭 Cámaras totales/día:** {camaras:.1f}")
st.markdown(f"**👓 Lentes/día:** {lentes:.0f}")
st.markdown(f"**📦 Jobs/día:** {jobs:.0f}")

st.plotly_chart(grafico_3d(num_maquinas), use_container_width=True)