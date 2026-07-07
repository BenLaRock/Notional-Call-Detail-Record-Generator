from creation_utils.constants import CELL_TOWERS_MX, CELL_TOWERS_US_CA, CELL_TOWERS_US_AZ

def generate_towers():
    towers = []
    towers.extend(CELL_TOWERS_MX + CELL_TOWERS_US_CA + CELL_TOWERS_US_AZ)
    return towers