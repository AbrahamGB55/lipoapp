import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Configuración de la página
st.set_page_config(
    page_title="Calculadora de Pérdida Permisible de Grasa en Liposucción",
    page_icon="🏥",
    layout="wide"
)

# Título principal
st.title("🏥 Calculadora de Pérdida Permisible de Grasa en Liposucción")
st.markdown("### Basada en: Manzaneda Cipriani R. et al. (2021)")
st.markdown("*Cir. plást. iberolatinoam. Vol. 47 - Nº 1*")

# Información del estudio
with st.expander("📊 Información del estudio original"):
    st.info("""
    **Población del estudio:**
    - 102 pacientes (97 mujeres, 5 hombres)
    - Edad promedio: 32.5 años (rango 18-54)
    - IMC promedio: 22.06
    - Infiltración superhúmeda (relación 1:1)
    - Hemoglobina postoperatoria objetivo: 10 ± 0.5 g/dl
    
    **Poder predictivo de los modelos:**
    - Modelo simple: R² = 47%
    - Modelo con edad: R² = 49%
    """)

# Crear columnas para el layout
col1, col2 = st.columns(2)

with col1:
    st.header("📋 Datos del Paciente")
    
    # Inputs del paciente
    peso = st.number_input("Peso (kg)", min_value=40.0, max_value=200.0, value=70.0, step=0.5,
                          help="Peso del paciente en kilogramos")
    
    altura = st.number_input("Altura (cm)", min_value=140.0, max_value=220.0, value=170.0, step=1.0,
                            help="Altura del paciente en centímetros")
    
    genero = st.selectbox("Género", ["Masculino", "Femenino"])
    
    edad = st.number_input("Edad (años)", min_value=18, max_value=70, value=30, step=1,
                          help="En el estudio original: 18-54 años")
    
    hb_actual = st.number_input("Hemoglobina actual (g/dl)", min_value=10.0, max_value=20.0, value=13.0, step=0.1,
                               help="Hemoglobina preoperatoria del paciente")
    
    hb_minima = st.number_input("Hemoglobina mínima aceptable (g/dl)", min_value=7.0, max_value=12.0, value=10.0, step=0.1,
                               help="El estudio utilizó 10 g/dl como estándar de seguridad")
    
    # Calcular IMC
    imc = peso / ((altura/100) ** 2)
    st.metric("IMC", f"{imc:.2f} kg/m²", 
              delta=f"{imc - 22.06:.2f} vs promedio del estudio")

with col2:
    st.header("🩸 Cálculo del Volumen Sanguíneo")
    
    # Cálculo del volumen sanguíneo según Nadler
    if genero == "Masculino":
        # Fórmula exacta del paper
        vol_sang_nadler = (0.006012 * (altura ** 3)) / (14.6 * peso) + 604
        vol_sang_simple = peso * 75
    else:
        # Fórmula exacta del paper
        vol_sang_nadler = (0.005835 * (altura ** 3)) / (15 * peso) + 183
        vol_sang_simple = peso * 65
    
    # Mostrar ambos métodos de cálculo
    st.metric("Volumen sanguíneo (Ecuación de Nadler)", f"{vol_sang_nadler:.1f} ml",
             help="Método más preciso según el paper")
    st.metric("Volumen sanguíneo (Método simplificado)", f"{vol_sang_simple:.1f} ml",
             help="Hombres: 75 ml/kg, Mujeres: 65 ml/kg")
    
    # Permitir al usuario elegir qué método usar
    metodo_vol = st.radio("Seleccione método de cálculo:", 
                         ["Ecuación de Nadler (recomendado)", "Método simplificado"])
    
    if metodo_vol == "Ecuación de Nadler (recomendado)":
        vol_sanguineo = vol_sang_nadler
    else:
        vol_sanguineo = vol_sang_simple

# Separador
st.markdown("---")

# Cálculos principales
st.header("📊 Resultados de Pérdida Permisible de Grasa")

# Calcular pérdida permisible de sangre (MPSA) - Fórmula correcta del paper
mpsa = (hb_actual - hb_minima) * peso * vol_sanguineo

# Mostrar cálculo detallado
with st.expander("🧮 Ver cálculo detallado de MPSA"):
    st.latex(r"MPSA = (Hb_{actual} - Hb_{mínima}) \times Peso \times Volumen_{sanguíneo}")
    st.write(f"MPSA = ({hb_actual} - {hb_minima}) × {peso} × {vol_sanguineo:.1f}")
    st.write(f"MPSA = {mpsa:.1f} ml")

