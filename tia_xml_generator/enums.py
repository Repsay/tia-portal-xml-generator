from enum import Enum

class ProgrammingLanguage(Enum):
    LAD = 1
    FBD = 2

class Remanence(Enum):
    SetInIDB = 1
    NonRetain = 2
    Retain = 3

class Accessibility(Enum):
    Public = 1
    Internal = 2
    Protected = 3
    Private = 4