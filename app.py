import streamlit as st
import pandas as pd

# Configurazione grafica della pagina
st.set_page_config(page_title="Digital Card", page_icon="📇", layout="centered")

# Funzione per generare il tracciato vCard (.vcf) con Azienda dinamica
def generate_vcard(nome, cognome, azienda, ruolo, telefono, email):
    vcard = f"""BEGIN:VCARD
VERSION:3.0
N:{cognome};{nome};;;
FN:{nome} {cognome}
ORG:{azienda}
TITLE:{ruolo}
TEL;TYPE=WORK,VOICE:{telefono}
EMAIL;TYPE=WORK:{email}
END:VCARD"""
    return vcard

# Caricamento del database Excel
@st.cache_data
def load_data():
    try:
        # Il file team.xlsx deve ora contenere la colonna 'Azienda'
        df = pd.read_excel("team.xlsx")
        df["ID"] = df["ID"].astype(str).str.lower()
        return df
    except FileNotFoundError:
        st.error("File 'team.xlsx' non trovato. Crealo per caricare il database dei contatti.")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    query_params = st.query_params
    
    if "id" in query_params:
        contact_id = query_params["id"].lower()
        
        user_data = df[df["ID"] == contact_id]
        
        if not user_data.empty:
            user = user_data.iloc[0]
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Intestazione con nome, ruolo e Azienda dinamica
            st.title(f"{user['Nome']} {user['Cognome']}")
            st.subheader(f"{user['Ruolo']}")
            st.caption(f"🏢 {user['Azienda']}")
            
            st.divider()
            
            st.markdown(f"**📞 Telefono:** {user['Telefono']}")
            st.markdown(f"**✉️ Email:** {user['Email']}")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Generazione dinamica della vCard
            vcard_content = generate_vcard(
                user['Nome'], 
                user['Cognome'],
                user['Azienda'], 
                user['Ruolo'], 
                user['Telefono'], 
                user['Email']
            )
            
            st.download_button(
                label="💾 Salva in Rubrica",
                data=vcard_content,
                file_name=f"{user['Nome']}_{user['Cognome']}.vcf",
                mime="text/vcard",
                use_container_width=True
            )
            
        else:
            st.warning("Nessun contatto trovato con questo ID.")
    else:
        st.info("Avvicina la card NFC al telefono per caricare i dati del contatto.")