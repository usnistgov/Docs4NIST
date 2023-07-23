class File:
    def __init__(self):
        pass

    @property
    def path(self):
        raise NotImplementedError

    def get_contents(self):
        return ""

    def write(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open(mode='w') as file:
            file.write(self.get_contents())
