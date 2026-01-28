# Architecture — Plan‑Gated Folder Tidy

> **Last Updated**: 2026-01-28  
> **Status**: Core implementation complete ✅

## Layers

### 1. Provider Layer
**Status**: ✅ Implemented

- **LocalWalkProvider** (`src/inventory_master/providers/local_walk.py`): Fallback provider for local file scanning
  - Recursive directory walk
  - Optional file hashing (SHA-256)
  - File metadata collection (size, mtime)
  
- **Everything ES Provider** (`src/inventory_master/providers/everything_es.py`): Everything ES CLI integration (preferred)
  - Requires Everything to be installed and running
  - Uses ES CLI: `-path <root>`, `/a-d` (files only), `-s` (sort by path)
  - Auto-discovers `es.exe` via PATH or common install paths
  - `find_es_exe()`, `is_available()` for fallback logic
  - Optional `hash_files` (SHA-256); timeout and max_results configurable
  - Fast indexed file search; skips `_meta` paths
  
- **Provider Base** (`src/inventory_master/providers/base.py`): Abstract provider interface
  - `Provider` ABC with `iter_files()` method
  - `FileRecord` dataclass for file metadata

### 2. Analysis Layer
**Status**: ✅ Implemented

- **Reporting** (`src/inventory_master/reporting.py`): Read-only report generation
  - Extension statistics
  - File counts
  - Reports saved to `_meta/reports/`
  - Markdown format output

### 3. Planner Layer
**Status**: ✅ Implemented

- **Planner** (`src/inventory_master/planner.py`): Plan JSON generation
  - Generates immutable plan JSON under `_meta/plans/`
  - Default rule: Move `.tmp`/`.bak` files to `99_QUARANTINE/`
  - Policy enforcement (allow_delete, require_hash_verify, require_dry_run, max_actions)
  - Plan ID based on timestamp

### 4. Approve Gate Layer
**Status**: ✅ Implemented

- **Approval** (`src/inventory_master/approve.py`): Human approval gate
  - Creates approval token file under `_meta/approvals/`
  - Token format: `APPROVED__{plan_id}.token`
  - Required before any apply operation

### 5. Executor Layer
**Status**: ✅ Implemented

- **Executor** (`src/inventory_master/executor.py`): Transactional apply with safety checks
  - **Dry-run mode**: Preview changes without applying
  - **Approval verification**: Checks for approval token
  - **Dry-run requirement**: Enforces dry-run before actual apply
  - **Atomic operations**: Uses `os.rename()` for atomic moves
  - **Hash verification**: Optional SHA-256 verification (pre/post)
  - **Rollback**: Automatic rollback on verification failure
  - **Audit logging**: All operations logged to `_meta/audit/audit.jsonl`

### 6. Verify Layer
**Status**: ✅ Implemented

- **Snapshot** (`src/inventory_master/snapshot.py`): Before/after snapshots
  - Creates file manifest with paths, sizes, mtimes, hashes
  - JSON format stored in `_meta/snapshots/`
  - Hash-based change detection
  - Supports hash verification for integrity checks

### 7. Supporting Systems
**Status**: ✅ Implemented

- **Audit** (`src/inventory_master/audit.py`): Append-only audit logging
  - JSONL format (one event per line)
  - Timestamped events
  - Events: `dry_run`, `apply_start`, `action_committed`, `apply_done`
  
- **Hashing** (`src/inventory_master/hashing.py`): SHA-256 file hashing
  - Streaming hash calculation (memory efficient)
  - Chunk-based reading (1MB chunks)
  
- **Meta Paths** (`src/inventory_master/meta_paths.py`): Metadata directory management
  - Ensures `_meta/*` directory structure
  - Creates: inventory, reports, plans, audit, snapshots, approvals
  
- **Models** (`src/inventory_master/models.py`): Data models
  - `FileRecord`: File metadata (path, size, mtime, sha256)
  - `PlanAction`: Plan action definition (id, type, src, dst)
  - `ActionType`: Literal type for action types (move, rename, quarantine)

### 8. CLI Interface
**Status**: ✅ Implemented

- **CLI** (`src/inventory_master/cli.py`): Command-line interface
  - `report`: Generate read-only report
  - `plan`: Generate plan JSON
  - `approve`: Create approval token
  - `apply`: Apply plan (requires `--dry-run` first)

## Data Flow

```
User Command
    ↓
CLI (cli.py)
    ↓
┌─────────────────────────────────────┐
│  report: Reporting → _meta/reports/ │
│  plan: Planner → _meta/plans/        │
│  approve: Approve → _meta/approvals/ │
│  apply: Executor → File operations   │
└─────────────────────────────────────┘
    ↓
Provider (LocalWalk/Everything)
    ↓
Audit Logging
    ↓
Snapshot Verification
```

## Safety Mechanisms

1. **Approval Gate**: All apply operations require explicit approval token
2. **Dry-run Required**: Must execute dry-run before actual apply
3. **Hash Verification**: Optional SHA-256 verification for file integrity
4. **Atomic Operations**: Uses `os.rename()` for atomic file moves
5. **Rollback**: Automatic rollback on verification failure
6. **Audit Trail**: All operations logged to append-only audit log
7. **Snapshots**: Before/after snapshots for recovery

## Local root
Default root is `C:\\inventory_master\\` (override with `--root`).

## Everything integration notes
- ES requires Everything to be running.
- HTTP server can expose indexed files, so bind to 127.0.0.1 and disable downloads.
- LocalWalkProvider serves as fallback when Everything is unavailable.

## Implementation Status

### ✅ Completed (2026-01-28)
- Core CLI commands (report, plan, approve, apply)
- Planner with default quarantine rule
- Executor with transactional apply
- Approval gate system
- Audit logging system
- Snapshot system
- Hashing system
- LocalWalkProvider
- Basic test coverage (6 tests passing)

### ✅ Everything ES Provider (2026-01-28)
- ES CLI integration complete with `-path`, `/a-d`, `-s`
- Provider selection in reporting: try Everything first, fallback to LocalWalk
- Fallback on failure (not running, timeout, etc.)

### Everything HTTP Provider (2026-01-28)
- **EverythingHTTPProvider** (`src/inventory_master/providers/everything_http.py`): Everything HTTP Server (read-only)
  - Requires HTTP Server enabled in Everything (Tools → Options → HTTP Server; default port 8080)
  - Uses stdlib `urllib` only (no extra deps)
  - `is_available(host, port)` for health check
  - Query: `s=<path>`, `p=1` (path match), `j=1` (JSON), path/size/date_modified columns
  - Security: bind to 127.0.0.1; disable file download in Everything options

### Everything SDK Provider (2026-01-28)
- **EverythingSDKProvider** (`src/inventory_master/providers/everything_sdk.py`): Everything SDK DLL (Windows only)
  - Requires Everything running and Everything64.dll / Everything32.dll
  - Uses ctypes; auto-discovers DLL in common paths
  - `is_available(dll_path)` for availability check
  - SetSearchW(path), SetMatchPath(1), QueryW(1), GetResultFullPathNameW, IsFileResult, GetResultSize, GetResultDateModified
  - Skips `_meta`; optional `hash_files`, `max_results`

### Provider fallback order (reporting)
1. Everything ES (es.exe)
2. Everything HTTP (localhost:8080)
3. Everything SDK (DLL)
4. LocalWalk (filesystem)

### 🚧 Future Enhancements
- Advanced classification rules
- Performance optimizations
- Extended test coverage
