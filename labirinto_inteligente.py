# -*- coding: utf-8 -*-
"""
IA - AVALIAÇÃO UNIDADE 2

Desafio do Labirinto Inteligente

Implementar um agente racional capaz de encontrar o caminho mais curto através
de um labirinto, utilizando técnicas de resolução de problemas.
"""

# Importanto bibliotecas numpy, clear_output, copy e time
import numpy as np
from IPython.display import clear_output
import copy, time, os


# Classe estática de labirintos
class Mazes:

  size = 5 # Tamanho padrão do labirinto
  maze = np.empty([size*3, size*3],dtype=str) # Labirinto vazio

  start = [1,size*3-2] # Posição inicial padrão
  goal = [1,1] # Posição inicial padrão

    # As posições iniciais e finais são redefinidas no método carve_maze
    # Para alterá-las, edite dentro do método

  # Método público de gerar labirinto
  @staticmethod
  def generate(size=5):
    Mazes.maze = Mazes.__carve_maze(size)

  # Método privado de gerar labirinto
    # Utiliza um algoritmo de árvore binária
    # Referência: https://python.plainenglish.io/maze-generation-algorithms-with-matrices-in-python-i-33bc69aacbc4
  @staticmethod
  def __carve_maze(size=5):
    n = 1
    p = 0.5
    grid = np.random.binomial(n,p, size=(size,size))

    first_row = grid[0]
    first_row[first_row == 1] = 0
    grid[0] = first_row
    for i in range(1,size):
      grid[i,size-1] = 1

    Mazes.size = size
    Mazes.start = [1,size*3-2]
    Mazes.goal = [1,1]

    output_grid = np.empty([size*3, size*3],dtype=str)
    output_grid[:] = ':'
    i = 0
    j = 0
    while i < size:
      w = i*3 + 1
      while j < size:
        k = j*3 + 1
        toss = grid[i,j]
        output_grid[w,k] = ' '
        if toss == 0 and k+2 < size*3:
          output_grid[w,k+1] = ' '
          output_grid[w,k+2] = ' '
        if toss == 1 and w-2 >=0:
          output_grid[w-1,k] = ' '
          output_grid[w-2,k] = ' '
        j = j + 1
      i = i + 1
      j = 0

    # Define visualmente a posição inicial e final
    output_grid[Mazes.start[1],Mazes.start[0]-1] = '<'
    output_grid[Mazes.goal[1],Mazes.goal[0]-1] = '<'

    return output_grid

  # Imprime o labirinto e o mapa de posições visitadas
  @staticmethod
  def print_raw(visited):
    clear_output()
    os.system('cls')

    for i in range(len(Mazes.maze)):
      line = " ".join(Mazes.maze[i])
      line += "  "
      for j in range(len(visited[i])):
        if visited[i][j] == "V":
          line += "■"
        else:
          line += "□"
      print(line)

  # Imprime o labirinto, o mapa de posições visitadas e o caminho mais curto
  @staticmethod
  def print_shortest(visited, path):
    clear_output()
    os.system('cls')

    for i in range(len(Mazes.maze)):
      line = " ".join(Mazes.maze[i])
      line += "  "
      for j in range(len(visited[i])):
        if visited[i][j] == "V":
          line += "■"
        else:
          line += "□"
      line += "  "
      for j in range(len(path[i])):
        if path[i][j] == "V":
          line += "■"
        else:
          line += "□"
      print(line)

  # Imprime o labirinto e o caminho mais curto, posicionando uma caractere
  # especial na posição atual do agente
  @staticmethod
  def print_agent(x, y, path):
    temp = copy.copy(Mazes.maze)
    temp[y,x] = '✪'

    clear_output()
    os.system('cls')

    for i in range(len(temp)):
      line = " ".join(temp[i])
      line += "  "
      for j in range(len(path[i])):
        if path[i][j] == "V":
          line += "■"
        else:
          line += "□"
      print(line)

