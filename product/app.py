import streamlit as st
from model import MedDRAMatcher
from drug_extractor import extract_drugs
import pandas as pd


@st.cache_data
def load_drug_knowledge():
    return pd.read_csv("data/adr_drug_knowledge.csv")

drug_kb = load_drug_knowledge()

st.set_page_config(
    page_title="ADR → MedDRA Standardizer",
    page_icon="💊",
    layout="wide"
)

st.title("💊 ADR to MedDRA Standardization")
st.caption("ADR normalization + optional drug association (research prototype)")

@st.cache_resource
def load_model():
    return MedDRAMatcher("data/meddra_terms.csv")

matcher = load_model()

st.subheader("Enter clinical text / patient narrative")
text = st.text_area(
    "Example: After taking atorvastatin, I experienced severe pain in calf muscles",
    height=120
)

top_k = st.slider("Top-K MedDRA predictions", 1, 10, 5)

if st.button("🔍 Analyze"):
    if text.strip() == "":
        st.warning("Please enter clinical text")
    else:
        # ---- Drug extraction ----
        drugs = extract_drugs(text)

        if drugs:
            detected_drug = drugs[0]
            drug_status = "Detected from user text"
        else:
            detected_drug = None
            drug_status = "Not reported by user"

        # ---- ADR → MedDRA ----
        st.subheader("🩺 MedDRA Standardization")
        results = matcher.predict(text, top_k)

    for i, r in enumerate(results, 1):
        # -------- Decide drug display FIRST --------
        if detected_drug:
            drug_display = f"**{detected_drug}** ({drug_status})"
        else:
            matches = drug_kb[
                drug_kb["pt_name"].str.lower() == r["pt_name"].lower()
            ]

            if not matches.empty:
                drug_display = matches.iloc[0]["common_drugs"] + " (reference)"
            else:
                drug_display = "No reference drugs available"

        # -------- NOW display --------
        st.markdown(
            f"""
            ### {i}. {r['pt_name']}
            **PT Code:** `{r['pt_code']}`  
            **Similarity Score:** `{r['score']:.4f}`  

            💊 **Associated medicine(s):** {drug_display}
            """
        )



# Note: This is a research prototype and not for clinical use.
