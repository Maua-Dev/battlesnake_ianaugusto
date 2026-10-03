# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \   __\   __\  | _/ __ \ /  ___//    \__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\_____>
#
# ESTE É O ARQUIVO QUE VOCÊ VAI EDITAR. Todo o resto do projeto existe
# só para levar o estado do jogo até as quatro funções abaixo.

import random
import logging
from .models import GameState, MoveResponse

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def info() -> dict:
    logger.info("INFO")
    return {
        "apiversion": "1",
        "author": "Ian",
        "color": "#E906B0",
        "head": "default",
        "tail": "default",
        "version": "1.0.0",
    }


def start(state: GameState) -> None:
    logger.info("JOGO COMEÇOU (partida %s)", state.game.id)


def end(state: GameState) -> None:
    logger.info("FIM DE JOGO após %d turnos", state.turn)


def get_move(state: GameState) -> MoveResponse:
    is_move_safe: dict[str, bool] = {
        "up": True,
        "down": True,
        "left": True,
        "right": True,
    }

    my_head = state.you.body[0]
    my_neck = state.you.body[1] if len(state.you.body) >= 2 else None

    if my_neck is not None:
        if my_neck.x < my_head.x:
            is_move_safe["left"] = False
        elif my_neck.x > my_head.x:
            is_move_safe["right"] = False
        elif my_neck.y < my_head.y:
            is_move_safe["down"] = False
        elif my_neck.y > my_head.y:
            is_move_safe["up"] = False

    board_width = state.board.width
    board_height = state.board.height

    if my_head.x + 1 >= board_width:
        is_move_safe["right"] = False
    if my_head.x - 1 < 0:
        is_move_safe["left"] = False
    if my_head.y + 1 >= board_height:
        is_move_safe["up"] = False
    if my_head.y - 1 < 0:
        is_move_safe["down"] = False

    my_body = state.you.body
    for segment in my_body:
        if segment.x == my_head.x + 1 and segment.y == my_head.y:
            is_move_safe["right"] = False
        if segment.x == my_head.x - 1 and segment.y == my_head.y:
            is_move_safe["left"] = False
        if segment.x == my_head.x and segment.y == my_head.y + 1:
            is_move_safe["up"] = False
        if segment.x == my_head.x and segment.y == my_head.y - 1:
            is_move_safe["down"] = False

    # --- SISTEMA DE BLOCOS E FRONTEIRAS (ESTRUTURA JOGO DA VELHA) ---
    estado = {"emergencia": False}

    blocos = {
        "b1": {
            "coords": [
                {'x': 0, 'y': 10}, {'x': 1, 'y': 10}, {'x': 2, 'y': 10},
                {'x': 0, 'y': 9},  {'x': 1, 'y': 9},  {'x': 2, 'y': 9},
                {'x': 0, 'y': 8},  {'x': 1, 'y': 8},  {'x': 2, 'y': 8}
            ],
            "pontos": 0
        },
        "b2": {
            "coords": [
                {'x': 3, 'y': 10}, {'x': 4, 'y': 10}, {'x': 5, 'y': 10},
                {'x': 3, 'y': 9},  {'x': 4, 'y': 9},  {'x': 5, 'y': 9},
                {'x': 3, 'y': 8},  {'x': 4, 'y': 8},  {'x': 5, 'y': 8}
            ],
            "pontos": 0
        },
        "b3": {
            "coords": [
                {'x': 6, 'y': 10}, {'x': 7, 'y': 10}, {'x': 8, 'y': 10},
                {'x': 6, 'y': 9},  {'x': 7, 'y': 9},  {'x': 8, 'y': 9},
                {'x': 6, 'y': 8},  {'x': 7, 'y': 8},  {'x': 8, 'y': 8}
            ],
            "pontos": 0
        },
        "b4": {
            "coords": [
                {'x': 0, 'y': 7}, {'x': 1, 'y': 7}, {'x': 2, 'y': 7},
                {'x': 0, 'y': 6}, {'x': 1, 'y': 6}, {'x': 2, 'y': 6},
                {'x': 0, 'y': 5}, {'x': 1, 'y': 5}, {'x': 2, 'y': 5}
            ],
            "pontos": 0
        },
        "b5": {
            "coords": [
                {'x': 3, 'y': 7}, {'x': 4, 'y': 7}, {'x': 5, 'y': 7},
                {'x': 3, 'y': 6}, {'x': 4, 'y': 6}, {'x': 5, 'y': 6},
                {'x': 3, 'y': 5}, {'x': 4, 'y': 5}, {'x': 5, 'y': 5}
            ],
            "pontos": 0
        },
        "b6": {
            "coords": [
                {'x': 6, 'y': 7}, {'x': 7, 'y': 7}, {'x': 8, 'y': 7},
                {'x': 6, 'y': 6}, {'x': 7, 'y': 6}, {'x': 8, 'y': 6},
                {'x': 6, 'y': 5}, {'x': 7, 'y': 5}, {'x': 8, 'y': 5}
            ],
            "pontos": 0
        },
        "b7": {
            "coords": [
                {'x': 0, 'y': 4}, {'x': 1, 'y': 4}, {'x': 2, 'y': 4},
                {'x': 0, 'y': 3}, {'x': 1, 'y': 3}, {'x': 2, 'y': 3},
                {'x': 0, 'y': 2}, {'x': 1, 'y': 2}, {'x': 2, 'y': 2}
            ],
            "pontos": 0
        },
        "b8": {
            "coords": [
                {'x': 3, 'y': 4}, {'x': 4, 'y': 4}, {'x': 5, 'y': 4},
                {'x': 3, 'y': 3}, {'x': 4, 'y': 3}, {'x': 5, 'y': 3},
                {'x': 3, 'y': 2}, {'x': 4, 'y': 2}, {'x': 5, 'y': 2}
            ],
            "pontos": 0
        },
        "b9": {
            "coords": [
                {'x': 6, 'y': 4}, {'x': 7, 'y': 4}, {'x': 8, 'y': 4},
                {'x': 6, 'y': 3}, {'x': 7, 'y': 3}, {'x': 8, 'y': 3},
                {'x': 6, 'y': 2}, {'x': 7, 'y': 2}, {'x': 8, 'y': 2}
            ],
            "pontos": 0
        }
    }

    vizinhos_blocos = {
        "b1": ["b2", "b4"],
        "b2": ["b1", "b3", "b5"],
        "b3": ["b2", "b6"],
        "b4": ["b1", "b5", "b7"],
        "b5": ["b2", "b4", "b6", "b8"],
        "b6": ["b3", "b5", "b9"],
        "b7": ["b4", "b8"],
        "b8": ["b7", "b5", "b9"],
        "b9": ["b6", "b8"]
    }

    fronteiras = {
        "b1_b2": {"coords": [{'x': 2, 'y': 10}, {'x': 2, 'y': 9}, {'x': 2, 'y': 8}]},
        "b1_b4": {"coords": [{'x': 0, 'y': 7}, {'x': 1, 'y': 7}, {'x': 2, 'y': 7}]},
        "b2_b3": {"coords": [{'x': 5, 'y': 10}, {'x': 5, 'y': 9}, {'x': 5, 'y': 8}]},
        "b2_b5": {"coords": [{'x': 3, 'y': 7}, {'x': 4, 'y': 7}, {'x': 5, 'y': 7}]},
        "b3_b6": {"coords": [{'x': 6, 'y': 7}, {'x': 7, 'y': 7}, {'x': 8, 'y': 7}]},
        "b4_b5": {"coords": [{'x': 2, 'y': 7}, {'x': 2, 'y': 6}, {'x': 2, 'y': 5}]},
        "b4_b7": {"coords": [{'x': 0, 'y': 4}, {'x': 1, 'y': 4}, {'x': 2, 'y': 4}]},
        "b5_b6": {"coords": [{'x': 5, 'y': 7}, {'x': 5, 'y': 6}, {'x': 5, 'y': 5}]},
        "b5_b8": {"coords": [{'x': 3, 'y': 4}, {'x': 4, 'y': 4}, {'x': 5, 'y': 4}]},
        "b6_b9": {"coords": [{'x': 6, 'y': 4}, {'x': 7, 'y': 4}, {'x': 8, 'y': 4}]},
        "b7_b8": {"coords": [{'x': 2, 'y': 4}, {'x': 2, 'y': 3}, {'x': 2, 'y': 2}]},
        "b8_b9": {"coords": [{'x': 5, 'y': 4}, {'x': 5, 'y': 3}, {'x': 5, 'y': 2}]}
    }

    food_list = state.board.food

    def ponturaComida():
        for comida in food_list:
            c_dict = {'x': comida.x, 'y': comida.y}
            for dados in blocos.values():
                if c_dict in dados["coords"]:
                    dados["pontos"] += 3

    def acharVizinho():
        ondeEstou = None
        head_dict = {'x': my_head.x, 'y': my_head.y}
        for nome_bloco, local in blocos.items():
            if head_dict in local["coords"]:
                local["pontos"] += 15
                ondeEstou = nome_bloco
                break
        if ondeEstou:
            vizinhos = vizinhos_blocos[ondeEstou]
            for v in vizinhos:
                blocos[v]["pontos"] += 15

    def calcularInimigos():
        inimigos = state.board.snakes
        for inimigo in inimigos:
            for parte in inimigo.body:
                p_dict = {'x': parte.x, 'y': parte.y}
                for locais in blocos.values():
                    if p_dict in locais["coords"]:
                        locais["pontos"] -= 50

    def evitarInimigos():
        movimentos_possiveis = {
            "up": {'x': my_head.x, 'y': my_head.y + 1},
            "down": {'x': my_head.x, 'y': my_head.y - 1},
            "left": {'x': my_head.x - 1, 'y': my_head.y},
            "right": {'x': my_head.x + 1, 'y': my_head.y}
        }
        inimigos = state.board.snakes
        for inimigo in inimigos:
            for parte in inimigo.body:
                for direcao, proxima_pos in movimentos_possiveis.items():
                    if parte.x == proxima_pos['x'] and parte.y == proxima_pos['y']:
                        is_move_safe[direcao] = False

    def acharMelhorBloco():
        macas_no_destino = []
        usarFronteira = None
        blocoAtual = None
        melhor_bloco_nome = None
        maior_pontuacao = -9999 
        coords_do_bloco = []
        coords_da_fronteira = []

        for nome_bloco, local in blocos.items():
            if local["pontos"] > maior_pontuacao:
                maior_pontuacao = local["pontos"]
                melhor_bloco_nome = nome_bloco

        if melhor_bloco_nome:
            coords_do_bloco = blocos[melhor_bloco_nome]["coords"]

        head_dict = {'x': my_head.x, 'y': my_head.y}
        for nome_bloco, local in blocos.items():     
            if head_dict in local['coords']:
                blocoAtual = nome_bloco
                break

        # Blinda caso a cobra esteja navegando pelas linhas do jogo da velha (corredores/fronteiras)
        if blocoAtual and melhor_bloco_nome:
            for locais in fronteiras:
                if locais == blocoAtual + '_' + melhor_bloco_nome or locais == melhor_bloco_nome + '_' + blocoAtual:
                    usarFronteira = locais
                    break

        if usarFronteira and usarFronteira in fronteiras:
            coords_da_fronteira = fronteiras[usarFronteira]["coords"]

        for comida in food_list:
            c_dict = {'x': comida.x, 'y': comida.y}
            if c_dict in coords_da_fronteira:
                if is_move_safe["right"] and my_head.x < comida.x: return "right"
                if is_move_safe["left"] and my_head.x > comida.x: return "left"
                if is_move_safe["up"] and my_head.y < comida.y: return "up"
                if is_move_safe["down"] and my_head.y > comida.y: return "down"

        for comida in food_list:
            c_dict = {'x': comida.x, 'y': comida.y}
            if c_dict in coords_do_bloco:
                macas_no_destino.append(comida)

        if macas_no_destino:
            alvo = macas_no_destino[0]
            if is_move_safe["right"] and my_head.x < alvo.x: return "right"
            if is_move_safe["left"] and my_head.x > alvo.x: return "left"
            if is_move_safe["up"] and my_head.y < alvo.y: return "up"
            if is_move_safe["down"] and my_head.y > alvo.y: return "down"

        return None

    def inimigoNoMeuBloco():
        blocoAtual = None
        head_dict = {'x': my_head.x, 'y': my_head.y}
        for nome_bloco, local in blocos.items():     
            if head_dict in local['coords']:
                blocoAtual = nome_bloco
                break
                
        if blocoAtual:
            coords_do_bloco = blocos[blocoAtual]["coords"]
            inimigos = state.board.snakes
            for inimigo in inimigos:
                if inimigo.id != state.you.id:
                    inimigo_cabeca = {'x': inimigo.body[0].x, 'y': inimigo.body[0].y}
                    if inimigo_cabeca in coords_do_bloco:
                        estado["emergencia"] = True
                        return
                        
        estado["emergencia"] = False

    def modoDefensivo():
        if estado["emergencia"]:
            rabo = state.you.body[-1]
            
            if is_move_safe["right"] and my_head.x < rabo.x: return "right"
            if is_move_safe["left"] and my_head.x > rabo.x: return "left"
            if is_move_safe["up"] and my_head.y < rabo.y: return "up"
            if is_move_safe["down"] and my_head.y > rabo.y: return "down"

            for direcao, segura in is_move_safe.items():
                if segura:
                    return direcao
                    
        return None

    # EXECUTANDO AS FUNÇÕES DO TURNO
    ponturaComida()
    acharVizinho()
    calcularInimigos()
    evitarInimigos()
    inimigoNoMeuBloco()

    direcao_alvo = modoDefensivo()
    if not direcao_alvo:
        direcao_alvo = acharMelhorBloco()

    safe_moves = [direction for direction, safe in is_move_safe.items() if safe]

    if not safe_moves:
        all_moves = ["up", "down", "left", "right"]
        fallback = random.choice(all_moves)
        logger.info("MOVE %d: sem saída! emergência -> %s", state.turn, fallback)
        return MoveResponse(move=fallback)

    if direcao_alvo and direcao_alvo in safe_moves:
        chosen = direcao_alvo
    else:
        chosen = random.choice(safe_moves)

    logger.debug("MOVE %d: %s", state.turn, chosen)
    return MoveResponse(move=chosen)