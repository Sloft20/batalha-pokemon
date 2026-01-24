# cartas_db.py

# --- IMAGENS DE ENERGIA ---
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

# --- POKÉDEX COMPLETA ---
POKEDEX = {
    "Dragapult ex": {"hp": 320, "tipo": "Dragão 🐉", "fraq": "Nenhuma", "res": "Nenhuma", "recuo": 1, "custo": ["Fogo 🔥", "Psíquico 🌀"], "img": "https://dz3we2x72f7ol.cloudfront.net/expansions/prismatic-evolutions/pt-br/SV8pt5_PTBR_73.png"},
    "Drakloak": {"hp": 90, "tipo": "Dragão 🐉", "fraq": "Nenhuma", "res": "Nenhuma", "recuo": 1, "custo": ["Fogo 🔥", "Psíquico 🌀"], "hab": "Reconhecimento", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/TWM/TWM_129_R_EN_PNG.png"},
    "Dreepy": {"hp": 70, "tipo": "Dragão 🐉", "fraq": "Nenhuma", "res": "Nenhuma", "recuo": 1, "custo": ["Psíquico 🌀"], "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/TWM/TWM_128_R_EN_PNG.png"},
    "Xatu": {"hp": 100, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "recuo": 1, "custo": ["Psíquico 🌀", "Incolor ⭐"], "hab": "Sentido Clarividente", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/PAR/PAR_072_R_EN_PNG.png"},
    "Natu": {"hp": 60, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "recuo": 1, "custo": ["Psíquico 🌀"], "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/PAR/PAR_071_R_EN_PNG.png"},
    "Fezandipiti ex": {"hp": 210, "tipo": "Psíquico 🌀", "fraq": "Metal ⚙️", "res": "Nenhuma", "recuo": 1, "custo": ["Incolor ⭐", "Incolor ⭐", "Incolor ⭐"], "hab": "Virar o Jogo", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/SFA/SFA_038_R_EN_PNG.png"},
    "Charizard ex": {"hp": 330, "tipo": "Escuridão 🌙", "fraq": "Planta 🌱", "res": "Nenhuma", "recuo": 2, "custo": ["Fogo 🔥", "Fogo 🔥"], "hab": "Reino Infernal", "img": "https://dz3we2x72f7ol.cloudfront.net/expansions/obsidian-flames/pt-br/SV03_PTBR_125.png"},
    "Charmeleon": {"hp": 90, "tipo": "Fogo 🔥", "fraq": "Água 💧", "res": "Nenhuma", "recuo": 2, "custo": ["Fogo 🔥", "Fogo 🔥"], "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/OBF/OBF_027_R_EN_PNG.png"},
    "Charmander": {"hp": 70, "tipo": "Fogo 🔥", "fraq": "Água 💧", "res": "Nenhuma", "recuo": 1, "custo": ["Fogo 🔥"], "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/OBF/OBF_026_R_EN_PNG.png"},
    "Pidgeot ex": {"hp": 280, "tipo": "Normal ⚪", "fraq": "Elétrico ⚡", "res": "Luta 🥊", "recuo": 0, "custo": ["Incolor ⭐", "Incolor ⭐"], "hab": "Busca Rápida", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/OBF/OBF_164_R_EN_PNG.png"},
    "Pidgey": {"hp": 60, "tipo": "Normal ⚪", "fraq": "Elétrico ⚡", "res": "Luta 🥊", "recuo": 1, "custo": ["Incolor ⭐"], "hab": "Chamar a Família", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/OBF/OBF_162_R_EN_PNG.png"},
    "Moltres": {"hp": 120, "tipo": "Fogo 🔥", "fraq": "Água 💧", "res": "Nenhuma", "recuo": 1, "custo": ["Fogo 🔥", "Fogo 🔥", "Incolor ⭐"], "hab": "Símbolo de Fogo", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/BRS/BRS_021_R_EN_PNG.png"},
    "Gardevoir ex": {"hp": 310, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "recuo": 2, "custo": ["Psíquico 🌀", "Psíquico 🌀", "Incolor ⭐"], "hab": "Abraço Psíquico", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/SVI/SVI_086_R_EN_PNG.png"},
    "Kirlia": {"hp": 80, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "recuo": 2, "custo": ["Psíquico 🌀", "Incolor ⭐"], "hab": "Refinamento", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/SVI/SVI_085_R_EN_PNG.png"},
    "Ralts": {"hp": 60, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "recuo": 1, "custo": ["Psíquico 🌀"], "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/SVI/SVI_084_R_EN_PNG.png"},
    "Drifloon": {"hp": 70, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "recuo": 1, "custo": ["Incolor ⭐", "Incolor ⭐"], "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/SVI/SVI_089_R_EN_PNG.png"},
    "Scream Tail": {"hp": 90, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "recuo": 1, "custo": ["Psíquico 🌀", "Incolor ⭐"], "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/PAR/PAR_086_R_EN_PNG.png"},
    "Mew ex": {"hp": 180, "tipo": "Psíquico 🌀", "fraq": "Escuridão 🌙", "res": "Luta 🥊", "recuo": 0, "custo": ["Incolor ⭐", "Incolor ⭐", "Incolor ⭐"], "hab": "Reinício", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/MEW/MEW_151_R_EN_PNG.png"},
    "Radiant Greninja": {"hp": 130, "tipo": "Água 💧", "fraq": "Elétrico ⚡", "res": "Nenhuma", "recuo": 1, "custo": ["Água 💧", "Água 💧", "Incolor ⭐"], "hab": "Cartas Ocultas", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/ASR/ASR_046_R_EN_PNG.png"},
    "Lugia VSTAR": {"hp": 280, "tipo": "Normal ⚪", "fraq": "Elétrico ⚡", "res": "Luta 🥊", "recuo": 2, "custo": ["Incolor ⭐", "Incolor ⭐", "Incolor ⭐", "Incolor ⭐"], "hab": "Astro Invocador", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/SIT/SIT_139_R_EN_PNG.png"},
    "Lugia V": {"hp": 220, "tipo": "Normal ⚪", "fraq": "Elétrico ⚡", "res": "Luta 🥊", "recuo": 2, "custo": ["Incolor ⭐", "Incolor ⭐", "Incolor ⭐", "Incolor ⭐"], "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/SIT/SIT_138_R_EN_PNG.png"},
    "Archeops": {"hp": 150, "tipo": "Normal ⚪", "fraq": "Elétrico ⚡", "res": "Luta 🥊", "recuo": 1, "custo": ["Incolor ⭐", "Incolor ⭐", "Incolor ⭐"], "hab": "Turbo Primitivo", "img": "https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/SIT/SIT_147_R_EN_PNG.png"},
}

# --- LISTA DE DECKS ---
LISTA_DECKS = ["Charizard ex", "Dragapult ex", "Lugia VSTAR", "Gardevoir ex", "Raging Bolt ex", "Iron Thorns ex", "Outro"]

# --- FERRAMENTAS ---
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

