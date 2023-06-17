import os
import json

import jwt
from OpenSSL.crypto import (
  X509Store,
  X509StoreContext,
  X509StoreContextError,
  load_certificate,
  FILETYPE_ASN1,
  FILETYPE_PEM
)


def add_labels(key: str) -> bytes:
  return ("-----BEGIN CERTIFICATE-----\n" + key + "\n-----END CERTIFICATE-----").encode()


def _get_root_cert(root_cert_path):

  fn = os.environ.get("APPLE_ROOT_CA")
  if fn is None:
    fn = root_cert_path or "AppleRootCA-G3.cer"

  fn = os.path.expanduser(fn)
  with open(fn, "rb") as f:
    data = f.read()
    root_cert = load_certificate(FILETYPE_ASN1, data)

  return root_cert

class InvalidTokenError(Exception):
  pass


def _decode_jws(token, root_cert_path):
  try:
    header = jwt.get_unverified_header(token)

    # the first cert contains the public key used to sign the jwt
    first_cert_data = header["x5c"][0]
    first_cert_data = add_labels(first_cert_data)
    first_cert = load_certificate(FILETYPE_PEM, first_cert_data)

    # the other certs are an x5c (X.509 certificate chain)
    chain_datas = header["x5c"][1:]
    chain_datas = [add_labels(cd) for cd in chain_datas]
    chain = [load_certificate(FILETYPE_PEM, cd) for cd in chain_datas]

    public_key = first_cert.get_pubkey().to_cryptography_key()

    store = X509Store()
    store.add_cert(_get_root_cert(root_cert_path))
    ctx = X509StoreContext(store=store, certificate=first_cert, chain=chain)
    ctx.verify_certificate()

    alg = header["alg"]
    return jwt.decode(token, public_key, algorithms=[alg])
  except (ValueError, KeyError, jwt.exceptions.PyJWTError, X509StoreContextError) as err:
    raise InvalidTokenError from err


def parse(req_body, apple_root_cert_path=None):
  token = json.loads(req_body)["signedPayload"]

  # decode main token
  payload = _decode_jws(token, root_cert_path=apple_root_cert_path)

  if payload['notificationType'] == 'TEST':
    return payload

  # decode signedTransactionInfo & substitute decoded into payload
  signedTransactionInfo = _decode_jws(payload["data"]["signedTransactionInfo"], root_cert_path=apple_root_cert_path)
  payload["data"]["signedTransactionInfo"] = signedTransactionInfo

  # decode signedRenewalInfo & substitute decoded into payload
  if "signedRenewalInfo" in payload["data"]:
    signedRenewalInfo = _decode_jws(payload["data"]["signedRenewalInfo"], root_cert_path=apple_root_cert_path)
    payload["data"]["signedRenewalInfo"] = signedRenewalInfo

  return payload
