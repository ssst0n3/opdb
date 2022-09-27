import opcode
import logging

logger = logging.getLogger('st0n3_pdb')
FORMAT = "[%(levelname)s] [%(funcName)s] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.INFO)


def debug_dis(op, oparg):
    logger.debug("{} {}".format(opcode.opname[op], oparg))
