
import streamlit as st
import pandas as pd
from datetime import datetime
from qp_generator import QualityPlanGenerator
from pdf_generator import generate_qp_pdf
import os

st.set_page_config(page_title="GMPI - Générateur QP", layout="wide")
generator = QualityPlanGenerator()

st.title("🏭 GLOBAL METALLIC PRODUCT INDUSTRIES")
st.subheader("Générateur automatique de Quality Plan (FO-24-PRO)")

mode = st.sidebar.radio("Mode de saisie", ["📄 Importer un OF", "✏️ Saisie manuelle"])

if mode == "📄 Importer un OF":
    uploaded = st.file_uploader("Déposez votre fichier OF", type=['txt','pdf','doc','docx'])
    if uploaded:
        content = uploaded.read().decode('utf-8', errors='ignore') if uploaded.type == "text/plain" else uploaded.name
        of_data = generator.parse_of_file(content)
        st.success("Fichier importé")
        st.json(of_data)
else:
    with st.form("manual"):
        col1, col2 = st.columns(2)
        with col1:
            customer = st.text_input("Client", "NUMHYD")
            order = st.text_input("N° Commande", "4500766320")
            wo = st.text_input("N° WO", "WO-2023-001")
        with col2:
            product = st.text_input("Produit", "ADAPTER FLANGE 3 1/16\" 10K")
            grade = st.text_input("Grade", "AISI 4130")
            std = st.selectbox("Standard", ["API 6A", "API 5CT", "API 7-1"])
        psl = st.selectbox("PSL", ["1","2","3","4"])
        submit = st.form_submit_button("Générer")
        if submit:
            of_data = {
                'raw_text': f"{product} {grade} {std} PSL{psl}",
                'customer': customer,
                'order_no': order,
                'wo_no': wo,
                'product': product,
                'grade': grade,
                'date': datetime.now().strftime("%d/%m/%Y")
            }

if 'of_data' in locals():
    st.divider()
    with st.spinner("Génération..."):
        ops, material = generator.generate_operations(of_data)
    st.dataframe(pd.DataFrame(ops), use_container_width=True)
    
    qcp_ref = f"QCP-{of_data['wo_no']}-{datetime.now().strftime('%Y%m%d')}"
    if st.button("📥 Générer PDF"):
        pdf = generate_qp_pdf(ops, of_data, qcp_ref, material)
        with open(pdf, "rb") as f:
            st.download_button("Télécharger PDF", f, file_name=f"QP_{of_data['wo_no']}.pdf")
