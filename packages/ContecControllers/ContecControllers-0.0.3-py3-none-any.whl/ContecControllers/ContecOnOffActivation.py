
from typing import Protocol
from .ContecActivation import ContecActivation
from .ActivationType import ActivationType
from .IControllerUnit import IControllerUnit

class StateChangeCallback(Protocol):
    def __call__(
        self, isOn: bool
    ) -> None:
        """Define StateChangeCallback type."""

class ContecOnOffActivation(ContecActivation):
    _stateChangeCallbacks: list[StateChangeCallback] = []

    def __init__(self, activationNumber: int, controllerUnit: IControllerUnit) -> None:
        super().__init__(activationNumber, controllerUnit, ActivationType.OnOff)
        self.__IsOn = False

    @property
    def IsOn(self) -> bool:
        return self.__IsOn

    def SetStateChangedCallback(self, stateChangeCallback: StateChangeCallback) -> None:
        self._stateChangeCallbacks.append(stateChangeCallback)
    
    def SetNewState(self, isOn: bool):
        if self.IsOn != isOn:
            self.__IsOn = isOn
            for stateChangeCallback in self._stateChangeCallbacks:
                stateChangeCallback(isOn)
        
    async def SetActivationState(self, isOn: bool) -> None:
        mask: int = 1 << self.StartActivationNumber
        await self.ControllerUnit.ChangeActivationRegister(mask, isOn)

    def ParseStateRegisters(self, stateRegisters: list[int]) -> None:
        activationsPushersState, activationsOnOffState = stateRegisters[0].to_bytes(2, "big")
        isOn: bool = ContecActivation.IsByteOn(activationsOnOffState, self.StartActivationNumber)
        self.SetNewState(isOn)