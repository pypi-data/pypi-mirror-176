from __future__ import annotations

import sys
from typing import IO, cast

import click

from lockfile_diff.base import InputSchema
from lockfile_diff.registries import Registries
from lockfile_diff.types import ParsedData
from lockfile_diff.util.io.rewind import capture


class AutoDetectSchema(InputSchema):
    schema = "auto-detect"

    def parse(self, source: IO) -> ParsedData:
        errors = []
        for schema_cls in Registries.get_default().schemas.values():
            if schema_cls is AutoDetectSchema:
                continue
            try:
                with capture(source):
                    return cast(InputSchema, schema_cls()).parse(source)
            except Exception as e:
                errors.append(f"  - `{schema_cls.schema}`: {e}")

        click.echo(
            f"ERROR: `auto-detect` failed to parse {getattr(source, 'name', str(source))!r} with "
            "any of the following schemas:"
        )
        click.echo("\n".join(errors))
        sys.exit(1)
