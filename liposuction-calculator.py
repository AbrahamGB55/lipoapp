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

# ============================================================================
# TAB 1: PÉRDIDA PERMISIBLE DE GRASA (PPG)
# ============================================================================
with tab1:
    st.markdown('<h2 class="tab-header">Cálculo de Pérdida Permisible de Grasa</h2>', unsafe_allow_html=True)
    
    # Inputs organizados en columnas (igual que la app original)
    col1, col2 = st.columns(2)
    
    with col1:
        weight = st.number_input(
            "Peso (kg)",
            min_value=40.0,
            max_value=200.0,
            value=70.0,
            step=0.5,
            key="weight"
        )
        
        min_hemoglobin = st.number_input(
            "Hemoglobina Mínima (g/dL)",
            min_value=7.0,
            max_value=12.0,
            value=10.0,
            step=0.1,
            key="min_hb"
        )
        
        age = st.number_input(
            "Edad (años)",
            min_value=18,
            max_value=70,
            value=30,
            step=1,
            key="age"
        )
    
    with col2:
        gender = st.selectbox(
            "Género",
            ["Masculino", "Femenino"],
            key="gender"
        )
        
        initial_hemoglobin = st.number_input(
            "Hemoglobina Inicial (g/dL)",
            min_value=10.0,
            max_value=20.0,
            value=13.0,
            step=0.1,
            key="initial_hb"
        )
    
    # Botón de cálculo
    if st.button("CALCULAR PÉRDIDA PERMISIBLE DE GRASA", use_container_width=True, key="calc_ppg"):
        if initial_hemoglobin <= min_hemoglobin:
            st.markdown('<div class="error-box">⚠️ La hemoglobina inicial debe ser mayor que la mínima</div>', unsafe_allow_html=True)
        else:
            # Calcular volumen circulante (método simplificado)
            blood_volume = weight * (75 if gender == "Masculino" else 65)
            
            # Calcular pérdida permisible de sangre (MPSA)
            hb_difference = initial_hemoglobin - min_hemoglobin
            permissible_blood_loss = (hb_difference / initial_hemoglobin) * blood_volume
            
            # Calcular pérdida permisible de grasa (PPG)
            # Fórmula: PPG = 383.725 + 3.406(MPSA) - 29.116(Edad)
            permissible_fat_loss = 383.725 + (3.406 * permissible_blood_loss) - (29.116 * age)
            
            # Aplicar límites de seguridad
            permissible_fat_loss = max(0, min(permissible_fat_loss, 10000))
            
            # Mostrar resultados
            st.markdown('<div class="result-container">', unsafe_allow_html=True)
            
            # Métricas principales
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Volumen Circulante",
                    f"{blood_volume:.0f} cc",
                    help="Volumen sanguíneo estimado"
                )
            
            with col2:
                st.metric(
                    "Pérdida Permisible de Sangre",
                    f"{permissible_blood_loss:.0f} cc",
                    help="Máxima pérdida sanguínea segura (MPSA)"
                )
            
            with col3:
                st.metric(
                    "Pérdida Permisible de Grasa",
                    f"{permissible_fat_loss:.0f} cc",
                    help="Máximo volumen de grasa a aspirar (PPG)"
                )
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Advertencias según volumen
            if permissible_fat_loss > 5000:
                st.markdown('<div class="warning-box">⚠️ <strong>Atención:</strong> Volumen > 5000 cc. Se recomienda realizar el procedimiento en centro con UCI.</div>', unsafe_allow_html=True)
            
            if permissible_fat_loss > 3000:
                st.markdown('<div class="warning-box">💡 <strong>Recomendación:</strong> Considerar manejo hidroelectrolítico especializado.</div>', unsafe_allow_html=True)
            
            if permissible_fat_loss < 1000:
                st.markdown('<div class="info-box">ℹ️ <strong>Nota:</strong> Volumen bajo. Verificar parámetros del paciente.</div>', unsafe_allow_html=True)
    
    # Información del método
    with st.expander("ℹ️ Información del Método"):
        st.markdown("""
        **Modelo Predictivo de Pérdida Permisible de Grasa (PPG):**
        
        Esta fórmula predictiva está hecha para uso exclusivo de cirujanos plásticos. El cirujano plástico puede tener con esta aplicación una aproximación de cuánta grasa se puede retirar sin incrementar el riesgo de complicaciones o necesidad de transfusiones sanguíneas.
        
        **Fórmula (Modelo Multivariado):**
        ```
        PPG = 383.725 + 3.406 × (MPSA) - 29.116 × (Edad)
        ```
        
        **Cálculo del Volumen Circulante:**
        - **Hombres:** Peso (kg) × 75 cc/kg
        - **Mujeres:** Peso (kg) × 65 cc/kg
        
        **Máxima Pérdida Sanguínea Permisible (MPSA):**
        ```
        MPSA = [(Hb Inicial - Hb Mínima) / Hb Inicial] × Volumen Circulante
        ```
        
        **Fundamento científico:**
        - Estudio con 102 pacientes
        - R² = 49% (modelo multivariado)
        - Nivel de confianza: 95%
        - Variables predictoras: MPSA y Edad
        
        **Limitaciones:**
        - Aplicable a liposucción con técnica superhúmeda
        - Hemoglobina mínima recomendada: 10 g/dL
        - Requiere supervisión anestésica adecuada
        """)

