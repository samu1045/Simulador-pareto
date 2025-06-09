import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random

# Configurar página
st.set_page_config(page_title="Simulador Inteligente - Diagrama de Pareto", layout="centered")

st.title("🧠 Simulador Diagnóstico Empresarial - Método de Pareto")

# Escenarios con descripciones
escenarios = {
    "Fábrica de tazas metálicas": {
        "descripcion": "Una empresa de manufactura que produce tazas metálicas antivuelco ha recibido múltiples quejas por defectos de calidad y problemas logísticos.",
        "problemas": [
            {"Problema": "Producto rayado", "Descripción": "Tazas llegan con rayones visibles", "Incidencias": 25},
            {"Problema": "Mal ensamblaje", "Descripción": "La tapa no cierra correctamente", "Incidencias": 18},
            {"Problema": "Demora en entrega", "Descripción": "Los pedidos llegan tarde", "Incidencias": 30},
            {"Problema": "Fuga por válvula", "Descripción": "Las tazas gotean durante su uso", "Incidencias": 12},
            {"Problema": "Atención al cliente", "Descripción": "Respuestas tardías o poco útiles", "Incidencias": 9},
            {"Problema": "Empaque deficiente", "Descripción": "Cajas dañadas o sin instrucciones", "Incidencias": 6}
        ]
    },
    "Clínica privada": {
        "descripcion": "Una clínica ha recibido varias quejas de pacientes sobre la atención médica, los procesos administrativos y la limpieza.",
        "problemas": [
            {"Problema": "Retrasos en consultas", "Descripción": "El doctor tarda en atender", "Incidencias": 22},
            {"Problema": "Errores en facturación", "Descripción": "Cobros incorrectos", "Incidencias": 16},
            {"Problema": "Falta de camas", "Descripción": "No hay disponibilidad", "Incidencias": 24},
            {"Problema": "Mal trato del personal", "Descripción": "Falta de empatía", "Incidencias": 15},
            {"Problema": "Errores en recetas", "Descripción": "Medicamentos equivocados", "Incidencias": 12},
            {"Problema": "Poca limpieza", "Descripción": "Quejas por sanitarios", "Incidencias": 7}
        ]
    },
    "Tienda online": {
        "descripcion": "Una plataforma de ventas en línea enfrenta quejas constantes relacionadas con el proceso de entrega y postventa.",
        "problemas": [
            {"Problema": "Retraso en entregas", "Descripción": "Llegan después de la fecha", "Incidencias": 28},
            {"Problema": "Producto equivocado", "Descripción": "No coincide con lo comprado", "Incidencias": 21},
            {"Problema": "Falla en pagos", "Descripción": "Problemas con tarjeta o PayPal", "Incidencias": 10},
            {"Problema": "Atención por chat lenta", "Descripción": "Soporte tarda en responder", "Incidencias": 12},
            {"Problema": "Producto dañado", "Descripción": "Empaque o contenido roto", "Incidencias": 18},
            {"Problema": "Dificultad para devolver", "Descripción": "Proceso complicado", "Incidencias": 8}
        ]
    }
}

# Selección del escenario
escenario = st.selectbox("📌 Selecciona un escenario:", list(escenarios.keys()))
descripcion = escenarios[escenario]["descripcion"]
problemas = escenarios[escenario]["problemas"]

st.markdown(f"### 📝 Descripción del escenario seleccionado:")
st.info(descripcion)

# Mezclar aleatoriamente una sola vez por escenario
if "mezcla" not in st.session_state or st.session_state.escenario_actual != escenario:
    st.session_state.mezcla = random.sample(problemas, len(problemas))
    st.session_state.escenario_actual = escenario

problemas_mezclados = st.session_state.mezcla

st.markdown("### 🎯 Asigna una prioridad (1–10) a cada problema según tu percepción:")

entradas = []
for i, item in enumerate(problemas_mezclados):
    prioridad = st.slider(
        f"({item['Problema']} – {item['Incidencias']} quejas) {item['Descripción']}",
        min_value=1, max_value=10, value=10 - i, key=f"{escenario}_{i}"
    )
    entradas.append({
        "Problema": item["Problema"],
        "Incidencias": item["Incidencias"],
        "Prioridad": prioridad
    })

# Evaluación
if st.button("📊 Evaluar mi diagnóstico"):
    df_usuario = pd.DataFrame(entradas)
    df_usuario = df_usuario.sort_values(by=["Prioridad", "Incidencias"], ascending=[False, False])
    df_usuario["Acumulado"] = df_usuario["Incidencias"].cumsum()
    df_usuario["% Acumulado"] = 100 * df_usuario["Acumulado"] / df_usuario["Incidencias"].sum()

    # Gráfico del usuario
    st.markdown("## 🔍 Tu Diagrama de Pareto")
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_usuario["Problema"],
        y=df_usuario["Incidencias"],
        name="Incidencias",
        marker_color="blue"
    ))
    fig.add_trace(go.Scatter(
        x=df_usuario["Problema"],
        y=df_usuario["% Acumulado"],
        name="% Acumulado",
        yaxis="y2",
        mode="lines+markers",
        marker=dict(color="red")
    ))
    fig.update_layout(
        title="Diagrama de Pareto (según tus prioridades)",
        xaxis=dict(title="Problemas"),
        yaxis=dict(title="Incidencias"),
        yaxis2=dict(
            title="% Acumulado",
            overlaying="y",
            side="right",
            range=[0, 110]
        )
    )
    st.plotly_chart(fig)

    # Comparación con datos reales
    df_real = pd.DataFrame(problemas)
    df_real = df_real.sort_values(by="Incidencias", ascending=False)
    df_real["Acumulado"] = df_real["Incidencias"].cumsum()
    df_real["% Acumulado"] = 100 * df_real["Acumulado"] / df_real["Incidencias"].sum()

    top_real = df_real[df_real["% Acumulado"] <= 80]["Problema"].tolist()
    top_usuario = df_usuario.head(len(top_real))["Problema"].tolist()
    aciertos = len(set(top_real) & set(top_usuario))

    st.markdown("### 📈 Análisis de tu priorización:")
    st.write(f"Problemas clave reales (cubren el 80 %): {', '.join(top_real)}")
    st.write(f"Tú priorizaste correctamente **{aciertos} de {len(top_real)}** problemas clave.")

    if aciertos == len(top_real):
        st.success("🎉 ¡Excelente! Tu análisis se alinea perfectamente con los datos reales.")
    elif aciertos >= len(top_real) // 2:
        st.warning("🔎 Aceptable. Identificaste algunos problemas importantes, pero podrías mejorar tu enfoque.")
    else:
        st.error("⚠️ Tus prioridades se alejaron de los datos reales. Revisa bien los patrones de ocurrencia.")

    with st.expander("📊 Ver Diagrama de Pareto Real"):
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=df_real["Problema"],
            y=df_real["Incidencias"],
            name="Incidencias",
            marker_color="green"
        ))
        fig2.add_trace(go.Scatter(
            x=df_real["Problema"],
            y=df_real["% Acumulado"],
            name="% Acumulado",
            yaxis="y2",
            mode="lines+markers",
            marker=dict(color="darkred")
        ))
        fig2.update_layout(
            title="Diagrama de Pareto Real (según datos)",
            xaxis=dict(title="Problemas"),
            yaxis=dict(title="Incidencias"),
            yaxis2=dict(
                title="% Acumulado",
                overlaying="y",
                side="right",
                range=[0, 110]
            )
        )
        st.plotly_chart(fig2)
