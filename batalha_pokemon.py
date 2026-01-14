import streamlit as st
import datetime
import random 

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="PokéBattle 2.2", page_icon="⚔️", layout="wide")

# --- 1. CLASSE POKEMON ---
class Pokemon:
    def __init__(self, nome, hp_max, imagem_url=""):
        self.nome = nome
        self.hp_max = int(hp_max)
        self.hp_atual = int(hp_max)
        self.imagem_url = imagem_url if imagem_url else "https://tcg.pokemon.com/assets/img/global/tcg-card-back-2x.jpg"
        self.id_unico = datetime.datetime.now().timestamp()

    def receber_dano(self, dano):
        self.hp_atual -= dano
        if self.hp_atual < 0: self.hp_atual = 0
        if self.hp_atual > self.hp_max: self.hp_atual = self.hp_max

# --- 2. GERENCIAMENTO DE ESTADO ---
def inicializar_jogo():
    if 'jogadores' not in st.session_state:
        # AGORA TEMOS A LISTA 'DESCARTE'
        st.session_state.jogadores = {
            "Jogador 1": {"ativo": None, "banco": [], "descarte": []},
            "Jogador 2": {"ativo": None, "banco": [], "descarte": []}
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
    
    st.subheader("🪙 Moeda")
    if st.button("Jogar Moeda"):
        resultado = random.choice(["CARA (Heads)", "COROA (Tails)"])
        adicionar_log(f"A moeda caiu em: {resultado}")
        st.success(f"Resultado: {resultado}")

    st.divider()

    st.subheader("➕ Novo Pokémon")
    with st.form("add_poke"):
        dono = st.selectbox("Para quem?", ["Jogador 1", "Jogador 2"])
        nome = st.text_input("Nome (ex: Charizard ex)")
        hp = st.number_input("HP Máximo", value=60, step=10)
        img = st.text_input("Link da Imagem (URL)")
        destino = st.radio("Colocar onde?", ["Automático", "Forçar no Banco"])
        
        btn_add = st.form_submit_button("Adicionar Carta")

        if btn_add and nome:
            novo_poke = Pokemon(nome, hp, img)
            player_data = st.session_state.jogadores[dono]
            
            if destino == "Forçar no Banco":
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
    player = st.session_state.jogadores[nome_jogador]
    cor = "blue" if nome_jogador == "Jogador 1" else "red"
    
    st.markdown(f":{cor}[**ÁREA DO {nome_jogador.upper()}**]")
    
    # --- ÁREA DO ATIVO ---
    ativo = player['ativo']
    if ativo:
        with st.container(border=True):
            col_img, col_infos = st.columns([1, 2])
            with col_img:
                st.image(ativo.imagem_url, use_container_width=True)
            
            with col_infos:
                st.subheader(ativo.nome)
                st.progress(ativo.hp_atual / ativo.hp_max)
                st.write(f"HP: **{ativo.hp_atual}** / {ativo.hp_max}")
                
                # --- LÓGICA DE ABATE + DESCARTE ---
                if ativo.hp_atual == 0:
                    st.error("💀 POKÉMON ABATIDO!")
                    if st.button("Enviar para o Descarte 🗑️", key=f"ko_{ativo.id_unico}"):
                        # 1. Adiciona na lista de descarte
                        player['descarte'].append(ativo)
                        # 2. Remove do ativo
                        player['ativo'] = None
                        adicionar_log(f"☠️ {ativo.nome} ({nome_jogador}) foi para o descarte!")
                        st.rerun()
                else:
                    c1, c2, c3 = st.columns(3)
                    if c1.button("💥 -10", key=f"d10_{ativo.id_unico}"):
                        ativo.receber_dano(10)
                        st.rerun()
                    if c2.button("🔥 -30", key=f"d30_{ativo.id_unico}"):
                        ativo.receber_dano(30)
                        st.rerun()
                    if c3.button("💣 -50", key=f"d50_{ativo.id_unico}"):
                        ativo.receber_dano(50)
                        st.rerun()
                    
                    if st.button("Recuar / Sair", key=f"recuar_{ativo.id_unico}"):
                        if len(player['banco']) > 0:
                            player['banco'].append(ativo)
                            player['ativo'] = None
                            adicionar_log(f"{ativo.nome} recuou para o banco.")
                        else:
                            player['ativo'] = None
                            adicionar_log(f"{ativo.nome} saiu do campo.")
                        st.rerun()
    else:
        st.info(f"Sem Pokémon Ativo.")

    # --- ÁREA DO BANCO ---
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
                        else:
                            st.toast("Já tem ativo!")
                    
                    if st.button("💔 -10", key=f"dano_banco_{poke.id_unico}"):
                        poke.receber_dano(10)
                        st.rerun()
    
    # --- ÁREA DO DESCARTE (NOVA) ---
    # Só aparece se tiver cartas lá
    if player['descarte']:
        with st.expander(f"🗑️ Ver Pilha de Descarte ({len(player['descarte'])})"):
            for carta in player['descarte']:
                # Mostra o nome e um ícone de caveira
                st.write(f"💀 {carta.nome}")

# --- 5. TELA PRINCIPAL ---
st.title("🏆 Arena Pokémon TCG")
c1, c2 = st.columns(2)
with c1: renderizar_mesa_jogador("Jogador 1")
with c2: renderizar_mesa_jogador("Jogador 2")

st.divider()
with st.expander("Histórico de Ações"):
    for log in st.session_state.log: st.text(log)