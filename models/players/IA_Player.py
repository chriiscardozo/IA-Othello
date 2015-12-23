class IA_Player:

#  def __init__(self, color):
#    self.color = color


#  import random

#  def play(self, board):
#    return self.random.choice(board.valid_moves(self.color))

  def __init__(self, color):
    self.color = color
    self.X1 = [-1,-1,0,1,1,1,0,-1]
    self.Y1 = [0,1,1,1,0,-1,-1,-1]
    self.V = [None,None,None,None,None,None,None,None]
    self.V[0] = [ 30, -25, 10, 5, 5, 10, -25,  30]
    self.V[1] = [-25, -25,  1, 1, 1,  1, -25, -25]
    self.V[2] = [ 10,   1,  5, 2, 2,  5,   1,  10]
    self.V[3] = [  5,   1,  2, 1, 1,  2,   1,   5]
    self.V[4] = [  5,   1,  2, 1, 1,  2,   1,   5]
    self.V[5] = [ 10,   1,  5, 2, 2,  5,   1,  10]
    self.V[6] = [-25, -25,  1, 1, 1,  1, -25, -25]
    self.V[7] = [ 30, -25, 10, 5, 5, 10, -25,  30]
    self.gerados = 0

  def play(self, board):
    score = board.score()
    livres = 64 - score[0] - score[1]
    depth = 3

    self.gerados = 0
    if(livres < 7):
      depth = 5

    return self.alphabeta(board, depth, -float("inf"), float("inf"), (self.color == '@'))[1]

  def alphabeta(self, board, depth, alfa, beta, maxPlayer):
    if(depth <= 0 and self.gerados > 100):
      return [self.h(board), None];

    if(maxPlayer):
      childs = board.valid_moves('@')
      self.gerados += len(childs)
      if(len(childs) == 0):
        return [self.h(board), None]

      jogada = [None,None]
      jogada[0] = -float("inf")

      for child in childs:
        temp_board = board.get_clone()
        temp_board.play(child, '@')

        jogadaAtual = self.alphabeta(temp_board, depth-1, alfa, beta, False)
        jogadaAtual[1] = child

        if(jogadaAtual[0] > jogada[0]):
          jogada = jogadaAtual

        alfa = max(alfa, jogada[0])
        if(beta <= alfa):
          break

      return jogada
    else:
      childs = board.valid_moves('o')
      self.gerados += len(childs)
      if(len(childs) == 0):
        return [self.h(board), None]

      jogada = [None, None]
      jogada[0] = float("inf")

      for child in childs:
        temp_board = board.get_clone()
        temp_board.play(child, 'o')

        jogadaAtual = self.alphabeta(temp_board, depth-1, alfa, beta, True)
        jogadaAtual[1] = child

        if(jogadaAtual[0] < jogada[0]):
          jogada = jogadaAtual

        beta = min(beta, jogada[0])
        if(beta <= alfa):
          break

      return jogada


  def h(self, board):
    score = board.score()
    livres = 64 - score[0] - score[1]

    return (10*self.h_qtd_pecas(board)) + (801.724*self.h_dominio_corner(board)) + (382.026*self.h_prox_corner(board)) + (78.922*self.h_mobilidade(board)) + (74.396*self.h_fronteira(board)) +  (10*self.h_posicional(board))
    #if(livres > 55):
    #  return -100*self.h_qtd_pecas(board) + (801.724*self.h_dominio_corner(board)) + (382.026*self.h_prox_corner(board))
    #elif(livres >= 15 and livres <= 55):
    #  return (10*self.h_qtd_pecas(board)) + (10*self.h_posicional(board)) + (801.724*self.h_dominio_corner(board)) + (382.026*self.h_prox_corner(board))
    #else:
    #  return (78.922*self.h_mobilidade(board)) + (10*self.h_qtd_pecas(board)) + (10*self.h_posicional(board)) + (801.724*self.h_dominio_corner(board)) + (382.026*self.h_prox_corner(board))


  def h_mobilidade(self, board):
    maxi = len(board.valid_moves('@'))
    mini = len(board.valid_moves('o'))

    if(maxi == 0 and mini == 0):
      score = board.score()
      if(score[0] > score[1]):
        return 100
      elif(score[1] > score[0]):
        return -100
      else:
        return 0

    if(maxi > mini):
      return 100*(maxi/(maxi+mini))
    elif(maxi < mini):
      return -100*(mini/(maxi+mini))
    else:
      return 0

  def h_qtd_pecas(self, board):
  	score = board.score()
  	maxi_score = score[0]
  	mini_score = score[1]

  	if(maxi_score > mini_score):
  		return 100.0*(maxi_score/(maxi_score+mini_score))
  	else:
  		return -100.0*(mini_score/(mini_score+maxi_score))

  def h_dominio_corner(self, board):
  	black = white = 0
  	if(board.get_square_color(0,0) == '@'):
  		black += 1
  	elif(board.get_square_color(0,0) == 'o'):
  		white += 1
  	if(board.get_square_color(0,7) == '@'):
  		black += 1
  	elif(board.get_square_color(0,7) == 'o'):
  		white += 1
  	if(board.get_square_color(7,0) == '@'):
  		black += 1
  	elif(board.get_square_color(7,0) == 'o'):
  		white += 1
  	if(board.get_square_color(7,7) == '@'):
  		black += 1
  	elif(board.get_square_color(7,7) == 'o'):
  		white += 1

  	return 25.0 * (black-white)

  def h_prox_corner(self, board):
  	black = white = 0
  	if(board.get_square_color(0,0) == '.'):
  		if(board.get_square_color(0,1) == '@'):
  			black += 1
  		elif(board.get_square_color(0,1) == 'o'):
  			white += 1
  		if(board.get_square_color(1,1) == '@'):
  			black += 1
  		elif(board.get_square_color(1,1) == 'o'):
  			white += 1
  		if(board.get_square_color(1,0) == '@'):
  			black += 1
  		elif(board.get_square_color(1,0) == 'o'):
  			white += 1
  	if(board.get_square_color(0,7) == '.'):
  		if(board.get_square_color(0,6) == '@'):
  			black += 1
  		elif(board.get_square_color(0,6) == 'o'):
  			white += 1
  		if(board.get_square_color(1,6) == '@'):
  			black += 1
  		elif(board.get_square_color(1,6) == 'o'):
  			white += 1
  		if(board.get_square_color(1,7) == '@'):
  			black += 1
  		elif(board.get_square_color(1,7) == 'o'):
  			white += 1
  	if(board.get_square_color(7,0) == '.'):
  		if(board.get_square_color(7,1) == '@'):
  			black += 1
  		elif(board.get_square_color(7,1) == 'o'):
  			white += 1
  		if(board.get_square_color(6,1) == '@'):
  			black += 1
  		elif(board.get_square_color(6,1) == 'o'):
  			white += 1
  		if(board.get_square_color(6,0) == '@'):
  			black += 1
  		elif(board.get_square_color(6,0) == 'o'):
  			white += 1
  	if(board.get_square_color(7,7) == '.'):
  		if(board.get_square_color(6,7) == '@'):
  			black += 1
  		elif(board.get_square_color(6,7) == 'o'):
  			white += 1
  		if(board.get_square_color(6,6) == '@'):
  			black += 1
  		elif(board.get_square_color(6,6) == 'o'):
  			white += 1
  		if(board.get_square_color(7,6) == '@'):
  			black += 1
  		elif(board.get_square_color(7,6) == 'o'):
  			white += 1

  	return -12.5 * (black - white)

  def h_posicional(self, board):
    d = 0
    for i in range (0, 7):
      for j in range (0, 7):
        if(board.get_square_color(i,j) == self.color):
          d += self.V[i][j]
        elif(board.get_square_color(i,j) != self.color and board.get_square_color(i,j) != '.'):
          d -= self.V[i][j]

    return d

  def h_fronteira(self, board):
    black_front_tiles = 0
    white_front_tiles = 0

    for i in range(0, 7):
      for j in range(0, 7):
        if(board.get_square_color(i,j) == '.'):
          for k in range(0,7):
            x = i + self.X1[k]
            y = j + self.Y1[k]
            if(x >= 0 and x < 8 and y >= 0 and y < 8 and board.get_square_color(x,y) == '.'):
              if(board.get_square_color(i,j) == '@'):
                black_front_tiles += 1
              else:
                white_front_tiles += 1
              break

    if(black_front_tiles > white_front_tiles):
      return -100*(black_front_tiles)/(black_front_tiles+white_front_tiles)
    elif(black_front_tiles < white_front_tiles):
      return 100*(white_front_tiles)/(black_front_tiles+white_front_tiles)
    else:
      return 0
