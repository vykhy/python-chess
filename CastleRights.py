
class CastleRights():
    def __init__(self, wks, wqs, bks, bqs):
        self.wks = wks
        self.wqs = wqs
        self.bks = bks
        self.bqs = bqs
    
    def __str__(self) -> str:
        return f"{self.wks}, {self.wqs}, {self.bks}, {self.bqs}"
