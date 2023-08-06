import hashlib
import datetime
import json
import uuid

def get_hash_uuid(payload: dict) -> uuid:
    try:
        payload["date"] = str(datetime.date.today())
        hash_object = hashlib.sha256(json.dumps(payload, sort_keys=True).encode())
        hex_dig = hash_object.hexdigest()
        return uuid.uuid5(uuid.NAMESPACE_DNS, hex_dig)
    except Exception as e:
        return e


if __name__ == "__main__":
    get_hash_uuid({"test": "test"})