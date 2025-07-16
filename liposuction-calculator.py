import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Configuración de la página
st.set_page_config(
    page_title="Calculadora de Liposucción Segura",
    page_icon="🏥",
    layout="wide"
)

# Título principal
st.title("🏥 Calculadora de Pérdida Permisible de Grasa en Liposucción")
st.markdown("### Basada en la fórmula de Manzaneda Cipriani et al.")

# Crear columnas para el layout
col1, col2 = st.columns(2)

with col1:
    st.header("📋 Datos del Paciente")
    
    # Inputs del paciente
    peso = st.number_input("Peso (kg)", min_value=40.0, max_value=200.0, value=70.0, step=0.5)
    altura = st.number_input("Altura (cm)", min_value=140.0, max_value=220.0, value=170.0, step=1.0)
    genero = st.selectbox("Género", ["Masculino", "Femenino"])
    edad = st.number_input("Edad (años)", min_value=18, max_value=70, value=30, step=1)
    hb_actual = st.number_input("Hemoglobina actual (g/dl)", min_value=10.0, max_value=20.0, value=13.0, step=0.1)
    hb_minima = st.number_input("Hemoglobina mínima aceptable (g/dl)", min_value=7.0, max_value=12.0, value=10.0, step=0.1)

with col2:
    st.header("🩸 Cálculos de Volumen Sanguíneo")
    
    # Cálculo del volumen sanguíneo según Nadler
    if genero == "Masculino":
        vol_sang_nadler = (0.006012 * (altura ** 3)) / (14.6 * peso) + 604
        vol_sang_simple = peso * 75
    else:
        vol_sang_nadler = (0.005835 * (altura ** 3)) / (15 * peso) + 183
        vol_sang_simple = peso * 65
    
    # Mostrar ambos métodos de cálculo
    st.info(f"**Volumen sanguíneo (Ecuación de Nadler):** {vol_sang_nadler:.1f} ml")
    st.info(f"**Volumen sanguíneo (Método simplificado):** {vol_sang_simple:.1f} ml")
    
    # Permitir al usuario elegir qué método usar
    metodo_vol = st.radio("Seleccione método de cálculo:", 
                         ["Ecuación de Nadler (más precisa)", "Método simplificado"])
    
    if metodo_vol == "Ecuación de Nadler (más precisa)":
        vol_sanguineo = vol_sang_nadler
    else:
        vol_sanguineo = vol_sang_simple

# Separador
st.markdown("---")

# Cálculos principales
st.header("📊 Resultados")

# Calcular pérdida permisible de sangre (MPSA)
mpsa = (hb_actual - hb_minima) * peso * vol_sanguineo / 100

# Modelo predictivo simple
vol_grasa_simple = 3.4356 * mpsa + 61.269

# Modelo predictivo múltiple (con edad)
vol_grasa_multiple = 383.725 + 3.406 * mpsa - 29.116 * edad

# Crear columnas para mostrar resultados
res_col1, res_col2, res_col3 = st.columns(3)

with res_col1:
    st.metric("Pérdida Permisible de Sangre", f"{mpsa:.0f} cc", 
              help="Máxima pérdida sanguínea segura")

with res_col2:
    st.metric("Volumen de Grasa (Modelo Simple)", f"{vol_grasa_simple:.0f} cc",
              help="Basado en pérdida sanguínea únicamente")

with res_col3:
    st.metric("Volumen de Grasa (Modelo con Edad)", f"{vol_grasa_multiple:.0f} cc",
              help="Modelo más preciso que incluye la edad", 
              delta=f"{vol_grasa_multiple - vol_grasa_simple:.0f} cc")

# Gráfico comparativo
st.markdown("---")
st.header("📈 Visualización de Resultados")

fig = go.Figure()

# Agregar barras
categorias = ['Pérdida Sangre', 'Grasa (Simple)', 'Grasa (Con Edad)']
valores = [mpsa, vol_grasa_simple, vol_grasa_multiple]
colores = ['#ff4b4b', '#ffb74b', '#4bff4b']

