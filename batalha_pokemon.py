import streamlit as st
import datetime
import random 
import re 

st.set_page_config(page_title="PokéBattle 10.0 (Ultimate UI)", page_icon="⚔️", layout="wide")

# --- 0. CONFIGURAÇÃO DE IMAGENS ---
# Mude este link se você tiver um repositório melhor. 
# Se usar "", ele usa os links individuais do dicionário POKEDEX.
BASE_IMG_URL = "" 

# --- 1. CSS PREMIUM (ESTILO DARK NAVY) ---
def configurar_visual():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
        html, body, [class*="css"] { font-family: 'Roboto', sans-serif; }

        /* Fundo Geral */
        [data-testid="stAppViewContainer"] {
            background-color: #0f172a; /* Azul Navy Profundo */
            color: #f1f5f9;
        }
        [data-testid="stHeader"] { background-color: rgba(0,0,0,0); }

        /* Containers (Cartas e Painéis) */
        div[data-testid="stVerticalBlockBorderWrapper"], div[data-testid="stExpander"] {
            background-color: #1e293b; /* Azul um pouco mais claro */
            border: 1px solid #334155;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        }

        /* Inputs e Selects */
        .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
            background-color: #0f172a !important;
            color: #e2e8f0 !important;
            border: 1px solid #475569 !important;
            border-radius: 6px;
        }

        /* --- BOTÕES PERSONALIZADOS --- */
        .stButton > button {
            border-radius: 8px;
            font-weight: 600;
            border: none !important;
            transition: all 0.2s;
        }

        /* Botão AMARELO (Ação Principal - Atacar/Adicionar) */
        .btn-yellow > button {
            background-color: #FFC107 !important;
            color: #0f172a !important;
        }
        .btn-yellow > button:hover { background-color: #FFD54F !important; transform: scale(1.02); }

        /* Botão AZUL (Log/Ranking) */
        .btn-blue > button {
            background-color: #3B82F6 !important;
            color: white !important;
        }
        
        /* Botão VERMELHO (Reset/Dano) */
        .btn-red > button {
            background-color: #EF4444 !important;
            color: white !important;
        }

        /* Botão VERDE (Turno) */
        .btn-green > button {
            background-color: #22c55e !important;
            color: white !important;
        }

        /* Botões Pequenos de Dano (+10, +20) */
        .btn-small > button {
            background-color: #334155 !important;
            color: white !important;
            padding: 2px 8px !important;
            font-size: 12px !important;
            min-height: 0px !important;
            height: 30px !important;
        }
        .btn-small > button:hover { background-color: #475569 !important; }

        /* Badges (Etiquetas) */
        .badge {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
            margin-right: 5px;
        }
        .badge-ex { background-color: #FFC107; color: black; }
        .badge-status { background-color: #22c55e; color: black; }
        .badge-type { background-color: #64748b; color: white; }
        
        /* Barra de Progresso Custom */
        .stProgress > div > div > div > div {
            background-color: #22c55e; /* Verde Vida */
        }

        hr { border-color: #334155; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

configurar_visual()

# --- 2. BANCO DE DADOS ---
POKEDEX = {
    "Dragapult ex": {"hp": 320, "tipo": "Dragão 🐉", "fraq": "Nenhuma", "res": "Nenhuma", "recuo": 1, "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/TWM/TWM_130_R_EN_PNG.png"},
    "Drakloak": {"hp": 90, "tipo": "Dragão 🐉", "fraq": "Nenhuma", "res": "Nenhuma", "recuo": 1, "hab": "Reconnaissance", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/TWM/TWM_129_R_EN_PNG.png"},
    "Dreepy": {"hp": 70, "tipo": "Dragão 🐉", "fraq": "Nenhuma", "res": "Nenhuma", "recuo": 1, "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/TWM/TWM_128_R_EN_PNG.png"},
    "Xatu": {"hp": 100, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "recuo": 1, "hab": "Clairvoyant Sense", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/PAR/PAR_072_R_EN_PNG.png"},
    "Natu": {"hp": 60, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "recuo": 1, "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/PAR/PAR_071_R_EN_PNG.png"},
    "Fezandipiti ex": {"hp": 210, "tipo": "Psíquico 🌀", "fraq": "Metal ⚙️", "res": "Nenhuma", "recuo": 1, "hab": "Flip the Script", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/SFA/SFA_038_R_EN_PNG.png"},
    "Charizard ex": {"hp": 330, "tipo": "Escuridão 🌙", "fraq": "Planta 🌱", "res": "Nenhuma", "recuo": 2, "hab": "Infernal Reign", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/OBF/OBF_125_R_EN_PNG.png"},
    "Charmeleon": {"hp": 90, "tipo": "Fogo 🔥", "fraq": "Água 💧", "res": "Nenhuma", "recuo": 2, "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/OBF/OBF_027_R_EN_PNG.png"},
    "Charmander": {"hp": 70, "tipo": "Fogo 🔥", "fraq": "Água 💧", "res": "Nenhuma", "recuo": 1, "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/OBF/OBF_026_R_EN_PNG.png"},
    "Pidgeot ex": {"hp": 280, "tipo": "Normal ⚪", "fraq": "Elétrico ⚡", "res": "Luta 🥊", "recuo": 0, "hab": "Quick Search", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/OBF/OBF_164_R_EN_PNG.png"},
    "Pidgey": {"hp": 60, "tipo": "Normal ⚪", "fraq": "Elétrico ⚡", "res": "Luta 🥊", "recuo": 1, "hab": "Call for Family", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/OBF/OBF_162_R_EN_PNG.png"},
    "Moltres": {"hp": 120, "tipo": "Fogo 🔥", "fraq": "Água 💧", "res": "Nenhuma", "recuo": 1, "hab": "Flare Symbol", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/BRS/BRS_021_R_EN_PNG.png"},
    "Gardevoir ex": {"hp": 310, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "recuo": 2, "hab": "Psychic Embrace", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/SVI/SVI_086_R_EN_PNG.png"},
    "Kirlia": {"hp": 80, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "recuo": 2, "hab": "Refinement", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/SVI/SVI_085_R_EN_PNG.png"},
    "Ralts": {"hp": 60, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "recuo": 1, "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/SVI/SVI_084_R_EN_PNG.png"},
    "Drifloon": {"hp": 70, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "recuo": 1, "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/SVI/SVI_089_R_EN_PNG.png"},
    "Scream Tail": {"hp": 90, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "recuo": 1, "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/PAR/PAR_086_R_EN_PNG.png"},
    "Mew ex": {"hp": 180, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "recuo": 0, "hab": "Restart", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/MEW/MEW_151_R_EN_PNG.png"},
    "Radiant Greninja": {"hp": 130, "tipo": "Água 💧", "fraq": "Elétrico ⚡", "res": "Nenhuma", "recuo": 1, "hab": "Concealed Cards", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/ASR/ASR_046_R_EN_PNG.png"},
    "Lugia VSTAR": {"hp": 280, "tipo": "Normal ⚪", "fraq": "Elétrico ⚡", "res": "Luta 🥊", "recuo": 2, "hab": "Summoning Star", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/SIT/SIT_139_R_EN_PNG.png"},
    "Lugia V": {"hp": 220, "tipo": "Normal ⚪", "fraq": "Elétrico ⚡", "res": "Luta 🥊", "recuo": 2, "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/SIT/SIT_138_R_EN_PNG.png"},
    "Archeops": {"hp": 150, "tipo": "Normal ⚪", "fraq": "Elétrico ⚡", "res": "Luta 🥊", "recuo": 1, "hab": "Primal Turbo", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/SIT/SIT_147_R_EN_PNG.png"},
}

TOOLS_DB = {
    "Nenhuma": {"efeito": "nada", "hp_bonus": 0},
    "Bravery Charm (+50 HP)": {"efeito": "hp", "hp_bonus": 50},
    "Hero's Cape (+100 HP)": {"efeito": "hp", "hp_bonus": 100},
    "Maximum Belt (+50 Dmg ex)": {"efeito": "dmg", "hp_bonus": 0},
    "Defiance Band (+30 Dmg)": {"efeito": "dmg", "hp_bonus": 0},
    "Rescue Board (-1 Recuo)": {"efeito": "util", "hp_bonus": 0},
    "TM: Evolution": {"efeito": "atk", "hp_bonus": 0},
    "TM: Devolution": {"efeito": "atk", "hp_bonus": 0},
}

# --- 3. CLASSES E LÓGICA ---
class Pokemon:
    def __init__(self, nome, hp_max, tipo, fraqueza, resistencia, recuo, imagem_url="", habilidade=None):
        self.nome = nome
        self.hp_base = int(hp_max)
        self.hp_max = int(hp_max)
        self.hp_atual = int(hp_max)
        
        # Lógica de Imagem (Repositório Custom ou Padrão)
        img_padrao = imagem_url if imagem_url else "https://upload.wikimedia.org/wikipedia/en/3/3b/Pokemon_Trading_Card_Game_cardback.jpg"
        if BASE_IMG_URL:
            # Exemplo: Se sua URL for "mysite.com/cards/", ele tentará "mysite.com/cards/Charizard ex.png"
            self.imagem_url = f"{BASE_IMG_URL}/{nome}.png"
        else:
            self.imagem_url = img_padrao
            
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
            self.receber_dano(10)
            logs.append(f"🧪 {self.nome} sofreu 10 de veneno.")
        elif self.status == "Queimado 🔥":
            self.receber_dano(20)
            logs.append(f"🔥 {self.nome} sofreu 20 de queimadura.")
            moeda = random.choice(["CARA", "COROA"])
            if moeda == "CARA":
                self.status = "Saudável"
                logs.append(f"🪙 Deu CARA! {self.nome} se curou da Queimadura!")
            else:
                logs.append(f"🪙 Deu COROA! {self.nome} continua Queimado.")
        elif self.status == "Adormecido 💤":
            moeda = random.choice(["CARA", "COROA"])
            if moeda == "CARA":
                self.status = "Saudável"
                logs.append(f"🪙 Deu CARA! {self.nome} acordou!")
            else:
                logs.append(f"🪙 Deu COROA! {self.nome} continua dormindo.")
        return logs

    def evoluir_para(self, novo_nome, novo_hp, novo_tipo, nova_fraqueza, nova_resistencia, novo_recuo, nova_img, nova_hab=None):
        dano_sofrido = self.hp_max - self.hp_atual
        self.nome = novo_nome
        self.hp_base = int(novo_hp)
        bonus_ferramenta = TOOLS_DB[self.ferramenta]["hp_bonus"]
        self.hp_max = self.hp_base + bonus_ferramenta
        self.tipo = novo_tipo
        self.fraqueza = nova_fraqueza
        self.resistencia = nova_resistencia
        self.recuo = novo_recuo
        
        # Imagem
        if BASE_IMG_URL: self.imagem_url = f"{BASE_IMG_URL}/{novo_nome}.png"
        elif nova_img: self.imagem_url = nova_img
        
        self.habilidade = nova_hab if nova_hab else (POKEDEX[novo_nome].get("hab") if novo_nome in POKEDEX else None)
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
        if self.ferramenta == "Rescue Board (-1 Recuo)": custo = max(0, custo - 1)
        
        if total_energias >= custo:
            removidas = 0
            chaves = list(self.energias.keys())
            for tipo in chaves:
                while self.energias[tipo] > 0 and removidas < custo:
                    self.energias[tipo] -= 1
                    removidas += 1
                if self.energias[tipo] <= 0: del self.energias[tipo]
            self.status = "Saudável"
            return True, f"Pagou {custo} de energia e recuou."
        else:
            return False, f"Precisa de {custo} energias (tem {total_energias})."

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
    # Buffer para dano calculado (dicionário para guardar o valor do input de cada pokemon)
    if 'dmg_buffer' not in st.session_state: st.session_state.dmg_buffer = {}

def adicionar_log(mensagem, tipo="neutro"):
    hora = datetime.datetime.now().strftime("%H:%M")
    colors = {"ataque": "#f87171", "energia": "#c084fc", "cura": "#4ade80", "ko": "#fb923c", "tool": "#60a5fa", "neutro": "#94a3b8"}
    c = colors.get(tipo, "white")
    st.session_state.log.insert(0, f"<div class='log-entry' style='color:{c}'>[{hora}] {mensagem}</div>")

inicializar_jogo()

# --- 4. TOP BAR ---
col_logo, col_buttons = st.columns([2, 3])

with col_logo:
    st.markdown("### ⚔️ PokéBattle — Registro TCG")
    # Edição de nomes compacta
    with st.expander("👤 Jogadores (Editar)", expanded=False):
        c1, c2 = st.columns(2)
        n1 = c1.text_input("Treinador 1", value=st.session_state.Treinadores["Treinador 1"]["nome"])
        n2 = c2.text_input("Treinador 2", value=st.session_state.Treinadores["Treinador 2"]["nome"])
        if c1.button("Salvar Nomes"):
            st.session_state.Treinadores["Treinador 1"]["nome"] = n1
            st.session_state.Treinadores["Treinador 2"]["nome"] = n2
            st.rerun()
    # Indicador de Turno
    nome_vez = st.session_state.Treinadores[st.session_state.turno_atual]['nome']
    st.markdown(f"**Vez de:** <span style='color:#FFC107'>{nome_vez}</span>", unsafe_allow_html=True)

with col_buttons:
    c_rank, c_log, c_clear, c_turn, c_new, c_save = st.columns(6)
    with c_rank:
        st.markdown('<div class="btn-blue">', unsafe_allow_html=True)
        if st.button("🏆 Placar", use_container_width=True):
            st.toast(f"P1: {st.session_state.Treinadores['Treinador 1']['premios']} | P2: {st.session_state.Treinadores['Treinador 2']['premios']}")
        st.markdown('</div>', unsafe_allow_html=True)
    with c_log:
        st.markdown('<div class="btn-blue">', unsafe_allow_html=True)
        if st.session_state.log:
            txt = "\n".join([re.sub('<[^<]+?>', '', l) for l in st.session_state.log[::-1]])
            st.download_button("⬇️ Log", txt, "log.txt", use_container_width=True)
        else: st.button("⬇️ Log", disabled=True, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c_clear:
        st.markdown('<div class="btn-red">', unsafe_allow_html=True)
        if st.button("🧹 Limpar", use_container_width=True):
            st.session_state.log = []
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c_turn:
        st.markdown('<div class="btn-green">', unsafe_allow_html=True)
        if st.button("➡ Turno", help="Passar Vez", use_container_width=True):
            # Checkup
            for p in ["Treinador 1", "Treinador 2"]:
                if st.session_state.Treinadores[p]['ativo']:
                    res = st.session_state.Treinadores[p]['ativo'].resolver_checkup()
                    if res: 
                        for r in res: adicionar_log(r, "ko")
            st.session_state.habilidades_usadas = []
            antigo = st.session_state.turno_atual
            novo = "Treinador 2" if antigo == "Treinador 1" else "Treinador 1"
            st.session_state.turno_atual = novo
            adicionar_log(f"🕒 Fim de turno. Vez de {st.session_state.Treinadores[novo]['nome']}.", "neutro")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c_new:
        st.markdown('<div class="btn-blue">', unsafe_allow_html=True)
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.clear()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c_save:
        st.markdown('<div class="btn-yellow">', unsafe_allow_html=True)
        st.button("💾 Salvar", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- 5. BARRA DE CRIAÇÃO (FUNDO AZUL ESCURO) ---
st.markdown("---")
st.markdown("##### 📦 Adicionar Pokémon")
with st.container():
    c1, c2, c3, c4, c5 = st.columns([1.5, 1.5, 2, 1.5, 1])
    with c1:
        dono = st.selectbox("Jogador", ["Treinador 1", "Treinador 2"], format_func=lambda x: st.session_state.Treinadores[x]['nome'], label_visibility="collapsed")
    with c2:
        deck_filter = st.selectbox("Filtro Tipo", ["Todos"] + sorted(list(set([v['tipo'] for k,v in POKEDEX.items()]))), label_visibility="collapsed")
    with c3:
        lista = list(POKEDEX.keys())
        if deck_filter != "Todos": lista = [k for k,v in POKEDEX.items() if v['tipo'] == deck_filter]
        escolha = st.selectbox("Pokémon", lista, label_visibility="collapsed")
    with c4:
        dest = st.selectbox("Destino", ["Banco", "Ativo"], label_visibility="collapsed")
    with c5:
        st.markdown('<div class="btn-yellow">', unsafe_allow_html=True)
        if st.button("+ Adicionar", use_container_width=True):
            d = POKEDEX[escolha]
            n = Pokemon(escolha, d["hp"], d["tipo"], d["fraq"], d["res"], d.get("recuo",1), d["img"], d.get("hab"))
            p = st.session_state.Treinadores[dono]
            if dest == "Ativo" and p['ativo'] is None:
                p['ativo'] = n
                adicionar_log(f"🆕 {escolha} entrou como Ativo.", "neutro")
            elif len(p['banco']) < 5:
                p['banco'].append(n)
                adicionar_log(f"🆕 {escolha} foi pro Banco.", "neutro")
            else: st.error("Cheio!")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- 6. RENDERIZAÇÃO DA CARTA ATIVA (ESTILO IMAGEM) ---
def render_active_card(player_key, opponent_key):
    player = st.session_state.Treinadores[player_key]
    opponent = st.session_state.Treinadores[opponent_key]
    
    # Header Player
    c_h1, c_h2 = st.columns([3, 1])
    c_h1.markdown(f"#### {player['nome']}")
    c_h2.markdown(f"**🏆 {player['premios']}**")
    
    ativo = player['ativo']
    
    # Caixa Principal (Card Container)
    with st.container(): # Borda já aplicada pelo CSS global
        if not ativo:
            st.info("Sem Pokémon Ativo")
            return

        c_img, c_data = st.columns([1, 1.5])
        
        # --- COLUNA DA ESQUERDA: IMAGEM ---
        with c_img:
            st.image(ativo.imagem_url, use_container_width=True)
            
            # Badges Abaixo da Imagem
            is_ex = "ex" in ativo.nome.lower() or "v" in ativo.nome.lower()
            badges_html = ""
            if is_ex: badges_html += "<span class='badge badge-ex'>★ EX/V</span>"
            badges_html += f"<span class='badge badge-status'>{ativo.status}</span>"
            badges_html += f"<span class='badge badge-type'>{ativo.tipo}</span>"
            st.markdown(badges_html, unsafe_allow_html=True)
            
            # Recuo e Weakness
            st.caption(f"Fraq: {ativo.fraqueza} | Res: {ativo.resistencia}")
            
            # Ação de Recuo
            custo = ativo.recuo
            if ativo.ferramenta == "Rescue Board (-1 Recuo)": custo = max(0, custo - 1)
            if st.button(f"🏃 Recuar (Custo {custo})", key=f"run_{ativo.id_unico}", use_container_width=True):
                pode, msg = ativo.tentar_recuar()
                if pode:
                    if player['banco']:
                        player['banco'].append(ativo)
                        player['ativo'] = None
                        adicionar_log(f"🏃 {ativo.nome} recuou.", "neutro")
                        st.rerun()
                    else: st.warning("Banco vazio!")
                else: st.error(msg)

        # --- COLUNA DA DIREITA: DADOS E AÇÕES ---
        with c_data:
            # Nome e HP
            st.markdown(f"**{ativo.nome}**")
            st.progress(ativo.hp_atual / ativo.hp_max)
            st.caption(f"HP: {ativo.hp_atual} / {ativo.hp_max}")
            
            if ativo.hp_atual == 0:
                st.error("💀 NOCAUTEADO")
                st.markdown('<div class="btn-red">', unsafe_allow_html=True)
                if st.button("Enviar p/ Descarte", key=f"ko_{ativo.id_unico}", use_container_width=True):
                    player['descarte'].append(ativo)
                    player['ativo'] = None
                    adicionar_log(f"💀 {ativo.nome} nocauteado!", "ko")
                    qtd = 2 if ("ex" in ativo.nome.lower() or "v" in ativo.nome.lower()) else 1
                    opponent['premios'] -= qtd
                    adicionar_log(f"🏆 Oponente pegou {qtd} prêmios!", "ko")
                    if checar_vitoria(player_key): st.session_state.vencedor = opponent['nome'] # Se eu morri, checo se ele ganhou
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            
            else:
                # --- CALCULADORA DE DANO (Nova Feature) ---
                st.markdown("**Dano do Ataque**")
                
                # Inicializa buffer de dano
                if ativo.id_unico not in st.session_state.dmg_buffer:
                    st.session_state.dmg_buffer[ativo.id_unico] = 0
                
                # Botões de Atalho
                cb1, cb2, cb3, cb4, cb5 = st.columns(5)
                with cb1: 
                    st.markdown('<div class="btn-red btn-small">', unsafe_allow_html=True)
                    if st.button("Zerar", key=f"z_{ativo.id_unico}"): st.session_state.dmg_buffer[ativo.id_unico] = 0; st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                with cb2: 
                    st.markdown('<div class="btn-small">', unsafe_allow_html=True)
                    if st.button("+10", key=f"p10_{ativo.id_unico}"): st.session_state.dmg_buffer[ativo.id_unico] += 10; st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                with cb3: 
                    st.markdown('<div class="btn-small">', unsafe_allow_html=True)
                    if st.button("+20", key=f"p20_{ativo.id_unico}"): st.session_state.dmg_buffer[ativo.id_unico] += 20; st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                with cb4: 
                    st.markdown('<div class="btn-small">', unsafe_allow_html=True)
                    if st.button("+50", key=f"p50_{ativo.id_unico}"): st.session_state.dmg_buffer[ativo.id_unico] += 50; st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                with cb5: 
                    st.markdown('<div class="btn-small">', unsafe_allow_html=True)
                    if st.button("+100", key=f"p100_{ativo.id_unico}"): st.session_state.dmg_buffer[ativo.id_unico] += 100; st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

                # Input numérico ligado ao buffer
                dano_input = st.number_input("Valor", value=st.session_state.dmg_buffer[ativo.id_unico], step=10, key=f"inp_{ativo.id_unico}", label_visibility="collapsed")
                st.session_state.dmg_buffer[ativo.id_unico] = dano_input # Sincroniza manual

                # Botão ATACAR
                st.markdown('<div class="btn-yellow">', unsafe_allow_html=True)
                if st.button("⚔️ Atacar", key=f"atk_{ativo.id_unico}", use_container_width=True):
                    op_ativo = opponent['ativo']
                    if op_ativo:
                        mult = 2 if ativo.tipo == op_ativo.fraqueza else 1
                        red = 30 if ativo.tipo == op_ativo.resistencia else 0
                        final = (dano_input * mult) - red
                        if final < 0: final = 0
                        op_ativo.receber_dano(final)
                        adicionar_log(f"⚔️ {ativo.nome} causou {final} de dano!", "ataque")
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown("---")
                # Habilidade e Energias
                if ativo.habilidade:
                    ja_usou = ativo.id_unico in st.session_state.habilidades_usadas
                    label = "✅ Usado" if ja_usou else f"✨ {ativo.habilidade}"
                    disabled = ja_usou
                    st.markdown('<div class="btn-blue">', unsafe_allow_html=True)
                    if st.button(label, key=f"hab_{ativo.id_unico}", disabled=disabled, use_container_width=True):
                        st.session_state.habilidades_usadas.append(ativo.id_unico)
                        adicionar_log(f"✨ {ativo.nome} usou {ativo.habilidade}!", "tool")
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with st.expander("⚡ Energia / Status"):
                    c_e1, c_e2 = st.columns(2)
                    with c_e1:
                        e = st.selectbox("Tipo", ["Fogo 🔥", "Água 💧", "Planta 🌱", "Elétrico ⚡", "Psíquico 🌀"], key=f"te_{ativo.id_unico}")
                        if st.button("Add E", key=f"ade_{ativo.id_unico}"): 
                            ativo.anexar_energia(e); st.rerun()
                    with c_e2:
                        st.selectbox("Status", ["Saudável", "Envenenado 🧪", "Queimado 🔥", "Adormecido 💤", "Paralisado ⚡"], key=f"st_{ativo.id_unico}", on_change=lambda: setattr(ativo, 'status', st.session_state[f"st_{ativo.id_unico}"]))
                    
                    st.write("Energias atuais: " + " ".join([f"{k}x{v}" for k,v in ativo.energias.items()]))

    # Banco
    if player['banco']:
        st.caption(f"Banco ({len(player['banco'])})")
        cols = st.columns(5)
        for i, p in enumerate(player['banco']):
            with cols[i]:
                st.image(p.imagem_url)
                if p.hp_atual == 0:
                    st.error("💀")
                    if st.button("KO", key=f"kob_{p.id_unico}"):
                        player['banco'].pop(i); player['descarte'].append(p)
                        adicionar_log(f"💀 {p.nome} (Banco) morreu.", "ko")
                        # Lógica prêmio
                        qtd = 2 if "ex" in p.nome.lower() else 1
                        opponent['premios'] -= qtd
                        if checar_vitoria(id_jogador_chave): st.session_state.vencedor = opponent['nome']
                        st.rerun()
                else:
                    if st.button("⬆️", key=f"up_{p.id_unico}"):
                        if not player['ativo']: 
                            player['ativo'] = player['banco'].pop(i); st.rerun()
                    if st.button("💔", key=f"dmg_b_{p.id_unico}"):
                        p.receber_dano(10); st.rerun()
                    if p.habilidade:
                        ja_usou = p.id_unico in st.session_state.habilidades_usadas
                        if st.button("✨", key=f"hbb_{p.id_unico}", disabled=ja_usou, help=p.habilidade):
                            st.session_state.habilidades_usadas.append(p.id_unico)
                            adicionar_log(f"✨ {p.nome} (Banco) usou hab.", "tool")
                            st.rerun()

# --- 7. TELA PRINCIPAL ---
if st.session_state.vencedor:
    st.balloons()
    st.title(f"🏆 {st.session_state.vencedor} VENCEU! 🏆")
    if st.button("Reiniciar"):
        st.session_state.clear(); st.rerun()
else:
    c1, c2 = st.columns(2)
    with c1: render_active_card("Treinador 1", "Treinador 2")
    with c2: render_active_card("Treinador 2", "Treinador 1")
