# First time configuration
Launch any command for the first time.


This will create a default configuration file in ~/.vecb/config.ini

You should replace the endpoint with the one of your server
~~~
[API]
endpoint = https://<ENDPOINT>/api/v1
token = 
~~~


# Login
~~~
$ vecb login --username <USERNAME>
~~~

It will ask for a password, authenticate you with the online API and write a token in config.ini

From this moment on you can launch any command without the need of authenticate again.


# Logout
~~~
$ vecb logout
~~~

This will remove the token from config.ini. You will need to re-authenticate to use the API.

# Who am I
~~~
$ vecb whoami
~~~

It will print the information of the current logged in user


# Search
~~~
$ vecb search <SEQUENCE HERE .... GATGGCGGG ....>
~~~
