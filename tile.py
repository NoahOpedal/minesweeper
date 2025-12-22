import pygame

import functions

class Tile():
    """
    A class representing a minesweeper tile.

    Attributes:
        clicked (bool): Whether the tile has been clicked.
        flagged (bool): Whether the tile has been flagged.
        is_mine (bool): Whether the tile is a mine.
        n_mines_around (int): The number of mines around the tile.
    """

    def __init__(self, is_mine: bool):
        self.clicked = False
        self.flagged = False
        self.is_mine = is_mine
        self.n_mines_around = 0


    def draw(self, pos: tuple[int, int], size: tuple[int, int], screen: pygame.Surface, clicked_color: str = "white", unclicked_color: str = "light grey", flagged_color: str = "red", font_size: int = 12) -> None:
        """
        Draw the tile on the given screen.
        Args:
            pos (tuple[int, int]): The (x, y) position to draw the tile at.
            size (tuple[int, int]): The (width, height) size of the tile.
            screen (pygame.Surface): The surface to draw the tile on.
            clicked_color (str): The color of a clicked tile. Default is "white". Should be a valid pygame color.
            unclicked_color (str): The color of an unclicked tile. Default is "light grey". Should be a valid pygame color.
            flagged_color (str): The color of a flagged tile. Default is "red". Should be a valid pygame color.
            font_size (int): The font size for the number of mines around. Default is 12.
        """
        x, y = pos
        width, height = size
        if self.flagged:
            color = flagged_color
        #elif self.is_mine:     # For debugging
        #    color = "black"
        elif self.clicked:
            color = clicked_color
        else:
            color = unclicked_color

        pygame.draw.rect(screen, color, (x, y, width, height))        

        if self.n_mines_around != 0 and self.clicked:
            font = pygame.font.Font(None, font_size)
            number_text = font.render(str(self.n_mines_around), True, "black")
            text_rect = number_text.get_rect(center=((width//2)+x, (height//2)+y))
            screen.blit(number_text, text_rect)