import uuid
import time
import hashlib
import json

def get_event_metadata():
    return {
        "run_id": str(uuid.uuid1()),
        "timestamp": round(time.time()),
        "event_id": str(uuid.uuid4())

    }

def generate_md5_hash_from_payload(payload:dict):
    return hashlib.md5(str(payload).encode()).hexdigest()

def generate_sha256_hash_from_payload(payload:dict):
    return hashlib.sha256(str(payload).encode()).hexdigest()

def enrich_valid_event(event, version, count):
    metadata = get_event_metadata()
    event['pipeline']['run_id'] = metadata['run_id']

    event['event']['id'] = metadata['event_id']

    event['data']['checksum_md5'] = generate_md5_hash_from_payload(event['data']['payload'])
    event['data']['checksum_sha256'] = generate_sha256_hash_from_payload(event['data']['payload'])

    event['reporter']['version'] = version
    event['reporter']['sequence'] = count
    event['reporter']['timestamp'] = round(time.time())

    return event

    
