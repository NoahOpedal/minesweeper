import pygame
import time

from board import Board
from counter import Counter


def open_adjacent_zeroes(tile_pos: tuple[int, int], board: Board) -> None:
    """
    Recursively open all adjacent tiles with 0 mines around.
    
    Args:
        tile_pos (tuple[int, int]): The position of the tile to start from.
        board (Board): A minesweeper board.
    """
    tile_x, tile_y = tile_pos
    adjacent_cols = [tile_x]
    adjacent_rows = [tile_y]
    board_width, board_height = board.size
    
    if tile_x > 0:
        adjacent_cols.append(tile_x - 1)
    if tile_x < board_width-1:
        adjacent_cols.append(tile_x + 1)
    if tile_y > 0:
        adjacent_rows.append(tile_y - 1)
    if tile_y < board_height-1:
        adjacent_rows.append(tile_y + 1)


    for row in adjacent_rows:
        for col in adjacent_cols:
            tile = board.get((col, row))

            if not tile.clicked:
                tile.clicked = True
                if tile.n_mines_around==0 and not tile.is_mine:
                    open_adjacent_zeroes((col, row), board)


def update_screen(screen: pygame.Surface, board: Board, tile_size: tuple[int, int], timer: Counter, mine_counter: Counter, background_color: str = "dark grey") -> None:
    """
    Update the pygame screen.

    Args:
        screen (pygame.display): The screen to update.
        board (Board): A minesweeper board.
        tile_size (tuple[int, int]): The size of a tile, in px.
        background_color (str): The background color. Defaults to dark grey. Must be in pygame's list of accepted colors.
    """

    screen.fill(background_color)

    tile_x, tile_y = 1, 1
    tile_width, tile_height = tile_size
    for row in board.tiles:
        for tile in row:
            tile.draw((tile_x+1, tile_y+1), (tile_width-2, tile_height-2), screen, font_size=20)
            tile_x += tile_width
        
        tile_x = 1
        tile_y += tile_height
        
    timer_text = pygame.font.Font(None, 36).render(f"Time: {timer.value}", True, "red")
    screen.blit(timer_text, timer.screen_pos)
    mine_counter_text = pygame.font.Font(None, 36).render(f"Mines: {mine_counter.value}", True, "red")
    screen.blit(mine_counter_text, mine_counter.screen_pos)


def spacebar_functionality(tile_pos: tuple[int, int], board: Board) -> str|None:
    """
    When spacebar is pressed while hovering over an opened tile, click all tiles around if number of flags around match the number on the tile.

    Args:
        tile_pos (tuple[int, int]): The position of the tile being pressed spacebar on.
        board (Board): A minesweeper board.

    Returns:
        str|None: "exploded" if a mine was revealed, None otherwise.
    """

    tile_x, tile_y = tile_pos
    adjacent_cols = [tile_x]
    adjacent_rows = [tile_y]
    board_width, board_height = board.size
    
    if tile_x > 0:
        adjacent_cols.append(tile_x - 1)
    if tile_x < board_width-1:
        adjacent_cols.append(tile_x + 1)
    if tile_y > 0:
        adjacent_rows.append(tile_y - 1)
    if tile_y < board_height-1:
        adjacent_rows.append(tile_y + 1)

    number_of_adjacent_flags = 0
    n_mines_around = board.get((tile_x, tile_y)).n_mines_around

    for col in adjacent_cols:
        for row in adjacent_rows:
            if board.get((col, row)).flagged:
                number_of_adjacent_flags += 1
    
    if number_of_adjacent_flags == n_mines_around:
        for row in adjacent_rows:
            for col in adjacent_cols:
                tile = board.get((col, row))

                if not tile.flagged:
                    tile.clicked = True
                    if tile.is_mine:
                        return "exploded"
                    elif tile.n_mines_around == 0:
                        open_adjacent_zeroes((col, row), board)


