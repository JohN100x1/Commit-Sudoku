from random import randint


class Factory:
    @staticmethod
    def create_random_board():
        return [[randint(1, 9) for _ in range(9)] for _ in range(9)]

    @staticmethod
    def create_empty_board():
        return [[0 for _ in range(9)] for _ in range(9)]
