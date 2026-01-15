import streamlit as st
import datetime
import random 

st.set_page_config(page_title="PokéBattle 4.3 (Final)", page_icon="👑", layout="wide")

# --- 0. CONFIGURAÇÃO VISUAL (MANTIDA DA SUA VERSÃO) ---
def configurar_visual():
    st.markdown("""
    <style>
        /* Importando Fonte Roboto do Google */
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Roboto', sans-serif;
        }

        /* --- 1. SEU FUNDO DE ARENA --- */
        [data-testid="stAppViewContainer"] {
            background-image: url("https://pokemonrevolution.net/forum/uploads/monthly_2021_03/DVMT-6OXcAE2rZY.jpg.afab972f972bd7fbd4253bc7aa1cf27f.jpg");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
        
        /* Deixar o cabeçalho transparente */
        [data-testid="stHeader"] {
            background-color: rgba(0,0,0,0);
        }

        /* --- 2. EFEITO DE VIDRO ESCURO --- */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: rgba(0, 0, 0, 0.8); /* Um pouco mais escuro para ler melhor */
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 15px;
            padding: 15px;
            backdrop-filter: blur(5px);
        }

        /* --- 3. TEXTOS BRANCOS --- */
        h1, h2, h3, p, span, div, label {
            color: #FFFFFF !important;
            text-shadow: 2px 2px 4px #000000;
        }
        
        /* Ajuste para inputs */
        .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
            background-color: rgba(255, 255, 255, 0.15);
            color: white;
            border: 1px solid rgba(255,255,255,0.5);
        }

        /* --- 4. BOTÕES (CORRIGIDOS SEM BORDA) --- */
        .stButton > button, .stButton > button:focus, .stButton > button:active {
            background-color: #FFCB05 !important;
            color: #2a3b96 !important;
            border-radius: 20px;
            border: 0px solid transparent !important;
            outline: none !important;
            box-shadow: none !important;
            font-weight: bold;
            transition: all 0.2s;
        }
        .stButton > button:hover {
            transform: scale(1.05);
            box-shadow: 0px 0px 15px rgba(255, 203, 5, 0.8) !important;
            color: black !important;
        }

        /* --- NOVO: ESTILO DO LOG COLORIDO --- */
        .log-entry {
            padding: 5px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            font-size: 14px;
        }
    </style>
    """, unsafe_allow_html=True)

configurar_visual()

