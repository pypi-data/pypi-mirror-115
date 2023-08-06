import asyncio
from datetime import timedelta, datetime
from .CommunicationManager import CommunicationManager
from .ContecConectivityConfiguration import ContecConectivityConfiguration
from .ControllersStatusReader import ControllersStatusReader
from .ControllerUnit import ControllerUnit
from .ActivationType import ActivationType
from .ContecOnOffActivation import ContecOnOffActivation
from .ContecBlindActivation import ContecBlindActivation
from .ITracer import ConsoleTracer, ITracer

class ControllerManager:
    _controllerUnits: list[ControllerUnit]
    _controllersStatusReader: ControllersStatusReader
    _contecConectivityConfiguration: ContecConectivityConfiguration
    _communicationManager: CommunicationManager
    _tracer: ITracer

    def __init__(self, tracer: ITracer, contecConectivityConfiguration: ContecConectivityConfiguration) -> None:
        self._tracer = tracer
        self._contecConectivityConfiguration = contecConectivityConfiguration
        self._communicationManager = CommunicationManager(tracer, self._contecConectivityConfiguration.ControllerIp, self._contecConectivityConfiguration.ControllerPort)
        #CommunicationManager.ConnectionEstablished += ConnectionEstablished;
        #CommunicationManager.ConnectionLost += ConnectionLost;
        self._controllerUnits = []
        for i in range(self._contecConectivityConfiguration.NumberOfControllers):
            self._controllerUnits.append(ControllerUnit(tracer, self._contecConectivityConfiguration, self._communicationManager, i))
        
        self._controllersStatusReader = ControllersStatusReader(tracer, self._contecConectivityConfiguration, self._controllerUnits)
        self.__OnOffActivations = []
        self.__BlindActivations = []
    
    @property
    def OnOffActivations(self)-> list[ContecOnOffActivation]:
        return self.__OnOffActivations
    
    @property
    def BlindActivations(self)-> list[ContecBlindActivation]:
        return self.__BlindActivations

    async def CloseAsync(self) -> None:
        await self._communicationManager.CloseAsync()
        await self._controllersStatusReader.Close()
        #CommunicationManager.ConnectionEstablished -= ConnectionEstablished;
        #CommunicationManager.ConnectionLost -= ConnectionLost;
    
    def Init(self) -> None:
        self._communicationManager.StartListening()

    #async def SetEntitiesFromDatabaseAsync

    async def DiscoverEntitiesAsync(self) -> None:
        for controllerUnit in self._controllerUnits:
            newActivations = await controllerUnit.DiscoverAsync()
            self._tracer.TraceInformation(f"Discovered {len(newActivations)} activations in controller {controllerUnit.UnitId}.")
            for activation in newActivations:
                if activation.ActivationType == ActivationType.Blind:
                    self.__BlindActivations.append(activation)
                else:
                    self.__OnOffActivations.append(activation)

    async def IsConnected(self, timeToWaitForConnection: timedelta) -> bool:
        destinationTime: datetime = datetime.now() + timeToWaitForConnection
        while datetime.now() < destinationTime:
            if self._communicationManager.IsConnected:
                return True
            await asyncio.sleep(0.25)
        return False
        

async def Main() -> None:
    controllerManager = ControllerManager(ConsoleTracer(), ContecConectivityConfiguration(2, '127.0.0.1', 1234))
    controllerManager.Init()
    isConnected = await controllerManager.IsConnected(timedelta(seconds=5))
    if not isConnected:
        print("Not Connected!!!")
        await controllerManager.CloseAsync()
        print("Closed")
        return
    await controllerManager.DiscoverEntitiesAsync()
    onOffActivations: list[ContecOnOffActivation] = controllerManager.OnOffActivations
    blindActivations: list[ContecBlindActivation] = controllerManager.BlindActivations
    print(f"onOff - {len(onOffActivations)}. Blind - {len(blindActivations)}")
    import os
    clear = lambda: os.system('cls')
    for i in range(100):
        await asyncio.sleep(1)
        clear()
        for onOff in onOffActivations:
            print(f"[OnOff] - {onOff.ControllerUnit.UnitId}-{onOff.StartActivationNumber} - {onOff.IsOn}")
        for blind in blindActivations:
            print(f"[Blind] - {blind.ControllerUnit.UnitId}-{blind.StartActivationNumber} - {blind.MovingDirection} ({blind.BlindOpeningPercentage}%)")

if __name__ == "__main__":
    asyncio.run(Main())