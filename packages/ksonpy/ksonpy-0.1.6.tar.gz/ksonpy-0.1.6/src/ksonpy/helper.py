DB_IMPORT_TYPE_RULES = {
    str: {
        'rule': 'VARCHAR',
        'accept': ['INTEGER', 'DOUBLE'],
        'upgrade': []
    },
    int: {
        'rule': 'INTEGER',
        'accept': ['DOUBLE'],
        'upgrade': []
    },
    float: {
        'rule': 'DOUBLE',
        'accept': [],
        'upgrade': ['INTEGER']
    }
}
