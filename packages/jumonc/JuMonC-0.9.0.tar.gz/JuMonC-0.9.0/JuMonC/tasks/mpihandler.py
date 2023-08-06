import logging

from mpi4py import MPI

from typing import Any, List, Optional, Tuple


from JuMonC.tasks.taskSwitcher import task_switcher
from JuMonC.tasks import taskPool
from JuMonC.models import dataStore
from JuMonC.tasks import mpibase


logger = logging.getLogger(__name__)


__comm = MPI.COMM_WORLD



def waitForCommands() -> None:
    data: Optional[List[int]] = None
    taskPool.setupTaskPool()
    while mpibase.keepRunning():
        with mpibase.mpi_lock:
            logging.debug("rank %i waiting for mpi command", __comm.Get_rank())
            data = __comm.bcast(data, root=0)
        logging.debug("recieved mpi command with data: %s", str(data))
        task_switcher.addTask(data)


def sendResults(args, kwargs) -> None:    
    print(args)
    print(kwargs)
    dataID = kwargs["dataID"]
    print(dataID)
    with mpibase.mpi_lock:
        mpiOperation = 6


        if mpiOperation == mpibase.MPIGatherFunctionality.ONENODE.value:
            pass

        (rec_res_avai, result) = __testResultAvaiable(dataID)
        if rec_res_avai == 1:
            if mpiOperation == mpibase.MPIGatherFunctionality.MIN.value:
                __comm.reduce(result, op = MPI.MIN, root = 0)
            elif mpiOperation == mpibase.MPIGatherFunctionality.MAX.value:
                __comm.reduce(result, op = MPI.MAX, root = 0)
            elif mpiOperation == mpibase.MPIGatherFunctionality.AVERAGE.value:
                __comm.reduce(result, op = MPI.SUM, root = 0)
            elif mpiOperation == mpibase.MPIGatherFunctionality.SUM.value:
                __comm.reduce(result, op = MPI.SUM, root = 0)
            elif mpiOperation == mpibase.MPIGatherFunctionality.ALL.value:
                __comm.gather(result, root=0)
            dataStore.removeResult(dataID)

        
def __testResultAvaiable(dataID: int) -> Tuple[int, Optional[Any]]:
    result_avaiable: int = 0
    result: Optional[Any] = None
    try:
        result = dataStore.getResult(dataID)
        result_avaiable = 1
    except KeyError:
        result_avaiable = 0
        
    rec_res_avai: int = 0
    __comm.gather(result_avaiable, root=0)
    res = 0
    rec_res_avai = __comm.bcast(res, root=0)
    return (rec_res_avai, result)