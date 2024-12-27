from gvars import PATH_LOGS, FILENAME
import pieces

def create_logger():
    
    path_file =  PATH_LOGS
    filename = FILENAME
    
    if not pieces.os.path.isdir(path_file):
        pieces.os.mkdir(path_file)
   
    if not pieces.os.path.exists(filename):
        with open(filename, 'a'): 
            pass

    # create Logger
    logger = pieces.logging.getLogger(__name__)
    logger.setLevel(pieces.logging.DEBUG)
    logger.propagate = False

    # create console handler and set level
    ch = pieces.logging.StreamHandler()
    ch.setLevel(pieces.logging.DEBUG)

    # create file handler and set level
    fh = pieces.logging.FileHandler(
        filename=filename, 
        mode="a", 
        encoding="utf-8"
    )
    fh.setLevel(pieces.logging.DEBUG)

    # create formatter
    formatter = pieces.logging.Formatter(
        "%(asctime)s - [%(levelname)s] - {%(filename)s:%(lineno)d} - %(message)s", 
        datefmt="%d-%m-%y %H:%M:%S %p"
    )

    # add formatter to ch and fh
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # add ch and fh to Logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger

# set logger global variable
global logger
logger = create_logger()

if __name__ == "__main__":
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")