fig.add_trace(go.Bar(
    x=categorias,
    y=valores,
    text=[f'{v:.0f} cc' for v in valores],
    textposition='auto',
    marker_color=colores
))

fig.update_layout(
    title="Comparación de Volúmenes Calculados",
    yaxis_title="Volumen (cc)",
    showlegend=False,
    height=400
)

st.plotly_chart(fig, use_container_width=True)

# Calculadora de fluidos de Rohrich
st.markdown("---")
st.header("💧 Manejo de Fluidos Intraoperatorios (Fórmula de Rohrich)")

fluid_col1, fluid_col2 = st.columns(2)

with fluid_col1:
    vol_aspirado = st.number_input("Volumen aspirado total (cc)", 
                                   min_value=0, max_value=10000, value=int(vol_grasa_multiple), step=100)
    vol_infiltrado = st.number_input("Volumen infiltrado (cc)", 
                                     min_value=0, max_value=20000, value=int(vol_aspirado), step=100)
    vol_iv = st.number_input("Volumen IV administrado (cc)", 
                             min_value=0, max_value=10000, value=1500, step=100)

with fluid_col2:
    # Calcular ratio
    if vol_aspirado > 0:
        ratio_actual = (vol_iv + vol_infiltrado) / vol_aspirado
        ratio_recomendado = 1.8 if vol_aspirado < 5000 else 1.2
        
        st.metric("Ratio actual", f"{ratio_actual:.2f}")
        st.metric("Ratio recomendado", f"{ratio_recomendado:.1f}")
        
        if ratio_actual < ratio_recomendado * 0.9:
            st.error("⚠️ Ratio por debajo del recomendado. Considere aumentar fluidos IV.")
        elif ratio_actual > ratio_recomendado * 1.1:
            st.warning("⚠️ Ratio por encima del recomendado. Riesgo de sobrecarga hídrica.")
        else:
            st.success("✅ Ratio de fluidos adecuado.")

# Recomendaciones
st.markdown("---")
st.header("📝 Recomendaciones y Notas")

with st.expander("ℹ️ Información sobre los cálculos"):
    st.markdown("""
    ### Fórmulas utilizadas:
    
    **1. Volumen sanguíneo (Ecuación de Nadler):**
    - Hombres: (0.006012 × altura³) / (14.6 × peso) + 604
    - Mujeres: (0.005835 × altura³) / (15 × peso) + 183
    
    **2. Pérdida Permisible de Sangre (MPSA):**
    - MPSA = (Hb actual - Hb mínima) × peso × volumen sanguíneo / 100
    
    **3. Modelo predictivo simple:**
    - Volumen grasa = 3.4356 × MPSA + 61.269
    
    **4. Modelo predictivo con edad:**
    - Volumen grasa = 383.725 + 3.406 × MPSA - 29.116 × edad
    
    **5. Ratio de fluidos de Rohrich:**
    - Aspirado < 5000 cc: ratio recomendado = 1.8
    - Aspirado ≥ 5000 cc: ratio recomendado = 1.2
    """)

with st.expander("⚠️ Advertencias importantes"):
    st.warning("""
    - Esta calculadora es una herramienta de apoyo y no reemplaza el juicio clínico.
    - Los valores son estimaciones basadas en el estudio de Manzaneda Cipriani et al.
    - Siempre considere las características individuales del paciente.
    - Para liposucciones > 5000 cc se recomienda centro con UCI.
    - Monitoree constantemente los signos vitales del paciente.
    """)

# Footer
st.markdown("---")
st.caption("Basado en: Manzaneda Cipriani R. et al. 'Pérdida permisible de grasa en liposucción: fórmula y aplicación informática para cuantificar un nuevo concepto'. Cir. plást. iberolatinoam. 2021;47(1):19-28")
