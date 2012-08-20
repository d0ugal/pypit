from celery import Task


class BaseChallenge(Task):

    def __init__(self, release):
        self.release = release

    def setup(self):
        pass

    def run(self):
        pass

    def finish(self):
        pass


class SourceChallenge(BaseChallenge):
    """
    A source challenge performs itself against the source code that is
    downloaded and stored on disk.
    """

    def setup(self):
        """
        1. Download package
        2. Extract package
        """
        super(SourceChallenge, self).setup()

    def run(self):
        super(SourceChallenge, self).run()

    def finish(self):
        """
        1. Delete package
        """
        super(SourceChallenge, self).finish()


class PythonChallenge(BaseChallenge):
    """
    A python challenge attempts to use the library in terms of running code
    and thus needs a virtualenv.
    """

    def setup(self):
        """
        1. Create virtualenv
        2. install package
        """
        super(PythonChallenge, self).setup()

    def run(self):
        super(PythonChallenge, self).run()

    def finish(self):
        """
        1. Delete virtualenv
        """
        super(PythonChallenge, self).finish()
