from enum import Enum


class OptionType(Enum):
    findelement = 0
    optiondriver = 1
if __name__ == '__main__':
    print(OptionType.findelement.value)