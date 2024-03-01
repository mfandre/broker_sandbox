import json

class JsonObject:
    def to_json_string(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    
    @classmethod
    def from_json_string(cls, json_str):
        json_dict = json.loads(json_str)
        return cls(**json_dict)