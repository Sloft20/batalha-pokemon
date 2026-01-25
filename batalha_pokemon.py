import streamlit as st
import datetime
import random 
import re 
import json
import os
import pandas as pd

# Tenta importar, se falhar usa dados locais
try:
    from cartas_db import POKEDEX, ENERGY_IMGS, LISTA_DECKS, TOOLS_DB
except ImportError:
    # (Dados de backup para garantir que rode sempre)
    ENERGY_IMGS = {
    "Planta 🌱": "https://archives.bulbagarden.net/media/upload/thumb/2/2e/Grass-attack.png/20px-Grass-attack.png",
    "Fogo 🔥": "https://archives.bulbagarden.net/media/upload/thumb/a/ad/Fire-attack.png/20px-Fire-attack.png",
    "Água 💧": "https://archives.bulbagarden.net/media/upload/thumb/1/11/Water-attack.png/20px-Water-attack.png",
    "Elétrico ⚡": "https://archives.bulbagarden.net/media/upload/thumb/0/04/Lightning-attack.png/20px-Lightning-attack.png",
    "Psíquico 🌀": "https://archives.bulbagarden.net/media/upload/thumb/e/ef/Psychic-attack.png/20px-Psychic-attack.png",
    "Luta 🥊": "https://archives.bulbagarden.net/media/upload/thumb/4/48/Fighting-attack.png/20px-Fighting-attack.png",
    "Escuridão 🌙": "https://archives.bulbagarden.net/media/upload/thumb/a/ab/Darkness-attack.png/20px-Darkness-attack.png",
    "Metal ⚙️": "https://archives.bulbagarden.net/media/upload/thumb/6/64/Metal-attack.png/20px-Metal-attack.png",
    "Incolor ⭐": "https://archives.bulbagarden.net/media/upload/thumb/1/1d/Colorless-attack.png/20px-Colorless-attack.png"
}
    POKEDEX = {"Charizard ex": {"hp": 330, "tipo": "Escuridão 🌙", "fraq": "Planta 🌱", "res": "Nenhuma", "recuo": 2, "custo": ["Fogo 🔥", "Fogo 🔥"], "hab": "Reino Infernal", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/OBF/OBF_125_R_EN_PNG.png"}} # Exemplo curto
    TOOLS_DB = {"Nenhuma": {"hp_bonus": 0}}
    LISTA_DECKS = ["Charizard ex", "Outro"]

st.set_page_config(page_title="PokéBattle 43.0 (Pro UI)", page_icon="⚔️", layout="wide")

# --- 0. CONFIGURAÇÃO VISUAL TOTALMENTE NOVA ---
def configurar_visual():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500&display=swap');

        /* --- GLOBAL RESET --- */
        html, body, [class*="css"] { 
            font-family: 'Inter', sans-serif; 
            color: #e2e8f0;
        }
        
        /* Fundo da Aplicação (Deep Navy) */
        [data-testid="stAppViewContainer"] {
            background-color: #020617; /* Quase preto */
            background-image: radial-gradient(circle at top, #1e293b 0%, #020617 60%);
        }
        [data-testid="stHeader"] { background-color: rgba(0,0,0,0); }

        /* --- CARDS E CONTAINERS (O EFEITO DASHBOARD) --- */
        /* Remove bordas padrão do Streamlit e aplica estilo custom */
        div[data-testid="stVerticalBlockBorderWrapper"], div[data-testid="stExpander"] {
            background-color: #0f172a; /* Slate 900 */
            border: 1px solid #334155; /* Slate 700 */
            border-radius: 12px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
            padding: 16px;
        }

        /* --- INPUTS MODERNOS --- */
        .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
            background-color: #1e293b !important; 
            color: #f8fafc !important;
            border: 1px solid #475569 !important;
            border-radius: 6px;
            height: 40px;
        }
        .stSelectbox label, .stTextInput label, .stNumberInput label {
            color: #94a3b8 !important;
            font-size: 12px;
            text-transform: uppercase;
            font-weight: 600;
        }

        /* --- BOTÕES REDESENHADOS --- */
        .stButton > button {
            border-radius: 8px;
            font-weight: 600;
            border: none !important;
            width: 100%;
            height: 42px;
            transition: all 0.2s ease;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        }
        .stButton > button:hover { transform: translateY(-1px); filter: brightness(1.1); }
        .stButton > button:active { transform: translateY(1px); }

        /* Cores Específicas */
        .turn-btn button, .atk-btn button { 
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%) !important; /* Gold */
            color: #0f172a !important;
        }
        .btn-red button { background: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%) !important; color: white; }
        .game-btn button, .menu-item button { background: #334155 !important; color: white; border: 1px solid #475569 !important; }
        
        /* Botão do Menu (Topo) */
        div[data-testid="stPopover"] > div > button {
            background-color: #1e293b !important;
            border: 1px solid #475569 !important;
            color: #e2e8f0 !important;
            height: 45px;
            width: 100%;
        }

        /* --- COMPONENTES DO JOGO --- */
        .rank-card { 
            background-color: #1e293b; border: 1px solid #334155; 
            border-radius: 8px; padding: 12px; margin-bottom: 8px; 
        }
        
        /* Título Principal */
        .main-title { 
            font-size: 24px; font-weight: 800; 
            background: linear-gradient(to right, #38bdf8, #818cf8); 
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
        }
        .turn-display { 
            font-size: 14px; font-weight: 600; color: #fbbf24; 
            background: rgba(251, 191, 36, 0.1); 
            padding: 4px 12px; border-radius: 20px; display: inline-block;
            margin-top: 5px; border: 1px solid rgba(251, 191, 36, 0.3);
        }
        
        /* Barra de Vida */
        .hp-bar-bg { width: 100%; background-color: #0f172a; border-radius: 4px; height: 8px; margin: 8px 0; overflow: hidden; }
        .hp-fill { height: 100%; border-radius: 4px; transition: width 0.5s ease; }
        
        /* Energias */
        .energy-container {
            display: flex; gap: 4px; justify-content: center; flex-wrap: wrap;
            background: #0f172a; padding: 6px; border-radius: 8px; 
            border: 1px solid #334155; margin-top: 8px;
        }
        .energy-icon { width: 18px; height: 18px; filter: drop-shadow(0 2px 2px rgba(0,0,0,0.5)); }
        
        /* Stats Box */
        .stats-box {
            display: flex; justify-content: space-between; 
            background: #0f172a; padding: 8px; border-radius: 8px; 
            border: 1px solid #334155; margin-top: 8px;
        }
        .stat-item { text-align: center; width: 32%; }
        .stat-label { font-size: 10px; color: #94a3b8; font-weight: 700; text-transform: uppercase; }
        
        /* Log */
        .log-container {
            font-family: 'JetBrains Mono', monospace; font-size: 11px; 
            color: #94a3b8; padding: 6px 0; border-bottom: 1px solid #334155;
        }
        .tag-log { border-radius: 4px; padding: 2px 6px; font-weight: bold; font-size: 10px; margin-right: 8px; }
        .tag-ataque { background: rgba(239, 68, 68, 0.2); color: #fca5a5; }
        .tag-energia { background: rgba(234, 179, 8, 0.2); color: #fde047; }
        .tag-turno { background: rgba(59, 130, 246, 0.2); color: #93c5fd; }
        
        div[data-testid="column"] { display: flex; flex-direction: column; justify-content: flex-start; }
    </style>
    """, unsafe_allow_html=True)

configurar_visual()

# --- 1. CONFIGURAÇÃO DE ARQUIVOS E DADOS ---
HISTORY_FILE = "historico.json"

def carregar_historico():
    if not os.path.exists(HISTORY_FILE): return []
    try: with open(HISTORY_FILE, "r") as f: return json.load(f)
    except: return []

def salvar_partida(vencedor, perdedor, deck_venc, deck_perd, log_partida):
    hist = carregar_historico()
    partida = {
        "data": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "vencedor": vencedor, "perdedor": perdedor,
        "deck_vencedor": deck_venc, "deck_perdedor": deck_perd,
        "log": log_partida 
    }
    hist.append(partida)
    with open(HISTORY_FILE, "w") as f: json.dump(hist, f)

def calcular_stats():
    dados = carregar_historico()
    if not dados: return None, None, dados 
    stats_jog = {}; stats_deck = {}
    for d in dados:
        v, p = d['vencedor'], d['perdedor']
        if v not in stats_jog: stats_jog[v] = {'p':0, 'v':0}
        if p not in stats_jog: stats_jog[p] = {'p':0, 'v':0}
        stats_jog[v]['p'] += 1; stats_jog[v]['v'] += 1; stats_jog[p]['p'] += 1
        dv, dp = d['deck_vencedor'], d['deck_perdedor']
        if dv not in stats_deck: stats_deck[dv] = {'p':0, 'v':0}
        if dp not in stats_deck: stats_deck[dp] = {'p':0, 'v':0}
        stats_deck[dv]['p'] += 1; stats_deck[dv]['v'] += 1; stats_deck[dp]['p'] += 1
    df_jog = pd.DataFrame.from_dict(stats_jog, orient='index').reset_index()
    df_jog.columns = ['Nome', 'Partidas', 'Vitorias']
    df_jog['Winrate'] = (df_jog['Vitorias'] / df_jog['Partidas']) * 100
    df_deck = pd.DataFrame.from_dict(stats_deck, orient='index').reset_index()
    df_deck.columns = ['Deck', 'Partidas', 'Vitorias']
    df_deck['Winrate'] = (df_deck['Vitorias'] / df_deck['Partidas']) * 100
    return df_jog.sort_values(by='Vitorias', ascending=False), df_deck.sort_values(by='Vitorias', ascending=False), dados

# --- 2. CLASSE POKEMON ---
class Pokemon:
    def __init__(self, nome, hp_max, tipo, fraqueza, resistencia, recuo, imagem_url="", habilidade=None):
        self.nome = nome
        self.hp_base = int(hp_max); self.hp_max = int(hp_max); self.hp_atual = int(hp_max)
        self.imagem_url = imagem_url if imagem_url else "https://upload.wikimedia.org/wikipedia/en/3/3b/Pokemon_Trading_Card_Game_cardback.jpg"
        self.id_unico = datetime.datetime.now().timestamp() + random.random()
        self.tipo = tipo; self.fraqueza = fraqueza; self.resistencia = resistencia; self.recuo = recuo
        self.status = "Saudável"; self.energias = {}; self.ferramenta = "Nenhuma"
        self.habilidade = habilidade if habilidade else (POKEDEX[nome].get("hab") if nome in POKEDEX else None)

    def equipar_ferramenta(self, nome_ferramenta):
        if self.ferramenta in TOOLS_DB: self.hp_max -= TOOLS_DB[self.ferramenta]["hp_bonus"]; self.hp_atual = min(self.hp_atual, self.hp_max)
        self.ferramenta = nome_ferramenta
        if nome_ferramenta in TOOLS_DB: self.hp_max += TOOLS_DB[nome_ferramenta]["hp_bonus"]; self.hp_atual += TOOLS_DB[nome_ferramenta]["hp_bonus"]
        return True

    def receber_dano(self, dano):
        self.hp_atual = max(0, self.hp_atual - dano)

    def resolver_checkup(self):
        logs = []
        if self.status == "Envenenado 🧪": self.receber_dano(10); logs.append(f"🧪 {self.nome} sofreu 10 de veneno.")
        elif self.status == "Queimado 🔥":
            self.receber_dano(20); logs.append(f"🔥 {self.nome} sofreu 20 de queimadura.")
            if random.choice(["CARA", "COROA"]) == "CARA": self.status = "Saudável"; logs.append(f"🪙 {self.nome} curou queimadura!")
        elif self.status == "Adormecido 💤":
            if random.choice(["CARA", "COROA"]) == "CARA": self.status = "Saudável"; logs.append(f"🪙 {self.nome} acordou!")
        return logs

    def evoluir_para(self, novo_nome, novo_hp, novo_tipo, nova_fraqueza, nova_resistencia, nova_recuo, nova_img, nova_hab=None):
        dano = self.hp_max - self.hp_atual
        self.nome = novo_nome; self.hp_base = int(novo_hp); self.hp_max = self.hp_base + TOOLS_DB[self.ferramenta]["hp_bonus"]
        self.tipo = novo_tipo; self.fraqueza = nova_fraqueza; self.resistencia = nova_resistencia
        self.recuo = nova_recuo; self.imagem_url = nova_img if nova_img else self.imagem_url
        self.habilidade = nova_hab if nova_hab else POKEDEX.get(novo_nome, {}).get("hab")
        self.hp_atual = max(0, self.hp_max - dano); self.status = "Saudável"

    def anexar_energia(self, tipo): self.energias[tipo] = self.energias.get(tipo, 0) + 1
    def remover_energia(self, tipo):
        if tipo in self.energias:
            self.energias[tipo] -= 1
            if self.energias[tipo] <= 0: del self.energias[tipo]
            return True
        return False
    
    def tentar_recuar(self):
        total = sum(self.energias.values())
        custo = max(0, self.recuo - 1) if self.ferramenta == "Skate de Resgate (-1 Recuo)" else self.recuo
        if total >= custo:
            rem = 0
            for t in list(self.energias.keys()):
                while self.energias[t] > 0 and rem < custo: self.energias[t] -= 1; rem += 1
                if self.energias[t] <= 0: del self.energias[t]
            self.status = "Saudável"; return True, f"Pagou {custo}."
        return False, f"Falta energia ({total}/{custo})."

def verificar_custo_ataque(pokemon):
    custo_lista = POKEDEX.get(pokemon.nome, {}).get("custo", ["Incolor ⭐"])
    pool = pokemon.energias.copy()
    for req in [c for c in custo_lista if "Incolor" not in c]:
        if pool.get(req, 0) > 0: pool[req] -= 1
        else: return False 
    incolores_nec = len([c for c in custo_lista if "Incolor" in c])
    return sum(pool.values()) >= incolores_nec

def gerar_html_energia(energias_dict):
    if not energias_dict: return "<div class='energy-container' style='opacity:0'>.</div>"
    html = "<div class='energy-container'>"
    for tipo_chave, qtd in energias_dict.items():
        img_url = ENERGY_IMGS.get(tipo_chave, "")
        if img_url:
            for _ in range(qtd): html += f"<img src='{img_url}' class='energy-icon' title='{tipo_chave}'>"
        else:
            html += f"<span style='font-size:12px; margin:0 2px;'>{tipo_chave} x{qtd}</span>"
    html += "</div>"
    return html

def get_icon_html(tipo_str):
    url = ENERGY_IMGS.get(tipo_str)
    if url: return f"<img src='{url}' class='stat-icon'>"
    return "<span style='font-size:12px; color:#64748b'>-</span>"

def render_custo_html(nome_poke):
    custo = POKEDEX.get(nome_poke, {}).get("custo", ["Incolor ⭐"])
    html = "<div class='atk-cost-display' style='display:flex; justify-content:center; gap:2px; margin-bottom:5px;'>"
    for c in custo:
        url = ENERGY_IMGS.get(c)
        if url: html += f"<img src='{url}' style='width:16px;'>"
    html += "</div>"
    return html

# --- 3. ESTADO ---
def inicializar_jogo():
    if 'Treinadores' not in st.session_state:
        st.session_state.Treinadores = {
            "Treinador 1": {"nome": "Treinador 1", "ativo": None, "banco": [], "descarte": [], "premios": 6, "deck": "Charizard ex"},
            "Treinador 2": {"nome": "Treinador 2", "ativo": None, "banco": [], "descarte": [], "premios": 6, "deck": "Dragapult ex"}
        }
    if 'log' not in st.session_state: st.session_state.log = []
    if 'vencedor' not in st.session_state: st.session_state.vencedor = None
    if 'turno_atual' not in st.session_state: st.session_state.turno_atual = "Treinador 1"
    if 'habilidades_usadas' not in st.session_state: st.session_state.habilidades_usadas = []
    if 'evolucoes_turno' not in st.session_state: st.session_state.evolucoes_turno = []
    if 'energias_anexadas_neste_turno' not in st.session_state: st.session_state.energias_anexadas_neste_turno = []
    if 'dmg_buffer' not in st.session_state: st.session_state.dmg_buffer = {}
    if 'tela_ranking' not in st.session_state: st.session_state.tela_ranking = False

def adicionar_log(cat, msg, player=None):
    hora = datetime.datetime.now().strftime("%H:%M")
    css_class = {"Inicio": "tag-inicio", "Turno": "tag-turno", "Ataque": "tag-ataque", "Energia": "tag-energia", "Tool": "tag-tool", "KO": "tag-ko", "Status": "tag-status", "Moeda": "tag-tool"}.get(cat, "tag-log")
    prefixo = f"<b>{player}</b>: " if player else ""
    st.session_state.log.insert(0, f"<div class='log-container'><span style='color:#64748b;margin-right:8px'>[{hora}]</span><span class='tag-log {css_class}'>{cat}</span><span>{prefixo}{msg}</span></div>")

inicializar_jogo()

# =================================================================================
# === TELA DE RANKING ===
# =================================================================================
if st.session_state.tela_ranking:
    st.markdown('<div class="main-title">🏆 Ranking Global</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 5])
    with c1:
        st.markdown('<div class="menu-item">', unsafe_allow_html=True)
        if st.button("⬅ Voltar", use_container_width=True): st.session_state.tela_ranking = False; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="btn-red">', unsafe_allow_html=True)
        if st.button("🗑️ Resetar", use_container_width=True):
            if os.path.exists(HISTORY_FILE): os.remove(HISTORY_FILE); st.toast("Resetado!"); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    df_jog, df_deck, dados_brutos = calcular_stats()
    
    if df_jog is not None and not df_jog.empty:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"### 👤 Top Jogadores")
            for index, row in df_jog.iterrows():
                cor = "#22c55e" if row['Winrate'] >= 50 else "#ef4444"
                st.markdown(f"""<div class="rank-card"><div class="rank-name">#{index+1} {row['Nome']}</div><div class="rank-stats">V: {row['Vitorias']} | WR: {row['Winrate']:.1f}%</div><div class="rank-bar-bg"><div class="rank-bar-fill" style="width:{row['Winrate']}%; background-color:{cor};"></div></div></div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"### 🃏 Top Decks")
            for index, row in df_deck.iterrows():
                cor = "#3b82f6" if row['Winrate'] >= 50 else "#64748b"
                st.markdown(f"""<div class="rank-card"><div class="rank-name">{row['Deck']}</div><div class="rank-stats">V: {row['Vitorias']} | WR: {row['Winrate']:.1f}%</div><div class="rank-bar-bg"><div class="rank-bar-fill" style="width:{row['Winrate']}%; background-color:{cor};"></div></div></div>""", unsafe_allow_html=True)
    else: st.info("Sem dados ainda.")

else:
    # =================================================================================
    # === TELA DE JOGO (LAYOUT PROFISSIONAL) ===
    # =================================================================================
    c_title, c_spacer, c_buttons = st.columns([2, 1, 1.2])
    with c_title:
        st.markdown('<div class="main-title">⚔️ PokéBattle</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="turn-display">👉 {st.session_state.Treinadores[st.session_state.turno_atual]["nome"]}</div>', unsafe_allow_html=True)

    with c_buttons:
        with st.popover("⚙️ Menu", use_container_width=True):
            st.markdown('<div class="menu-item">', unsafe_allow_html=True)
            if st.button("🏆 Placar", use_container_width=True): st.session_state.tela_ranking = True; st.rerun()
            if st.button("🪙 Moeda", use_container_width=True): r = random.choice(["CARA", "COROA"]); st.toast(f"{r}"); adicionar_log("Moeda", f"Resultado: {r}")
            if st.session_state.log:
                txt = "\n".join([re.sub('<[^<]+?>', '', l) for l in st.session_state.log[::-1]])
                st.download_button("📜 Baixar Log", txt, "log.txt", use_container_width=True)
            if st.button("🗑️ Reset Jogo", use_container_width=True): st.session_state.clear(); st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
        st.markdown('<div class="turn-btn">', unsafe_allow_html=True)
        if st.button("➡ Fim Turno", use_container_width=True):
            logs_check = []
            for p in ["Treinador 1", "Treinador 2"]:
                if st.session_state.Treinadores[p]['ativo']:
                    r = st.session_state.Treinadores[p]['ativo'].resolver_checkup(); logs_check.extend(r)
            for l in logs_check: adicionar_log("Status", l)
            st.session_state.habilidades_usadas = []
            st.session_state.evolucoes_turno = []
            st.session_state.energias_anexadas_neste_turno = []
            ant = st.session_state.turno_atual
            novo = "Treinador 2" if ant == "Treinador 1" else "Treinador 1"
            st.session_state.turno_atual = novo
            adicionar_log("Turno", f"Início de {st.session_state.Treinadores[novo]['nome']}.")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # --- SIDEBAR ---
    with st.sidebar:
        st.header("⚙️ Config")
        with st.expander("👤 Jogadores", expanded=True):
            n1 = st.text_input("J1", value=st.session_state.Treinadores["Treinador 1"]["nome"])
            d1 = st.selectbox("Deck J1", LISTA_DECKS, index=0)
            st.divider()
            n2 = st.text_input("J2", value=st.session_state.Treinadores["Treinador 2"]["nome"])
            d2 = st.selectbox("Deck J2", LISTA_DECKS, index=1)
            if st.button("Salvar", type="primary"):
                st.session_state.Treinadores["Treinador 1"]["nome"] = n1; st.session_state.Treinadores["Treinador 1"]["deck"] = d1
                st.session_state.Treinadores["Treinador 2"]["nome"] = n2; st.session_state.Treinadores["Treinador 2"]["deck"] = d2; st.rerun()
        
        st.markdown("### ➕ Cartas")
        dono_key = st.selectbox("Treinador", ["Treinador 1", "Treinador 2"], format_func=lambda x: st.session_state.Treinadores[x]['nome'])
        player = st.session_state.Treinadores[dono_key]
        acao = st.radio("Ação", ["Novo Básico", "Evoluir"], horizontal=True)
        
        if acao == "Novo Básico":
            escolha = st.selectbox("Pokémon", list(POKEDEX.keys())); dados = POKEDEX[escolha]; st.image(dados["img"], width=80)
            local = st.radio("Local", ["Banco", "Ativo"], horizontal=True)
            if st.button("Adicionar"):
                novo = Pokemon(escolha, dados["hp"], dados["tipo"], dados["fraq"], dados["res"], dados.get("recuo", 1), dados["img"], dados.get("hab"))
                st.session_state.evolucoes_turno.append(novo.id_unico)
                if local == "Ativo" and not player['ativo']: player['ativo'] = novo; adicionar_log("Inicio", f"Colocou {escolha} Ativo.", player['nome']); st.rerun()
                elif local == "Banco" and len(player['banco']) < 5: player['banco'].append(novo); adicionar_log("Inicio", f"Colocou {escolha} Banco.", player['nome']); st.rerun()
                else: st.error("Ocupado!")
        elif acao == "Evoluir":
            opcoes = []
            if player['ativo']: opcoes.append(f"[Ativo] {player['ativo'].nome}")
            for i, p in enumerate(player['banco']): opcoes.append(f"[Banco {i+1}] {p.nome}")
            if opcoes:
                alvo = st.selectbox("Quem?", opcoes); evo = st.selectbox("Para:", list(POKEDEX.keys()))
                if st.button("Evoluir"):
                    obj = player['ativo'] if "[Ativo]" in alvo else player['banco'][int(alvo.split("]")[0].split(" ")[1])-1]
                    if obj.id_unico in st.session_state.evolucoes_turno: st.error("🚫 Já evoluiu!")
                    else:
                        d = POKEDEX[evo]
                        obj.evoluir_para(evo, d["hp"], d["tipo"], d["fraq"], d["res"], d.get("recuo",1), d["img"], d.get("hab"))
                        st.session_state.evolucoes_turno.append(obj.id_unico)
                        adicionar_log("Energia", f"Evoluiu para {evo}!", player['nome']); st.rerun()

    def checar_vitoria(id_chave):
        if st.session_state.Treinadores[id_chave]['premios'] <= 0: return True
        if st.session_state.Treinadores[id_chave]['ativo'] is None and len(st.session_state.Treinadores[id_chave]['banco']) == 0: return True
        return False

    def render_player(key):
        p = st.session_state.Treinadores[key]
        eh_vez = (st.session_state.turno_atual == key)
        borda = "2px solid #FFC107" if eh_vez else "1px solid #334155"
        
        st.markdown(f"<div style='border:{borda}; background-color:#1e293b; padding:12px; border-radius:12px; margin-bottom:12px;'>", unsafe_allow_html=True)
        c1, c2 = st.columns([3, 1])
        c1.markdown(f"<h4 style='margin:0'>{p['nome']} <span style='font-size:12px;color:#94a3b8'>({p['deck']})</span></h4>", unsafe_allow_html=True)
        c2.markdown(f"<h5 style='margin:0; text-align:right'>{p['premios']} 🎴</h5>", unsafe_allow_html=True)
        
        ativo = p['ativo']
        if ativo:
            st.markdown("---")
            c_img, c_info = st.columns([1, 1.8])
            with c_img:
                st.image(ativo.imagem_url, use_container_width=True)
                if ativo.status != "Saudável": st.warning(ativo.status)
                st.markdown(gerar_html_energia(ativo.energias), unsafe_allow_html=True)
                if ativo.ferramenta != "Nenhuma": st.caption(f"🛠️ {ativo.ferramenta}")
            with c_info:
                nome_disp = f'<span style="color:#FFD700; text-shadow: 0 0 5px rgba(255, 215, 0, 0.6);">★ {ativo.nome}</span>' if any(x in ativo.nome.lower() for x in ["ex", "v", "vstar"]) else f"**{ativo.nome}**"
                st.markdown(f"{nome_disp} <span style='float:right; font-size:12px;'>{ativo.hp_atual}/{ativo.hp_max}</span>", unsafe_allow_html=True)
                pct = max(0, min(100, (ativo.hp_atual / ativo.hp_max) * 100))
                color_hp = "#22c55e" if pct > 50 else ("#eab308" if pct > 20 else "#ef4444")
                st.markdown(f"""<div class="hp-bar-bg"><div class="hp-fill" style="width:{pct}%; background-color:{color_hp};"></div></div>""", unsafe_allow_html=True)
                
                # STATS
                fraq = get_icon_html(ativo.fraqueza); res = get_icon_html(ativo.resistencia)
                rec = "".join([f"<img src='{ENERGY_IMGS['Incolor ⭐']}' class='energy-icon'>" for _ in range(ativo.recuo)]) if ativo.recuo else "<span style='font-size:10px'>LIVRE</span>"
                st.markdown(f"""<div class="stats-box"><div class="stat-item"><div class="stat-label">Fraqueza</div>{fraq}</div><div class="stat-item"><div class="stat-label">Resistência</div>{res}</div><div class="stat-item"><div class="stat-label">Recuo</div><div>{rec}</div></div></div>""", unsafe_allow_html=True)

                if ativo.hp_atual == 0:
                    st.markdown('<div class="btn-red">', unsafe_allow_html=True)
                    if st.button("Enviar p/ Descarte", key=f"ko_{ativo.id_unico}"):
                        p['descarte'].append(ativo); p['ativo'] = None
                        adicionar_log("KO", f"💀 {ativo.nome} caiu!", p['nome'])
                        op_key = "Treinador 2" if key == "Treinador 1" else "Treinador 1"
                        st.session_state.Treinadores[op_key]['premios'] -= 2 if "ex" in ativo.nome.lower() else 1
                        if checar_vitoria(key): st.session_state.vencedor = st.session_state.Treinadores[op_key]['nome']; salvar_partida(st.session_state.Treinadores[op_key]['nome'], p['nome'], st.session_state.Treinadores[op_key]['deck'], p['deck'], list(st.session_state.log))
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    if ativo.id_unico not in st.session_state.dmg_buffer: st.session_state.dmg_buffer[ativo.id_unico] = 0
                    dmg = st.number_input("Dano", value=st.session_state.dmg_buffer[ativo.id_unico], step=10, key=f"d_{ativo.id_unico}", label_visibility="collapsed")
                    st.session_state.dmg_buffer[ativo.id_unico] = dmg
                    
                    st.markdown(render_custo_html(ativo.nome), unsafe_allow_html=True)

                    st.markdown('<div class="atk-btn">', unsafe_allow_html=True)
                    if st.button("ATACAR", key=f"atk_{ativo.id_unico}"):
                        if not verificar_custo_ataque(ativo): st.error("🚫 Falta Energia!")
                        else:
                            op_key = "Treinador 2" if key == "Treinador 1" else "Treinador 1"
                            op = st.session_state.Treinadores[op_key]
                            if op['ativo']:
                                mult = 2 if ativo.tipo == op['ativo'].fraqueza else 1
                                red = 30 if ativo.tipo == op['ativo'].resistencia else 0
                                final = max(0, (dmg * mult) - red)
                                op['ativo'].receber_dano(final)
                                adicionar_log("Ataque", f"{ativo.nome} causou {final} em {op['ativo'].nome}.", p['nome'])
                                # Checkup
                                logs_check = []
                                for x in ["Treinador 1", "Treinador 2"]:
                                    if st.session_state.Treinadores[x]['ativo']: logs_check.extend(st.session_state.Treinadores[x]['ativo'].resolver_checkup())
                                for l in logs_check: adicionar_log("Status", l)
                                # Passa Turno
                                st.session_state.habilidades_usadas = []
                                st.session_state.evolucoes_turno = []
                                st.session_state.energias_anexadas_neste_turno = []
                                ant = st.session_state.turno_atual
                                st.session_state.turno_atual = "Treinador 2" if ant == "Treinador 1" else "Treinador 1"
                                adicionar_log("Turno", f"Início de {st.session_state.Treinadores[st.session_state.turno_atual]['nome']}.")
                                st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

                    with st.popover("⚡ / Status / Tool / Evo", use_container_width=True):
                        t1, t2, t3, t4 = st.tabs(["Energia", "Status", "Tool", "Evoluir"])
                        with t1:
                            e = st.selectbox("Tipo", ["Fogo 🔥", "Água 💧", "Planta 🌱", "Elétrico ⚡", "Psíquico 🌀", "Luta 🥊", "Escuridão 🌙", "Metal ⚙️", "Incolor ⭐", "Dragão 🐉", "Fada 🧚"], key=f"ae_{ativo.id_unico}")
                            st.image(ENERGY_IMGS[e], width=20)
                            c1, c2 = st.columns(2)
                            with c1: 
                                if st.button("➕", key=f"ba_{ativo.id_unico}"):
                                    if ativo.id_unico in st.session_state.energias_anexadas_neste_turno: st.error("🚫 Já ligou!")
                                    else: ativo.anexar_energia(e); st.session_state.energias_anexadas_neste_turno.append(ativo.id_unico); adicionar_log("Energia", f"Ligou {e}", p['nome']); st.rerun()
                            with c2:
                                if st.button("➖", key=f"br_{ativo.id_unico}"): ativo.remover_energia(e); adicionar_log("Energia", f"Removeu {e}", p['nome']); st.rerun()
                        with t2: st.selectbox("Status", ["Saudável", "Envenenado 🧪", "Queimado 🔥", "Adormecido 💤", "Paralisado ⚡"], key=f"st_{ativo.id_unico}", on_change=lambda: setattr(ativo, 'status', st.session_state[f"st_{ativo.id_unico}"]))
                        with t3:
                            tl = st.selectbox("Tool", list(TOOLS_DB.keys()), key=f"tl_{ativo.id_unico}")
                            if st.button("Equipar", key=f"btl_{ativo.id_unico}"): ativo.equipar_ferramenta(tl); adicionar_log("Tool", f"Equipou {tl}", p['nome']); st.rerun()
                        with t4:
                            ev = st.selectbox("Para:", list(POKEDEX.keys()), key=f"evs_{ativo.id_unico}")
                            if st.button("Evoluir", key=f"bev_{ativo.id_unico}"):
                                if ativo.id_unico in st.session_state.evolucoes_turno: st.error("🚫 Já evoluiu!")
                                else:
                                    d = POKEDEX[ev]; ativo.evoluir_para(ev, d["hp"], d["tipo"], d["fraq"], d["res"], d.get("recuo",1), d["img"], d.get("hab"))
                                    st.session_state.evolucoes_turno.append(ativo.id_unico); adicionar_log("Energia", f"Evoluiu para {ev}!", p['nome']); st.rerun()
                    
                    if ativo.habilidade:
                        ja = ativo.id_unico in st.session_state.habilidades_usadas
                        cls = "game-btn" if ja else "menu-btn"
                        lbl = "✅ Hab Usada" if ja else f"✨ {ativo.habilidade}"
                        st.markdown(f'<div class="{cls}">', unsafe_allow_html=True)
                        if st.button(lbl, key=f"hab_{ativo.id_unico}", disabled=ja):
                            st.session_state.habilidades_usadas.append(ativo.id_unico)
                            adicionar_log("Tool", f"Usou {ativo.habilidade}", p['nome']); st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    custo = max(0, ativo.recuo - 1) if ativo.ferramenta == "Skate de Resgate (-1 Recuo)" else ativo.recuo
                    if st.button(f"Recuar ({custo})", key=f"run_{ativo.id_unico}"):
                        pode, msg = ativo.tentar_recuar()
                        if pode:
                            if p['banco']: p['banco'].append(ativo); p['ativo'] = None; adicionar_log("Inicio", f"Recuou.", p['nome']); st.rerun()
                            else: st.warning("Banco vazio!")
                        else: st.error(msg)
        
        if p['banco']:
            st.markdown("---")
            cols = st.columns(max(5, len(p['banco'])))
            for i, bp in enumerate(p['banco']):
                with cols[i]:
                    st.image(bp.imagem_url, use_container_width=True)
                    st.markdown(f"<div style='text-align:center; font-size:11px; font-weight:bold; color:#cbd5e1; margin-top:-5px;'>HP: {bp.hp_atual}/{bp.hp_max}</div>", unsafe_allow_html=True)
                    st.markdown(gerar_html_energia(bp.energias), unsafe_allow_html=True)
                    
                    if bp.hp_atual == 0:
                        st.markdown('<div class="btn-red">', unsafe_allow_html=True)
                        if st.button("💀", key=f"kob_{bp.id_unico}"):
                            p['banco'].pop(i); p['descarte'].append(bp); adicionar_log("KO", f"💀 {bp.nome} (Banco) caiu!", p['nome'])
                            op_key = "Treinador 2" if key == "Treinador 1" else "Treinador 1"
                            st.session_state.Treinadores[op_key]['premios'] -= 2 if "ex" in bp.nome.lower() else 1
                            if checar_vitoria(key): st.session_state.vencedor = st.session_state.Treinadores[op_key]['nome']; salvar_partida(st.session_state.Treinadores[op_key]['nome'], p['nome'], st.session_state.Treinadores[op_key]['deck'], p['deck'], list(st.session_state.log))
                            st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        c_up, c_dmg = st.columns(2)
                        with c_up: 
                            if st.button("⬆️", key=f"up_{bp.id_unico}"): 
                                if not p['ativo']: adicionar_log("Inicio", f"{bp.nome} subiu.", p['nome']); p['ativo'] = p['banco'].pop(i); st.rerun()
                        with c_dmg: 
                            if st.button("💔", key=f"dmb_{bp.id_unico}"): bp.receber_dano(10); st.rerun()
                        
                        with st.popover("⚡", use_container_width=True):
                            t1, t2, t3, t4 = st.tabs(["Add", "Del", "Tool", "Evoluir"])
                            with t1:
                                eb = st.selectbox("Tipo", ["Fogo 🔥", "Água 💧", "Planta 🌱", "Elétrico ⚡", "Psíquico 🌀", "Luta 🥊", "Escuridão 🌙", "Metal ⚙️", "Incolor ⭐", "Dragão 🐉", "Fada 🧚"], key=f"aeb_{bp.id_unico}")
                                st.image(ENERGY_IMGS[eb], width=20)
                                if st.button("Add", key=f"baeb_{bp.id_unico}"): 
                                    if bp.id_unico in st.session_state.energias_anexadas_neste_turno: st.error("🚫 Já ligou!")
                                    else: bp.anexar_energia(eb); st.session_state.energias_anexadas_neste_turno.append(bp.id_unico); adicionar_log("Energia", f"Ligou {eb} no banco", p['nome']); st.rerun()
                            with t2:
                                if bp.energias:
                                    rb = st.selectbox("Rem", list(bp.energias.keys()), key=f"reb_{bp.id_unico}")
                                    if st.button("Del", key=f"breb_{bp.id_unico}"): bp.remover_energia(rb); adicionar_log("Energia", f"Removeu {rb}", p['nome']); st.rerun()
                            with t3:
                                tlb = st.selectbox("Tool", list(TOOLS_DB.keys()), key=f"tlb_{bp.id_unico}")
                                if st.button("Eqp", key=f"btlb_{bp.id_unico}"): bp.equipar_ferramenta(tlb); adicionar_log("Tool", f"Equipou {tlb}", p['nome']); st.rerun()
                            with t4:
                                evb = st.selectbox("Para:", list(POKEDEX.keys()), key=f"evsb_{bp.id_unico}")
                                if st.button("Evoluir", key=f"bevb_{bp.id_unico}"):
                                    if bp.id_unico in st.session_state.evolucoes_turno: st.error("🚫 Já evoluiu!")
                                    else:
                                        d = POKEDEX[evb]; bp.evoluir_para(evb, d["hp"], d["tipo"], d["fraq"], d["res"], d.get("recuo",1), d["img"], d.get("hab"))
                                        st.session_state.evolucoes_turno.append(bp.id_unico); adicionar_log("Energia", f"{bp.nome} evoluiu!", p['nome']); st.rerun()

                        if bp.habilidade:
                            ja = bp.id_unico in st.session_state.habilidades_usadas
                            if st.button("✨", key=f"hbb_{bp.id_unico}", disabled=ja, help=bp.habilidade):
                                st.session_state.habilidades_usadas.append(bp.id_unico); adicionar_log("Tool", f"✨ {bp.nome} hab.", p['nome']); st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.vencedor:
        st.balloons()
        st.markdown(f"<h1 style='text-align:center'>🏆 {st.session_state.vencedor} VENCEU!</h1>", unsafe_allow_html=True)
        if st.button("Novo Jogo"): st.session_state.clear(); st.rerun()
    else:
        c1, c_div, c2 = st.columns([1, 0.1, 1])
        with c1: render_player("Treinador 1")
        with c_div: st.markdown("""<div style='height: 100%; min-height: 800px; width: 1px; background-color: #334155; margin: 0 auto;'></div>""", unsafe_allow_html=True)
        with c2: render_player("Treinador 2")
        st.divider()
        st.subheader("📜 Registro")
        with st.container(height=300): st.markdown("".join(st.session_state.log), unsafe_allow_html=True)
