from datetime import datetime
from ldap3 import ALL_ATTRIBUTES, MODIFY_REPLACE
from ad_leavers.models.core.ad_ops import AdOperations
from ad_leavers.models.core.exceptions import AdSearchException, AdModifyException
from ad_leavers.models.core.object_class import ObjectClass
from ad_leavers.models.data_classes.user import User

# > This is the UserOps class that will work with the User dataclass
# > It inherits the AdOperations base class for operations
class UserOps(AdOperations):
    
    # FIXME(Make sure to call escape_filter_chars() from ldap3.utils.conv on any user input before placing it into a .search() call. This is to avoid possible injection of malicious code. Look at https://www.linkedin.com/pulse/ldap-injection-django-jerin-jose for more information.)

    def __init__(self, hosts, username, password) -> None: 

        """
            This class will model a User/Person in an AD
            It inherits the AdOperations abstract class
            Authentication is done in constructor
            It users the filter (|(objectclass=user)(objectclass=person)) from ldap3

        Args:
            hosts (list[str]): This is a list of AD hosts that will be added to the Server Pool
            username (str): This is the username that ldap3 will assume to connect to the AD sosts
            password (str): This is the password for the account
        """        
        
        # * Set the object type
        self.object_class_type = '(|(objectclass=user)(objectclass=person))'

        # * Initialize the parent class
        super().__init__(hosts, username, password)
    
    # > Inherited methods from Parent abstract class
    def get_all(self, search_base: str) -> list[User]: 

        """
            This function will get all User/Person from the given search base

        Args:
            search_base (str): The AD search base that will be looked up from

        Raises:
            AdSearchException: If the search is not successful, this exception will be raised

        Returns:
            list[User]: The AD list of users obtained
        """      
        
        # * Make API call
        status, result, response, _ = self.connection.search(
            search_base=search_base,
            search_filter=self.object_class_type,
            attributes=ALL_ATTRIBUTES
        )

        if not status: raise AdSearchException(f"Error while searching the searchbase {search_base}: {result['message']}")

        # * Return the schema in the ObjectClass model format
        return [User(schema=schema) for schema in response]

    def deep_single_search(self, search_base: str, unique_identifier: str) -> User: 

        """
            This function will search for a single User that matches the unique_identifier criteria.
            If multiple is obtained, it will return the first one obtained.

        Args:
            search_base (str): The AD search base that will be looked up from
            unique_identifier (str): A unique identifier that will be used to identify the user

        Returns:
            User: returns a User object
        """        

        # * Construct filter that will perform the deep search
        search_filter = f"""
        (|(mail={unique_identifier})
        (sAMAccountName={unique_identifier.split('@')[0] if '@' in unique_identifier else unique_identifier})
        (cn={unique_identifier.replace('.', ' ')}))
        """

        # * Make API call
        _, _, response, _ = self.connection.search(
            search_base=search_base,
            search_filter=search_filter,
            attributes=ALL_ATTRIBUTES
        )

        # * Get the users obtained
        users = [User(schema=schema) for schema in response]

        # * Return the user if it's found
        return users[0] if len(users) != 0 else None 
    
    def delete(self, distinguished_name: str) -> None: 

        """
            This function will delete a User from AD

        Args:
            distinguished_name (str): The dn of the User

        Raises:
            AdModifyException: If an error occurs while deleting the User, it will raise this exception
        """        
        
        # * Delete the dn
        status, result, _, _  = self.connection.delete(distinguished_name)

        if not status: raise AdModifyException(f"Error while deleting {distinguished_name}: {result['message']}")

    def move(self, distinguished_name: str, cn:str, new_ou: dict) -> None: 

        """
            This function will move one User from an OU to another

        Args:
            distinguished_name (str): The dn of the User
            cn (str): The cn of the User
            new_ou (dict): The OU where to move the User

        Raises:
            AdModifyException: If an error occurs while moving the User, it will raise this exception
        """        
        
        # * Modify the DN
        status, result, _, _  = self.connection.modify_dn(distinguished_name, f'cn={cn}', new_superior=new_ou)

        if not status: raise AdModifyException(f"Error while moving {distinguished_name}: {result['message']}")

    # > Unique class methods
    def set_expiration(self, distinguished_name: str, expiration_date: datetime):

        """
            This function will set an expiration on the User's account in AD

        Args:
            distinguished_name (str): The dn of the user account
            expiration_date (datetime): The datetime to expire the account

        Raises:
            AdModifyException: If an error occurs while setting an expiration on the account, it will raise this exception
        """        
        
        # * Set the expiration date
        status, result, _, _ = self.connection.modify(
            distinguished_name,
            {
                'accountExpires': [(MODIFY_REPLACE, [expiration_date])]
            }
        ) 

        if not status: raise AdModifyException(f"Error while setting an expiration date on {distinguished_name}: {result['message']}")

    def disable(self, distinguished_name: str):
        """
            This function will disable a User account in AD

        Args:
            distinguished_name (str): The dn of the user account

        Raises:
            AdModifyException: If an error occurs while disabling the User, it will raise this exception
        """        
        
        # * Disable the account
        status, result, _, _ = self.connection.modify(
            distinguished_name,
            {
                'userAccountControl': [(MODIFY_REPLACE, [514])]
            }
        ) 

        if not status: raise AdModifyException(f"Error while disabling account on {distinguished_name}: {result['message']}")