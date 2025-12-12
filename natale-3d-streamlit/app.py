import numpy as np
import plotly.graph_objects as go
import streamlit as st

# ================== CONFIGURAZIONE ==================
st.set_page_config(page_title="Buon Natale, amore", page_icon="🎄", layout="centered")

# ================== TESTI PERSONALIZZABILI ==================
# QUI PUOI CAMBIARE IL TITOLO
titolo_default = "🎄 Buon Natale, amore mio! 🎁"
# QUI PUOI CAMBIARE IL SOTTOTITOLO
sottotitolo_default = "Una piccola scena 3D per festeggiare insieme."
# MODIFICA QUI IL TESTO DEL TUO MESSAGGIO DI NATALE
messaggio_default = (
    "In questo albero ci sono le nostre luci, i nostri sogni e il calore che condividiamo. "
    "Grazie per rendere ogni giorno speciale: questo Natale è tutto per te."
)

TITOLO = titolo_default
SOTTOTITOLO = sottotitolo_default
MESSAGGIO = messaggio_default

# ================== FUNZIONI DI SUPPORTO ==================

def crea_cono_albero(altezza, raggio_base, z_offset, colore_principale, nome, rugosita=0.06, ondulazioni=6):
    """Crea una superficie conica leggermente irregolare per simulare rami più realistici."""
    theta = np.linspace(0, 2 * np.pi, 90)
    z = np.linspace(0, altezza, 60)
    theta_grid, z_grid = np.meshgrid(theta, z)

    # Piccola ondulazione per dare irregolarità al bordo dei rami
    ripple = 1 + rugosita * np.sin(ondulazioni * theta_grid) * np.cos(1.5 * np.pi * (z_grid / altezza))
    r_base = raggio_base * (1 - z_grid / altezza)
    r_grid = r_base * ripple

    x = r_grid * np.cos(theta_grid)
    y = r_grid * np.sin(theta_grid)
    z = z_grid + z_offset

    # Colori leggermente variabili lungo l'altezza per dare profondità
    colorscale = [
        [0, colore_principale],
        [1, "#1ca968"],
    ]

    return go.Surface(
        x=x,
        y=y,
        z=z,
        surfacecolor=z,
        colorscale=colorscale,
        showscale=False,
        opacity=0.98,
        lighting=dict(ambient=0.35, diffuse=0.75, roughness=0.4, specular=0.12),
        lightposition=dict(x=100, y=80, z=220),
        name=nome,
    )


def crea_cilindro_tronco(altezza, raggio, colore, z_offset=0.0, nome="Tronco"):
    theta = np.linspace(0, 2 * np.pi, 40)
    z = np.linspace(0, altezza, 10)
    theta_grid, z_grid = np.meshgrid(theta, z)
    x = raggio * np.cos(theta_grid)
    y = raggio * np.sin(theta_grid)
    z = z_grid + z_offset

    return go.Surface(
        x=x,
        y=y,
        z=z,
        colorscale=[[0, colore], [1, "#9b6c3c"]],
        showscale=False,
        opacity=1.0,
        lighting=dict(ambient=0.3, diffuse=0.65, specular=0.08, roughness=0.4),
        name=nome,
    )


def crea_pavimento(raggio=2.2, colore="#f3f5f9", z=0.0):
    theta = np.linspace(0, 2 * np.pi, 80)
    r = np.linspace(0, raggio, 30)
    r_grid, theta_grid = np.meshgrid(r, theta)
    x = r_grid * np.cos(theta_grid)
    y = r_grid * np.sin(theta_grid)
    z_grid = np.full_like(x, z)
    return go.Surface(
        x=x,
        y=y,
        z=z_grid,
        colorscale=[[0, colore], [1, colore]],
        showscale=False,
        opacity=0.95,
        lighting=dict(ambient=0.5, diffuse=0.5, roughness=0.9),
        name="Pavimento innevato",
    )


