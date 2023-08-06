from py4jps import agentlogging

def test_demo():
    """
        Demo the logging functionality.
    """
    print("=== Development Logging ===")
    dev_logger = agentlogging.get_logger("dev")
    dev_logger.debug("This is a DEBUG statement")
    dev_logger.info("This is an INFO statement")
    dev_logger.warning("This is a WARNING statement.")
    dev_logger.error("This is an ERROR statement.")
    dev_logger.critical("This is a CRITICAL statement.")

    print("=== Production Logging ===")
    prod_logger = agentlogging.get_logger("prod")
    prod_logger.debug("This is a DEBUG statement")
    prod_logger.info("This is an INFO statement")
    prod_logger.warning("This is a WARNING statement.")
    prod_logger.error("This is an ERROR statement.")
    prod_logger.critical("This is a CRITICAL statement.")

    print("=== System Stream ===")
    print("This is a STANDARD OUT statement.")
