
from enum import Enum, auto
import playsets.example_playset.explorer as explorer


class ExplorerMappingsEnum(Enum):

    BASIC_EXPLORER = auto()

explorer_mappings = {
                        ExplorerMappingsEnum.BASIC_EXPLORER: explorer.Basic_Explorer()
                    }
