import sys
import csv
import os
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit,
    QTextEdit, QHBoxLayout, QComboBox, QMessageBox, QMenuBar, QAction,
    QDialog, QScrollArea, QSystemTrayIcon, QMenu
)
from PyQt5.QtGui import QIcon, QPixmap, QDesktopServices, QKeySequence, QPainter, QBrush
from PyQt5.QtCore import QUrl, Qt, QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
from fpdf import FPDF
import matplotlib.pyplot as plt

ARCHIVO = "registro_sintomas.csv"
CARPETA_REPORTES = "reportes"

class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Acerca de - Mis alergias y Yo")
        self.setFixedSize(400, 500)
        self.setWindowIcon(QIcon("img/logo.png"))
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Logo
        logo_label = QLabel()
        pixmap = QPixmap("img/logo.png")
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)
        
        # Título
        title_label = QLabel("Mis alergias y Yo")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Descripción
        description = QLabel(
            "Mis alergias y Yo es una aplicación especializada para el seguimiento "
            "integral de alergias medicamentosas por descongestivos nasales (Respibien/Utabon) "
            "tras operación de cornetes nasales.\n\n"
            "📋 Funcionalidades:\n"
            "• Registro completo de síntomas nasales, respiratorios y cutáneos\n"
            "• Control específico de medicamentos (Respibien/Utabon)\n"
            "• Seguimiento detallado de recuperación post-operatoria\n"
            "• Cronología de tiempos de recuperación esperados\n"
            "• Gráficos detallados de evolución en tiempo real\n"
            "• Exportación completa a PDF para consultas médicas\n"
            "• Alertas de seguridad para síntomas severos\n\n"
            "⚠️ IMPORTANTE: Esta aplicación es complementaria al seguimiento médico. "
            "Proporciona información orientativa sobre tiempos de recuperación típicos "
            "pero cada caso es único. En síntomas severos, busca atención médica inmediata.\n\n"
            "La recuperación completa puede tomar de 3-12 semanas dependiendo de "
            "factores individuales y la combinación de tratamientos."
        )
        description.setWordWrap(True)
        description.setStyleSheet("margin: 10px; line-height: 1.4;")
        layout.addWidget(description)
        
        # Enlace a GitHub
        github_label = QLabel()
        github_label.setText('<a href="https://github.com/sapoclay/mis-alergias-y-yo">Ver en GitHub</a>')
        github_label.setOpenExternalLinks(True)
        github_label.setAlignment(Qt.AlignCenter)
        github_label.setStyleSheet("margin: 10px; font-size: 14px;")
        layout.addWidget(github_label)
        
        # Botón cerrar
        close_btn = QPushButton("Cerrar")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