# --- 1. BANCO DE DADOS (PRESETS - NOVO) ---
# --- 1. BANCO DE DADOS (DECKS NIVEL 3) ---
POKEDEX = {
    # --- DECK DRAGAPULT EX (Dragão/Fantasma) ---
    "Dragapult ex": {"hp": 320, "tipo": "Dragão 🐉", "fraq": "Nenhuma", "res": "Nenhuma", "img": "https://repositorio.sbrauble.com/arquivos/in/pokemon_bkp/cd/538/664e7dfe2f85e-ub7gp-matci-bf0a677346ca8d8f5a187aed2c1b61c1.jpg"},
    "Drakloak": {"hp": 90, "tipo": "Dragão 🐉", "fraq": "Nenhuma", "res": "Nenhuma", "img": "https://repositorio.sbrauble.com/arquivos/in/pokemon_bkp/cd/649/678a967bd1518-jil3f-br0ju-4359ccc37706d80d5ae766a57d5be016.jpg"},
    "Dreepy": {"hp": 70, "tipo": "Dragão 🐉", "fraq": "Nenhuma", "res": "Nenhuma", "img": "https://repositorio.sbrauble.com/arquivos/in/pokemon_bkp/cd/649/678a967a09a20-i90ol-r0wyq-4359ccc37706d80d5ae766a57d5be016.jpg"},
    "Fezandipiti ex": {"hp": 210, "tipo": "Psíquico 🔮", "fraq": "Metal ⚙️", "res": "Nenhuma", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/SFA/SFA_038_R_EN_PNG.png"},

    # --- DECK CHARIZARD EX (Escuridão/Fogo) ---
    "Charizard ex": {"hp": 330, "tipo": "Escuridão 🌑", "fraq": "Planta 🌿", "res": "Nenhuma", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/OBF/OBF_125_R_EN_PNG.png"},
    "Charmeleon": {"hp": 90, "tipo": "Fogo 🔥", "fraq": "Água 💧", "res": "Nenhuma", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/OBF/OBF_027_R_EN_PNG.png"},
    "Charmander": {"hp": 70, "tipo": "Fogo 🔥", "fraq": "Água 💧", "res": "Nenhuma", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/OBF/OBF_026_R_EN_PNG.png"},
    "Pidgeot ex": {"hp": 280, "tipo": "Sem Cor ⚪", "fraq": "Elétrico ⚡", "res": "Luta 👊", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/OBF/OBF_164_R_EN_PNG.png"},
    "Pidgeotto": {"hp": 90, "tipo": "Sem Cor ⚪", "fraq": "Elétrico ⚡", "res": "Luta 👊", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/OBF/OBF_163_R_EN_PNG.png"},
    "Pidgey": {"hp": 60, "tipo": "Sem Cor ⚪", "fraq": "Elétrico ⚡", "res": "Luta 👊", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/OBF/OBF_162_R_EN_PNG.png"},
    "Moltres": {"hp": 120, "tipo": "Fogo 🔥", "fraq": "Água 💧", "res": "Nenhuma", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/BRS/BRS_021_R_EN_PNG.png"},

    # --- DECK GARDEVOIR EX (Psíquico) ---
    "Gardevoir ex": {"hp": 310, "tipo": "Psíquico 🔮", "fraq": "Escuridão 🌑", "res": "Luta 👊", "img": "https://repositorio.sbrauble.com/arquivos/in/pokemon_bkp/cd/343/1640s_086.jpg"},
    "Kirlia": {"hp": 80, "tipo": "Psíquico 🔮", "fraq": "Escuridão 🌑", "res": "Luta 👊", "img": "https://repositorio.sbrauble.com/arquivos/in/pokemon_bkp/cd/286/75s_068.jpg"},
    "Ralts": {"hp": 60, "tipo": "Psíquico 🔮", "fraq": "Escuridão 🌑", "res": "Luta 👊", "img": "https://repositorio.sbrauble.com/arquivos/in/pokemon_bkp/cd/286/74s_067.jpg"},
    "Drifloon": {"hp": 70, "tipo": "Psíquico 🔮", "fraq": "Escuridão 🌑", "res": "Luta 👊", "img": "https://repositorio.sbrauble.com/arquivos/in/pokemon_bkp/cd/343/393s_089.jpg"},
    "Cresselia": {"hp": 120, "tipo": "Psíquico 🔮", "fraq": "Escuridão 🌑", "res": "Luta 👊", "img": "https://repositorio.sbrauble.com/arquivos/in/pokemon_bkp/cd/278/149s_074.jpg"},
    "Mew ex": {"hp": 180, "tipo": "Psíquico 🔮", "fraq": "Escuridão 🌑", "res": "Luta 👊", "img": "https://repositorio.sbrauble.com/arquivos/in/pokemon_bkp/cd/411/476s_151.jpg"},
    "Radiant Greninja": {"hp": 130, "tipo": "Água 💧", "fraq": "Elétrico ⚡", "res": "Nenhuma", "img": "https://repositorio.sbrauble.com/arquivos/in/pokemon_bkp/cd/526/65a992bc19258-8xsro-px0ed-b30a9be639100643633b71d0a31c115c.jpg"},
}

# --- 2. CLASSE POKEMON ---
class Pokemon:
    def __init__(self, nome, hp_max, tipo, fraqueza, resistencia, imagem_url=""):
        self.nome = nome
        self.hp_max = int(hp_max)
        self.hp_atual = int(hp_max)
        
        # --- CORREÇÃO DA IMAGEM PADRÃO ---
        link_padrao = "https://upload.wikimedia.org/wikipedia/en/3/3b/Pokemon_Trading_Card_Game_cardback.jpg"
        self.imagem_url = imagem_url if imagem_url else link_padrao
        
        self.id_unico = datetime.datetime.now().timestamp() + random.random()
        
        self.tipo = tipo
        self.fraqueza = fraqueza
        self.resistencia = resistencia
        self.status = "Saudável"
        self.energias = {} 

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
        self.hp_max = int(novo_hp)
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
        # Adicionei 'premios' aqui
        st.session_state.Treinadores = {
            "Treinador 1": {"ativo": None, "banco": [], "descarte": [], "premios": 6},
            "Treinador 2": {"ativo": None, "banco": [], "descarte": [], "premios": 6}
        }
    if 'log' not in st.session_state:
        st.session_state.log = []
    if 'vencedor' not in st.session_state:
        st.session_state.vencedor = None

# Função de Log Atualizada (Com Cores)
def adicionar_log(mensagem, tipo="neutro"):
    hora = datetime.datetime.now().strftime("%H:%M")
    cor = "white"
    if tipo == "ataque": cor = "#ffcccb" 
    elif tipo == "energia": cor = "#fffacd" 
    elif tipo == "cura": cor = "#90ee90" 
    elif tipo == "ko": cor = "#ff4500" 
    
    st.session_state.log.insert(0, f"<div class='log-entry' style='color:{cor}'>[{hora}] {mensagem}</div>")

inicializar_jogo()

# --- 4. BARRA LATERAL (CONTROLE) ---
with st.sidebar:
    st.header("⚙️ Controle")
    
    # --- PLACAR ---
    st.subheader("🏆 Placar")
    c1, c2 = st.columns(2)
    p1 = st.session_state.Treinadores["Treinador 1"]["premios"]
    p2 = st.session_state.Treinadores["Treinador 2"]["premios"]
    c1.metric("Treinador 1", f"{p1} 🎴")
    c2.metric("Treinador 2", f"{p2} 🎴")
    
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

    # --- GERENCIADOR DE CARTAS ---
    st.subheader("➕ Gerenciar Cartas")
    
    dono = st.selectbox("Treinador:", ["Treinador 1", "Treinador 2"])
    
    # Seletor de Modo
    modo = st.radio("Modo de Criação:", ["📚 Pokedex (Automático)", "✍️ Manual (Customizado)"], horizontal=True)
    
    # Variáveis vazias para preencher
    nome_final = ""
    hp_final = 0
    tipo_final = ""
    fraq_final = ""
    res_final = ""
    img_final = ""
    
    # LÓGICA DO FORMULÁRIO
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
        # --- AQUI ESTÁ A OPÇÃO DE IMAGEM QUE VOCÊ QUERIA ---
        nome_final = st.text_input("Nome do Pokémon")
        hp_final = st.number_input("HP Máximo", value=60, step=10)
        
        # Campo para colar o link da imagem
        img_final = st.text_input("Cole o Link da Imagem aqui 👇")
        
        lista_tipos = ["Sem Cor ⚪", "Fogo 🔥", "Água 💧", "Planta 🌿", "Elétrico ⚡", "Psíquico 🔮", "Luta 👊", "Escuridão 🌑", "Metal ⚙️", "Dragão 🐉"]
        tipo_final = st.selectbox("Tipo", lista_tipos)
        fraq_final = st.selectbox("Fraqueza", lista_tipos)
        res_final = st.selectbox("Resistência", ["Nenhuma"] + lista_tipos)

    # Lógica de Evolução
    player_temp = st.session_state.Treinadores[dono]
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

    # Botão de Adicionar
    if st.button("✨ Criar Carta", type="primary"):
        if acao == "Novo Básico":
            if nome_final:
                novo = Pokemon(nome_final, hp_final, tipo_final, fraq_final, res_final, img_final)
                if destino == "Ativo" and player_temp['ativo'] is None:
                    player_temp['ativo'] = novo
                    adicionar_log(f"🆕 {nome_final} entrou como Ativo do {dono}.", "neutro")
                elif len(player_temp['banco']) < 5:
                    player_temp['banco'].append(novo)
                    adicionar_log(f"🆕 {nome_final} entrou no Banco do {dono}.", "neutro")
                else:
                    st.error("Sem espaço!")
                st.rerun()
            else:
                st.error("O Pokémon precisa de um nome!")
        
        elif acao == "Evoluir" and alvo_evolucao:
            # Lógica para achar quem está evoluindo
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
def checar_vitoria(nome_oponente):
    if st.session_state.Treinadores[nome_oponente]['premios'] <= 0: return True
    oponente = st.session_state.Treinadores[nome_oponente]
    if oponente['ativo'] is None and len(oponente['banco']) == 0: return True
    return False

def renderizar_mesa_jogador(nome_jogador):
    player = st.session_state.Treinadores[nome_jogador]
    
    cor_texto = "#89CFF0" if nome_jogador == "Treinador 1" else "#FF6961"
    border_color = "#89CFF0" if nome_jogador == "Treinador 1" else "#FF6961"
    
    nome_oponente = "Treinador 2" if nome_jogador == "Treinador 1" else "Treinador 1"
    player_oponente = st.session_state.Treinadores[nome_oponente]
    ativo_oponente = player_oponente['ativo'] 
    
    st.markdown(f"""
        <div style='background-color: rgba(0,0,0,0.5); padding: 5px; border-radius: 10px; text-align: center; margin-bottom: 10px; border: 2px solid {border_color};'>
            <h2 style='margin:0; color: {cor_texto};'>{nome_jogador.upper()}</h2>
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
            
            with col_infos:
                st.subheader(ativo.nome)
                st.progress(ativo.hp_atual / ativo.hp_max)
                st.write(f"HP: {ativo.hp_atual}/{ativo.hp_max}")
                
                if ativo.hp_atual == 0:
                    st.error("💀 NOCAUTEADO!")
                    if st.button("Enviar p/ Descarte 💀", key=f"ko_{ativo.id_unico}"):
                        player['descarte'].append(ativo)
                        player['ativo'] = None
                        adicionar_log(f"☠️ {ativo.nome} ({nome_jogador}) foi nocauteado!", "ko")
                        # Lógica de Prêmio
                        player_oponente['premios'] -= 1
                        adicionar_log(f"🏆 {nome_oponente} pegou uma carta prêmio!", "ko")
                        
                        if checar_vitoria(nome_jogador):
                            st.session_state.vencedor = nome_oponente
                        st.rerun()
                else:
                    novo_status = st.selectbox("Status", ["Saudável", "Envenenado 🧪", "Queimado 🔥", "Adormecido 💤", "Paralisado ⚡"], key=f"st_{ativo.id_unico}")
                    if novo_status != ativo.status:
                        ativo.status = novo_status
                        st.rerun()
                    
                    with st.popover("⚡ Energia"):
                        t1, t2 = st.tabs(["Ligar", "Tirar"])
                        with t1:
                            escolha = st.selectbox("Tipo", ["Fogo 🔥", "Água 💧", "Planta 🌿", "Elétrico ⚡", "Psíquico 🔮", "Luta 👊", "Escuridão 🌑", "Metal ⚙️"], key=f"add_e_{ativo.id_unico}")
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
    st.title("🏆 Arena Pokémon TCG 4.3")
    c1, c2 = st.columns(2)
    with c1: renderizar_mesa_jogador("Treinador 1")
    with c2: renderizar_mesa_jogador("Treinador 2")

    st.divider()
    st.subheader("📜 Log de Batalha")
    # Log com HTML
    log_html = "".join(st.session_state.log)
    st.markdown(f"<div style='max-height: 200px; overflow-y: auto; background-color: rgba(0,0,0,0.5); border-radius: 10px;'>{log_html}</div>", unsafe_allow_html=True)

