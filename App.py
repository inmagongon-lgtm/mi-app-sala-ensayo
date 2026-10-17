
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Gestión Sala de Ensayo",
    page_icon="🎸",
    layout="wide"
)

st.title("🎸 Gestión de mi sala de ensayo")
st.caption("Reservas, bonos, pagos y rentabilidad")

if "reservas" not in st.session_state:
    st.session_state.reservas = []

if "gastos" not in st.session_state:
    st.session_state.gastos = []

if "bonos" not in st.session_state:
    st.session_state.bonos = []

if "pagos" not in st.session_state:
    st.session_state.pagos = []

menu = st.sidebar.radio(
    "Menú",
    [
        "Resumen",
        "Reservas",
        "Bonos y horas",
        "Pagos",
        "Gastos"
    ]
)

if menu == "Resumen":
    st.header("📊 Resumen económico")

    ingresos = sum(p["importe"] for p in st.session_state.pagos)
    gastos = sum(g["importe"] for g in st.session_state.gastos)

    c1, c2, c3 = st.columns(3)
    c1.metric("Ingresos", f"{ingresos:.2f} €")
    c2.metric("Gastos", f"{gastos:.2f} €")
    c3.metric("Resultado", f"{ingresos-gastos:.2f} €")

    st.info("Añade tus reservas, pagos y gastos desde el menú.")

elif menu == "Reservas":
    st.header("📅 Nueva reserva")

    with st.form("reserva"):
        cliente = st.text_input("Nombre del cliente o grupo")
        fecha = st.date_input("Fecha")
        hora = st.time_input("Hora de inicio")
        duracion = st.number_input("Duración (horas)", 1, 24, 2)
        sala = st.selectbox("Sala", ["Sala Bowie", "Sala polivalente"])
        importe = st.number_input("Importe (€)", min_value=0.0, step=5.0)
        guardar = st.form_submit_button("Guardar reserva")

        if guardar:
            st.session_state.reservas.append({
                "cliente": cliente,
                "fecha": str(fecha),
                "hora": str(hora),
                "duracion": duracion,
                "sala": sala,
                "importe": importe
            })
            st.success("Reserva guardada")

    if st.session_state.reservas:
        st.dataframe(pd.DataFrame(st.session_state.reservas),
                     use_container_width=True)

elif menu == "Bonos y horas":
    st.header("🎟️ Bonos")

    with st.form("bono"):
        cliente = st.text_input("Cliente o grupo")
        horas = st.number_input("Horas compradas", 1, 100, 10)
        precio = st.number_input("Precio del bono (€)", min_value=0.0)
        consumidas = st.number_input("Horas consumidas", 0, 100, 0)
        guardar = st.form_submit_button("Guardar bono")

        if guardar:
            st.session_state.bonos.append({
                "cliente": cliente,
                "horas_compradas": horas,
                "horas_consumidas": consumidas,
                "horas_restantes": horas-consumidas,
                "precio": precio
            })
            st.success("Bono guardado")

    if st.session_state.bonos:
        st.dataframe(pd.DataFrame(st.session_state.bonos),
                     use_container_width=True)

elif menu == "Pagos":
    st.header("💶 Registrar pago")

    with st.form("pago"):
        cliente = st.text_input("Cliente")
        fecha = st.date_input("Fecha de pago")
        concepto = st.text_input("Concepto")
        importe = st.number_input("Importe (€)", min_value=0.0)
        metodo = st.selectbox("Método", ["Bizum", "Efectivo", "Transferencia"])
        guardar = st.form_submit_button("Guardar pago")

        if guardar:
            st.session_state.pagos.append({
                "cliente": cliente,
                "fecha": str(fecha),
                "concepto": concepto,
                "importe": importe,
                "metodo": metodo
            })
            st.success("Pago guardado")

    if st.session_state.pagos:
        st.dataframe(pd.DataFrame(st.session_state.pagos),
                     use_container_width=True)

elif menu == "Gastos":
    st.header("🧾 Registrar gasto")

    with st.form("gasto"):
        concepto = st.text_input("Concepto del gasto")
        fecha = st.date_input("Fecha del gasto")
        importe = st.number_input("Importe (€)", min_value=0.0)
        guardar = st.form_submit_button("Guardar gasto")

        if guardar:
            st.session_state.gastos.append({
                "concepto": concepto,
                "fecha": str(fecha),
                "importe": importe
            })
            st.success("Gasto guardado")

    if st.session_state.gastos:
        st.dataframe(pd.DataFrame(st.session_state.gastos),
                     use_container_width=True)
