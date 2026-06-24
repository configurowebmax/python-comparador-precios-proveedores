"""
=====================================================================
 Comparador de Precios de Proveedores
 ConfiguroWeb · 2026 · Python real en el navegador (PyScript)
=====================================================================
"""
from pyscript import document, window
from js import localStorage
import json
import math

APP_CLAVE = "python_comparador_precios_proveedores_datos"
VERSION = "1.0.0"


# =====================================================================
#  Lógica de negocio
# =====================================================================
class Calculadora:
    """Modelo de cálculo de Comparador de Precios de Proveedores."""

    def __init__(self, p1, p2, p3):
        self.p1 = float(p1)
        self.p2 = float(p2)
        self.p3 = float(p3)

    def calcular(self):
        """Ejecuta el cálculo principal y devuelve un dict de resultados."""

        precios = {"Proveedor 1": self.p1, "Proveedor 2": self.p2, "Proveedor 3": self.p3}
        menor_nombre = min(precios, key=precios.get)
        menor = precios[menor_nombre]
        promedio = sum(precios.values()) / 3
        ahorro = promedio - menor
        return {"precios": precios, "menor_nombre": menor_nombre, "menor": menor, "ahorro": ahorro}


    def diagnostico(self, resultados):
        """Texto explicativo del resultado."""
        return "✅ Mejor opción identificada."


# =====================================================================
#  Formateadores
# =====================================================================
def fmt_moneda(v):
    if v is None:
        return "—"
    if math.isinf(v):
        return "∞"
    return f"${v:,.0f}"

def fmt_num(v):
    if v is None:
        return "—"
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return f"{v:,}"

def fmt_pct(v):
    if v is None:
        return "—"
    return f"{v:.1f}%"


# =====================================================================
#  Persistencia localStorage
# =====================================================================
def cargar_guardado():
    try:
        raw = localStorage.getItem(APP_CLAVE)
        if raw:
            return json.loads(raw)
    except Exception:
        pass
    return None

def guardar_ls(datos):
    try:
        localStorage.setItem(APP_CLAVE, json.dumps(datos))
        return True
    except Exception:
        return False


# =====================================================================
#  UI helpers
# =====================================================================
def input_float(eid):
    el = document.querySelector(f"#{eid}")
    if not el or not el.value:
        return 0.0
    try:
        return float(el.value)
    except (ValueError, TypeError):
        return 0.0

def mostrar(html, clase=""):
    caja = document.querySelector("#resultado")
    caja.innerHTML = html
    caja.classList.remove("hidden", "is-error", "is-success")
    if clase:
        caja.classList.add(clase)


# =====================================================================
#  Handlers
# =====================================================================
def calcular_handler(event=None):
    """Lee inputs, instancia, calcula y muestra."""

    c = Calculadora(input_float("p1"), input_float("p2"), input_float("p3"))
    r = c.calcular()
    html = f"""
      <div class="result-value">🆚 Mejor: {r["menor_nombre"]} ({fmt_moneda(r["menor"])})</div>
      <p class="result-detail">Ahorro vs promedio: {fmt_moneda(r["ahorro"])}</p>
    """
    mostrar(html, clase="is-success")



def guardar_datos(event=None):
    datos = {
            "p1": input_float("p1"),
            "p2": input_float("p2"),
            "p3": input_float("p3"),
        "version": VERSION,
    }
    ok = guardar_ls(datos)
    if ok:
        mostrar("💾 Datos guardados en este navegador.", clase="is-success")
    else:
        mostrar("❌ No se pudieron guardar los datos.", clase="is-error")


def cargar_al_inicio():
    datos = cargar_guardado()
    if not datos:
        return
    try:
            if "p1" in datos:
                document.querySelector("#p1").value = datos["p1"]
            if "p2" in datos:
                document.querySelector("#p2").value = datos["p2"]
            if "p3" in datos:
                document.querySelector("#p3").value = datos["p3"]
        aviso = document.querySelector("#resultado")
        aviso.innerHTML = "📂 Datos cargados. Pulsa <em>Calcular</em>."
        aviso.classList.remove("hidden")
    except Exception:
        pass


def inicializar():
    cargar_al_inicio()
    window.dispatchEvent(window.Event.new("py:ready"))

inicializar()
