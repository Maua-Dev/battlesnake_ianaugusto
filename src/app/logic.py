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
    # embaralha a ordem das direções a cada turno, para nenhuma ter prioridade fixa
    direcoes = ["up", "down", "left", "right"]
    random.shuffle(direcoes)
    is_move_safe: dict[str, bool] = {d: True for d in direcoes}

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

    # Se eu não acabei de comer, o rabo sai do lugar no próximo turno, então entrar nele é seguro
    raboLivre = state.you.health < 100

    my_body = state.you.body
    for i, segment in enumerate(my_body):
        if raboLivre and i == len(my_body) - 1:
            continue
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
                {'x': 4, 'y': 10}, {'x': 5, 'y': 10}, {'x': 6, 'y': 10},
                {'x': 4, 'y': 9},  {'x': 5, 'y': 9},  {'x': 6, 'y': 9},
                {'x': 4, 'y': 8},  {'x': 5, 'y': 8},  {'x': 6, 'y': 8}
            ],
            "pontos": 0
        },
        "b3": {
            "coords": [
                {'x': 8, 'y': 10}, {'x': 9, 'y': 10}, {'x': 10, 'y': 10},
                {'x': 8, 'y': 9},  {'x': 9, 'y': 9},  {'x': 10, 'y': 9},
                {'x': 8, 'y': 8},  {'x': 9, 'y': 8},  {'x': 10, 'y': 8}
            ],
            "pontos": 0
        },
        "b4": {
            "coords": [
                {'x': 0, 'y': 6}, {'x': 1, 'y': 6}, {'x': 2, 'y': 6},
                {'x': 0, 'y': 5}, {'x': 1, 'y': 5}, {'x': 2, 'y': 5},
                {'x': 0, 'y': 4}, {'x': 1, 'y': 4}, {'x': 2, 'y': 4}
            ],
            "pontos": 0
        },
        "b5": {
            "coords": [
                {'x': 4, 'y': 6}, {'x': 5, 'y': 6}, {'x': 6, 'y': 6},
                {'x': 4, 'y': 5}, {'x': 5, 'y': 5}, {'x': 6, 'y': 5},
                {'x': 4, 'y': 4}, {'x': 5, 'y': 4}, {'x': 6, 'y': 4}
            ],
            "pontos": 0
        },
        "b6": {
            "coords": [
                {'x': 8, 'y': 6}, {'x': 9, 'y': 6}, {'x': 10, 'y': 6},
                {'x': 8, 'y': 5}, {'x': 9, 'y': 5}, {'x': 10, 'y': 5},
                {'x': 8, 'y': 4}, {'x': 9, 'y': 4}, {'x': 10, 'y': 4}
            ],
            "pontos": 0
        },
        "b7": {
            "coords": [
                {'x': 0, 'y': 2}, {'x': 1, 'y': 2}, {'x': 2, 'y': 2},
                {'x': 0, 'y': 1}, {'x': 1, 'y': 1}, {'x': 2, 'y': 1},
                {'x': 0, 'y': 0}, {'x': 1, 'y': 0}, {'x': 2, 'y': 0}
            ],
            "pontos": 0
        },
        "b8": {
            "coords": [
                {'x': 4, 'y': 2}, {'x': 5, 'y': 2}, {'x': 6, 'y': 2},
                {'x': 4, 'y': 1}, {'x': 5, 'y': 1}, {'x': 6, 'y': 1},
                {'x': 4, 'y': 0}, {'x': 5, 'y': 0}, {'x': 6, 'y': 0}
            ],
            "pontos": 0
        },
        "b9": {
            "coords": [
                {'x': 8, 'y': 2}, {'x': 9, 'y': 2}, {'x': 10, 'y': 2},
                {'x': 8, 'y': 1}, {'x': 9, 'y': 1}, {'x': 10, 'y': 1},
                {'x': 8, 'y': 0}, {'x': 9, 'y': 0}, {'x': 10, 'y': 0}
            ],
            "pontos": 0
        }
    }

    vizinhosBlocos = {
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

    listaComida = state.board.food

    # --- LÓGICA DO PESO DA COMIDA ---
    pesoComida = 15
    if state.you.health < 50:
        pesoComida = 30

    tamanhoInimigos = 0
    qtdInimigos = 0
    meuTamanho = len(state.you.body)

    for inimigo in state.board.snakes:
        if inimigo.id != state.you.id:
            tamanhoInimigos += len(inimigo.body)
            qtdInimigos += 1

    if qtdInimigos > 0:
        mediaTamanho = tamanhoInimigos / qtdInimigos
        if meuTamanho < mediaTamanho:
            pesoComida = 90

    desespero = state.you.health < 30

    def pontuarComida():
        ordenadas = sorted(listaComida, key=lambda c: abs(c.x - my_head.x) + abs(c.y - my_head.y))
        for posicao, comida in enumerate(ordenadas):
            if posicao == 0:
                pontos = pesoComida * 3
            elif posicao == 1:
                pontos = pesoComida * 2
            else:
                pontos = pesoComida
            
            c_dict = {'x': comida.x, 'y': comida.y}
            for dados in blocos.values():
                if c_dict in dados["coords"]:
                    dados["pontos"] += pontos

    def acharVizinho():
        ondeEstou = None
        head_dict = {'x': my_head.x, 'y': my_head.y}
        for nomeBloco, local in blocos.items():
            if head_dict in local["coords"]:
                local["pontos"] += 15
                ondeEstou = nomeBloco
                break
        if ondeEstou:
            vizinhos = vizinhosBlocos[ondeEstou]
            for v in vizinhos:
                blocos[v]["pontos"] += 15

    def calcularInimigos():
        inimigos = state.board.snakes
        for inimigo in inimigos:
            if inimigo.id == state.you.id:
                continue
            for parte in inimigo.body:
                p_dict = {'x': parte.x, 'y': parte.y}
                for locais in blocos.values():
                    if p_dict in locais["coords"]:
                        locais["pontos"] -= 50

    def evitarInimigos():
        movimentosPossiveis = {
            "up": {'x': my_head.x, 'y': my_head.y + 1},
            "down": {'x': my_head.x, 'y': my_head.y - 1},
            "left": {'x': my_head.x - 1, 'y': my_head.y},
            "right": {'x': my_head.x + 1, 'y': my_head.y}
        }
        inimigos = state.board.snakes
        for inimigo in inimigos:
            if inimigo.id == state.you.id:
                continue
            for parte in inimigo.body:
                for direcao, proximaPos in movimentosPossiveis.items():
                    if parte.x == proximaPos['x'] and parte.y == proximaPos['y']:
                        is_move_safe[direcao] = False

        perigoCabeca = []
        for inimigo in inimigos:
            if inimigo.id == state.you.id:
                continue
            if len(inimigo.body) >= len(state.you.body):
                cab = inimigo.body[0]
                for direcao, proximaPos in movimentosPossiveis.items():
                    if abs(cab.x - proximaPos['x']) + abs(cab.y - proximaPos['y']) == 1:
                        perigoCabeca.append(direcao)
        
        sobram = []
        for d, seg in is_move_safe.items():
            if seg == True and d not in perigoCabeca:
                sobram.append(d)
                
        if len(sobram) > 0:
            for d in perigoCabeca:
                is_move_safe[d] = False

    def evitarBordas():
        movimentosPossiveis = {
            "up": {'x': my_head.x, 'y': my_head.y + 1},
            "down": {'x': my_head.x, 'y': my_head.y - 1},
            "left": {'x': my_head.x - 1, 'y': my_head.y},
            "right": {'x': my_head.x + 1, 'y': my_head.y}
        }
        
        beiradas = []
        for direcao, pos in movimentosPossiveis.items():
            if pos['x'] == 0 or pos['x'] == 10 or pos['y'] == 0 or pos['y'] == 10:
                beiradas.append(direcao)
                
        # Conta quantas saídas seguras sobram se a gente não for para a beirada
        sobram = []
        for direcao, segura in is_move_safe.items():
            if segura == True:
                if direcao not in beiradas:
                    sobram.append(direcao)
        
        # Só evita a borda se a gente tiver para onde fugir
        if len(sobram) > 0:
            for direcaoBorda in beiradas:
                temMaca = False
                posicaoBorda = movimentosPossiveis[direcaoBorda]
                
                # Checa se tem uma maçã especificamente nessa borda
                for comida in listaComida:
                    if comida.x == posicaoBorda['x'] and comida.y == posicaoBorda['y']:
                        temMaca = True
                        break
                
                # Se for seguro, mas não tiver maçã, a gente finge que a parede é perigosa
                if temMaca == False:
                    is_move_safe[direcaoBorda] = False

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

        if melhorBlocoNome:
            coordsDoBloco = blocos[melhorBlocoNome]["coords"]

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
                if is_move_safe["right"] and my_head.x < comida.x: return "right"
                if is_move_safe["left"] and my_head.x > comida.x: return "left"
                if is_move_safe["up"] and my_head.y < comida.y: return "up"
                if is_move_safe["down"] and my_head.y > comida.y: return "down"

        for comida in listaComida:
            c_dict = {'x': comida.x, 'y': comida.y}
            if c_dict in coordsDoBloco:
                macasNoDestino.append(comida)

        if macasNoDestino:
            alvo = macasNoDestino[0]
            if is_move_safe["right"] and my_head.x < alvo.x: return "right"
            if is_move_safe["left"] and my_head.x > alvo.x: return "left"
            if is_move_safe["up"] and my_head.y < alvo.y: return "up"
            if is_move_safe["down"] and my_head.y > alvo.y: return "down"

        return None

    def inimigoNoMeuBloco():
        blocoAtual = None
        head_dict = {'x': my_head.x, 'y': my_head.y}
        for nomeBloco, local in blocos.items():     
            if head_dict in local['coords']:
                blocoAtual = nomeBloco
                break
                
        if blocoAtual:
            coordsDoBloco = blocos[blocoAtual]["coords"]
            inimigos = state.board.snakes
            for inimigo in inimigos:
                if inimigo.id != state.you.id:
                    inimigoCabeca = {'x': inimigo.body[0].x, 'y': inimigo.body[0].y}
                    if inimigoCabeca in coordsDoBloco:
                        estado["emergencia"] = True
                        return
                        
        estado["emergencia"] = False

    def modoDefensivo():
        if estado["emergencia"] and len(state.you.body) >= 4:
            rabo = state.you.body[-1]
            
            if is_move_safe["right"] and my_head.x < rabo.x: return "right"
            if is_move_safe["left"] and my_head.x > rabo.x: return "left"
            if is_move_safe["up"] and my_head.y < rabo.y: return "up"
            if is_move_safe["down"] and my_head.y > rabo.y: return "down"

            for direcao, segura in is_move_safe.items():
                if segura:
                    return direcao
                    
        return None

    def deuRuimKKK():
        distancia = 9999
        alvo = None

        if desespero:
            for comida in listaComida:
                d = abs(comida.x - my_head.x) + abs(comida.y - my_head.y)
                if d < distancia:
                    distancia = d
                    alvo = comida

        if alvo:
            if is_move_safe["right"] and my_head.x < alvo.x: return "right"
            if is_move_safe["left"] and my_head.x > alvo.x: return "left"
            if is_move_safe["up"] and my_head.y < alvo.y: return "up"
            if is_move_safe["down"] and my_head.y > alvo.y: return "down"

        return None

    pontuarComida()
    acharVizinho()
    calcularInimigos()
    evitarInimigos()
    evitarBordas()      
    inimigoNoMeuBloco()

    direcao_alvo = deuRuimKKK()
    if not direcao_alvo:
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