import streamlit as st
import datetime
import random 
import re 
import json
import os
import pandas as pd

st.set_page_config(page_title="PokéBattle 44.0 (Reference UI)", page_icon="⚔️", layout="wide")

# --- 0. CONFIGURAÇÃO VISUAL (ESTILO REFERÊNCIA) ---
def configurar_visual():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@500;700;900&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500&display=swap');

        /* RESET & FONTS */
        html, body, [class*="css"] { 
            font-family: 'Roboto', sans-serif; 
            background-color: #0f172a; /* Navy Dark */
            color: #f8fafc;
        }

        /* FUNDO DA APLICAÇÃO */
        [data-testid="stAppViewContainer"] {
            background-color: #0f172a;
            background-image: 
                linear-gradient(180deg, rgba(15, 23, 42, 0.9) 0%, rgba(15, 23, 42, 0.7) 100%),
                url("https://pokemonrevolution.net/forum/uploads/monthly_2021_03/DVMT-6OXcAE2rZY.jpg.afab972f972bd7fbd4253bc7aa1cf27f.jpg");
            background-size: cover;
            background-attachment: fixed;
        }
        [data-testid="stHeader"] { background-color: rgba(0,0,0,0); }

        /* CONTAINERS (OS "PLAYMATS") */
        [data-testid="stVerticalBlockBorderWrapper"], [data-testid="stExpander"] {
            background-color: #1e293b; /* Slate 800 */
            border: 1px solid #334155; /* Slate 700 */
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
            padding: 16px;
        }

        /* INPUTS ESTILIZADOS */
        .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
            background-color: #020617 !important; /* Slate 950 */
            color: #e2e8f0 !important;
            border: 1px solid #475569 !important;
            border-radius: 6px;
        }

        /* --- BOTÕES TIPO JOGO --- */
        .stButton > button {
            border-radius: 8px;
            font-weight: 700;
            border: none !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            height: 40px;
            transition: all 0.2s;
            width: 100%;
        }

        /* Botão Ação (Cinza/Azul) */
        .game-btn > button {
            background-color: #334155 !important; 
            color: #f8fafc !important;
            border: 1px solid #475569 !important;
        }
        .game-btn > button:hover { background-color: #475569 !important; transform: translateY(-2px); }

        /* Botão Destaque (Amarelo - Atacar/Turno) */
        .action-btn > button {
            background: linear-gradient(145deg, #fbbf24, #d97706) !important;
            color: #0f172a !important;
            box-shadow: 0 4px 0 #92400e !important; /* Efeito 3D */
            margin-bottom: 4px;
        }
        .action-btn > button:hover { filter: brightness(1.1); transform: translateY(-2px); box-shadow: 0 6px 0 #92400e !important; }
        .action-btn > button:active { transform: translateY(2px); box-shadow: 0 2px 0 #92400e !important; }

        /* Botão Perigo (Vermelho) */
        .danger-btn > button {
            background: linear-gradient(145deg, #ef4444, #b91c1c) !important;
            color: white !important;
        }

        /* Botão Topo (Menu/Log) */
        .top-btn button {
            background-color: #1e293b !important;
            border: 1px solid #475569 !important;
            color: #94a3b8 !important;
            height: 38px !important;
            font-size: 13px !important;
        }
        .top-btn button:hover { background-color: #334155 !important; color: white !important; }

        /* --- ELEMENTOS DO JOGO --- */
        /* Barra de Vida */
        .hp-bar-bg { width: 100%; background: #020617; border-radius: 4px; height: 10px; margin: 8px 0; border: 1px solid #334155; }
        .hp-fill { height: 100%; border-radius: 3px; transition: width 0.5s ease; }
        
        /* Box de Stats */
        .stats-box {
            display: flex; justify-content: space-around; 
            background: #020617; border: 1px solid #334155; 
            border-radius: 6px; padding: 6px; margin-top: 8px;
        }
        .stat-item { text-align: center; width: 33%; font-size: 11px; color: #94a3b8; }
        .stat-icon { width: 16px; vertical-align: middle; }

        /* Container de Energia */
        .energy-container {
            display: flex; flex-wrap: wrap; gap: 3px; justify-content: flex-start;
            background: rgba(0,0,0,0.3); padding: 5px; border-radius: 6px;
            margin-top: 5px; min-height: 28px; align-items: center;
        }
        .energy-icon { width: 18px; filter: drop-shadow(0 2px 1px rgba(0,0,0,0.5)); }

        /* Log */
        .log-container {
            font-family: 'JetBrains Mono', monospace; font-size: 12px; 
            color: #94a3b8; padding: 4px 0; border-bottom: 1px solid #334155;
        }
        .tag-log { padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 10px; margin-right: 6px; }
        
        /* Títulos */
        .main-title { font-size: 24px; font-weight: 900; color: #f8fafc; letter-spacing: -1px; }
        .turn-indicator { font-size: 16px; font-weight: 700; color: #fbbf24; text-transform: uppercase; }

        div[data-testid="column"] { display: flex; flex-direction: column; justify-content: flex-start; }
    </style>
    """, unsafe_allow_html=True)

configurar_visual()

# --- 1. DADOS E FUNÇÕES AUXILIARES (INTACTOS) ---
ENERGY_IMGS = {
    "Planta 🌱": "https://limitlesstcg.nyc3.cdn.digitaloceanspaces.com/web/energies/grass.png",
    "Fogo 🔥": "https://limitlesstcg.nyc3.cdn.digitaloceanspaces.com/web/energies/fire.png",
    "Água 💧": "https://limitlesstcg.nyc3.cdn.digitaloceanspaces.com/web/energies/water.png",
    "Elétrico ⚡": "https://limitlesstcg.nyc3.cdn.digitaloceanspaces.com/web/energies/lightning.png",
    "Psíquico 🌀": "https://limitlesstcg.nyc3.cdn.digitaloceanspaces.com/web/energies/psychic.png",
    "Luta 🥊": "https://limitlesstcg.nyc3.cdn.digitaloceanspaces.com/web/energies/fighting.png",
    "Escuridão 🌙": "https://limitlesstcg.nyc3.cdn.digitaloceanspaces.com/web/energies/darkness.png",
    "Metal ⚙️": "https://limitlesstcg.nyc3.cdn.digitaloceanspaces.com/web/energies/metal.png",
    "Incolor ⭐": "https://limitlesstcg.nyc3.cdn.digitaloceanspaces.com/web/energies/colorless.png",
    "Dragão 🐉": "https://limitlesstcg.nyc3.cdn.digitaloceanspaces.com/web/energies/dragon.png",
    "Fada 🧚": "https://limitlesstcg.nyc3.cdn.digitaloceanspaces.com/web/energies/fairy.png"
}

# (Mantendo o resto dos dados igual para economizar espaço aqui, mas use o dicionário completo POKEDEX da versão anterior)
try:
    from cartas_db import POKEDEX, TOOLS_DB, LISTA_DECKS
except:
    # Backup curto para rodar
    POKEDEX = {"Charizard ex": {"hp": 330, "tipo": "Escuridão 🌙", "fraq": "Planta 🌱", "res": "Nenhuma", "recuo": 2, "custo": ["Fogo 🔥", "Fogo 🔥"], "hab": "Reino Infernal", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/OBF/OBF_125_R_EN_PNG.png"}}
    TOOLS_DB = {"Nenhuma": {"hp_bonus": 0}}
    LISTA_DECKS = ["Charizard ex", "Outro"]

HISTORY_FILE = "historico.json"

def carregar_historico():
    if not os.path.exists(HISTORY_FILE): return []
    try: with open(HISTORY_FILE, "r") as f: return json.load(f)
    except: return []

def salvar_partida(vencedor, perdedor, deck_venc, deck_perd, log_partida):
    hist = carregar_historico()
    partida = {
        "data": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "vencedor": vencedor, "perdedor": perdedor, "deck_vencedor": deck_venc, "deck_perdedor": deck_perd, "log": log_partida 
    }
    hist.append(partida)
    with open(HISTORY_FILE, "w") as f: json.dump(hist, f)

def get_icon_html(tipo_str):
    url = ENERGY_IMGS.get(tipo_str)
    if url: return f"<img src='{url}' class='stat-icon'>"
    return "-"

def gerar_html_energia(energias_dict):
    if not energias_dict: return "<div class='energy-container' style='opacity:0.3; font-size:10px'>Vazio</div>"
    html = "<div class='energy-container'>"
    for tipo_chave, qtd in energias_dict.items():
        img_url = ENERGY_IMGS.get(tipo_chave, "")
        if img_url:
            for _ in range(qtd): html += f"<img src='{img_url}' class='energy-icon' title='{tipo_chave}'>"
        else: html += f"<span style='font-size:12px; margin:0 2px;'>{tipo_chave} x{qtd}</span>"
    html += "</div>"
    return html

def render_custo_html(nome_poke):
    custo = POKEDEX.get(nome_poke, {}).get("custo", ["Incolor ⭐"])
    html = "<div style='display:flex; align-items:center; justify-content:center; gap:2px; margin-bottom:5px;'>"
    html += "<span style='font-size:10px; color:#64748b; font-weight:bold; margin-right:4px'>CUSTO:</span>"
    for c in custo:
        url = ENERGY_IMGS.get(c)
        if url: html += f"<img src='{url}' style='width:16px;'>"
    html += "</div>"
    return html

# --- LÓGICA DO POKEMON (Mantida) ---
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
    def receber_dano(self, dano): self.hp_atual = max(0, self.hp_atual - dano)
    def resolver_checkup(self):
        logs = []
        if self.status == "Envenenado 🧪": self.receber_dano(10); logs.append(f"🧪 {self.nome} sofreu 10 veneno.")
        elif self.status == "Queimado 🔥":
            self.receber_dano(20); logs.append(f"🔥 {self.nome} sofreu 20 queimadura.")
            if random.choice(["CARA", "COROA"]) == "CARA": self.status = "Saudável"; logs.append(f"🪙 {self.nome} curou!")
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
        if tipo in self.energias: self.energias[tipo] -= 1; 
        if self.energias[tipo] <= 0: del self.energias[tipo]; return True
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
        return False, f"Falta energia."

def verificar_custo_ataque(pokemon):
    custo_lista = POKEDEX.get(pokemon.nome, {}).get("custo", ["Incolor ⭐"])
    pool = pokemon.energias.copy()
    for req in [c for c in custo_lista if "Incolor" not in c]:
        if pool.get(req, 0) > 0: pool[req] -= 1
        else: return False 
    incolores_nec = len([c for c in custo_lista if "Incolor" in c])
    return sum(pool.values()) >= incolores_nec

# --- STATE ---
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

def adicionar_log(cat, msg, player=None):
    hora = datetime.datetime.now().strftime("%H:%M")
    colors = {"Ataque": "#fca5a5", "Energia": "#fde047", "KO": "#fdba74", "Turno": "#93c5fd"}
    c = colors.get(cat, "#cbd5e1")
    st.session_state.log.insert(0, f"<div class='log-container'><span style='color:{c}'>[{hora}] <b>{cat}</b></span> {msg}</div>")

inicializar_jogo()

# --- LAYOUT PRINCIPAL ---
c_head, c_actions = st.columns([1, 1.5])
with c_head:
    st.markdown('<div class="main-title">⚔️ PokéBattle</div>', unsafe_allow_html=True)
    nome_vez = st.session_state.Treinadores[st.session_state.turno_atual]['nome']
    st.markdown(f'<div class="turn-display">Vez de: {nome_vez}</div>', unsafe_allow_html=True)

with c_actions:
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="top-btn">', unsafe_allow_html=True)
        with st.popover("Menu", use_container_width=True):
            if st.button("Resetar Jogo"): st.session_state.clear(); st.rerun()
            if st.button("Baixar Log"): pass 
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="top-btn">', unsafe_allow_html=True)
        if st.button("Moeda", use_container_width=True):
             r = random.choice(["CARA", "COROA"]); st.toast(f"{r}")
        st.markdown('</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="action-btn">', unsafe_allow_html=True)
        if st.button("PASSAR VEZ", use_container_width=True):
            # Checkup e Passa
            logs = []
            for p in ["Treinador 1", "Treinador 2"]:
                if st.session_state.Treinadores[p]['ativo']: logs.extend(st.session_state.Treinadores[p]['ativo'].resolver_checkup())
            for l in logs: adicionar_log("Status", l)
            
            st.session_state.habilidades_usadas = []
            st.session_state.evolucoes_turno = []
            st.session_state.energias_anexadas_neste_turno = []
            ant = st.session_state.turno_atual
            novo = "Treinador 2" if ant == "Treinador 1" else "Treinador 1"
            st.session_state.turno_atual = novo
            adicionar_log("Turno", f"Início de {st.session_state.Treinadores[novo]['nome']}")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# --- SIDEBAR (CONFIG) ---
with st.sidebar:
    st.header("⚙️ Configuração")
    with st.expander("👤 Jogadores"):
        n1 = st.text_input("J1", value=st.session_state.Treinadores["Treinador 1"]["nome"])
        n2 = st.text_input("J2", value=st.session_state.Treinadores["Treinador 2"]["nome"])
        if st.button("Salvar Nomes"):
            st.session_state.Treinadores["Treinador 1"]["nome"] = n1
            st.session_state.Treinadores["Treinador 2"]["nome"] = n2; st.rerun()

    st.markdown("### ➕ Cartas")
    dono = st.selectbox("Treinador", ["Treinador 1", "Treinador 2"], format_func=lambda x: st.session_state.Treinadores[x]['nome'])
    p = st.session_state.Treinadores[dono]
    
    escolha = st.selectbox("Pokémon", list(POKEDEX.keys()))
    if st.button(f"Adicionar {escolha}"):
        d = POKEDEX[escolha]
        novo = Pokemon(escolha, d["hp"], d["tipo"], d["fraq"], d["res"], d.get("recuo",1), d["img"], d.get("hab"))
        st.session_state.evolucoes_turno.append(novo.id_unico)
        if not p['ativo']: p['ativo'] = novo; st.rerun()
        elif len(p['banco']) < 5: p['banco'].append(novo); st.rerun()
        else: st.error("Cheio!")

# --- MESA ---
def render_player(key):
    p = st.session_state.Treinadores[key]
    eh_vez = (st.session_state.turno_atual == key)
    borda = "2px solid #fbbf24" if eh_vez else "1px solid #334155"
    
    st.markdown(f"<div style='border:{borda}; background-color:#1e293b; padding:12px; border-radius:12px; margin-bottom:12px;'>", unsafe_allow_html=True)
    
    c1, c2 = st.columns([3, 1])
    c1.markdown(f"<h4 style='margin:0'>{p['nome']}</h4>", unsafe_allow_html=True)
    c2.markdown(f"<h5 style='margin:0; text-align:right; color:#fbbf24'>{p['premios']} 🎴</h5>", unsafe_allow_html=True)
    
    ativo = p['ativo']
    if ativo:
        st.markdown("---")
        c_img, c_info = st.columns([1, 1.8])
        with c_img:
            st.image(ativo.imagem_url, use_container_width=True)
            st.markdown(gerar_html_energia(ativo.energias), unsafe_allow_html=True)
            if ativo.status != "Saudável": st.warning(ativo.status)
        
        with c_info:
            st.markdown(f"**{ativo.nome}** <span style='float:right'>{ativo.hp_atual}/{ativo.hp_max}</span>", unsafe_allow_html=True)
            pct = max(0, min(100, (ativo.hp_atual / ativo.hp_max) * 100))
            color_hp = "#22c55e" if pct > 50 else "#ef4444"
            st.markdown(f"""<div class="hp-bar-bg"><div class="hp-fill" style="width:{pct}%; background-color:{color_hp};"></div></div>""", unsafe_allow_html=True)
            
            # Stats
            rec_img = "".join([f"<img src='{ENERGY_IMGS['Incolor ⭐']}' class='energy-icon'>" for _ in range(ativo.recuo)]) if ativo.recuo else "LIVRE"
            st.markdown(f"""<div class="stats-box"><div class="stat-item">FRAQ<br>{get_icon_html(ativo.fraqueza)}</div><div class="stat-item">RES<br>{get_icon_html(ativo.resistencia)}</div><div class="stat-item">REC<br>{rec_img}</div></div>""", unsafe_allow_html=True)

            if ativo.hp_atual == 0:
                st.markdown('<div class="danger-btn">', unsafe_allow_html=True)
                if st.button("💀 KO / Descartar", key=f"ko_{ativo.id_unico}"):
                    p['descarte'].append(ativo); p['ativo'] = None
                    op_key = "Treinador 2" if key == "Treinador 1" else "Treinador 1"
                    qtd = 2 if "ex" in ativo.nome.lower() else 1
                    st.session_state.Treinadores[op_key]['premios'] -= qtd
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                # Controles
                if ativo.id_unico not in st.session_state.dmg_buffer: st.session_state.dmg_buffer[ativo.id_unico] = 0
                dmg = st.number_input("Dano", value=st.session_state.dmg_buffer[ativo.id_unico], step=10, key=f"d_{ativo.id_unico}")
                st.session_state.dmg_buffer[ativo.id_unico] = dmg
                
                st.markdown(render_custo_html(ativo.nome), unsafe_allow_html=True)
                st.markdown('<div class="action-btn">', unsafe_allow_html=True)
                if st.button("⚔️ ATACAR", key=f"atk_{ativo.id_unico}"):
                    if not verificar_custo_ataque(ativo): st.error("Falta Energia!")
                    else:
                        op_key = "Treinador 2" if key == "Treinador 1" else "Treinador 1"
                        op = st.session_state.Treinadores[op_key]
                        if op['ativo']:
                            mult = 2 if ativo.tipo == op['ativo'].fraqueza else 1
                            final = max(0, (dmg * mult))
                            op['ativo'].receber_dano(final)
                            # Passa Turno Auto
                            st.session_state.habilidades_usadas = []
                            st.session_state.evolucoes_turno = []
                            st.session_state.energias_anexadas_neste_turno = []
                            ant = st.session_state.turno_atual
                            novo = "Treinador 2" if ant == "Treinador 1" else "Treinador 1"
                            st.session_state.turno_atual = novo
                            st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

                with st.popover("⚡ / Status / Tool"):
                    t1, t2, t3 = st.tabs(["Energia", "Status", "Tool"])
                    with t1:
                        e_type = st.selectbox("Tipo", list(ENERGY_IMGS.keys()), key=f"et_{ativo.id_unico}")
                        if st.button("Adicionar", key=f"add_{ativo.id_unico}"):
                            if ativo.id_unico in st.session_state.energias_anexadas_neste_turno: st.error("Já ligou!")
                            else: ativo.anexar_energia(e_type); st.session_state.energias_anexadas_neste_turno.append(ativo.id_unico); st.rerun()
                    with t2: st.selectbox("Status", ["Saudável", "Envenenado 🧪"], key=f"st_{ativo.id_unico}")
                    with t3: st.selectbox("Tool", list(TOOLS_DB.keys()), key=f"tl_{ativo.id_unico}")

    # Banco
    if p['banco']:
        st.markdown("---")
        cols = st.columns(max(5, len(p['banco'])))
        for i, bp in enumerate(p['banco']):
            with cols[i]:
                st.image(bp.imagem_url)
                st.caption(f"HP: {bp.hp_atual}/{bp.hp_max}")
                st.markdown(gerar_html_energia(bp.energias), unsafe_allow_html=True)
                if bp.hp_atual == 0:
                    st.markdown('<div class="danger-btn">', unsafe_allow_html=True)
                    if st.button("💀", key=f"kob_{bp.id_unico}"):
                        p['banco'].pop(i); st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    if st.button("⬆️", key=f"up_{bp.id_unico}"):
                        if not p['ativo']: p['ativo'] = p['banco'].pop(i); st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# --- TELA ---
c1, c2 = st.columns(2)
with c1: render_player("Treinador 1")
with c2: render_player("Treinador 2")

st.divider()
st.subheader("📜 Registro")
st.markdown("".join(st.session_state.log), unsafe_allow_html=True)
