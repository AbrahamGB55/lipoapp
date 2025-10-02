import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="Calculadora de Pérdida Permisible de Grasa",
    page_icon="🏥",
    layout="centered"
)

# CSS profesional
st.markdown("""
<style>
    .stApp {
        max-width: 600px;
        margin: 0 auto;
        font-family: 'Segoe UI', sans-serif;
    }
    
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .header-title {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .header-subtitle {
        font-size: 1rem;
        opacity: 0.9;
        margin-bottom: 0;
    }
    
    .result-container {
        background: #f8f9ff;
        border: 2px solid #e1e8ff;
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .metric-container {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #2c3e50;
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #7f8c8d;
        margin-top: 0.5rem;
    }
    
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #fdcb6e;
    }
    
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #28a745;
    }
    
    .error-box {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #dc3545;
    }
    
    .info-box {
        background: #e3f2fd;
        border: 1px solid #bbdefb;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    
    .tab-header {
        text-align: center;
        color: #2c3e50;
        font-size: 1.4rem;
        font-weight: 600;
        margin: 1rem 0 2rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    .stSelectbox > div > div {
        border-radius: 8px;
    }
    
    .stNumberInput > div > div {
        border-radius: 8px;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2.2rem;
        font-weight: 700;
        color: #2c3e50;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
        color: #7f8c8d;
    }
    
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 2rem;
        border-top: 1px solid #e9ecef;
        color: #6c757d;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-container">
    <h1 class="header-title">Calculadora de Pérdida Permisible de Grasa</h1>
    <p class="header-subtitle">Herramienta profesional para planificación quirúrgica en liposucción</p>
</div>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2 = st.tabs(["🧮 Pérdida Permisible de Grasa", "💧 Fórmula de Rohrich"])

# Tab 1: Calculadora Principal
with tab1:
    st.markdown('<h2 class="tab-header">Cálculo de Pérdida Permisible de Grasa</h2>', unsafe_allow_html=True)
    
    # Inputs organizados en columnas
    col1, col2 = st.columns(2)
    
    with col1:
        weight = st.number_input(
            "Peso (kg)",
            min_value=40.0,
            max_value=200.0,
            value=70.0,
            step=0.5
        )
        
        gender = st.selectbox(
            "Sexo",
            ["Masculino", "Femenino"]
        )
        
        initial_hemoglobin = st.number_input(
            "Hemoglobina Inicial (g/dL)",
            min_value=10.0,
            max_value=20.0,
            value=13.0,
            step=0.1
        )
    
    with col2:
        age = st.number_input(
            "Edad (años)",
            min_value=18,
            max_value=70,
            value=30,
            step=1
        )
        
        min_hemoglobin = st.number_input(
            "Hemoglobina Mínima (g/dL)",
            min_value=7.0,
            max_value=12.0,
            value=10.0,
            step=0.1
        )
    
    # Método de cálculo de volumen sanguíneo
    st.markdown("### Método de Cálculo del Volumen Sanguíneo")
    
    calc_method = st.radio(
        "Seleccione el método:",
        ["Método Simplificado", "Fórmula de Nadler"],
        horizontal=True
    )
    
    if calc_method == "Fórmula de Nadler":
        height = st.number_input(
            "Altura (cm)",
            min_value=140.0,
            max_value=220.0,
            value=170.0,
            step=1.0
        )
    
    # Botón de cálculo
    if st.button("CALCULAR", use_container_width=True):
        if initial_hemoglobin <= min_hemoglobin:
            st.markdown('<div class="error-box">⚠️ La hemoglobina inicial debe ser mayor que la mínima</div>', unsafe_allow_html=True)
        else:
            # Calcular volumen sanguíneo
            if calc_method == "Método Simplificado":
                blood_volume = weight * (75 if gender == "Masculino" else 65)
            else:
                # Fórmula de Nadler (mantenida original)
                if gender == "Masculino":
                    blood_volume = (0.006012 * (height ** 3)) / (14.6 * weight) + 604
                else:
                    blood_volume = (0.005835 * (height ** 3)) / (15 * weight) + 183
            
            # Calcular pérdida permisible de sangre (fórmula estándar)
            hb_difference = initial_hemoglobin - min_hemoglobin
            permissible_blood_loss = (hb_difference / initial_hemoglobin) * blood_volume
            
            # Calcular pérdida permisible de grasa (modelo predictivo del paper)
            # Y2 = 383.725 + 3.406(MPSA) - 29.116(Edad)
            permissible_fat_loss = 383.725 + (3.406 * permissible_blood_loss) - (29.116 * age)
            
            # Aplicar límites de seguridad
            permissible_fat_loss = max(0, min(permissible_fat_loss, 10000))
            
            # Mostrar resultados
            st.markdown('<div class="result-container">', unsafe_allow_html=True)
            
            # Métricas principales
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(
                    "Pérdida Permisible de Sangre",
                    f"{permissible_blood_loss:.0f} ml",
                    help="Máxima pérdida sanguínea segura"
                )
            
            with col2:
                st.metric(
                    "Pérdida Permisible de Grasa",
                    f"{permissible_fat_loss:.0f} ml",
                    help="Máximo volumen de grasa a aspirar"
                )
            
            # Información adicional
            st.markdown(f"**Volumen Sanguíneo Estimado:** {blood_volume:.0f} ml")
            st.markdown(f"**Método Utilizado:** {calc_method}")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Advertencias
            if permissible_fat_loss > 5000:
                st.markdown('<div class="warning-box">⚠️ <strong>Atención:</strong> Volumen > 5000 ml. Se recomienda realizar el procedimiento en centro con UCI.</div>', unsafe_allow_html=True)
            
            if permissible_fat_loss > 3000:
                st.markdown('<div class="warning-box">💡 <strong>Recomendación:</strong> Considerar manejo hidroelectrolítico especializado.</div>', unsafe_allow_html=True)
    
    # Información del método
    with st.expander("ℹ️ Información del Método"):
        st.markdown("""
        **Modelo Predictivo:**
        
        La fórmula utilizada se basa en el estudio de Manzaneda Cipriani et al., que desarrolló un modelo predictivo con 102 pacientes para determinar la pérdida permisible de grasa en liposucción.
        
        **Fórmula (Modelo Multivariado):**
        ```
        Pérdida Permisible de Grasa = 383.725 + 3.406 × (MPSA) - 29.116 × (Edad)
        ```
        
        **Métodos de Cálculo del Volumen Sanguíneo:**
        - **Simplificado:** Masculino (75 ml/kg), Femenino (65 ml/kg)
        - **Nadler:** Fórmula específica basada en altura y peso
        """)

# Tab 2: Fórmula de Rohrich (CORREGIDA)
with tab2:
    st.markdown('<h2 class="tab-header">Fórmula de Rohrich</h2>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #6c757d; margin-bottom: 2rem;">Evaluación del balance hídrico en liposucción tipo súper húmeda</p>', unsafe_allow_html=True)
    
    # Inputs
    col1, col2 = st.columns(2)
    
    with col1:
        total_aspirate = st.number_input(
            "Aspirado Total (cc)",
            min_value=0,
            max_value=10000,
            value=3000,
            step=100
        )
        
        liquid_infiltrated = st.number_input(
            "Líquido Infiltrado (cc)",
            min_value=0,
            max_value=20000,
            value=3000,
            step=100
        )
    
    with col2:
        endovenous_liquid = st.number_input(
            "Líquido Endovenoso (cc)",
            min_value=0,
            max_value=10000,
            value=1500,
            step=100
        )
    
    # Botón de cálculo
    if st.button("CALCULAR RATIO", use_container_width=True):
        if total_aspirate > 0:
            # Calcular líquidos administrados totales
            total_liquids = endovenous_liquid + liquid_infiltrated
            ratio = total_liquids / total_aspirate
            
            # Determinar líquidos recomendados según Rohrich 2006
            if total_aspirate < 5000:
                # Para pequeño volumen: Ratio 1.8, sin líquido de reemplazo
                base_ratio = 1.8
                replacement_fluid = 0
                recommended_total = base_ratio * total_aspirate
                replacement_message = "No se requiere líquido de reemplazo adicional (volumen < 5000 cc)"
            else:
                # Para gran volumen: Ratio 1.2 + líquido de reemplazo
                base_ratio = 1.2
                # Líquido de reemplazo = 0.25 cc × (Aspirado - 5000)
                replacement_fluid = 0.25 * (total_aspirate - 5000)
                # Total recomendado = (1.2 × Aspirado) + Líquido de reemplazo
                recommended_total = (base_ratio * total_aspirate) + replacement_fluid
                replacement_message = f"Líquido de reemplazo adicional requerido: {replacement_fluid:.0f} cc IV"
            
            # Calcular ratio efectivo recomendado
            recommended_ratio = recommended_total / total_aspirate
            
            # Mostrar resultados
            st.markdown('<div class="result-container">', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Ratio Calculado", f"{ratio:.2f}")
            
            with col2:
                st.metric("Ratio Recomendado", f"{recommended_ratio:.2f}")
            
            with col3:
                st.metric("Líquidos Recomendados", f"{recommended_total:.0f} cc")
            
            # Mostrar información sobre líquido de reemplazo
            if total_aspirate >= 5000:
                st.markdown(f'<div class="info-box">💉 <strong>Líquido de Reemplazo IV Adicional:</strong> {replacement_fluid:.0f} cc (0.25 × [{total_aspirate} - 5000])<br>Este volumen se suma a los líquidos base (Ratio 1.2 × Aspirado)</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="info-box">ℹ️ {replacement_message}</div>', unsafe_allow_html=True)
            
            # Evaluación del ratio
            difference = abs(ratio - recommended_ratio)
            tolerance = recommended_ratio * 0.15  # 15% de tolerancia
            
            if difference <= tolerance:
                st.markdown('<div class="success-box">✅ <strong>Ratio Adecuado:</strong> El balance hídrico está dentro del rango recomendado.</div>', unsafe_allow_html=True)
            elif ratio < recommended_ratio:
                deficit = recommended_total - total_liquids
                st.markdown(f'<div class="warning-box">⚠️ <strong>Ratio Bajo:</strong> Considere aumentar la reposición de líquidos. Déficit aproximado: {deficit:.0f} cc</div>', unsafe_allow_html=True)
            else:
                excess = total_liquids - recommended_total
                st.markdown(f'<div class="error-box">⚠️ <strong>Ratio Alto:</strong> Riesgo de sobrecarga hídrica. Exceso aproximado: {excess:.0f} cc. Considere reducir la reposición.</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Detalles del cálculo
            with st.expander("📊 Detalles del Cálculo"):
                details_text = f"""
                **Cálculo del Ratio Actual:**
                - Líquido Infiltrado: {liquid_infiltrated} cc
                - Líquido Endovenoso: {endovenous_liquid} cc
                - **Líquido Total Administrado:** {liquid_infiltrated} + {endovenous_liquid} = **{total_liquids} cc**
                - Aspirado Total: {total_aspirate} cc
                - **Ratio Actual:** {total_liquids} ÷ {total_aspirate} = **{ratio:.2f}**
                
                **Criterio Aplicado (Rohrich 2006):**
                """
                
                if total_aspirate < 5000:
                    details_text += f"""
                - Volumen < 5000 cc: Ratio base = **1.8**
                - **Líquidos Recomendados:** 1.8 × {total_aspirate} = **{recommended_total:.0f} cc**
                - No requiere líquido de reemplazo adicional
                """
                else:
                    base_liquids = base_ratio * total_aspirate
                    details_text += f"""
                - Volumen ≥ 5000 cc: Ratio base = **1.2**
                - **Líquidos base:** 1.2 × {total_aspirate} = {base_liquids:.0f} cc
                - **Líquido de reemplazo:** 0.25 × ({total_aspirate} - 5000) = **{replacement_fluid:.0f} cc**
                - **Total Recomendado:** {base_liquids:.0f} + {replacement_fluid:.0f} = **{recommended_total:.0f} cc**
                - **Ratio efectivo:** {recommended_total:.0f} ÷ {total_aspirate} = **{recommended_ratio:.2f}**
                """
                
                details_text += f"""
                
                **Evaluación:**
                - Líquidos administrados: {total_liquids} cc
                - Líquidos recomendados: {recommended_total:.0f} cc
                - **Diferencia:** {total_liquids - recommended_total:+.0f} cc
                """
                
                st.markdown(details_text)
        else:
            st.markdown('<div class="error-box">⚠️ El aspirado total debe ser mayor que 0</div>', unsafe_allow_html=True)
    
    # Información del método
    with st.expander("ℹ️ Información del Método"):
        st.markdown("""
        **Fórmula de Rohrich para Balance Hídrico (Versión 2006):**
        
        Esta fórmula evalúa el balance hídrico en pacientes sometidos a liposucción tipo súper húmeda.
        
        **Cálculo del Ratio:**
        ```
        Ratio = (Líquido Endovenoso + Líquido Infiltrado) ÷ Aspirado Total
        ```
        
        **Criterios según volumen aspirado:**
        
        **📌 Para volumen < 5000 cc:**
        - Ratio objetivo: **1.8**
        - Líquidos recomendados = 1.8 × Aspirado
        - Composición: Mantenimiento + Infiltración superhúmeda (1:1)
        - **No requiere líquido de reemplazo adicional**
        
        **📌 Para volumen ≥ 5000 cc:**
        - Ratio base: **1.2**
        - **Líquido de reemplazo adicional:** 0.25 × (Aspirado - 5000) cc IV
        - **Líquidos recomendados totales** = (1.2 × Aspirado) + Líquido de reemplazo
        - Composición: Mantenimiento + Infiltración + Reemplazo
        
        **Ejemplo para 7000 cc de aspirado:**
        - Líquidos base: 1.2 × 7000 = 8,400 cc
        - Líquido de reemplazo: 0.25 × (7000 - 5000) = 500 cc
        - **Total recomendado: 8,900 cc**
        - Ratio efectivo: 8,900 ÷ 7,000 = **1.27**
        
        **Cambios respecto a versión anterior (1998):**
        - Umbral aumentado de 4000 cc a **5000 cc**
        - Ratio pequeño volumen reducido de 2.1 a **1.8**
        - Ratio gran volumen reducido de 1.4 a **1.2**
        - Objetivo: Reducir sobrecarga de líquidos y gasto urinario excesivo
        
        **Referencia:**
        Rohrich RJ, Leedy JE, Swamy R, Brown SA, Coleman J. Fluid resuscitation in liposuction: a retrospective review of 89 consecutive patients. Plast Reconstr Surg. 2006;117(2):431-5.
        """)

# Footer
st.markdown("""
<div class="footer">
    <p><strong>Referencia:</strong> Manzaneda Cipriani R. et al. Pérdida permisible de grasa en liposucción: fórmula y aplicación informática para cuantificar un nuevo concepto. Cir. plást. iberolatinoam. 2021;47(1):19-28</p>
    <p><em>Herramienta desarrollada para uso profesional en cirugía plástica</em></p>
</div>
""", unsafe_allow_html=True)
