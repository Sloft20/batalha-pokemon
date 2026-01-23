import streamlit as st
import datetime
import random 
import re 

st.set_page_config(page_title="PokéBattle 13.0 (Log Tático)", page_icon="⚔️", layout="wide")

# --- 0. CONFIGURAÇÃO VISUAL ---
def configurar_visual():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap'); /* Fonte mono para log */

        html, body, [class*="css"] { font-family: 'Roboto', sans-serif; }

        /* Fundo Geral */
        [data-testid="stAppViewContainer"] {
            background-color: #0f172a;
            color: #f1f5f9;
        }
        [data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #1e293b;
            border-right: 1px solid #334155;
        }

        /* Containers */
        div[data-testid="stVerticalBlockBorderWrapper"], div[data-testid="stExpander"], div[data-testid="stContainer"] {
            background-color: #1e293b;
            border: 1px solid #334155;
            border-radius: 8px;
        }

        /* Inputs Escuros */
        .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
            background-color: #0f172a !important;
            color: #e2e8f0 !important;
            border: 1px solid #475569 !important;
            border-radius: 6px;
        }

        /* Botões */
        .stButton > button { border-radius: 6px; font-weight: 600; border: none !important; }
        .top-btn > button { background-color: #1e293b !important; border: 1px solid #475569 !important; min-height: 40px; }
        .turn-btn > button { background-color: #FFC107 !important; color: #0f172a !important; font-weight: bold; }
        .game-btn > button { background-color: #334155 !important; color: white !important; width: 100%; }
        .atk-btn > button { background-color: #FFC107 !important; color: #0f172a !important; font-weight: bold; }
        .btn-red > button { background-color: #EF4444 !important; color: white !important; }
        .small-btn > button { padding: 2px 0px !important; font-size: 11px !important; min-height: 25px !important; background-color: #0f172a !important; border: 1px solid #334155 !important; }

        /* Barra de Vida */
        .hp-bar-bg { width: 100%; background-color: #334155; border-radius: 4px; height: 10px; margin-bottom: 10px; }
        .hp-bar-fill { height: 100%; border-radius: 4px; transition: width 0.5s; }

        /* --- ESTILO DO LOG NOVO --- */
        .log-container {
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
            color: #cbd5e1;
            padding: 4px 0;
            border-bottom: 1px solid #334155;
        }
        .log-time { color: #64748b; margin-right: 8px; }
        
        /* Badges de Categoria do Log */
        .tag-log {
            display: inline-block;
            padding: 1px 6px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 10px;
            margin-right: 8px;
            text-transform: uppercase;
            width: 70px; /* Largura fixa para alinhar */
            text-align: center;
        }
        .tag-inicio { background-color: #22c55e; color: #0f172a; }
        .tag-turno { background-color: #3b82f6; color: #fff; }
        .tag-ataque { background-color: #ef4444; color: #fff; }
        .tag-energia { background-color: #eab308; color: #0f172a; }
        .tag-tool { background-color: #a855f7; color: #fff; }
        .tag-ko { background-color: #000; color: #ef4444; border: 1px solid #ef4444; }
        .tag-status { background-color: #f97316; color: #fff; }

        .turn-display { font-size: 18px; font-weight: bold; color: #FFC107; margin-top: -15px; margin-bottom: 10px; }
        .main-title { font-size: 28px; font-weight: 800; color: #f1f5f9; margin-bottom: 0px; }
    </style>
    """, unsafe_allow_html=True)

configurar_visual()

# --- 1. BANCO DE DADOS ---
POKEDEX = {
    "Dragapult ex": {"hp": 320, "tipo": "Dragão 🐉", "fraq": "Nenhuma", "res": "Nenhuma", "recuo": 1, "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/TWM/TWM_130_R_EN_PNG.png"},
    "Drakloak": {"hp": 90, "tipo": "Dragão 🐉", "fraq": "Nenhuma", "res": "Nenhuma", "recuo": 1, "hab": "Reconhecimento", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/TWM/TWM_129_R_EN_PNG.png"},
    "Dreepy": {"hp": 70, "tipo": "Dragão 🐉", "fraq": "Nenhuma", "res": "Nenhuma", "recuo": 1, "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/TWM/TWM_128_R_EN_PNG.png"},
    "Xatu": {"hp": 100, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "recuo": 1, "hab": "Sentido Clarividente", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/PAR/PAR_072_R_EN_PNG.png"},
    "Natu": {"hp": 60, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "recuo": 1, "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/PAR/PAR_071_R_EN_PNG.png"},
    "Fezandipiti ex": {"hp": 210, "tipo": "Psíquico 🌀", "fraq": "Metal ⚙️", "res": "Nenhuma", "recuo": 1, "hab": "Virar o Jogo", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/SFA/SFA_038_R_EN_PNG.png"},
    "Charizard ex": {"hp": 330, "tipo": "Escuridão 🌙", "fraq": "Planta 🌱", "res": "Nenhuma", "recuo": 2, "hab": "Reino Infernal", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/OBF/OBF_125_R_EN_PNG.png"},
    "Charmeleon": {"hp": 90, "tipo": "Fogo 🔥", "fraq": "Água 💧", "res": "Nenhuma", "recuo": 2, "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/OBF/OBF_027_R_EN_PNG.png"},
    "Charmander": {"hp": 70, "tipo": "Fogo 🔥", "fraq": "Água 💧", "res": "Nenhuma", "recuo": 1, "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/OBF/OBF_026_R_EN_PNG.png"},
    "Pidgeot ex": {"hp": 280, "tipo": "Normal ⚪", "fraq": "Elétrico ⚡", "res": "Luta 🥊", "recuo": 0, "hab": "Busca Rápida", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/OBF/OBF_164_R_EN_PNG.png"},
    "Pidgey": {"hp": 60, "tipo": "Normal ⚪", "fraq": "Elétrico ⚡", "res": "Luta 🥊", "recuo": 1, "hab": "Chamar a Família", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/OBF/OBF_162_R_EN_PNG.png"},
    "Moltres": {"hp": 120, "tipo": "Fogo 🔥", "fraq": "Água 💧", "res": "Nenhuma", "recuo": 1, "hab": "Símbolo de Fogo", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/BRS/BRS_021_R_EN_PNG.png"},
    "Gardevoir ex": {"hp": 310, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "recuo": 2, "hab": "Abraço Psíquico", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/SVI/SVI_086_R_EN_PNG.png"},
    "Kirlia": {"hp": 80, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "recuo": 2, "hab": "Refinamento", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/SVI/SVI_085_R_EN_PNG.png"},
    "Ralts": {"hp": 60, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "recuo": 1, "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/SVI/SVI_084_R_EN_PNG.png"},
    "Drifloon": {"hp": 70, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "recuo": 1, "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/SVI/SVI_089_R_EN_PNG.png"},
    "Scream Tail": {"hp": 90, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "recuo": 1, "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/PAR/PAR_086_R_EN_PNG.png"},
    "Mew ex": {"hp": 180, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "recuo": 0, "hab": "Reinício", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/MEW/MEW_151_R_EN_PNG.png"},
    "Radiant Greninja": {"hp": 130, "tipo": "Água 💧", "fraq": "Elétrico ⚡", "res": "Nenhuma", "recuo": 1, "hab": "Cartas Ocultas", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/ASR/ASR_046_R_EN_PNG.png"},
    "Lugia VSTAR": {"hp": 280, "tipo": "Normal ⚪", "fraq": "Elétrico ⚡", "res": "Luta 🥊", "recuo": 2, "hab": "Astro Invocador", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/SIT/SIT_139_R_EN_PNG.png"},
    "Lugia V": {"hp": 220, "tipo": "Normal ⚪", "fraq": "Elétrico ⚡", "res": "Luta 🥊", "recuo": 2, "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/SIT/SIT_138_R_EN_PNG.png"},
    "Archeops": {"hp": 150, "tipo": "Normal ⚪", "fraq": "Elétrico ⚡", "res": "Luta 🥊", "recuo": 1, "hab": "Turbo Primitivo", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/SIT/SIT_147_R_EN_PNG.png"},
}

TOOLS_DB = {
    "Nenhuma": {"efeito": "nada", "hp_bonus": 0},
    "Pingente de Bravura (+50 HP)": {"efeito": "hp", "hp_bonus": 50},
    "Capa do Herói (+100 HP)": {"efeito": "hp", "hp_bonus": 100},
    "Cinto Máximo (+50 Dano ex)": {"efeito": "dmg", "hp_bonus": 0},
    "Faixa de Desafio (+30 Dano)": {"efeito": "dmg", "hp_bonus": 0},
    "Skate de Resgate (-1 Recuo)": {"efeito": "util", "hp_bonus": 0},
    "MT: Evolução": {"efeito": "atk", "hp_bonus": 0},
    "MT: Devolução": {"efeito": "atk", "hp_bonus": 0},
}

# --- 2. CLASSES ---
class Pokemon:
    def __init__(self, nome, hp_max, tipo, fraqueza, resistencia, recuo, imagem_url="", habilidade=None):
        self.nome = nome
        self.hp_base = int(hp_max)
        self.hp_max = int(hp_max)
        self.hp_atual = int(hp_max)
        img_padrao = "https://upload.wikimedia.org/wikipedia/en/3/3b/Pokemon_Trading_Card_Game_cardback.jpg"
        self.imagem_url = imagem_url if imagem_url else img_padrao
        self.id_unico = datetime.datetime.now().timestamp() + random.random()
        self.tipo = tipo
        self.fraqueza = fraqueza
        self.resistencia = resistencia
        self.recuo = recuo
        self.status = "Saudável"
        self.energias = {}
        self.ferramenta = "Nenhuma"
        if habilidade: self.habilidade = habilidade
        else: self.habilidade = POKEDEX[nome].get("hab") if nome in POKEDEX else None

    def equipar_ferramenta(self, nome_ferramenta):
        if self.ferramenta in TOOLS_DB:
            bonus_antigo = TOOLS_DB[self.ferramenta]["hp_bonus"]
            self.hp_max -= bonus_antigo
            if self.hp_atual > self.hp_max: self.hp_atual = self.hp_max
        self.ferramenta = nome_ferramenta
        if nome_ferramenta in TOOLS_DB:
            novo_bonus = TOOLS_DB[nome_ferramenta]["hp_bonus"]
            self.hp_max += novo_bonus
            self.hp_atual += novo_bonus
        return True

    def receber_dano(self, dano):
        self.hp_atual -= dano
        if self.hp_atual < 0: self.hp_atual = 0
        if self.hp_atual > self.hp_max: self.hp_atual = self.hp_max

    def resolver_checkup(self):
        logs = []
        if self.status == "Envenenado 🧪":
            self.receber_dano(10); logs.append(f"🧪 {self.nome} sofreu 10 de veneno.")
        elif self.status == "Queimado 🔥":
            self.receber_dano(20); logs.append(f"🔥 {self.nome} sofreu 20 de queimadura.")
            if random.choice(["CARA", "COROA"]) == "CARA":
                self.status = "Saudável"; logs.append(f"🪙 {self.nome} curou queimadura!")
            else: logs.append(f"🪙 {self.nome} continua queimado.")
        elif self.status == "Adormecido 💤":
            if random.choice(["CARA", "COROA"]) == "CARA":
                self.status = "Saudável"; logs.append(f"🪙 {self.nome} acordou!")
            else: logs.append(f"🪙 {self.nome} dormindo.")
        return logs

    def evoluir_para(self, novo_nome, novo_hp, novo_tipo, nova_fraqueza, nova_resistencia, nova_img, nova_hab=None):
        dano_sofrido = self.hp_max - self.hp_atual
        self.nome = novo_nome
        self.hp_base = int(novo_hp)
        bonus_ferramenta = TOOLS_DB[self.ferramenta]["hp_bonus"]
        self.hp_max = self.hp_base + bonus_ferramenta
        self.tipo = novo_tipo
        self.fraqueza = nova_fraqueza
        self.resistencia = nova_resistencia
        dados_novos = POKEDEX.get(novo_nome, {})
        self.recuo = dados_novos.get("recuo", 1) 
        if nova_img: self.imagem_url = nova_img
        self.habilidade = nova_hab if nova_hab else dados_novos.get("hab")
        self.hp_atual = self.hp_max - dano_sofrido
        if self.hp_atual < 0: self.hp_atual = 0
        self.status = "Saudável"

    def anexar_energia(self, tipo_energia):
        if tipo_energia in self.energias: self.energias[tipo_energia] += 1
        else: self.energias[tipo_energia] = 1

    def remover_energia(self, tipo_energia):
        if tipo_energia in self.energias:
            self.energias[tipo_energia] -= 1
            if self.energias[tipo_energia] <= 0: del self.energias[tipo_energia]
            return True
        return False
    
    def tentar_recuar(self):
        total_energias = sum(self.energias.values())
        custo = self.recuo
        if self.ferramenta == "Skate de Resgate (-1 Recuo)": custo = max(0, custo - 1)
        if total_energias >= custo:
            removidas = 0
            chaves = list(self.energias.keys())
            for tipo in chaves:
                while self.energias[tipo] > 0 and removidas < custo:
                    self.energias[tipo] -= 1
                    removidas += 1
                if self.energias[tipo] <= 0: del self.energias[tipo]
            self.status = "Saudável"
            return True, f"Pagou {custo} de energia."
        else: return False, f"Precisa de {custo} energias."

# --- 3. ESTADO ---
def inicializar_jogo():
    if 'Treinadores' not in st.session_state:
        st.session_state.Treinadores = {
            "Treinador 1": {"nome": "Treinador 1", "ativo": None, "banco": [], "descarte": [], "premios": 6},
            "Treinador 2": {"nome": "Treinador 2", "ativo": None, "banco": [], "descarte": [], "premios": 6}
        }
    if 'log' not in st.session_state: st.session_state.log = []
    if 'vencedor' not in st.session_state: st.session_state.vencedor = None
    if 'turno_atual' not in st.session_state: st.session_state.turno_atual = "Treinador 1"
    if 'habilidades_usadas' not in st.session_state: st.session_state.habilidades_usadas = []
    if 'dmg_buffer' not in st.session_state: st.session_state.dmg_buffer = {}

# --- FUNÇÃO DE LOG NOVA ---
def adicionar_log(categoria, mensagem):
    hora = datetime.datetime.now().strftime("%H:%M")
    
    # Classes CSS por categoria
    cat_class = {
        "Inicio": "tag-inicio",
        "Turno": "tag-turno",
        "Ataque": "tag-ataque",
        "Energia": "tag-energia",
        "Tool": "tag-tool",
        "KO": "tag-ko",
        "Status": "tag-status",
        "Moeda": "tag-tool"
    }.get(categoria, "tag-log")
    
    html = f"""
    <div class='log-container'>
        <span class='log-time'>[{hora}]</span>
        <span class='tag-log {cat_class}'>{categoria}</span>
        <span>{mensagem}</span>
    </div>
    """
    st.session_state.log.insert(0, html)

inicializar_jogo()

# --- 4. TOP BAR ---
col_top_title, col_top_actions = st.columns([1.5, 3])

with col_top_title:
    st.markdown('<div class="main-title">⚔️ PokéBattle</div>', unsafe_allow_html=True)
    nome_vez = st.session_state.Treinadores[st.session_state.turno_atual]['nome']
    st.markdown(f'<div class="turn-display">👉 Vez de: {nome_vez}</div>', unsafe_allow_html=True)

with col_top_actions:
    c_p1, c_coin, c_reset, c_log, c_turn = st.columns([1, 1, 1, 1, 1.5])
    with c_p1:
        st.markdown('<div class="top-btn">', unsafe_allow_html=True)
        if st.button("🏆 Placar", use_container_width=True):
            st.toast(f"P1: {st.session_state.Treinadores['Treinador 1']['premios']} | P2: {st.session_state.Treinadores['Treinador 2']['premios']}")
        st.markdown('</div>', unsafe_allow_html=True)
    with c_coin:
        st.markdown('<div class="top-btn">', unsafe_allow_html=True)
        if st.button("🪙 Moeda", use_container_width=True):
            r = random.choice(["CARA", "COROA"])
            st.toast(f"Moeda: {r}"); adicionar_log("Moeda", f"Resultado: {r}")
        st.markdown('</div>', unsafe_allow_html=True)
    with c_reset:
        st.markdown('<div class="top-btn">', unsafe_allow_html=True)
        if st.button("🗑️ Reset", use_container_width=True):
            st.session_state.clear(); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c_log:
        st.markdown('<div class="top-btn">', unsafe_allow_html=True)
        if st.session_state.log:
            txt = "\n".join([re.sub('<[^<]+?>', '', l) for l in st.session_state.log[::-1]])
            st.download_button("📜 Baixar", txt, "log.txt", use_container_width=True)
        else: st.button("📜 Baixar", disabled=True, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c_turn:
        st.markdown('<div class="turn-btn">', unsafe_allow_html=True)
        if st.button("➡ Fim Turno", help="Faz Checkup e Passa Vez", use_container_width=True):
            logs_check = []
            for p in ["Treinador 1", "Treinador 2"]:
                if st.session_state.Treinadores[p]['ativo']:
                    r = st.session_state.Treinadores[p]['ativo'].resolver_checkup()
                    if r: 
                        for msg in r: adicionar_log("Status", msg)
            
            st.session_state.habilidades_usadas = []
            antigo = st.session_state.turno_atual
            novo = "Treinador 2" if antigo == "Treinador 1" else "Treinador 1"
            st.session_state.turno_atual = novo
            adicionar_log("Turno", f"Fim de turno de {st.session_state.Treinadores[antigo]['nome']}. Início de {st.session_state.Treinadores[novo]['nome']}.")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# --- 5. SIDEBAR (CONFIG) ---
with st.sidebar:
    st.header("⚙️ Configuração")
    with st.expander("👤 Nomes", expanded=False):
        n1 = st.text_input("J1", value=st.session_state.Treinadores["Treinador 1"]["nome"])
        n2 = st.text_input("J2", value=st.session_state.Treinadores["Treinador 2"]["nome"])
        if st.button("Salvar Nomes"):
            st.session_state.Treinadores["Treinador 1"]["nome"] = n1
            st.session_state.Treinadores["Treinador 2"]["nome"] = n2
            st.rerun()
    
    st.markdown("### ➕ Adicionar")
    dono_key = st.selectbox("Treinador", ["Treinador 1", "Treinador 2"], format_func=lambda x: st.session_state.Treinadores[x]['nome'])
    modo = st.radio("Modo", ["📚 Pokedex", "✍️ Manual"])
    
    if "Pokedex" in modo:
        escolha = st.selectbox("Poke", list(POKEDEX.keys()))
        dados = POKEDEX[escolha]
        st.image(dados["img"], width=100)
        if st.button("Adicionar"):
            novo = Pokemon(escolha, dados["hp"], dados["tipo"], dados["fraq"], dados["res"], dados.get("recuo", 1), dados["img"], dados.get("hab"))
            player = st.session_state.Treinadores[dono_key]
            if not player['ativo']: 
                player['ativo'] = novo
                adicionar_log("Inicio", f"{escolha} entrou como Ativo de {player['nome']}.")
            elif len(player['banco']) < 5: 
                player['banco'].append(novo)
                adicionar_log("Inicio", f"{escolha} entrou no Banco de {player['nome']}.")
            else: st.error("Cheio!")
            st.rerun()
    else:
        nome_m = st.text_input("Nome")
        hp_m = st.number_input("HP", value=60, step=10)
        img_m = st.text_input("URL Imagem")
        if st.button("Criar"):
            novo = Pokemon(nome_m, hp_m, "Normal", "Nenhuma", "Nenhuma", 1, img_m)
            player = st.session_state.Treinadores[dono_key]
            if not player['ativo']: player['ativo'] = novo
            elif len(player['banco']) < 5: player['banco'].append(novo)
            st.rerun()

# --- 6. RENDERIZAÇÃO ---
def checar_vitoria(id_oponente_chave):
    if st.session_state.Treinadores[id_oponente_chave]['premios'] <= 0: return True
    oponente = st.session_state.Treinadores[id_oponente_chave]
    if oponente['ativo'] is None and len(oponente['banco']) == 0: return True
    return False

def render_player(key):
    p = st.session_state.Treinadores[key]
    eh_vez = (st.session_state.turno_atual == key)
    borda = "2px solid #FFC107" if eh_vez else "1px solid #334155"
    opacity = "1" if eh_vez else "0.8"
    
    st.markdown(f"<div style='border:{borda}; opacity:{opacity}; background-color:#1e293b; padding:10px; border-radius:10px; margin-bottom:10px;'>", unsafe_allow_html=True)
    
    c_h1, c_h2 = st.columns([3, 1])
    c_h1.markdown(f"<h4 style='margin:0'>{p['nome']}</h4>", unsafe_allow_html=True)
    c_h2.markdown(f"<h5 style='margin:0; text-align:right'>{p['premios']} 🎴</h5>", unsafe_allow_html=True)
    
    ativo = p['ativo']
    if ativo:
        st.markdown("---")
        c_img, c_info = st.columns([1, 1.8])
        with c_img:
            st.image(ativo.imagem_url, use_container_width=True)
            if ativo.status != "Saudável": st.warning(ativo.status)
            txt_en = " ".join([f"{k.split()[-1]}x{v}" for k,v in ativo.energias.items()])
            if txt_en: st.markdown(f"<div style='background:#0f172a; padding:4px; border-radius:4px; margin-top:5px; font-size:12px; border:1px solid #334155; text-align:center;'>⚡ {txt_en}</div>", unsafe_allow_html=True)
            if ativo.ferramenta != "Nenhuma": st.caption(f"🛠️ {ativo.ferramenta}")

        with c_info:
            st.markdown(f"**{ativo.nome}** <span style='float:right; font-size:12px;'>{ativo.hp_atual}/{ativo.hp_max}</span>", unsafe_allow_html=True)
            pct = max(0, min(100, (ativo.hp_atual / ativo.hp_max) * 100))
            color_hp = "#22c55e" if pct > 50 else ("#eab308" if pct > 20 else "#ef4444")
            st.markdown(f"""<div class="hp-bar-bg"><div class="hp-bar-fill" style="width:{pct}%; background-color:{color_hp};"></div></div>""", unsafe_allow_html=True)
            
            if ativo.hp_atual == 0:
                st.error("💀 NOCAUTEADO")
                st.markdown('<div class="btn-red">', unsafe_allow_html=True)
                if st.button("Enviar p/ Descarte", key=f"ko_{ativo.id_unico}"):
                    p['descarte'].append(ativo)
                    p['ativo'] = None
                    adicionar_log("KO", f"💀 {ativo.nome} foi nocauteado!")
                    op_key = "Treinador 2" if key == "Treinador 1" else "Treinador 1"
                    qtd = 2 if "ex" in ativo.nome.lower() else 1
                    st.session_state.Treinadores[op_key]['premios'] -= qtd
                    adicionar_log("KO", f"🏆 Oponente pegou {qtd} prêmio(s).")
                    if checar_vitoria(key): st.session_state.vencedor = st.session_state.Treinadores[op_key]['nome']
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                if ativo.id_unico not in st.session_state.dmg_buffer: st.session_state.dmg_buffer[ativo.id_unico] = 0
                cb1, cb2, cb3, cb4 = st.columns(4)
                with cb1: 
                    st.markdown('<div class="small-btn">', unsafe_allow_html=True)
                    if st.button("0", key=f"z_{ativo.id_unico}"): st.session_state.dmg_buffer[ativo.id_unico] = 0; st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                with cb2: 
                    st.markdown('<div class="small-btn">', unsafe_allow_html=True)
                    if st.button("+10", key=f"p10_{ativo.id_unico}"): st.session_state.dmg_buffer[ativo.id_unico] += 10; st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                with cb3: 
                    st.markdown('<div class="small-btn">', unsafe_allow_html=True)
                    if st.button("+20", key=f"p20_{ativo.id_unico}"): st.session_state.dmg_buffer[ativo.id_unico] += 20; st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                with cb4: 
                    st.markdown('<div class="small-btn">', unsafe_allow_html=True)
                    if st.button("+50", key=f"p50_{ativo.id_unico}"): st.session_state.dmg_buffer[ativo.id_unico] += 50; st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                
                dmg = st.number_input("Dano", value=st.session_state.dmg_buffer[ativo.id_unico], step=10, key=f"d_{ativo.id_unico}", label_visibility="collapsed")
                st.session_state.dmg_buffer[ativo.id_unico] = dmg

                st.markdown('<div class="atk-btn">', unsafe_allow_html=True)
                if st.button("⚔️ ATACAR", key=f"atk_{ativo.id_unico}"):
                    op_key = "Treinador 2" if key == "Treinador 1" else "Treinador 1"
                    op = st.session_state.Treinadores[op_key]
                    if op['ativo']:
                        mult = 2 if ativo.tipo == op['ativo'].fraqueza else 1
                        red = 30 if ativo.tipo == op['ativo'].resistencia else 0
                        final = (dmg * mult) - red
                        if final < 0: final = 0
                        op['ativo'].receber_dano(final)
                        
                        # LOG DETALHADO DE ATAQUE
                        msg_atk = f"{p['nome']}: {ativo.nome} causou {final} dano em {op['ativo'].nome} (Base: {dmg}). HP Restante: {op['ativo'].hp_atual}"
                        adicionar_log("Ataque", msg_atk)
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
                
                with st.popover("⚡ Energia / Status / Tool"):
                    t1, t2, t3, t4 = st.tabs(["+ E", "- E", "Stat", "Tool"])
                    with t1:
                        e = st.selectbox("Tipo", ["Fogo 🔥", "Água 💧", "Planta 🌱", "Elétrico ⚡", "Psíquico 🌀", "Luta 🥊", "Escuridão 🌙", "Metal ⚙️"], key=f"ae_{ativo.id_unico}")
                        if st.button("Add", key=f"bae_{ativo.id_unico}"): 
                            ativo.anexar_energia(e)
                            adicionar_log("Energia", f"{p['nome']}: Anexou {e} em {ativo.nome}.")
                            st.rerun()
                    with t2:
                        if ativo.energias:
                            r = st.selectbox("Remover", list(ativo.energias.keys()), key=f"re_{ativo.id_unico}")
                            if st.button("Del", key=f"bre_{ativo.id_unico}"): 
                                ativo.remover_energia(r)
                                adicionar_log("Energia", f"{p['nome']}: Removeu {r} de {ativo.nome}.")
                                st.rerun()
                        else: st.info("Vazio")
                    with t3:
                        st.selectbox("Status", ["Saudável", "Envenenado 🧪", "Queimado 🔥", "Adormecido 💤", "Paralisado ⚡"], key=f"st_{ativo.id_unico}", on_change=lambda: setattr(ativo, 'status', st.session_state[f"st_{ativo.id_unico}"]))
                    with t4:
                        tl = st.selectbox("Tool", list(TOOLS_DB.keys()), key=f"tl_{ativo.id_unico}")
                        if st.button("Equipar", key=f"btl_{ativo.id_unico}"): 
                            ativo.equipar_ferramenta(tl)
                            adicionar_log("Tool", f"{p['nome']}: Equipou {tl} em {ativo.nome}.")
                            st.rerun()

                if ativo.habilidade:
                    ja = ativo.id_unico in st.session_state.habilidades_usadas
                    cls = "game-btn" if ja else "game-btn"
                    lbl = "✅ Hab Usada" if ja else f"✨ {ativo.habilidade}"
                    st.markdown(f'<div class="{cls}">', unsafe_allow_html=True)
                    if st.button(lbl, key=f"hab_{ativo.id_unico}", disabled=ja):
                        st.session_state.habilidades_usadas.append(ativo.id_unico)
                        adicionar_log("Tool", f"✨ {ativo.nome} usou habilidade {ativo.habilidade}.")
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                
                custo = ativo.recuo
                if ativo.ferramenta == "Skate de Resgate (-1 Recuo)": custo = max(0, custo - 1)
                if st.button(f"🏃 Recuar ({custo})", key=f"run_{ativo.id_unico}"):
                    pode, msg = ativo.tentar_recuar()
                    if pode:
                        if p['banco']:
                            p['banco'].append(ativo)
                            p['ativo'] = None
                            adicionar_log("Inicio", f"🏃 {ativo.nome} recuou para o banco.")
                            st.rerun()
                        else: st.warning("Banco vazio!")
                    else: st.error(msg)

    if p['banco']:
        st.markdown("---")
        cols = st.columns(5)
        for i, bp in enumerate(p['banco']):
            with cols[i]:
                st.image(bp.imagem_url, use_container_width=True)
                if bp.hp_atual == 0:
                    st.markdown('<div class="btn-red">', unsafe_allow_html=True)
                    if st.button("💀", key=f"ko_b_{bp.id_unico}"):
                        p['banco'].pop(i); p['descarte'].append(bp)
                        adicionar_log("KO", f"💀 {bp.nome} (Banco) nocauteado.")
                        op_key = "Treinador 2" if key == "Treinador 1" else "Treinador 1"
                        q = 2 if "ex" in bp.nome.lower() else 1
                        st.session_state.Treinadores[op_key]['premios'] -= q
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    if st.button("⬆️", key=f"up_{bp.id_unico}"):
                        if not p['ativo']: 
                            p['ativo'] = p['banco'].pop(i)
                            adicionar_log("Inicio", f"🆙 {bp.nome} subiu para o Ativo.")
                            st.rerun()
                    if st.button("💔", key=f"dmb_{bp.id_unico}"): bp.receber_dano(10); st.rerun()
                    if bp.habilidade:
                        ja = bp.id_unico in st.session_state.habilidades_usadas
                        if st.button("✨", key=f"hbb_{bp.id_unico}", disabled=ja, help=bp.habilidade):
                            st.session_state.habilidades_usadas.append(bp.id_unico)
                            adicionar_log("Tool", f"✨ {bp.nome} (Banco) usou habilidade.")
                            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# --- 7. TELA PRINCIPAL ---
if st.session_state.vencedor:
    st.balloons()
    st.markdown(f"<h1 style='text-align:center'>🏆 {st.session_state.vencedor} VENCEU!</h1>", unsafe_allow_html=True)
    if st.button("Novo Jogo"): st.session_state.clear(); st.rerun()
else:
    c1, c2 = st.columns(2)
    with c1: render_player("Treinador 1")
    with c2: render_player("Treinador 2")
    
    st.divider()
    st.subheader("📜 Registro de Batalha")
    with st.container(height=300):
        st.markdown("".join(st.session_state.log), unsafe_allow_html=True)
