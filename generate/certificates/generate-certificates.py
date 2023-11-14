#!/usr/bin/env python3

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat
from cryptography.x509.oid import NameOID
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.x509 import CertificateBuilder

from cryptography import x509
from cryptography.hazmat.primitives import hashes

import datetime


def generate_ca_cert_key(country, state, locality, org, days):
    # Generate a CA key
    ca_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )

    # Serialize the CA key to a PEM format
    ca_key_pem = ca_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    # Generate a CA certificate
    subject = issuer = x509.Name(
        [
            x509.NameAttribute(NameOID.COUNTRY_NAME, country),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state),
            x509.NameAttribute(NameOID.LOCALITY_NAME, locality),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, org),
        ]
    )

    ca_cert = (
        CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(ca_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=days))
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
        .sign(ca_key, hashes.SHA256(), default_backend())
    )

    # Serialize the CA certificate to a PEM format
    ca_cert_pem = ca_cert.public_bytes(Encoding.PEM)

    return ca_key_pem, ca_cert_pem


def generate_server_cert_key(
    country, state, locality, org, days, ca_key_pem, ca_cert_pem
):
    # Deserialize the CA key and certificate from bytes
    ca_key = serialization.load_pem_private_key(
        ca_key_pem, password=None, backend=default_backend()
    )
    ca_cert = x509.load_pem_x509_certificate(ca_cert_pem, backend=default_backend())

    # Generate a server key
    server_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )

    # Serialize the server key to a PEM format
    server_key_pem = server_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    # Generate a server certificate
    subject = x509.Name(
        [
            x509.NameAttribute(NameOID.COUNTRY_NAME, country),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state),
            x509.NameAttribute(NameOID.LOCALITY_NAME, locality),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, org),
            x509.NameAttribute(NameOID.COMMON_NAME, "Server"),
        ]
    )

    server_cert = (
        CertificateBuilder()
        .subject_name(subject)
        .issuer_name(ca_cert.subject)
        .public_key(server_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=days))
        .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
        .sign(ca_key, hashes.SHA256(), default_backend())
    )

    # Serialize the server certificate to a PEM format
    server_cert_pem = server_cert.public_bytes(Encoding.PEM)

    return server_key_pem, server_cert_pem


def generate_client_cert_key(
    country, state, locality, org, days, ca_key_pem, ca_cert_pem
):
    # Deserialize the CA key and certificate from bytes
    ca_key = serialization.load_pem_private_key(
        ca_key_pem, password=None, backend=default_backend()
    )
    ca_cert = x509.load_pem_x509_certificate(ca_cert_pem, backend=default_backend())

    # Generate a client key
    client_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )

    # Serialize the client key to a PEM format
    client_key_pem = client_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    # Generate a client certificate
    subject = x509.Name(
        [
            x509.NameAttribute(NameOID.COUNTRY_NAME, country),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state),
            x509.NameAttribute(NameOID.LOCALITY_NAME, locality),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, org),
            x509.NameAttribute(NameOID.COMMON_NAME, "Client"),
        ]
    )

    client_cert = (
        CertificateBuilder()
        .subject_name(subject)
        .issuer_name(ca_cert.subject)
        .public_key(client_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=days))
        .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
        .sign(ca_key, hashes.SHA256(), default_backend())
    )

    # Serialize the client certificate to a PEM format
    client_cert_pem = client_cert.public_bytes(Encoding.PEM)

    return client_key_pem, client_cert_pem


def generate_dh_params():
    # Generate Diffie-Hellman parameters
    parameters = dh.generate_parameters(
        generator=2, key_size=2048, backend=default_backend()
    )

    # Serialize the DH parameters to a PEM format
    dh_params_pem = parameters.parameter_bytes(
        Encoding.PEM, serialization.ParameterFormat.PKCS3
    )

    return dh_params_pem


if __name__ == "__main__":
    # Customize these variables according to your requirements
    country = "US"
    state = "California"
    locality = "Los Angeles"
    org = "My Organization"
    days = 365  # Adjust the number of days as needed

    # Generate CA certificate and key
    ca_key, ca_cert = generate_ca_cert_key(country, state, locality, org, days)

    # Generate server certificate and key
    server_key, server_cert = generate_server_cert_key(
        country, state, locality, org, days, ca_key, ca_cert
    )

    # Generate client certificate and key
    client_key, client_cert = generate_client_cert_key(
        country, state, locality, org, days, ca_key, ca_cert
    )

    # Generate Diffie-Hellman parameters
    dh_params = generate_dh_params()

    # Save certificates and keys to files
    with open("ca.key", "wb") as ca_key_file:
        ca_key_file.write(ca_key)

    with open("ca.crt", "wb") as ca_cert_file:
        ca_cert_file.write(ca_cert)

    with open("server.key", "wb") as server_key_file:
        server_key_file.write(server_key)

    with open("server.crt", "wb") as server_cert_file:
        server_cert_file.write(server_cert)

    with open("client.key", "wb") as client_key_file:
        client_key_file.write(client_key)

    with open("client.crt", "wb") as client_cert_file:
        client_cert_file.write(client_cert)

    with open("dh.pem", "wb") as dh_file:
        dh_file.write(dh_params)