class SintomasApp(QWidget):
    def __init__(self):
        super().__init__()
        self.tray_icon = None
        self.tray_timer = None
        
        self.setWindowTitle("Mis alergias y Yo - Seguimiento Post-Operatorio")
        self.setGeometry(100, 100, 1000, 700)  # Ventana más grande por defecto
        
        # Configuración robusta del icono de la aplicación
        self.configurar_icono_aplicacion()

        # Layout principal
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # Crear menú
        self.create_menu(main_layout)
        
        # Crear área de scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Widget contenedor para el contenido scrolleable
        scroll_widget = QWidget()
        self.layout = QVBoxLayout(scroll_widget)
        
        # Añadir el widget al área de scroll
        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area)

        self.init_ui()
        self.init_csv()
        self.graficar()

    def configurar_icono_aplicacion(self):
        """Configuración robusta del icono para múltiples plataformas"""
        icon_paths = [
            "img/logo.png",
            "./img/logo.png",
            os.path.join(os.path.dirname(__file__), "img", "logo.png")
        ]
        
        app_icon = None
        icon_loaded = False
        
        # Intentar cargar desde diferentes rutas
        for icon_path in icon_paths:
            if os.path.exists(icon_path):
                app_icon = QIcon(icon_path)
                if not app_icon.isNull():
                    icon_loaded = True
                    print(f"✅ Icono cargado correctamente: {icon_path}")
                    break
        
        # Si no se pudo cargar, crear icono por defecto
        if not icon_loaded:
            print("⚠️ Creando icono por defecto")
            app_icon = self.create_default_icon()
        
        # Establecer icono en la aplicación
        if app_icon and not app_icon.isNull():
            self.setWindowIcon(app_icon)
            QApplication.instance().setWindowIcon(app_icon)
            
            # Configurar System Tray Icon para GNOME3
            self.configurar_system_tray(app_icon)
        
        return app_icon

    def configurar_system_tray(self, app_icon):
        """Configurar icono de bandeja del sistema optimizado para GNOME3"""
        try:
            # Verificar si el sistema soporta system tray
            if not QSystemTrayIcon.isSystemTrayAvailable():
                print("⚠️ System tray no disponible en este sistema")
                return
            
            # Crear el icono de bandeja
            self.tray_icon = QSystemTrayIcon(app_icon, self)
            
            # Crear menú contextual para el tray
            tray_menu = QMenu()
            
            # Acción mostrar
            show_action = QAction("Mostrar aplicación", self)
            show_action.triggered.connect(self.show_from_tray)
            tray_menu.addAction(show_action)
            
            # Separador
            tray_menu.addSeparator()
            
            # Acción salir
            quit_action = QAction("Salir", self)
            quit_action.triggered.connect(self.salir_aplicacion)
            tray_menu.addAction(quit_action)
            
            self.tray_icon.setContextMenu(tray_menu)
            
            # Conectar señales
            self.tray_icon.activated.connect(self.tray_icon_activated)
            
            # Mostrar el icono en la bandeja
            self.tray_icon.show()
            
            # Timer para forzar visibilidad en GNOME3
            self.tray_timer = QTimer()
            self.tray_timer.timeout.connect(self.refresh_tray_icon)
            self.tray_timer.start(5000)  # Cada 5 segundos
            
            print("✅ System tray configurado para GNOME3")
            
        except Exception as e:
            print(f"❌ Error configurando system tray: {e}")

    def refresh_tray_icon(self):
        """Refrescar el icono de bandeja periódicamente para GNOME3"""
        if self.tray_icon and self.tray_icon.isVisible():
            # Forzar actualización del tooltip
            self.tray_icon.setToolTip("Mis Alergias y Yo - Seguimiento Post-Operatorio")
            
            # Parar el timer después de 30 segundos para no consumir recursos
            if hasattr(self, 'tray_refresh_count'):
                self.tray_refresh_count += 1
                if self.tray_refresh_count > 6:  # 6 * 5 segundos = 30 segundos
                    self.tray_timer.stop()
            else:
                self.tray_refresh_count = 1

    def tray_icon_activated(self, reason):
        """Manejar activación del icono de bandeja"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_from_tray()
        elif reason == QSystemTrayIcon.Trigger:
            self.show_from_tray()

    def show_from_tray(self):
        """Mostrar la aplicación desde la bandeja del sistema"""
        self.show()
        self.raise_()
        self.activateWindow()

    def closeEvent(self, event):
        """Manejar el cierre de la ventana"""
        if self.tray_icon and self.tray_icon.isVisible():
            # Minimizar a bandeja en lugar de cerrar
            self.hide()
            self.tray_icon.showMessage(
                "Mis Alergias y Yo",
                "La aplicación se ha minimizado a la bandeja del sistema",
                QSystemTrayIcon.Information,
                2000
            )
            event.ignore()
        else:
            event.accept()

    def salir_aplicacion(self):
        """Salir completamente de la aplicación"""
        if self.tray_icon:
            self.tray_icon.hide()
        QApplication.instance().quit()
    
    def create_default_icon(self):
        """Crear un icono por defecto si no se puede cargar el archivo"""
        try:
            # Crear un pixmap de 64x64 con diseño médico
            pixmap = QPixmap(64, 64)
            pixmap.fill(Qt.transparent)
            
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Fondo circular rojo médico
            painter.setBrush(QBrush(Qt.darkRed))
            painter.setPen(Qt.white)
            painter.drawEllipse(8, 8, 48, 48)
            
            # Cruz médica blanca
            painter.setBrush(QBrush(Qt.white))
            painter.drawRect(28, 16, 8, 32)  # vertical
            painter.drawRect(16, 28, 32, 8)  # horizontal
            
            painter.end()
            
            icon = QIcon(pixmap)
            print("🔵 Icono médico por defecto creado")
            return icon
            
        except Exception as e:
            print(f"❌ Error creando icono por defecto: {e}")
            return QIcon()  # Retornar icono vacío
    
    def keyPressEvent(self, event):
        """Manejar eventos de teclado"""
        if event.key() == Qt.Key_F11:
            self.toggle_pantalla_completa()
        elif event.key() == Qt.Key_Escape and self.isFullScreen():
            self.ventana_normal()
        elif event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_S:
            self.guardar_sintomas()
        elif event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_E:
            self.exportar_pdf()
        else:
            super().keyPressEvent(event)
    
    def create_menu(self, main_layout):
        # Crear barra de menú
        menubar = QMenuBar(self)
        main_layout.addWidget(menubar)
        
        # Menú Archivo
        archivo_menu = menubar.addMenu('Archivo')
        
        # Acción Guardar
        guardar_action = QAction('Guardar síntomas', self)
        guardar_action.setShortcut('Ctrl+S')
        guardar_action.triggered.connect(self.guardar_sintomas)
        archivo_menu.addAction(guardar_action)
        
        # Acción Exportar
        exportar_action = QAction('Exportar a PDF', self)
        exportar_action.setShortcut('Ctrl+E')
        exportar_action.triggered.connect(self.exportar_pdf)
        archivo_menu.addAction(exportar_action)
        
        archivo_menu.addSeparator()
        
        # Acción Salir
        salir_action = QAction('Salir', self)
        salir_action.setShortcut('Ctrl+Q')
        salir_action.triggered.connect(self.salir_aplicacion)
        archivo_menu.addAction(salir_action)
        
        # Menú Ver
        ver_menu = menubar.addMenu('Ver')
        
        # Acción Pantalla completa
        pantalla_completa_action = QAction('Pantalla completa', self)
        pantalla_completa_action.setShortcut('F11')
        pantalla_completa_action.triggered.connect(self.toggle_pantalla_completa)
        ver_menu.addAction(pantalla_completa_action)
        
        # Acción Ventana normal
        ventana_normal_action = QAction('Ventana normal', self)
        ventana_normal_action.setShortcut('Escape')
        ventana_normal_action.triggered.connect(self.ventana_normal)
        ver_menu.addAction(ventana_normal_action)
        
        # Menú Ayuda
        ayuda_menu = menubar.addMenu('Ayuda')
        
        # Acción About
        about_action = QAction('Acerca de...', self)
        about_action.triggered.connect(self.mostrar_about)
        ayuda_menu.addAction(about_action)
    
    def toggle_pantalla_completa(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
    
    def ventana_normal(self):
        if self.isFullScreen():
            self.showNormal()
    
    def mostrar_about(self):
        dialog = AboutDialog()
        dialog.exec_()

    def init_ui(self):
        self.label_info = QLabel("Mis alergias y Yo - Seguimiento de recuperación post-operatoria:")
        self.label_info.setStyleSheet("font-weight: bold; font-size: 16px; margin: 15px 0; color: #2c3e50; text-align: center;")
        self.layout.addWidget(self.label_info)

        # Sección de síntomas nasales básicos
        nasal_label = QLabel("📋 Síntomas Nasales:")
        nasal_label.setStyleSheet("font-weight: bold; color: #2c3e50; margin-top: 15px;")
        self.layout.addWidget(nasal_label)

        self.congestion_input = QLineEdit()
        self.congestion_input.setPlaceholderText("Congestión nasal (0-10)")
        self.layout.addWidget(self.congestion_input)

        self.picor_input = QLineEdit()
        self.picor_input.setPlaceholderText("Picor nasal (0-10)")
        self.layout.addWidget(self.picor_input)

        self.dolor_input = QComboBox()
        self.dolor_input.addItems(["no", "leve", "moderado", "severo"])
        self.layout.addWidget(QLabel("Dolor nasal/facial:"))
        self.layout.addWidget(self.dolor_input)

        self.secrecion_input = QComboBox()
        self.secrecion_input.addItems(["no", "clara", "espesa", "sanguinolenta"])
        self.layout.addWidget(QLabel("Tipo de secreción nasal:"))
        self.layout.addWidget(self.secrecion_input)

        # Sección de síntomas respiratorios
        resp_label = QLabel("🫁 Síntomas Respiratorios:")
        resp_label.setStyleSheet("font-weight: bold; color: #2c3e50; margin-top: 15px;")
        self.layout.addWidget(resp_label)

        self.dificultad_respirar = QComboBox()
        self.dificultad_respirar.addItems(["no", "leve", "moderada", "severa"])
        self.layout.addWidget(QLabel("Dificultad para respirar:"))
        self.layout.addWidget(self.dificultad_respirar)

        self.tos_input = QComboBox()
        self.tos_input.addItems(["no", "seca", "con flemas", "persistente"])
        self.layout.addWidget(QLabel("Tos:"))
        self.layout.addWidget(self.tos_input)

        self.estornudos_input = QLineEdit()
        self.estornudos_input.setPlaceholderText("Frecuencia de estornudos (0-10)")
        self.layout.addWidget(self.estornudos_input)

        # Sección de síntomas cutáneos (importantes en alergias medicamentosas)
        skin_label = QLabel("🌡️ Síntomas Cutáneos:")
        skin_label.setStyleSheet("font-weight: bold; color: #2c3e50; margin-top: 15px;")
        self.layout.addWidget(skin_label)

        self.erupciones_input = QComboBox()
        self.erupciones_input.addItems(["no", "leves", "moderadas", "severas"])
        self.layout.addWidget(QLabel("Erupciones cutáneas:"))
        self.layout.addWidget(self.erupciones_input)

        self.urticaria_input = QComboBox()
        self.urticaria_input.addItems(["no", "localizada", "generalizada"])
        self.layout.addWidget(QLabel("Urticaria:"))
        self.layout.addWidget(self.urticaria_input)

        self.hinchazón_input = QComboBox()
        self.hinchazón_input.addItems(["no", "facial", "labios/ojos", "generalizada"])
        self.layout.addWidget(QLabel("Hinchazón:"))
        self.layout.addWidget(self.hinchazón_input)

        # Sección específica de medicamentos
        med_label = QLabel("💊 Control de Medicamentos:")
        med_label.setStyleSheet("font-weight: bold; color: #2c3e50; margin-top: 15px;")
        self.layout.addWidget(med_label)

        self.respibien_suspendido = QComboBox()
        self.respibien_suspendido.addItems(["no", "sí - hoy", "sí - hace 1 día", "sí - hace 2-3 días", "sí - hace >3 días"])
        self.layout.addWidget(QLabel("¿Respibien suspendido?:"))
        self.layout.addWidget(self.respibien_suspendido)

        self.utabon_suspendido = QComboBox()
        self.utabon_suspendido.addItems(["no", "sí - hoy", "sí - hace 1 día", "sí - hace 2-3 días", "sí - hace >3 días"])
        self.layout.addWidget(QLabel("¿Utabon suspendido?:"))
        self.layout.addWidget(self.utabon_suspendido)

        self.otros_medicamentos = QLineEdit()
        self.otros_medicamentos.setPlaceholderText("Otros medicamentos tomados hoy")
        self.layout.addWidget(QLabel("Otros medicamentos:"))
        self.layout.addWidget(self.otros_medicamentos)

        # Sección de recuperación post-operatoria
        postop_label = QLabel("🏥 Estado Post-Operatorio:")
        postop_label.setStyleSheet("font-weight: bold; color: #2c3e50; margin-top: 15px;")
        self.layout.addWidget(postop_label)

        self.dias_postop = QLineEdit()
        self.dias_postop.setPlaceholderText("Días desde la operación de cornetes")
        self.layout.addWidget(self.dias_postop)

        self.mejoria_respiracion = QComboBox()
        self.mejoria_respiracion.addItems(["sin cambios", "ligeramente mejor", "mucho mejor", "empeorando"])
        self.layout.addWidget(QLabel("Mejoría respiratoria vs pre-operación:"))
        self.layout.addWidget(self.mejoria_respiracion)

        self.notas_input = QTextEdit()
        self.notas_input.setPlaceholderText("Notas adicionales, síntomas específicos, observaciones...")
        self.layout.addWidget(QLabel("Notas adicionales:"))
        self.layout.addWidget(self.notas_input)

        self.curacion_info = QLabel(
            "⚠️ INFORMACIÓN IMPORTANTE - TIEMPOS DE RECUPERACIÓN:\n\n"
            "🔸 SUSPENSIÓN DE DESCONGESTIVOS NASALES (Respibien/Utabon):\n"
            "• Días 1-3: Puede empeorar temporalmente la congestión (efecto rebote)\n"
            "• Días 4-7: Gradual mejoría de la respiración nasal\n"
            "• Días 8-14: Normalización progresiva de la mucosa nasal\n"
            "• Semanas 3-4: Recuperación completa de la función nasal\n\n"
            "🔸 RECUPERACIÓN POST-OPERACIÓN CORNETES:\n"
            "• Días 1-7: Inflamación máxima, respiración limitada\n"
            "• Semanas 2-3: Reducción de inflamación, mejora gradual\n"
            "• Semanas 4-6: Cicatrización completa, respiración mejorada\n"
            "• Meses 2-3: Resultado final estabilizado\n\n"
            "🔸 ALERGIA MEDICAMENTOSA:\n"
            "• Días 1-3: Eliminación del medicamento del organismo\n"
            "• Días 4-10: Reducción de síntomas alérgicos\n"
            "• Semanas 2-4: Resolución completa de la reacción alérgica\n\n"
            "🚨 CONSULTA INMEDIATA si experimentas: dificultad respiratoria severa, "
            "hinchazón facial, urticaria generalizada o empeoramiento tras 7 días de suspensión."
        )
        self.curacion_info.setStyleSheet(
            "background-color: #e8f4fd; border: 2px solid #3498db; "
            "padding: 15px; border-radius: 8px; margin: 15px 0; "
            "font-size: 11px; line-height: 1.3;"
        )
        self.curacion_info.setWordWrap(True)
        self.layout.addWidget(self.curacion_info)

        self.guardar_btn = QPushButton("Guardar síntomas")
        self.guardar_btn.clicked.connect(self.guardar_sintomas)
        self.layout.addWidget(self.guardar_btn)

        self.exportar_btn = QPushButton("Exportar historial a PDF")
        self.exportar_btn.clicked.connect(self.exportar_pdf)
        self.layout.addWidget(self.exportar_btn)

        self.figure = Figure(figsize=(12, 8))  # Gráfico más grande
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setMinimumHeight(400)  # Altura mínima para el gráfico
        self.layout.addWidget(self.canvas)

    def init_csv(self):
        if not os.path.exists(ARCHIVO):
            with open(ARCHIVO, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    "Fecha", "Congestion", "Picor", "Dolor", "Secrecion", 
                    "Dificultad_Respirar", "Tos", "Estornudos", "Erupciones", 
                    "Urticaria", "Hinchazón", "Respibien_Suspendido", 
                    "Utabon_Suspendido", "Otros_Medicamentos", "Dias_PostOp", 
                    "Mejoria_Respiracion", "Notas"
                ])

    def guardar_sintomas(self):
        try:
            fecha = datetime.now().strftime("%d-%m-%Y")
            congestion = int(self.congestion_input.text()) if self.congestion_input.text() else 0
            picor = int(self.picor_input.text()) if self.picor_input.text() else 0
            estornudos = int(self.estornudos_input.text()) if self.estornudos_input.text() else 0
            dias_postop = int(self.dias_postop.text()) if self.dias_postop.text() else 0
        except ValueError:
            QMessageBox.warning(self, "Error", "Los campos numéricos deben contener valores válidos entre 0 y 10.")
            return

        # Recolectar todos los datos
        dolor = self.dolor_input.currentText()
        secrecion = self.secrecion_input.currentText()
        dificultad_respirar = self.dificultad_respirar.currentText()
        tos = self.tos_input.currentText()
        erupciones = self.erupciones_input.currentText()
        urticaria = self.urticaria_input.currentText()
        hinchazón = self.hinchazón_input.currentText()
        respibien_suspendido = self.respibien_suspendido.currentText()
        utabon_suspendido = self.utabon_suspendido.currentText()
        otros_medicamentos = self.otros_medicamentos.text()
        mejoria_respiracion = self.mejoria_respiracion.currentText()
        notas = self.notas_input.toPlainText()

        # Validar campos críticos
        if respibien_suspendido == "no" and utabon_suspendido == "no":
            reply = QMessageBox.question(self, "Advertencia", 
                "¿Sigues tomando ambos medicamentos (Respibien y Utabon)? Si tienes síntomas de alergia, considera consultar con tu médico sobre suspenderlos.",
                QMessageBox.Yes | QMessageBox.No)
            if reply != QMessageBox.Yes:
                return

        with open(ARCHIVO, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                fecha, congestion, picor, dolor, secrecion,
                dificultad_respirar, tos, estornudos, erupciones,
                urticaria, hinchazón, respibien_suspendido,
                utabon_suspendido, otros_medicamentos, dias_postop,
                mejoria_respiracion, notas
            ])

        QMessageBox.information(self, "Éxito", "Registro guardado correctamente.")

        # Limpiar campos
        self.congestion_input.clear()
        self.picor_input.clear()
        self.estornudos_input.clear()
        self.otros_medicamentos.clear()
        self.dias_postop.clear()
        self.notas_input.clear()
        self.graficar()

    def graficar(self):
        self.figure.clear()
        
        try:
            df = pd.read_csv(ARCHIVO)
            if df.empty:
                ax = self.figure.add_subplot(111)
                ax.text(0.5, 0.5, "No hay datos para mostrar", ha='center', va='center')
                self.canvas.draw()
                return
                
            df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d-%m-%Y')
            df.sort_values(by='Fecha', inplace=True)
            
            # Crear subgráficos
            ax1 = self.figure.add_subplot(2, 2, 1)
            ax2 = self.figure.add_subplot(2, 2, 2)
            ax3 = self.figure.add_subplot(2, 2, 3)
            ax4 = self.figure.add_subplot(2, 2, 4)
            
            # Gráfico 1: Síntomas nasales principales
            ax1.plot(df['Fecha'], df['Congestion'], marker='o', label='Congestión', color='red')
            ax1.plot(df['Fecha'], df['Picor'], marker='s', label='Picor', color='orange')
            if 'Estornudos' in df.columns:
                ax1.plot(df['Fecha'], df['Estornudos'], marker='^', label='Estornudos', color='blue')
            ax1.set_title("Síntomas Nasales")
            ax1.set_ylabel("Intensidad (0-10)")
            ax1.legend(fontsize=8)
            ax1.tick_params(axis='x', rotation=45, labelsize=8)
            
            # Gráfico 2: Estado de medicamentos (días desde suspensión)
            respibien_days = []
            utabon_days = []
            
            for _, row in df.iterrows():
                # Convertir texto de suspensión a días
                resp_val = 0
                uta_val = 0
                
                if 'Respibien_Suspendido' in df.columns:
                    resp_text = str(row['Respibien_Suspendido'])
                    if 'hoy' in resp_text: resp_val = 0
                    elif '1 día' in resp_text: resp_val = 1
                    elif '2-3 días' in resp_text: resp_val = 2.5
                    elif '>3 días' in resp_text: resp_val = 5
                    
                if 'Utabon_Suspendido' in df.columns:
                    uta_text = str(row['Utabon_Suspendido'])
                    if 'hoy' in uta_text: uta_val = 0
                    elif '1 día' in uta_text: uta_val = 1
                    elif '2-3 días' in uta_text: uta_val = 2.5
                    elif '>3 días' in uta_text: uta_val = 5
                    
                respibien_days.append(resp_val)
                utabon_days.append(uta_val)
            
            ax2.plot(df['Fecha'], respibien_days, marker='o', label='Respibien', color='green')
            ax2.plot(df['Fecha'], utabon_days, marker='s', label='Utabon', color='purple')
            ax2.set_title("Días desde suspensión")
            ax2.set_ylabel("Días")
            ax2.legend(fontsize=8)
            ax2.tick_params(axis='x', rotation=45, labelsize=8)
            
            # Gráfico 3: Síntomas sistémicos (presencia/ausencia)
            if 'Dias_PostOp' in df.columns:
                ax3.plot(df['Fecha'], df['Dias_PostOp'], marker='d', label='Días post-op', color='brown')
                ax3.set_title("Recuperación Post-operatoria")
                ax3.set_ylabel("Días desde operación")
                ax3.legend(fontsize=8)
                ax3.tick_params(axis='x', rotation=45, labelsize=8)
            
            # Gráfico 4: Resumen de mejora
            dolor_numeric = []
            for _, row in df.iterrows():
                dolor_val = 0
                if 'Dolor' in df.columns:
                    dolor_text = str(row['Dolor']).lower()
                    if 'leve' in dolor_text: dolor_val = 2
                    elif 'moderado' in dolor_text: dolor_val = 5
                    elif 'severo' in dolor_text: dolor_val = 8
                dolor_numeric.append(dolor_val)
            
            ax4.plot(df['Fecha'], dolor_numeric, marker='x', label='Dolor', color='red')
            ax4.set_title("Evolución del Dolor")
            ax4.set_ylabel("Intensidad")
            ax4.legend(fontsize=8)
            ax4.tick_params(axis='x', rotation=45, labelsize=8)
            
            self.figure.tight_layout()
            
        except Exception as e:
            ax = self.figure.add_subplot(111)
            ax.text(0.5, 0.5, f"Error al generar gráfico:\n{str(e)}", ha='center', va='center')

        self.canvas.draw()

    def exportar_pdf(self):
        try:
            if not os.path.exists(CARPETA_REPORTES):
                os.makedirs(CARPETA_REPORTES)

            df = pd.read_csv(ARCHIVO)
            
            if df.empty:
                QMessageBox.warning(self, "Advertencia", "No hay datos para exportar.")
                return

            # Crear una figura nueva para PDF usando la misma lógica que la interfaz
            fig = plt.figure(figsize=(16, 12))
            df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d-%m-%Y')
            df.sort_values(by='Fecha', inplace=True)
            
            # Crear los 4 subgráficos exactamente como en la interfaz
            ax1 = fig.add_subplot(2, 2, 1)
            ax2 = fig.add_subplot(2, 2, 2)
            ax3 = fig.add_subplot(2, 2, 3)
            ax4 = fig.add_subplot(2, 2, 4)
            
            # Gráfico 1: Síntomas nasales principales (igual que en graficar())
            ax1.plot(df['Fecha'], df['Congestion'], marker='o', label='Congestión', color='red')
            ax1.plot(df['Fecha'], df['Picor'], marker='s', label='Picor', color='orange')
            if 'Estornudos' in df.columns:
                ax1.plot(df['Fecha'], df['Estornudos'], marker='^', label='Estornudos', color='blue')
            ax1.set_title("Síntomas Nasales", fontsize=14, fontweight='bold')
            ax1.set_ylabel("Intensidad (0-10)")
            ax1.legend(fontsize=10)
            ax1.tick_params(axis='x', rotation=45, labelsize=10)
            ax1.grid(True, alpha=0.3)
            
            # Gráfico 2: Estado de medicamentos (igual que en graficar())
            respibien_days = []
            utabon_days = []
            
            for _, row in df.iterrows():
                resp_val = 0
                uta_val = 0
                
                if 'Respibien_Suspendido' in df.columns:
                    resp_text = str(row['Respibien_Suspendido'])
                    if 'hoy' in resp_text: resp_val = 0
                    elif '1 día' in resp_text: resp_val = 1
                    elif '2-3 días' in resp_text: resp_val = 2.5
                    elif '>3 días' in resp_text: resp_val = 5
                    
                if 'Utabon_Suspendido' in df.columns:
                    uta_text = str(row['Utabon_Suspendido'])
                    if 'hoy' in uta_text: uta_val = 0
                    elif '1 día' in uta_text: uta_val = 1
                    elif '2-3 días' in uta_text: uta_val = 2.5
                    elif '>3 días' in uta_text: uta_val = 5
                    
                respibien_days.append(resp_val)
                utabon_days.append(uta_val)
            
            ax2.plot(df['Fecha'], respibien_days, marker='o', label='Respibien', color='green')
            ax2.plot(df['Fecha'], utabon_days, marker='s', label='Utabon', color='purple')
            ax2.set_title("Días desde suspensión", fontsize=14, fontweight='bold')
            ax2.set_ylabel("Días")
            ax2.legend(fontsize=10)
            ax2.tick_params(axis='x', rotation=45, labelsize=10)
            ax2.grid(True, alpha=0.3)
            
            # Gráfico 3: Recuperación Post-operatoria (igual que en graficar())
            if 'Dias_PostOp' in df.columns and not df['Dias_PostOp'].isna().all():
                ax3.plot(df['Fecha'], df['Dias_PostOp'], marker='d', label='Días post-op', color='brown', linewidth=2)
                ax3.set_title("Recuperación Post-operatoria", fontsize=14, fontweight='bold')
                ax3.set_ylabel("Días desde operación")
                ax3.legend(fontsize=10)
                ax3.tick_params(axis='x', rotation=45, labelsize=10)
                ax3.grid(True, alpha=0.3)
            else:
                ax3.text(0.5, 0.5, "No hay datos\npost-operatorios", ha='center', va='center', 
                        fontsize=12, transform=ax3.transAxes)
                ax3.set_title("Recuperación Post-operatoria", fontsize=14, fontweight='bold')
            
            # Gráfico 4: Evolución del Dolor (igual que en graficar())
            dolor_numeric = []
            for _, row in df.iterrows():
                dolor_val = 0
                if 'Dolor' in df.columns:
                    dolor_text = str(row['Dolor']).lower()
                    if 'leve' in dolor_text: dolor_val = 2
                    elif 'moderado' in dolor_text: dolor_val = 5
                    elif 'severo' in dolor_text: dolor_val = 8
                dolor_numeric.append(dolor_val)
            
            ax4.plot(df['Fecha'], dolor_numeric, marker='x', label='Dolor', color='red', linewidth=2, markersize=8)
            ax4.set_title("Evolución del Dolor", fontsize=14, fontweight='bold')
            ax4.set_ylabel("Intensidad")
            ax4.legend(fontsize=10)
            ax4.tick_params(axis='x', rotation=45, labelsize=10)
            ax4.grid(True, alpha=0.3)
            
            # Ajustar el layout para mejor apariencia
            plt.tight_layout(pad=3.0)

            # Guardar imagen
            fecha_actual = datetime.now().strftime('%Y%m%d_%H%M%S')
            img_path = os.path.join(CARPETA_REPORTES, f"grafico_sintomas_{fecha_actual}.png")
            pdf_path = os.path.join(CARPETA_REPORTES, f"historial_sintomas_{fecha_actual}.pdf")

            plt.savefig(img_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
            plt.close()

            # Crear PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=16)
            pdf.cell(200, 10, txt="Mis alergias y Yo", ln=True, align='C')
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 8, txt="Seguimiento de Recuperación Post-Operatoria", ln=True, align='C')
            pdf.cell(200, 6, txt="Alergia Medicamentosa - Descongestivos Nasales", ln=True, align='C')
            pdf.ln(10)

            # Resumen
            pdf.set_font("Arial", size=10)
            pdf.cell(200, 6, txt=f"Reporte generado: {datetime.now().strftime('%d-%m-%Y %H:%M')}", ln=True)
            pdf.cell(200, 6, txt=f"Total de registros: {len(df)}", ln=True)
            
            # Estadísticas resumidas
            if not df.empty:
                congestion_promedio = df['Congestion'].mean()
                picor_promedio = df['Picor'].mean()
                pdf.cell(200, 6, txt=f"Congestión promedio: {congestion_promedio:.1f} | Picor promedio: {picor_promedio:.1f}", ln=True)
            
            pdf.ln(5)

            # Detalles de cada registro
            pdf.set_font("Arial", size=8)
            for index, row in df.iterrows():
                fecha_str = row['Fecha'] if isinstance(row['Fecha'], str) else row['Fecha'].strftime('%d-%m-%Y')
                
                # Información básica
                texto_basico = f"FECHA: {fecha_str} | Congestión: {row['Congestion']} | Picor: {row['Picor']} | Dolor: {row['Dolor']} | Secreción: {row['Secrecion']}"
                pdf.multi_cell(0, 4, texto_basico)
                
                # Información de medicamentos
                if 'Respibien_Suspendido' in df.columns and 'Utabon_Suspendido' in df.columns:
                    texto_med = f"Medicamentos - Respibien: {row['Respibien_Suspendido']} | Utabon: {row['Utabon_Suspendido']}"
                    if 'Otros_Medicamentos' in df.columns and str(row['Otros_Medicamentos']) != 'nan' and row['Otros_Medicamentos']:
                        texto_med += f" | Otros: {row['Otros_Medicamentos']}"
                    pdf.multi_cell(0, 4, texto_med)
                
                # Síntomas respiratorios
                if 'Dificultad_Respirar' in df.columns:
                    texto_resp = f"Respiratorio - Dificultad: {row['Dificultad_Respirar']} | Tos: {row['Tos']} | Estornudos: {row['Estornudos']}"
                    pdf.multi_cell(0, 4, texto_resp)
                
                # Síntomas cutáneos
                if 'Erupciones' in df.columns:
                    texto_cutaneo = f"Cutáneo - Erupciones: {row['Erupciones']} | Urticaria: {row['Urticaria']} | Hinchazón: {row['Hinchazón']}"
                    pdf.multi_cell(0, 4, texto_cutaneo)
                
                # Información post-operatoria
                if 'Dias_PostOp' in df.columns:
                    texto_postop = f"Post-op - Días: {row['Dias_PostOp']} | Mejoría respiratoria: {row['Mejoria_Respiracion']}"
                    pdf.multi_cell(0, 4, texto_postop)
                
                # Notas
                if 'Notas' in df.columns and str(row['Notas']) != 'nan' and row['Notas']:
                    pdf.multi_cell(0, 4, f"Notas: {row['Notas']}")
                
                pdf.ln(2)

            # Añadir página nueva para el gráfico si es necesario
            if pdf.get_y() > 200:
                pdf.add_page()

            # Añadir gráfico completo con los 4 subgráficos
            try:
                pdf.ln(5)
                pdf.set_font("Arial", size=12)
                pdf.cell(200, 8, txt="Gráficos de Evolución", ln=True, align='C')
                pdf.ln(5)
                pdf.image(img_path, x=10, w=190)
            except Exception as img_error:
                pdf.cell(200, 10, txt=f"Error al insertar gráfico: {str(img_error)}", ln=True, align='C')

            pdf.output(pdf_path)

            QMessageBox.information(self, "Exportado", 
                f"✅ Exportación completada:\n\n"
                f"📄 PDF: {pdf_path}\n"
                f"🖼️ Imagen (4 gráficos): {img_path}\n\n"
                f"El archivo contiene todos los gráficos de seguimiento.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"❌ No se pudo exportar a PDF:\n{str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Configuración específica para GNOME3 y AppIndicator
    app.setQuitOnLastWindowClosed(False)  # No cerrar cuando se minimiza a tray
    app.setApplicationName("Mis alergias y Yo")
    app.setApplicationDisplayName("Mis alergias y Yo")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("SaludApp")
    app.setOrganizationDomain("saludapp.local")
    
    # Configuración del icono de la aplicación para la barra de tareas
    icon_path = "img/logo.png"
    if os.path.exists(icon_path):
        icon = QIcon(icon_path)
        app.setWindowIcon(icon)
        
        # Forzar la carga del icono con diferentes tamaños
        pixmap = QPixmap(icon_path)
        if not pixmap.isNull():
            # Crear iconos de diferentes tamaños para mejor compatibilidad
            icon.addPixmap(pixmap.scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            icon.addPixmap(pixmap.scaled(22, 22, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            icon.addPixmap(pixmap.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            icon.addPixmap(pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            icon.addPixmap(pixmap.scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            icon.addPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            app.setWindowIcon(icon)
            print(f"🎨 Icono configurado con múltiples tamaños: {icon_path}")
    
    # Configuración adicional para Linux/X11 y GNOME3
    if hasattr(app, 'setAttribute'):
        try:
            from PyQt5.QtCore import Qt
            app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
            # Configuración específica para temas GTK en GNOME3
            if hasattr(Qt, 'AA_UseStyleSheetPropagationInWidgetStyles'):
                app.setAttribute(Qt.AA_UseStyleSheetPropagationInWidgetStyles, True)
        except:
            pass
    
    # Variables de entorno específicas para GNOME3 system tray
    os.environ['QT_QPA_PLATFORMTHEME'] = 'gtk3'
    
    window = SintomasApp()
    window.show()
    
    # Asegurar que la ventana tenga el foco y se muestre correctamente
    window.raise_()
    window.activateWindow()
    
    print(f"🚀 Aplicación iniciada: {app.applicationName()}")
    print(f"🖼️ Icono configurado: {icon_path}")
    print(f"🔔 System Tray: {'✅ Disponible' if QSystemTrayIcon.isSystemTrayAvailable() else '❌ No disponible'}")
    
    # Información específica para GNOME3
    print("💡 Para GNOME3:")
    print("   - El icono debería aparecer en la esquina superior derecha")
    print("   - Si no lo ves, asegúrate de tener 'AppIndicator' habilitado")
    print("   - Comando: gnome-extensions enable ubuntu-appindicators@ubuntu.com")
    
    sys.exit(app.exec_())
