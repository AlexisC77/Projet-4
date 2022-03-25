from controllers.base import Controllers
from views.base import create_tournament


def main():
    tournament = create_tournament()
    controller = Controllers(tournament)
    controller.run()


if __name__ == "__main__":
    main()
