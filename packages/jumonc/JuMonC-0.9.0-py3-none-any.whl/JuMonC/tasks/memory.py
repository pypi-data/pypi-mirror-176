import logging

from typing import Dict, List, Union, Optional
from types import ModuleType

from JuMonC.tasks import Plugin
from JuMonC.tasks.taskSwitcher import task_switcher
from JuMonC.tasks.mpi_helper import multi_node_information
from JuMonC.helpers import convertNumbers
from JuMonC import settings


logger = logging.getLogger(__name__)


class _memoryPlugin(Plugin.Plugin): 
    
    _psutil: Optional[ModuleType]
    
    def __init__(self) -> None:
        super().__init__()
        self.isWorking()
        
        self.free_mpi_id = task_switcher.addFunction(self.getFree)
        self.used_mpi_id = task_switcher.addFunction(self.getUsed)
        self.total_mpi_id = task_switcher.addFunction(self.getTotal)
    
    
    def _isWorking(self) -> bool:
        try:
            self._psutil = __import__('psutil')
        except ModuleNotFoundError:
            logging.warning("psutil can not be imported, therefore memory functionality not avaiable")
            return False
        return True
    
    @multi_node_information()
    def getFree(self) -> float:
        if isinstance(self._psutil, ModuleType):
            return self._psutil.virtual_memory().free
        logging.error("Something went wrong, in memory plugin psutil is not ModuleType")
        return -1.0
    
    @multi_node_information()
    def getUsed(self) -> float:
        if isinstance(self._psutil, ModuleType):
            return self._psutil.virtual_memory().used
        logging.error("Something went wrong, in memory plugin psutil is not ModuleType")
        return -1.0
    
    @multi_node_information()
    def getTotal(self) -> float:
        if isinstance(self._psutil, ModuleType):
            return self._psutil.virtual_memory().total
        logging.error("Something went wrong, in memory plugin psutil is not ModuleType")
        return -1.0
    
    
    def getStatusData(self,
                      dataType: str, 
                      duration: float = -1.0, 
                      overrideHumanReadableWithValue: Optional[bool] = None) -> List[Dict[str, Union[bool, int, float ,str]]]:
        logging.debug("get memory status data with type=%s, duration=%s, overrride humand readable=%s",
                     str(dataType),
                     str(duration),
                     str(overrideHumanReadableWithValue))
        if dataType == "free":
            return [self.convertNumber(self.getFree(id=self.free_mpi_id), "free", "B", overrideHumanReadableWithValue)]
        if dataType == "used":
            return [self.convertNumber(self.getUsed(id=self.used_mpi_id), "used", "B", overrideHumanReadableWithValue)]
        return []
    
    
    def getConfigData(self,
                      dataType: str, 
                      overrideHumanReadableWithValue: Optional[bool] = None) -> List[Dict[str, Union[bool, int, float ,str]]]:
        logging.debug("get memory config data with type=%s, overrride humand readable=%s",
                     str(dataType),
                     str(overrideHumanReadableWithValue))
        if dataType == "total":
            return [self.convertNumber(self.getTotal(id=self.total_mpi_id), "total", "B", overrideHumanReadableWithValue)]
        return []
    
    
    def convertNumber(self, 
                      num: Union[int,float], 
                      name: str, 
                      unit: str, 
                      overrideHumanReadableWithValue: Optional[bool]
                ) -> Dict[str, Union[bool, int, float ,str]]:
        if overrideHumanReadableWithValue or (overrideHumanReadableWithValue is None and settings.DEFAULT_TO_HUMAN_READABLE_NUMBERS) :
            (value, unitPrefix) = convertNumbers.convertBinaryPrefix(num)
            return {name + "[" + unitPrefix + unit + "]" : value}
        
        return {name + "[" + unit + "]" : str(num)}
    
    
plugin = _memoryPlugin()