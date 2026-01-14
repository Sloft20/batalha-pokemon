import streamlit as st
import datetime
import random 

st.set_page_config(page_title="PokéBattle 2.4 (Treinador)", page_icon="🧪", layout="wide")

# --- 1. CLASSE POKEMON ---
class Pokemon:
    def __init__(self, nome, hp_max, imagem_url=""):
        self.nome = nome
        self.hp_max = int(hp_max)
        self.hp_atual = int(hp_max)
        self.imagem_url = imagem_url if imagem_url else "https://tcg.pokemon.com/assets/img/global/tcg-card-back-2x.jpg"
        self.id_unico = datetime.datetime.now().timestamp()
        
        # Memória de Status
        self.status = "Saudável" 

    def receber_dano(self, dano):
        self.hp_atual -= dano
        if self.hp_atual < 0: self.hp_atual = 0
        if self.hp_atual > self.hp_max: self.hp_atual = self.hp_max

    def aplicar_dano_status(self):
        dano = 0
        msg = ""
        
        if self.status == "Envenenado 🧪":
            dano = 10
            msg = f"{self.nome} sofreu 10 de veneno."
        elif self.status == "Queimado 🔥":
            dano = 20
            msg = f"{self.nome} sofreu 20 de queimadura."
            
        if dano > 0:
            self.receber_dano(dano)
            return msg
        return None

# --- 2. GERENCIAMENTO DE ESTADO ---
def inicializar_jogo():
    if 'Treinadores' not in st.session_state:
        st.session_state.Treinadores = {
            "Treinador 1": {"ativo": None, "banco": [], "descarte": []},
            "Treinador 2": {"ativo": None, "banco": [], "descarte": []}
        }
    if 'log' not in st.session_state:
        st.session_state.log = []

def adicionar_log(mensagem):
    hora = datetime.datetime.now().strftime("%H:%M")
    st.session_state.log.insert(0, f"[{hora}] {mensagem}")

inicializar_jogo()

# --- 3. BARRA LATERAL ---
with st.sidebar:
    st.header("⚙️ Controle da Mesa")
    
    # --- AQUI ESTÁ A MOEDA DE VOLTA! ---
    st.subheader("🪙 Moeda")
    if st.button("Jogar Moeda"):
        resultado = random.choice(["CARA (Heads)", "COROA (Tails)"])
        adicionar_log(f"A moeda caiu em: {resultado}")
        if "CARA" in resultado:
            st.success(f"Resultado: {resultado}")
        else:
            st.error(f"Resultado: {resultado}")
    
    st.divider()
    # -----------------------------------
    
    # Botão Mestre de Checkup
    st.info("Fim de Turno / Checkup")
    if st.button("☣️ Aplicar Danos de Status"):
        logs_status = []
        for nome_jog in ["Treinador 1", "Treinador 2"]:
            ativo = st.session_state.Treinadores[nome_jog]['ativo']
            if ativo:
                resultado = ativo.aplicar_dano_status()
                if resultado:
                    logs_status.append(resultado)
        
        if logs_status:
            for log in logs_status:
                adicionar_log(log)
            st.success("Danos de status aplicados!")
            st.rerun()
        else:
            st.toast("Ninguém tem status de dano.")

    st.divider()

    st.subheader("➕ Novo Pokémon")
    with st.form("add_poke"):
        dono = st.selectbox("Para quem?", ["Treinador 1", "Treinador 2"])
        nome = st.text_input("Nome (ex: Charizard ex)")
        hp = st.number_input("HP Máximo", value=60, step=10)
        img = st.text_input("Link da Imagem (URL)")
        destino = st.radio("Colocar onde?", ["Ativo", "Banco"])
        
        btn_add = st.form_submit_button("Adicionar Carta")

        if btn_add and nome:
            novo_poke = Pokemon(nome, hp, img)
            player_data = st.session_state.Treinadores[dono]
            
            if destino == "Banco":
                 if len(player_data['banco']) < 5:
                    player_data['banco'].append(novo_poke)
                    adicionar_log(f"{nome} entrou no Banco do {dono}.")
                 else:
                     st.error("Banco cheio!")
            else: 
                if player_data['ativo'] is None:
                    player_data['ativo'] = novo_poke
                    adicionar_log(f"{nome} é o novo Ativo do {dono}.")
                elif len(player_data['banco']) < 5:
                    player_data['banco'].append(novo_poke)
                    adicionar_log(f"{nome} entrou no Banco do {dono}.")
                else:
                    st.error("Mesa cheia!")
            st.rerun()

    if st.button("🗑️ Reiniciar Tudo", type="primary"):
        st.session_state.clear()
        st.rerun()

