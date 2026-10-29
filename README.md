# i_storage

A small Python library for representing storage through interfaces, with a local
filesystem implementation. Build application code around folders, byte-oriented
files, and component-based paths, then implement the same interfaces for other
storage backends.

- Abstract interfaces for files, folders, paths, and filename rules.
- Local filesystem implementations with binary read, write, and append operations.
- Explicit success and failure results for storage mutations.
- Filename validation and mutable or immutable path objects.
- Python 3.10+ with no runtime dependencies.

## Installation

Install directly from GitHub:

```bash
python -m pip install "git+https://github.com/GGN-2015/i_storage.git"
```

Or install from a local checkout:

```bash
python -m pip install .
```

For an editable development installation, use `python -m pip install -e .`.
The distribution name is `i-storage`; the Python import is `i_storage`.

## Quick start

This example creates `storage/reports/example.txt`, writes its contents, and reads
them back. `C_Folder` takes an absolute filesystem path. Creating a file also
creates its parent directories.

```python
from pathlib import Path

from i_storage import C_Folder, C_Path, I_Status


def require_success(status: I_Status) -> None:
    if not status.isSuccess():
        raise RuntimeError(status.getFailueReason())


storage = C_Folder(str(Path("storage").resolve()))
file_path = C_Path(["reports", "example.txt"])

require_success(storage.createDataFile(file_path))
data_file = storage.getDataFile(file_path)
if data_file is None:
    raise FileNotFoundError("/".join(file_path.getList()))

require_success(data_file.setContent(b"Hello"))
require_success(data_file.append(b", storage!\n"))

print(data_file.getContent().decode("utf-8"), end="")
print(data_file.getLength())
```

Output:

```text
Hello, storage!
16
```

`createDataFile()` preserves an existing file's contents. `setContent()` replaces
the contents, while `append()` adds bytes to the end.

## Core types

All public types are available directly from `i_storage`.

| Interface | Implementation | Purpose |
| --- | --- | --- |
| `I_Status` | `C_Success`, `C_Failure` | Operation results and failure messages. |
| `I_File` | Shared base type | Common type for data files and folders. |
| `I_DataFile` | `C_DataFile` | Read, replace, and append binary contents. |
| `I_Folder` | `C_Folder` | Create, retrieve, and remove files and folders. |
| `I_Path` | `C_Path` | Read path components through an immutable path. |
| `I_MutablePath` | `C_MutablePath` | A path with push and pop operations. |
| `I_NameRule` | Custom rule implementations | Validate one filename component. |
| `I_NameRuleList` | `C_NameRuleList` | Apply filename rules in order. |

## Paths and filename validation

Paths are lists of individual names relative to a `C_Folder`:

```python
from i_storage import C_Path

path = C_Path(["reports", "2026", "summary.txt"])

assert path.getDepth() == 3
assert path.getName(0) == "reports"
assert path.getList() == ["reports", "2026", "summary.txt"]
```

Use one component per directory or filename, rather than a string containing path
separators. `C_Path([])` refers to the folder itself. Parent traversal through
`..` is rejected by the built-in validation rules.

`C_Path` and `C_MutablePath` use `C_NameRuleList`, which rejects:

- Empty names and ASCII control characters from 0 through 31.
- Names ending in a dot or starting or ending with whitespace.
- Forward slashes and backslashes.
- Characters in `:<>?|*`, single and double quotes, and backticks.
- Exact names `CON`, `PRN`, `AUX`, `NUL`, `COM1` through `COM9`, and `LPT1` through
  `LPT9`, ignoring case. The full name is checked, so `CON.txt` passes this rule.

An invalid component makes `C_Path` raise `FileNameNotPermitted`, a subclass of
`ValueError`:

```python
from i_storage import C_Path, FileNameNotPermitted

try:
    C_Path(["reports", "bad/name.txt"])
except FileNameNotPermitted as error:
    print(f"Invalid path component: {error}")
```

For incremental construction, `pushBack()` returns an `I_Status` and appends the
component only when validation succeeds. `pop()` removes the last component and
does nothing on an empty path.

```python
from i_storage import C_MutablePath

mutable_path = C_MutablePath()
for component in ("reports", "2026"):
    status = mutable_path.pushBack(component)
    if not status.isSuccess():
        raise ValueError(status.getFailueReason())

mutable_path.pop()
assert mutable_path.getList() == ["reports"]
```

## Folder operations

| Method | Behavior |
| --- | --- |
| `createDataFile(path)` | Create an empty file and its parent directories. Preserve an existing file. Return `I_Status`. |
| `createFolder(path)` | Create a directory and its parents. An existing directory is accepted. Return `I_Status`. |
| `isExist(path)` | Return whether a file or folder exists; return `False` on a caught error. |
| `getDataFile(path)` | Return an `I_DataFile`, or `None` if missing, not a file, or a caught error occurs. |
| `getFolder(path)` | Return an `I_Folder`, or `None` if missing, not a folder, or a caught error occurs. |
| `remove(path)` | Remove a file or recursively remove a directory. An absent target is accepted. Return `I_Status`. |

Removing a directory deletes its contents. Removing the folder itself with
`remove(C_Path([]))` returns a failure.

## Data file operations

| Method | Behavior |
| --- | --- |
| `getLength()` | Return the file size in bytes. Filesystem errors propagate as exceptions. |
| `getContent()` | Read the entire file as `bytes`. Return `b""` on a caught error. |
| `setContent(content)` | Replace the file's contents with `bytes`. Return `I_Status`. |
| `append(content)` | Append `bytes` to the file. Return `I_Status`. |

Encode and decode text explicitly, as shown in the quick start. An empty result
from `getContent()` can mean either an empty file or a read failure.

## Status results and error helpers

Check `isSuccess()` after a mutation and use `getFailueReason()` to retrieve its
failure message. `C_Success` returns `True` and an empty message; `C_Failure`
returns `False` and the supplied message.

Two decorators are also exported for use in your own implementations:

- `W_ErrorWrap`: convert a caught `Exception` into `C_Failure(repr(error))`, while
  preserving the wrapped function's normal return value.
- `W_ErrorDefault(default_value)`: return the supplied fallback value when the
  wrapped function raises an `Exception`.

## Extending the library

Implement `I_Folder` and `I_DataFile` to provide another storage backend while
keeping callers on the same interfaces. Implement `I_Path` for another path
representation, or `I_MutablePath` for an incrementally built path.

For custom filename validation, implement `I_NameRule.check(name)` and expose
rules through an `I_NameRuleList` implementation. Its inherited `check()` method
runs the rules in order and returns the first failure. A custom path
implementation can use this rule list in place of the built-in rules.

## License

MIT. See [LICENSE](LICENSE).
