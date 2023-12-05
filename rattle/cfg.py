from .recover import InternalRecover
from .evmasm import EVMAsm
from typing import Dict, List, Tuple
from collections import defaultdict


def build_cfg(bytecode: bytes) -> Tuple[Dict[int, EVMAsm.EVMInstruction], List[Tuple[int, int]]]:
    if bytecode.startswith(b"0x"):
        bytecode = bytecode[2:]
    internal = InternalRecover(bytecode, edges=[])
    nodes = {}
    edges = []
    blocks = {}
    visited = defaultdict(bool)
    for f in internal.functions:
        for block in f:
            blocks[block.offset] = block

    def trace(block):
        visited[block] = True
        nodes[block.offset] = block
        insns = block.insns
        for i in range(len(insns)):
            nodes[insns[i].offset] = insns[i].insn
            if i == len(insns) - 1:
                continue
            edges.append((insns[i].offset, insns[i + 1].offset))
        if block.fallthrough_edge is not None:
            edges.append((block.insns[-1].offset, block.fallthrough_edge.offset))
            if not visited[block.fallthrough_edge]:
                trace(block.fallthrough_edge)
        for jump in block.jump_edges:
            edges.append((block.insns[-1].offset, jump.offset))
            if not visited[jump]:
                trace(jump)

    trace(internal.functions[0].blocks[0])

    return nodes, edges