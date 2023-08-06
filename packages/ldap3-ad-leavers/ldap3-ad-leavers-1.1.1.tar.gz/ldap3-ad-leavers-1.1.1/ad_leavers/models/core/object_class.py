from datetime import datetime

class ObjectClass:

    def __init__(self, name: str, distinguished_name: str, when_created: datetime):
        """
            This is the ObjectClass model
            This is the Parent class for all AD objects

        Args:
            name (str): The name of the AD object
            distinguished_name (str): The dn of the AD object
            when_created (datetime): The datetime when the AD object was created
        """        
        self.name = name
        self.when_created = when_created
        self.distinguished_name = distinguished_name