# --- 4. FUNÇÃO DE DESENHO ---
def renderizar_mesa_jogador(nome_jogador):
    player = st.session_state.Treinadores[nome_jogador]
    cor = "blue" if nome_jogador == "Treinador 1" else "red"
    
    # Busca oponente para ataque
    nome_oponente = "Treinador 2" if nome_jogador == "Treinador 1" else "Treinador 1"
    player_oponente = st.session_state.Treinadores[nome_oponente]
    ativo_oponente = player_oponente['ativo'] 
    
    st.markdown(f":{cor}[**ÁREA DO {nome_jogador.upper()}**]")
    
    # --- ÁREA DO ATIVO ---
    ativo = player['ativo']
    if ativo:
        with st.container(border=True):
            col_img, col_infos = st.columns([1, 2])
            with col_img:
                st.image(ativo.imagem_url, use_container_width=True)
                
                if ativo.status != "Saudável":
                    st.warning(f"Estado: {ativo.status}")
            
            with col_infos:
                st.subheader(ativo.nome)
                st.progress(ativo.hp_atual / ativo.hp_max)
                st.write(f"HP: **{ativo.hp_atual}** / {ativo.hp_max}")
                
                if ativo.hp_atual == 0:
                    st.error("💀 POKÉMON ABATIDO!")
                    if st.button("Enviar para o Descarte 🗑️", key=f"ko_{ativo.id_unico}"):
                        player['descarte'].append(ativo)
                        player['ativo'] = None
                        adicionar_log(f"☠️ {ativo.nome} ({nome_jogador}) foi para o descarte!")
                        st.rerun()
                else:
                    st.write("**Ações:**")
                    
                    # --- BOTÕES DE STATUS ---
                    lista_status = ["Saudável", "Envenenado 🧪", "Queimado 🔥", "Adormecido 💤", "Paralisado ⚡"]
                    index_atual = lista_status.index(ativo.status) if ativo.status in lista_status else 0
                    
                    novo_status = st.selectbox("Alterar Condição Especial:", lista_status, index=index_atual, key=f"status_{ativo.id_unico}")
                    
                    if novo_status != ativo.status:
                        ativo.status = novo_status
                        adicionar_log(f"{ativo.nome} agora está {novo_status}")
                        st.rerun()

                    st.divider()

                    # Ataque e Dano
                    col_atk_oponente, col_atk_self = st.columns(2)
                    with col_atk_oponente:
                        dano_ataque = st.number_input("Dano no Oponente", value=0, step=10, key=f"input_atk_{ativo.id_unico}")
                        if st.button("⚔️ ATACAR", key=f"btn_atk_{ativo.id_unico}", type="primary"):
                            if ativo_oponente is not None:
                                ativo_oponente.receber_dano(dano_ataque)
                                adicionar_log(f"⚔️ {ativo.nome} atacou {ativo_oponente.nome} ({dano_ataque})!")
                                st.rerun()
                            else:
                                st.error("Sem alvo!")

                    with col_atk_self:
                        c1, c2 = st.columns(2)
                        if c1.button("💥 Self-10", key=f"d10_{ativo.id_unico}"):
                            ativo.receber_dano(10)
                            st.rerun()
                        if c2.button("🏃 Recuar", key=f"recuar_{ativo.id_unico}"):
                            ativo.status = "Saudável" 
                            if len(player['banco']) > 0:
                                player['banco'].append(ativo)
                                player['ativo'] = None
                                adicionar_log(f"{ativo.nome} recuou e curou status.")
                            else:
                                player['ativo'] = None
                                adicionar_log(f"{ativo.nome} saiu.")
                            st.rerun()
    else:
        st.info(f"Sem Pokémon Ativo.")

    # --- BANCO E DESCARTE ---
    if player['banco']:
        with st.expander(f"Ver Banco ({len(player['banco'])})", expanded=True):
            cols_banco = st.columns(5)
            for i, poke in enumerate(player['banco']):
                with cols_banco[i]:
                    st.image(poke.imagem_url, caption=poke.nome, use_container_width=True)
                    st.caption(f"HP: {poke.hp_atual}")
                    if st.button("⬆️", key=f"promover_{poke.id_unico}"):
                        if player['ativo'] is None:
                            player['ativo'] = player['banco'].pop(i)
                            adicionar_log(f"{poke.nome} subiu para o Ativo.")
                            st.rerun()
                        else: st.toast("Já tem ativo!")
                    if st.button("💔 -10", key=f"dano_banco_{poke.id_unico}"):
                        poke.receber_dano(10)
                        st.rerun()
    
    if player['descarte']:
        with st.expander(f"🗑️ Descarte ({len(player['descarte'])})"):
            for carta in player['descarte']: st.write(f"💀 {carta.nome}")

# --- 5. TELA PRINCIPAL ---
st.title("🏆 Arena Pokémon TCG (Com Status)")
c1, c2 = st.columns(2)
with c1: renderizar_mesa_jogador("Treinador 1")
with c2: renderizar_mesa_jogador("Treinador 2")

st.divider()
with st.expander("Histórico de Ações"):
    for log in st.session_state.log: st.text(log)
