import streamlit as st
import datetime
import random 
import re 

st.set_page_config(page_title="PokéBattle 11.0 (Sidebar Dark)", page_icon="⚔️", layout="wide")

# --- 0. CONFIGURAÇÃO VISUAL (DARK + SIDEBAR + SEM BORDAS) ---
def configurar_visual():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
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
        div[data-testid="stVerticalBlockBorderWrapper"], div[data-testid="stExpander"] {
            background-color: #1e293b;
            border: 1px solid #334155;
            border-radius: 12px;
        }

        /* Inputs Escuros */
        .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
            background-color: #0f172a !important;
            color: #e2e8f0 !important;
            border: 1px solid #475569 !important;
            border-radius: 6px;
        }

        /* --- BOTÕES (SEM BORDAS BRANCAS) --- */
        .stButton > button {
            border-radius: 8px;
            font-weight: 600;
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
            transition: all 0.2s;
            width: 100%;
        }

        /* Botão Padrão (Dark Blue) */
        .stButton > button {
            background-color: #334155 !important;
            color: white !important;
        }
        .stButton > button:hover { background-color: #475569 !important; }

        /* Botão AMARELO (Ação) */
        .btn-yellow > button {
            background-color: #FFC107 !important;
            color: #0f172a !important;
        }
        .btn-yellow > button:hover { background-color: #FFD54F !important; transform: scale(1.02); }

        /* Botão VERMELHO (Dano/KO) */
        .btn-red > button {
            background-color: #EF4444 !important;
            color: white !important;
        }

        /* Botão VERDE (Turno) */
        .btn-green > button {
            background-color: #22c55e !important;
            color: white !important;
            height: 50px;
            font-size: 18px !important;
        }

        /* Botão AZUL (Habilidade) */
        .btn-blue > button {
            background-color: #3B82F6 !important;
            color: white !important;
        }
        
        /* Botões Pequenos (+10, +20) */
        .btn-small > button {
            padding: 2px 5px !important;
            font-size: 12px !important;
            min-height: 30px !important;
        }

        /* Badges */
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
        
        .log-entry {
            padding: 4px;
            border-bottom: 1px solid #334155;
            font-size: 13px;
        }
    </style>
    """, unsafe_allow_html=True)

configurar_visual()

# --- 1. BANCO DE DADOS ---
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

# --- 2. CLASSE POKEMON ---
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
            return True, f"Pagou {custo} de energia."
        else: return False, f"Precisa de {custo} energias."

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
    if 'dmg_buffer' not in st.session_state: st.session_state.dmg_buffer = {}

def adicionar_log(mensagem, tipo="neutro"):
    hora = datetime.datetime.now().strftime("%H:%M")
    colors = {"ataque": "#f87171", "energia": "#c084fc", "cura": "#4ade80", "ko": "#fb923c", "tool": "#60a5fa", "neutro": "#94a3b8"}
    c = colors.get(tipo, "white")
    st.session_state.log.insert(0, f"<div class='log-entry' style='color:{c}'>[{hora}] {mensagem}</div>")

inicializar_jogo()

# --- 4. BARRA LATERAL (VOLTOU) ---
with st.sidebar:
    st.markdown("### ⚙️ Controle")
    
    st.markdown('<div class="btn-green">', unsafe_allow_html=True)
    if st.button("⏳ PASSAR TURNO", help="Limpa habilidades e passa a vez"):
        st.session_state.habilidades_usadas = []
        antigo = st.session_state.turno_atual
        novo = "Treinador 2" if antigo == "Treinador 1" else "Treinador 1"
        st.session_state.turno_atual = novo
        nome_novo = st.session_state.Treinadores[novo]['nome']
        adicionar_log(f"🕒 <b>Fim do turno.</b> Vez de <b>{nome_novo}</b>!", "neutro")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    with st.expander("👤 Jogadores", expanded=True):
        n1 = st.text_input("J1", value=st.session_state.Treinadores["Treinador 1"]["nome"])
        n2 = st.text_input("J2", value=st.session_state.Treinadores["Treinador 2"]["nome"])
        if st.button("Salvar Nomes"):
            st.session_state.Treinadores["Treinador 1"]["nome"] = n1
            st.session_state.Treinadores["Treinador 2"]["nome"] = n2
            st.rerun()
    
    st.markdown("### 🏆 Placar")
    c1, c2 = st.columns(2)
    c1.metric(n1, f"{st.session_state.Treinadores['Treinador 1']['premios']} 🎴")
    c2.metric(n2, f"{st.session_state.Treinadores['Treinador 2']['premios']} 🎴")
    
    st.divider()
    
    st.markdown('<div class="btn-yellow">', unsafe_allow_html=True)
    if st.button("🔄 Checkup Auto"):
        logs_totais = []
        for p in ["Treinador 1", "Treinador 2"]:
            if st.session_state.Treinadores[p]['ativo']:
                res = st.session_state.Treinadores[p]['ativo'].resolver_checkup()
                if res: logs_totais.extend(res)
        if logs_totais:
            for l in logs_totais: adicionar_log(l, "ko")
            st.success("Checkup OK")
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("🪙 Moeda"):
        res = random.choice(["CARA", "COROA"])
        adicionar_log(f"🪙 Moeda: {res}")
        st.toast(f"Moeda: {res}")

    if st.button("🗑️ Reset Jogo"):
        st.session_state.clear()
        st.rerun()

    if st.session_state.log:
        txt_log = "\n".join([re.sub('<[^<]+?>', '', l) for l in st.session_state.log[::-1]])
        st.download_button("💾 Baixar Log", txt_log, "log.txt")

    st.divider()
    st.markdown("### ➕ Add Pokémon")
    dono_key = st.selectbox("Dono", ["Treinador 1", "Treinador 2"], format_func=lambda x: st.session_state.Treinadores[x]['nome'])
    modo = st.radio("Modo", ["📚 Pokedex", "✍️ Manual"])
    
    if "Pokedex" in modo:
        escolha = st.selectbox("Poke", list(POKEDEX.keys()))
        dados = POKEDEX[escolha]
        st.image(dados["img"], width=100)
        if st.button("Adicionar"):
            novo = Pokemon(escolha, dados["hp"], dados["tipo"], dados["fraq"], dados["res"], dados.get("recuo", 1), dados["img"], dados.get("hab"))
            player = st.session_state.Treinadores[dono_key]
            if not player['ativo']: player['ativo'] = novo
            elif len(player['banco']) < 5: player['banco'].append(novo)
            else: st.error("Cheio!")
            st.rerun()
    else:
        nome_m = st.text_input("Nome")
        hp_m = st.number_input("HP", value=60, step=10)
        img_m = st.text_input("URL Imagem")
        if st.button("Criar Manual"):
            novo = Pokemon(nome_m, hp_m, "Normal", "Nenhuma", "Nenhuma", 1, img_m)
            player = st.session_state.Treinadores[dono_key]
            if not player['ativo']: player['ativo'] = novo
            elif len(player['banco']) < 5: player['banco'].append(novo)
            st.rerun()

# --- 5. MESA ---
def render_player(key):
    p = st.session_state.Treinadores[key]
    eh_vez = (st.session_state.turno_atual == key)
    borda = "2px solid #FFCB05" if eh_vez else "1px solid #334155"
    
    st.markdown(f"<div style='border:{borda}; background-color:#1e293b; padding:10px; border-radius:10px; margin-bottom:10px;'>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='margin:0'>{p['nome']}</h3>", unsafe_allow_html=True)
    
    ativo = p['ativo']
    if ativo:
        st.markdown("---")
        c_img, c_info = st.columns([1, 2])
        with c_img:
            st.image(ativo.imagem_url, use_container_width=True)
            
            # --- STATUS / ENERGIA VISÍVEL (Pedido Atendido) ---
            badges = ""
            if "ex" in ativo.nome.lower(): badges += "<span class='badge badge-ex'>EX</span>"
            badges += f"<span class='badge badge-status'>{ativo.status}</span>"
            st.markdown(badges, unsafe_allow_html=True)
            
            # Energias visíveis na carta
            txt_en = " ".join([f"{k.split()[-1]}x{v}" for k,v in ativo.energias.items()])
            if txt_en: st.markdown(f"<div style='background:#0f172a; padding:5px; border-radius:5px; margin-top:5px; font-size:12px; border:1px solid #334155;'>⚡ {txt_en}</div>", unsafe_allow_html=True)
            if ativo.ferramenta != "Nenhuma": st.caption(f"🛠️ {ativo.ferramenta}")

        with c_info:
            st.markdown(f"**{ativo.nome}** <span style='float:right'>HP: {ativo.hp_atual}/{ativo.hp_max}</span>", unsafe_allow_html=True)
            st.progress(ativo.hp_atual / ativo.hp_max)
            
            if ativo.hp_atual == 0:
                st.error("💀 NOCAUTEADO")
                st.markdown('<div class="btn-red">', unsafe_allow_html=True)
                if st.button("Enviar p/ Descarte", key=f"ko_{ativo.id_unico}"):
                    p['descarte'].append(ativo)
                    p['ativo'] = None
                    adicionar_log(f"💀 {ativo.nome} caiu!", "ko")
                    op_key = "Treinador 2" if key == "Treinador 1" else "Treinador 1"
                    qtd = 2 if "ex" in ativo.nome.lower() else 1
                    st.session_state.Treinadores[op_key]['premios'] -= qtd
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                # Calculadora Dano
                if ativo.id_unico not in st.session_state.dmg_buffer: st.session_state.dmg_buffer[ativo.id_unico] = 0
                cb1, cb2, cb3, cb4 = st.columns(4)
                with cb1: 
                    st.markdown('<div class="btn-small">', unsafe_allow_html=True)
                    if st.button("0", key=f"z_{ativo.id_unico}"): st.session_state.dmg_buffer[ativo.id_unico] = 0; st.rerun()
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
                
                dmg = st.number_input("Dano", value=st.session_state.dmg_buffer[ativo.id_unico], step=10, key=f"d_{ativo.id_unico}", label_visibility="collapsed")
                st.session_state.dmg_buffer[ativo.id_unico] = dmg

                st.markdown('<div class="btn-yellow">', unsafe_allow_html=True)
                if st.button("⚔️ ATACAR", key=f"atk_{ativo.id_unico}"):
                    op_key = "Treinador 2" if key == "Treinador 1" else "Treinador 1"
                    op = st.session_state.Treinadores[op_key]
                    if op['ativo']:
                        mult = 2 if ativo.tipo == op['ativo'].fraqueza else 1
                        red = 30 if ativo.tipo == op['ativo'].resistencia else 0
                        final = (dmg * mult) - red
                        if final < 0: final = 0
                        op['ativo'].receber_dano(final)
                        adicionar_log(f"⚔️ {ativo.nome} causou {final}!", "ataque")
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
                
                # --- MENU COMPLETO (Consertado) ---
                with st.popover("⚡ Energia / Status / 🛠️"):
                    t1, t2, t3, t4 = st.tabs(["+ Energia", "- Energia", "Status", "Tool"])
                    
                    with t1: # Add Energia
                        e = st.selectbox("Tipo", ["Fogo 🔥", "Água 💧", "Planta 🌱", "Elétrico ⚡", "Psíquico 🌀", "Luta 🥊", "Escuridão 🌙", "Metal ⚙️"], key=f"ae_{ativo.id_unico}")
                        if st.button("Adicionar", key=f"bae_{ativo.id_unico}"): 
                            ativo.anexar_energia(e); st.rerun()
                    
                    with t2: # Remove Energia (VOLTOU!)
                        if ativo.energias:
                            r = st.selectbox("Remover", list(ativo.energias.keys()), key=f"re_{ativo.id_unico}")
                            if st.button("Remover", key=f"bre_{ativo.id_unico}"): 
                                ativo.remover_energia(r); st.rerun()
                        else: st.info("Sem energias.")

                    with t3: # Status
                        st.selectbox("Condição", ["Saudável", "Envenenado 🧪", "Queimado 🔥", "Adormecido 💤", "Paralisado ⚡"], key=f"st_{ativo.id_unico}", on_change=lambda: setattr(ativo, 'status', st.session_state[f"st_{ativo.id_unico}"]))
                    
                    with t4: # Tools (VOLTOU!)
                        tl = st.selectbox("Ferramenta", list(TOOLS_DB.keys()), key=f"tl_{ativo.id_unico}")
                        if st.button("Equipar", key=f"btl_{ativo.id_unico}"):
                            ativo.equipar_ferramenta(tl); st.rerun()

                # Habilidade
                if ativo.habilidade:
                    ja = ativo.id_unico in st.session_state.habilidades_usadas
                    cls = "stButton" if ja else "btn-blue"
                    lbl = "✅ Usado" if ja else f"✨ {ativo.habilidade}"
                    st.markdown(f'<div class="{cls}">', unsafe_allow_html=True)
                    if st.button(lbl, key=f"hab_{ativo.id_unico}", disabled=ja):
                        st.session_state.habilidades_usadas.append(ativo.id_unico)
                        adicionar_log(f"✨ {ativo.nome} usou {ativo.habilidade}!", "tool")
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
    
    # Banco
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
                        adicionar_log(f"💀 {bp.nome} (Banco) caiu!", "ko")
                        # Premio
                        op_key = "Treinador 2" if key == "Treinador 1" else "Treinador 1"
                        q = 2 if "ex" in bp.nome.lower() else 1
                        st.session_state.Treinadores[op_key]['premios'] -= q
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    if st.button("⬆️", key=f"up_{bp.id_unico}"):
                        if not p['ativo']: p['ativo'] = p['banco'].pop(i); st.rerun()
                    if st.button("💔", key=f"dmb_{bp.id_unico}"):
                        bp.receber_dano(10); st.rerun()
                    if bp.habilidade:
                        ja = bp.id_unico in st.session_state.habilidades_usadas
                        if st.button("✨", key=f"hbb_{bp.id_unico}", disabled=ja, help=bp.habilidade):
                            st.session_state.habilidades_usadas.append(bp.id_unico)
                            adicionar_log(f"✨ {bp.nome} (Banco) hab.", "tool")
                            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# --- 6. RENDERIZAÇÃO ---
if st.session_state.vencedor:
    st.balloons()
    st.title(f"🏆 {st.session_state.vencedor} VENCEU!")
    if st.button("Novo Jogo"): st.session_state.clear(); st.rerun()
else:
    st.title("🏆 PokéBattle 11.0")
    c1, c2 = st.columns(2)
    with c1: render_player("Treinador 1")
    with c2: render_player("Treinador 2")
    
    st.divider()
    st.subheader("📜 Histórico")
    st.markdown("".join(st.session_state.log), unsafe_allow_html=True)
