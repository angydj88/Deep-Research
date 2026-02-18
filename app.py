"""
🔬 Deep Research Automator v5.0
Interfaz web con Streamlit
"""

import time
import streamlit as st
from config import Config
from dimensions import crear_dimensiones
from gemini_client import GeminiClient
from report_builder import ReportBuilder


# ═══════════════ CONFIGURACIÓN DE PÁGINA ═══════════════
st.set_page_config(
    page_title="🔬 Deep Research Automator",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ═══════════════ SIDEBAR ═══════════════
with st.sidebar:
    st.title("🔬 Deep Research")
    st.caption(f"v{Config.VERSION} · Powered by Gemini")

    st.divider()

    # API Key
    api_key = st.text_input(
        "🔑 Gemini API Key",
        value=Config.API_KEY,
        type="password",
        help="Obtén tu key en aistudio.google.com",
    )
    if api_key:
        Config.API_KEY = api_key

    st.divider()

    # Configuración avanzada
    with st.expander("⚙️ Configuración avanzada"):
        Config.MODEL = st.selectbox(
            "Modelo",
            [
                "gemini-2.0-flash",
                "gemini-2.5-flash-preview-05-20",
                "gemini-3-flash-preview",
            ],
            index=0,
        )
        Config.TEMPERATURE = st.slider(
            "Temperatura", 0.0, 1.0, 0.3, 0.1
        )
        Config.MAX_TOKENS = st.select_slider(
            "Max tokens",
            [4096, 8192, 16384, 32768],
            value=8192,
        )
        Config.DELAY_BETWEEN_CALLS = st.slider(
            "Pausa entre llamadas (s)", 1, 10, 3
        )

    st.divider()

    # Test
    if st.button("🧪 Test de conexión", use_container_width=True):
        with st.spinner("Probando..."):
            try:
                client = GeminiClient()
                resultado = client.test_conexion()
                if resultado["base"]:
                    st.success(f"✅ Conexión OK\n\n{resultado['detalle']}")
                else:
                    st.error(f"❌ Fallo: {resultado['detalle']}")
            except Exception as e:
                st.error(f"❌ Error: {e}")


# ═══════════════ CONTENIDO PRINCIPAL ═══════════════
st.title("🔬 Deep Research Automator")
st.markdown(
    "Investigación exhaustiva en **7 dimensiones** usando Gemini con Google Search."
)

# Input del objetivo
objetivo = st.text_area(
    "🎯 ¿Qué quieres investigar?",
    placeholder="Ej: El mejor proceso en Zaragoza para blanqueamiento dental...",
    height=100,
)

# Selección de dimensiones
st.markdown("### 📐 Dimensiones a investigar")
col1, col2 = st.columns(2)

todas_dims = [
    "📖 Lenguaje y Terminología",
    "💰 Economía y Mercado",
    "📊 Datos y Estadísticas",
    "🏭 Sector y Competencia",
    "🎯 Estrategias y Consejos",
    "⚠️ Riesgos y Amenazas",
    "🚀 Oportunidades y Futuro",
]

seleccionadas = []
for i, dim in enumerate(todas_dims):
    col = col1 if i < 4 else col2
    if col.checkbox(dim, value=True, key=f"dim_{i}"):
        seleccionadas.append(i)

incluir_resumen = st.checkbox("📋 Incluir resumen ejecutivo", value=True)

st.divider()


# ═══════════════ EJECUTAR INVESTIGACIÓN ═══════════════
if st.button(
    "🚀 INICIAR INVESTIGACIÓN PROFUNDA",
    type="primary",
    use_container_width=True,
    disabled=not objetivo or not seleccionadas,
):
    # Validar
    errores = Config.validate()
    if errores:
        for e in errores:
            st.error(f"❌ {e}")
        st.stop()

    if len(objetivo.strip()) < 5:
        st.error("❌ El objetivo es demasiado corto")
        st.stop()

    # Iniciar
    client = GeminiClient()
    builder = ReportBuilder(objetivo)
    dimensiones = crear_dimensiones(objetivo)

    # Filtrar dimensiones seleccionadas
    dims_activas = [dimensiones[i] for i in seleccionadas]

    # Barra de progreso
    progress_bar = st.progress(0)
    status_text = st.empty()
    tiempo_inicio = time.time()

    # Contenedor para resultados en vivo
    tabs = st.tabs(
        [f"{d['emoji']} {d['nombre'][:15]}" for d in dims_activas]
        + (["📋 Resumen"] if incluir_resumen else [])
    )

    # Ejecutar cada dimensión
    for idx, dim in enumerate(dims_activas):
        progreso = (idx) / (len(dims_activas) + (1 if incluir_resumen else 0))
        progress_bar.progress(progreso)
        status_text.markdown(
            f"⏳ **[{idx + 1}/{len(dims_activas)}]** "
            f"Investigando: {dim['emoji']} {dim['nombre']}..."
        )

        with tabs[idx]:
            with st.spinner(f"Investigando {dim['nombre']}..."):
                try:
                    resultado = client.generar(dim["prompt"])
                    st.markdown(resultado["texto"])

                    if resultado["fuentes"]:
                        with st.expander("📚 Fuentes consultadas"):
                            for fuente in resultado["fuentes"]:
                                st.markdown(f"- {fuente}")

                    st.success(
                        f"✅ {len(resultado['texto']):,} caracteres "
                        f"· Método: {resultado['metodo']}"
                    )

                    builder.agregar_seccion(
                        dim, resultado["texto"],
                        resultado["fuentes"], True
                    )

                except Exception as e:
                    st.error(f"❌ Error: {e}")
                    builder.agregar_seccion(dim, str(e), [], False)

        # Pausa entre llamadas
        if idx < len(dims_activas) - 1:
            time.sleep(Config.DELAY_BETWEEN_CALLS)

    # ── Resumen ejecutivo ──
    if incluir_resumen:
        progreso = len(dims_activas) / (len(dims_activas) + 1)
        progress_bar.progress(progreso)
        status_text.markdown("⏳ Generando **resumen ejecutivo**...")

        tab_resumen = tabs[-1]
        with tab_resumen:
            with st.spinner("Sintetizando hallazgos..."):
                try:
                    extractos = "\n\n".join(
                        f"**{s['dimension']['nombre']}:**\n"
                        f"{s['contenido'][:1500]}..."
                        for s in builder.secciones if s["exito"]
                    )

                    prompt_resumen = (
                        f'Eres un consultor ejecutivo de élite.\n\n'
                        f'OBJETIVO: "{objetivo}"\n\n'
                        f'Extractos de 7 dimensiones:\n\n{extractos}\n\n'
                        f'GENERA UN RESUMEN EJECUTIVO con:\n'
                        f'1. CONCLUSIÓN PRINCIPAL\n'
                        f'2. 10 INSIGHTS MÁS IMPORTANTES\n'
                        f'3. PLAN DE ACCIÓN (5 pasos inmediatos)\n'
                        f'4. DECISIÓN CRÍTICA\n'
                        f'5. VENTAJA COMPETITIVA\n'
                        f'6. MAYOR RIESGO + mitigación\n'
                        f'7. OPORTUNIDAD DORADA\n'
                        f'8. PREDICCIÓN a 12 meses\n\n'
                        f'Sé directo y accionable.'
                    )

                    resp_resumen = client.generar(prompt_resumen)
                    st.markdown(resp_resumen["texto"])
                    builder.set_resumen(resp_resumen["texto"])
                    st.success("✅ Resumen generado")

                except Exception as e:
                    st.error(f"⚠️ Error en resumen: {e}")

    # ── Finalizar ──
    progress_bar.progress(1.0)
    duracion = time.time() - tiempo_inicio
    stats = builder.stats

    status_text.markdown(
        f"✅ **¡COMPLETADO!** · {stats['exitosas']}/{stats['total']} secciones "
        f"· {stats['caracteres']:,} caracteres "
        f"· {duracion / 60:.1f} minutos"
    )

    st.balloons()

    # ── Descargas ──
    st.divider()
    st.subheader("📥 Descargar informe")

    rutas = builder.guardar_todo()

    col_d1, col_d2, col_d3 = st.columns(3)

    with col_d1:
        md_content = builder.exportar_markdown()
        st.download_button(
            "📄 Descargar Markdown",
            data=md_content,
            file_name=f"informe_{objetivo[:30]}.md",
            mime="text/markdown",
            use_container_width=True,
        )

    with col_d2:
        txt_content = builder.exportar_texto_plano()
        st.download_button(
            "📝 Descargar TXT (para IA)",
            data=txt_content,
            file_name=f"informe_{objetivo[:30]}.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with col_d3:
        with open(rutas["docx"], "rb") as f:
            st.download_button(
                "📘 Descargar Word",
                data=f.read(),
                file_name=f"informe_{objetivo[:30]}.docx",
                mime="application/vnd.openxmlformats-officedocument"
                     ".wordprocessingml.document",
                use_container_width=True,
            )


# ═══════════════ FOOTER ═══════════════
st.divider()
st.caption(
    f"Deep Research Automator v{Config.VERSION} · "
    f"Modelo: {Config.MODEL} · "
    f"Powered by Google Gemini"
)