# Modelo predictivo simple (R² = 47%)
vol_grasa_simple = 3.4356 * mpsa + 61.269

# Modelo predictivo múltiple con edad (R² = 49%)
vol_grasa_multiple = 383.725 + 3.406 * mpsa - 29.116 * edad

# Crear columnas para mostrar resultados
res_col1, res_col2, res_col3 = st.columns(3)

with res_col1:
    st.metric("Pérdida Permisible de Sangre (MPSA)", f"{mpsa:.0f} ml", 
              help="Máxima pérdida sanguínea para llegar a Hb mínima")

with res_col2:
    st.metric("Volumen de Grasa - Modelo Simple", f"{vol_grasa_simple:.0f} ml",
              help="Y = 3.4356 × MPSA + 61.269 (R² = 47%)")

with res_col3:
    st.metric("Volumen de Grasa - Modelo con Edad", f"{vol_grasa_multiple:.0f} ml",
              help="Y₂ = 383.725 + 3.406 × MPSA - 29.116 × edad (R² = 49%)", 
              delta=f"{vol_grasa_multiple - vol_grasa_simple:.0f} ml diferencia")

# Advertencia si el volumen es mayor a 5000cc
if vol_grasa_multiple > 5000:
    st.warning("⚠️ **Atención**: Volumen > 5000 cc. Se recomienda realizar el procedimiento en centro con UCI disponible.")

# Gráfico comparativo
st.markdown("---")
st.header("📈 Visualización de Resultados")

# Crear dos columnas para gráficos
graf_col1, graf_col2 = st.columns(2)

with graf_col1:
    # Gráfico de barras
    fig_bar = go.Figure()
    
    categorias = ['Pérdida Sangre\n(MPSA)', 'Grasa\n(Modelo Simple)', 'Grasa\n(Modelo con Edad)']
    valores = [mpsa, vol_grasa_simple, vol_grasa_multiple]
    colores = ['#ff4b4b', '#4b9bff', '#4bff4b']
    
    fig_bar.add_trace(go.Bar(
        x=categorias,
        y=valores,
        text=[f'{v:.0f} ml' for v in valores],
        textposition='auto',
        marker_color=colores
    ))
    
    fig_bar.update_layout(
        title="Comparación de Volúmenes Calculados",
        yaxis_title="Volumen (ml)",
        showlegend=False,
        height=400
    )
    
    st.plotly_chart(fig_bar, use_container_width=True)

with graf_col2:
    # Gráfico de la relación lineal (como en el paper)
    mpsa_range = np.linspace(0, 2500, 100)
    grasa_simple = 3.4356 * mpsa_range + 61.269
    
    fig_scatter = go.Figure()
    
    # Línea de regresión
    fig_scatter.add_trace(go.Scatter(
        x=mpsa_range,
        y=grasa_simple,
        mode='lines',
        name='Modelo de regresión',
        line=dict(color='blue', width=2)
    ))
    
    # Punto actual
    fig_scatter.add_trace(go.Scatter(
        x=[mpsa],
        y=[vol_grasa_simple],
        mode='markers',
        name='Paciente actual',
        marker=dict(color='red', size=12)
    ))
    
    fig_scatter.update_layout(
        title="Relación MPSA vs Volumen de Grasa<br>(y = 3.4356x + 61.269)",
        xaxis_title="Pérdida permisible de sangre (ml)",
        yaxis_title="Volumen aspirado de grasa (ml)",
        height=400,
        showlegend=True
    )
    
    st.plotly_chart(fig_scatter, use_container_width=True)

# Calculadora de fluidos de Rohrich
st.markdown("---")
st.header("💧 Manejo de Fluidos Intraoperatorios (Rohrich et al.)")

fluid_col1, fluid_col2 = st.columns(2)

with fluid_col1:
    st.subheader("Datos de la cirugía")
    vol_aspirado = st.number_input("Volumen aspirado total (ml)", 
                                   min_value=0, max_value=10000, value=int(vol_grasa_multiple), step=100,
                                   help="Volumen total aspirado durante la liposucción")
    
    vol_infiltrado = st.number_input("Volumen infiltrado (ml)", 
                                     min_value=0, max_value=20000, value=int(vol_aspirado), step=100,
                                     help="Técnica superhúmeda: relación 1:1")
    
    vol_iv = st.number_input("Volumen IV administrado (ml)", 
                             min_value=0, max_value=10000, value=1500, step=100,
                             help="Volumen de fluidos intravenosos")

