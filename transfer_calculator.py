import streamlit as st
import time

# Constantes de conversion
# 1 Octet = 8 bits
BITS_PER_BYTE = 8

# Pré-calcul des facteurs pour simplifier la logique
# Taille : Mo ou Go -> Octets
MB_TO_BYTES = 1024 * 1024
GB_TO_BYTES = 1024 * 1024 * 1024

# Vitesse : Mbps ou Gbps -> bits/seconde (base décimale 1000 pour les débits réseau)
MBPS_TO_BPS = 1_000_000  # 10^6
GBPS_TO_BPS = 1_000_000_000 # 10^9

def calculate_time(file_size_val, file_size_unit, link_speed_val, link_speed_unit, overhead_percent):
    """Calcule le temps de transfert théorique."""
    
    # 1. Conversion de la taille du fichier en OCTETS
    if file_size_unit == 'Mo':
        size_bytes = file_size_val * MB_TO_BYTES
    else: # 'Go'
        size_bytes = file_size_val * GB_TO_BYTES
        
    # 2. Application de l'overhead (surcharge, ex: en-têtes TCP/IP)
    overhead_factor = 1 + (overhead_percent / 100)
    total_size_bytes = size_bytes * overhead_factor
    
    # 3. Conversion de la taille en BITS
    total_size_bits = total_size_bytes * BITS_PER_BYTE
    
    # 4. Conversion de la vitesse en BITS PAR SECONDE
    if link_speed_unit == 'Mbps':
        speed_bps = link_speed_val * MBPS_TO_BPS
    else: # 'Gbps'
        speed_bps = link_speed_val * GBPS_TO_BPS
        
    # Gestion du cas où la vitesse est zéro
    if speed_bps == 0:
        return 0, "Vitesse du lien ne peut être zéro."
    
    # 5. Calcul du temps
    time_seconds = total_size_bits / speed_bps
    
    return time_seconds, None

def format_time(seconds):
    """Convertit le temps en secondes en un format lisible (h:m:s)."""
    if seconds == 0:
        return "N/A"
        
    # time.gmtime(seconds) retourne un objet struct_time en UTC (ignore les fuseaux horaires)
    # C'est parfait pour formater une durée
    if seconds < 60:
        # Affiche simplement les secondes avec 3 décimales pour les transferts très rapides
        return f"**{seconds:,.3f}** secondes"
    elif seconds < 3600:
        # Format Minutes et Secondes
        minutes = int(seconds // 60)
        remaining_seconds = seconds % 60
        return f"**{minutes}** minute(s) et **{remaining_seconds:,.2f}** secondes"
    else:
        # Format Heures, Minutes et Secondes
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        remaining_seconds = seconds % 60
        return f"**{hours}** heure(s), **{minutes}** minute(s) et **{remaining_seconds:,.2f}** secondes"

# --- Interface Streamlit ---
st.set_page_config(
    page_title="Calculateur de Temps de Transfert CCNA", 
    layout="centered"
)

st.title("Projet réalisé par Farah ghazouani, Arij Ben Rabiaa, Mayssa Laribi")
st.title("2ING1")
st.title("⏱️ Calculateur de Temps de Transfert Théorique")
st.markdown("---")

# --- Barre Latérale pour les Options (Surcharge) ---
with st.sidebar:
    st.header("⚙️ Options de Calcul")
    overhead = st.slider(
        "Surcharge Protocolaire (Overhead)",
        min_value=0,
        max_value=20,
        value=10,
        step=1,
        help="Pourcentage de données supplémentaires (en-têtes TCP/IP, etc.) à ajouter à la taille du fichier."
    )
    st.info(f"Surcharge appliquée : **{overhead}%**")
    st.markdown("---")
    st.caption("Projet CCNA Streamlit - Gemini 'Coding Engine'")


# --- Entrées Principales ---

st.header("1. Taille du Fichier à Transférer")
col1_size, col2_size = st.columns([3, 1])

with col1_size:
    file_size = st.number_input(
        "Valeur de la Taille",
        min_value=0.01,
        value=1.5,
        step=0.1,
        format="%f",
        key="size_val",
        help="Entrez la taille du fichier."
    )

with col2_size:
    file_unit = st.selectbox(
        "Unité",
        ('Go', 'Mo'),
        index=0,
        key="size_unit"
    )

st.header("2. Vitesse du Lien Réseau")
col1_speed, col2_speed = st.columns([3, 1])

with col1_speed:
    link_speed = st.number_input(
        "Valeur de la Vitesse",
        min_value=0.01,
        value=100.0,
        step=10.0,
        format="%f",
        key="speed_val",
        help="Entrez le débit maximal du lien."
    )

with col2_speed:
    speed_unit = st.selectbox(
        "Unité",
        ('Mbps', 'Gbps'),
        index=0,
        key="speed_unit"
    )

st.markdown("---")

# --- Calcul et Affichage du Résultat ---
time_result, error = calculate_time(file_size, file_unit, link_speed, speed_unit, overhead)

st.header("🚀 Résultat du Transfert")

if error:
    st.error(f"Erreur de Calcul : {error}")
else:
    # Affichage du temps
    st.metric(
        label="Temps de Transfert Estimé", 
        value=format_time(time_result)
    )
    
    # Affichage des détails techniques
    with st.expander("Détails Techniques du Calcul"):
        st.write("Le calcul est basé sur la formule : Temps = (Taille du Fichier en bits) / (Vitesse du Lien en bits/seconde).")
        st.markdown(f"* Taille totale avec **{overhead}%** d'overhead : **{file_size * (1 + overhead / 100):,.2f} {file_unit}**")
        st.markdown(f"* Vitesse du lien utilisée : **{link_speed} {speed_unit}**")
        st.info("Le code utilise la norme décimale (base 1000) pour les débits réseau (Mbps/Gbps) et la norme binaire (base 1024) pour les tailles de fichier (Mo/Go), conformément aux pratiques courantes du réseau.")