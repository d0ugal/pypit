from pkgutil import iter_modules

from pit import challenges
from pit.challenges import BaseChallenge


class Runner(object):

    def find_challenges(self):
        # Yay. Magic. \o/
        prefix = challenges.__name__ + "."
        list(iter_modules(challenges.__path__, prefix))
        return BaseChallenge.__subclasses__()

    def run(self, package_release):

        challenge_classes = self.find_challenges()

        all_challenges = [C(package_release) for C in challenge_classes]

        for challenge in all_challenges:
            challenge.setup()

        for challenge in all_challenges:
            challenge.run()

        for challenge in all_challenges:
            challenge.finish()
