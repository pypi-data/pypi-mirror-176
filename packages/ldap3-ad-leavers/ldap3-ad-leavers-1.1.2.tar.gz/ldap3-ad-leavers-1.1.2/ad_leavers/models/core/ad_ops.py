from abc import ABC, abstractmethod
from ldap3 import Server, ServerPool, Connection, SAFE_SYNC, RANDOM
from ad_leavers.models.core.object_class import ObjectClass

class AdOperations(ABC):

    __CONNECTION_TIMEOUT = 10

    def __init__(self, hosts, username: str, password: str) -> None:

        """
            This is an abstract class that will model all AD objects of this project
            All AD object class operations will inherit from this class
            Authentication is done in constructor

        Args:
            hosts (list[str]): This is a list of AD hosts that will be added to the Server Pool
            username (str): This is the username that ldap3 will assume to connect to the AD sosts
            password (str): This is the password for the account
        """        

        # * Create a server pool and add the servers in it
        server_pool = ServerPool([Server(host, connect_timeout=self.__CONNECTION_TIMEOUT) for host in hosts], RANDOM)

        # * Create a connection for use
        self.connection = Connection(server_pool, username, password, client_strategy=SAFE_SYNC, auto_bind=True)

    @abstractmethod
    def get_all(self, search_base: str) -> list[ObjectClass]: 

        """
            This function will get all objects from the given search base

        Args:
            search_base (str): The AD search base that will be looked up from

        Returns:
            list[ObjectClass]: The AD list of objects obtained
        """        
        pass

    @abstractmethod
    def deep_single_search(self, search_base: str, unique_identifier: str) -> ObjectClass:

        """
            This function will search for single object that matches the unique_identifier criteria.
            If multiple is obtained, it will return the first one obtained.

        Args:
            search_base (str): The AD search base that will be looked up from
            unique_identifier (str): A unique identifier that will be used to identify the object

        Returns:
            ObjectClass: An AD object class
        """        
        pass

    @abstractmethod
    def move(self, distinguished_name: str, cn:str, new_ou: dict) -> None: 

        """
            This function will move one AD object from an OU to another

        Args:
            distinguished_name (str): The dn of the AD object
            cn (str): The cn of the AD object
            new_ou (dict): The OU where to move the AD object
        """        
        pass

    @abstractmethod
    def delete(self, distinguished_name: str) -> None: 

        """
            This function will delete an AD object

        Args:
            distinguished_name (str): The dn of the AD object
        """        
        pass

    