def genera_decorazioni(n_palline, livelli_info, brillantezza=1.0, seed=42):
    rng = np.random.default_rng(seed)
    x, y, z, colori, size = [], [], [], [], []
    palette = ["#b22222", "#d4af37", "#1e90ff", "#ff69b4", "#ffd700"]
    luci_palette = ["#fff7d6", "#fffacd", "#ffffe0"]

    for idx, info in enumerate(livelli_info):
        h, r_base, z0 = info
        n_level = max(5, n_palline // len(livelli_info))
        height_points = rng.uniform(0.1, h * 0.95, size=n_level)
        angles = rng.uniform(0, 2 * np.pi, size=n_level)
        radii = r_base * (1 - height_points / h)
        x.extend(radii * np.cos(angles))
        y.extend(radii * np.sin(angles))
        z.extend(height_points + z0)
        colori.extend(rng.choice(palette, size=n_level))
        size.extend(rng.uniform(5, 11, size=n_level) * brillantezza)

        # Piccole lucine decorative
        n_luci = max(6, n_level // 2)
        h_lights = rng.uniform(0.05, h * 0.9, size=n_luci)
        ang_lights = rng.uniform(0, 2 * np.pi, size=n_luci)
        r_lights = r_base * (1 - h_lights / h)
        x.extend(r_lights * np.cos(ang_lights))
        y.extend(r_lights * np.sin(ang_lights))
        z.extend(h_lights + z0)
        colori.extend(rng.choice(luci_palette, size=n_luci))
        size.extend(rng.uniform(2.5, 4.5, size=n_luci) * (1 + 0.3 * (brillantezza - 1)))

    return go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode="markers",
        marker=dict(size=size, color=colori, opacity=0.95),
        name="Decorazioni",
    )


def crea_puntale(z_top):
    return go.Scatter3d(
        x=[0],
        y=[0],
        z=[z_top + 0.15],
        mode="markers",
        marker=dict(size=14, color="#ffd700", opacity=1.0, symbol="star"),
        name="Puntale",
    )


def crea_regali(dim_base, z_base):
    gift_positions = [(-0.9, -0.4), (0.7, -0.6), (0.2, 0.9), (-0.5, 0.7)]
    gift_colors = ["#d93644", "#3b82f6", "#6b21a8", "#10b981"]

    traces = []
    for (gx, gy), color in zip(gift_positions, gift_colors):
        size = dim_base * np.random.uniform(0.9, 1.2)
        h = size * 0.7
        # Vertici del cubo
        vertices = np.array(
            [
                [gx, gy, z_base],
                [gx + size, gy, z_base],
                [gx + size, gy + size, z_base],
                [gx, gy + size, z_base],
                [gx, gy, z_base + h],
                [gx + size, gy, z_base + h],
                [gx + size, gy + size, z_base + h],
                [gx, gy + size, z_base + h],
            ]
        )
        i, j, k = (
            [0, 0, 0, 4, 4, 2],
            [1, 2, 3, 5, 6, 6],
            [2, 3, 1, 6, 7, 5],
        )
        traces.append(
            go.Mesh3d(
                x=vertices[:, 0],
                y=vertices[:, 1],
                z=vertices[:, 2],
                color=color,
                opacity=0.95,
                i=i,
                j=j,
                k=k,
                name="Pacco regalo",
            )
        )
        # Fiocco superiore e nastri incrociati
        traces.append(
            go.Mesh3d(
                x=vertices[:, 0],
                y=vertices[:, 1],
                z=vertices[:, 2],
                color="#f8fafc",
                opacity=0.92,
                i=[4, 4],
                j=[5, 6],
                k=[6, 7],
                name="Fiocco",
                showscale=False,
            )
        )
        # Nastri laterali per un aspetto più realistico
        nastro_x = [gx + size / 2] * 4 + [None] + [gx, gx + size]
        nastro_y = [gy, gy + size, gy + size, gy, None, gy + size / 2, gy + size / 2]
        nastro_z = [z_base, z_base, z_base + h, z_base + h, None, z_base, z_base + h]
        traces.append(
            go.Scatter3d(
                x=nastro_x,
                y=nastro_y,
                z=nastro_z,
                mode="lines",
                line=dict(color="#fbbf24", width=6),
                name="Nastro regalo",
            )
        )
    return traces


def crea_fiocchi_neve(n_fiocchi=120, raggio=2.5, altezza=4.0, seed=123):
    rng = np.random.default_rng(seed)
    angoli = rng.uniform(0, 2 * np.pi, size=n_fiocchi)
    raggi = rng.uniform(0.2, raggio, size=n_fiocchi)
    x = raggi * np.cos(angoli)
    y = raggi * np.sin(angoli)
    z = rng.uniform(0.2, altezza + 0.6, size=n_fiocchi)
    return go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode="markers",
        marker=dict(color="#ffffff", size=rng.uniform(2, 4, size=n_fiocchi), opacity=0.85),
        name="Neve",
    )


