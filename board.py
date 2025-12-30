from tile import Tile
import random

class Board:
    def __init__(self, size: tuple[int, int], n_mines: int = -1):
        """
        Generate a minesweeper board with the given dimensions and number of tiles.

        Args:
            size (tuple[int, int]): The dimensions of the board.
            n_mines (int): The number of mines on the board. If n_mines < 0, a default value making the total ratio of mines/total_tiles 2/9. e.g. a board of size (30, 30) would get a mine count of 200.
        """

        board_x, board_y = size
        n_tiles = board_x*board_y
        if (n_mines < 0) or (n_mines > n_tiles//2):
            n_mines = (n_tiles*2) // 9
        tiles = []
        n_non_mines = n_tiles-n_mines
        n_mines_to_place = n_mines
        
        for row in range(board_y):
            new_row = []
        
            for column in range(board_x):
                is_mine = random.choice([False]*n_non_mines+[True]*n_mines_to_place)
                new_mine = Tile(is_mine)

                if is_mine:
                    n_mines_to_place -= 1
                else:
                    n_non_mines -= 1
                n_tiles -= 1

                new_row.append(new_mine)

            tiles.append(new_row)

        self.tiles = tiles
        self.n_tiles = n_tiles
        self.n_mines = n_mines
        self.n_non_mines = n_tiles - n_mines
        self.size = size

        # Calculate number of mines around each tile
        for y in range(board_y):
            for x in range(board_x):
                tile = tiles[y][x]
                tile.n_mines_around = self.calculate_n_mines_around((x, y))

    def get(self, pos: tuple[int, int]) -> Tile:
        """
        Get the tile at the given position.

        Args:
            pos (tuple[int, int]): The (x, y) position of the tile to get.

        Returns:
            Tile: The tile at the given position.
        """
        x, y = pos
        return self.tiles[y][x]

        
    def calculate_n_mines_around(self, tile_pos: tuple[int, int]) -> int:
        """
        Calculate the number of mines around a tile.

        Args:
            board (Board): A minesweeper board.
            tile_pos (tuple[int, int]): The position of the tile in question, measured in tiles

        Returns:
            int: The number of mines surrounding the given tile.
        """

        n_mines_around = 0
        tile_x, tile_y = tile_pos
        adjacent_columns = [tile_x]
        adjacent_rows = [tile_y]
        board_width, board_height = self.size
        
        if tile_x > 0:
            adjacent_columns.append(tile_x - 1)
        if tile_x < board_width-1:
            adjacent_columns.append(tile_x + 1)
        if tile_y > 0:
            adjacent_rows.append(tile_y - 1)
        if tile_y < board_height-1:
            adjacent_rows.append(tile_y + 1)
        
        for x in adjacent_columns:
            for y in adjacent_rows:
                if self.get((x, y)).is_mine:
                    n_mines_around += 1

        return n_mines_around

