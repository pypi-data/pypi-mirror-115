import re
import urllib.request

from grpc_tools import protoc
from glob import glob
from os import mkdir, walk, rmdir
from pathlib import Path
from shutil import move


class BuildProtos:

    PROTO_ROOT = "https://raw.githubusercontent.com/lightningnetwork/lnd/master/lnrpc/"

    PROTOS = [
        f"{rpc}.proto"
        for rpc in [
            "lightning",
            "autopilotrpc/autopilot",
            "chainrpc/chainnotifier",
            "invoicesrpc/invoices",
            "lnclipb/lncli",
            "routerrpc/router",
            "signrpc/signer",
            "verrpc/verrpc",
            "walletrpc/walletkit",
            "watchtowerrpc/watchtower",
            "wtclientrpc/wtclient",
        ]
    ]

    REPO_PATH = Path(__file__).parents[1]
    ROOT_PATH = REPO_PATH / "lndpy"
    PROTOS_PATH = ROOT_PATH / "protos"
    SERVICES_PATH = ROOT_PATH / "services"

    def run(self):
        self.fetch()
        self.build()

    def fetch(self):
        try:
            mkdir(self.PROTOS_PATH)
        except FileExistsError:
            pass

        for proto in self.PROTOS:
            print(f"Fetching {proto}...")
            proto_path = proto.split("/")
            dirname = proto_path[0] if len(proto_path) > 1 else None
            if dirname:
                try:
                    mkdir(self.PROTOS_PATH / dirname)
                except FileExistsError:
                    pass
            with urllib.request.urlopen(self.PROTO_ROOT + proto) as res:
                with open(self.PROTOS_PATH / proto, "wb") as f:
                    f.write(res.read())

    def build(self):
        googleapis_path = self.REPO_PATH / "googleapis"
        if not googleapis_path.exists():
            googleapis_path = self.REPO_PATH.parent / "googleapis"
        if not googleapis_path.exists():
            raise Exception(
                "Google APIs repo must be installed either in repo, or as it's sibling. Aborting..."
            )

        for proto in glob(f"{self.PROTOS_PATH}/**/*.proto", recursive=True):
            print(f"Building {proto}...")
            protoc.main(
                [
                    "grpc_tools.protoc",
                    f"--proto_path={googleapis_path}:{self.PROTOS_PATH}",
                    f"--python_out={self.SERVICES_PATH}",
                    f"--grpc_python_out={self.SERVICES_PATH}",
                    proto,
                ]
            )

        # move all services into a flat directory structure
        for proto in glob(f"{self.SERVICES_PATH}/**/*grpc.py"):
            move(proto, self.SERVICES_PATH / proto.split("/")[-1])

        # touch __init__.py files so we can import the rpc libs
        for _root, dirs, _files in walk(self.SERVICES_PATH):
            for dirname in dirs:
                if dirname != "__pycache__":
                    (self.SERVICES_PATH / dirname / "__init__.py").touch()

        # edit the imports to use relative imports, per:
        # https://github.com/protocolbuffers/protobuf/issues/1491
        # this is gonna get ugly - two types of change are required here
        for srv in glob(f"{self.SERVICES_PATH}/*.py"):
            with open(srv, "r+") as f:
                code = f.read()
                f.seek(0)
                f.write(
                    re.sub(
                        r"from\ (.+rpc.*)",
                        "from .\\1",
                        re.sub(r"\n(import .+_pb2.*)", "from . \\1", code),
                    )
                )
                f.truncate()

        # service files in nested directories need `..` relative imports
        for srv in glob(f"{self.SERVICES_PATH}/**/*.py"):
            with open(srv, "r+") as f:
                code = f.read()
                f.seek(0)
                f.write(re.sub(r"\n(import .+_pb2.*)", "from .. \\1", code))
                f.truncate()


if __name__ == "__main__":
    BuildProtos().run()
