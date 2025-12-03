


Installation
------------

::

   git clone https://github.com/erykglowacki1/vulpy.git

   cd vulpy
   
   activate venv

   pip3 install  -r requirements.txt
   
   ./vulpy.py


Features
--------

- Login/Logout
- Read posts from other users
- Publish posts
- Multi-Factor Authentication (MFA)
- API for read and write posts
- Content Security Policy
- SSL/TLS Server



Database Initialization
-----------------------

Both, "BAD" and "GOOD" versions, requires an initialization of the database.

This is done with the script "db_init.py" inside each of the directories (bad, and good).

Each version has their own sqlite files for the users and posts.

The execution of the script is, for example:

::

   cd bad
   ./db_init.py


Default Credentials
-------------------

After database initialization, three users are created:

::

   Username    Password
   --------    -----------
   admin       SuperSecret
   elliot      123123123
   tim         12345678


You can login with any user, the application doesn't have a permissions system, so, the three have the same permissions.


