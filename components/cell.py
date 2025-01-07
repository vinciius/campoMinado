class Cell:
    def __init__(self, is_mine=False):
        self.is_mine = is_mine  # Indica se a célula contém uma mina
        self.mine_count = 0     # Contagem de minas ao redor
        self.is_revealed = False # Indica se a célula foi revelada

    def count_mines_around(self, board, x, y):
        # Contar minas ao redor da célula (x, y)
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),         (0, 1),
                      (1, -1), (1, 0), (1, 1)]
        count = 0
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(board) and 0 <= ny < len(board[0]):
                if board[nx][ny].is_mine:
                    count += 1
        self.mine_count = count