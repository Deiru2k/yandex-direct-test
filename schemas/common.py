string = {"type": ["string", "null"]}
integer = {"type": ["integer", "null"]}
float = {"type": ["number", "null"]}
_id = {"type": "object", "properties": {"$oid": string}}
datetime = {"type": "object", "properties": {"date": float}}