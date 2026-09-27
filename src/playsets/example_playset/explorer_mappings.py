
from enum import Enum, auto
import playsets.example_playset.explorer as explorers


class ExplorerMappingsEnum(Enum):

    BASIC_EXPLORER = auto()

explorer_mappings = {
                        ExplorerMappings.BASIC_EXPLORER: explorers.BasicExplorer
                    }
