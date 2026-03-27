#!/usr/bin/env python3

"""Execute the shipped example notebooks as a smoke test."""

from __future__ import annotations

import argparse
import os
import sys
import tempfile
from pathlib import Path

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from jupyter_client.kernelspec import NoSuchKernel


def notebook_paths(root: Path) -> list[Path]:
    groups = [
        root / 'opal' / 'test',
        root / 'tests',
        root / 'surrogate',
    ]
    paths = []
    for group in groups:
        paths.extend(sorted(group.glob('*.ipynb')))
    return paths


def configure_environment(root: Path) -> None:
    os.environ['PYTHONPATH'] = os.pathsep.join(
        filter(None, [str(root), os.environ.get('PYTHONPATH')])
    )
    cache_root = Path(tempfile.gettempdir()) / 'pyopaltools-notebooks'
    os.environ.setdefault('MPLCONFIGDIR', str(cache_root / 'mpl'))
    os.environ.setdefault('XDG_CACHE_HOME', str(cache_root / 'xdg'))
    os.environ.setdefault('IPYTHONDIR', str(cache_root / 'ipython'))
    os.environ.setdefault('PYTHONPYCACHEPREFIX', str(cache_root / 'pycache'))


def run_notebook(path: Path) -> None:
    with path.open() as handle:
        notebook = nbformat.read(handle, as_version=4)

    kernel_name = notebook.metadata.get('kernelspec', {}).get('name', 'python3')
    resources = {'metadata': {'path': str(path.parent)}}

    try:
        executor = ExecutePreprocessor(timeout=180, kernel_name=kernel_name)
        executor.preprocess(notebook, resources)
    except NoSuchKernel:
        executor = ExecutePreprocessor(timeout=180, kernel_name='python3')
        executor.preprocess(notebook, resources)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('notebooks', nargs='*', help='Optional notebook paths to run')
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    configure_environment(root)

    if args.notebooks:
        targets = [Path(notebook).resolve() for notebook in args.notebooks]
    else:
        targets = notebook_paths(root)

    failures = []
    for notebook in targets:
        relpath = notebook.relative_to(root)
        print(f'RUN {relpath}', flush=True)
        try:
            run_notebook(notebook)
        except Exception as exc:  # pragma: no cover - smoke-test reporting
            failures.append((relpath, exc))
            print(f'FAIL {relpath}: {exc}', flush=True)
        else:
            print(f'OK {relpath}', flush=True)

    if failures:
        print('\nNotebook failures:')
        for relpath, exc in failures:
            print(f'- {relpath}: {exc}')
        return 1

    print(f'\nExecuted {len(targets)} notebooks successfully.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
