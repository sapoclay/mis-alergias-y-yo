# 💊 Mis Alergias y Yo

![about-mis-alergias-y-yo](https://github.com/user-attachments/assets/0d7f1e5d-24fb-4a1c-a429-3ac0b6609e5f)

**Seguimiento de alergias medicamentosas post-operatorias**

Esta es una pequeña aplicación que se ha creado para el monitoreo y seguimiento de alergias medicamentosas por descongestivos nasales tras una cirugía de cornetes nasales a la que me he sometido hace poco.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Platform](https://img.shields.io/badge/Platform-Linux%20|%20Windows%20|%20macOS-lightgrey.svg)

## 📋 Descripción

**Mis Alergias y Yo** es una herramienta de seguimiento médico diseñada específicamente para pacientes que han experimentado reacciones alérgicas a descongestivos nasales y que los ha llevado a una cirugía de cornetes nasales para intentar mejorar la respiración que se ha vuelto imposible. Esto no hubiese ocurrido si no hubiese tenido que esperar 6 años para que me atendiesen ... pero es lo que hay.

### 🎯 ¿Para qué sirve?

- **Seguimiento post-operatorio**: Monitorizar la recuperación tras cirugía de cornetes nasales
- **Control de alergias medicamentosas**: Rastrea síntomas relacionados con descongestivos nasales
- **Documentación médica**: Genera reportes detallados para consultas médicas
- **Cronología de recuperación**: Proporciona información sobre tiempos esperados de mejoría

## ✨ Características principales

### 📊 Registro completo de síntomas
![mis-alergias-y-yo-formulario](https://github.com/user-attachments/assets/72c98b7e-9724-4fdb-ba28-e722700560a2)
- **Síntomas nasales**: Congestión, picor, dolor, tipo de secreción
- **Síntomas respiratorios**: Dificultad para respirar, tos, estornudos
- **Síntomas cutáneos**: Erupciones, urticaria, hinchazón
- **Estado post-operatorio**: Días desde cirugía, mejoría respiratoria

### 💊 Control de medicamentos
- Seguimiento específico de **Respibien** y **Utabon** ... que son los medicamentos de los que yo en particular tuve que tirar durante tantisimo tiempo.
- Registro de suspensión de medicamentos
- Control de otros medicamentos tomados
- Alertas de seguridad

### 📈 Visualización de datos
![mis-alergias-y-yo-graficos](https://github.com/user-attachments/assets/e6322046-8104-4c36-bd76-cebbfa635064)
- **4 gráficos especializados**:
  - Evolución de síntomas nasales
  - Días desde suspensión de medicamentos
  - Progreso post-operatorio
  - Evolución del dolor

### 📄 Exportación profesional
- **PDF completo** con todos los datos y gráficos
- **Imágenes PNG** de alta resolución
- Formato optimizado para consultas médicas
- Cronología detallada de cada registro

### 🖥️ Interfaz de usuario
- **Diseño médico profesional** con iconos intuitivos
- **Scroll vertical** para formularios extensos
- **Menús contextuales** completos
- **Pantalla completa** (F11) para mejor visualización

## 🚀 Instalación y uso

### Requisitos del sistema
- Python 3.8 o superior
- Sistema operativo: Linux, Windows, macOS
- Para GNOME3: Extensión AppIndicator recomendada

### Instalación rápida

```bash
# Clonar el repositorio
git clone https://github.com/usuario/alergia-medicamentosa.git
cd alergia-medicamentosa

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python3 main.py
```

### Instalación con Entorno Virtual (Recomendado)

```bash
# Ejecutar
python3 run_app.py
```

## 📖 Guía de uso

### 1. **Registro diario de síntomas**
- Abre la aplicación y completa los campos del formulario
- Usa las escalas de 0-10 para síntomas cuantificables (0 = nada, 10 = insufrible)
- Selecciona opciones específicas en los menús desplegables
- Añade observaciones en el campo de notas

### 2. **Interpretación de gráficos**
- **Síntomas nasales**: Muestra congestión, picor y estornudos en el tiempo
- **Medicamentos**: Visualiza días desde la suspensión de Respibien/Utabon
- **Post-operatorio**: Progreso desde la cirugía de cornetes
- **Dolor**: Evolución de la intensidad del dolor

### 3. **Exportación de reportes**
- Usa `Archivo > Exportar a PDF` para generar reporte completo
- El PDF incluye todos los datos, gráficos y cronología
- Ideal para llevar a consultas médicas

### 4. **Atajos de teclado**
- `Ctrl + S`: Guardar síntomas
- `Ctrl + E`: Exportar a PDF
- `F11`: Pantalla completa
- `Ctrl + Q`: Salir

## 📚 Información médica incluida

### Cronología de recuperación

#### 🔸 **Suspensión de descongestivos nasales**
- **Días 1-3**: Posible empeoramiento temporal (efecto rebote)
- **Días 4-7**: Mejora gradual de la respiración nasal
- **Días 8-14**: Normalización progresiva de la mucosa
- **Semanas 3-4**: Recuperación completa de la función nasal

#### 🔸 **Recuperación Post-Cirugía de cornetes**
- **Días 1-7**: Inflamación máxima, respiración limitada
- **Semanas 2-3**: Reducción de inflamación
- **Semanas 4-6**: Cicatrización completa
- **Meses 2-3**: Resultado final estabilizado

#### 🔸 **Resolución de alergia medicamentosa**
- **Días 1-3**: Eliminación del medicamento
- **Días 4-10**: Reducción de síntomas alérgicos
- **Semanas 2-4**: Resolución completa

## ⚠️ Importante - uso médico

> **Esta aplicación es complementaria al seguimiento médico profesional**

- Proporciona información "orientativa" sobre tiempos de recuperación
- Cada caso es único y puede variar
- **Consulta inmediata** si experimentas:
  - Dificultad respiratoria severa
  - Hinchazón facial
  - Urticaria generalizada
  - Empeoramiento tras 7 días de suspensión

## 🛠️ Características técnicas

### Tecnologías utilizadas
- **Python 3.8+**: Lenguaje principal
- **PyQt5**: Interfaz gráfica
- **Pandas**: Análisis de datos
- **Matplotlib**: Generación de gráficos
- **FPDF**: Exportación a PDF

### Arquitectura
- **MVC Pattern**: Separación de lógica y presentación
- **CSV Storage**: Base de datos ligera
- **Modular Design**: Fácil mantenimiento y extensión

### Compatibilidad
- **Linux**: Optimizado para GNOME3 con system tray
- **Windows**: Soporte completo
- **macOS**: Compatible

## 📁 Estructura del proyecto

```
alergia-medicamentosa/
├── main.py                          # Aplicación principal
├── run_app.py                       # Script de ejecución con entorno virtual
├── requirements.txt                 # Dependencias Python
├── img/
│   └── logo.png                     # Icono de la aplicación
├── reportes/                        # Directorio de exportaciones
└──  registro_sintomas.csv            # Base de datos de síntomas

```

## 🔧 Configuración avanzada

### Para Usuarios de GNOME3

1. **Habilitar AppIndicator**:
   ```bash
   gnome-extensions enable ubuntu-appindicators@ubuntu.com
   ```

2. **Reinstalar si es necesario**:
   ```bash
   sudo apt install gnome-shell-extension-appindicator
   ```

3. **Verificar configuración**:
   ```bash
   ./configurar_gnome3_tray.sh
   ```

### Personalización

- **Icono personalizado**: Reemplaza `img/logo.png`
- **Colores**: Modifica los estilos CSS en `main.py`
- **Campos adicionales**: Extiende el formulario en `init_ui()`

## 🐛 Solución de problemas

### Problema: "No veo el icono en GNOME3"
**Solución**: Instalar y habilitar extensión AppIndicator

### Problema: "Error al exportar PDF"
**Solución**: Verificar permisos de escritura en directorio `reportes/`

### Problema: "Aplicación no inicia"
**Solución**: Verificar dependencias con `pip install -r requirements.txt`

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas!

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 📞 Soporte

- **Issues**: [GitHub Issues](https://github.com/usuario/alergia-medicamentosa/issues)
- **Documentación**: Ver archivos README adicionales en el proyecto

---

### 🎯 Casos de usos típicos

1. **Post-cirugía inmediata**: Seguimiento diario de síntomas los primeros 7 días
2. **Suspensión de medicamentos**: Monitoreo del efecto rebote días 1-7
3. **Seguimiento a largo plazo**: Control mensual hasta la recuperación completa
4. **Preparación para citas médicas**: Exportación de reportes con historial completo

### 📊 Ejemplo de datos registrados

La aplicación rastrea automáticamente:
- 📅 **Fecha**: Formato dd-mm-aaaa
- 🌡️ **Síntomas**: Escala 0-10 y categorías específicas
- 💊 **Medicamentos**: Estado de suspensión detallado
- 📈 **Progreso**: Días post-operatorios y mejoría
- 📝 **Notas**: Observaciones personalizadas


## 👨‍⚕️ Autor

Desarrollado por entreunosyceros ... con mucho 😴 ... para ayudar en el seguimiento de alergias medicamentosas post-operatorias.
