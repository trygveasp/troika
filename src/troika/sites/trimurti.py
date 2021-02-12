"""Site accessed via trimurti"""

import logging
import pathlib
import subprocess

from .. import ConfigurationError, InvocationError
from .base import Site

_logger = logging.getLogger(__name__)


class TrimurtiSite(Site):
    """Site accessed via trimurti"""

    def __init__(self, config):
        super().__init__(config)
        self._host = config['host']
        self._trimurti_path = pathlib.Path(config['trimurti_path']).resolve()
        if not self._trimurti_path.exists():
            raise ConfigurationError(
                f"Trimurti path {str(self._trimurti_path)!r} does not exist")

    def submit(self, script, user, output, dryrun=False):
        """See `troika.sites.Site.submit`"""
        script = pathlib.Path(script).resolve()
        if not script.exists():
            raise InvocationError(f"Script file {str(script)!r} does not exist")
        args = [self._trimurti_path, user, self._host, script, output]
        if not dryrun:
            _logger.debug("Executing %s", " ".join(repr(str(arg)) for arg in args))
            subprocess.run(args, check=True)
        else:
            _logger.info("Submit: %s", " ".join(repr(str(arg)) for arg in args))

    def __repr__(self):
        return f"{self.__class__.__name__}(host={self._host!r}, trimurti_path={str(self._trimurti_path)!r})"