# Classe estática que controla o algoritmo de busca em largura
class BFS:

  start_time = 0 # Tempo inicial da execução
  end_time = 0 # Tempo final da execução

  shortest_path = [] # Vetor que armazenará o caminho mais curto

  # Método público para iniciar o BFS
  @staticmethod
  def start ():
    queue = []
    visited = np.empty([Mazes.size*3, Mazes.size*3],dtype=str)
    BFS.start_time = time.perf_counter()
    BFS.find(Mazes.start[0], Mazes.start[1], queue, visited)

  # Método para encontrar as próximas posições possíveis para a busca
    # Há um viés de qual direção o agente irá seguir por conta
    # da ordem de execução do script
  @staticmethod
  def neighbors (x, y, visited):
    output = [] # Vetor de próximas posições possíveis

    # Vizinho de cima
    if Mazes.maze[y-1][x] == ' ' and visited[y-1][x] != 'V':
      output.append([x,y-1])
    # Vizinho da direita
    if Mazes.maze[y][x+1] == ' ' and visited[y][x+1] != 'V':
      output.append([x+1,y])
    # Vizinho de baixo
    if Mazes.maze[y+1][x] == ' ' and visited[y+1][x] != 'V':
      output.append([x,y+1])
    # Vizinho da esquerda
    if Mazes.maze[y][x-1] == ' ' and visited[y][x-1] != 'V':
      output.append([x-1,y])

    return output

  # Método recursivo do BFS
  @staticmethod
  def find (x, y, queue, visited):

    # Imprime o estado atual da busca
    Mazes.print_raw(visited)

    visited[y][x] = 'V' # Marca a posição atual como visitada
    queue.append([x,y]) # Adiciona a posição atual na fila

    # Checa se o agente não está na posição final antes de continuar
    if (x != Mazes.goal[0] or y != Mazes.goal[1]):

      neighbors = BFS.neighbors(x, y, visited) # Encontra as próximas posições possíveis
      print(neighbors)

      # Checa se há vizinhos disponíveis antes de prosseguir
      if len(neighbors) > 0:

        # Continua a recursão seguindo para o primeiro vizinho disponível
        BFS.find(neighbors[0][0], neighbors[0][1], queue, visited)

      else:

        # Caso não há vizinhos disponíveis e a fila não esteja vazia
        if len(queue) > 1:

          # Retornar uma posição na fila
          queue.pop()
          next = queue.pop()
          BFS.find(next[0], next[1], queue, visited)

        else:

          # Caso contrário não há caminhos a seguir
          print("Sem caminhos possíveis")

    else:

      BFS.end_time = time.perf_counter() # Marca o tempo final do BFS
      elapsed_time = BFS.end_time - BFS.start_time # Calcula o tempo de execução

      BFS.shortest_path = queue # Usa a fila final como caminho mais curto

      # Cria uma matriz marcando as posições do caminho final para
      # facilitar a visualização
      path_matrix = np.empty([Mazes.size*3, Mazes.size*3],dtype=str)
      for vector in BFS.shortest_path:
        path_matrix[vector[1]][vector[0]] = "V"

      # Imprime o resultado final da busca
      Mazes.print_shortest(visited, path_matrix)
      print("           [LABIRINTO  -  EXPLORAÇÃO (BFS)  -  CAMINHO MAIS CURTO]")
      print("")
      print(f"Labirinto mais curto encontrado em {round(elapsed_time, 2)} seg")
      print("Aguarde 15 seg para a demonstração do caminho")
      time.sleep(15)

      # Segue para a demonstração depois de 15 segundos
      BFS.follow(path_matrix)

  # Método para demonstrar visualmente o caminho mais curto
  def follow (path_matrix):

    path = BFS.shortest_path # Caminho mais curto

    # Para cada posição do caminho mais curto mostrar uma representação
    # visual do agente se movendo pelo caminho
    for i in range(len(path)):
      time.sleep(0.5)
      Mazes.print_agent(path[i][0], path[i][1], path_matrix)

    # Aguardar 10 segundos para fechar o programa
    time.sleep(10)

# Parte principal da execução
print("DESAFIO DE LABIRINTO INTELIGENTE")
print("")

maze_size = 0
while type(maze_size) is not int or maze_size <= 1 or maze_size >= 16:
  try:
    maze_size = int(input("Tamanho do labirinto:"))
    if maze_size <= 1 or maze_size >= 16:
      raise Exception("Use um número entre 2 e 15")
  except ValueError:
    print("Use um número inteiro")
    print("")
  except Exception as e:
    print(e)
    print("")

Mazes.generate(maze_size)
BFS.start()