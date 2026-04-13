# 💊 Prédiction du Risque de Distribution des Médicaments en Tunisie

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/XGBoost-2.0-FF6600?style=for-the-badge&logo=xgboost&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-1.29-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white"/>
  <img src="https://img.shields.io/badge/F1--Score-0.81-27AE60?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/AUC--ROC-0.891-2ECC71?style=for-the-badge"/>
</p>

---

## 👤 Auteur

**Ferdaous Ben Taleb**
Projet Machine Learning — Ecole Polytechnique de Sousse
Année académique : 2025-2026

---

## 📋 Description du Projet

Ce projet prédit si un médicament autorisé en Tunisie sera effectivement distribué en pharmacie.

Sur **6 053 médicaments** ayant obtenu une Autorisation de Mise sur le Marché (AMM) officielle,
**1 695 (28%)** ne sont jamais distribués en pharmacie malgré leur autorisation légale.

Ce projet construit un modèle de **classification binaire supervisée** pour prédire ce risque
à partir des caractéristiques du médicament, avant sa commercialisation.

**Variable cible :** `reaches_pharmacy`
- `1` → Le médicament est distribué en pharmacie
- `0` → Le médicament n'est jamais distribué en pharmacie

---

## 📊 Dataset et Sources

| Propriété | Valeur |
|-----------|--------|
| Nombre de médicaments | 6 053 |
| Nombre de features | 28 |
| Médicaments distribués | 4 358 (72%) |
| Médicaments non distribués | 1 695 (28%) |
| Déséquilibre | 72% / 28% |

**Sources :**
- 🏥 **DPM** (Direction de la Pharmacie et du Médicament) — dpm.tn
- 💊 **PHCT** (Pharmacies tunisiennes) — phct.com.tn

**Méthode de collecte :** Web scraping Python (BeautifulSoup + Requests)

---

## ❓ Problématique

Un laboratoire pharmaceutique tunisien développe un médicament et obtient l'AMM officielle de l'État.

**Problème :** Il ne sait pas si ce médicament sera distribué en pharmacie ou non.
**Impact :** 28% des autorisations accordées restent sans distribution — investissement perdu, patients non soignés.

**Solution proposée :** Un modèle XGBoost qui prédit, à partir des 27 caractéristiques du médicament,
la probabilité qu'il soit distribué en pharmacie — **avant la commercialisation**.

---

## 🗂️ Structure du Projet

```
projet-ml-medicaments/
│
├── notebooks/
│   ├── 01_EDA_Pretraitement.ipynb     # Analyse exploratoire + prétraitement
│   └── 02_Modelisation.ipynb          # Modélisation + évaluation + SHAP
│
├── src/
│   └── interface.py                   # Application Streamlit (prédiction)
│
├── data_ml/                           # Données prétraitées (générées automatiquement)
│   ├── X_train_sm.pkl
│   ├── y_train_sm.pkl
│   ├── X_test.pkl
│   └── y_test.pkl
│
├── README.md                          # Ce fichier
├── requirements.txt                   # Dépendances Python
├── environment.yml                    # Environnement Conda
└── .gitignore                         # Fichiers à ignorer par Git
```

---

## ⚙️ Guide d'Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/ferdaous-bt/risque-distribution-pharma-tn
cd medicaments-tunisie-ml
```

### 2. Option A — Avec pip

```bash
python -m venv env
source env/bin/activate        # Linux / Mac
env\Scripts\activate           # Windows

pip install -r requirements.txt
```

### 3. Option B — Avec Conda

```bash
conda env create -f environment.yml
conda activate medicaments-ml
```

### 4. Lancer les notebooks dans l'ordre

```bash
jupyter notebook
```

Ouvrir et exécuter dans l'ordre :
1. `notebooks/01_EDA_Pretraitement.ipynb`
2. `notebooks/02_Modelisation.ipynb`

### 5. Lancer l'interface Streamlit

```bash
streamlit run src/interface.py
```

L'interface s'ouvre sur : http://localhost:8501

---

## 🔬 Pipeline ML

```
Collecte (Web Scraping)
        |
        v
EDA — Analyse Exploratoire
  - Statistiques descriptives
  - Visualisation distributions
  - Identification valeurs manquantes
  - Matrice de corrélation
        |
        v
Prétraitement
  - Nettoyage (doublons, NaN, colonnes inutiles)
  - Feature Engineering
      * vital_et_injectable  (raison médicale)
      * monopole             (raison commerciale)
      * ratio_generique      (raison concurrentielle)
  - Encodage (Ordinal, One-Hot, Label)
  - Split Train/Test 80/20 avec stratify=y
  - SMOTE (équilibrage — train uniquement)
  - Normalisation StandardScaler
        |
        v
Modélisation
  - Régression Logistique (baseline)
  - Random Forest + RandomizedSearchCV
  - XGBoost + RandomizedSearchCV
        |
        v
Évaluation
  - F1-Score Macro (métrique principale)
  - AUC-ROC
  - Matrice de Confusion
        |
        v
Interprétation — SHAP Values
```

---

## 📈 Résultats

### Comparaison des 3 modèles

| Modèle | F1-Score Macro | AUC-ROC |
|--------|---------------|---------|
| Régression Logistique | 0.62 | 0.684 |
| Random Forest | 0.80 | 0.897 |
| **XGBoost** ⭐ | **0.81** | **0.891** |

### Matrice de confusion — XGBoost

| | Prédit 0 | Prédit 1 |
|--|----------|----------|
| **Réel 0** | TN = 224 ✓ | FP = 111 ✗ |
| **Réel 1** | FN = 65 ✗  | TP = 811 ✓ |

### Top 5 features importantes (SHAP)

| Rang | Feature | Signification |
|------|---------|---------------|
| 1 | `anciennete_amm` | Ancienneté du médicament sur le marché |
| 2 | `laboratoire_enc` | Le laboratoire fabricant |
| 3 | `forme_enc` | La forme pharmaceutique |
| 4 | `veic_enc` | Classification VEIC |
| 5 | `dci_enc` | La molécule (DCI) |

---

## 🚀 Choix Techniques

| Composant | Choix | Justification |
|-----------|-------|---------------|
| Algorithme | XGBoost | Meilleur F1-Score sur données tabulaires déséquilibrées |
| Optimisation | RandomizedSearchCV | 20 combinaisons x 5-fold CV |
| Déséquilibre | SMOTE | Observations synthétiques — train uniquement |
| Métrique | F1-Score Macro | 2 classes à égalité malgré déséquilibre 72/28 |
| Interprétation | SHAP Values | Explique chaque prédiction individuelle |

---

## ⚠️ Points Clés Anti Data Leakage

- SMOTE appliqué uniquement sur X_train — jamais sur X_test
- StandardScaler : fit_transform sur train, transform seulement sur test
- ratio_generique calculé après le split, sur X_train uniquement
- vital_et_injectable et monopole créées avant l'encodage

---

## 📝 Licence

Projet académique — Ecole Polytechnique de Sousse — 2025-2026
