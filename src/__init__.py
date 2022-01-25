import json
import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.x509 import load_pem_x509_certificate

class InvalidTokenError(Exception):
  pass

def _decode_jws(token):
  try:
    header = jwt.get_unverified_header(token)
    first_cert_data = header['x5c'][0]
    alg = header['alg']

    cert = "-----BEGIN CERTIFICATE-----\n" + (first_cert_data) + "\n-----END CERTIFICATE-----"
    cert_obj = load_pem_x509_certificate(cert.encode(), default_backend()) 
    return jwt.decode(token, cert_obj.public_key(), algorithms=[alg])
  except (ValueError, KeyError, jwt.exceptions.PyJWTError):
    raise InvalidTokenError

def parse(req_body):
  token = json.loads(req_body)['signedPayload']

  # decode main token
  payload = _decode_jws(token)

  # decode signedTransactionInfo & substitute decoded into payload
  signedTransactionInfo = _decode_jws(payload['data']['signedTransactionInfo'])
  payload['data']['signedTransactionInfo'] = signedTransactionInfo

  # decode signedRenewalInfo & substitute decoded into payload
  if 'signedRenewalInfo' in payload['data']:
    signedRenewalInfo = _decode_jws(payload['data']['signedRenewalInfo'])
    payload['data']['signedRenewalInfo'] = signedRenewalInfo

  return payload

