

class Moon:

    """
    from: https://he.wikipedia.org/wiki/%D7%94%D7%99%D7%A8%D7%97
    """

    RADIUS = 1.7374e6           # meters
    ACC = 1.622                 # m / s ^ 2
    EQ_SPEED = 1700             # m / s
    MASS = 7.3477e22            # KG
    # G = 6.67e-11

    @staticmethod
    def getAcc(speed):
        return (1 - abs(speed) / Moon.EQ_SPEED) * Moon.ACC
