from __future__ import annotations

import os
import pathlib
from typing import Dict, Optional, Sequence, TYPE_CHECKING, Tuple, Union
from zipfile import ZIP_DEFLATED

from bioimageio.spec.shared import raw_nodes
from bioimageio.spec.shared.base_nodes import URI
from bioimageio.spec.shared.common import get_format_version_module, get_latest_format_version_module
from bioimageio.spec.shared.io_ import IO_Interface, resolve_rdf_source_and_type
from bioimageio.spec.shared.nodes import ResourceDescription
from bioimageio.spec.shared.raw_nodes import ResourceDescription as RawResourceDescription

if TYPE_CHECKING:
    import bioimageio.spec.model


def _get_matching_io_class(type_: str, data_version: str = "latest") -> IO_Interface:
    if not isinstance(data_version, str):
        raise TypeError("missing or invalid 'format_version'")

    if data_version == "latest":
        v_mod = get_latest_format_version_module(type_)
    else:
        v_mod = get_format_version_module(type_, data_version)

    return v_mod.utils.IO


def load_raw_resource_description(
    source: Union[os.PathLike, str, dict, URI], update_to_current_format: bool = False
) -> RawResourceDescription:
    """load a raw python representation from a BioImage.IO resource description file (RDF).
    Use `load_resource_description` for a more convenient representation.

    Args:
        source: resource description file (RDF)
        update_to_current_format: auto convert content to adhere to the latest appropriate RDF format version

    Returns:
        raw BioImage.IO resource
    """
    data, type_ = resolve_rdf_source_and_type(source)
    io_cls = _get_matching_io_class(
        type_, "latest" if update_to_current_format else data.get("format_version", "latest")
    )

    # not using data here, because a remote source differs from a local source
    return io_cls.load_raw_resource_description(source=source)


def serialize_raw_resource_description_to_dict(raw_rd: RawResourceDescription) -> dict:
    io_cls = _get_matching_io_class(raw_rd.type, raw_rd.format_version)
    return io_cls.serialize_raw_resource_description_to_dict(raw_rd)


def save_raw_resource_description(raw_rd: RawResourceDescription, path: pathlib.Path):
    io_cls = _get_matching_io_class(raw_rd.type, raw_rd.format_version)
    return io_cls.save_raw_resource_description(raw_rd, path)


def serialize_raw_resource_description(raw_rd: Union[dict, RawResourceDescription]) -> str:
    if isinstance(raw_rd, raw_nodes.RawNode):
        assert hasattr(raw_rd, "type")
        type_ = raw_rd.type  # noqa
        assert hasattr(raw_rd, "format_version")
        format_version = raw_rd.format_version  # noqa
    else:
        assert "type" in raw_rd
        type_ = raw_rd["type"]
        assert "format_version" in raw_rd
        format_version = raw_rd["format_version"]

    io_cls = _get_matching_io_class(type_, format_version)
    return io_cls.serialize_raw_resource_description(raw_rd)


def ensure_raw_resource_description(
    raw_rd: Union[str, dict, os.PathLike, URI, RawResourceDescription],
    root_path: os.PathLike = pathlib.Path(),
    update_to_current_format: bool = True,
) -> Tuple[RawResourceDescription, pathlib.Path]:
    if isinstance(raw_rd, raw_nodes.ResourceDescription) and not isinstance(raw_rd, URI):
        return raw_rd, pathlib.Path(root_path)

    data, type_ = resolve_rdf_source_and_type(raw_rd)
    format_version = "latest" if update_to_current_format else data.get("format_version", "latest")
    io_cls = _get_matching_io_class(type_, format_version)

    return io_cls.ensure_raw_rd(raw_rd, root_path)


def load_resource_description(
    source: Union[RawResourceDescription, os.PathLike, str, dict, URI],
    root_path: os.PathLike = pathlib.Path(),
    *,
    update_to_current_format: bool = True,
    weights_priority_order: Optional[Sequence[str]] = None,
) -> ResourceDescription:
    """load a BioImage.IO resource description file (RDF).
    This includes some transformations for convenience, e.g. importing `source`.
    Use `load_raw_resource_description` to obtain a raw representation instead.

    Args:
        source: resource description file (RDF) or raw BioImage.IO resource
        root_path: to resolve relative paths in the RDF (ignored if source is path/URI)
        update_to_current_format: auto convert content to adhere to the latest appropriate RDF format version
        weights_priority_order: If given only the first weights format present in the model resource is included
    Returns:
        BioImage.IO resource
    """
    raw_rd, _ = ensure_raw_resource_description(source, root_path, update_to_current_format)

    io_cls = _get_matching_io_class(raw_rd.type, raw_rd.format_version)
    return io_cls.load_resource_description(source, root_path, weights_priority_order=weights_priority_order)


def export_resource_package(
    source: Union[RawResourceDescription, os.PathLike, str, dict, URI],
    root_path: os.PathLike = pathlib.Path(),
    *,
    output_path: Optional[os.PathLike] = None,
    update_to_current_format: bool = False,
    weights_priority_order: Optional[Sequence[Union[bioimageio.spec.model.v0_3.base_nodes.WeightsFormat]]] = None,
    compression: int = ZIP_DEFLATED,
    compression_level: int = 1,
) -> pathlib.Path:
    """Package a BioImage.IO resource as a zip file.

    Args:
        source: raw resource description, path, URI or raw data as dict
        root_path: for relative paths (only used if source is RawResourceDescription or dict)
        output_path: file path to write package to
        update_to_current_format: Convert not only the patch version, but also the major and minor version.
        weights_priority_order: If given only the first weights format present in the model is included.
                                If none of the prioritized weights formats is found all are included.
        compression: The numeric constant of compression method.
        compression_level: Compression level to use when writing files to the archive.
                           See https://docs.python.org/3/library/zipfile.html#zipfile.ZipFile

    Returns:
        path to zipped BioImage.IO package in BIOIMAGEIO_CACHE_PATH or 'output_path'
    """
    raw_rd, _ = ensure_raw_resource_description(source, root_path, update_to_current_format)
    io_cls = _get_matching_io_class(raw_rd.type, raw_rd.format_version)
    return io_cls.export_resource_package(
        source,
        root_path,
        output_path=output_path,
        weights_priority_order=weights_priority_order,
        compression=compression,
        compression_level=compression_level,
    )


def get_resource_package_content(
    source: Union[RawResourceDescription, os.PathLike, str, dict],
    root_path: pathlib.Path,
    update_to_current_format: bool = False,
    *,
    weights_priority_order: Optional[Sequence[str]] = None,
) -> Dict[str, Union[str, pathlib.Path]]:
    """
    Args:
        source: raw resource description, path, URI or raw data as dict
        root_path:  for relative paths (only used if source is RawResourceDescription or dict)
        update_to_current_format: Convert not only the patch version, but also the major and minor version.
        weights_priority_order: If given only the first weights format present in the model is included.
                                If none of the prioritized weights formats is found all are included.

    Returns:
        Package content of local file paths or text content keyed by file names.
    """
    raw_rd, _ = ensure_raw_resource_description(source, root_path, update_to_current_format)
    io_cls = _get_matching_io_class(raw_rd.type, raw_rd.format_version)
    return io_cls.get_resource_package_content(source, root_path, weights_priority_order=weights_priority_order)
