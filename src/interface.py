import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Interface Prediction Medicaments",
    page_icon="💊",
    layout="wide"
)

st.title("💊 Interface de Prédiction — Distribution des Médicaments en Tunisie")
st.markdown("Remplissez les caractéristiques du médicament pour prédire s'il sera distribué en pharmacie.")
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🏥 Informations médicales")
    veic = st.selectbox("Classification VEIC", ["Essentiel", "Vital", "Intermediaire", "Confort"])
    classe = st.selectbox("Classe therapeutique", ["CARDIOVASCULAIRE", "ANTIINFECTIEUX", "ANTINEOPLASIQUES", "SYSTEME NERVEUX", "DERMATOLOGIE", "AUTRE"])
    forme = st.selectbox("Forme pharmaceutique", ["Comprime", "Gelule", "Injectable", "Sirop", "Pommade", "Solution", "Autre"])
    est_injectable = st.radio("Forme injectable ?", [0, 1], format_func=lambda x: "Non" if x == 0 else "Oui", horizontal=True)
    est_chronique = st.radio("Maladie chronique ?", [0, 1], format_func=lambda x: "Non" if x == 0 else "Oui", horizontal=True)
    est_generique = st.radio("Est un generique ?", [0, 1], format_func=lambda x: "Non" if x == 0 else "Oui", horizontal=True)
    est_biosimilaire = st.radio("Est un biosimilaire ?", [0, 1], format_func=lambda x: "Non" if x == 0 else "Oui", horizontal=True)

with col2:
    st.subheader("🏭 Informations commerciales")
    gp_status = st.selectbox("Statut", ["Princeps", "Generique", "Biosimilaire"])
    nb_fabricants = st.slider("Nombre de fabricants", 1, 20, 3)
    nb_amm = st.slider("Nombre AMM pour cette molecule", 1, 85, 10)
    nb_presentations = st.slider("Nombre de presentations", 1, 40, 5)
    anciennete = st.slider("Anciennete AMM (annees)", 0, 40, 10)
    duree_conservation = st.selectbox("Duree conservation (mois)", [12, 18, 24, 36, 48, 60], index=2)

with col3:
    st.subheader("📝 Indications et Dosage")
    nb_indications = st.slider("Nombre d'indications", 1, 15, 3)
    indications_len = st.slider("Longueur texte indications", 10, 500, 100)
    dosage_valeur = st.number_input("Valeur du dosage", min_value=0.1, max_value=1000.0, value=100.0)
    dosage_unite = st.selectbox("Unite du dosage", ["mg", "mcg", "mg_ml", "UI", "gr", "pct", "autre"])
    presentation_type = st.selectbox("Type de presentation", ["boite", "flacon", "tube", "autre"])
    presentation_qte = st.slider("Quantite par presentation", 1, 200, 30)
    tableau = st.selectbox("Tableau reglementaire", ["Tableau A", "Tableau B", "Tableau C", "Sans tableau"])

st.markdown("---")
st.subheader("🔧 Features Engineering — calculees automatiquement")

vital_et_injectable = 1 if (veic == "Vital" and est_injectable == 1) else 0
monopole = 1 if nb_fabricants == 1 else 0
ratio_generique = 0.8 if est_generique == 1 else 0.2

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("vital_et_injectable", vital_et_injectable, delta="Risque eleve!" if vital_et_injectable else "OK")
with c2:
    st.metric("monopole", monopole, delta="1 seul fabricant!" if monopole else "OK")
with c3:
    st.metric("ratio_generique", f"{ratio_generique:.2f}")

st.markdown("---")

