from controllers.base import Controllers
from models.base import Tournament


def main():
    tournament = Tournament(date="date", name="name",  place="place", description="description",
                            time_control="time control")
    controller = Controllers(tournament)
    controller.run()


if __name__ == "__main__":
    main()
