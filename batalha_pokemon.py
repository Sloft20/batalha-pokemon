import streamlit as st
import datetime
import random 
import re 
import json
import os
import pandas as pd

st.set_page_config(page_title="PokéBattle 35.0 (Bench Fix)", page_icon="⚔️", layout="wide")

# --- 0. CONFIGURAÇÃO VISUAL ---
def configurar_visual():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');

        html, body, [class*="css"] { font-family: 'Roboto', sans-serif; }
        [data-testid="stAppViewContainer"] { background-color: #0f172a; color: #f1f5f9; }
        [data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
        
        [data-testid="stSidebar"], div[data-testid="stVerticalBlockBorderWrapper"], div[data-testid="stExpander"] {
            background-color: #1e293b; border: 1px solid #334155; border-radius: 8px;
        }
        
        /* SELECTBOX COMPACTO */
        .stSelectbox div[data-baseweb="select"] > div {
            background-color: #0f172a !important; 
            color: #e2e8f0 !important; 
            border: 1px solid #475569 !important; 
            border-radius: 6px;
            font-size: 13px !important;
            min-height: 38px !important;
            height: 38px !important;
            padding-top: 0px !important;
            padding-bottom: 0px !important;
            display: flex;
            align-items: center;
        }
        .stSelectbox label {
            font-size: 12px !important;
            margin-bottom: 2px !important;
        }

        .stTextInput input, .stNumberInput input {
            background-color: #0f172a !important; color: #e2e8f0 !important; border: 1px solid #475569 !important; border-radius: 6px;
        }

        .stButton > button { border-radius: 6px; font-weight: 600; border: none !important; width: 100%; }
        
        /* Botões Topo */
        div[data-testid="stPopover"] > div > button, .turn-btn button {
            min-height: 45px !important; height: 45px !important; width: 100% !important;
            border-radius: 8px !important; font-size: 15px !important; margin-bottom: 5px !important;
        }
        div[data-testid="stPopover"] > div > button {
            background-color: #1e293b !important; border: 1px solid #475569 !important; color: #e2e8f0 !important;
        }
        div[data-testid="stPopover"] > div > button:hover { background-color: #334155 !important; }
        .turn-btn button { 
            background-color: #FFC107 !important; color: #0f172a !important; font-weight: bold !important; border: 1px solid #FFC107 !important;
        }
        .turn-btn button:hover { background-color: #FFD54F !important; }

        /* Botão Atacar */
        .atk-btn > button { 
            background-color: #FFC107 !important; color: #0f172a !important; font-weight: bold; 
            min-height: 45px !important; margin-top: 5px !important; width: 100% !important;
        }

        .menu-item button { background-color: #1e293b !important; border: 1px solid #475569 !important; min-height: 40px; }
        .btn-red > button { background-color: #EF4444 !important; color: white; }
        .game-btn > button { background-color: #334155 !important; color: white; }

        .log-container { font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #cbd5e1; padding: 4px 0; border-bottom: 1px solid #334155; }
        .tag-log { display: inline-block; padding: 1px 6px; border-radius: 4px; font-weight: bold; font-size: 10px; margin-right: 8px; width: 70px; text-align: center; }
        .tag-inicio { background-color: #22c55e; color: #0f172a; } .tag-turno { background-color: #3b82f6; color: #fff; } 
        .tag-ataque { background-color: #ef4444; color: #fff; } .tag-energia { background-color: #eab308; color: #0f172a; } 
        .tag-tool { background-color: #a855f7; color: #fff; } .tag-ko { background-color: #000; color: #ef4444; border: 1px solid #ef4444; } 
        .tag-status { background-color: #f97316; color: #fff; }

        .rank-card { background-color: #0f172a; border: 1px solid #334155; border-radius: 8px; padding: 15px; margin-bottom: 10px; }
        .rank-name { font-size: 16px; font-weight: bold; color: #f1f5f9; margin-bottom: 5px; }
        .rank-stats { font-size: 12px; color: #94a3b8; margin-bottom: 8px; }
        .rank-bar-bg { width: 100%; height: 6px; background-color: #334155; border-radius: 3px; }
        .rank-bar-fill { height: 100%; border-radius: 3px; }
        
        .main-title { font-size: 26px; font-weight: 800; color: #f1f5f9; line-height: 1.2; }
        .turn-display { font-size: 16px; font-weight: bold; color: #FFC107; margin-bottom: 10px; }
        .hp-bar-bg { width: 100%; background-color: #334155; border-radius: 4px; height: 10px; margin-bottom: 15px; display: block; }
        .hp-fill { height: 100%; border-radius: 6px; transition: width 0.6s ease-in-out; }
        div[data-testid="column"] { display: flex; flex-direction: column; justify-content: center; }
        
        /* ENERGIAS (CARTAS) */
        .energy-container {
            display: flex; flex-wrap: wrap; gap: 3px; justify-content: center;
            background-color: rgba(15, 23, 42, 0.6); padding: 6px; border-radius: 20px;
            margin-top: 6px; border: 1px solid #334155; min-height: 32px;
        }
        .energy-icon { width: 16px; height: 16px; filter: drop-shadow(0px 1px 1px rgba(0,0,0,0.6)); transition: transform 0.2s; }
        .energy-icon:hover { transform: scale(1.2); }
        
        .stats-box {
            display: flex; justify-content: space-between; align-items: center;
            font-size: 11px; color: #94a3b8; background: #0f172a; padding: 4px 8px; 
            border-radius: 4px; border: 1px solid #334155; margin-top: 8px;
        }
        .recuo-img { width: 14px; vertical-align: middle; margin-left: 1px; }
    </style>
    """, unsafe_allow_html=True)

configurar_visual()

# --- 1. DADOS ---
ENERGY_IMGS = {
    "Planta 🌱": "https://archives.bulbagarden.net/media/upload/thumb/2/2e/Grass-attack.png/20px-Grass-attack.png",
    "Fogo 🔥": "https://archives.bulbagarden.net/media/upload/thumb/a/ad/Fire-attack.png/20px-Fire-attack.png",
    "Água 💧": "https://archives.bulbagarden.net/media/upload/thumb/1/11/Water-attack.png/20px-Water-attack.png",
    "Elétrico ⚡": "https://archives.bulbagarden.net/media/upload/thumb/0/04/Lightning-attack.png/20px-Lightning-attack.png",
    "Psíquico 🌀": "https://archives.bulbagarden.net/media/upload/thumb/e/ef/Psychic-attack.png/20px-Psychic-attack.png",
    "Luta 🥊": "https://archives.bulbagarden.net/media/upload/thumb/4/48/Fighting-attack.png/20px-Fighting-attack.png",
    "Escuridão 🌙": "https://archives.bulbagarden.net/media/upload/thumb/a/ab/Darkness-attack.png/20px-Darkness-attack.png",
    "Metal ⚙️": "https://archives.bulbagarden.net/media/upload/thumb/6/64/Metal-attack.png/20px-Metal-attack.png",
    "Incolor ⭐": "https://archives.bulbagarden.net/media/upload/thumb/1/1d/Colorless-attack.png/20px-Colorless-attack.png"
}

POKEDEX = POKEDEX = {
    ##-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------##
    ##                                                                                 DECK DE DRAGAPULT EX
    ##-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------##
    "Dragapult ex": {"hp": 320, "tipo": "Dragão 🐉", "fraq": "Nenhuma", "res": "Nenhuma", "recuo": 1, "img": "https://dz3we2x72f7ol.cloudfront.net/expansions/prismatic-evolutions/pt-br/SV8pt5_PTBR_73.png"},
    "Drakloak": {"hp": 90, "tipo": "Dragão 🐉", "fraq": "Nenhuma", "res": "Nenhuma", "recuo": 1, "hab": "Ordem De Reconhecimento", "img": "https://dz3we2x72f7ol.cloudfront.net/expansions/prismatic-evolutions/pt-br/SV8pt5_PTBR_72.png"},
    "Dreepy": {"hp": 70, "tipo": "Dragão 🐉", "fraq": "Nenhuma", "res": "Nenhuma", "recuo": 1, "img": "https://dz3we2x72f7ol.cloudfront.net/expansions/prismatic-evolutions/pt-br/SV8pt5_PTBR_71.png"},
    "Duskull": {"hp": 60, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "recuo": 1, "img": "https://dz3we2x72f7ol.cloudfront.net/expansions/prismatic-evolutions/pt-br/SV8pt5_PTBR_35.png"},
    "Dusclops": {"hp": 90, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "recuo": 1, "hab":"Explosão Maldita", "img": "https://dz3we2x72f7ol.cloudfront.net/expansions/prismatic-evolutions/pt-br/SV8pt5_PTBR_36.png"},
    "Munkidori": {"hp": 110, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "recuo": 1, "hab":"Adrena-cérebro", "img": "https://dz3we2x72f7ol.cloudfront.net/expansions/prismatic-evolutions/pt-br/SV8pt5_PTBR_44.png"},
    "Budew": {"hp": 30, "tipo": "Planta 🌱", "fraq": "Fogo 🔥", "res": "", "recuo": 0, "hab":"Comichão De Pólen", "img": "https://dz3we2x72f7ol.cloudfront.net/expansions/prismatic-evolutions/pt-br/SV8pt5_PTBR_4.png"},
    "Fezandipiti ex": {"hp": 210, "tipo": "Psíquico 🌀", "fraq": "Metal ⚙️", "res": "Nenhuma", "recuo": 1, "hab": "Virar o Jogo", "img": "https://dz3we2x72f7ol.cloudfront.net/expansions/shrouded-fable/pt-br/SV6pt5_PTBR_38.png"},
    ##-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------##
    ##                                                                                 DECK DE CHARIZARD EX
    ##-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------##
    "Charizard ex": {"hp": 330, "tipo": "Escuridão 🌙", "fraq": "Planta 🌱", "res": "Nenhuma", "recuo": 2, "hab": "Reino Infernal", "img": "https://dz3we2x72f7ol.cloudfront.net/expansions/obsidian-flames/pt-br/SV03_PTBR_125.png"},
    "Charmeleon": {"hp": 90, "tipo": "Fogo 🔥", "fraq": "Água 💧", "res": "Nenhuma", "recuo": 2, "hab": "Véu De Chamas", "img": "https://dz3we2x72f7ol.cloudfront.net/expansions/paldean-fates/pt-br/SV4pt5_PTBR_8.png"},
    "Charmander": {"hp": 70, "tipo": "Fogo 🔥", "fraq": "Água 💧", "res": "Nenhuma", "recuo": 1, "img": "https://dz3we2x72f7ol.cloudfront.net/expansions/paldean-fates/pt-br/SV4pt5_PTBR_7.png"},
    "Pidgeot ex": {"hp": 280, "tipo": "Normal ⚪", "fraq": "Elétrico ⚡", "res": "Luta 🥊", "recuo": 0, "hab": "Busca Rápida", "img": "https://dz3we2x72f7ol.cloudfront.net/expansions/obsidian-flames/pt-br/SV03_PTBR_164.png"},
    "Pidgeotto": {"hp": 80, "tipo": "Normal ⚪", "fraq": "Elétrico ⚡", "res": "Luta 🥊", "recuo": 0, "img": "https://dz3we2x72f7ol.cloudfront.net/expansions/151/pt-br/SV3pt5_PTBR_17.png"},
    "Pidgey": {"hp": 60, "tipo": "Normal ⚪", "fraq": "Elétrico ⚡", "res": "Luta 🥊", "recuo": 0, "hab": "Chamar a Família", "img": "https://dz3we2x72f7ol.cloudfront.net/expansions/151/pt-br/SV3pt5_PTBR_16.png"},
    "Moltres": {"hp": 120, "tipo": "Fogo 🔥", "fraq": "Elétrico ⚡", "res": "Luta 🥊", "recuo": 2, "hab": "Chamas á Deriva", "img": "https://dz3we2x72f7ol.cloudfront.net/expansions/151/pt-br/SV3pt5_PTBR_146.png"},
    ##-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------##
    ##                                                                                 DECK DE GARDEVOIR EX
    ##-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------##
    "Gardevoir ex": {"hp": 310, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "recuo": 2, "hab": "Abraço Psíquico", "img": "https://dz3we2x72f7ol.cloudfront.net/expansions/scarlet-violet/pt-br/SV01_PTBR_86.png"},
    "Kirlia": {"hp": 80, "tipo": "Psíquico 🌀", "fraq": "Metal ⚙️", "res": "Luta 🥊", "recuo": 2, "hab": "Requinte", "img": "https://assets.pokemon.com/static-assets/content-assets/cms2-pt-br/img/cards/web/SWSH12/SWSH12_PT-BR_68.png"},
    "Ralts": {"hp": 60, "tipo": "Psíquico 🌀", "fraq": "Metal ⚙️", "res": "", "recuo": 1, "img": "https://assets.pokemon.com/static-assets/content-assets/cms2-pt-br/img/cards/web/SWSH12/SWSH12_PT-BR_67.png"},
    "Drifloon": {"hp": 70, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "recuo": 1, "img": "https://assets.pokemon.com/static-assets/content-assets/cms2-pt-br/img/cards/web/SV01/SV01_PT-BR_89.png"},
    "Mew ex": {"hp": 180, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "recuo": 1, "hab": "Recomeçar", "img": "https://dz3we2x72f7ol.cloudfront.net/expansions/151/pt-br/SV3pt5_PTBR_151.png"},
    "Radiant Greninja": {"hp": 130, "tipo": "Água 💧", "fraq": "Elétrico ⚡", "res": "Nenhuma", "recuo": 1, "hab": "Cartas Na Manga", "img": "https://assets.pokemon.com/static-assets/content-assets/cms2-pt-br/img/cards/web/SWSH10/SWSH10_PT-BR_46.png"},
    "Fezandipiti": {"hp": 120, "tipo": "Psíquico 🌀", "fraq": "Metal ⚙️", "res": "Nenhuma", "recuo": 1, "hab": "Adrena-Feromônio", "img": "https://dz3we2x72f7ol.cloudfront.net/expansions/prismatic-evolutions/pt-br/SV8pt5_PTBR_45.png"},
    "Yamask": {"hp": 70, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "recuo": 2, "img": "https://assets.pokemon.com/static-assets/content-assets/cms2-pt-br/img/cards/web/RSV10PT5/RSV10PT5_PT-BR_39.png"},
    "Cofagrius": {"hp": 120, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "recuo": 2, "img": "https://assets.pokemon.com/static-assets/content-assets/cms2-pt-br/img/cards/web/RSV10PT5/RSV10PT5_PT-BR_40.png"},
    "Frilish": {"hp": 80, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "recuo": 3, "img": "https://assets.pokemon.com/static-assets/content-assets/cms2-pt-br/img/cards/web/RSV10PT5/RSV10PT5_PT-BR_44.png"},
    ##-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------##
    ##                                                                                 DECK DE LUGIA VSTAR
    ##-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------##
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

HISTORY_FILE = "historico.json"
LISTA_DECKS = ["Charizard ex", "Dragapult ex", "Lugia VSTAR", "Gardevoir ex", "Raging Bolt ex", "Iron Thorns ex", "Outro"]

def carregar_historico():
    if not os.path.exists(HISTORY_FILE): return []
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except: return []

def salvar_partida(vencedor, perdedor, deck_venc, deck_perd, log_partida):
    hist = carregar_historico()
    partida = {
        "data": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "vencedor": vencedor,
        "perdedor": perdedor,
        "deck_vencedor": deck_venc,
        "deck_perdedor": deck_perd,
        "log": log_partida 
    }
    hist.append(partida)
    with open(HISTORY_FILE, "w") as f: json.dump(hist, f)

def calcular_stats():
    dados = carregar_historico()
    if not dados: return None, None, dados 
    stats_jog = {}; stats_deck = {}
    for d in dados:
        v, p = d['vencedor'], d['perdedor']
        if v not in stats_jog: stats_jog[v] = {'p':0, 'v':0}
        if p not in stats_jog: stats_jog[p] = {'p':0, 'v':0}
        stats_jog[v]['p'] += 1; stats_jog[v]['v'] += 1; stats_jog[p]['p'] += 1
        dv, dp = d['deck_vencedor'], d['deck_perdedor']
        if dv not in stats_deck: stats_deck[dv] = {'p':0, 'v':0}
        if dp not in stats_deck: stats_deck[dp] = {'p':0, 'v':0}
        stats_deck[dv]['p'] += 1; stats_deck[dv]['v'] += 1; stats_deck[dp]['p'] += 1
    df_jog = pd.DataFrame.from_dict(stats_jog, orient='index').reset_index()
    df_jog.columns = ['Nome', 'Partidas', 'Vitorias']
    df_jog['Winrate'] = (df_jog['Vitorias'] / df_jog['Partidas']) * 100
    df_jog = df_jog.sort_values(by=['Vitorias', 'Winrate'], ascending=False)
    df_deck = pd.DataFrame.from_dict(stats_deck, orient='index').reset_index()
    df_deck.columns = ['Deck', 'Partidas', 'Vitorias']
    df_deck['Winrate'] = (df_deck['Vitorias'] / df_deck['Partidas']) * 100
    df_deck = df_deck.sort_values(by=['Vitorias', 'Winrate'], ascending=False)
    return df_jog, df_deck, dados

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

    def receber_dano(self, dano):
        self.hp_atual -= dano
        if self.hp_atual < 0: self.hp_atual = 0
        if self.hp_atual > self.hp_max: self.hp_atual = self.hp_max

    def resolver_checkup(self):
        logs = []
        if self.status == "Envenenado 🧪": self.receber_dano(10); logs.append(f"🧪 {self.nome} sofreu 10 de veneno.")
        elif self.status == "Queimado 🔥":
            self.receber_dano(20); logs.append(f"🔥 {self.nome} sofreu 20 de queimadura.")
            if random.choice(["CARA", "COROA"]) == "CARA": self.status = "Saudável"; logs.append(f"🪙 {self.nome} curou queimadura!")
            else: logs.append(f"🪙 {self.nome} continua queimado.")
        elif self.status == "Adormecido 💤":
            if random.choice(["CARA", "COROA"]) == "CARA": self.status = "Saudável"; logs.append(f"🪙 {self.nome} acordou!")
            else: logs.append(f"🪙 {self.nome} dormindo.")
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
        if tipo in self.energias:
            self.energias[tipo] -= 1
            if self.energias[tipo] <= 0: del self.energias[tipo]
            return True
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
        return False, f"Falta energia ({total}/{custo})."

def gerar_html_energia(energias_dict):
    if not energias_dict: return "<div class='energy-container' style='opacity:0'>.</div>"
    html = "<div class='energy-container'>"
    for tipo_chave, qtd in energias_dict.items():
        img_url = ENERGY_IMGS.get(tipo_chave, "")
        if img_url:
            for _ in range(qtd):
                html += f"<img src='{img_url}' class='energy-icon' title='{tipo_chave}'>"
        else:
            html += f"<span style='font-size:12px; margin:0 2px;'>{tipo_chave} x{qtd}</span>"
    html += "</div>"
    return html

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
    if 'dmg_buffer' not in st.session_state: st.session_state.dmg_buffer = {}
    if 'tela_ranking' not in st.session_state: st.session_state.tela_ranking = False

def adicionar_log(cat, msg, player=None):
    hora = datetime.datetime.now().strftime("%H:%M")
    css_class = {"Inicio": "tag-inicio", "Turno": "tag-turno", "Ataque": "tag-ataque", "Energia": "tag-energia", "Tool": "tag-tool", "KO": "tag-ko", "Status": "tag-status", "Moeda": "tag-tool"}.get(cat, "tag-log")
    prefixo = f"<b>{player}</b>: " if player else ""
    st.session_state.log.insert(0, f"<div class='log-container'><span style='color:#64748b;margin-right:8px'>[{hora}]</span><span class='tag-log {css_class}'>{cat}</span><span>{prefixo}{msg}</span></div>")

inicializar_jogo()

if st.session_state.tela_ranking:
    st.markdown('<div class="main-title">🏆 Ranking</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 5])
    with c1:
        st.markdown('<div class="menu-item">', unsafe_allow_html=True)
        if st.button("Voltar", icon=":material/arrow_back:", use_container_width=True): st.session_state.tela_ranking = False; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="btn-red">', unsafe_allow_html=True)
        if st.button("Resetar", icon=":material/delete_forever:", use_container_width=True):
            if os.path.exists(HISTORY_FILE): os.remove(HISTORY_FILE); st.toast("Resetado!"); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    df_jog, df_deck, dados_brutos = calcular_stats()
    
    if df_jog is not None and not df_jog.empty:
        c_jog, c_dck = st.columns(2)
        with c_jog:
            st.markdown(f"### 👤 Jogadores ({len(df_jog)})")
            for index, row in df_jog.iterrows():
                cor = "#22c55e" if row['Winrate'] >= 50 else ("#eab308" if row['Winrate'] >= 30 else "#ef4444")
                st.markdown(f"""<div class="rank-card"><div class="rank-name">#{index+1} {row['Nome']}</div><div class="rank-stats">P: {row['Partidas']} • V: {row['Vitorias']} • {row['Winrate']:.1f}%</div><div class="rank-bar-bg"><div class="rank-bar-fill" style="width:{row['Winrate']}%; background-color:{cor};"></div></div></div>""", unsafe_allow_html=True)
        with c_dck:
            st.markdown(f"### 🃏 Decks ({len(df_deck)})")
            for index, row in df_deck.iterrows():
                cor = "#3b82f6" if row['Winrate'] >= 50 else "#64748b"
                st.markdown(f"""<div class="rank-card"><div class="rank-name">{row['Deck']}</div><div class="rank-stats">V: {row['Vitorias']} / P: {row['Partidas']}</div><div class="rank-bar-bg"><div class="rank-bar-fill" style="width:{row['Winrate']}%; background-color:{cor};"></div></div></div>""", unsafe_allow_html=True)
        
        st.divider()
        st.markdown("### 📜 Histórico de Partidas")
        if dados_brutos:
            for p in reversed(dados_brutos):
                with st.expander(f"{p['data']} - 🏆 {p['vencedor']} (vs {p['perdedor']})"):
                    st.markdown(f"**Decks:** {p['deck_vencedor']} vs {p['deck_perdedor']}")
                    if 'log' in p and p['log']:
                        st.markdown("---")
                        st.markdown("".join(p['log']), unsafe_allow_html=True)
                    else: st.caption("Log detalhado não disponível.")
    else: st.info("Sem dados ainda.")

else:
    c_title, c_spacer, c_buttons = st.columns([2, 1, 1.2])
    with c_title:
        st.markdown('<div class="main-title">⚔️ PokéBattle</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="turn-display">👉 {st.session_state.Treinadores[st.session_state.turno_atual]["nome"]}</div>', unsafe_allow_html=True)

    with c_buttons:
        with st.popover("Menu", icon=":material/menu:", use_container_width=True):
            st.markdown('<div class="menu-item">', unsafe_allow_html=True)
            if st.button("Placar", icon=":material/leaderboard:", use_container_width=True): st.session_state.tela_ranking = True; st.rerun()
            if st.button("Moeda", icon=":material/casino:", use_container_width=True): r = random.choice(["CARA", "COROA"]); st.toast(f"{r}"); adicionar_log("Moeda", f"Resultado: {r}")
            if st.session_state.log:
                txt = "\n".join([re.sub('<[^<]+?>', '', l) for l in st.session_state.log[::-1]])
                st.download_button("Baixar Log", txt, "log.txt", icon=":material/download:", use_container_width=True)
            if st.button("Reset Jogo", icon=":material/restart_alt:", use_container_width=True): st.session_state.clear(); st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
        st.markdown('<div class="turn-btn">', unsafe_allow_html=True)
        if st.button("Fim Turno", icon=":material/skip_next:", use_container_width=True):
            logs_check = []
            for p in ["Treinador 1", "Treinador 2"]:
                if st.session_state.Treinadores[p]['ativo']:
                    r = st.session_state.Treinadores[p]['ativo'].resolver_checkup(); logs_check.extend(r)
            for l in logs_check: adicionar_log("Status", l)
            st.session_state.habilidades_usadas = []
            ant = st.session_state.turno_atual
            novo = "Treinador 2" if ant == "Treinador 1" else "Treinador 1"
            st.session_state.turno_atual = novo
            adicionar_log("Turno", f"Início de {st.session_state.Treinadores[novo]['nome']}.")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    with st.sidebar:
        st.header("⚙️ Configuração")
        with st.expander("👤 Jogadores", expanded=True):
            n1 = st.text_input("J1", value=st.session_state.Treinadores["Treinador 1"]["nome"])
            d1 = st.selectbox("Deck J1", LISTA_DECKS, index=0)
            st.divider()
            n2 = st.text_input("J2", value=st.session_state.Treinadores["Treinador 2"]["nome"])
            d2 = st.selectbox("Deck J2", LISTA_DECKS, index=1)
            if st.button("Salvar", icon=":material/save:", type="primary"):
                st.session_state.Treinadores["Treinador 1"]["nome"] = n1; st.session_state.Treinadores["Treinador 1"]["deck"] = d1
                st.session_state.Treinadores["Treinador 2"]["nome"] = n2; st.session_state.Treinadores["Treinador 2"]["deck"] = d2; st.rerun()
        
        st.markdown("### ➕ Cartas")
        dono_key = st.selectbox("Treinador", ["Treinador 1", "Treinador 2"], format_func=lambda x: st.session_state.Treinadores[x]['nome'])
        player = st.session_state.Treinadores[dono_key]
        acao = st.radio("Ação", ["Novo Básico", "Evoluir"], horizontal=True)
        
        if acao == "Novo Básico":
            escolha = st.selectbox("Pokémon", list(POKEDEX.keys())); dados = POKEDEX[escolha]; st.image(dados["img"], width=80)
            local = st.radio("Local", ["Banco", "Ativo"], horizontal=True)
            if st.button("Adicionar", icon=":material/add_circle:"):
                novo = Pokemon(escolha, dados["hp"], dados["tipo"], dados["fraq"], dados["res"], dados.get("recuo", 1), dados["img"], dados.get("hab"))
                if local == "Ativo":
                    if not player['ativo']: 
                        adicionar_log("Inicio", f"Colocou {escolha} como Ativo.", player['nome'])
                        player['ativo'] = novo 
                        st.rerun()
                    else: st.error("Ocupado!")
                elif local == "Banco":
                    if len(player['banco']) < 5: 
                        adicionar_log("Inicio", f"Colocou {escolha} no Banco.", player['nome'])
                        player['banco'].append(novo) 
                        st.rerun()
                    else: st.error("Banco Cheio!")
        
        elif acao == "Evoluir":
            opcoes = []
            if player['ativo']: opcoes.append(f"[Ativo] {player['ativo'].nome}")
            for i, p in enumerate(player['banco']): opcoes.append(f"[Banco {i+1}] {p.nome}")
            if opcoes:
                alvo_str = st.selectbox("Quem?", opcoes); escolha_evo = st.selectbox("Evoluir Para", list(POKEDEX.keys()))
                if st.button("Evoluir", icon=":material/upgrade:"):
                    d = POKEDEX[escolha_evo]
                    obj = player['ativo'] if "[Ativo]" in alvo_str else player['banco'][int(alvo_str.split("]")[0].split(" ")[1])-1]
                    obj.evoluir_para(escolha_evo, d["hp"], d["tipo"], d["fraq"], d["res"], d.get("recuo",1), d["img"], d.get("hab"))
                    adicionar_log("Energia", f"{obj.nome} evoluiu!", player['nome'])
                    st.rerun()

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
        c_h1.markdown(f"<h4 style='margin:0'>{p['nome']} <span style='font-size:12px;color:#94a3b8'>({p['deck']})</span></h4>", unsafe_allow_html=True)
        c_h2.markdown(f"<h5 style='margin:0; text-align:right'>{p['premios']} 🎴</h5>", unsafe_allow_html=True)
        
        ativo = p['ativo']
        if ativo:
            st.markdown("---")
            c_img, c_info = st.columns([1, 1.8])
            with c_img:
                st.image(ativo.imagem_url, use_container_width=True)
                if ativo.status != "Saudável": st.warning(ativo.status)
                st.markdown(gerar_html_energia(ativo.energias), unsafe_allow_html=True)
                if ativo.ferramenta != "Nenhuma": st.caption(f"🛠️ {ativo.ferramenta}")

            with c_info:
                nome_disp = f'<span style="color:#FFD700; text-shadow: 0 0 5px rgba(255, 215, 0, 0.6);">★ {ativo.nome}</span>' if any(x in ativo.nome.lower() for x in ["ex", "v", "vstar"]) else f"**{ativo.nome}**"
                st.markdown(f"{nome_disp} <span style='float:right; font-size:12px;'>{ativo.hp_atual}/{ativo.hp_max}</span>", unsafe_allow_html=True)
                pct = max(0, min(100, (ativo.hp_atual / ativo.hp_max) * 100))
                color_hp = "#22c55e" if pct > 50 else ("#eab308" if pct > 20 else "#ef4444")
                st.markdown(f"""<div class="hp-bar-bg"><div class="hp-fill" style="width:{pct}%; background-color:{color_hp};"></div></div>""", unsafe_allow_html=True)
                
                # --- STATS BOX (COM RECUO VISUAL) ---
                if ativo.recuo > 0:
                    recuo_html = ""
                    img_recuo = ENERGY_IMGS["Incolor ⭐"]
                    for _ in range(ativo.recuo):
                        recuo_html += f"<img src='{img_recuo}' class='recuo-img'>"
                else:
                    recuo_html = "Livre"

                stats_html = f"""
                <div class="stats-box">
                    <span>⚔️ {ativo.fraqueza}</span>
                    <span>🛡️ {ativo.resistencia}</span>
                    <span>🦶 {recuo_html}</span>
                </div>
                """
                st.markdown(stats_html, unsafe_allow_html=True)

                if ativo.hp_atual == 0:
                    st.error("💀 NOCAUTEADO")
                    st.markdown('<div class="btn-red">', unsafe_allow_html=True)
                    if st.button("Enviar p/ Descarte", icon=":material/delete:", key=f"ko_{ativo.id_unico}"):
                        p['descarte'].append(ativo); p['ativo'] = None; 
                        adicionar_log("KO", f"💀 {ativo.nome} caiu!", p['nome'])
                        op_key = "Treinador 2" if key == "Treinador 1" else "Treinador 1"
                        st.session_state.Treinadores[op_key]['premios'] -= 2 if "ex" in ativo.nome.lower() else 1
                        if checar_vitoria(key):
                            st.session_state.vencedor = st.session_state.Treinadores[op_key]['nome']
                            salvar_partida(st.session_state.Treinadores[op_key]['nome'], p['nome'], st.session_state.Treinadores[op_key]['deck'], p['deck'], list(st.session_state.log))
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    if ativo.id_unico not in st.session_state.dmg_buffer: st.session_state.dmg_buffer[ativo.id_unico] = 0
                    dmg = st.number_input("Dano do ataque", value=st.session_state.dmg_buffer[ativo.id_unico], step=10, key=f"d_{ativo.id_unico}", label_visibility="collapsed")
                    st.session_state.dmg_buffer[ativo.id_unico] = dmg

                    st.markdown('<div class="atk-btn">', unsafe_allow_html=True)
                    if st.button("ATACAR", icon=":material/swords:", key=f"atk_{ativo.id_unico}"):
                        op_key = "Treinador 2" if key == "Treinador 1" else "Treinador 1"
                        op = st.session_state.Treinadores[op_key]
                        if op['ativo']:
                            mult = 2 if ativo.tipo == op['ativo'].fraqueza else 1
                            red = 30 if ativo.tipo == op['ativo'].resistencia else 0
                            final = max(0, (dmg * mult) - red)
                            op['ativo'].receber_dano(final)
                            adicionar_log("Ataque", f"{ativo.nome} causou {final} em {op['ativo'].nome}.", p['nome'])
                            
                            logs_check = []
                            for p_chk in ["Treinador 1", "Treinador 2"]:
                                if st.session_state.Treinadores[p_chk]['ativo']:
                                    r = st.session_state.Treinadores[p_chk]['ativo'].resolver_checkup()
                                    if r: logs_check.extend(r)
                            for l in logs_check: adicionar_log("Status", l)

                            st.session_state.habilidades_usadas = []
                            ant = st.session_state.turno_atual
                            novo = "Treinador 2" if ant == "Treinador 1" else "Treinador 1"
                            st.session_state.turno_atual = novo
                            adicionar_log("Turno", f"Fim de turno (Ataque). Início de {st.session_state.Treinadores[novo]['nome']}.")
                            st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    with st.popover("Energia / Status / Tool", icon=":material/flash_on:"):
                        t1, t2, t3 = st.tabs(["Energia", "Status", "Tool"])
                        with t1:
                            # SELECTBOX
                            escolha_e = st.selectbox("Tipo", ["Fogo 🔥", "Água 💧", "Planta 🌱", "Elétrico ⚡", "Psíquico 🌀", "Luta 🥊", "Escuridão 🌙", "Metal ⚙️", "Incolor ⭐", "Dragão 🐉", "Fada 🧚"], key=f"ae_{ativo.id_unico}")
                            
                            # --- PREVIEW REDUZIDO (20px) ---
                            img_preview = ENERGY_IMGS.get(escolha_e)
                            if img_preview: st.image(img_preview, width=20)
                            
                            c1, c2 = st.columns(2)
                            with c1: 
                                if st.button("", icon=":material/add:", key=f"ba_{ativo.id_unico}"): 
                                    ativo.anexar_energia(escolha_e)
                                    adicionar_log("Energia", f"Ligou {escolha_e}", p['nome'])
                                    st.rerun()
                            with c2:
                                if st.button("", icon=":material/remove:", key=f"br_{ativo.id_unico}"): 
                                    ativo.remover_energia(escolha_e)
                                    adicionar_log("Energia", f"Removeu {escolha_e}", p['nome'])
                                    st.rerun()
                        with t2:
                            st.selectbox("Status", ["Saudável", "Envenenado 🧪", "Queimado 🔥", "Adormecido 💤", "Paralisado ⚡"], key=f"st_{ativo.id_unico}", on_change=lambda: setattr(ativo, 'status', st.session_state[f"st_{ativo.id_unico}"]))
                        with t3:
                            tl = st.selectbox("Tool", list(TOOLS_DB.keys()), key=f"tl_{ativo.id_unico}")
                            if st.button("Equipar", icon=":material/build:", key=f"btl_{ativo.id_unico}"): 
                                ativo.equipar_ferramenta(tl)
                                adicionar_log("Tool", f"Equipou {tl}", p['nome'])
                                st.rerun()

                    if ativo.habilidade:
                        ja = ativo.id_unico in st.session_state.habilidades_usadas
                        cls = "game-btn" if ja else "game-btn"
                        lbl = "✅ Hab Usada" if ja else f"✨ {ativo.habilidade}"
                        st.markdown(f'<div class="{cls}">', unsafe_allow_html=True)
                        if st.button(lbl, key=f"hab_{ativo.id_unico}", disabled=ja):
                            st.session_state.habilidades_usadas.append(ativo.id_unico)
                            adicionar_log("Tool", f"{ativo.nome} usou habilidade.", p['nome'])
                            st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    custo = ativo.recuo
                    if ativo.ferramenta == "Skate de Resgate (-1 Recuo)": custo = max(0, custo - 1)
                    if st.button(f"Recuar ({custo})", icon=":material/logout:", key=f"run_{ativo.id_unico}"):
                        pode, msg = ativo.tentar_recuar()
                        if pode:
                            if p['banco']: 
                                p['banco'].append(ativo); p['ativo'] = None; 
                                adicionar_log("Inicio", f"{ativo.nome} recuou.", p['nome'])
                                st.rerun()
                            else: st.warning("Banco vazio!")
                        else: st.error(msg)

        if p['banco']:
            st.markdown("---")
            cols = st.columns(max(5, len(p['banco'])))
            for i, bp in enumerate(p['banco']):
                with cols[i]:
                    st.image(bp.imagem_url, use_container_width=True)
                    st.markdown(f"<div style='text-align:center; font-size:11px; font-weight:bold; color:#cbd5e1; margin-top:-5px;'>HP: {bp.hp_atual}/{bp.hp_max}</div>", unsafe_allow_html=True)
                    st.markdown(gerar_html_energia(bp.energias), unsafe_allow_html=True)
                    
                    if bp.hp_atual == 0:
                        st.markdown('<div class="btn-red">', unsafe_allow_html=True)
                        if st.button("💀", key=f"ko_b_{bp.id_unico}"):
                            p['banco'].pop(i); p['descarte'].append(bp); 
                            adicionar_log("KO", f"💀 {bp.nome} (Banco) caiu!", p['nome'])
                            op_key = "Treinador 2" if key == "Treinador 1" else "Treinador 1"
                            st.session_state.Treinadores[op_key]['premios'] -= 2 if "ex" in bp.nome.lower() else 1
                            if checar_vitoria(key):
                                st.session_state.vencedor = st.session_state.Treinadores[op_key]['nome']
                                salvar_partida(st.session_state.Treinadores[op_key]['nome'], p['nome'], st.session_state.Treinadores[op_key]['deck'], p['deck'], list(st.session_state.log))
                            st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        c_up, c_dmg = st.columns(2)
                        with c_up: 
                            if st.button("⬆️", key=f"up_{bp.id_unico}"): 
                                if not p['ativo']: 
                                    adicionar_log("Inicio", f"{bp.nome} subiu para o Ativo.", p['nome'])
                                    p['ativo'] = p['banco'].pop(i)
                                    st.rerun()
                        with c_dmg: 
                            if st.button("💔", key=f"dmb_{bp.id_unico}"): bp.receber_dano(10); st.rerun()
                        
                        # --- POPOVER DO BANCO ATUALIZADO ---
                        with st.popover("⚡", icon=":material/flash_on:", use_container_width=True):
                            t1, t2, t3 = st.tabs(["Energia", "Status", "Tool"]) # NOMES CORRETOS
                            
                            with t1: # ABA ENERGIA
                                eb = st.selectbox("Tipo", ["Fogo 🔥", "Água 💧", "Planta 🌱", "Elétrico ⚡", "Psíquico 🌀", "Luta 🥊", "Escuridão 🌙", "Metal ⚙️", "Incolor ⭐", "Dragão 🐉", "Fada 🧚"], key=f"aeb_{bp.id_unico}")
                                
                                # PREVIEW NO BANCO (20px)
                                img_preview_b = ENERGY_IMGS.get(eb)
                                if img_preview_b: st.image(img_preview_b, width=20)

                                c_b1, c_b2 = st.columns(2)
                                with c_b1:
                                    if st.button("", icon=":material/add:", key=f"baeb_{bp.id_unico}"): 
                                        bp.anexar_energia(eb)
                                        adicionar_log("Energia", f"Ligou {eb} no banco", p['nome'])
                                        st.rerun()
                                with c_b2:
                                    if st.button("", icon=":material/remove:", key=f"breb_{bp.id_unico}"): 
                                        bp.remover_energia(eb)
                                        adicionar_log("Energia", f"Removeu {eb} do banco", p['nome'])
                                        st.rerun()
                            
                            with t2: # ABA STATUS (NOVA)
                                st.selectbox("Status", ["Saudável", "Envenenado 🧪", "Queimado 🔥", "Adormecido 💤", "Paralisado ⚡"], key=f"st_b_{bp.id_unico}", on_change=lambda: setattr(bp, 'status', st.session_state[f"st_b_{bp.id_unico}"]))

                            with t3: # ABA TOOL
                                tlb = st.selectbox("Tool", list(TOOLS_DB.keys()), key=f"tlb_{bp.id_unico}")
                                if st.button("Eqp", icon=":material/build:", key=f"btlb_{bp.id_unico}"): bp.equipar_ferramenta(tlb); st.rerun()

                        if bp.habilidade:
                            ja = bp.id_unico in st.session_state.habilidades_usadas
                            if st.button("✨", key=f"hbb_{bp.id_unico}", disabled=ja, help=bp.habilidade):
                                st.session_state.habilidades_usadas.append(bp.id_unico)
                                adicionar_log("Tool", f"✨ {bp.nome} (Banco) hab.", p['nome'])
                                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.vencedor:
        st.balloons()
        st.markdown(f"<h1 style='text-align:center'>🏆 {st.session_state.vencedor} VENCEU!</h1>", unsafe_allow_html=True)
        if st.button("Novo Jogo"): st.session_state.clear(); st.rerun()
    else:
        c1, c_div, c2 = st.columns([1, 0.1, 1])
        with c1: render_player("Treinador 1")
        with c_div:
            st.markdown("""<div style='height: 100%; min-height: 800px; width: 1px; background-color: #334155; margin: 0 auto;'></div>""", unsafe_allow_html=True)
        with c2: render_player("Treinador 2")
        
        st.divider()
        st.subheader("📜 Registro")
        with st.container(height=300):
            st.markdown("".join(st.session_state.log), unsafe_allow_html=True)