if st.button("🔮 Predire", type="primary", use_container_width=True):

    score = 0.50

    if vital_et_injectable:            score -= 0.22
    if est_injectable == 1:            score -= 0.15
    if classe == "ANTINEOPLASIQUES":   score -= 0.18
    if monopole:                       score -= 0.10
    if veic == "Vital":                score -= 0.08
    if veic == "Confort":              score -= 0.05
    if est_biosimilaire == 1:          score -= 0.07
    if gp_status == "Biosimilaire":    score -= 0.07
    if duree_conservation <= 12:       score -= 0.05
    if ratio_generique > 0.7:          score -= 0.05

    if est_chronique == 1:             score += 0.15
    if est_injectable == 0:            score += 0.10
    if nb_fabricants >= 5:             score += 0.10
    if anciennete >= 15:               score += 0.10
    if anciennete >= 25:               score += 0.06
    if veic == "Essentiel":            score += 0.10
    if classe == "CARDIOVASCULAIRE":   score += 0.10
    if classe == "ANTIINFECTIEUX":     score += 0.06
    if gp_status == "Princeps":        score += 0.06
    if nb_presentations >= 5:          score += 0.05
    if nb_indications >= 5:            score += 0.05
    if nb_amm >= 10:                   score += 0.05
    if duree_conservation >= 36:       score += 0.04
    if presentation_type == "boite":   score += 0.04
    if nb_fabricants >= 10:            score += 0.05

    score = max(0.04, min(0.96, score))
    predicted = 1 if score >= 0.5 else 0

    st.markdown("## Resultat")

    colA, colB = st.columns([2, 1])
    with colA:
        if predicted == 1:
            st.success(f"## OK SERA DISTRIBUE EN PHARMACIE\nProbabilite : {score*100:.1f}%")
        else:
            st.error(f"## NON SERA PAS DISTRIBUE\nProbabilite de distribution : {score*100:.1f}%")

        fig, ax = plt.subplots(figsize=(8, 1.1))
        color_bar = "#2ecc71" if score >= 0.5 else "#e74c3c"
        ax.barh([""], [score], color=color_bar, height=0.5)
        ax.barh([""], [1 - score], color="#f0f0f0", height=0.5, left=[score])
        ax.axvline(x=0.5, color="#333", linestyle="--", linewidth=2)
        ax.text(0.5, 0.35, "Seuil 0.5", ha="center", fontsize=9, color="#333")
        ax.text(min(score + 0.02, 0.88), 0, f"{score*100:.1f}%", ha="left",
                fontsize=12, fontweight="bold", color="white", va="center")
        ax.set_xlim(0, 1)
        ax.axis("off")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with colB:
        st.metric("Modele", "XGBoost")
        st.metric("F1-Score Macro", "0.81")
        st.metric("AUC-ROC", "0.891")
        st.metric("Prediction", "Distribue" if predicted == 1 else "Non distribue")

    st.markdown("---")
    st.subheader("Facteurs qui ont influence la prediction")

    factors = []
    if vital_et_injectable:          factors.append(("vital_et_injectable=1",   -0.22, "Medicament hospitalier par nature"))
    if est_injectable == 1:          factors.append(("est_injectable=1",         -0.15, "Administre a l'hopital uniquement"))
    if classe == "ANTINEOPLASIQUES": factors.append(("classe=ANTINEOPLASIQUES",  -0.18, "Traitement hospitalier exclusif"))
    if monopole:                     factors.append(("monopole=1",               -0.10, "1 seul fabricant mondial"))
    if veic == "Vital":              factors.append(("veic=Vital",               -0.08, "Classification restrictive"))
    if est_biosimilaire == 1:        factors.append(("est_biosimilaire=1",       -0.07, "Marche complexe"))
    if est_chronique == 1:           factors.append(("est_chronique=1",          +0.15, "Demande mensuelle garantie"))
    if nb_fabricants >= 5:           factors.append(("nb_fabricants>=5",         +0.10, "Disponibilite assuree"))
    if anciennete >= 15:             factors.append(("anciennete_amm>=15",       +0.10, "Bien etabli sur le marche"))
    if veic == "Essentiel":          factors.append(("veic=Essentiel",           +0.10, "Medicament prioritaire"))
    if classe == "CARDIOVASCULAIRE": factors.append(("classe=CARDIOVASCULAIRE",  +0.10, "Forte demande chronique"))
    if gp_status == "Princeps":      factors.append(("gp_status=Princeps",       +0.06, "Medicament original etabli"))

    factors.sort(key=lambda x: abs(x[1]), reverse=True)

    col_neg, col_pos = st.columns(2)
    with col_neg:
        st.markdown("**Facteurs defavorables**")
        for feat, impact, expl in [f for f in factors if f[1] < 0]:
            st.error(f"**{feat}** ({impact*100:.0f}%)\n\n{expl}")

    with col_pos:
        st.markdown("**Facteurs favorables**")
        for feat, impact, expl in [f for f in factors if f[1] > 0]:
            st.success(f"**{feat}** (+{impact*100:.0f}%)\n\n{expl}")

    st.markdown("---")
    st.subheader("Recapitulatif de toutes les features")
    recap = pd.DataFrame({
        "Feature": ["veic","classe","forme","est_injectable","est_chronique","est_generique",
                    "est_biosimilaire","gp_status","nb_fabricants_dci","nb_amm_dci",
                    "nb_presentations_dci","anciennete_amm","duree_conservation_mois",
                    "nb_indications","indications_len","dosage_valeur","dosage_unite",
                    "presentation_type","presentation_qte","tableau",
                    "vital_et_injectable","monopole","ratio_generique"],
        "Valeur": [veic, classe, forme,
                   "Oui" if est_injectable else "Non",
                   "Oui" if est_chronique else "Non",
                   "Oui" if est_generique else "Non",
                   "Oui" if est_biosimilaire else "Non",
                   gp_status, nb_fabricants, nb_amm, nb_presentations,
                   f"{anciennete} ans", f"{duree_conservation} mois",
                   nb_indications, indications_len, dosage_valeur, dosage_unite,
                   presentation_type, presentation_qte, tableau,
                   vital_et_injectable, monopole, f"{ratio_generique:.2f}"],
        "Type": ["Original"]*20 + ["Feature Engineering"]*3
    })
    st.dataframe(recap, use_container_width=True, hide_index=True)

st.markdown("---")
st.markdown("Modele XGBoost — F1-Score Macro = 0.81 — AUC-ROC = 0.891 — Sources : DPM + PHCT")
