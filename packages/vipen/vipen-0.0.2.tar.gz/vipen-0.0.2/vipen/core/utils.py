import dataclasses
import random
import string
from dataclasses import field

import paramiko
from cryptography.hazmat.primitives import serialization


def ssh_key_fingerprint(key_path):
    k = paramiko.RSAKey.from_private_key_file(key_path)
    return ":".join(["%02x" % a for a in k.get_fingerprint()])


def ssh_key_public_key(key_path):
    k = paramiko.RSAKey.from_private_key_file(key_path)
    return (
        k.key.public_key()
        .public_bytes(
            serialization.Encoding.OpenSSH, serialization.PublicFormat.OpenSSH
        )
        .decode("utf-8")
    )


def random_string_lower(c=12) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=c))


def random_string(c=12) -> str:
    return "".join(
        random.choices(
            string.ascii_lowercase + string.ascii_uppercase + string.digits, k=c
        )
    )


def dataclass(*args, **kwargs):
    """
    A wrapper around @dataclass. It removes all class fields starting with
    an underscore (_) from the fields list.
    """
    from dataclasses import dataclass as original_dataclass

    d = original_dataclass(*args, **kwargs)
    for k in [x for x in d.__dataclass_fields__ if x.startswith("_")]:
        d.__dataclass_fields__.pop(k)
    return d


def PromptField(type="input", required=True, **kwargs):
    return dataclasses.field(
        metadata={"prompt": {"type": type, "required": required, **kwargs}}
    )


def prompt_factory(cls):
    prompts = []
    for f in dataclasses.fields(cls):
        p = f.metadata.get("prompt")
        if not p:
            continue
        if not p.get("message"):
            p["message"] = f"Enter {f.name}"
        if not p.get("name"):
            p["name"] = f.name

        if "required" in p and p.pop("required"):
            v = p.get("validate")
            if v:
                p["validate"] = lambda r: r and v(r)
            else:
                p["validate"] = lambda r: r

        if "default_factory" in p:
            p["default"] = p.pop("default_factory")()

        prompts.append(p)
    return prompts