# ================== INTERFACCIA UTENTE ==================
st.title(TITOLO)
st.write(SOTTOTITOLO)

nome = st.text_input("Scrivi il nome della persona a cui vuoi fare gli auguri", "Amore")
st.markdown(f"### 💌 Per {nome}")
st.write(MESSAGGIO)

st.markdown("---")
st.subheader("Scena 3D di Natale")

# Slider di interazione
n_palline = st.slider("Quante decorazioni vuoi sull'albero?", min_value=20, max_value=80, value=40, step=5)
dimensione_regali = st.slider("Dimensione dei pacchi regalo", min_value=0.15, max_value=0.5, value=0.25, step=0.05)
scala_altezza = st.slider("Scala l'altezza dell'albero", min_value=0.85, max_value=1.25, value=1.0, step=0.05)
brillantezza = st.slider("Brillantezza palline e lucine", min_value=0.8, max_value=1.5, value=1.0, step=0.05)

# ================== SCENA 3D (ALBERO, REGALI, ECC.) ==================
fig = go.Figure()

# Pavimento
fig.add_trace(crea_pavimento(raggio=2.4, colore="#eef3f7", z=-0.02))

# Tronco
altezza_tronco = 0.4 * scala_altezza
t = crea_cilindro_tronco(altezza=altezza_tronco, raggio=0.12, colore="#8b5a2b", z_offset=0.0)
fig.add_trace(t)

# Livelli dell'albero con colori diversi e sovrapposti
# Se hai un modello 3D scaricato (OBJ/STL) puoi sostituire questi livelli con un go.Mesh3d basato sui vertici del file.
livelli_base = [
    (1.4, 1.2, "#0a5c36"),
    (1.1, 1.05, "#0d7040"),
    (0.9, 0.85, "#118e4d"),
    (0.65, 0.62, "#15ab5f"),
]

livelli_info = []
z_corrente = altezza_tronco - 0.05
scala_raggio = 0.9 + 0.25 * (scala_altezza - 1)

for h, r, col in livelli_base:
    h_scaled = h * scala_altezza
    r_scaled = r * scala_raggio
    fig.add_trace(crea_cono_albero(h_scaled, r_scaled, z_corrente, col, nome="Chioma"))
    livelli_info.append((h_scaled, r_scaled, z_corrente))
    z_corrente += h_scaled * 0.78

# Decorazioni e lucine
fig.add_trace(genera_decorazioni(n_palline, livelli_info, brillantezza=brillantezza))

# Puntale
z_top = livelli_info[-1][2] + livelli_info[-1][0]
fig.add_trace(crea_puntale(z_top))

# Pacchi regalo
for regalo in crea_regali(dim_base=dimensione_regali, z_base=-0.02):
    fig.add_trace(regalo)

# Fiocchi di neve fluttuanti per maggiore atmosfera invernale
fig.add_trace(crea_fiocchi_neve(n_fiocchi=140, raggio=2.4, altezza=z_top + 0.8))

# Layout generale
fig.update_layout(
    showlegend=False,
    scene=dict(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        zaxis=dict(visible=False),
        aspectratio=dict(x=1, y=1, z=1.25),
        # Modalità di trascinamento orbitale per esplorare facilmente con mouse o dito
        dragmode="orbit",
        camera=dict(eye=dict(x=1.5, y=1.4, z=1.25)),
    ),
    margin=dict(l=0, r=0, t=0, b=0),
)

# Configurazione Plotly per zoom con scroll e gesti touch
chart_config = {
    "scrollZoom": True,
    "displaylogo": False,
    "modeBarButtonsToRemove": ["zoom", "resetCameraDefault3d"],
    "doubleClick": "reset",
}

# Mostra figura 3D (explorabile e zoomabile con dito o mouse)
st.plotly_chart(fig, use_container_width=True, config=chart_config)

# ================== FOOTER ==================
# CAMBIA QUI IL TUO NOME
autore = "Il tuo nome"
st.caption(f"Creata con ❤️ da {autore}")
