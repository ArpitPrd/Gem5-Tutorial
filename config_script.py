from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.no_cache import NoCache
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.processors.simple_processor import SimpleProcessor
# from gem5.components.processors.o3_cpu import O3CPU
from gem5.components.processors.cpu_types import CPUTypes
from gem5.isas import ISA
from gem5.resources.resource import BinaryResource
from gem5.simulate.simulator import Simulator
import sys

def get_simulator(board:any) -> any:
    """
    return the simulator
    """
    return Simulator(board)

def get_binary_file(filename:str) -> any:
    """
    returns the binary file modidy any change of obtaining resources only inside this
    currently supports:
        1. BinaryResource
    outsourcing not supported
    """
    return BinaryResource(filename)

def get_cache_hierarchy(cache_type:str):
    """
    keep adding support for additional caches
    current support for:
        1. NoCache NoCache()
    """

    if cache_type=="NoCache":
        return NoCache()
    else:
        print(f"{cache_type} Not Supported")
        sys.exit()
    
def get_memory(mem_type:str, size:str):
    """
    keep adding support for additional memory types

    current support for:
        1. DDR3 SingleChannelDDR3_1600(size)
    """
    if mem_type=="DDR3":
        return SingleChannelDDR3_1600(size)
    else:
        print(f"{mem_type} not supported")
        sys.exit()
    
def prepare_board(freq:str, processor:any, memory:any, cache_hierarchy:any) -> any:
    """
    prepares a board with above listed features
    """
    return SimpleBoard(
        clk_freq=freq,
        processor=processor,
        memory=memory,
        cache_hierarchy=cache_hierarchy,
    )

def set_workload(board:any, type_of_workload:str, binary:any) -> None:
    """
    sets your binary workload
    current support for 
        1. SE board.set_se_binary_workload(binary)
    """
    if type_of_workload=="SE":
        board.set_se_binary_workload(binary)
    
    else:
        print(f"{type_of_workload} not supported")
        sys.exit()

def get_cpu_type(cpu_type:str) -> any:
    """
    keep adding more cpu types
    current support for
        1. ATMOIC cpu_types.ATOMIC
    """
    if cpu_type=="ATOMIC":
        return CPUTypes.ATOMIC
    else:
        print(f"{cpu_type} not supported")
    
def get_isa(isa_type:str) -> any:
    """
    keep adding more isa_types
    current support for 
        1. X86
    """
    if isa_type=="X86":
        return ISA.X86
    else:
        print(f"{isa_type} not supported")
        sys.exit()

def get_processor(processor_type:str, cpu_type:str, num_cores:int, isa_type:str) -> any:
    """
    return a simple processor with above mentioned features
    current support for
        1. SIMPLE
        2. O3CPU (not tested)
    """
    _cpu_type=get_cpu_type(cpu_type)
    _isa = get_isa(isa_type)
    if processor_type=="SIMPLE":
        return SimpleProcessor(
            cpu_type=_cpu_type, 
            num_cores=num_cores, 
            isa=_isa
        )
    # if processor_type=="O3CPU":
    #     return O3CPU(isa=_isa, num_cores=num_cores)
    else:
        print(f"{isa_type} not supported")

def prepare_simulator(
        processor_type:str,
        cpu_type:str, 
        num_cores:int, 
        isa_type:str, 
        mem_type:str,
        mem_size:str,
        cache_type:str,
        cpu_freq:str,
        binary_filename:str,
        type_of_workload:str
    ) -> any:
    """
    sets up the entire system for run, provides one with the following
    - motherboard
    - processor
    assumes no cache hierarchy
    """
    processor = get_processor(processor_type, cpu_type=cpu_type, num_cores=num_cores, isa_type=isa_type)

    cache_hierarchy = get_cache_hierarchy(cache_type)
    memory = get_memory(mem_type, mem_size)
    
    board = prepare_board(cpu_freq, processor, memory, cache_hierarchy)

    binary = get_binary_file(binary_filename)
    
    set_workload(board, type_of_workload, binary)

    simulator = get_simulator(board)
    
    return simulator

def _run_simulator(simulator) -> None:
    """
    general purpose doc for running a simulator
    """
    print("running the simulation")
    simulator.run()

def run_simulation(
        processor_type:str,
        cpu_type:str, 
        num_cores:int, 
        isa_type:str, 
        mem_type:str,
        mem_size:str,
        cache_type:str,
        cpu_freq:str,
        binary_filename:str,
        type_of_workload:str
    ):
    """
    simulator runner
    support for:\n
        1. processor_type: SIMPLE
        2. cpu_type: ATOMIC
        3. num_cores: >=1
        4. isa_type: X86
        5. mem_type: DDR3
        6. mem_size: 1GiB
        7. cache_type: NoCache
        8. cpu_freq: 600MHz
        9. binary_filename: str
        10. type_of_workload: SE
    """
    simulator = prepare_simulator(processor_type,
        cpu_type,
        num_cores,
        isa_type,
        mem_type,
        mem_size,
        cache_type,
        cpu_freq,
        binary_filename,
        type_of_workload
    )
    
    _run_simulator(simulator)
    

"""
Types of CPUs
- AtomicSimpleCPU
- O3CPU
- TimingSimpleCPu
- KvmCPU
- MinorCPU

Memconfigs
"""
cpu_typesList = ["ATOMIC", ]
MemoryConfigs = []
FrequencyList = [str(i)+"MHz" for i in range(600, 3300, 200)]

run_simulation(
    "SIMPLE",
    "ATOMIC",
    1,
    "X86",
    "DDR3",
    "1GiB",
    "NoCache",
    "600MHz",
    "hello-world",
    "SE"
)