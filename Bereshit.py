
class Bereshit:
    """
    This class represents the basic flight controller of the Bereshit space craft.
    """

    WEIGHT_EMP = 165  # KG
    WEIGHT_FUEL = 420  # KG
    WEIGHT_FULL = WEIGHT_EMP + WEIGHT_FUEL  # KG

    # https://davidson.weizmann.ac.il/online/askexpert/%D7%90%D7%99%D7%9A-%D7%9E%D7%98%D7%99%D7%A1%D7%99%D7%9D-%D7%97%D7%9C%D7%9C%D7%99%D7%AA-%D7%9C%D7%99%D7%A8%D7%97

    MAIN_ENG_F = 430  # N
    SECOND_ENG_F = 25  # N
    ALL_F = MAIN_ENG_F + 8 * SECOND_ENG_F   # 630 N
    MAIN_BURN = 0.15  # Liter per sec, 12 Liter per minute
    SECOND_BURN = 0.009  # Liter per sec, 0.6 Liter per minute
    ALL_BURN = MAIN_BURN + 8 * SECOND_BURN

    def __init__(self):
        self.vs = 24.3  # vertical speed
        self.hs = 10  # horizontal speed
        self.acc = 0  # acceleration
        self.ang = 58.3  # angel to the planet
        self.alt = 50_000  # altitude
        self.fuel = 121
        self.weight = self.WEIGHT_EMP + self.fuel
        self.EnginePower = 1  # [0, 1]

    @staticmethod
    def accelerate(weight, main, seconds):
        t = 0

        if main:
            t += Bereshit.MAIN_ENG_F

        t += seconds * Bereshit.SECOND_ENG_F

        return t / weight
