# Análisis de Sistema Linux

Programa en Python con interfaz gráfica que muestra el estado del sistema operativo y el uso de memoria RAM en tiempo real.

## Características

- Información del sistema operativo (nombre, versión, arquitectura)
- Uso de CPU en tiempo real con gráfica
- Uso de memoria RAM con barra de progreso
- Uso de disco duro
- Información de red
- Actualización automática cada 2 segundos
- Interfaz gráfica moderna con Tkinter

## Requisitos

- Python 3.8+
- Sistema operativo Linux

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/alinge20/linux_analizis.git
cd linux_analizis

# Instalar dependencias
pip install -r requirements.txt
```

## Uso

```bash
python main.py
```

## Dependencias

- `psutil` — Información del sistema y procesos
- `tkinter` — Interfaz gráfica (incluido con Python)
- `matplotlib` — Gráficas de uso de CPU

## Capturas

La aplicación muestra paneles con:
- Panel de Sistema: nombre del SO, versión del kernel, arquitectura, tiempo encendido
- Panel de CPU: porcentaje de uso por núcleo y gráfica en tiempo real
- Panel de RAM: memoria total, usada, disponible y barra de progreso
- Panel de Disco: espacio total, usado y libre por partición
- Panel de Red: direcciones IP, bytes enviados y recibidos

## Autora

Allison Guerrero — [@alinge20](https://github.com/alinge20)
