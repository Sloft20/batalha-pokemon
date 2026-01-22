import streamlit as st
import datetime
import random 
import re 

st.set_page_config(page_title="PokéBattle 7.0 (Top Bar)", page_icon="🏟️", layout="wide")

# --- 0. CONFIGURAÇÃO VISUAL (VISUAL 5.10 LIMPO + NOVOS AJUSTES) ---
def configurar_visual():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
        html, body, [class*="css"] { font-family: 'Roboto', sans-serif; }

        /* Fundo da Arena */
        [data-testid="stAppViewContainer"] {
            background-image: url("https://pokemonrevolution.net/forum/uploads/monthly_2021_03/DVMT-6OXcAE2rZY.jpg.afab972f972bd7fbd4253bc7aa1cf27f.jpg");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
        
        [data-testid="stHeader"] { background-color: rgba(0,0,0,0); }

        /* Caixas de Vidro */
        div[data-testid="stVerticalBlockBorderWrapper"], div[data-testid="stExpander"] {
            background-color: rgba(0, 0, 0, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 15px;
            backdrop-filter: blur(5px);
        }

        h1, h2, h3, p, span, div, label {
            color: #FFFFFF !important;
            text-shadow: 1px 1px 3px #000000;
        }

        /* Inputs Limpos */
        .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
            background-color: rgba(255, 255, 255, 0.15) !important;
            color: white !important;
            border: 0px solid transparent !important;
            box-shadow: none !important;
        }

        /* --- BOTÕES GERAIS --- */
        .stButton > button {
            background-color: #FFCB05 !important;
            color: #2a3b96 !important;
            border-radius: 10px;
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
            font-weight: bold;
            width: 100%;
            transition: transform 0.1s;
        }
        .stButton > button:hover {
            transform: scale(1.02);
            background-color: #ffdb4d !important;
            color: black !important;
        }
        .stButton > button:active, .stButton > button:focus {
            background-color: #FFCB05 !important;
            color: #2a3b96 !important;
            box-shadow: none !important;
        }

        /* --- BOTÕES ESPECIAIS DO TOPO --- */
        
        /* Passar Turno (Verde) */
        .turn-btn > button {
            background-color: #4CAF50 !important;
            color: white !important;
            height: 60px; /* Mais alto */
            font-size: 18px !important;
        }
        .turn-btn > button:hover { background-color: #45a049 !important; }

        /* Checkup (Laranja) */
        .check-btn > button {
            background-color: #FF9800 !important;
            color: white !important;
            height: 60px;
            font-size: 18px !important;
        }
        .check-btn > button:hover { background-color: #e68900 !important; }

        /* Moeda (Cinza/Prata) */
        .coin-btn > button {
            background-color: #607D8B !important;
            color: white !important;
            height: 60px;
        }

        /* Habilidade (Azul) */
        .hab-btn > button { background-color: #3b4cca !important; color: white !important; }
        .hab-btn-used > button { background-color: #555 !important; color: #aaa !important; cursor: not-allowed; }

        .log-entry {
            padding: 3px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            font-size: 13px;
        }
    </style>
    """, unsafe_allow_html=True)

configurar_visual()

# --- 1. BANCO DE DADOS ---
POKEDEX = {
    # --- DECK DRAGAPULT EX ---
    "Dragapult ex": {"hp": 320, "tipo": "Dragão 🐉", "fraq": "Nenhuma", "res": "Nenhuma", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/TWM/TWM_130_R_EN_PNG.png"},
    "Drakloak": {"hp": 90, "tipo": "Dragão 🐉", "fraq": "Nenhuma", "res": "Nenhuma", "hab": "Reconnaissance (Olhar Topo)", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/TWM/TWM_129_R_EN_PNG.png"},
    "Dreepy": {"hp": 70, "tipo": "Dragão 🐉", "fraq": "Nenhuma", "res": "Nenhuma", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/TWM/TWM_128_R_EN_PNG.png"},
    "Xatu": {"hp": 100, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "hab": "Clairvoyant Sense (Ligar + Draw 2)", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/PAR/PAR_072_R_EN_PNG.png"},
    "Natu": {"hp": 60, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/PAR/PAR_071_R_EN_PNG.png"},
    "Fezandipiti ex": {"hp": 210, "tipo": "Psíquico 🌀", "fraq": "Metal ⚙️", "res": "Nenhuma", "hab": "Flip the Script (Draw 3)", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/SFA/SFA_038_R_EN_PNG.png"},

    # --- DECK CHARIZARD EX ---
    "Charizard ex": {"hp": 330, "tipo": "Escuridão 🌙", "fraq": "Planta 🌱", "res": "Nenhuma", "hab": "Infernal Reign (Buscar 3 Energias)", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/OBF/OBF_125_R_EN_PNG.png"},
    "Charmeleon": {"hp": 90, "tipo": "Fogo 🔥", "fraq": "Água 💧", "res": "Nenhuma", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/OBF/OBF_027_R_EN_PNG.png"},
    "Charmander": {"hp": 70, "tipo": "Fogo 🔥", "fraq": "Água 💧", "res": "Nenhuma", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/OBF/OBF_026_R_EN_PNG.png"},
    "Pidgeot ex": {"hp": 280, "tipo": "Normal ⚪", "fraq": "Elétrico ⚡", "res": "Luta 🥊", "hab": "Quick Search (Buscar Qualquer Carta)", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/OBF/OBF_164_R_EN_PNG.png"},
    "Pidgey": {"hp": 60, "tipo": "Normal ⚪", "fraq": "Elétrico ⚡", "res": "Luta 🥊", "hab": "Call for Family (Buscar Básico)", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/OBF/OBF_162_R_EN_PNG.png"},
    "Moltres": {"hp": 120, "tipo": "Fogo 🔥", "fraq": "Água 💧", "res": "Nenhuma", "hab": "Flare Symbol (+10 Dano Fogo)", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/BRS/BRS_021_R_EN_PNG.png"},

    # --- DECK GARDEVOIR EX ---
    "Gardevoir ex": {"hp": 310, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "hab": "Psychic Embrace (Ligar do Descarte)", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/SVI/SVI_086_R_EN_PNG.png"},
    "Kirlia": {"hp": 80, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "hab": "Refinement (Descarta 1, Draw 2)", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/SVI/SVI_085_R_EN_PNG.png"},
    "Ralts": {"hp": 60, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/SVI/SVI_084_R_EN_PNG.png"},
    "Drifloon": {"hp": 70, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/SVI/SVI_089_R_EN_PNG.png"},
    "Scream Tail": {"hp": 90, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/PAR/PAR_086_R_EN_PNG.png"},
    "Mew ex": {"hp": 180, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "hab": "Restart (Comprar até ter 3)", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/MEW/MEW_151_R_EN_PNG.png"},
    "Radiant Greninja": {"hp": 130, "tipo": "Água 💧", "fraq": "Elétrico ⚡", "res": "Nenhuma", "hab": "Concealed Cards (Descarta Energia, Draw 2)", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/ASR/ASR_046_R_EN_PNG.png"},
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
    def __init__(self, nome, hp_max, tipo, fraqueza, resistencia, imagem_url="", habilidade=None):
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

    def evoluir_para(self, novo_nome, novo_hp, novo_tipo, nova_fraqueza, nova_resistencia, nova_img, nova_hab=None):
        dano_sofrido = self.hp_max - self.hp_atual
        self.nome = novo_nome
        self.hp_base = int(novo_hp)
        bonus_ferramenta = TOOLS_DB[self.ferramenta]["hp_bonus"]
        self.hp_max = self.hp_base + bonus_ferramenta
        self.tipo = novo_tipo
        self.fraqueza = nova_fraqueza
        self.resistencia = nova_resistencia
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
    cor = "white"
    if tipo == "ataque": cor = "#ffcccb" 
    elif tipo == "energia": cor = "#fffacd" 
    elif tipo == "cura": cor = "#90ee90" 
    elif tipo == "ko": cor = "#ff4500" 
    elif tipo == "tool": cor = "#add8e6"
    st.session_state.log.insert(0, f"<div class='log-entry' style='color:{cor}'>[{hora}] {mensagem}</div>")

inicializar_jogo()

# --- 4. ÁREA SUPERIOR (DASHBOARD) ---
# Título pequeno
st.markdown("<h2 style='text-align:center;'>🏆 Arena PokéBattle</h2>", unsafe_allow_html=True)

# Container Principal do Topo
with st.container(border=True):
    col_p1, col_pass, col_check, col_coin, col_p2 = st.columns([2, 1.5, 1.5, 1, 2])
    
    # 1. Placar P1
    with col_p1:
        n1 = st.session_state.Treinadores["Treinador 1"]["nome"]
        p1 = st.session_state.Treinadores["Treinador 1"]["premios"]
        cor_t1 = "#4CAF50" if st.session_state.turno_atual == "Treinador 1" else "#89CFF0"
        st.markdown(f"<h3 style='color:{cor_t1} !important; text-align:center;'>{n1}</h3>", unsafe_allow_html=True)
        st.markdown(f"<h4 style='text-align:center;'>{p1} 🎴</h4>", unsafe_allow_html=True)

    # 2. Botão Passar Turno
    with col_pass:
        st.markdown('<div class="turn-btn">', unsafe_allow_html=True)
        if st.button("⏳ PASSAR", help="Passar a Vez"):
            st.session_state.habilidades_usadas = []
            antigo = st.session_state.turno_atual
            novo = "Treinador 2" if antigo == "Treinador 1" else "Treinador 1"
            st.session_state.turno_atual = novo
            nome_novo = st.session_state.Treinadores[novo]['nome']
            adicionar_log(f"🕒 <b>Fim do turno.</b> Vez de <b>{nome_novo}</b>!", "neutro")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # 3. Botão Checkup
    with col_check:
        st.markdown('<div class="check-btn">', unsafe_allow_html=True)
        if st.button("🔄 CHECKUP", help="Resolver Veneno/Queimadura"):
            logs_totais = []
            for nome_jog in ["Treinador 1", "Treinador 2"]:
                ativo = st.session_state.Treinadores[nome_jog]['ativo']
                if ativo:
                    res = ativo.resolver_checkup()
                    if res: logs_totais.extend(res)
            if logs_totais:
                for l in logs_totais: adicionar_log(l, "ko")
                st.success("Checkup OK!")
                st.rerun()
            else: st.toast("Nada p/ resolver.")
        st.markdown('</div>', unsafe_allow_html=True)

    # 4. Moeda
    with col_coin:
        st.markdown('<div class="coin-btn">', unsafe_allow_html=True)
        if st.button("🪙", help="Jogar Moeda"):
            res = random.choice(["CARA", "COROA"])
            adicionar_log(f"🪙 Moeda: {res}")
            st.toast(f"Moeda: {res}")
        st.markdown('</div>', unsafe_allow_html=True)

    # 5. Placar P2
    with col_p2:
        n2 = st.session_state.Treinadores["Treinador 2"]["nome"]
        p2 = st.session_state.Treinadores["Treinador 2"]["premios"]
        cor_t2 = "#4CAF50" if st.session_state.turno_atual == "Treinador 2" else "#FF6961"
        st.markdown(f"<h3 style='color:{cor_t2} !important; text-align:center;'>{n2}</h3>", unsafe_allow_html=True)
        st.markdown(f"<h4 style='text-align:center;'>{p2} 🎴</h4>", unsafe_allow_html=True)

# --- 5. MENU DE CONFIGURAÇÃO (EXPANDER NO TOPO) ---
with st.expander("⚙️ Menu de Jogo / Criar Cartas (Clique para abrir)", expanded=False):
    c_nome, c_save = st.columns(2)
    with c_nome:
        st.caption("Personalizar Nomes")
        n1_in = st.text_input("Nome J1", value=st.session_state.Treinadores["Treinador 1"]["nome"])
        n2_in = st.text_input("Nome J2", value=st.session_state.Treinadores["Treinador 2"]["nome"])
        if st.button("Atualizar Nomes"):
            st.session_state.Treinadores["Treinador 1"]["nome"] = n1_in
            st.session_state.Treinadores["Treinador 2"]["nome"] = n2_in
            st.rerun()
            
    with c_save:
        st.caption("Opções")
        if st.session_state.log:
            txt_log = f"LOG DE BATALHA - {datetime.datetime.now()}\n" + "\n".join([re.sub('<[^<]+?>', '', l) for l in st.session_state.log[::-1]])
            st.download_button("💾 Baixar Log (.txt)", txt_log, "log.txt")
        if st.button("🗑️ Reiniciar Jogo Completo"):
            st.session_state.clear()
            st.rerun()

    st.divider()
    st.markdown("### ➕ Criar / Evoluir Pokémon")
    c_ger_1, c_ger_2 = st.columns([1, 2])
    
    with c_ger_1:
        dono_key = st.selectbox("Treinador:", ["Treinador 1", "Treinador 2"], format_func=lambda x: st.session_state.Treinadores[x]['nome'])
        modo = st.radio("Modo:", ["📚 Pokedex", "✍️ Manual"], horizontal=True)
        acao = st.radio("Ação:", ["Novo Básico", "Evoluir"], horizontal=True)
        destino = "Banco"
        if acao == "Novo Básico": destino = st.radio("Onde?", ["Ativo", "Banco"], horizontal=True)
        
        # Opções Evolução
        player_temp = st.session_state.Treinadores[dono_key]
        opcoes_evolucao = []
        if player_temp['ativo']: opcoes_evolucao.append(f"[Ativo] {player_temp['ativo'].nome}")
        for i, p in enumerate(player_temp['banco']): opcoes_evolucao.append(f"[Banco {i+1}] {p.nome}")
        alvo_evolucao = st.selectbox("Quem evolui?", opcoes_evolucao) if acao == "Evoluir" and opcoes_evolucao else None

    with c_ger_2:
        nome_f, hp_f, tipo_f, fraq_f, res_f, img_f, hab_f = "", 0, "", "", "", "", None
        
        if "Pokedex" in modo:
            escolha = st.selectbox("Pokémon:", list(POKEDEX.keys()))
            dados = POKEDEX[escolha]
            nome_f, hp_f, tipo_f, fraq_f, res_f, img_f = escolha, dados["hp"], dados["tipo"], dados["fraq"], dados["res"], dados["img"]
            hab_f = dados.get("hab")
            st.image(img_f, width=80)
        else:
            c_m1, c_m2 = st.columns(2)
            with c_m1:
                nome_f = st.text_input("Nome")
                hp_f = st.number_input("HP", value=60, step=10)
                hab_f = st.text_input("Habilidade (Opcional)") or None
            with c_m2:
                img_f = st.text_input("URL Imagem")
                lista_t = ["Normal ⚪", "Fogo 🔥", "Água 💧", "Planta 🌱", "Elétrico ⚡", "Psíquico 🌀", "Luta 🥊", "Escuridão 🌙", "Metal ⚙️", "Dragão 🐉"]
                tipo_f = st.selectbox("Tipo", lista_t)
                fraq_f = st.selectbox("Fraqueza", lista_t)
                res_f = st.selectbox("Resistência", ["Nenhuma"] + lista_t)

        if st.button("✨ CONFIRMAR CRIAÇÃO / EVOLUÇÃO", type="primary"):
            if acao == "Novo Básico":
                if nome_f:
                    novo = Pokemon(nome_f, hp_f, tipo_f, fraq_f, res_f, img_f, hab_f)
                    if destino == "Ativo" and player_temp['ativo'] is None:
                        player_temp['ativo'] = novo
                        adicionar_log(f"🆕 {nome_f} entrou como Ativo.", "neutro")
                    elif len(player_temp['banco']) < 5:
                        player_temp['banco'].append(novo)
                        adicionar_log(f"🆕 {nome_f} entrou no Banco.", "neutro")
                    else: st.error("Banco cheio!")
                    st.rerun()
            elif acao == "Evoluir" and alvo_evolucao:
                obj = player_temp['ativo'] if "[Ativo]" in alvo_evolucao else player_temp['banco'][int(alvo_evolucao.split("]")[0].split(" ")[1])-1]
                obj.evoluir_para(nome_f, hp_f, tipo_f, fraq_f, res_f, img_f, hab_f)
                adicionar_log(f"🧬 Evoluiu para {nome_f}!", "energia")
                st.rerun()

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
    borda = "2px solid #4CAF50" if eh_vez else "1px solid rgba(255,255,255,0.2)"
    bg = "rgba(0,100,0,0.3)" if eh_vez else "rgba(0,0,0,0.5)"
    
    st.markdown(f"<div style='border:{borda}; background-color:{bg}; padding:10px; border-radius:10px; margin-bottom:10px;'>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='margin:0; text-align:center;'>{player['nome']}</h3>", unsafe_allow_html=True)
    
    ativo = player['ativo']
    if ativo:
        with st.container(border=True):
            col_img, col_infos = st.columns([1, 2])
            with col_img:
                st.image(ativo.imagem_url, use_container_width=True)
                if ativo.status != "Saudável": st.warning(ativo.status)
                txt_en = "".join([f"{k.split()[-1]}x{v} " for k,v in ativo.energias.items()])
                if txt_en: st.markdown(f"**⚡ {txt_en}**")
                if ativo.ferramenta != "Nenhuma": st.info(f"🛠️ {ativo.ferramenta}")
                
                if ativo.habilidade:
                    ja_usou = ativo.id_unico in st.session_state.habilidades_usadas
                    classe = "hab-btn-used" if ja_usou else "hab-btn"
                    lbl = "✅" if ja_usou else f"✨ {ativo.habilidade}"
                    st.markdown(f'<div class="{classe}">', unsafe_allow_html=True)
                    if st.button(lbl, key=f"h_at_{ativo.id_unico}", disabled=ja_usou):
                        st.session_state.habilidades_usadas.append(ativo.id_unico)
                        adicionar_log(f"✨ **{ativo.nome}** usou **{ativo.habilidade}**", "tool")
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

            with col_infos:
                st.write(f"**{ativo.nome}** | HP: {ativo.hp_atual}/{ativo.hp_max}")
                st.progress(ativo.hp_atual / ativo.hp_max)
                
                if ativo.hp_atual == 0:
                    st.error("NOCAUTEADO")
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
                    # Ações Ativo
                    st.selectbox("Status", ["Saudável", "Envenenado 🧪", "Queimado 🔥", "Adormecido 💤", "Paralisado ⚡"], key=f"st_{ativo.id_unico}", on_change=lambda: setattr(ativo, 'status', st.session_state[f"st_{ativo.id_unico}"]))
                    
                    with st.popover("⚡ Energia / 🛠️ Tool"):
                        t1, t2, t3 = st.tabs(["Add E", "Del E", "Tool"])
                        with t1:
                            e = st.selectbox("Tipo", ["Fogo 🔥", "Água 💧", "Planta 🌱", "Elétrico ⚡", "Psíquico 🌀", "Luta 🥊", "Escuridão 🌙", "Metal ⚙️"], key=f"ae_{ativo.id_unico}")
                            if st.button("Add", key=f"bae_{ativo.id_unico}"): 
                                ativo.anexar_energia(e)
                                st.rerun()
                        with t2: 
                            if ativo.energias:
                                r = st.selectbox("Remover", list(ativo.energias.keys()), key=f"re_{ativo.id_unico}")
                                if st.button("Del", key=f"bre_{ativo.id_unico}"): 
                                    ativo.remover_energia(r)
                                    st.rerun()
                        with t3:
                            tl = st.selectbox("Tool", list(TOOLS_DB.keys()), key=f"tl_{ativo.id_unico}")
                            if st.button("Equipar", key=f"btl_{ativo.id_unico}"):
                                ativo.equipar_ferramenta(tl)
                                st.rerun()
                    
                    c_dmg, c_act = st.columns(2)
                    with c_dmg:
                        dmg = st.number_input("Dano", step=10, key=f"dmg_{ativo.id_unico}")
                        if st.button("⚔️ ATACAR", key=f"atk_{ativo.id_unico}"):
                            op_key = "Treinador 2" if id_jogador_chave == "Treinador 1" else "Treinador 1"
                            op_ativo = st.session_state.Treinadores[op_key]['ativo']
                            if op_ativo:
                                mult = 2 if ativo.tipo == op_ativo.fraqueza else 1
                                red = 30 if ativo.tipo == op_ativo.resistencia else 0
                                final = (dmg * mult) - red
                                if final < 0: final = 0
                                op_ativo.receber_dano(final)
                                adicionar_log(f"⚔️ {ativo.nome} causou {final} de dano!", "ataque")
                                st.rerun()
                    with c_act:
                        if st.button("💔 -10", key=f"self_{ativo.id_unico}"): 
                            ativo.receber_dano(10)
                            st.rerun()
                        if st.button("🏃 Recuar", key=f"run_{ativo.id_unico}"):
                            ativo.status = "Saudável"
                            if player['banco']:
                                player['banco'].append(ativo)
                                player['ativo'] = None
                                adicionar_log(f"🏃 {ativo.nome} recuou.", "neutro")
                            else: player['ativo'] = None
                            st.rerun()

    # Banco Horizontal
    if player['banco']:
        st.markdown("---")
        cols = st.columns(5)
        for i, p in enumerate(player['banco']):
            with cols[i]:
                st.image(p.imagem_url)
                st.caption(f"{p.nome} ({p.hp_atual})")
                
                if p.hp_atual == 0:
                    if st.button("💀 KO", key=f"kob_{p.id_unico}"):
                        player['banco'].pop(i)
                        player['descarte'].append(p)
                        adicionar_log(f"💀 {p.nome} (Banco) morreu.", "ko")
                        # Premios
                        op_key = "Treinador 2" if id_jogador_chave == "Treinador 1" else "Treinador 1"
                        qtd = 2 if "ex" in p.nome.lower() else 1
                        st.session_state.Treinadores[op_key]['premios'] -= qtd
                        adicionar_log(f"🏆 {qtd} Prêmios pegos.", "ko")
                        if checar_vitoria(id_jogador_chave): st.session_state.vencedor = st.session_state.Treinadores[op_key]['nome']
                        st.rerun()
                else:
                    c1, c2 = st.columns(2)
                    with c1: 
                        if st.button("⬆️", key=f"up_{p.id_unico}"):
                            if not player['ativo']:
                                player['ativo'] = player['banco'].pop(i)
                                adicionar_log(f"🆙 {p.nome} subiu!", "neutro")
                                st.rerun()
                    with c2:
                        if st.button("💔", key=f"dmb_{p.id_unico}"):
                            p.receber_dano(10)
                            st.rerun()
                    
                    if p.habilidade:
                        ja_usou = p.id_unico in st.session_state.habilidades_usadas
                        cls = "hab-btn-used" if ja_usou else "hab-btn"
                        st.markdown(f'<div class="{cls}">', unsafe_allow_html=True)
                        if st.button("✨", key=f"hb_{p.id_unico}", help=p.habilidade, disabled=ja_usou):
                            st.session_state.habilidades_usadas.append(p.id_unico)
                            adicionar_log(f"✨ {p.nome} (Banco) usou habilidade.", "tool")
                            st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# --- 7. TELA PRINCIPAL ---
if st.session_state.vencedor:
    st.balloons()
    st.markdown(f"<h1 style='text-align: center; font-size: 80px; color: gold !important;'>🏆 {st.session_state.vencedor} VENCEU! 🏆</h1>", unsafe_allow_html=True)
    if st.button("Jogar Novamente", type="primary"):
        st.session_state.clear()
        st.rerun()
else:
    c1, c2 = st.columns(2)
    with c1: renderizar_mesa_jogador("Treinador 1")
    with c2: renderizar_mesa_jogador("Treinador 2")

    st.divider()
    st.subheader("📜 Log de Batalha")
    log_html = "".join(st.session_state.log)
    st.markdown(f"<div style='max-height: 200px; overflow-y: auto; background-color: rgba(0,0,0,0.5); border-radius: 10px;'>{log_html}</div>", unsafe_allow_html=True)
