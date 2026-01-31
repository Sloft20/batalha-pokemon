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


