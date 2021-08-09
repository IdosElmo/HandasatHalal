
class PidController:

    def __init__(self, P, I, D, oMax, oMin):
        # The proportional term produces an output value that
        # is proportional to the current error value
        self.__GainP = P

        # The integral term is proportional to both the magnitude
        # of the error and the duration of the error
        self.__GainI = I

        # The derivative term is proportional to the rate of
        # change of the error
        self.__GainD = D

        # The max output value the control device can accept.
        self.__outputMax = oMax

        # The minimum ouput value the control device can accept.
        self.__outputMin = oMin

        # Adjustment made by considering the accumulated error over time
        # An alternative formulation of the integral action, is the
        # proportional-summation-difference used in discrete-time systems
        self.__integralTerm = 0

        self.__processVar = 0

        # The last reported value (used to calculate the rate of change)
        self.__processVarLast = 0

        # The desired value
        self.__setPoint = 0

    def control(self, dt):
        error = self.__setPoint - self.__processVar

        self.__integralTerm += self.__GainI * error * dt
        self.__integralTerm = self.clamp(self.__integralTerm)

        return self.clamp(self.__GainP * error)

    def setProcessVar(self, val):
        self.__processVarLast = self.__processVar
        self.__processVar = val

    def clamp(self, var):
        """
        Limit a variable to the set OutputMax and OutputMin properties
        :param var: variable to be clamped
        :return: A value that is between the OutputMax and OutputMin properties
        """
        return self.__outputMin if var <= self.__outputMin else self.__outputMax if var >= self.__outputMax else var
