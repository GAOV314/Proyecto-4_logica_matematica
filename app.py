import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
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
    page_title="Sistema de Bienestar Laboral",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
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
st.markdown('<h1 class="main-header">💼 Sistema de Bienestar Laboral Inteligente</h1>', unsafe_allow_html=True)

# Sidebar para navegación
st.sidebar.title("🔍 Navegación")
modo = st.sidebar.radio("Selecciona el modo:", ["Diagnóstico Individual", "Análisis de Equipo", "Dashboard General"])

if modo == "Diagnóstico Individual":
    st.header("🎯 Diagnóstico Individual")
    
    # Formulario de entrada
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
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Recomendaciones - VERSIÓN MEJORADA
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
                        <strong>{rec['mensaje']}</strong><br>
                        <span style="color: #666; font-size: 0.9rem;">
                        📝 <em>Acción recomendada:</em> {rec['accion']}
                        </span>
                    </div>
                    """, unsafe_allow_html=True)

elif modo == "Análisis de Equipo":
    st.header("👥 Análisis de Equipo")
    
    st.info("""
    **Funcionalidad para managers y RRHH:**
    Sube un CSV con datos del equipo o ingrésalos manualmente para obtener un análisis grupal.
    """)
    
    # Opción de carga de archivo
    archivo = st.file_uploader("Subir CSV con datos del equipo", type=['csv'])
    
    if archivo is not None:
        datos_equipo = pd.read_csv(archivo)
        st.write("Datos cargados:", datos_equipo.head())
    else:
        # Datos de ejemplo
        st.subheader("Ingresar Datos Manualmente")
        num_empleados = st.number_input("Número de empleados:", min_value=1, max_value=20, value=3)
        
        datos_equipo = []
        for i in range(num_empleados):
            st.write(f"--- Empleado {i+1} ---")
            col1, col2 = st.columns(2)
            with col1:
                nombre = st.text_input(f"Nombre", value=f"Empleado {i+1}", key=f"nombre_{i}")
                horas = st.slider(f"Horas", 0, 80, 40, key=f"horas_{i}")
            with col2:
                sueno = st.slider(f"Sueño", 1, 10, 6, key=f"sueno_{i}")
                carga = st.slider(f"Carga", 1, 10, 5, key=f"carga_{i}")
                satisf = st.slider(f"Satisfacción", 1, 10, 7, key=f"satisf_{i}")
            
            datos_equipo.append({
                'nombre': nombre,
                'horas_trabajo': horas,
                'calidad_sueno': sueno,
                'carga_mental': carga,
                'satisfaccion': satisf
            })
        
        datos_equipo = pd.DataFrame(datos_equipo)
    
    if st.button("📊 Analizar Equipo") and not datos_equipo.empty:
        # Realizar diagnósticos para cada empleado
        resultados = []
        for _, empleado in datos_equipo.iterrows():
            diag = sistema.diagnosticar(
                empleado['horas_trabajo'],
                empleado['calidad_sueno'],
                empleado['carga_mental'],
                empleado['satisfaccion']
            )
            if 'error' not in diag:
                resultados.append({
                    'nombre': empleado['nombre'],
                    'estres': diag['nivel_estres'],
                    'productividad': diag['productividad'],
                    'prioridad': diag['prioridad_accion']
                })
        
        if resultados:
            df_resultados = pd.DataFrame(resultados)
            
            # Mostrar tabla de resultados
            st.subheader("📋 Resultados del Equipo")
            st.dataframe(df_resultados.style.background_gradient(subset=['estres', 'prioridad']))
            
            # Gráfico de dispersión
            fig = px.scatter(
                df_resultados, 
                x='estres', 
                y='productividad',
                size='prioridad',
                color='prioridad',
                hover_name='nombre',
                title='Estrés vs Productividad del Equipo',
                labels={'estres': 'Nivel de Estrés (%)', 'productividad': 'Productividad (%)'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Identificar casos críticos
            casos_criticos = df_resultados[df_resultados['prioridad'] > 7]
            if not casos_criticos.empty:
                st.warning(f"🚨 Casos que requieren atención inmediata: {', '.join(casos_criticos['nombre'].tolist())}")

else:  # Dashboard General
    st.header("📊 Dashboard General")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📈 Tendencias de Bienestar Laboral")
        
        # Datos de ejemplo para tendencias
        meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
        estres_promedio = [45, 52, 48, 65, 58, 42]
        productividad_promedio = [75, 68, 72, 60, 65, 78]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=meses, y=estres_promedio, name='Estrés Promedio', line=dict(color='red')))
        fig.add_trace(go.Scatter(x=meses, y=productividad_promedio, name='Productividad', line=dict(color='green')))
        
        fig.update_layout(
            title="Evolución Mensual del Bienestar",
            xaxis_title="Mes",
            yaxis_title="Porcentaje (%)",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📋 Estadísticas Rápidas")
        
        st.metric("Diagnósticos Realizados", "1,247", "+15%")
        st.metric("Estrés Promedio", "52%", "-8%")
        st.metric("Productividad Media", "68%", "+5%")
        st.metric("Casos Críticos", "12", "-3")

# Footer
st.markdown("---")
st.markdown(
    "**💡 Consejo:** Este sistema utiliza lógica difusa para proporcionar recomendaciones personalizadas. "
    "Los resultados son orientativos y no sustituyen el consejo profesional."
)