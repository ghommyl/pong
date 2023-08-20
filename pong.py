import logging
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)-7s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

from game import Game

game = Game()
game.run()
