# ldap3-ad-leavers

This is an extension to the orginal project [ldap3](https://pypi.org/project/ldap3/) python library.

This library provides facilities to access the ldap3 library and functions that will be helpful when offboarding users from an AD.

## Getting Started

Assuming that you have Python and virtualenv installed, set up your environment and install the required dependencies using pip:

```
pip install ldap3-ad-leavers
```

## Using the module

After installing the module, you need to import the main class operations object and instantiate it to create a connection to AWS:

Currently, the followign class operations available are:

- UserOps: To manipulate user objects in AD

## Classes and methods

* [user\_operations](#user_operations)

* [UserOps](#user_operations.UserOps)
  * [\_\_init\_\_](#user_operations.UserOps.__init__)
  * [get\_all](#user_operations.UserOps.get_all)
  * [deep\_single\_search](#user_operations.UserOps.deep_single_search)
  * [delete](#user_operations.UserOps.delete)
  * [move](#user_operations.UserOps.move)
  * [set\_expiration](#user_operations.UserOps.set_expiration)
  * [disable](#user_operations.UserOps.disable)
* [models](#models)
* [models.core.object\_class](#models.core.object_class)
  * [ObjectClass](#models.core.object_class.ObjectClass)
    * [\_\_init\_\_](#models.core.object_class.ObjectClass.__init__)
* [models.core](#models.core)
* [models.core.ad\_ops](#models.core.ad_ops)
  * [AdOperations](#models.core.ad_ops.AdOperations)
    * [\_\_init\_\_](#models.core.ad_ops.AdOperations.__init__)
    * [get\_all](#models.core.ad_ops.AdOperations.get_all)
    * [deep\_single\_search](#models.core.ad_ops.AdOperations.deep_single_search)
    * [move](#models.core.ad_ops.AdOperations.move)
    * [delete](#models.core.ad_ops.AdOperations.delete)
* [models.core.exceptions](#models.core.exceptions)
  * [AdSearchException](#models.core.exceptions.AdSearchException)
  * [AdModifyException](#models.core.exceptions.AdModifyException)
* [models.data\_classes.user](#models.data_classes.user)
  * [User](#models.data_classes.user.User)
    * [\_\_init\_\_](#models.data_classes.user.User.__init__)
    * [is\_eligible\_to\_disable](#models.data_classes.user.User.is_eligible_to_disable)
    * [is\_eligible\_for\_deletion](#models.data_classes.user.User.is_eligible_for_deletion)
* [models.data\_classes](#models.data_classes)

`<a id="__init__"></a>`

# \_\_init\_\_

`<a id="user_operations"></a>`

# user\_operations

`<a id="user_operations.UserOps"></a>`

## UserOps Objects

```python
class UserOps(AdOperations)
```

`<a id="user_operations.UserOps.__init__"></a>`

#### \_\_init\_\_

```python
def __init__(hosts, username, password) -> None
```

This class will model a User/Person in an AD
It inherits the AdOperations abstract class
Authentication is done in constructor
It users the filter (|(objectclass=user)(objectclass=person)) from ldap3

**Arguments**:

- `hosts` _list[str]_ - This is a list of AD hosts that will be added to the Server Pool
- `username` _str_ - This is the username that ldap3 will assume to connect to the AD sosts
- `password` _str_ - This is the password for the account

`<a id="user_operations.UserOps.get_all"></a>`

#### get\_all

```python
def get_all(search_base: str) -> list[User]
```

This function will get all User/Person from the given search base

**Arguments**:

- `search_base` _str_ - The AD search base that will be looked up from

**Raises**:

- `AdSearchException` - If the search is not successful, this exception will be raised

**Returns**:

- `list[User]` - The AD list of users obtained

`<a id="user_operations.UserOps.deep_single_search"></a>`

#### deep\_single\_search

```python
def deep_single_search(search_base: str, unique_identifier: str) -> User
```

This function will search for a single User that matches the unique_identifier criteria.
If multiple is obtained, it will return the first one obtained.

**Arguments**:

- `search_base` _str_ - The AD search base that will be looked up from
- `unique_identifier` _str_ - A unique identifier that will be used to identify the user

**Returns**:

- `User` - returns a User object

`<a id="user_operations.UserOps.delete"></a>`

#### delete

```python
def delete(distinguished_name: str) -> None
```

This function will delete a User from AD

**Arguments**:

- `distinguished_name` _str_ - The dn of the User

**Raises**:

- `AdModifyException` - If an error occurs while deleting the User, it will raise this exception

`<a id="user_operations.UserOps.move"></a>`

#### move

```python
def move(distinguished_name: str, cn: str, new_ou: dict) -> None
```

This function will move one User from an OU to another

**Arguments**:

- `distinguished_name` _str_ - The dn of the User
- `cn` _str_ - The cn of the User
- `new_ou` _dict_ - The OU where to move the User

**Raises**:

- `AdModifyException` - If an error occurs while moving the User, it will raise this exception

`<a id="user_operations.UserOps.set_expiration"></a>`

#### set\_expiration

```python
def set_expiration(distinguished_name: str, expiration_date: datetime)
```

This function will set an expiration on the User's account in AD

**Arguments**:

- `distinguished_name` _str_ - The dn of the user account
- `expiration_date` _datetime_ - The datetime to expire the account

**Raises**:

- `AdModifyException` - If an error occurs while setting an expiration on the account, it will raise this exception

`<a id="user_operations.UserOps.disable"></a>`

#### disable

```python
def disable(distinguished_name: str)
```

This function will disable a User account in AD

**Arguments**:

- `distinguished_name` _str_ - The dn of the user account

**Raises**:

- `AdModifyException` - If an error occurs while disabling the User, it will raise this exception

`<a id="models"></a>`

# models

`<a id="models.core.object_class"></a>`

# models.core.object\_class

`<a id="models.core.object_class.ObjectClass"></a>`

## ObjectClass Objects

```python
class ObjectClass()
```

`<a id="models.core.object_class.ObjectClass.__init__"></a>`

#### \_\_init\_\_

```python
def __init__(name: str, distinguished_name: str, when_created: datetime)
```

This is the ObjectClass model
This is the Parent class for all AD objects

**Arguments**:

- `name` _str_ - The name of the AD object
- `distinguished_name` _str_ - The dn of the AD object
- `when_created` _datetime_ - The datetime when the AD object was created

`<a id="models.core"></a>`

# models.core

`<a id="models.core.ad_ops"></a>`

# models.core.ad\_ops

`<a id="models.core.ad_ops.AdOperations"></a>`

## AdOperations Objects

```python
class AdOperations(ABC)
```

`<a id="models.core.ad_ops.AdOperations.__init__"></a>`

#### \_\_init\_\_

```python
def __init__(hosts, username: str, password: str) -> None
```

This is an abstract class that will model all AD objects of this project
All AD object class operations will inherit from this class
Authentication is done in constructor

**Arguments**:

- `hosts` _list[str]_ - This is a list of AD hosts that will be added to the Server Pool
- `username` _str_ - This is the username that ldap3 will assume to connect to the AD sosts
- `password` _str_ - This is the password for the account

`<a id="models.core.ad_ops.AdOperations.get_all"></a>`

#### get\_all

```python
@abstractmethod
def get_all(search_base: str) -> list[ObjectClass]
```

This function will get all objects from the given search base

**Arguments**:

- `search_base` _str_ - The AD search base that will be looked up from

**Returns**:

- `list[ObjectClass]` - The AD list of objects obtained

`<a id="models.core.ad_ops.AdOperations.deep_single_search"></a>`

#### deep\_single\_search

```python
@abstractmethod
def deep_single_search(search_base: str,
                       unique_identifier: str) -> ObjectClass
```

This function will search for single object that matches the unique_identifier criteria.
If multiple is obtained, it will return the first one obtained.

**Arguments**:

- `search_base` _str_ - The AD search base that will be looked up from
- `unique_identifier` _str_ - A unique identifier that will be used to identify the object

**Returns**:

- `ObjectClass` - An AD object class

`<a id="models.core.ad_ops.AdOperations.move"></a>`

#### move

```python
@abstractmethod
def move(distinguished_name: str, cn: str, new_ou: dict) -> None
```

This function will move one AD object from an OU to another

**Arguments**:

- `distinguished_name` _str_ - The dn of the AD object
- `cn` _str_ - The cn of the AD object
- `new_ou` _dict_ - The OU where to move the AD object

`<a id="models.core.ad_ops.AdOperations.delete"></a>`

#### delete

```python
@abstractmethod
def delete(distinguished_name: str) -> None
```

This function will delete an AD object

**Arguments**:

- `distinguished_name` _str_ - The dn of the AD object

`<a id="models.core.exceptions"></a>`

# models.core.exceptions

`<a id="models.core.exceptions.AdSearchException"></a>`

## AdSearchException Objects

```python
class AdSearchException(Exception)
```

Will raise all exceptions that are related to an AD search operation

**Arguments**:

- `Exception` _Exception_ - Inherits the Exception class

`<a id="models.core.exceptions.AdModifyException"></a>`

## AdModifyException Objects

```python
class AdModifyException(Exception)
```

Will raise all exceptions that are related to an AD Modify operation

**Arguments**:

- `Exception` _Exception_ - Inherits the Exception class

`<a id="models.data_classes.user"></a>`

# models.data\_classes.user

`<a id="models.data_classes.user.User"></a>`

## User Objects

```python
@dataclass
class User(ObjectClass)
```

`<a id="models.data_classes.user.User.__init__"></a>`

#### \_\_init\_\_

```python
def __init__(schema: dict)
```

This is the User data class model
It inherits from the ObjectClass model
This class will model a user object in an AD

**Arguments**:

- `schema` _dict_ - The schema of an AD object that represent a User/Person from ldap3

`<a id="models.data_classes.user.User.is_eligible_to_disable"></a>`

#### is\_eligible\_to\_disable

```python
def is_eligible_to_disable()
```

This function will verify if the user is eligible to have its account disabled
Eligibility will be calculated whether the account has already expired or not

**Returns**:

- `bool` - Returns True or False

`<a id="models.data_classes.user.User.is_eligible_for_deletion"></a>`

#### is\_eligible\_for\_deletion

```python
def is_eligible_for_deletion(days_limit: int)
```

This function will verify if the user is eligible to have its account deleted
Eligibility will be calculated whether the days_limit argument has already exceeded the
date that the account has been expired

**Arguments**:

- `days_limit` _int_ - The days after which an account is considered eligible to be deleted after it has been expired

**Returns**:

- `bool` - Returns True or False

`<a id="models.data_classes"></a>`

# models.data\_classe

* [\_\_init\_\_](#__init__)
* [user\_operations](#user_operations)
  * [UserOps](#user_operations.UserOps)
    * [\_\_init\_\_](#user_operations.UserOps.__init__)
    * [get\_all](#user_operations.UserOps.get_all)
* [models](#models)
* [models.core.object\_class](#models.core.object_class)
  * [ObjectClass](#models.core.object_class.ObjectClass)
    * [\_\_init\_\_](#models.core.object_class.ObjectClass.__init__)
* [models.core](#models.core)
* [models.core.ad\_ops](#models.core.ad_ops)
  * [AdOperations](#models.core.ad_ops.AdOperations)
    * [\_\_init\_\_](#models.core.ad_ops.AdOperations.__init__)
    * [get\_all](#models.core.ad_ops.AdOperations.get_all)
    * [deep\_single\_search](#models.core.ad_ops.AdOperations.deep_single_search)
    * [move](#models.core.ad_ops.AdOperations.move)
    * [delete](#models.core.ad_ops.AdOperations.delete)
* [models.core.exceptions](#models.core.exceptions)
  * [AdSearchException](#models.core.exceptions.AdSearchException)
  * [AdModifyException](#models.core.exceptions.AdModifyException)
* [models.data\_classes.user](#models.data_classes.user)
  * [User](#models.data_classes.user.User)
    * [\_\_init\_\_](#models.data_classes.user.User.__init__)
    * [is\_eligible\_to\_disable](#models.data_classes.user.User.is_eligible_to_disable)
    * [is\_eligible\_for\_deletion](#models.data_classes.user.User.is_eligible_for_deletion)
* [models.data\_classes](#models.data_classes)

`<a id="__init__"></a>`

# \_\_init\_\_

`<a id="user_operations"></a>`

# user\_operations

`<a id="user_operations.UserOps"></a>`

## UserOps Objects

```python
class UserOps(AdOperations)
```

`<a id="user_operations.UserOps.__init__"></a>`

#### \_\_init\_\_

```python
def __init__(hosts, username, password) -> None
```

This class will model a User/Person in an AD
It inherits the AdOperations abstract class
Authentication is done in constructor

**Arguments**:

- `hosts` _list[str]_ - This is a list of AD hosts that will be added to the Server Pool
- `username` _str_ - This is the username that ldap3 will assume to connect to the AD sosts
- `password` _str_ - This is the password for the account

`<a id="user_operations.UserOps.get_all"></a>`

#### get\_all

```python
def get_all(search_base: str) -> list[User]
```

This function will get all User/Person from the given search base

**Arguments**:

- `search_base` _str_ - The AD search base that will be looked up from

**Raises**:

- `AdSearchException` - If the search is not successful, this exception will be raised

**Returns**:

- `list[User]` - The AD list of users obtained

`<a id="models"></a>`

# models

`<a id="models.core.object_class"></a>`

# models.core.object\_class

`<a id="models.core.object_class.ObjectClass"></a>`

## ObjectClass Objects

```python
class ObjectClass()
```

`<a id="models.core.object_class.ObjectClass.__init__"></a>`

#### \_\_init\_\_

```python
def __init__(name: str, distinguished_name: str, when_created: datetime)
```

This is the ObjectClass model
This is the Parent class for all AD objects

**Arguments**:

- `name` _str_ - The name of the AD object
- `distinguished_name` _str_ - The dn of the AD object
- `when_created` _datetime_ - The datetime when the AD object was created

`<a id="models.core"></a>`

# models.core

`<a id="models.core.ad_ops"></a>`

# models.core.ad\_ops

`<a id="models.core.ad_ops.AdOperations"></a>`

## AdOperations Objects

```python
class AdOperations(ABC)
```

`<a id="models.core.ad_ops.AdOperations.__init__"></a>`

#### \_\_init\_\_

```python
def __init__(hosts, username: str, password: str) -> None
```

This is an abstract class that will model all AD objects of this project
All AD object class operations will inherit from this class
Authentication is done in constructor

**Arguments**:

- `hosts` _list[str]_ - This is a list of AD hosts that will be added to the Server Pool
- `username` _str_ - This is the username that ldap3 will assume to connect to the AD sosts
- `password` _str_ - This is the password for the account

`<a id="models.core.ad_ops.AdOperations.get_all"></a>`

#### get\_all

```python
@abstractmethod
def get_all(search_base: str) -> list[ObjectClass]
```

This function will get all objects from the given search base

**Arguments**:

- `search_base` _str_ - The AD search base that will be looked up from

**Returns**:

- `list[ObjectClass]` - The AD list of objects obtained

`<a id="models.core.ad_ops.AdOperations.deep_single_search"></a>`

#### deep\_single\_search

```python
@abstractmethod
def deep_single_search(search_base: str,
                       unique_identifier: str) -> ObjectClass
```

This function will search for single object that matches the unique_identifier criteria.
If multiple is obtained, it will return the first one obtained.

**Arguments**:

- `search_base` _str_ - The AD search base that will be looked up from
- `unique_identifier` _str_ - A unique identifier that will be used to identify the object

**Returns**:

- `ObjectClass` - An AD object class

`<a id="models.core.ad_ops.AdOperations.move"></a>`

#### move

```python
@abstractmethod
def move(distinguished_name: str, cn: str, new_ou: dict) -> None
```

This function will move one AD object from an OU to another

**Arguments**:

- `distinguished_name` _str_ - The dn of the AD object
- `cn` _str_ - The cn of the AD object
- `new_ou` _dict_ - The OU where to move the AD object

`<a id="models.core.ad_ops.AdOperations.delete"></a>`

#### delete

```python
@abstractmethod
def delete(distinguished_name: str) -> None
```

This function will delete an AD object

**Arguments**:

- `distinguished_name` _str_ - The dn of the AD object

`<a id="models.core.exceptions"></a>`

# models.core.exceptions

`<a id="models.core.exceptions.AdSearchException"></a>`

## AdSearchException Objects

```python
class AdSearchException(Exception)
```

Will raise all exceptions that are related to an AD search operation

**Arguments**:

- `Exception` _Exception_ - Inherits the Exception class

`<a id="models.core.exceptions.AdModifyException"></a>`

## AdModifyException Objects

```python
class AdModifyException(Exception)
```

Will raise all exceptions that are related to an AD Modify operation

**Arguments**:

- `Exception` _Exception_ - Inherits the Exception class

`<a id="models.data_classes.user"></a>`

# models.data\_classes.user

`<a id="models.data_classes.user.User"></a>`

## User Objects

```python
@dataclass
class User(ObjectClass)
```

`<a id="models.data_classes.user.User.__init__"></a>`

#### \_\_init\_\_

```python
def __init__(schema: dict)
```

This is the User data class model
It inherits from the ObjectClass model
This class will model a user object in an AD

**Arguments**:

- `schema` _dict_ - The schema of an AD object that represent a User/Person from ldap3

`<a id="models.data_classes.user.User.is_eligible_to_disable"></a>`

#### is\_eligible\_to\_disable

```python
def is_eligible_to_disable()
```

This function will verify if the user is eligible to have its account disabled
Eligibility will be calculated whether the account has already expired or not

**Returns**:

- `bool` - Returns True or False

`<a id="models.data_classes.user.User.is_eligible_for_deletion"></a>`

#### is\_eligible\_for\_deletion

```python
def is_eligible_for_deletion(days_limit: int)
```

This function will verify if the user is eligible to have its account deleted
Eligibility will be calculated whether the days_limit argument has already exceeded the
date that the account has been expired

**Arguments**:

- `days_limit` _int_ - The days after which an account is considered eligible to be deleted after it has been expired

**Returns**:

- `bool` - Returns True or False

`<a id="models.data_classes"></a>`

## Running Tests

You can run the tests by following the steps below:

1. Clone or download the project to a folder on your computer.
2. Run the tests using the command `./run_test.sh`

## License

```
Copyright Mervin Hemaraju
```
