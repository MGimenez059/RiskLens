"""Confined immutable artifacts and transactional SQLite metadata."""

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from tempfile import NamedTemporaryFile
from threading import RLock
from uuid import uuid4

from pydantic import BaseModel, ValidationError

from risklens.application.contracts import (
    AnalysisRequest,
    Event,
    OperationError,
    ParserLimits,
    Result,
    RunManifest,
    canonical,
    sha256,
)
from risklens.application.ports import (
    ARTIFACT_STAGES,
    Artifact,
    Bundle,
    CommittedPublication,
    ImportBinding,
    InputIssue,
    RunOutputIdentity,
    Scan,
    SnapshotBinding,
    SnapshotIdentity,
    StoredRun,
)
from risklens.infrastructure.parser import BundleScanner, frame, unframe

_WRITER = RLock()
_SCHEMA = """
CREATE TABLE IF NOT EXISTS bundles (
    ref TEXT PRIMARY KEY, manifest_length INTEGER, csv_length INTEGER, issue TEXT
);
CREATE TABLE IF NOT EXISTS runs (
    run_id TEXT PRIMARY KEY, analysis_key TEXT UNIQUE, fingerprint TEXT,
    revision INTEGER NOT NULL, request TEXT NOT NULL, result TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS snapshots (
    snapshot_id TEXT PRIMARY KEY, portfolio_id TEXT NOT NULL,
    bundle_hash TEXT NOT NULL REFERENCES bundles(ref), artifact_hash TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS imports (
    key TEXT PRIMARY KEY, parser_hash TEXT NOT NULL,
    bundle_hash TEXT NOT NULL REFERENCES bundles(ref),
    import_id TEXT NOT NULL UNIQUE, report_hash TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS artifacts (
    run_id TEXT NOT NULL REFERENCES runs(run_id), artifact_id TEXT NOT NULL,
    kind TEXT NOT NULL, sha256 TEXT NOT NULL, PRIMARY KEY(run_id, artifact_id)
);
CREATE TABLE IF NOT EXISTS artifact_publications (
    run_id TEXT NOT NULL, artifact_id TEXT NOT NULL, metadata TEXT NOT NULL,
    PRIMARY KEY(run_id, artifact_id),
    FOREIGN KEY(run_id, artifact_id) REFERENCES artifacts(run_id, artifact_id)
);
CREATE TABLE IF NOT EXISTS events (
    run_id TEXT NOT NULL REFERENCES runs(run_id), event_id TEXT PRIMARY KEY, body TEXT NOT NULL
);
"""


class _RunHeader(BaseModel):
    run: RunManifest


