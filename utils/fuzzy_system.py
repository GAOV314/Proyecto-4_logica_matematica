import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class SistemaBienestarLaboral:
    def __init__(self):
        self._configurar_sistema()
    
    def _configurar_sistema(self):
        """Configura el sistema de lógica difusa completo"""
        # Definir variables de entrada (Antecedentes)
        self.horas_trabajo = ctrl.Antecedent(np.arange(0, 81, 1), 'horas_trabajo')
        self.calidad_sueno = ctrl.Antecedent(np.arange(1, 11, 1), 'calidad_sueno')
        self.carga_mental = ctrl.Antecedent(np.arange(1, 11, 1), 'carga_mental')
        self.satisfaccion = ctrl.Antecedent(np.arange(1, 11, 1), 'satisfaccion')
        
        # Definir variables de salida (Consecuentes)
        self.nivel_estres = ctrl.Consequent(np.arange(0, 101, 1), 'nivel_estres')
        self.productividad = ctrl.Consequent(np.arange(0, 101, 1), 'productividad')
        self.prioridad_accion = ctrl.Consequent(np.arange(1, 11, 1), 'prioridad_accion')
        
        # Configurar funciones de pertenencia
        self._configurar_funciones_pertenencia()
        
        # Crear reglas difusas
        self._crear_reglas()
        
        # Crear sistema de control
        self.sistema_control = ctrl.ControlSystem(self.reglas)
        self.simulador = ctrl.ControlSystemSimulation(self.sistema_control)
    
    def _configurar_funciones_pertenencia(self):
        """Configura las funciones de pertenencia para todas las variables"""
        # Horas de trabajo (0-80) - CORREGIDO
        self.horas_trabajo['bajas'] = fuzz.trapmf(self.horas_trabajo.universe, [0, 0, 30, 45])
        self.horas_trabajo['normales'] = fuzz.trapmf(self.horas_trabajo.universe, [30, 40, 50, 60])
        self.horas_trabajo['altas'] = fuzz.trapmf(self.horas_trabajo.universe, [50, 65, 80, 80])
        
        # Calidad de sueño (1-10) - CORREGIDO para todo el rango
        self.calidad_sueno['mala'] = fuzz.trapmf(self.calidad_sueno.universe, [1, 1, 3, 5])
        self.calidad_sueno['regular'] = fuzz.trapmf(self.calidad_sueno.universe, [3, 4, 6, 7])
        self.calidad_sueno['buena'] = fuzz.trapmf(self.calidad_sueno.universe, [5, 7, 10, 10])
        
        # Carga mental (1-10) - CORREGIDO para todo el rango
        self.carga_mental['leve'] = fuzz.trapmf(self.carga_mental.universe, [1, 1, 3, 5])
        self.carga_mental['moderada'] = fuzz.trapmf(self.carga_mental.universe, [3, 4, 6, 7])
        self.carga_mental['intensa'] = fuzz.trapmf(self.carga_mental.universe, [5, 7, 10, 10])
        
        # Satisfacción laboral (1-10) - CORREGIDO para todo el rango
        self.satisfaccion['baja'] = fuzz.trapmf(self.satisfaccion.universe, [1, 1, 3, 5])
        self.satisfaccion['media'] = fuzz.trapmf(self.satisfaccion.universe, [3, 4, 6, 7])
        self.satisfaccion['alta'] = fuzz.trapmf(self.satisfaccion.universe, [5, 7, 10, 10])
        
        # Nivel de estrés (0-100)
        self.nivel_estres['bajo'] = fuzz.trimf(self.nivel_estres.universe, [0, 0, 40])
        self.nivel_estres['moderado'] = fuzz.trimf(self.nivel_estres.universe, [20, 50, 80])
        self.nivel_estres['alto'] = fuzz.trimf(self.nivel_estres.universe, [60, 100, 100])
        
        # Productividad (0-100)
        self.productividad['baja'] = fuzz.trimf(self.productividad.universe, [0, 0, 50])
        self.productividad['optima'] = fuzz.trimf(self.productividad.universe, [30, 60, 90])
        self.productividad['sobrecargada'] = fuzz.trimf(self.productividad.universe, [70, 100, 100])
        
        # Prioridad de acción (1-10)
        self.prioridad_accion['baja'] = fuzz.trimf(self.prioridad_accion.universe, [1, 1, 5])
        self.prioridad_accion['media'] = fuzz.trimf(self.prioridad_accion.universe, [3, 5, 7])
        self.prioridad_accion['alta'] = fuzz.trimf(self.prioridad_accion.universe, [5, 10, 10])
    
    def _crear_reglas(self):
        """Crea las reglas difusas del sistema"""
        self.reglas = []
        
        # REGLAS PARA ESTRÉS ALTO - Casos extremos
        self.reglas.append(ctrl.Rule(
            self.satisfaccion['baja'] | self.calidad_sueno['mala'] | 
            self.carga_mental['intensa'] | self.horas_trabajo['altas'],
            self.nivel_estres['alto']
        ))
        
        # REGLAS PARA ESTRÉS MODERADO - Combinaciones comunes
        self.reglas.append(ctrl.Rule(
            (self.horas_trabajo['normales'] & self.carga_mental['moderada']) |
            (self.calidad_sueno['regular'] & self.satisfaccion['media']) |
            (self.horas_trabajo['altas'] & self.satisfaccion['alta']),
            self.nivel_estres['moderado']
        ))
        
        # REGLAS PARA ESTRÉS BAJO - Condiciones ideales
        self.reglas.append(ctrl.Rule(
            self.horas_trabajo['bajas'] & self.calidad_sueno['buena'] & 
            self.carga_mental['leve'] & self.satisfaccion['alta'],
            self.nivel_estres['bajo']
        ))
        
        # REGLAS DE PRODUCTIVIDAD
        self.reglas.append(ctrl.Rule(
            self.nivel_estres['bajo'] | self.satisfaccion['alta'], 
            self.productividad['optima']
        ))
        self.reglas.append(ctrl.Rule(
            self.nivel_estres['alto'] | self.calidad_sueno['mala'], 
            self.productividad['baja']
        ))
        self.reglas.append(ctrl.Rule(
            self.nivel_estres['moderado'] & self.horas_trabajo['altas'], 
            self.productividad['sobrecargada']
        ))
        
        # REGLAS DE PRIORIDAD
        self.reglas.append(ctrl.Rule(
            self.nivel_estres['alto'] | self.productividad['baja'], 
            self.prioridad_accion['alta']
        ))
        self.reglas.append(ctrl.Rule(
            self.nivel_estres['moderado'] | self.satisfaccion['baja'], 
            self.prioridad_accion['media']
        ))
        self.reglas.append(ctrl.Rule(
            self.nivel_estres['bajo'] & self.productividad['optima'], 
            self.prioridad_accion['baja']
        ))
        
        # REGLAS DE FALLBACK CRÍTICAS - Para asegurar que siempre haya salida
        self.reglas.append(ctrl.Rule(
            self.calidad_sueno['mala'] | self.satisfaccion['baja'], 
            self.prioridad_accion['media']
        ))
        self.reglas.append(ctrl.Rule(
            self.horas_trabajo['normales'], 
            self.nivel_estres['moderado']
        ))
    
    def diagnosticar(self, horas, sueno, carga, satisf):
        """Realiza diagnóstico completo con manejo de errores mejorado"""
        try:
            # Validar rangos de entrada
            horas = max(0, min(80, horas))
            sueno = max(1, min(10, sueno))
            carga = max(1, min(10, carga))
            satisf = max(1, min(10, satisf))
            
            self.simulador.input['horas_trabajo'] = horas
            self.simulador.input['calidad_sueno'] = sueno
            self.simulador.input['carga_mental'] = carga
            self.simulador.input['satisfaccion'] = satisf
            
            self.simulador.compute()
            
            return {
                'nivel_estres': self.simulador.output['nivel_estres'],
                'productividad': self.simulador.output['productividad'],
                'prioridad_accion': self.simulador.output['prioridad_accion'],
                'recomendaciones': self._generar_recomendaciones(
                    self.simulador.output['nivel_estres'],
                    self.simulador.output['productividad'],
                    self.simulador.output['prioridad_accion']
                )
            }
        except Exception as e:
            # Fallback: cálculo manual si el sistema difuso falla
            return self._diagnostico_manual(horas, sueno, carga, satisf, str(e))

    def _diagnostico_manual(self, horas, sueno, carga, satisf, error_msg):
        """Cálculo manual de respaldo cuando el sistema difuso falla"""
        
        # Cálculos simples basados en lógica lineal
        nivel_estres = (
            (horas / 80 * 30) + 
            ((10 - sueno) / 10 * 30) + 
            (carga / 10 * 30) + 
            ((10 - satisf) / 10 * 10)
        )
        
        productividad = max(20, 100 - nivel_estres + 15)
        prioridad_accion = (nivel_estres / 100) * 8 + 2
        
        # Asegurar rangos válidos
        nivel_estres = max(0, min(100, nivel_estres))
        productividad = max(0, min(100, productividad))
        prioridad_accion = max(1, min(10, prioridad_accion))
        
        return {
            'nivel_estres': nivel_estres,
            'productividad': productividad,
            'prioridad_accion': prioridad_accion,
            'recomendaciones': self._generar_recomendaciones(nivel_estres, productividad, prioridad_accion),
            'advertencia': f"Sistema difuso temporalmente no disponible. {error_msg}"
        }
    
    def _generar_recomendaciones(self, estres, productividad, prioridad):
        """Genera recomendaciones basadas en los resultados del diagnóstico"""
        recomendaciones = []
        
        # Recomendaciones por nivel de estrés
        if estres > 70:
            recomendaciones.extend([
                {"tipo": "🚨 CRÍTICO", "mensaje": "Nivel de estrés crítico detectado", "accion": "Consulta inmediata con profesional"},
                {"tipo": "🩺 SALUD", "mensaje": "Considerar días de descanso urgentes", "accion": "Coordinar con RRHH"},
                {"tipo": "⚖️ CARGA", "mensaje": "Revisión urgente de carga laboral", "accion": "Hablar con supervisor"}
            ])
        elif estres > 40:
            recomendaciones.extend([
                {"tipo": "⚠️ ALERTA", "mensaje": "Estrés moderado - atención requerida", "accion": "Implementar técnicas de relajación"},
                {"tipo": "😴 SUEÑO", "mensaje": "Mejorar higiene de sueño", "accion": "Establecer rutina nocturna"},
                {"tipo": "⏰ LÍMITES", "mensaje": "Establecer límites laborales claros", "accion": "Definir horarios de desconexión"}
            ])
        else:
            recomendaciones.append({
                "tipo": "✅ ÓPTIMO", 
                "mensaje": "Nivel de estrés saludable", 
                "accion": "Mantener buenos hábitos actuales"
            })
        
        # Recomendaciones por productividad
        if productividad < 50:
            recomendaciones.extend([
                {"tipo": "📉 PRODUCTIVIDAD", "mensaje": "Productividad por debajo del óptimo", "accion": "Revisar distribución de tareas"},
                {"tipo": "🎯 ENFOQUE", "mensaje": "Implementar técnicas de concentración", "accion": "Usar método Pomodoro"},
                {"tipo": "🚫 DISTRACCIONES", "mensaje": "Identificar y eliminar distracciones", "accion": "Bloquear notificaciones innecesarias"}
            ])
        elif productividad > 80:
            recomendaciones.append({
                "tipo": "🔥 SOBRECARGA", 
                "mensaje": "Productividad muy alta - riesgo de burnout", 
                "accion": "Evaluar sostenibilidad del ritmo"
            })
        
        # Recomendación por prioridad
        if prioridad > 7:
            recomendaciones.append({
                "tipo": "🎯 PRIORIDAD", 
                "mensaje": "ACCIÓN INMEDIATA REQUERIDA", 
                "accion": "Implementar recomendaciones urgentemente"
            })
        
        return recomendaciones
