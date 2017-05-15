import os
import logging


MISSING_MODULE_NAME_KWARG_ERR = ('missing required module_name kwarg. Try '
                                 'passing __name__ from module where used')


def log_warning(message, module_name=None):
    if module_name is None:
        raise TypeError(MISSING_MODULE_NAME_KWARG_ERR)

    logger = logging.getLogger(module_name)
    logger.warn(message)


def env_get_or_warn(variable):
    try:
        return os.environ[variable]
    except KeyError:
        log_warning("Environment variable {} is not set!".format(variable),
                    module_name=__name__)
        pass
