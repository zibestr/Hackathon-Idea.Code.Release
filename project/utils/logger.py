import time
import logging
from pathlib import Path
from functools import wraps
import asyncio
from config import settings


def setup_logger():
    log_path = Path(settings.log_path)
    log_dir = log_path.parent
    log_dir.mkdir(parents=True, exist_ok=True)
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)

    logging.basicConfig(
        level=log_level,
        filename=log_path,
        format=settings.log_format,
        datefmt=settings.date_format
    )

    if not settings.silent:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        formatter = logging.Formatter(settings.log_format, datefmt=settings.date_format)
        console_handler.setFormatter(formatter)
        logging.getLogger().addHandler(console_handler)


def logs(func=None, level=None):
    """
    Декоратор для логирования выполнения функций (синхронных и асинхронных).
    Ошибки выводятся в одну строку.
    """
    if func is None:
        return lambda f: logs(f, level=level)

    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__module__)
        log_level = level if level is not None else logging.INFO
        
        start_time = time.time()
        params = []
        if args:
            params.append(', '.join(repr(arg) for arg in args))
        if kwargs:
            params.append(', '.join(f'{k}={repr(v)}' for k, v in kwargs.items()))
        params_str = ', '.join(params)
        
        try:
            result = await func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.log(log_level, f"{func.__name__}({params_str}): completed in {execution_time:.2f}s")
            return result

        except Exception as e:
            error_msg = f"{func.__name__}({params_str}): {type(e).__name__} - {str(e)}"
            if hasattr(e, '__traceback__'):
                tb = e.__traceback__
                filename = tb.tb_frame.f_code.co_filename
                lineno = tb.tb_lineno
                error_msg += f" [at {filename}:{lineno}]"
            
            logger.error(error_msg, exc_info=False)
            raise

    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__module__)
        log_level = level if level is not None else logging.INFO
        
        start_time = time.time()
        params = []
        if args:
            params.append(', '.join(repr(arg) for arg in args))
        if kwargs:
            params.append(', '.join(f'{k}={repr(v)}' for k, v in kwargs.items()))
        params_str = ', '.join(params)
        
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.log(log_level, f"{func.__name__}({params_str}): completed in {execution_time:.2f}s")
            return result

        except Exception as e:
            error_msg = f"{func.__name__}({params_str}): {type(e).__name__} - {str(e)}"
            if hasattr(e, '__traceback__'):
                tb = e.__traceback__
                filename = tb.tb_frame.f_code.co_filename
                lineno = tb.tb_lineno
                error_msg += f" [at {filename}:{lineno}]"
            
            logger.error(error_msg, exc_info=False)
            raise

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    return sync_wrapper
