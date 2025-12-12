# Natale 3D Streamlit

Una piccola web app di auguri di Natale realizzata con Streamlit e Plotly 3D: un albero multilivello con chioma più realistica, palline, lucine, pacchi regalo, fiocchi di neve e un messaggio romantico personalizzabile.

## Controlli 3D
- Trascina con mouse o dito per ruotare la scena in 3D (dragmode orbit).
- Usa scroll o pinch per zoommare e doppio click per resettare la vista.

## Come eseguire in locale
1. Clona questa repository.
2. (Opzionale) crea un ambiente virtuale: `python -m venv .venv && source .venv/bin/activate`.
3. Installa le dipendenze: `pip install -r requirements.txt`.
4. Avvia l'app: `streamlit run app.py`.

## Personalizzazione rapida
- Modifica i testi in cima a `app.py` dove trovi i commenti in maiuscolo.
- Usa gli slider per numero di palline, altezza albero, brillantezza lucine e dimensione dei regali.
- Se vuoi usare un modello 3D gratuito (OBJ/STL) scaricato online, puoi caricarlo nella cartella del progetto e sostituire la funzione `crea_cono_albero` con un `go.Mesh3d` basato sui vertici del tuo file (senza dipendenze aggiuntive) oppure affiancarlo ai livelli già presenti.

## Pubblicazione su Streamlit Community Cloud
1. Carica questa cartella su un repository GitHub.
2. Vai su [Streamlit Community Cloud](https://streamlit.io/cloud) e collega il repository.
3. Seleziona `app.py` come file principale.
4. Distribuisci l'app e condividi il link con chi ami.
