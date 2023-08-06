
# > All custom exceptions are defined here

class AdSearchException(Exception):
    """
        Will raise all exceptions that are related to an AD search operation
    Args:
        Exception (Exception): Inherits the Exception class
    """    
    pass

class AdModifyException(Exception): 
    """
        Will raise all exceptions that are related to an AD Modify operation
    Args:
        Exception (Exception): Inherits the Exception class
    """    
    pass