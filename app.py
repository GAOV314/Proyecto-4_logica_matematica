import streamlit as st
import plotly.graph_objects as go
from utils.fuzzy_system import SistemaBienestarLaboral

def get_badge_html(tipo):
    """Genera HTML para badges según el tipo de recomendación"""
    badge_class = "badge-info"  # default
    
    if "CRÍTICO" in tipo or "ALERTA" in tipo:
        badge_class = "badge-critical"
    elif "PRIORIDAD" in tipo or "ATENCIÓN" in tipo:
        badge_class = "badge-warning"
    elif "ÓPTIMO" in tipo or "SALUD" in tipo:
        badge_class = "badge-success"
    
    return f'<span class="badge {badge_class}">{tipo}</span>'

# Configuración de la página
st.set_page_config(
    page_title="Mi Bienestar Laboral",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado mejorado
st.markdown("""
<style>
    /* Header principal */
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Tarjetas de métricas */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #1f77b4;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    .alert-high {
        border-left: 5px solid #ff4b4b !important;
        background: linear-gradient(135deg, #fff5f5 0%, #ffeaea 100%);
    }
    
    .alert-medium {
        border-left: 5px solid #ffa500 !important;
        background: linear-gradient(135deg, #fff9e6 0%, #fff2cc 100%);
    }
    
    .alert-low {
        border-left: 5px solid #00cc96 !important;
        background: linear-gradient(135deg, #f0fff4 0%, #e6ffec 100%);
    }
    
    /* Tarjetas de recomendaciones */
    .recommendation-card {
        background: white;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        border-left: 4px solid #667eea;
    }
    
    .recommendation-critical {
        border-left: 4px solid #ff4b4b;
        background: linear-gradient(135deg, #fff5f5 0%, #ffeaea 100%);
        animation: pulse 2s infinite;
    }
    
    .recommendation-warning {
        border-left: 4px solid #ffa500;
        background: linear-gradient(135deg, #fff9e6 0%, #fff2cc 100%);
    }
    
    /* Animaciones */
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 75, 75, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(255, 75, 75, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 75, 75, 0); }
    }
    
    /* Mejoras para los sliders */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Botones personalizados */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Mejora del sidebar */
    .css-1d391kg {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Títulos de secciones */
    .section-title {
        font-size: 1.5rem;
        color: #333;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #667eea;
        font-weight: 600;
    }
    
    /* Badges para tipos de recomendación */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }
    
    .badge-critical {
        background: #ff4b4b;
        color: white;
    }
    
    .badge-warning {
        background: #ffa500;
        color: white;
    }
    
    .badge-info {
        background: #667eea;
        color: white;
    }
    
    .badge-success {
        background: #00cc96;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar sistema de lógica difusa
@st.cache_resource
def cargar_sistema():
    return SistemaBienestarLaboral()

sistema = cargar_sistema()

# Header principal
st.markdown('<h1 class="main-header">💼 Mi Bienestar Laboral</h1>', unsafe_allow_html=True)

# Formulario de entrada
st.header("🎯 Diagnóstico Personal")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Datos Laborales")
    horas_trabajo = st.slider("Horas de trabajo semanales:", 0, 80, 40, 
                             help="Total de horas trabajadas en la semana")
    carga_mental = st.slider("Nivel de carga mental:", 1, 10, 5,
                            help="1 = Muy baja, 10 = Muy alta")
    satisfaccion = st.slider("Satisfacción laboral:", 1, 10, 7,
                            help="1 = Muy insatisfecho, 10 = Muy satisfecho")

with col2:
    st.subheader("😴 Bienestar Personal")
    calidad_sueno = st.slider("Calidad del sueño:", 1, 10, 6,
                             help="1 = Muy mala, 10 = Excelente")
    
    # Información adicional
    st.info("""
    **Instrucciones:**
    - Evalúa honestamente cada aspecto
    - Considera las últimas 2 semanas
    - Los resultados son confidenciales
    """)

# Botón de diagnóstico
if st.button("🎯 Realizar Diagnóstico", type="primary"):
    with st.spinner("Analizando tu bienestar laboral..."):
        resultado = sistema.diagnosticar(horas_trabajo, calidad_sueno, carga_mental, satisfaccion)
        
        if 'error' in resultado:
            st.error(f"Error en el análisis: {resultado['error']}")
        else:
            # Mostrar métricas principales
            st.success("✅ Diagnóstico completado")
            
            col1, col2, col3 = st.columns(3)
            
            # Determinar clases de alerta
            estres_class = "alert-high" if resultado['nivel_estres'] > 70 else "alert-medium" if resultado['nivel_estres'] > 40 else "alert-low"
            prod_class = "alert-high" if resultado['productividad'] < 50 else "alert-low"
            prior_class = "alert-high" if resultado['prioridad_accion'] > 7 else "alert-medium" if resultado['prioridad_accion'] > 5 else "alert-low"
            
            with col1:
                st.markdown(f'<div class="metric-card {estres_class}">', unsafe_allow_html=True)
                st.metric("Nivel de Estrés", f"{resultado['nivel_estres']:.1f}%")
                st.progress(resultado['nivel_estres'] / 100)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown(f'<div class="metric-card {prod_class}">', unsafe_allow_html=True)
                st.metric("Productividad Estimada", f"{resultado['productividad']:.1f}%")
                st.progress(resultado['productividad'] / 100)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown(f'<div class="metric-card {prior_class}">', unsafe_allow_html=True)
                st.metric("Prioridad de Acción", f"{resultado['prioridad_accion']:.1f}/10")
                st.progress(resultado['prioridad_accion'] / 10)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Gráfico radial
            st.subheader("📈 Perfil de Bienestar")
            categorias = ['Estrés', 'Productividad', 'Sueño', 'Satisfacción', 'Carga Mental']
            valores = [
                resultado['nivel_estres'],
                resultado['productividad'],
                calidad_sueno * 10,  # Escalar a 100
                satisfaccion * 10,   # Escalar a 100
                carga_mental * 10    # Escalar a 100
            ]
            
            fig = go.Figure(data=go.Scatterpolar(
                r=valores,
                theta=categorias,
                fill='toself',
                line=dict(color='#1f77b4')
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )),
                showlegend=False,
                height=400
            )
            
            st.plotly_chart(fig, width='stretch')
            
            # Recomendaciones
            st.markdown('<div class="section-title">💡 Plan de Acción Personalizado</div>', unsafe_allow_html=True)
            
            for rec in resultado['recomendaciones']:
                # Determinar clase CSS según criticidad
                card_class = "recommendation-card"
                if "CRÍTICO" in rec['tipo'] or "PRIORIDAD" in rec['tipo']:
                    card_class = "recommendation-card recommendation-critical"
                elif "ALERTA" in rec['tipo']:
                    card_class = "recommendation-card recommendation-warning"
                
                badge_html = get_badge_html(rec['tipo'])
                
                st.markdown(f"""
                <div class="{card_class}">
                    {badge_html}
                    <strong style="color: #000;">{rec['mensaje']}</strong><br>
                    <span style="color: #000; font-size: 0.9rem;">
                    📝 <em>Acción recomendada:</em> {rec['accion']}
                    </span>
                </div>
                """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    "**💡 Consejo:** Este sistema utiliza lógica difusa para proporcionar recomendaciones personalizadas. "
    "Los resultados son orientativos y no sustituyen el consejo profesional."
)
