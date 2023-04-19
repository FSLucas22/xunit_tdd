class Log:
    executed: str

    def __init__(self) -> None:
        self.executed = ""
        
    def register(self, name: str) -> None:
        if self.executed != "":
            self.executed += " "
        self.executed += name

    def register_count(self) -> int:
        return len(self.executed.split())
