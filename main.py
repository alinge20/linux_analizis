"""
Análisis de Sistema Linux
Programa con interfaz gráfica que muestra el estado del sistema
y uso de recursos en tiempo real.

Autora: Allison Guerrero
GitHub: @alinge20
"""

import tkinter as tk
from tkinter import ttk
import platform
import psutil
import datetime
import threading
import time

# Colores del tema
BG_COLOR = "#1a1a2e"
CARD_BG = "#16213e"
TEXT_COLOR = "#e4e6eb"
ACCENT_COLOR = "#3D5A80"
ACCENT_LIGHT = "#7BA3CC"
SUCCESS_COLOR = "#4ade80"
WARNING_COLOR = "#fbbf24"
DANGER_COLOR = "#f87171"


class SistemaApp:
    """Aplicación principal de análisis del sistema."""

    def __init__(self, root):
        self.root = root
        self.root.title("Análisis de Sistema Linux")
        self.root.geometry("900x700")
        self.root.configure(bg=BG_COLOR)
        self.root.minsize(800, 600)

        self.running = True
        self.cpu_history = [0] * 60  # Últimos 60 valores de CPU

        self._crear_interfaz()
        self._actualizar_datos()

    def _crear_interfaz(self):
        """Crea todos los elementos de la interfaz."""
        # Título principal
        titulo = tk.Label(
            self.root,
            text="Monitor del Sistema",
            font=("Helvetica", 20, "bold"),
            bg=BG_COLOR,
            fg=ACCENT_LIGHT,
        )
        titulo.pack(pady=(15, 5))

        subtitulo = tk.Label(
            self.root,
            text="Análisis en tiempo real de los recursos del sistema",
            font=("Helvetica", 10),
            bg=BG_COLOR,
            fg="#8899aa",
        )
        subtitulo.pack(pady=(0, 10))

        # Frame principal con scroll
        main_frame = tk.Frame(self.root, bg=BG_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        # Fila superior: Sistema + CPU
        fila_superior = tk.Frame(main_frame, bg=BG_COLOR)
        fila_superior.pack(fill=tk.X, pady=5)

        self.panel_sistema = self._crear_panel(fila_superior, "Sistema Operativo")
        self.panel_sistema.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        self.panel_cpu = self._crear_panel(fila_superior, "CPU")
        self.panel_cpu.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))

        # Fila media: RAM + Disco
        fila_media = tk.Frame(main_frame, bg=BG_COLOR)
        fila_media.pack(fill=tk.X, pady=5)

        self.panel_ram = self._crear_panel(fila_media, "Memoria RAM")
        self.panel_ram.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        self.panel_disco = self._crear_panel(fila_media, "Disco Duro")
        self.panel_disco.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))

        # Fila inferior: Red + Procesos
        fila_inferior = tk.Frame(main_frame, bg=BG_COLOR)
        fila_inferior.pack(fill=tk.X, pady=5)

        self.panel_red = self._crear_panel(fila_inferior, "Red")
        self.panel_red.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        self.panel_procesos = self._crear_panel(fila_inferior, "Top Procesos")
        self.panel_procesos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))

        # Barra de estado
        self.estado = tk.Label(
            self.root,
            text="Actualizando...",
            font=("Helvetica", 9),
            bg=BG_COLOR,
            fg="#667788",
            anchor="w",
        )
        self.estado.pack(fill=tk.X, padx=15, pady=(5, 10))

    def _crear_panel(self, parent, titulo):
        """Crea un panel con título y área de contenido."""
        frame = tk.Frame(parent, bg=CARD_BG, highlightbackground=ACCENT_COLOR,
                         highlightthickness=1, padx=12, pady=8)

        header = tk.Label(
            frame,
            text=titulo,
            font=("Helvetica", 11, "bold"),
            bg=CARD_BG,
            fg=ACCENT_LIGHT,
            anchor="w",
        )
        header.pack(fill=tk.X, pady=(0, 6))

        contenido = tk.Label(
            frame,
            text="Cargando...",
            font=("Courier", 9),
            bg=CARD_BG,
            fg=TEXT_COLOR,
            anchor="nw",
            justify=tk.LEFT,
        )
        contenido.pack(fill=tk.BOTH, expand=True)

        frame.contenido = contenido
        return frame

    def _formato_bytes(self, bytes_val):
        """Convierte bytes a formato legible (KB, MB, GB)."""
        for unidad in ["B", "KB", "MB", "GB", "TB"]:
            if bytes_val < 1024.0:
                return f"{bytes_val:.1f} {unidad}"
            bytes_val /= 1024.0
        return f"{bytes_val:.1f} PB"

    def _barra_progreso(self, porcentaje, ancho=20):
        """Crea una barra de progreso con texto."""
        lleno = int(ancho * porcentaje / 100)
        vacio = ancho - lleno

        if porcentaje < 50:
            color_texto = "OK"
        elif porcentaje < 80:
            color_texto = "MEDIO"
        else:
            color_texto = "ALTO"

        barra = "█" * lleno + "░" * vacio
        return f"[{barra}] {porcentaje:.1f}% ({color_texto})"

    def _tiempo_encendido(self, segundos):
        """Convierte segundos a formato legible."""
        dias = segundos // 86400
        horas = (segundos % 86400) // 3600
        minutos = (segundos % 3600) // 60

        partes = []
        if dias > 0:
            partes.append(f"{int(dias)}d")
        if horas > 0:
            partes.append(f"{int(horas)}h")
        partes.append(f"{int(minutos)}m")
        return " ".join(partes)

    def _obtener_info_sistema(self):
        """Obtiene información del sistema operativo."""
        uname = platform.uname()
        boot_time = psutil.boot_time()
        uptime = time.time() - boot_time
        boot_dt = datetime.datetime.fromtimestamp(boot_time)

        texto = (
            f"SO:       {uname.system} {uname.release}\n"
            f"Nombre:   {uname.node}\n"
            f"Versión:  {uname.version[:40]}\n"
            f"Arquit.:  {uname.machine}\n"
            f"Python:   {platform.python_version()}\n"
            f"Encendido: {self._tiempo_encendido(uptime)}\n"
            f"Inicio:   {boot_dt.strftime('%d/%m/%Y %H:%M')}"
        )
        return texto

    def _obtener_info_cpu(self):
        """Obtiene información del CPU."""
        cpu_percent = psutil.cpu_percent(interval=0)
        cpu_count = psutil.cpu_count(logical=True)
        cpu_physical = psutil.cpu_count(logical=False)
        per_cpu = psutil.cpu_percent(percpu=True)

        self.cpu_history.append(cpu_percent)
        self.cpu_history = self.cpu_history[-60:]

        # Mini gráfica con caracteres
        max_height = 8
        mini_graph_data = self.cpu_history[-30:]
        lineas_grafica = []
        for nivel in range(max_height, 0, -1):
            linea = ""
            umbral = (nivel / max_height) * 100
            for val in mini_graph_data:
                linea += "█" if val >= umbral else " "
            lineas_grafica.append(f"  {linea}")

        grafica = "\n".join(lineas_grafica)

        nucleos_texto = ""
        for i, p in enumerate(per_cpu[:8]):
            barra = "█" * int(p / 10) + "░" * (10 - int(p / 10))
            nucleos_texto += f"  Core {i}: [{barra}] {p:5.1f}%\n"

        texto = (
            f"Uso total: {self._barra_progreso(cpu_percent)}\n"
            f"Núcleos:   {cpu_physical} físicos, {cpu_count} lógicos\n\n"
            f"{nucleos_texto}\n"
            f"Historial (30s):\n{grafica}"
        )
        return texto

    def _obtener_info_ram(self):
        """Obtiene información de la memoria RAM."""
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()

        texto = (
            f"RAM Total:     {self._formato_bytes(mem.total)}\n"
            f"RAM Usada:     {self._formato_bytes(mem.used)}\n"
            f"RAM Disponible:{self._formato_bytes(mem.available)}\n"
            f"Uso RAM:  {self._barra_progreso(mem.percent)}\n\n"
            f"SWAP Total:    {self._formato_bytes(swap.total)}\n"
            f"SWAP Usada:    {self._formato_bytes(swap.used)}\n"
            f"Uso SWAP: {self._barra_progreso(swap.percent)}"
        )
        return texto

    def _obtener_info_disco(self):
        """Obtiene información de los discos."""
        particiones = psutil.disk_partitions()
        texto = ""

        for p in particiones[:4]:
            try:
                uso = psutil.disk_usage(p.mountpoint)
                texto += (
                    f"Partición: {p.mountpoint}\n"
                    f"  Sistema:  {p.fstype}\n"
                    f"  Total:    {self._formato_bytes(uso.total)}\n"
                    f"  Usado:    {self._formato_bytes(uso.used)}\n"
                    f"  Libre:    {self._formato_bytes(uso.free)}\n"
                    f"  {self._barra_progreso(uso.percent)}\n\n"
                )
            except PermissionError:
                texto += f"Partición: {p.mountpoint}\n  (sin acceso)\n\n"

        return texto.strip()

    def _obtener_info_red(self):
        """Obtiene información de red."""
        io = psutil.net_io_counters()
        addrs = psutil.net_if_addrs()

        texto = (
            f"Datos enviados:    {self._formato_bytes(io.bytes_sent)}\n"
            f"Datos recibidos:   {self._formato_bytes(io.bytes_recv)}\n"
            f"Paquetes enviados: {io.packets_sent:,}\n"
            f"Paquetes recibidos:{io.packets_recv:,}\n\n"
            f"Interfaces:\n"
        )

        for nombre, lista_addr in list(addrs.items())[:5]:
            for addr in lista_addr:
                if addr.family.name == "AF_INET":
                    texto += f"  {nombre}: {addr.address}\n"
                    break

        return texto

    def _obtener_top_procesos(self):
        """Obtiene los procesos que más CPU usan."""
        procesos = []
        for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
            try:
                info = proc.info
                if info["cpu_percent"] is not None and info["cpu_percent"] > 0:
                    procesos.append(info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        procesos.sort(key=lambda x: x["cpu_percent"] or 0, reverse=True)
        top = procesos[:8]

        texto = f"{'PID':<8} {'Nombre':<18} {'CPU%':>6} {'RAM%':>6}\n"
        texto += "─" * 40 + "\n"

        for p in top:
            nombre = (p["name"] or "?")[:17]
            cpu = p["cpu_percent"] or 0
            mem = p["memory_percent"] or 0
            texto += f"{p['pid']:<8} {nombre:<18} {cpu:>5.1f}% {mem:>5.1f}%\n"

        if not top:
            texto += "(recopilando datos...)\n"

        return texto

    def _actualizar_datos(self):
        """Actualiza todos los paneles con datos nuevos."""
        if not self.running:
            return

        try:
            self.panel_sistema.contenido.config(text=self._obtener_info_sistema())
            self.panel_cpu.contenido.config(text=self._obtener_info_cpu())
            self.panel_ram.contenido.config(text=self._obtener_info_ram())
            self.panel_disco.contenido.config(text=self._obtener_info_disco())
            self.panel_red.contenido.config(text=self._obtener_info_red())
            self.panel_procesos.contenido.config(text=self._obtener_top_procesos())

            ahora = datetime.datetime.now().strftime("%H:%M:%S")
            self.estado.config(text=f"Última actualización: {ahora}  |  Actualización cada 2 segundos")
        except Exception as e:
            self.estado.config(text=f"Error: {str(e)}")

        # Programar siguiente actualización
        self.root.after(2000, self._actualizar_datos)

    def cerrar(self):
        """Cierra la aplicación correctamente."""
        self.running = False
        self.root.destroy()


def main():
    """Punto de entrada de la aplicación."""
    root = tk.Tk()
    app = SistemaApp(root)
    root.protocol("WM_DELETE_WINDOW", app.cerrar)
    root.mainloop()


if __name__ == "__main__":
    main()
