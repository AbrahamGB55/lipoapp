import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="Permissible Fat Loss Calculator",
    page_icon="🏥",
    layout="centered"
)

# CSS personalizado para estilo similar a la app
st.markdown("""
<style>
    .stApp {
        max-width: 500px;
        margin: 0 auto;
    }
    .main-header {
        text-align: center;
        color: #2c5282;
        margin-bottom: 2rem;
    }
    .result-box {
        background-color: #e6f3ff;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
    }
    .formula-box {
        background-color: #f0f0f0;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-size: 0.9rem;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Tabs para las dos calculadoras
tab1, tab2 = st.tabs(["💉 Permissible Fat Loss", "💧 Rohrich Formula"])

# Tab 1: Permissible Fat Loss Calculator
with tab1:
    st.markdown("<h1 class='main-header'>Permissible Fat Loss</h1>", unsafe_allow_html=True)
    
    # Formulario principal
    with st.container():
        # Peso
        weight = st.number_input(
            "Enter your weight (kg)",
            min_value=40.0,
            max_value=200.0,
            value=70.0,
            step=0.5,
            key="weight"
        )
        
        # Género
        gender = st.selectbox(
            "Gender",
            ["Male", "Female"],
            key="gender"
        )
        
        # Volumen circulante
        st.markdown("**Circulating Volume**")
        if st.checkbox("Use simplified method", value=True):
            if gender == "Male":
                circulating_volume = weight * 75
            else:
                circulating_volume = weight * 65
        else:
            # Altura para cálculo de Nadler
            height = st.number_input(
                "Enter your height (cm)",
                min_value=140.0,
                max_value=220.0,
                value=170.0,
                step=1.0
            )
            if gender == "Male":
                circulating_volume = (0.006012 * (height ** 3)) / (14.6 * weight) + 604
            else:
                circulating_volume = (0.005835 * (height ** 3)) / (15 * weight) + 183
        
        st.info(f"Circulating Volume: **{circulating_volume:.0f} ml**")
        
        # Hemoglobina mínima
        min_hemoglobin = st.number_input(
            "Minimum Hemoglobin (g/dL)",
            min_value=7.0,
            max_value=12.0,
            value=10.0,
            step=0.1,
            key="min_hb"
        )
        
        # Hemoglobina inicial
        initial_hemoglobin = st.number_input(
            "Initial Hemoglobin (g/dL)",
            min_value=10.0,
            max_value=20.0,
            value=13.0,
            step=0.1,
            key="initial_hb"
        )
        
        # Edad
        age = st.number_input(
            "Enter your age",
            min_value=18,
            max_value=70,
            value=30,
            step=1,
            key="age"
        )
        
        # Botón de cálculo
        if st.button("CALCULATE PERMISSIBLE FAT LOSS", type="primary", use_container_width=True):
            # Calcular pérdida permisible de sangre
            permissible_blood_loss = (initial_hemoglobin - min_hemoglobin) * weight * circulating_volume
            
            # Calcular pérdida permisible de grasa con el modelo múltiple (más preciso)
            permissible_fat_loss = 383.725 + 3.406 * permissible_blood_loss - 29.116 * age
            
            # Mostrar resultados
            st.markdown("<div class='result-box'>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(
                    "Permissible Blood Loss",
                    f"{permissible_blood_loss:.0f} ml",
                    help="Maximum safe blood loss"
                )
            
            with col2:
                st.metric(
                    "Permissible Fat Loss",
                    f"{permissible_fat_loss:.0f} ml",
                    help="Maximum fat that can be aspirated"
                )
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Advertencia si es mayor a 5000ml
            if permissible_fat_loss > 5000:
                st.warning("⚠️ Volume > 5000 ml. Procedure should be performed in a facility with ICU.")
    
    # Fórmula predictiva
    with st.expander("📐 Predictive formula"):
        st.markdown("""
        This predictive formula is made for the exclusive use of plastic surgeons. 
        The plastic surgeon can have with this application an approach:
        
        **Formula used:**
        ```
        Fat Loss = 383.725 + 3.406 × MPSA - 29.116 × age
        ```
        
        Where MPSA = (Initial Hb - Minimum Hb) × Weight × Blood Volume
        """)

# Tab 2: Rohrich Formula
with tab2:
    st.markdown("<h1 class='main-header'>Rohrich Formula</h1>", unsafe_allow_html=True)
    
    # Entradas para la fórmula de Rohrich
    total_aspirate = st.number_input(
        "Total Aspirate (ml)",
        min_value=0,
        max_value=10000,
        value=3000,
        step=100,
        key="aspirate"
    )
    
    liquid_infiltrated = st.number_input(
        "Liquid infiltrated by the surgeon (ml)",
        min_value=0,
        max_value=20000,
        value=3000,
        step=100,
        key="infiltrated"
    )
    
    endovenous_liquid = st.number_input(
        "Endovenous liquid (ml)",
        min_value=0,
        max_value=10000,
        value=1500,
        step=100,
        key="iv"
    )
    
    # Botón de cálculo
    if st.button("GET RESULT", type="primary", use_container_width=True):
        if total_aspirate > 0:
            # Calcular ratio
            ratio = (endovenous_liquid + liquid_infiltrated) / total_aspirate
            
            # Determinar ratio recomendado
            if total_aspirate < 5000:
                recommended_ratio = 1.8
            else:
                recommended_ratio = 1.2
            
            # Mostrar resultado
            st.markdown("<div class='result-box'>", unsafe_allow_html=True)
            st.metric("Fluid Ratio", f"{ratio:.2f}")
            st.metric("Recommended Ratio", f"{recommended_ratio:.1f}")
            
            # Evaluación
            if ratio < recommended_ratio * 0.9:
                st.error("⚠️ Insufficient fluid ratio. Consider increasing IV fluids.")
            elif ratio > recommended_ratio * 1.1:
                st.warning("⚠️ High fluid ratio. Risk of fluid overload.")
            else:
                st.success("✅ Adequate fluid ratio.")
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Información de la fórmula
    st.markdown("<div class='formula-box'>", unsafe_allow_html=True)
    st.markdown("""
    **This formula is used to evaluate the hydric balance of patients who undergo Super Wet type liposuction.**
    
    Formula:
    - To an AT < 5000 ml applies → (AT × 1.8 = LI + LE)
    - To an AT ≥ 5000 ml applies → (AT × 1.2 = LI + LE)
    
    Where:
    - AT = total aspirate
    - LI = infiltrated liquid
    - LE = intravenous fluid
    
    *Rohrich RJ, Jason E, Leedy, Swamy JR. Fluid resuscitation in liposuction: 
    a retrospective review of 89 consecutive patients. Plast Reconstr Surg. 2006; 117:431-6*
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("Based on: Manzaneda Cipriani R. et al. Cir. plást. iberolatinoam. 2021;47(1):19-28")
