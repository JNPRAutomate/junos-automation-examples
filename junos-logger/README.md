# junos-logger

A Python logging utility for Junos on-box scripts that integrates with JCS functions.

## Overview

This library provides a simple logging interface that uses appropriate Juniper JCS functions (`jcs.output`, `jcs.emit_warning`, `jcs.emit_error`, `jcs.syslog`) based on log levels, making it easy to create well-structured on-box scripts for Junos devices.

## Features

- **Automatic JCS function mapping**: Log levels automatically map to appropriate JCS functions
  - INFO → `jcs.output()`
  - WARNING → `jcs.emit_warning()`
  - ERROR/CRITICAL → `jcs.emit_error()`
- **Syslog integration**: Optional syslog output via `jcs.syslog()`
- **Flexible configuration**: Enable/disable console and syslog handlers independently
- **Standard logging interface**: Uses Python's standard `logging` module

## Important notes

From Juniper documentation:

> The output() function is not supported in commit scripts. SLAX and XSLT commit scripts use the <xnm:warning> and <xnm:error> result tree elements to display text on the CLI, and Python commit scripts use the emit_warning() and emit_error() functions.

Therefore, if you are using these classes in a commit script you should call `logger.warning` and `logger.error` if you wish your message to be displayed.

## Installation

Copy the `JCSConsoleHandler`, `JCSSyslogHandler`, and `setup_logging` classes/functions from `junos_logger.py` directly into your script.

## Usage

### Basic Usage

```python
logger = setup_logging(context=my_app)

logger.debug("This is a debug message (won't show - level too low)")
logger.info("This is an info message (goes to console via jcs.output)")
logger.warning("This is a warning message (goes to console via jcs.emit_warning and syslog)")
logger.error("This is an error message (goes to console via jcs.emit_error and syslog)")
```

### Custom Setup

```python
logger = setup_logging(
    context='my_script',
    enable_console=True,
    enable_syslog=True,
    console_level=logging.DEBUG,
    syslog_level=logging.ERROR
)

logger.debug("This DEBUG message goes to console only")
logger.info("This INFO message goes to console only")
logger.error("This ERROR message goes to both console and syslog")
```

## Documentation

For more information on JCS functions, see the [Juniper documentation](https://www.juniper.net/documentation/us/en/software/junos/automation-scripting/topics/concept/junos-script-automation-junos-extension-functions-jcs-namespace.html).
