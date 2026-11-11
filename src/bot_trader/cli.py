"""Explicit local setup and finite synthetic worker commands."""

import argparse
import json
import time
from pathlib import Path
from typing import cast
from uuid import uuid4

import uvicorn

from bot_trader.api.credentials import ROLES, Role, issue_credential
from bot_trader.application import build_services
from bot_trader.core.contracts import DatasetSpec, Principal
from bot_trader.core.errors import PlatformError
from bot_trader.core.settings import Settings
from bot_trader.market_data.archive import SourceSpec
from bot_trader.persistence import Database, migrate
from bot_trader.simulation.bridge import NativeSliceProcess
from bot_trader.simulation.slice import SliceConfiguration


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Synthetic technical platform; no market execution."
    )
    parser.add_argument("--state-dir", type=Path, help="Local state directory (default .state).")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser(
        "init", help="Migrate, create private local credential and import hypotheses."
    )
    commands.add_parser("migrate", help="Explicitly upgrade metadata schema.")
    commands.add_parser("serve", help="Start built web/API on loopback port 8000.")
    fixture = commands.add_parser("fixture", help="Create only a seeded synthetic dataset.")
    fixture.add_argument("--seed", type=int, default=42)
    fixture.add_argument("--rows", type=int, default=120)
    worker = commands.add_parser("worker", help="Execute one queued technical job, or watch.")
    worker.add_argument("--watch", action="store_true")
    worker.add_argument("--worker-id", default=f"worker-{uuid4().hex}")
    recover = commands.add_parser(
        "recover", help="Mark a confirmed stopped worker's jobs interrupted."
    )
    recover.add_argument("worker_id")
    credential = commands.add_parser("credential", help="Create a private role credential once.")
    credential.add_argument("role", choices=ROLES)
    slice_command = commands.add_parser("slice", help="Run one synthetic integration fixture.")
    slice_command.add_argument("--source", type=Path, required=True)
    slice_command.add_argument("--manifest", type=Path, required=True)
    slice_command.add_argument("--config", type=Path)
    slice_command.add_argument("--native-python", type=Path, required=True)
    slice_command.add_argument("--run-dir", type=Path, required=True)
    args = parser.parse_args()
    settings = Settings() if args.state_dir is None else Settings(data_dir=args.state_dir)
    administrator = Principal(id="local-admin", role="admin")
    try:
        if args.command in {"init", "migrate"}:
            database = Database(settings)
            try:
                migrate(database)
            finally:
                database.close()
            if args.command == "migrate":
                print("Metadata schema migrated and verified.")
                return
            path = issue_credential(settings, "admin")
            services = build_services(settings)
            try:
                records = services.hypotheses.import_file(
                    settings.repository_root / "HYPOTHESES.md", administrator
                )
                print(f"Initialized {len(records)} hypotheses. Local credential file: {path}")
                print("Read this private file locally for sign-in; do not publish its contents.")
            finally:
                services.database.close()
            return
        if args.command == "credential":
            path = issue_credential(settings, cast(Role, args.role))
            print(f"Private local credential file: {path}")
            return
        if args.command == "serve":
            from bot_trader.api.app import create_app

            uvicorn.run(
                create_app(settings),
                host="127.0.0.1",
                port=8000,
                access_log=False,
                proxy_headers=False,
            )
            return
        services = build_services(settings)
        try:
            if args.command == "slice":
                source = SourceSpec.model_validate_json(args.manifest.read_bytes())
                config = (
                    SliceConfiguration()
                    if args.config is None
                    else SliceConfiguration.model_validate_json(args.config.read_bytes())
                )
                progress = services.slice.import_file(args.source, source, administrator)
                if progress.archive_hash is None:
                    parser.exit(
                        1, "Import incomplete; preserve the checkpoint and resume explicitly."
                    )
                report = services.slice.run(
                    progress.archive_hash,
                    config,
                    administrator,
                    execution=NativeSliceProcess(args.native_python),
                    directory=args.run_dir,
                )
                record = services.repository.put(
                    "technical-slice", str(report["canonical_hash"]), report
                )
                services.repository.append_audit(
                    administrator.id,
                    "technical-slice.run",
                    record.id,
                    str(report["status"]),
                    {"result_hash": record.content_hash},
                )
                print(json.dumps(report, sort_keys=True))
                if report["status"] != "reconciled":
                    parser.exit(
                        1, "Technical execution remains unresolved; inspect preserved evidence."
                    )
            elif args.command == "fixture":
                record = services.datasets.create(
                    DatasetSpec(seed=args.seed, rows=args.rows), administrator
                )
                print(
                    json.dumps(
                        {"dataset_id": record.id, "version": record.version, "synthetic": True}
                    )
                )
            elif args.command == "recover":
                services.policy.require(administrator, "runs.recover")
                recovered = services.repository.recover_interrupted(
                    args.worker_id, actor_id=administrator.id
                )
                print(json.dumps({"interrupted": recovered, "replayed": False}))
            elif args.command == "worker":
                print(f"Technical worker identity: {args.worker_id}", flush=True)
                while True:
                    result = services.lab.run_once(args.worker_id)
                    if result is not None:
                        print(json.dumps({"run_id": result.id, "state": result.state}), flush=True)
                    if not args.watch:
                        break
                    if result is None:
                        time.sleep(2)
        finally:
            services.database.close()
    except PlatformError as error:
        parser.exit(1, f"{error.code}: {error.message}\n")
    except (ValueError, OSError) as error:
        parser.exit(1, f"Technical input/execution rejected: {error}\n")
    except KeyboardInterrupt:
        parser.exit(130, "Stopped. Recover interrupted work explicitly if necessary.\n")


if __name__ == "__main__":
    main()