with fluid_col2:
    st.subheader("Análisis del ratio de fluidos")
    
    if vol_aspirado > 0:
        # Calcular ratio según fórmula del paper
        ratio_actual = (vol_iv + vol_infiltrado) / vol_aspirado
        
        # Determinar ratio recomendado según volumen
        if vol_aspirado <= 5000:
            ratio_recomendado = 1.8
            st.info("📌 Aspirado ≤ 5000 ml → Ratio recomendado: 1.8")
        else:
            ratio_recomendado = 1.2
            st.info("📌 Aspirado > 5000 ml → Ratio recomendado: 1.2")
        
        # Mostrar métricas
        st.metric("Ratio actual", f"{ratio_actual:.2f}")
        
        # Evaluar el ratio
        if ratio_actual < ratio_recomendado * 0.9:
            st.error(f"⚠️ Ratio insuficiente. Aumentar fluidos IV en ~{int((ratio_recomendado - ratio_actual) * vol_aspirado)} ml")
        elif ratio_actual > ratio_recomendado * 1.1:
            st.warning("⚠️ Ratio elevado. Riesgo de sobrecarga hídrica.")
        else:
            st.success("✅ Ratio de fluidos dentro del rango adecuado.")
        
        # Mostrar fórmula
        with st.expander("Ver fórmula del ratio"):
            st.latex(r"Ratio = \frac{Volumen_{IV} + Volumen_{infiltrado}}{Volumen_{aspirado}}")

# Información adicional
st.markdown("---")
st.header("📝 Información Importante")

col_info1, col_info2 = st.columns(2)

with col_info1:
    with st.expander("📐 Fórmulas matemáticas utilizadas"):
        st.markdown("""
        ### 1. Volumen sanguíneo (Ecuación de Nadler):
        **Hombres:**
        ```
        VS = (0.006012 × altura³) / (14.6 × peso) + 604
        ```
        **Mujeres:**
        ```
        VS = (0.005835 × altura³) / (15 × peso) + 183
        ```
        
        ### 2. Pérdida Permisible de Sangre (MPSA):
        ```
        MPSA = (Hb actual - Hb mínima) × peso × volumen sanguíneo
        ```
        
        ### 3. Modelo predictivo simple (R² = 0.47):
        ```
        Volumen grasa = 3.4356 × MPSA + 61.269
        ```
        
        ### 4. Modelo predictivo múltiple (R² = 0.49):
        ```
        Volumen grasa = 383.725 + 3.406 × MPSA - 29.116 × edad
        ```
        """)

with col_info2:
    with st.expander("⚠️ Consideraciones clínicas"):
        st.warning("""
        **IMPORTANTE:**
        - Esta calculadora es una herramienta de apoyo basada en evidencia científica
        - No reemplaza el juicio clínico individualizado
        - Basada en técnica de infiltración superhúmeda (1:1)
        - Hemoglobina objetivo postoperatoria: 10 g/dl
        - Para volúmenes > 5000 ml: requiere centro con UCI
        - Considerar comorbilidades del paciente
        - Monitoreo continuo de signos vitales
        - El estudio original excluyó procedimientos combinados
        """)

# Footer con referencia completa
st.markdown("---")
st.caption("""
**Referencia:** Manzaneda Cipriani R., Cano Guerra F.D., Adrianzen Núñez G.A. 
'Pérdida permisible de grasa en liposucción: fórmula y aplicación informática para cuantificar un nuevo concepto'. 
Cir. plást. iberolatinoam. 2021;47(1):19-28. DOI: 10.4321/S0376-78922021000100004
""")

# Sidebar con información adicional
st.sidebar.header("ℹ️ Acerca de esta calculadora")
st.sidebar.info("""
Esta aplicación implementa las fórmulas publicadas en el estudio de Manzaneda Cipriani et al. (2021), 
que desarrolló un modelo predictivo para calcular la pérdida permisible de grasa en liposucción 
basándose en parámetros hemodinámicos seguros.
""")

st.sidebar.markdown("### 🎯 Características del estudio:")
st.sidebar.markdown("""
- 102 pacientes (97 mujeres, 5 hombres)
- Edad: 18-54 años
- IMC promedio: 22.06
- Técnica: Infiltración superhúmeda
- Sin complicaciones mayores
- Hb postoperatoria objetivo: 10 g/dl
""")
