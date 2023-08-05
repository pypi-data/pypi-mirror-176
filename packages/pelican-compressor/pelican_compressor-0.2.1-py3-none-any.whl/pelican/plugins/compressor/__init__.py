"""
This module is part of the 'pelican-compressor' package,
which is released under GPL-3.0-only license.
"""

import logging
from pathlib import Path
from typing import List, Tuple, Union
import uuid

from web_compressor import WebCompressor

from pelican import Pelican, signals

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


def worker(pelican: Pelican) -> None:
    """
    Wrapper for 'WebCompressor'

    :param pelican: pelican.Pelican Pelican object
    :return: None
    """

    # Report initialization
    LOGGER.info("PLUGIN pelican-compressor was loaded")

    # Party time!
    obj = WebCompressor(Path(pelican.settings["OUTPUT_PATH"]))

    # Enable file exclusion (if specified)
    obj.block_list = pelican.settings.get("COMPRESSOR_BLOCK_LIST", [])

    # Apply 'pre' hook
    if (pre_hook := pelican.settings.get("COMPRESSOR_PRE_HOOK")) and callable(pre_hook):
        obj.apply_hook(pre_hook)

    # Minify web assets
    if pelican.settings.get("COMPRESSOR_ENABLE_MINIFY", True):
        obj.minify_assets(
            # For supported mediatypes,
            # see https://github.com/tdewolff/minify/tree/master/bindings/py#mediatypes
            mediatypes=pelican.settings.get("COMPRESSOR_MINIFY_MEDIATYPES"),
            options=pelican.settings.get("COMPRESSOR_MINIFY_OPTIONS"),
        )

    # Optimize images
    if pelican.settings.get("COMPRESSOR_ENABLE_IMAGEOPTIM", False):
        obj.optimize_images(
            mediatypes=pelican.settings.get("COMPRESSOR_IMAGEOPTIM_MEDIATYPES"),
            quality=pelican.settings.get("COMPRESSOR_JPEG_QUALITY", 75),
            strip_meta=pelican.settings.get("COMPRESSOR_STRIP_METADATA", True),
        )

    # Gotta hash 'em all
    if pelican.settings.get("COMPRESSOR_ENABLE_HASHING", True):
        obj.hash_assets(
            mediatypes=pelican.settings.get("COMPRESSOR_HASHING_MEDIATYPES"),
            hash_length=pelican.settings.get("COMPRESSOR_HASH_LENGTH", 10),
            use_mtime=pelican.settings.get("COMPRESSOR_HASH_MODIFIED", False),
        )

    # Convert images
    if pelican.settings.get("COMPRESSOR_ENABLE_MODERN_FORMATS", False):
        obj.convert_images(
            avif=pelican.settings.get("COMPRESSOR_AVIF_SETTINGS", {"quality": 90}),
            webp=pelican.settings.get("COMPRESSOR_WEBP_SETTINGS", {"method": 6}),
        )

    # Minify HTML files (see comment below)
    if pelican.settings.get("COMPRESSOR_ENABLE_MINIFY", True):
        obj.minify_html(options=pelican.settings.get("COMPRESSOR_MINIFY_OPTIONS"))

    # Add subresource integrity values (SRI)
    if pelican.settings.get("COMPRESSOR_ENABLE_SRI", True):
        obj.generate_sri(pelican.settings.get("COMPRESSOR_SRI_DIGEST", "sha512"))

    # Generate content security policy (CSP)
    if pelican.settings.get("COMPRESSOR_ENABLE_CSP", False):
        obj.generate_csp(
            digest=pelican.settings.get("COMPRESSOR_CSP_DIGEST", "sha512"),
            nonce=pelican.settings.get(
                "COMPRESSOR_CSP_NONCE", f"nonce-{uuid.uuid4().hex}"
            ),
            sets=pelican.settings.get("COMPRESSOR_CSP_DIRECTIVES", {}),
        )

    # Minify HTML files .. again (see comment below)
    if pelican.settings.get("COMPRESSOR_ENABLE_MINIFY", True):
        obj.minify_html(options=pelican.settings.get("COMPRESSOR_MINIFY_OPTIONS"))

    # NOTE:
    # Minifying HTML files also compresses inline styles/scripts,
    # which interferes with generating hashes for them, and since
    # this leads to invalid hashes, we have twice - any solutions
    # or PRs are welcome!

    # Apply 'post' hook
    if (post_hook := pelican.settings.get("COMPRESSOR_POST_HOOK")) and callable(
        post_hook
    ):
        obj.apply_hook(post_hook)


def register() -> None:
    """
    Registers 'WebCompressor' plugin

    For more information,
    see https://docs.getpelican.com/en/latest/plugins.html

    :return: None
    """

    signals.finalized.connect(worker)
