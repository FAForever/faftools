from enum import IntEnum, unique


@unique
class VictoryCondition(IntEnum):
    DEMORALIZATION = 0
    DOMINATION = 1
    ERADICATION = 2
    SANDBOX = 3

    @staticmethod
    def from_gpgnet_string(value):
        if value == "demoralization":
            return VictoryCondition.DEMORALIZATION
        elif value == "domination":
            return VictoryCondition.DOMINATION
        elif value == "eradication":
            return VictoryCondition.ERADICATION
        elif value == "sandbox":
            return VictoryCondition.SANDBOX
