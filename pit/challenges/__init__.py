

class BaseChallenge(object):

    def __init__(self, release):
        self.release = release

    def setup(self):
        pass

    def run(self):
        pass

    def finish(self):
        pass
