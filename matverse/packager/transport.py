#!/usr/bin/env python3
"""Transport helpers for MatVerse packager integration."""

from __future__ import annotations

import argparse
import logging
import os
import shutil
import sys
from dataclasses import dataclass
from importlib import import_module
from importlib.util import find_spec
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


@dataclass
class AndroidSdkCheck:
    android_home: Optional[str]
    android_home_exists: bool
    build_tools_exists: bool
    build_tools_versions: list[str]
    latest_build_tools: Optional[str]
    gradle_available: bool
    gradlew_exists: bool


class PackagerTransport:
    """Manage packager import paths and environment validation."""

    def __init__(self, root_path: Optional[Path] = None) -> None:
        self.root_path = root_path or Path(__file__).resolve().parents[2]
        self.packager_path = self.root_path / "matverse" / "packager"

    def setup_environment(self) -> None:
        """Ensure the repository root is on sys.path."""
        root_value = str(self.root_path)
        if root_value not in sys.path:
            sys.path.insert(0, root_value)

        logger.info("Packager environment configured", extra={"root": root_value})

    def check_android_sdk(self) -> AndroidSdkCheck:
        """Validate Android SDK presence and related tooling."""
        android_home = os.environ.get("ANDROID_HOME") or os.environ.get("ANDROID_SDK_ROOT")
        android_home_exists = bool(android_home and Path(android_home).exists())
        build_tools_versions: list[str] = []
        latest_build_tools: Optional[str] = None
        build_tools_exists = False

        if android_home_exists:
            build_tools = Path(android_home) / "build-tools"
            build_tools_exists = build_tools.exists()
            if build_tools_exists:
                build_tools_versions = sorted(
                    [p.name for p in build_tools.iterdir() if p.is_dir()]
                )
                latest_build_tools = build_tools_versions[-1] if build_tools_versions else None

        gradle_available = shutil.which("gradle") is not None
        gradlew_exists = (Path.cwd() / "gradlew").exists()

        return AndroidSdkCheck(
            android_home=android_home,
            android_home_exists=android_home_exists,
            build_tools_exists=build_tools_exists,
            build_tools_versions=build_tools_versions,
            latest_build_tools=latest_build_tools,
            gradle_available=gradle_available,
            gradlew_exists=gradlew_exists,
        )

    def import_packager(self) -> Any:
        """Import the Android packager module after verifying availability."""
        if find_spec("matverse.packager.android") is None:
            raise ModuleNotFoundError(
                "matverse.packager.android not found. Ensure the Android packager module "
                "is available in this repository."
            )

        module = import_module("matverse.packager.android")
        required = [
            "AndroidPackager",
            "AndroidPackagerConfig",
        ]
        for name in required:
            if not hasattr(module, name):
                raise AttributeError(
                    f"Android packager module is missing required attribute: {name}"
                )
        return module

    def create_config(self, **overrides: Any) -> Dict[str, Any]:
        """Create a configuration dictionary for AndroidPackagerConfig."""
        defaults: Dict[str, Any] = {
            "node_id": "matverse-android-packager",
            "project_root": Path.cwd(),
            "module_name": "app",
            "build_type": "release",
            "output_dir": Path.cwd() / "dist",
            "android_home": os.environ.get("ANDROID_HOME")
            or os.environ.get("ANDROID_SDK_ROOT"),
            "keystore_path": os.environ.get("MV_KEYSTORE"),
            "keystore_password": os.environ.get("MV_KEYSTORE_PASS"),
            "key_alias": os.environ.get("MV_KEY_ALIAS"),
            "key_password": os.environ.get("MV_KEY_PASS"),
        }
        defaults.update(overrides)
        return defaults

    def run_packager(self, **overrides: Any) -> Dict[str, Any]:
        """Run the Android packager and return its receipt."""
        self.setup_environment()
        sdk_check = self.check_android_sdk()
        logger.info("Android SDK check", extra={"sdk": sdk_check})

        module = self.import_packager()
        config_data = self.create_config(**overrides)
        config = module.AndroidPackagerConfig(**config_data)
        packager = module.AndroidPackager(config)

        receipt = packager.package()
        return {
            "success": True,
            "receipt": receipt,
        }


def create_transport(root_path: Optional[Path] = None) -> PackagerTransport:
    """Create a PackagerTransport instance."""
    return PackagerTransport(root_path=root_path)


def main() -> None:
    """CLI entrypoint for the transport helper."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    parser = argparse.ArgumentParser(
        description="MatVerse Android packager transport",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--project", default=".")
    parser.add_argument("--module", default="app")
    parser.add_argument("--type", default="release", choices=["debug", "release"])
    parser.add_argument("--out", default="dist")
    parser.add_argument("--keystore", default=None)
    parser.add_argument("--alias", default=None)
    parser.add_argument("--ks-pass", default=None)
    parser.add_argument("--key-pass", default=None)
    parser.add_argument("--check-sdk", action="store_true")

    args = parser.parse_args()

    transport = PackagerTransport()

    if args.check_sdk:
        transport.setup_environment()
        sdk = transport.check_android_sdk()
        print("\n=== Android SDK Check ===")
        print(f"android_home: {sdk.android_home}")
        print(f"android_home_exists: {sdk.android_home_exists}")
        print(f"build_tools_exists: {sdk.build_tools_exists}")
        print(f"build_tools_versions: {sdk.build_tools_versions}")
        print(f"latest_build_tools: {sdk.latest_build_tools}")
        print(f"gradle_available: {sdk.gradle_available}")
        print(f"gradlew_exists: {sdk.gradlew_exists}")
        return

    result = transport.run_packager(
        project_root=Path(args.project),
        module_name=args.module,
        build_type=args.type,
        output_dir=Path(args.out),
        keystore_path=Path(args.keystore) if args.keystore else None,
        key_alias=args.alias,
        keystore_password=args.ks_pass,
        key_password=args.key_pass,
    )

    if not result.get("success"):
        sys.exit(1)


if __name__ == "__main__":
    main()