class LocalState:
    def __init__(self, workspace: Path) -> None:
        self.root = workspace.resolve() / ".risklens" / "state"
        with self.writer(), self._db() as db:
            db.executescript(_SCHEMA)

    @contextmanager
    def writer(self) -> Iterator[None]:
        with _WRITER:
            yield

    def _path(self, relative: str) -> Path:
        path = self.root / relative
        if self.root.resolve() != self.root or not path.resolve().is_relative_to(self.root):
            raise OperationError("persistence_failed")
        return path

    @contextmanager
    def _db(self) -> Iterator[sqlite3.Connection]:
        try:
            path = self._path("risklens.sqlite3")
            path.parent.mkdir(parents=True, exist_ok=True)
            db = sqlite3.connect(path)
            try:
                db.row_factory = sqlite3.Row
                db.execute("PRAGMA foreign_keys=ON")
                with db:
                    yield db
            finally:
                db.close()
        except (OSError, sqlite3.Error) as error:
            raise OperationError("persistence_failed") from error
        except ValidationError as error:
            raise OperationError("integrity_error") from error

    def code_revision(self) -> str:
        root = Path(__file__).resolve().parents[1]
        return sha256(
            canonical(
                {
                    path.relative_to(root).as_posix(): sha256(path.read_bytes())
                    for path in root.rglob("*.py")
                }
            )
        )

    def _artifact(self, digest: str) -> Path:
        if len(digest) != 64 or any(char not in "0123456789abcdef" for char in digest):
            raise OperationError("integrity_error")
        return self._path(f"artifacts/sha256/{digest}")

    def read(self, digest: str) -> bytes:
        try:
            data = self._artifact(digest).read_bytes()
        except OSError as error:
            raise OperationError("integrity_error") from error
        if sha256(data) != digest:
            raise OperationError("integrity_error")
        return data

    def publish(self, data: bytes) -> str:
        digest = sha256(data)
        path = self._artifact(digest)
        if path.exists():
            self.read(digest)
            return digest
        staging = self._path("tmp")
        temporary = None
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            staging.mkdir(parents=True, exist_ok=True)
            with NamedTemporaryFile(dir=staging, delete=False) as file:
                temporary = Path(file.name)
                file.write(data)
            if sha256(temporary.read_bytes()) != digest:
                raise OperationError("integrity_error")
            temporary.replace(path)
        except OSError as error:
            raise OperationError("persistence_failed") from error
        finally:
            if temporary is not None:
                try:
                    temporary.unlink(missing_ok=True)
                except OSError:
                    # Uncommitted staging files are ignored by recovery.
                    pass
        return digest

    def register(self, manifest: bytes | None, csv: bytes | None, limits: ParserLimits) -> str:
        issue: InputIssue | None = None
        manifest_length = len(manifest or b"")
        csv_length = len(csv or b"")
        if (
            manifest_length > limits.max_manifest_bytes
            or manifest_length + csv_length > limits.max_input_bytes
        ):
            issue = "resource_limit"
        elif manifest is None or csv is None:
            issue = "unreadable_input"
        with self.writer():
            if issue is None:
                assert manifest is not None and csv is not None
                ref = self.publish(frame(manifest, csv))
            else:
                ref = uuid4().hex
            with self._db() as db:
                db.execute(
                    "INSERT OR IGNORE INTO bundles VALUES (?, ?, ?, ?)",
                    (ref, manifest_length, csv_length, issue),
                )
        return ref

    def bundle(self, ref: str, limits: ParserLimits) -> Bundle:
        with self._db() as db:
            row = db.execute("SELECT * FROM bundles WHERE ref = ?", (ref,)).fetchone()
        if row is None:
            raise OperationError("configuration_invalid")
        if (
            row["manifest_length"] > limits.max_manifest_bytes
            or row["manifest_length"] + row["csv_length"] > limits.max_input_bytes
        ):
            return Bundle(ref, None, None, "resource_limit")
        if row["issue"] is not None:
            return Bundle(ref, None, None, row["issue"])
        try:
            manifest, csv = unframe(self.read(ref))
        except ValueError as error:
            raise OperationError("integrity_error") from error
        if len(manifest) != row["manifest_length"] or len(csv) != row["csv_length"]:
            raise OperationError("integrity_error")
        return Bundle(ref, manifest, csv, None)

    def scan(self, bundle: Bundle, limits: ParserLimits) -> Scan:
        assert bundle.manifest is not None and bundle.csv is not None
        return BundleScanner(limits).scan(bundle.manifest, bundle.csv)

    def snapshot(self, snapshot_id: str) -> SnapshotBinding | None:
        with self._db() as db:
            row = db.execute(
                "SELECT * FROM snapshots WHERE snapshot_id = ?",
                (snapshot_id,),
            ).fetchone()
        return SnapshotBinding(*row) if row is not None else None

    def import_binding(self, key: str) -> ImportBinding | None:
        with self._db() as db:
            row = db.execute("SELECT * FROM imports WHERE key = ?", (key,)).fetchone()
        return ImportBinding(*row) if row is not None else None

    def _load_run(self, db: sqlite3.Connection, sql: str, key: str) -> StoredRun | None:
        row = db.execute(sql, (key,)).fetchone()
        if row is None:
            return None
        request = AnalysisRequest.model_validate_json(row["request"])
        result = Result.model_validate_json(row["result"])
        run = result.run
        fingerprint = row["fingerprint"]
        if (
            (run.run_id, run.revision) != (row["run_id"], row["revision"])
            or result.metrics is not None
            or (run.parent_run_id, run.requested_stages, result.configuration)
            != (
                request.parent_run_id,
                request.requested_stages,
                request.configuration,
            )
            or (run.input_hash is not None and run.input_hash != request.bundle_ref)
            or (
                result.validation is not None
                and result.validation.import_idempotency_key != request.import_idempotency_key
            )
            or (fingerprint is None) != (row["analysis_key"] is None)
            or (
                fingerprint is not None
                and (
                    run.input_hash is None
                    or fingerprint != request.fingerprint(run.input_hash)
                    or row["analysis_key"] != request.analysis_idempotency_key
                )
            )
        ):
            raise OperationError("integrity_error")
        return StoredRun(request, result, fingerprint)

    def analysis_binding(self, key: str) -> StoredRun | None:
        with self._db() as db:
            return self._load_run(db, "SELECT * FROM runs WHERE analysis_key = ?", key)

    def stored_run(self, run_id: str) -> StoredRun:
        with self._db() as db:
            record = self._load_run(db, "SELECT * FROM runs WHERE run_id = ?", run_id)
            if record is None:
                raise OperationError("configuration_invalid")
            return record

    def list_runs(self) -> list[RunManifest]:
        with self._db() as db:
            runs = []
            for row in db.execute("SELECT run_id, revision, result FROM runs ORDER BY rowid DESC"):
                run = _RunHeader.model_validate_json(row["result"]).run
                if (run.run_id, run.revision) != (row["run_id"], row["revision"]):
                    raise OperationError("integrity_error")
                runs.append(run)
            return runs

    def events(self, run_id: str) -> list[Event]:
        with self._db() as db:
            rows = db.execute("SELECT body FROM events WHERE run_id = ? ORDER BY rowid", (run_id,))
            return [Event.model_validate_json(row[0]) for row in rows]

    def artifact_refs(self, run_id: str) -> dict[str, Artifact]:
        with self._db() as db:
            rows = db.execute(
                """SELECT a.artifact_id, a.kind, a.sha256, p.metadata FROM artifacts a
                   LEFT JOIN artifact_publications p USING (run_id, artifact_id)
                   WHERE a.run_id = ?""",
                (run_id,),
            )
            refs = {}
            for key, kind, digest, metadata in rows:
                publication = (
                    CommittedPublication.model_validate_json(metadata) if metadata else None
                )
                if publication is not None:
                    try:
                        length = self._artifact(digest).stat().st_size
                    except OSError as error:
                        raise OperationError("integrity_error") from error
                    if (
                        publication.run_id,
                        publication.artifact_kind,
                        publication.artifact_hash,
                        publication.byte_length,
                    ) != (run_id, kind, digest, length):
                        raise OperationError("integrity_error")
                refs[key] = Artifact(kind, digest, publication)
            return refs

    @staticmethod
    def _event(db: sqlite3.Connection, event: Event) -> None:
        db.execute(
            "INSERT INTO events VALUES (?, ?, ?)",
            (event.run_id, event.event_id, event.model_dump_json()),
        )

    def append_event(self, event: Event) -> None:
        with self._db() as db:
            self._event(db, event)

    def start(
        self,
        request: AnalysisRequest,
        result: Result,
        fingerprint: str | None,
        event: Event | None,
        previous_revision: int | None,
    ) -> None:
        run = result.run
        with self._db() as db:
            if previous_revision is None:
                db.execute(
                    "INSERT INTO runs VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        run.run_id,
                        request.analysis_idempotency_key if fingerprint else None,
                        fingerprint,
                        run.revision,
                        request.model_dump_json(),
                        result.model_dump_json(),
                    ),
                )
            else:
                updated = db.execute(
                    "UPDATE runs SET revision=?, result=? WHERE run_id=? AND revision=?",
                    (run.revision, result.model_dump_json(), run.run_id, previous_revision),
                )
                if updated.rowcount != 1:
                    raise OperationError("idempotency_conflict")
            if event is not None:
                self._event(db, event)

    def finish(
        self,
        result: Result,
        previous_revision: int,
        artifacts: dict[str, Artifact],
        snapshot: SnapshotBinding | None,
        binding: ImportBinding | None,
        events: list[Event],
    ) -> None:
        run = result.run
        metadata = result.model_copy(update={"metrics": None}).model_dump_json()
        with self._db() as db:
            Result.model_validate_json(metadata)
            if snapshot is not None:
                values = (
                    snapshot.snapshot_id,
                    snapshot.portfolio_id,
                    snapshot.bundle_hash,
                    snapshot.artifact_hash,
                )
                db.execute(
                    "INSERT INTO snapshots VALUES (?, ?, ?, ?) ON CONFLICT(snapshot_id) DO NOTHING",
                    values,
                )
                stored = db.execute(
                    "SELECT * FROM snapshots WHERE snapshot_id=?",
                    (snapshot.snapshot_id,),
                ).fetchone()
                if tuple(stored) != values:
                    raise OperationError("identity_conflict")
            if binding is not None:
                inserted = db.execute(
                    "INSERT INTO imports VALUES (?, ?, ?, ?, ?) ON CONFLICT(key) DO NOTHING",
                    (
                        binding.key,
                        binding.parser_hash,
                        binding.bundle_hash,
                        binding.import_id,
                        binding.report_hash,
                    ),
                )
                if (
                    inserted.rowcount != 1
                    and db.execute(
                        "SELECT report_hash FROM imports WHERE key=?",
                        (binding.key,),
                    ).fetchone()[0]
                    != binding.report_hash
                ):
                    raise OperationError("idempotency_conflict")
            db.executemany(
                "INSERT INTO artifacts VALUES (?, ?, ?, ?)",
                [(run.run_id, key, ref.kind, ref.sha256) for key, ref in artifacts.items()],
            )
            publication_id = uuid4().hex
            for key, ref in artifacts.items():
                identity: SnapshotIdentity | RunOutputIdentity
                if ref.kind == "validated_snapshot":
                    assert snapshot is not None
                    identity = SnapshotIdentity(
                        snapshot_id=snapshot.snapshot_id,
                        portfolio_id=snapshot.portfolio_id,
                    )
                else:
                    identity = RunOutputIdentity(
                        run_id=run.run_id,
                        stage=ARTIFACT_STAGES[ref.kind],
                        config_hash=run.config_hash,
                    )
                publication = CommittedPublication(
                    publication_id=publication_id,
                    run_id=run.run_id,
                    artifact_hash=ref.sha256,
                    artifact_kind=ref.kind,
                    byte_length=self._artifact(ref.sha256).stat().st_size,
                    publication_state="committed",
                    expected_run_revision=previous_revision,
                    semantic_identity=identity,
                )
                db.execute(
                    "INSERT INTO artifact_publications VALUES (?, ?, ?)",
                    (run.run_id, key, publication.model_dump_json()),
                )
            updated = db.execute(
                "UPDATE runs SET revision=?, result=? WHERE run_id=? AND revision=?",
                (
                    run.revision,
                    metadata,
                    run.run_id,
                    previous_revision,
                ),
            )
            if updated.rowcount != 1:
                raise OperationError("idempotency_conflict")
            for event in events:
                self._event(db, event)
