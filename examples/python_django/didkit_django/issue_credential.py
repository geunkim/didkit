from python_django.settings import KEY_PATH
from django.core.files import File
from datetime import datetime, timedelta
import didkit
import json
import uuid


def issueCredential(request):
    with open(KEY_PATH, "r") as f:
        key_file = File(f)
        key = key_file.readline()
    key_file.close()

    did_key = request.POST.get('subject_id', didkit.keyToDID("key", key))
    verification_method = didkit.keyToVerificationMethod("key", key)
    issuance_date = datetime.utcnow().replace(microsecond=0)
    expiration_date = issuance_date + timedelta(weeks=24)

    credential = {
        "id": "urn:uuid:" + uuid.uuid4().__str__(),
        "@context": [
            "https://www.w3.org/2018/credentials/v1",
            "https://www.w3.org/2018/credentials/examples/v1",
        ],
        "type": ["VerifiableCredential"],
        "issuer": did_key,
        "issuanceDate": issuance_date.isoformat() + "Z",
        "expirationDate": expiration_date.isoformat() + "Z",
        "credentialSubject": {
            "@context": [
                {
                    "username": "https://schema.org/Text"
                }
            ],
            "id": "urn:uuid:" + uuid.uuid4().__str__(),
            "username": "Someone",
        },
    }

    didkit_options = {
        "proofPurpose": "assertionMethod",
        "verificationMethod": verification_method,
    }

    credential = didkit.issueCredential(
        credential.__str__().replace("'", '"'),
        didkit_options.__str__().replace("'", '"'),
        key)
    return json.loads(credential)
