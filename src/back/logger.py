import logging
import logging.handlers
from pathlib import Path
from datetime import datetime


_log_initialized: dict[str, logging.Logger] = {}


def get_logger(
    debug: bool = False,
    name: str = "main",
    add_stream_handler: bool = True,
    log_dir: str = "log",
    when: str = "midnight",
    interval: int = 1,
    backup_count: int = 7
) -> logging.Logger:
    """loggerを取得
    関数を読み込む前に実行
    Args:
        debug (bool): デバッグモードにするか?, Falseの場合、INFO
        name (str, optional): ログの名前
        add_stream_handler (bool, optional): ストリーム出力
        log_dir (str, optional): ログファイルを保存するディレクトリ
        when (str, optional): ログローテーションのタイミング
        interval (int, optional): ログローテーションの間隔
        backup_count (int, optional): 保存するバックアップファイルの数
    Returns:
        logging.Logger: Logger instance.
    """
    global _log_initialized
    logger = _log_initialized.get(name, None)
    if logger is not None:
        return logger

    format = (
        '%(levelname)-8s: %(asctime)s | %(filename)-12s - %(funcName)-12s : '
        '%(lineno)-4s -- %(message)s'
    )
    logger = logging.getLogger(name)

    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    if add_stream_handler:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter(format))
        logger.addHandler(stream_handler)

    # 日付形式のファイル名を生成
    filename = datetime.now().strftime("%Y%m%d.log")
    log_dir_path = Path(log_dir)
    log_dir_path.mkdir(parents=True, exist_ok=True)
    log_path = log_dir_path / filename
    file_handler = logging.handlers.TimedRotatingFileHandler(
        log_path,
        when=when,
        interval=interval,
        backupCount=backup_count,
        encoding="utf-8"
    )
    file_handler.setFormatter(logging.Formatter(
        format, datefmt='%Y-%m-%d %H:%M:%S'
    ))
    logger.addHandler(file_handler)

    _log_initialized[name] = logger
    return logger


if __name__ == "__main__":
    logger = get_logger(debug=False)
    logger.info("info message")
    logger.debug("debug message")
