import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class SistemaBienestarLaboral:
    def __init__(self):
        self._configurar_sistema()
    
    def _configurar_sistema(self):
        # Variables de entrada
        self.horas_trabajo = ctrl.Antecedent(np.arange(0, 81, 1), 'horas_trabajo')
        self.calidad_sueno = ctrl.Antecedent(np.arange(1, 11, 1), 'calidad_sueno')
        self.carga_mental = ctrl.Antecedent(np.arange(1, 11, 1), 'carga_mental')
        self.satisfaccion = ctrl.Antecedent(np.arange(1, 11, 1), 'satisfaccion')
        
        # Variables de salida
        self.nivel_estres = ctrl.Consequent(np.arange(0, 101, 1), 'nivel_estres')
        self.productividad = ctrl.Consequent(np.arange(0, 101, 1), 'productividad')
        self.prioridad_accion = ctrl.Consequent(np.arange(1, 11, 1), 'prioridad_accion')
        
        # Configurar funciones de pertenencia
        self._configurar_funciones_pertenencia()
        
        # Crear reglas
        self._crear_reglas()
        
        # Sistema de control
        self.sistema = ctrl.ControlSystem(self.reglas)
        self.simulador = ctrl.ControlSystemSimulation(self.sistema)
    
    def _configurar_funciones_pertenencia(self):
        # Horas de trabajo
        self.horas_trabajo['bajas'] = fuzz.trimf(self.horas_trabajo.universe, [0, 0, 40])
        self.horas_trabajo['normales'] = fuzz.trimf(self.horas_trabajo.universe, [35, 45, 55])
        self.horas_trabajo['altas'] = fuzz.trimf(self.horas_trabajo.universe, [50, 80, 80])
        
        # Calidad de sueño
        self.calidad_sueno['mala'] = fuzz.trimf(self.calidad_sueno.universe, [1, 1, 4])
        self.calidad_sueno['regular'] = fuzz.trimf(self.calidad_sueno.universe, [3, 5, 7])
        self.calidad_sueno['buena'] = fuzz.trimf(self.calidad_sueno.universe, [6, 10, 10])
        
        # Carga mental
        self.carga_mental['leve'] = fuzz.trimf(self.carga_mental.universe, [1, 1, 4])
        self.carga_mental['moderada'] = fuzz.trimf(self.carga_mental.universe, [3, 5, 7])
        self.carga_mental['intensa'] = fuzz.trimf(self.carga_mental.universe, [6, 10, 10])
        
        # Satisfacción laboral
        self.satisfaccion['baja'] = fuzz.trimf(self.satisfaccion.universe, [1, 1, 4])
        self.satisfaccion['media'] = fuzz.trimf(self.satisfaccion.universe, [3, 5, 7])
        self.satisfaccion['alta'] = fuzz.trimf(self.satisfaccion.universe, [6, 10, 10])
        
        # Nivel de estrés
        self.nivel_estres['bajo'] = fuzz.trimf(self.nivel_estres.universe, [0, 0, 30])
        self.nivel_estres['moderado'] = fuzz.trimf(self.nivel_estres.universe, [20, 50, 80])
        self.nivel_estres['alto'] = fuzz.trimf(self.nivel_estres.universe, [70, 100, 100])
        
        # Productividad
        self.productividad['baja'] = fuzz.trimf(self.productividad.universe, [0, 0, 40])
        self.productividad['optima'] = fuzz.trimf(self.productividad.universe, [30, 70, 100])
        self.productividad['sobrecargada'] = fuzz.trimf(self.productividad.universe, [80, 100, 100])
        
        # Prioridad de acción
        self.prioridad_accion['baja'] = fuzz.trimf(self.prioridad_accion.universe, [1, 1, 4])
        self.prioridad_accion['media'] = fuzz.trimf(self.prioridad_accion.universe, [3, 5, 7])
        self.prioridad_accion['alta'] = fuzz.trimf(self.prioridad_accion.universe, [6, 10, 10])
    
    def _crear_reglas(self):
        self.reglas = []
        
        # Reglas para ESTRÉS
        self.reglas.append(ctrl.Rule(
            self.horas_trabajo['altas'] & self.calidad_sueno['mala'] & self.carga_mental['intensa'],
            self.nivel_estres['alto']
        ))
        self.reglas.append(ctrl.Rule(
            self.horas_trabajo['normales'] & self.satisfaccion['alta'],
            self.nivel_estres['bajo']
        ))
        self.reglas.append(ctrl.Rule(
            self.carga_mental['intensa'] | self.calidad_sueno['mala'],
            self.nivel_estres['moderado']
        ))
        self.reglas.append(ctrl.Rule(
            self.horas_trabajo['bajas'] & self.satisfaccion['alta'],
            self.nivel_estres['bajo']
        ))
        
        # Reglas para PRODUCTIVIDAD
        self.reglas.append(ctrl.Rule(
            self.nivel_estres['bajo'] & self.satisfaccion['alta'],
            self.productividad['optima']
        ))
        self.reglas.append(ctrl.Rule(
            self.nivel_estres['alto'] & self.calidad_sueno['mala'],
            self.productividad['baja']
        ))
        self.reglas.append(ctrl.Rule(
            self.horas_trabajo['altas'] & self.nivel_estres['moderado'],
            self.productividad['sobrecargada']
        ))
        
        # Reglas para PRIORIDAD
        self.reglas.append(ctrl.Rule(
            self.nivel_estres['alto'] | self.productividad['baja'],
            self.prioridad_accion['alta']
        ))
        self.reglas.append(ctrl.Rule(
            self.nivel_estres['moderado'] & self.productividad['optima'],
            self.prioridad_accion['media']
        ))
        self.reglas.append(ctrl.Rule(
            self.nivel_estres['bajo'] & self.productividad['optima'],
            self.prioridad_accion['baja']
        ))
    
    def diagnosticar(self, horas, sueno, carga, satisf):
        """Realiza diagnóstico completo"""
        try:
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
            return {'error': str(e)}
    
    def _generar_recomendaciones(self, estres, productividad, prioridad):
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