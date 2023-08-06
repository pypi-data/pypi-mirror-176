import logging

from typing import List, Any, Callable

#from mpi4py import MPI

from functools import wraps


from JuMonC.tasks import mpibase, mpiroot
from JuMonC.tasks.taskSwitcher import task_switcher
from JuMonC.models import dataStore

logger = logging.getLogger(__name__)

def build_mpi_command(mpi_id: int, resultids:List[int], block_communication:bool = True, *args: Any, **kwargs: Any) -> List[int]:
    logging.debug("mpi command with: %i, %s", mpi_id, str(block_communication))
    logging.debug("args    %s", str(args))
    logging.debug("kwargs: %s", str(kwargs))
    data:List[Any] = [mpi_id]
    if block_communication:
        data.append(-1)
    else:
        data.append(1)
    data.append(args)
    data.append(kwargs)
    data.append(resultids)
    return data


def multi_node_information(results:int = 1) -> Callable[..., float]:
    def wrap(func: Callable[..., float]) -> Callable[..., float]:
        @wraps(func)
        def decorated_function(*args: Any, **kwargs: Any) -> float:
            logging.debug("args    %s", str(args))
            logging.debug("kwargs: %s", str(kwargs))
            if mpibase.size == 1:
                kwargs.pop("id", None)
                return func(*args, **kwargs)
            if "already_task" in kwargs.keys():
                kwargs.pop("already_task", None)
                kwargs.pop("id", None)
                logging.debug("multi_node_information is already a task")
                return func(*args, **kwargs)
            if mpibase.rank == 0:
                kwargs["already_task"] = True
                resultid = dataStore.getNextDataID()
                mpiroot.sendCommand(build_mpi_command(kwargs["id"], [resultid], *args, **kwargs))
                
                mpiroot.sendCommand(build_mpi_command(mpibase.gatherid, [-1], True, [], {"dataID": resultid}))
                
                return dataStore.getResult(resultid)
            logging.error("multi_node_information: should not reach here")
            
        return decorated_function
    return wrap
