from dataclasses import dataclass
# {
#     "name": "review",
#     "type": "VARCHAR",
#     "alias": "review",
#     "nullable": true,
#     "primaryKey": false,
#     "foreignKey": false,
#     "description": ""
# },


@dataclass
class TableColumnInfo:
    name: str
    type: str
    alias: str
    nullable: bool
    primaryKey: bool
    foreignKey: bool
    description: str
