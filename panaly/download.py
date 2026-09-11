"""Download missing source files and reuse existing local copies."""

import logging
from pathlib import Path
from urllib.request import urlretrieve

from panaly.models import Proceeding
from panaly.paths import Paths

logger = logging.getLogger(__name__)


def download_source(proceeding: Proceeding, paths: Paths) -> Path:
    cached = paths.source_path(proceeding)
    if cached.exists():
        logger.info("使用本地资源: %s", cached)
        return cached
    target = paths.raw_path(proceeding)
    target.parent.mkdir(parents=True, exist_ok=True)
    logger.info("下载: %s", proceeding.url)
    urlretrieve(proceeding.url, target)
    return target
