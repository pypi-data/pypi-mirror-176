class web3ConnectionError(Exception):
    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.link = args[0] if args else None
    
    def __str__(self) -> str:
        return f"Check the link - {self.link}!"