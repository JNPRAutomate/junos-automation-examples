import logging

import jcs


class JCSConsoleHandler(logging.Handler):
    """Custom handler that uses appropriate jcs functions based on log level"""

    def emit(self, record):
        try:
            msg = self.format(record)

            if record.levelno >= logging.ERROR:
                jcs.emit_error(msg)
            elif record.levelno >= logging.WARNING:
                jcs.emit_warning(msg)
            else:
                jcs.output(msg)

        except Exception:
            self.handleError(record)


class JCSSyslogHandler(logging.Handler):
    """Custom handler that uses jcs.syslog for syslog output"""

    LEVEL_MAP = {
        logging.DEBUG: "debug",
        logging.INFO: "info",
        logging.WARNING: "warning",
        logging.ERROR: "error",
        logging.CRITICAL: "critical",
    }

    def __init__(self, facility="external"):
        """
        Initialize the syslog handler.

        Args:
            facility: Syslog facility (e.g., 'external', 'pfe', 'daemon')
                     Do not include the severity - it will be added based on log level
        """
        super().__init__()
        self.facility = facility

    def emit(self, record):
        try:
            msg = self.format(record)
            severity = self.LEVEL_MAP.get(record.levelno, "info")
            priority = f"{self.facility}.{severity}"
            jcs.syslog(priority, msg)
        except Exception:
            self.handleError(record)


def setup_logging(
    context=__name__,
    enable_console=True,
    enable_syslog=True,
    console_level=logging.INFO,
    syslog_level=logging.WARNING,
):
    """
    Setup logging with JCS handlers.

    Args:
        context: Logger name/context (default: __name__)
        enable_console: Whether to enable console output via JCS functions (default: True)
        enable_syslog: Whether to enable syslog output (default: True)
        console_level: Logging level for console output (default: logging.INFO)
        syslog_level: Logging level for syslog output (default: logging.WARNING)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(context)
    logger.setLevel(logging.DEBUG)

    console_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    syslog_formatter = logging.Formatter("%(name)s[%(process)d]: %(levelname)s - %(message)s")

    if enable_console:
        console_handler = JCSConsoleHandler()
        console_handler.setLevel(console_level)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    if enable_syslog:
        syslog_handler = JCSSyslogHandler(facility="external")
        syslog_handler.setLevel(syslog_level)
        syslog_handler.setFormatter(syslog_formatter)
        logger.addHandler(syslog_handler)

    return logger
