from app.challenges import BaseChallenge


class SetupChallenge(BaseChallenge):

    def setup(self):
        # 1. create virtualenv template
        pass

    def run(self):
        # 1. Download package
        # 2. clone virtualenv
        # 2. Install package into virtualenv (use pip as a lib?)
        # 3. Verify installation worked - try importing? Check for an bin
        #    files (like django-admin.py)
        # 4. delete virtualenv
        pass

    def finish(self):
        # 1. delete virtualenv template
        pass
