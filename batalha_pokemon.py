import streamlit as st
import datetime
import random 
import re 

st.set_page_config(page_title="PokéBattle 5.3 (Regra EX)", page_icon="💀", layout="wide")

# --- 0. CONFIGURAÇÃO VISUAL ---
# --- 0. CONFIGURAÇÃO VISUAL (BOTÕES AJUSTADOS) ---
def configurar_visual():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Roboto', sans-serif; }

    [data-testid="stAppViewContainer"] {
        background-image: url("https://pokemonrevolution.net/forum/uploads/monthly_2021_03/DVMT-6OXcAE2rZY.jpg.afab972f972bd7fbd4253bc7aa1cf27f.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        filter: brightness(0.8);
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: rgba(0,0,0,0.85);
        border-radius: 16px;
        padding: 15px;
        backdrop-filter: blur(6px);
    }

    h1, h2, h3, p, span, label {
        color: white !important;
        text-shadow: 2px 2px 4px black;
    }

    .stButton > button {
        background-color: #FFCB05 !important;
        color: #2a3b96 !important;
        font-weight: bold;
        border-radius: 12px;
        width: 100%;
        padding: 6px;
        font-size: 16px;
    }

    .stButton > button:hover {
        transform: scale(1.03);
        box-shadow: 0px 0px 15px #ffcb05;
    }

    .damage {
        animation: shake 0.3s;
        color: #ff4c4c;
        font-weight: bold;
    }

    @keyframes shake {
        0% { transform: translateX(0); }
        25% { transform: translateX(-4px); }
        50% { transform: translateX(4px); }
        75% { transform: translateX(-4px); }
        100% { transform: translateX(0); }
    }
    </style>
    """, unsafe_allow_html=True)


configurar_visual()

# --- 1. BANCO DE DADOS ---
POKEDEX = {
    # --- DECK DRAGAPULT EX ---
    "Dragapult ex": {"hp": 320, "tipo": "Dragão 🐉", "fraq": "Nenhuma", "res": "Nenhuma", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/TWM/TWM_130_R_EN_PNG.png"},
    "Drakloak": {"hp": 90, "tipo": "Dragão 🐉", "fraq": "Nenhuma", "res": "Nenhuma", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/TWM/TWM_129_R_EN_PNG.png"},
    "Dreepy": {"hp": 70, "tipo": "Dragão 🐉", "fraq": "Nenhuma", "res": "Nenhuma", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/TWM/TWM_128_R_EN_PNG.png"},
    "Xatu": {"hp": 100, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/PAR/PAR_072_R_EN_PNG.png"},
    "Natu": {"hp": 60, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/PAR/PAR_071_R_EN_PNG.png"},
    "Fezandipiti ex": {"hp": 210, "tipo": "Psíquico 🌀", "fraq": "Metal ⚙️", "res": "Nenhuma", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/SFA/SFA_038_R_EN_PNG.png"},

    # --- DECK CHARIZARD EX ---
    "Charizard ex": {"hp": 330, "tipo": "Escuridão 🌙", "fraq": "Planta 🌱", "res": "Nenhuma", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/OBF/OBF_125_R_EN_PNG.png"},
    "Charmeleon": {"hp": 90, "tipo": "Fogo 🔥", "fraq": "Água 💧", "res": "Nenhuma", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/OBF/OBF_027_R_EN_PNG.png"},
    "Charmander": {"hp": 70, "tipo": "Fogo 🔥", "fraq": "Água 💧", "res": "Nenhuma", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/OBF/OBF_026_R_EN_PNG.png"},
    "Pidgeot ex": {"hp": 280, "tipo": "Normal ⚪", "fraq": "Elétrico ⚡", "res": "Luta 🥊", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/OBF/OBF_164_R_EN_PNG.png"},
    "Pidgey": {"hp": 60, "tipo": "Normal ⚪", "fraq": "Elétrico ⚡", "res": "Luta 🥊", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/OBF/OBF_162_R_EN_PNG.png"},
    "Moltres": {"hp": 120, "tipo": "Fogo 🔥", "fraq": "Água 💧", "res": "Nenhuma", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/BRS/BRS_021_R_EN_PNG.png"},

    # --- DECK GARDEVOIR EX ---
    "Gardevoir ex": {"hp": 310, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/SVI/SVI_086_R_EN_PNG.png"},
    "Kirlia": {"hp": 80, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/SVI/SVI_085_R_EN_PNG.png"},
    "Ralts": {"hp": 60, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/SVI/SVI_084_R_EN_PNG.png"},
    "Drifloon": {"hp": 70, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/SVI/SVI_089_R_EN_PNG.png"},
    "Scream Tail": {"hp": 90, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/PAR/PAR_086_R_EN_PNG.png"},
    "Mew ex": {"hp": 180, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/MEW/MEW_151_R_EN_PNG.png"},
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
    def __init__(self, nome, hp_max, tipo, fraqueza, resistencia, imagem_url=""):
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

    def equipar_ferramenta(self, nome_ferramenta):
        if self.ferramenta in TOOLS_DB:
            bonus_antigo = TOOLS_DB[self.ferramenta]["hp_bonus"]
            self.hp_max -= bonus_antigo
            if self.hp_atual > self.hp_max:
                self.hp_atual = self.hp_max

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

    def aplicar_dano_status(self):
        dano = 0
        msg = ""
        if self.status == "Envenenado 🧪":
            dano = 10
            msg = f"🧪 {self.nome} sofreu 10 de veneno."
        elif self.status == "Queimado 🔥":
            dano = 20
            msg = f"🔥 {self.nome} sofreu 20 de queimadura."
            
        if dano > 0:
            self.receber_dano(dano)
            return msg
        return None

    def evoluir_para(self, novo_nome, novo_hp, novo_tipo, nova_fraqueza, nova_resistencia, nova_img):
        dano_sofrido = self.hp_max - self.hp_atual
        self.nome = novo_nome
        self.hp_base = int(novo_hp)
        
        bonus_ferramenta = TOOLS_DB[self.ferramenta]["hp_bonus"]
        self.hp_max = self.hp_base + bonus_ferramenta
        
        self.tipo = novo_tipo
        self.fraqueza = nova_fraqueza
        self.resistencia = nova_resistencia
        if nova_img: self.imagem_url = nova_img
        
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
            "Treinador 1": {
                "nome": "Treinador 1",
                "ativo": None, 
                "banco": [], 
                "descarte": [], 
                "premios": 6 # Pode ajustar para 6 se for jogo oficial
            },
            "Treinador 2": {
                "nome": "Treinador 2",
                "ativo": None, 
                "banco": [], 
                "descarte": [], 
                "premios": 6
            }
        }
    if 'log' not in st.session_state:
        st.session_state.log = []
    if 'vencedor' not in st.session_state:
        st.session_state.vencedor = None

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

# --- 4. BARRA LATERAL ---
with st.sidebar:
    st.header("⚙️ Controle")
    
    with st.expander("👤 Personalizar Nomes", expanded=True):
        nome_t1_input = st.text_input("Nome Jogador 1", value=st.session_state.Treinadores["Treinador 1"]["nome"])
        nome_t2_input = st.text_input("Nome Jogador 2", value=st.session_state.Treinadores["Treinador 2"]["nome"])
        
        st.session_state.Treinadores["Treinador 1"]["nome"] = nome_t1_input
        st.session_state.Treinadores["Treinador 2"]["nome"] = nome_t2_input
    
    st.subheader("🏆 Placar")
    c1, c2 = st.columns(2)
    n1 = st.session_state.Treinadores["Treinador 1"]["nome"]
    p1 = st.session_state.Treinadores["Treinador 1"]["premios"]
    n2 = st.session_state.Treinadores["Treinador 2"]["nome"]
    p2 = st.session_state.Treinadores["Treinador 2"]["premios"]
    
    c1.metric(n1, f"{p1} 🎴")
    c2.metric(n2, f"{p2} 🎴")
    
    st.divider()

    st.subheader("🪙 Moeda")
    if st.button("Jogar Moeda"):
        resultado = random.choice(["CARA (Heads)", "COROA (Tails)"])
        adicionar_log(f"🪙 A moeda caiu em: {resultado}")
        if "CARA" in resultado: st.success(f"{resultado}")
        else: st.error(f"{resultado}")

    st.divider()
    
    st.info("Fim de Turno")
    if st.button("☣️ Aplicar Danos de Status"):
        logs_status = []
        for nome_jog in ["Treinador 1", "Treinador 2"]:
            ativo = st.session_state.Treinadores[nome_jog]['ativo']
            if ativo:
                resultado = ativo.aplicar_dano_status()
                if resultado: logs_status.append(resultado)
        if logs_status:
            for log in logs_status: adicionar_log(log, "ko")
            st.success("Danos aplicados!")
            st.rerun()
        else:
            st.toast("Sem danos de status.")

    st.divider()
    
    st.subheader("💾 Salvar Registro")
    if st.session_state.log:
        texto_log = "REGISTRO DE BATALHA POKEMON TCG\n"
        texto_log += f"Data: {datetime.datetime.now().strftime('%d/%m/%Y')}\n"
        texto_log += f"Jogadores: {n1} vs {n2}\n"
        texto_log += "-----------------------------------\n"
        
        log_reverso = st.session_state.log[::-1]
        for linha in log_reverso:
            texto_limpo = re.sub('<[^<]+?>', '', linha)
            texto_log += texto_limpo + "\n"
            
        st.download_button(
            label="📄 Baixar Arquivo .txt",
            data=texto_log,
            file_name="registro_batalha.txt",
            mime="text/plain"
        )
    else:
        st.caption("O registro está vazio.")

    st.divider()

    st.subheader("➕ Gerenciar Cartas")
    
    dono_key = st.selectbox(
        "Treinador:", 
        ["Treinador 1", "Treinador 2"], 
        format_func=lambda x: st.session_state.Treinadores[x]['nome']
    )
    
    modo = st.radio("Modo de Criação:", ["📚 Pokedex (Rápido)", "✍️ Manual (Customizado)"], horizontal=True)
    
    nome_final = ""
    hp_final = 0
    tipo_final = ""
    fraq_final = ""
    res_final = ""
    img_final = ""
    
    if "Pokedex" in modo:
        escolha_pokedex = st.selectbox("Escolha o Pokémon:", list(POKEDEX.keys()))
        dados = POKEDEX[escolha_pokedex]
        st.image(dados["img"], width=100)
        
        nome_final = escolha_pokedex
        hp_final = dados["hp"]
        tipo_final = dados["tipo"]
        fraq_final = dados["fraq"]
        res_final = dados["res"]
        img_final = dados["img"]
        
    else:
        nome_final = st.text_input("Nome do Pokémon")
        hp_final = st.number_input("HP Máximo", value=60, step=10)
        img_final = st.text_input("Cole o Link da Imagem aqui 👇")
        lista_tipos = ["Normal ⚪", "Fogo 🔥", "Água 💧", "Planta 🌱", "Elétrico ⚡", "Psíquico 🌀", "Luta 🥊", "Escuridão 🌙", "Metal ⚙️", "Dragão 🐉"]
        tipo_final = st.selectbox("Tipo", lista_tipos)
        fraq_final = st.selectbox("Fraqueza", lista_tipos)
        res_final = st.selectbox("Resistência", ["Nenhuma"] + lista_tipos)

    player_temp = st.session_state.Treinadores[dono_key]
    nome_dono_display = player_temp['nome']

    opcoes_evolucao = []
    if player_temp['ativo']: opcoes_evolucao.append(f"[Ativo] {player_temp['ativo'].nome}")
    for i, p in enumerate(player_temp['banco']): opcoes_evolucao.append(f"[Banco {i+1}] {p.nome}")
    
    acao = st.radio("Ação:", ["Novo Básico", "Evoluir"], horizontal=True)
    
    alvo_evolucao = None
    if acao == "Evoluir":
        if opcoes_evolucao: alvo_evolucao = st.selectbox("Quem evolui?", opcoes_evolucao)
        else: st.warning("Ninguém para evoluir.")
    
    destino = "Banco"
    if acao == "Novo Básico":
        destino = st.radio("Onde colocar?", ["Ativo", "Banco"], horizontal=True)

    if st.button("✨ Criar Carta", type="primary"):
        if acao == "Novo Básico":
            if nome_final:
                novo = Pokemon(nome_final, hp_final, tipo_final, fraq_final, res_final, img_final)
                if destino == "Ativo" and player_temp['ativo'] is None:
                    player_temp['ativo'] = novo
                    adicionar_log(f"🆕 {nome_final} entrou como Ativo de {nome_dono_display}.", "neutro")
                elif len(player_temp['banco']) < 5:
                    player_temp['banco'].append(novo)
                    adicionar_log(f"🆕 {nome_final} entrou no Banco de {nome_dono_display}.", "neutro")
                else:
                    st.error("Sem espaço!")
                st.rerun()
            else:
                st.error("O Pokémon precisa de um nome!")
        
        elif acao == "Evoluir" and alvo_evolucao:
            obj = player_temp['ativo'] if "[Ativo]" in alvo_evolucao else player_temp['banco'][int(alvo_evolucao.split("]")[0].split(" ")[1])-1]
            antigo = obj.nome
            obj.evoluir_para(nome_final, hp_final, tipo_final, fraq_final, res_final, img_final)
            adicionar_log(f"🧬 {antigo} evoluiu para {nome_final}!", "energia")
            st.balloons()
            st.rerun()

    if st.button("🗑️ Reiniciar Jogo"):
        st.session_state.clear()
        st.rerun()

# --- 5. LÓGICA DE VITÓRIA E RENDERIZAÇÃO ---
def checar_vitoria(id_oponente_chave):
    if st.session_state.Treinadores[id_oponente_chave]['premios'] <= 0: return True
    oponente = st.session_state.Treinadores[id_oponente_chave]
    if oponente['ativo'] is None and len(oponente['banco']) == 0: return True
    return False

def renderizar_mesa_jogador(id_jogador_chave):
    player = st.session_state.Treinadores[id_jogador_chave]
    nome_display = player['nome']
    
    cor_texto = "#89CFF0" if id_jogador_chave == "Treinador 1" else "#FF6961"
    border_color = "#89CFF0" if id_jogador_chave == "Treinador 1" else "#FF6961"
    
    id_oponente_chave = "Treinador 2" if id_jogador_chave == "Treinador 1" else "Treinador 1"
    player_oponente = st.session_state.Treinadores[id_oponente_chave]
    nome_oponente_display = player_oponente['nome']
    ativo_oponente = player_oponente['ativo'] 
    
    st.markdown(f"""
        <div style='background-color: rgba(0,0,0,0.5); padding: 5px; border-radius: 10px; text-align: center; margin-bottom: 10px; border: 2px solid {border_color};'>
            <h2 style='margin:0; color: {cor_texto};'>{nome_display.upper()}</h2>
            <p style='margin:0; color: white;'>Prêmios Restantes: <strong>{player['premios']}</strong> 🎴</p>
        </div>
    """, unsafe_allow_html=True)
    
    ativo = player['ativo']
    if ativo:
        with st.container(border=True):
            col_img, col_infos = st.columns([1, 2])
            with col_img:
                st.image(ativo.imagem_url, use_container_width=True)
                st.caption(f"{ativo.tipo} | Fraco: {ativo.fraqueza}")
                if ativo.status != "Saudável": st.warning(ativo.status)
                
                txt_en = "".join([f"{k.split()[-1]}x{v} " for k,v in ativo.energias.items()])
                if txt_en: st.markdown(f"**⚡ {txt_en}**")
                
                if ativo.ferramenta != "Nenhuma":
                    st.info(f"🛠️ {ativo.ferramenta}")
            
            with col_infos:
                st.subheader(ativo.nome)
                
                st.progress(ativo.hp_atual / ativo.hp_max)
                st.write(f"HP: {ativo.hp_atual}/{ativo.hp_max}")
                
                if ativo.hp_atual == 0:
                    st.error("💀 NOCAUTEADO!")
                    if st.button("Enviar p/ Descarte 💀", key=f"ko_{ativo.id_unico}"):
                        player['descarte'].append(ativo)
                        player['ativo'] = None
                        adicionar_log(f"☠️ {ativo.nome} ({nome_display}) foi nocauteado!", "ko")
                        
                        # --- NOVA LÓGICA: 2 PRÊMIOS SE FOR EX ---
                        qtd_premios = 2 if "ex" in ativo.nome.lower() else 1
                        
                        player_oponente['premios'] -= qtd_premios
                        pl = "s" if qtd_premios > 1 else ""
                        adicionar_log(f"🏆 {nome_oponente_display} pegou {qtd_premios} carta{pl} prêmio!", "ko")
                        
                        if checar_vitoria(id_jogador_chave):
                            st.session_state.vencedor = nome_oponente_display
                        st.rerun()
                else:
                    novo_status = st.selectbox("Status", ["Saudável", "Envenenado 🧪", "Queimado 🔥", "Adormecido 💤", "Paralisado ⚡"], key=f"st_{ativo.id_unico}")
                    if novo_status != ativo.status:
                        ativo.status = novo_status
                        st.rerun()
                    
                    with st.popover("⚡ Energia / 🛠️ Tool"):
                        t1, t2, t3 = st.tabs(["Ligar Energia", "Tirar Energia", "Equipar Tool"])
                        with t1:
                            escolha = st.selectbox("Tipo", ["Fogo 🔥", "Água 💧", "Planta 🌱", "Elétrico ⚡", "Psíquico 🌀", "Luta 🥊", "Escuridão 🌙", "Metal ⚙️"], key=f"add_e_{ativo.id_unico}")
                            if st.button("Ligar", key=f"btn_add_e_{ativo.id_unico}"):
                                ativo.anexar_energia(escolha)
                                adicionar_log(f"⚡ {ativo.nome} ligou Energia {escolha}.", "energia")
                                st.rerun()
                        with t2:
                            if ativo.energias:
                                rem = st.selectbox("Tirar", list(ativo.energias.keys()), key=f"rem_e_{ativo.id_unico}")
                                if st.button("Descartar", key=f"btn_rem_e_{ativo.id_unico}"):
                                    ativo.remover_energia(rem)
                                    adicionar_log(f"🗑️ {ativo.nome} descartou Energia {rem}.", "energia")
                                    st.rerun()
                        with t3:
                            lista_ferramentas = list(TOOLS_DB.keys())
                            escolha_tool = st.selectbox("Ferramenta:", lista_ferramentas, key=f"tool_{ativo.id_unico}")
                            if st.button("Equipar", key=f"btn_tool_{ativo.id_unico}"):
                                ativo.equipar_ferramenta(escolha_tool)
                                adicionar_log(f"🛠️ {ativo.nome} equipou {escolha_tool}.", "tool")
                                st.rerun()

                    st.divider()
                    c_atk, c_self = st.columns(2)
                    with c_atk:
                        dano = st.number_input("Dano", step=10, key=f"d_{ativo.id_unico}")
                        if st.button("⚔️ ATACAR", key=f"atk_{ativo.id_unico}"):
                            if ativo_oponente:
                                mult = 2 if ativo.tipo == ativo_oponente.fraqueza else 1
                                red = 30 if ativo.tipo == ativo_oponente.resistencia else 0
                                final = (dano * mult) - red
                                if final < 0: final = 0
                                
                                ativo_oponente.receber_dano(final)
                                msg_extra = " (x2)" if mult > 1 else " (-30)" if red > 0 else ""
                                adicionar_log(f"⚔️ {ativo.nome} atacou {ativo_oponente.nome} causando {final} de dano{msg_extra}!", "ataque")
                                st.rerun()
                    with c_self:
                        if st.button("💔 -10 Self", key=f"s_{ativo.id_unico}"):
                             ativo.receber_dano(10)
                             st.rerun()
                        if st.button("🏃 Recuar", key=f"r_{ativo.id_unico}"):
                            ativo.status = "Saudável"
                            if player['banco']:
                                player['banco'].append(ativo)
                                player['ativo'] = None
                                adicionar_log(f"🏃 {ativo.nome} recuou para o banco.", "neutro")
                            else:
                                player['ativo'] = None
                            st.rerun()

    if player['banco']:
        with st.expander(f"Banco ({len(player['banco'])})", expanded=True):
            cols = st.columns(5)
            for i, p in enumerate(player['banco']):
                with cols[i]:
                    st.image(p.imagem_url, caption=p.nome)
                    st.caption(f"HP: {p.hp_atual}")
                    if st.button("⬆️", key=f"up_{p.id_unico}"):
                        if not player['ativo']:
                            player['ativo'] = player['banco'].pop(i)
                            adicionar_log(f"🆙 {p.nome} subiu para o Ativo!", "neutro")
                            st.rerun()
                    if st.button("💔", key=f"db_{p.id_unico}"):
                        p.receber_dano(10)
                        st.rerun()
    
    if player['descarte']:
        with st.expander(f"🗑️ Descarte ({len(player['descarte'])})"):
            for carta in player['descarte']: st.write(f"💀 {carta.nome}")

# --- 6. TELA PRINCIPAL ---
if st.session_state.vencedor:
    st.balloons()
    st.markdown(f"<h1 style='text-align: center; font-size: 80px; color: gold !important;'>🏆 {st.session_state.vencedor} VENCEU! 🏆</h1>", unsafe_allow_html=True)
    if st.button("Jogar Novamente", type="primary"):
        st.session_state.clear()
        st.rerun()
else:
    st.title("🏆 Arena PokéBattle 5.3 (Final)")
    c1, c2 = st.columns(2)
    # Passamos as chaves fixas ("Treinador 1"), a função vai buscar o nome bonito lá dentro
    with c1: renderizar_mesa_jogador("Treinador 1")
    with c2: renderizar_mesa_jogador("Treinador 2")

    st.divider()
    st.subheader("📜 Log de Batalha")
    log_html = "".join(st.session_state.log)
    st.markdown(f"<div style='max-height: 200px; overflow-y: auto; background-color: rgba(0,0,0,0.5); border-radius: 10px;'>{log_html}</div>", unsafe_allow_html=True)