# ============================================================================
# TAB 2: FÓRMULA DE ROHRICH
# ============================================================================
with tab2:
    st.markdown('<h2 class="tab-header">Fórmula de Rohrich</h2>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #6c757d; margin-bottom: 2rem;">Evaluación del balance hídrico en liposucción tipo súper húmeda</p>', unsafe_allow_html=True)
    
    # Inputs
    col1, col2 = st.columns(2)
    
    with col1:
        total_aspirate = st.number_input(
            "Aspirado Total (AT)",
            min_value=0,
            max_value=10000,
            value=3000,
            step=100,
            help="Volumen total de grasa aspirada en cc",
            key="aspirate"
        )
        
        liquid_infiltrated = st.number_input(
            "Líquido Infiltrado (LI)",
            min_value=0,
            max_value=20000,
            value=3000,
            step=100,
            help="Volumen infiltrado por el cirujano en cc",
            key="infiltrated"
        )
    
    with col2:
        endovenous_liquid = st.number_input(
            "Líquido Endovenoso (LE)",
            min_value=0,
            max_value=10000,
            value=1500,
            step=100,
            help="Volumen administrado por vía IV en cc",
            key="endovenous"
        )
    
    # Botón de cálculo
    if st.button("CALCULAR RATIO", use_container_width=True, key="calc_rohrich"):
        if total_aspirate > 0:
            # Calcular líquidos administrados totales
            total_liquids = endovenous_liquid + liquid_infiltrated
            ratio = total_liquids / total_aspirate
            
            # Determinar ratio recomendado (versión simplificada de la app Manzaneda)
            if total_aspirate < 5000:
                recommended_ratio = 1.8
                formula_text = "AT × 1.8 = LI + LE"
            else:
                recommended_ratio = 1.2
                formula_text = "AT × 1.2 = LI + LE"
            
            # Calcular líquidos recomendados totales
            recommended_total = recommended_ratio * total_aspirate
            
            # Mostrar resultados
            st.markdown('<div class="result-container">', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Ratio Calculado", f"{ratio:.2f}")
            
            with col2:
                st.metric("Ratio Recomendado", f"{recommended_ratio:.1f}")
            
            with col3:
                st.metric("Líquidos Recomendados", f"{recommended_total:.0f} cc")
            
            # Mostrar fórmula aplicada
            st.markdown(f'<div class="info-box">📐 <strong>Fórmula aplicada:</strong> {formula_text}</div>', unsafe_allow_html=True)
            
            # Evaluación del balance hídrico
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
                st.markdown(f"""
                **Cálculo del Ratio Actual:**
                - Líquido Infiltrado (LI): {liquid_infiltrated:,} cc
                - Líquido Endovenoso (LE): {endovenous_liquid:,} cc
                - **Líquido Total Administrado:** {liquid_infiltrated:,} + {endovenous_liquid:,} = **{total_liquids:,} cc**
                - Aspirado Total (AT): {total_aspirate:,} cc
                - **Ratio Actual:** {total_liquids:,} ÷ {total_aspirate:,} = **{ratio:.2f}**
                
                **Fórmula Aplicada:**
                {formula_text}
                
                **Líquidos Recomendados:**
                - {recommended_ratio} × {total_aspirate:,} = **{recommended_total:,.0f} cc**
                
                **Evaluación:**
                - Líquidos administrados: {total_liquids:,} cc
                - Líquidos recomendados: {recommended_total:,.0f} cc
                - **Diferencia:** {total_liquids - recommended_total:+,.0f} cc
                - **Porcentaje de desviación:** {((ratio - recommended_ratio) / recommended_ratio * 100):+.1f}%
                """)
        else:
            st.markdown('<div class="error-box">⚠️ El aspirado total debe ser mayor que 0</div>', unsafe_allow_html=True)
    
    # Información del método
    with st.expander("ℹ️ Información del Método"):
        st.markdown("""
        **Fórmula de Rohrich para Balance Hídrico:**
        
        Esta fórmula sirve para evaluar el balance hídrico de los pacientes que se realizan liposucción tipo súper húmeda.
        
        **Fórmulas aplicadas según volumen aspirado:**
        
        **Para Aspirado Total (AT) < 5000 cc:**
        ```
        AT × 1.8 = LI + LE
        ```
        
        **Para Aspirado Total (AT) ≥ 5000 cc:**
        ```
        AT × 1.2 = LI + LE
        ```
        
        **Donde:**
        - **AT** = Aspirado Total (cc)
        - **LI** = Líquido Infiltrado por el cirujano (cc)
        - **LE** = Líquido Endovenoso administrado (cc)
        
        **Cálculo del Ratio:**
        ```
        Ratio = (Líquido Infiltrado + Líquido Endovenoso) ÷ Aspirado Total
        ```
        
        **Interpretación del Ratio:**
        - **Ratio < Recomendado:** Considerar aumentar líquidos (riesgo de hipovolemia)
        - **Ratio ≈ Recomendado:** Balance hídrico adecuado
        - **Ratio > Recomendado:** Riesgo de sobrecarga hídrica (edema pulmonar)
        
        **Consideraciones importantes:**
        - La técnica superhúmeda utiliza ratio de infiltración 1:1
        - Del líquido infiltrado, 22-29% se recupera en el aspirado
        - El resto pasa a la circulación general
        - Monitorizar diuresis: objetivo 1-1.2 ml/kg/hora
        
        **Referencia:**
        Rohrich RJ, Leedy JE, Swamy JR. Fluid resuscitation in liposuction: a retrospective review of 89 consecutive patients. Plast Reconstr Surg. 2006;117(2):431-436.
        """)

# Footer
st.markdown("""
<div class="footer">
    <p><strong>Referencia:</strong> Manzaneda Cipriani R. et al. Pérdida permisible de grasa en liposucción: fórmula y aplicación informática para cuantificar un nuevo concepto. Cir. plást. iberolatinoam. 2021;47(1):19-28</p>
    <p><em>Herramienta desarrollada para uso profesional en cirugía plástica</em></p>
    <p style="margin-top: 1rem; font-size: 0.75rem; opacity: 0.8;">Basada en la app móvil "Seguridad en Liposucción" por Dr. Raúl Manzaneda Cipriani</p>
</div>
""", unsafe_allow_html=True)
