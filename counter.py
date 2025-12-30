class Counter:
    """
    A simple counter class.

    Attributes:
        value (int): The current value of the counter.
        screen_pos (tuple[int, int]): The position on the screen where the counter is displayed, measured in px. This is where the top left of the counter will be drawn.
    """

    def __init__(self, screen_pos: tuple[int, int], size: tuple[int, int], start_value: int = 0):
        """
        Args:
            screen_pos (tuple[int, int]): The position on the screen where the counter is displayed, measured in px. This is where the top left of the counter will be drawn. Given as (x, y).
            size (tuple[int, int]): The size of one digit on the counter, measured in px. Given as (width, height).
            start_value (int): The starting value of the counter. Default is 0.
        """
        self.size = size
        self.screen_pos = screen_pos
        self.value = start_value

    def increment(self, amount: int = 1) -> None:
        """
        Increment the counter by the given amount.

        Args:
            amount (int): The amount to increment the counter by. Default is 1.
        """
        self.value += amount

    def decrement(self, amount: int = 1) -> None:
        """
        Decrement the counter by the given amount.

        Args:
            amount (int): The amount to decrement the counter by. Default is 1.
        """

        self.value -= amount

    def set(self, new_value: int = 0) -> None:
        """
        Set the counter to the given value.

        Args:
            new_value (int): The value to set the counter to. Default is 0.
        """
        self.value = new_value