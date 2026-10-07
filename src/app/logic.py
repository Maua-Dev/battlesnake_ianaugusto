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
    direcoes = ["up", "down", "left", "right"]
    random.shuffle(direcoes)
    is_move_safe: dict[str, bool] = {d: True for d in direcoes}

    my_head = state.you.body[0]
    my_neck = state.you.body[1] if len(state.you.body) >= 2 else None

    if my_neck is not None:
        if my_neck.x < my_head.x: is_move_safe["left"] = False
        elif my_neck.x > my_head.x: is_move_safe["right"] = False
        elif my_neck.y < my_head.y: is_move_safe["down"] = False
        elif my_neck.y > my_head.y: is_move_safe["up"] = False

    board_width = state.board.width
    board_height = state.board.height

    if my_head.x + 1 >= board_width: is_move_safe["right"] = False
    if my_head.x - 1 < 0: is_move_safe["left"] = False
    if my_head.y + 1 >= board_height: is_move_safe["up"] = False
    if my_head.y - 1 < 0: is_move_safe["down"] = False

    inimigo = None
    for cobra in state.board.snakes:
        if cobra.id != state.you.id:
            inimigo = cobra
            break
            
    meuTamanho = len(state.you.body)
    tamanhoInimigo = len(inimigo.body) if inimigo is not None else 0
    estouPerdendo = meuTamanho <= tamanhoInimigo

    my_body = state.you.body
    raboFixo = (len(my_body) >= 2 and my_body[-1].x == my_body[-2].x and my_body[-1].y == my_body[-2].y)

    for i, segment in enumerate(my_body):
        if not raboFixo and i == len(my_body) - 1:
            continue
        if segment.x == my_head.x + 1 and segment.y == my_head.y: is_move_safe["right"] = False
        if segment.x == my_head.x - 1 and segment.y == my_head.y: is_move_safe["left"] = False
        if segment.x == my_head.x and segment.y == my_head.y + 1: is_move_safe["up"] = False
        if segment.x == my_head.x and segment.y == my_head.y - 1: is_move_safe["down"] = False

    listaComida = []
    for comida in state.board.food:
        naBorda = (comida.x == 0 or comida.x == board_width - 1 or comida.y == 0 or comida.y == board_height - 1)
        if naBorda and not estouPerdendo:
            continue
        listaComida.append(comida)

    blocos = {
        "b1": {"coords": [{'x': 0, 'y': 10}, {'x': 1, 'y': 10}, {'x': 2, 'y': 10}, {'x': 0, 'y': 9},  {'x': 1, 'y': 9},  {'x': 2, 'y': 9}, {'x': 0, 'y': 8},  {'x': 1, 'y': 8},  {'x': 2, 'y': 8}], "pontos": 0},
        "b2": {"coords": [{'x': 4, 'y': 10}, {'x': 5, 'y': 10}, {'x': 6, 'y': 10}, {'x': 4, 'y': 9},  {'x': 5, 'y': 9},  {'x': 6, 'y': 9}, {'x': 4, 'y': 8},  {'x': 5, 'y': 8},  {'x': 6, 'y': 8}], "pontos": 0},
        "b3": {"coords": [{'x': 8, 'y': 10}, {'x': 9, 'y': 10}, {'x': 10, 'y': 10},{'x': 8, 'y': 9},  {'x': 9, 'y': 9},  {'x': 10, 'y': 9},{'x': 8, 'y': 8},  {'x': 9, 'y': 8},  {'x': 10, 'y': 8}], "pontos": 0},
        "b4": {"coords": [{'x': 0, 'y': 6}, {'x': 1, 'y': 6}, {'x': 2, 'y': 6},   {'x': 0, 'y': 5}, {'x': 1, 'y': 5}, {'x': 2, 'y': 5},   {'x': 0, 'y': 4}, {'x': 1, 'y': 4}, {'x': 2, 'y': 4}], "pontos": 0},
        "b5": {"coords": [{'x': 4, 'y': 6}, {'x': 5, 'y': 6}, {'x': 6, 'y': 6},   {'x': 4, 'y': 5}, {'x': 5, 'y': 5}, {'x': 6, 'y': 5},   {'x': 4, 'y': 4}, {'x': 5, 'y': 4}, {'x': 6, 'y': 4}], "pontos": 0},
        "b6": {"coords": [{'x': 8, 'y': 6}, {'x': 9, 'y': 6}, {'x': 10, 'y': 6},  {'x': 8, 'y': 5}, {'x': 9, 'y': 5}, {'x': 10, 'y': 5},  {'x': 8, 'y': 4}, {'x': 9, 'y': 4}, {'x': 10, 'y': 4}], "pontos": 0},
        "b7": {"coords": [{'x': 0, 'y': 2}, {'x': 1, 'y': 2}, {'x': 2, 'y': 2},   {'x': 0, 'y': 1}, {'x': 1, 'y': 1}, {'x': 2, 'y': 1},   {'x': 0, 'y': 0}, {'x': 1, 'y': 0}, {'x': 2, 'y': 0}], "pontos": 0},
        "b8": {"coords": [{'x': 4, 'y': 2}, {'x': 5, 'y': 2}, {'x': 6, 'y': 2},   {'x': 4, 'y': 1}, {'x': 5, 'y': 1}, {'x': 6, 'y': 1},   {'x': 4, 'y': 0}, {'x': 5, 'y': 0}, {'x': 6, 'y': 0}], "pontos": 0},
        "b9": {"coords": [{'x': 8, 'y': 2}, {'x': 9, 'y': 2}, {'x': 10, 'y': 2},  {'x': 8, 'y': 1}, {'x': 9, 'y': 1}, {'x': 10, 'y': 1},  {'x': 8, 'y': 0}, {'x': 9, 'y': 0}, {'x': 10, 'y': 0}], "pontos": 0}
    }

    vizinhosBlocos = {
        "b1": ["b2", "b4"], "b2": ["b1", "b3", "b5"], "b3": ["b2", "b6"],
        "b4": ["b1", "b5", "b7"], "b5": ["b2", "b4", "b6", "b8"], "b6": ["b3", "b5", "b9"],
        "b7": ["b4", "b8"], "b8": ["b7", "b5", "b9"], "b9": ["b6", "b8"]
    }

    fronteiras = {
        "b1_b2": {"coords": [{'x': 3, 'y': 10}, {'x': 3, 'y': 9}, {'x': 3, 'y': 8}]},
        "b1_b4": {"coords": [{'x': 0, 'y': 7}, {'x': 1, 'y': 7}, {'x': 2, 'y': 7}]},
        "b2_b3": {"coords": [{'x': 7, 'y': 10}, {'x': 7, 'y': 9}, {'x': 7, 'y': 8}]},
        "b2_b5": {"coords": [{'x': 4, 'y': 7}, {'x': 5, 'y': 7}, {'x': 6, 'y': 7}]},
        "b3_b6": {"coords": [{'x': 8, 'y': 7}, {'x': 9, 'y': 7}, {'x': 10, 'y': 7}]},
        "b4_b5": {"coords": [{'x': 3, 'y': 6}, {'x': 3, 'y': 5}, {'x': 3, 'y': 4}]},
        "b4_b7": {"coords": [{'x': 0, 'y': 3}, {'x': 1, 'y': 3}, {'x': 2, 'y': 3}]},
        "b5_b6": {"coords": [{'x': 7, 'y': 6}, {'x': 7, 'y': 5}, {'x': 7, 'y': 4}]},
        "b5_b8": {"coords": [{'x': 4, 'y': 3}, {'x': 5, 'y': 3}, {'x': 6, 'y': 3}]},
        "b6_b9": {"coords": [{'x': 8, 'y': 3}, {'x': 9, 'y': 3}, {'x': 10, 'y': 3}]},
        "b7_b8": {"coords": [{'x': 3, 'y': 2}, {'x': 3, 'y': 1}, {'x': 3, 'y': 0}]},
        "b8_b9": {"coords": [{'x': 7, 'y': 2}, {'x': 7, 'y': 1}, {'x': 7, 'y': 0}]}
    }

    pesoComida = 90 if estouPerdendo else 15

    def temEspacoSeguro(start_x, start_y, minimo=meuTamanho):
        visitados = set()
        fila = [{'x': start_x, 'y': start_y}]
        
        obstaculos = set()
        
        limite_meu_corpo = None if raboFixo else -1
        for p in state.you.body[:limite_meu_corpo]: 
            obstaculos.add((p.x, p.y))
            
        for cobra in state.board.snakes:
            if cobra.id == state.you.id: continue
            for p in cobra.body[:-1]:
                obstaculos.add((p.x, p.y))
                
        while fila:
            atual = fila.pop(0)
            pos_tuple = (atual['x'], atual['y'])
            if pos_tuple in visitados: continue
            visitados.add(pos_tuple)
            
            if len(visitados) >= minimo:
                return True
                
            for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
                nx, ny = atual['x'] + dx, atual['y'] + dy
                if 0 <= nx < board_width and 0 <= ny < board_height:
                    if (nx, ny) not in obstaculos and (nx, ny) not in visitados:
                        fila.append({'x': nx, 'y': ny})
                        
        return len(visitados) >= minimo

    def pontuarComida():
        ordenadas = sorted(listaComida, key=lambda c: abs(c.x - my_head.x) + abs(c.y - my_head.y))
        for posicao, comida in enumerate(ordenadas):
            if posicao == 0: pontos = pesoComida * 3
            elif posicao == 1: pontos = pesoComida * 2
            else: pontos = pesoComida
            
            c_dict = {'x': comida.x, 'y': comida.y}
            for dados in blocos.values():
                if c_dict in dados["coords"]:
                    dados["pontos"] += pontos

    def calcularInimigos():
        if inimigo is not None:
            for parte in inimigo.body:
                p_dict = {'x': parte.x, 'y': parte.y}
                for locais in blocos.values():
                    if p_dict in locais["coords"]:
                        if not estouPerdendo:
                            locais["pontos"] += 50
                        else:
                            locais["pontos"] -= 50

    def evitarInimigos():
        movimentosPossiveis = {
            "up": {'x': my_head.x, 'y': my_head.y + 1},
            "down": {'x': my_head.x, 'y': my_head.y - 1},
            "left": {'x': my_head.x - 1, 'y': my_head.y},
            "right": {'x': my_head.x + 1, 'y': my_head.y}
        }
        
        for cobra in state.board.snakes:
            if cobra.id == state.you.id: continue
            for parte in cobra.body:
                for direcao, proximaPos in movimentosPossiveis.items():
                    if parte.x == proximaPos['x'] and parte.y == proximaPos['y']:
                        is_move_safe[direcao] = False

        if estouPerdendo and inimigo is not None:
            perigoCabeca = []
            cab = inimigo.body[0]
            for direcao, proximaPos in movimentosPossiveis.items():
                if abs(cab.x - proximaPos['x']) + abs(cab.y - proximaPos['y']) == 1:
                    perigoCabeca.append(direcao)
            
            sobram = [d for d, seg in is_move_safe.items() if seg and d not in perigoCabeca]
            if len(sobram) > 0:
                for d in perigoCabeca:
                    is_move_safe[d] = False

    def evitarBordas():
        if inimigo is not None:
            dist = abs(my_head.x - inimigo.body[0].x) + abs(my_head.y - inimigo.body[0].y)
            if dist <= 3:
                return

        movimentosPossiveis = {
            "up": {'x': my_head.x, 'y': my_head.y + 1},
            "down": {'x': my_head.x, 'y': my_head.y - 1},
            "left": {'x': my_head.x - 1, 'y': my_head.y},
            "right": {'x': my_head.x + 1, 'y': my_head.y}
        }
        beiradas = []
        for direcao, pos in movimentosPossiveis.items():
            if pos['x'] == 0 or pos['x'] == board_width - 1 or pos['y'] == 0 or pos['y'] == board_height - 1:
                beiradas.append(direcao)
                
        sobram = [d for d, seg in is_move_safe.items() if seg and d not in beiradas]
        
        if len(sobram) > 0:
            for direcaoBorda in beiradas:
                temMaca = False
                posicaoBorda = movimentosPossiveis[direcaoBorda]
                for comida in listaComida:
                    if comida.x == posicaoBorda['x'] and comida.y == posicaoBorda['y']:
                        temMaca = True
                        break
                
                if not temMaca:
                    is_move_safe[direcaoBorda] = False

    def kamikasi():
        if inimigo is not None and meuTamanho >= tamanhoInimigo + 2:
            meu_bloco = None
            inimigo_bloco = None
            
            head_dict = {'x': my_head.x, 'y': my_head.y}
            cabeca_inimigo_dict = {'x': inimigo.body[0].x, 'y': inimigo.body[0].y}
            
            for nomeBloco, local in blocos.items():     
                if head_dict in local['coords']:
                    meu_bloco = nomeBloco
                if cabeca_inimigo_dict in local['coords']:
                    inimigo_bloco = nomeBloco
                    
            if meu_bloco and meu_bloco == inimigo_bloco:
                alvo = inimigo.body[0]
                if is_move_safe["right"] and my_head.x < alvo.x and temEspacoSeguro(my_head.x + 1, my_head.y): return "right"
                if is_move_safe["left"] and my_head.x > alvo.x and temEspacoSeguro(my_head.x - 1, my_head.y): return "left"
                if is_move_safe["up"] and my_head.y < alvo.y and temEspacoSeguro(my_head.x, my_head.y + 1): return "up"
                if is_move_safe["down"] and my_head.y > alvo.y and temEspacoSeguro(my_head.x, my_head.y - 1): return "down"
                
        return None

    def fecharInimigo():
        if not estouPerdendo and inimigo is not None:
            cabecaInimigo = inimigo.body[0]
            pescocoInimigo = inimigo.body[1] if len(inimigo.body) > 1 else cabecaInimigo
                
            indoParaCima = cabecaInimigo.y > pescocoInimigo.y
            indoParaBaixo = cabecaInimigo.y < pescocoInimigo.y
            indoParaDireita = cabecaInimigo.x > pescocoInimigo.x
            indoParaEsquerda = cabecaInimigo.x < pescocoInimigo.x
            
            if indoParaCima and abs(my_head.x - cabecaInimigo.x) == 1 and my_head.y > cabecaInimigo.y:
                if my_head.x < cabecaInimigo.x and is_move_safe["right"] and temEspacoSeguro(my_head.x + 1, my_head.y): return "right"
                if my_head.x > cabecaInimigo.x and is_move_safe["left"] and temEspacoSeguro(my_head.x - 1, my_head.y): return "left"
                
            if indoParaBaixo and abs(my_head.x - cabecaInimigo.x) == 1 and my_head.y < cabecaInimigo.y:
                if my_head.x < cabecaInimigo.x and is_move_safe["right"] and temEspacoSeguro(my_head.x + 1, my_head.y): return "right"
                if my_head.x > cabecaInimigo.x and is_move_safe["left"] and temEspacoSeguro(my_head.x - 1, my_head.y): return "left"
                
            if indoParaDireita and abs(my_head.y - cabecaInimigo.y) == 1 and my_head.x > cabecaInimigo.x:
                if my_head.y < cabecaInimigo.y and is_move_safe["up"] and temEspacoSeguro(my_head.x, my_head.y + 1): return "up"
                if my_head.y > cabecaInimigo.y and is_move_safe["down"] and temEspacoSeguro(my_head.x, my_head.y - 1): return "down"
                
            if indoParaEsquerda and abs(my_head.y - cabecaInimigo.y) == 1 and my_head.x < cabecaInimigo.x:
                if my_head.y < cabecaInimigo.y and is_move_safe["up"] and temEspacoSeguro(my_head.x, my_head.y + 1): return "up"
                if my_head.y > cabecaInimigo.y and is_move_safe["down"] and temEspacoSeguro(my_head.x, my_head.y - 1): return "down"
                
        return None

    def acharMelhorBloco():
        macasNoDestino = []
        usarFronteira = None
        blocoAtual = None
        melhorBlocoNome = None
        maiorPontuacao = -9999 
        coordsDoBloco = []
        coordsDaFronteira = []

        for nomeBloco, local in blocos.items():
            if local["pontos"] > maiorPontuacao:
                maiorPontuacao = local["pontos"]
                melhorBlocoNome = nomeBloco

        if melhorBlocoNome: coordsDoBloco = blocos[melhorBlocoNome]["coords"]

        head_dict = {'x': my_head.x, 'y': my_head.y}
        for nomeBloco, local in blocos.items():     
            if head_dict in local['coords']:
                blocoAtual = nomeBloco
                break

        if blocoAtual and melhorBlocoNome:
            for locais in fronteiras:
                if locais == blocoAtual + '_' + melhorBlocoNome or locais == melhorBlocoNome + '_' + blocoAtual:
                    usarFronteira = locais
                    break

        if usarFronteira and usarFronteira in fronteiras:
            coordsDaFronteira = fronteiras[usarFronteira]["coords"]

        for comida in listaComida:
            c_dict = {'x': comida.x, 'y': comida.y}
            if c_dict in coordsDaFronteira:
                if is_move_safe["right"] and my_head.x < comida.x and temEspacoSeguro(my_head.x + 1, my_head.y): return "right"
                if is_move_safe["left"] and my_head.x > comida.x and temEspacoSeguro(my_head.x - 1, my_head.y): return "left"
                if is_move_safe["up"] and my_head.y < comida.y and temEspacoSeguro(my_head.x, my_head.y + 1): return "up"
                if is_move_safe["down"] and my_head.y > comida.y and temEspacoSeguro(my_head.x, my_head.y - 1): return "down"

        for comida in listaComida:
            c_dict = {'x': comida.x, 'y': comida.y}
            if c_dict in coordsDoBloco:
                macasNoDestino.append(comida)

        if macasNoDestino:
            alvo = macasNoDestino[0]
            if is_move_safe["right"] and my_head.x < alvo.x and temEspacoSeguro(my_head.x + 1, my_head.y): return "right"
            if is_move_safe["left"] and my_head.x > alvo.x and temEspacoSeguro(my_head.x - 1, my_head.y): return "left"
            if is_move_safe["up"] and my_head.y < alvo.y and temEspacoSeguro(my_head.x, my_head.y + 1): return "up"
            if is_move_safe["down"] and my_head.y > alvo.y and temEspacoSeguro(my_head.x, my_head.y - 1): return "down"

        return None

    pontuarComida()
    calcularInimigos()
    evitarInimigos()
    evitarBordas()      

    direcao_alvo = kamikasi()
    
    if not direcao_alvo:
        direcao_alvo = fecharInimigo()
    
    if not direcao_alvo:
        direcao_alvo = acharMelhorBloco()

    safe_moves = []
    for d, seguro in is_move_safe.items():
        if seguro:
            nx, ny = my_head.x, my_head.y
            if d == "up": ny += 1
            elif d == "down": ny -= 1
            elif d == "right": nx += 1
            elif d == "left": nx -= 1
            
            if temEspacoSeguro(nx, ny):
                safe_moves.append(d)

    if not safe_moves:
        safe_moves = [direction for direction, safe in is_move_safe.items() if safe]

    if not safe_moves:
        fallback = random.choice(["up", "down", "left", "right"])
        logger.info("MOVE %d: sem saída! emergência -> %s", state.turn, fallback)
        return MoveResponse(move=fallback)

    if direcao_alvo and direcao_alvo in safe_moves:
        chosen = direcao_alvo
    else:
        chosen = random.choice(safe_moves)

    logger.debug("MOVE %d: %s", state.turn, chosen)
    return MoveResponse(move=chosen)