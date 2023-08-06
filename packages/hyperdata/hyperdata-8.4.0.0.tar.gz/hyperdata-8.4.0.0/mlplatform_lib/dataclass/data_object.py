from dataclasses import dataclass
from typing import List, Dict

# example
# "name": "TEST",
# "sourceTableName": "TEST",
# "subtype": "Table",
# "outCols": [
#     {
#         "name": "C1"
#     },
#     {
#         "name": "C2"
#     }
# ],
# "shareRelation": [
# ]


@dataclass
class DataObject:
    id: str
    name: str
    outCols: List[Dict[str, str]]
    shareRelation: List[str]
    sourceTableName: str
    subtype: str
    author: str
    description: str
    createdOn: str
    lastEdited: str
