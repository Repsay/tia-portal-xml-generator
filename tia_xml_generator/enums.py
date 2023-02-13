from enum import Enum


class ProgrammingLanguage(Enum):
    LAD = 1
    FBD = 2
    DB = 3


class Remanence(Enum):
    SetInIDB = 1
    NonRetain = 2
    Retain = 3


class Accessibility(Enum):
    Public = 1
    Internal = 2
    Protected = 3
    Private = 4


class MemoryLayout(Enum):
    Standard = 1
    Optimized = 2


class SecondaryType(Enum):
    ProgramCycle = 1
    ProgrammingError = 121
    RackOrStationFailure = 86
    Startup = 100
    DiagnosticErrorInterrupt = 82
    PullOrPlugOfModules = 83
    TimeDelayInterrupt = 20
    CyclicInterrupt = 30
    HardwareInterrupt = 40
    TimeErrorInterrupt = 80
    IOAccessError = 122
    TimeOfDay = 10
    SynchronousCycle = 61
    Status = 55
    Update = 56
    Profile = 57