def update_game(board: Board, click: bool, flag: bool, tile_clicked_pos: tuple[int, int]) -> str|None:
    """
    Update the game state after an action has occured. The action is either a mouse click or a spacebar click.

    Args:
        board (Board): A minesweeper board.
        click (bool): Whether a mouse click occured. Either this or flag should be False.
        flag (bool): Whether a flag action (spacebar press) occured. Either this or click should be False.
        tile_clicked_pos (tuple[int, int]): The position(col, row) of the tile that was clicked/flagged.

    Returns:
        str|None: "explosion" if a mine was clicked, None otherwise.
    """

    if click:
        tile = board.get(tile_clicked_pos)
        tile.clicked = True

        if tile.is_mine:
            return "exploded"
        
        elif tile.n_mines_around == 0:
            open_adjacent_zeroes(tile_clicked_pos, board)

    if flag:
        tile = board.get(tile_clicked_pos)
        if not tile.clicked:
            tile.flagged = not tile.flagged
        else:
            if spacebar_functionality(tile_clicked_pos, board) == "exploded":
                return "exploded" 
        

def regenerate_board(board: Board, n_mines: int, tile_clicked_pos: tuple[int, int]) -> Board:
    """
    Regenerate the board until the tile revealed by a given click is a 0.

    Args:
        tile_size (tuple[int, int]): The height and width of a tile, in px.
        board (Board): A minesweeper board.
        n_mines (int): The number of mines on the new board. Should be the same as the mine count of the original board.    TODO: replace this with get_mine_count function from board class.

    Returns:
        A minesweeper board.
    """
    board_width, board_height = board.size

    while not board.get(tile_clicked_pos).n_mines_around == 0 or board.get(tile_clicked_pos).is_mine:
        board = Board((board_width, board_height), n_mines=n_mines)
    
    return board


def game_loop():
    fps = 60
    board_width = 10    # Tiles
    board_height = 10
    window_width = 800  # Px. Because of a pygame rounding error the window width must be a multiple of the board width. The same applies to height.
    window_height = 800 # Px.
    info_display_height = 200   # Px. Height of the display for timer and mine count
    tile_width = (window_width//board_width)
    tile_height = (window_height//board_height)
    n_mines = -1

    screen = pygame.display.set_mode((window_width, window_height+info_display_height))
    pygame.display.set_caption("Minesweeper")
    board = Board((board_width, board_height), n_mines=n_mines)

    mine_counter = Counter((50, window_height + 50), (50, 100), start_value=board.n_mines)
    timer = Counter((window_width - 200, window_height + 50), (50, 100))

    start_time = pygame.time.get_ticks()  # milliseconds

    running = True
    first_click = True

    while running:
        flag = False
        click = False
        tile_clicked_pos = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                mouse_position = pygame.mouse.get_pos()
                tile_clicked_pos = (
                    int(mouse_position[0]//tile_width), 
                    int(mouse_position[1]//tile_height)
                )
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                flag = True
                mouse_position = pygame.mouse.get_pos()
                tile_clicked_pos = (
                    int(mouse_position[0]//tile_width), 
                    int(mouse_position[1]//tile_height)
                )

        if tile_clicked_pos and board.get(tile_clicked_pos).is_mine and click:
            # Make sure first click is always playable
            if first_click:
                board = regenerate_board(board, n_mines, tile_clicked_pos)
                update_game(board, click, flag, tile_clicked_pos)
            else:
                print("*explosion*")
                running = False

        elif click and first_click and tile_clicked_pos and not board.get(tile_clicked_pos).n_mines_around == 0:
            board = regenerate_board(board, n_mines, tile_clicked_pos)
            if update_game(board, click, flag, tile_clicked_pos) == "exploded":
                print("*explosion*")
                running = False


        elif tile_clicked_pos:
            if update_game(board, click, flag, tile_clicked_pos) == "exploded":
                print("*explosion*")
                running = False

        if first_click and tile_clicked_pos:
            first_click = False

        time_elapsed = (pygame.time.get_ticks() - start_time) // 1000  # seconds
        timer.set(time_elapsed)
        mine_counter.set(board.n_mines - sum(1 for row in board.tiles for tile in row if tile.flagged))

        update_screen(screen, board, (tile_width, tile_height), timer, mine_counter)

        pygame.display.flip()
        time.sleep(1/fps)