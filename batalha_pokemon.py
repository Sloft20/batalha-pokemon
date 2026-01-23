import streamlit as st
import datetime
import random 
import re 

st.set_page_config(page_title="PokéBattle 8.0 (Dark UI)", page_icon="⚔️", layout="wide")

# --- 0. CONFIGURAÇÃO VISUAL (TEMA DARK + TOP BAR) ---
def configurar_visual():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
        html, body, [class*="css"] { font-family: 'Roboto', sans-serif; }

        /* Fundo Geral (Dark Blue/Navy) */
        [data-testid="stAppViewContainer"] {
            background-color: #0E1117;
            background-image: radial-gradient(circle at 50% 50%, #1c2331 0%, #0E1117 100%);
            color: #ffffff;
        }
        
        [data-testid="stHeader"] { background-color: rgba(0,0,0,0); }

        /* Estilo dos Containers (Vidro Escuro) */
        div[data-testid="stVerticalBlockBorderWrapper"], div[data-testid="stExpander"] {
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 10px;
        }

        h1, h2, h3, p, span, div, label {
            color: #E6EDF3 !important;
        }

        /* Inputs Escuros */
        .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
            background-color: #0d1117 !important;
            color: #c9d1d9 !important;
            border: 1px solid #30363d !important;
            border-radius: 6px;
        }

        /* --- ESTILIZAÇÃO DOS BOTÕES (BASEADO NA IMAGEM) --- */
        
        /* Botão Padrão (Dark) */
        .stButton > button {
            background-color: #21262d !important;
            color: #c9d1d9 !important;
            border: 1px solid #30363d !important;
            border-radius: 6px;
            font-weight: 600;
            transition: all 0.2s;
        }
        .stButton > button:hover {
            background-color: #30363d !important;
            border-color: #8b949e !important;
        }

        /* Botão AMARELO (Ação Principal/Fim de Turno/Adicionar) */
        .primary-btn > button {
            background-color: #FFCB05 !important;
            color: #21262d !important;
            border: none !important;
        }
        .primary-btn > button:hover {
            background-color: #e6b800 !important;
        }

        /* Botão VERMELHO (Reset/Dano) */
        .danger-btn > button {
            background-color: #da3633 !important;
            color: white !important;
            border: none !important;
        }

        /* Botão AZUL (Habilidade) */
        .hab-btn > button {
            background-color: #238636 !important; /* Verde/Azul Github style */
            color: white !important;
        }

        /* Container de Criação (Faixa Azul) */
        .creation-container {
            background-color: #1f2937;
            padding: 15px;
            border-radius: 10px;
            border-left: 5px solid #FFCB05;
            margin-bottom: 20px;
        }

        .log-entry {
            padding: 4px;
            border-bottom: 1px solid #30363d;
            font-size: 13px;
            font-family: monospace;
        }
    </style>
    """, unsafe_allow_html=True)

configurar_visual()

# --- 1. BANCO DE DADOS (COM CUSTO DE RECUO) ---
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

# --- 2. CLASSE POKEMON ---
class Pokemon:
    def __init__(self, nome, hp_max, tipo, fraqueza, resistencia, recuo, imagem_url="", habilidade=None):
        self.nome = nome
        self.hp_base = int(hp_max)
        self.hp_max = int(hp_max)
        self.hp_atual = int(hp_max)
        link_padrao = "https://upload.wikimedia.org/wikipedia/en/3/3b/Pokemon_Trading_Card_Game_cardback.jpg"
        self.imagem_url = imagem_url if imagem_url else link_padrao
        self.id_unico = datetime.datetime.now().timestamp() + random.random()
        self.tipo = tipo
        self.fraqueza = fraqueza
        self.resistencia = resistencia
        self.recuo = recuo # Custo de Recuo
        self.status = "Saudável"
        self.energias = {} # Ex: {"Fogo": 2}
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
        if nova_img: self.imagem_url = nova_img
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
    
    # --- NOVO: LÓGICA DE RECUO ---
    def tentar_recuar(self):
        total_energias = sum(self.energias.values())
        custo = self.recuo
        
        # Rescue Board reduz recuo em 1
        if self.ferramenta == "Rescue Board (-1 Recuo)":
            custo -= 1
            if custo < 0: custo = 0
            
        if total_energias >= custo:
            # Remove energias (Simples: remove as primeiras que achar)
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

# --- 3. GERENCIAMENTO DE ESTADO ---
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

def adicionar_log(mensagem, tipo="neutro"):
    hora = datetime.datetime.now().strftime("%H:%M")
    colors = {"ataque": "#ff7b72", "energia": "#d2a8ff", "cura": "#7ee787", "ko": "#ffa657", "tool": "#79c0ff", "neutro": "#c9d1d9"}
    c = colors.get(tipo, "white")
    st.session_state.log.insert(0, f"<div class='log-entry' style='color:{c}'>[{hora}] {mensagem}</div>")

inicializar_jogo()

# --- 4. TOP BAR (LAYOUT BASEADO NA IMAGEM) ---
col_title, col_actions = st.columns([1.5, 2.5])

with col_title:
    st.markdown("## ⚔️ PokéBattle — Registro TCG")
    
    # Nomes dos Jogadores (Lado Esquerdo, abaixo do título)
    with st.expander("👤 Jogadores (Editar)", expanded=False):
        c1, c2 = st.columns(2)
        n1 = c1.text_input("Treinador 1", value=st.session_state.Treinadores["Treinador 1"]["nome"])
        n2 = c2.text_input("Treinador 2", value=st.session_state.Treinadores["Treinador 2"]["nome"])
        if c1.button("Salvar Nomes"):
            st.session_state.Treinadores["Treinador 1"]["nome"] = n1
            st.session_state.Treinadores["Treinador 2"]["nome"] = n2
            st.rerun()
            
    # Indicador de Turno
    t_atual = st.session_state.Treinadores[st.session_state.turno_atual]['nome']
    st.markdown(f"**Vez de:** <span style='color:#FFCB05'>{t_atual}</span>", unsafe_allow_html=True)

with col_actions:
    # Botões Superiores (Direita)
    c_rank, c_log, c_clear, c_turn, c_new, c_save = st.columns(6)
    
    with c_rank:
        if st.button("🏆 Placar"):
            st.toast(f"P1: {st.session_state.Treinadores['Treinador 1']['premios']} | P2: {st.session_state.Treinadores['Treinador 2']['premios']}")
    with c_log:
        if st.session_state.log:
            txt = "\n".join([re.sub('<[^<]+?>', '', l) for l in st.session_state.log[::-1]])
            st.download_button("⬇️ Log", txt, "log.txt")
    with c_clear:
        if st.button("🧹 Limpar"):
            st.session_state.log = []
            st.rerun()
    with c_turn:
        st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
        if st.button("➡ Fim Turno", help="Passa a vez + Checkup"):
            # Checkup Auto
            for p in ["Treinador 1", "Treinador 2"]:
                if st.session_state.Treinadores[p]['ativo']:
                    res = st.session_state.Treinadores[p]['ativo'].resolver_checkup()
                    if res: 
                        for r in res: adicionar_log(r, "ko")
            
            # Passa
            st.session_state.habilidades_usadas = []
            antigo = st.session_state.turno_atual
            novo = "Treinador 2" if antigo == "Treinador 1" else "Treinador 1"
            st.session_state.turno_atual = novo
            adicionar_log(f"🕒 Fim de turno de {st.session_state.Treinadores[antigo]['nome']}.", "neutro")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c_new:
        st.markdown('<div class="danger-btn">', unsafe_allow_html=True)
        if st.button("🔄 Reset"):
            st.session_state.clear()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c_save:
        if st.button("💾 Salvar"):
            st.balloons() # Apenas visual por enquanto

# --- 5. ÁREA DE CRIAÇÃO (FAIXA AZUL/ESCURA) ---
st.markdown('<div class="creation-container">', unsafe_allow_html=True)
st.markdown("#### 📦 Adicionar Pokémon (Rápido)")
c_cri_1, c_cri_2, c_cri_3, c_cri_4, c_cri_5 = st.columns([1.5, 2, 2, 1.5, 1])

with c_cri_1:
    dono = st.selectbox("Jogador", ["Treinador 1", "Treinador 2"], format_func=lambda x: st.session_state.Treinadores[x]['nome'], label_visibility="collapsed")
with c_cri_2:
    # Filtro de Deck (Simulado com selectbox de tipos ou nomes)
    deck_filter = st.selectbox("Deck/Tipo", ["Todos"] + sorted(list(set([v['tipo'] for k,v in POKEDEX.items()]))), label_visibility="collapsed")
with c_cri_3:
    # Filtra pokedex
    lista_pokes = list(POKEDEX.keys())
    if deck_filter != "Todos":
        lista_pokes = [k for k,v in POKEDEX.items() if v['tipo'] == deck_filter]
    escolha = st.selectbox("Pokémon", lista_pokes, label_visibility="collapsed")
with c_cri_4:
    dest = st.selectbox("Destino", ["Banco", "Ativo"], label_visibility="collapsed")
with c_cri_5:
    st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
    if st.button("+ Add", use_container_width=True):
        dados = POKEDEX[escolha]
        # Criação
        novo = Pokemon(escolha, dados["hp"], dados["tipo"], dados["fraq"], dados["res"], dados.get("recuo", 1), dados["img"], dados.get("hab"))
        player = st.session_state.Treinadores[dono]
        
        if dest == "Ativo" and player['ativo'] is None:
            player['ativo'] = novo
            adicionar_log(f"🆕 {escolha} entrou como Ativo de {player['nome']}.", "neutro")
        elif len(player['banco']) < 5:
            player['banco'].append(novo)
            adicionar_log(f"🆕 {escolha} entrou no Banco de {player['nome']}.", "neutro")
        else:
            st.error("Sem espaço!")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- 6. RENDERIZAÇÃO DA MESA ---
def checar_vitoria(id_oponente_chave):
    if st.session_state.Treinadores[id_oponente_chave]['premios'] <= 0: return True
    oponente = st.session_state.Treinadores[id_oponente_chave]
    if oponente['ativo'] is None and len(oponente['banco']) == 0: return True
    return False

def renderizar_mesa_jogador(id_jogador_chave):
    player = st.session_state.Treinadores[id_jogador_chave]
    
    # Visual da vez
    eh_vez = (st.session_state.turno_atual == id_jogador_chave)
    borda = "2px solid #FFCB05" if eh_vez else "1px solid #30363d"
    
    st.markdown(f"<div style='border:{borda}; background-color:#0d1117; padding:10px; border-radius:10px; margin-bottom:10px;'>", unsafe_allow_html=True)
    
    # Header do Jogador (Nome + Prêmios)
    c_head_1, c_head_2 = st.columns([3, 1])
    c_head_1.markdown(f"<h3 style='margin:0;'>{player['nome']}</h3>", unsafe_allow_html=True)
    c_head_2.markdown(f"<h4 style='margin:0; text-align:right;'>{player['premios']} 🎴</h4>", unsafe_allow_html=True)
    
    ativo = player['ativo']
    if ativo:
        st.markdown("---")
        with st.container():
            col_img, col_infos = st.columns([1, 2])
            with col_img:
                st.image(ativo.imagem_url, use_container_width=True)
                # Display de Energia e Status
                status_icon = "✅" if ativo.status == "Saudável" else ativo.status[-1]
                st.caption(f"{status_icon} {ativo.status}")
                
                txt_en = " ".join([f"{k.split()[-1]}x{v}" for k,v in ativo.energias.items()])
                if txt_en: st.markdown(f"**⚡ {txt_en}**")
                
                # Botão Habilidade
                if ativo.habilidade:
                    ja_usou = ativo.id_unico in st.session_state.habilidades_usadas
                    cls = "stButton" if ja_usou else "hab-btn"
                    lbl = "✅ Usado" if ja_usou else f"✨ {ativo.habilidade}"
                    st.markdown(f'<div class="{cls}">', unsafe_allow_html=True)
                    if st.button(lbl, key=f"hat_{ativo.id_unico}", disabled=ja_usou):
                        st.session_state.habilidades_usadas.append(ativo.id_unico)
                        adicionar_log(f"✨ {ativo.nome} usou {ativo.habilidade}!", "tool")
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

            with col_infos:
                # Info Principal
                st.markdown(f"**{ativo.nome}** <span style='float:right'>HP: {ativo.hp_atual}/{ativo.hp_max}</span>", unsafe_allow_html=True)
                st.progress(ativo.hp_atual / ativo.hp_max)
                
                if ativo.hp_atual == 0:
                    st.error("💀 NOCAUTEADO")
                    if st.button("Enviar p/ Descarte", key=f"ko_at_{ativo.id_unico}"):
                        player['descarte'].append(ativo)
                        player['ativo'] = None
                        adicionar_log(f"💀 {ativo.nome} caiu!", "ko")
                        # Prêmios
                        op_key = "Treinador 2" if id_jogador_chave == "Treinador 1" else "Treinador 1"
                        qtd = 2 if "ex" in ativo.nome.lower() else 1
                        st.session_state.Treinadores[op_key]['premios'] -= qtd
                        adicionar_log(f"🏆 Oponente pegou {qtd} prêmios!", "ko")
                        if checar_vitoria(id_jogador_chave): st.session_state.vencedor = st.session_state.Treinadores[op_key]['nome']
                        st.rerun()
                else:
                    # Controles de Batalha
                    c_act_1, c_act_2, c_act_3 = st.columns(3)
                    with c_act_1:
                        dmg = st.number_input("Dano", step=10, key=f"dmg_{ativo.id_unico}", label_visibility="collapsed")
                    with c_act_2:
                        st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
                        if st.button("⚔️ Atacar", key=f"atk_{ativo.id_unico}"):
                            op_key = "Treinador 2" if id_jogador_chave == "Treinador 1" else "Treinador 1"
                            op_ativo = st.session_state.Treinadores[op_key]['ativo']
                            if op_ativo:
                                mult = 2 if ativo.tipo == op_ativo.fraqueza else 1
                                red = 30 if ativo.tipo == op_ativo.resistencia else 0
                                final = (dmg * mult) - red
                                if final < 0: final = 0
                                op_ativo.receber_dano(final)
                                adicionar_log(f"⚔️ {ativo.nome} causou {final}!", "ataque")
                                st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)
                    with c_act_3:
                        # --- LÓGICA DE RECUO COM CUSTO ---
                        custo = ativo.recuo
                        if ativo.ferramenta == "Rescue Board (-1 Recuo)": custo = max(0, custo - 1)
                        
                        if st.button(f"🏃 Recuar ({custo})", key=f"run_{ativo.id_unico}"):
                            pode, msg = ativo.tentar_recuar()
                            if pode:
                                if player['banco']:
                                    player['banco'].append(ativo)
                                    player['ativo'] = None
                                    adicionar_log(f"🏃 {ativo.nome} recuou (Pagou {custo}).", "neutro")
                                    st.rerun()
                                else:
                                    st.warning("Banco vazio!")
                            else:
                                st.error(msg)

                    # Tools e Energia
                    with st.popover("⚡ Energia / Status / Tool"):
                        st.selectbox("Status", ["Saudável", "Envenenado 🧪", "Queimado 🔥", "Adormecido 💤", "Paralisado ⚡"], key=f"st_{ativo.id_unico}", on_change=lambda: setattr(ativo, 'status', st.session_state[f"st_{ativo.id_unico}"]))
                        e = st.selectbox("Add Energia", ["Fogo 🔥", "Água 💧", "Planta 🌱", "Elétrico ⚡", "Psíquico 🌀", "Luta 🥊", "Escuridão 🌙", "Metal ⚙️"], key=f"ae_{ativo.id_unico}")
                        if st.button("Adicionar", key=f"bae_{ativo.id_unico}"): 
                            ativo.anexar_energia(e)
                            st.rerun()
                        tl = st.selectbox("Tool", list(TOOLS_DB.keys()), key=f"tl_{ativo.id_unico}")
                        if st.button("Equipar", key=f"btl_{ativo.id_unico}"):
                            ativo.equipar_ferramenta(tl)
                            st.rerun()

    # Banco
    if player['banco']:
        st.markdown("---")
        st.caption(f"Banco ({len(player['banco'])})")
        cols = st.columns(5)
        for i, p in enumerate(player['banco']):
            with cols[i]:
                st.image(p.imagem_url)
                if p.hp_atual == 0:
                    if st.button("💀 KO", key=f"kob_{p.id_unico}"):
                        player['banco'].pop(i)
                        player['descarte'].append(p)
                        adicionar_log(f"💀 {p.nome} (Banco) morreu.", "ko")
                        # Prêmios
                        op_key = "Treinador 2" if id_jogador_chave == "Treinador 1" else "Treinador 1"
                        qtd = 2 if "ex" in p.nome.lower() else 1
                        st.session_state.Treinadores[op_key]['premios'] -= qtd
                        adicionar_log(f"🏆 {qtd} Prêmios pegos.", "ko")
                        if checar_vitoria(id_jogador_chave): st.session_state.vencedor = st.session_state.Treinadores[op_key]['nome']
                        st.rerun()
                else:
                    if st.button("⬆️", key=f"up_{p.id_unico}"):
                        if not player['ativo']:
                            player['ativo'] = player['banco'].pop(i)
                            adicionar_log(f"🆙 {p.nome} subiu!", "neutro")
                            st.rerun()
                    if st.button("💔", key=f"dmb_{p.id_unico}"):
                        p.receber_dano(10)
                        st.rerun()
                    if p.habilidade:
                        ja_usou = p.id_unico in st.session_state.habilidades_usadas
                        cls = "stButton" if ja_usou else "hab-btn"
                        st.markdown(f'<div class="{cls}">', unsafe_allow_html=True)
                        if st.button("✨", key=f"hb_{p.id_unico}", help=p.habilidade, disabled=ja_usou):
                            st.session_state.habilidades_usadas.append(p.id_unico)
                            adicionar_log(f"✨ {p.nome} (Banco) usou hab.", "tool")
                            st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# --- 7. TELA PRINCIPAL ---
if st.session_state.vencedor:
    st.balloons()
    st.markdown(f"<h1 style='text-align: center; color: #FFCB05 !important;'>🏆 {st.session_state.vencedor} VENCEU! 🏆</h1>", unsafe_allow_html=True)
    if st.button("Nova Partida", type="primary"):
        st.session_state.clear()
        st.rerun()
else:
    c1, c2 = st.columns(2)
    with c1: renderizar_mesa_jogador("Treinador 1")
    with c2: renderizar_mesa_jogador("Treinador 2")
    
    # Log no rodapé (opcional, já que tem botão de download)
    with st.expander("📜 Histórico Recente"):
        log_html = "".join(st.session_state.log[:10]) # Mostra só os ultimos 10
        st.markdown(f"{log_html}", unsafe_allow_html=True)
