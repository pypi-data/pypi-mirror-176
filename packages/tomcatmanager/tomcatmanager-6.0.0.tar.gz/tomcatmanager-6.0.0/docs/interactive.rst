Interactive Use
===============

After installation, you will have a new tool called ``tomcat-manager``. Run
this with no command line arguments to invoke an interactive, line-oriented
command interpreter:

.. code-block:: text

   $ tomcat-manager
   tomcat-manager> connect http://localhost:8080/manager admin newenglandclamchowder
   --connected to http://localhost:8080/manager as ace
   tomcat-manager> list
   Path                     Status  Sessions Directory
   ------------------------ ------- -------- ------------------------------------
   /                        running        0 ROOT
   /manager                 running       14 /usr/share/tomcat7-admin/manager
   /host-manager            running        0 /usr/share/tomcat7-admin/host-manager
   tomcat-manager> exit

Use the ``exit`` or ``quit`` command to exit the interpreter and return to your
operating system shell.


Available Commands
------------------

The interactive shell has a built-in list of all available commands:

.. code-block:: text

   tomcat-manager> help
   tomcat-manager is a command line tool for managing a Tomcat server

   Connecting to a Tomcat server
   ============================================================
   connect   Connect to a tomcat manager instance.
   which     Show the url of the tomcat server you are connected to.

   Managing applications
   ============================================================
   list      Show all installed applications.
   deploy    Deploy an application to the tomcat server.
   redeploy  Redeploy an application to the tomcat server.
   undeploy  Remove an application from the tomcat server.
   start     Start a deployed tomcat application that isn't running.
   stop      Stop a tomcat application and leave it deployed on the server.
   restart   Start and stop a tomcat application.
     reload  Synonym for 'restart'.
   sessions  Show active sessions for a tomcat application.
   expire    Expire idle sessions.

   Server information
   ============================================================
   findleakers          Show tomcat applications that leak memory.
   resources            Show global JNDI resources configured in Tomcat.
   serverinfo           Show information about the tomcat server.
   status               Show server status information in xml format.
   threaddump           Show a jvm thread dump.
   vminfo               Show diagnostic information about the jvm.

   TLS configuration
   ============================================================
   sslconnectorciphers       Show SSL/TLS ciphers configured for each connector.
   sslconnectorcerts         Show SSL/TLS certificate chain for each connector.
   sslconnectortrustedcerts  Show SSL/TLS trusted certificates for each connector.
   sslreload                 Reload SSL/TLS certificates and keys.

   Settings, configuration, and tools
   ============================================================
   config       Edit or show the location of the user configuration file.
   edit         Edit a file in the preferred text editor.
   exit_code    Show a number indicating the status of the previous command.
   history      View, run, edit, and save previously entered commands.
   py           Execute python commands.
   run_pyscript Run a file containing a python script.
   set          Change program settings.
   show         Show all settings or a specific setting.
     settings   Synonym for 'show'.
   shell        Execute a command in the operating system shell.
   shortcuts    Show shortcuts for other commands.

   Other
   ============================================================
   exit     Exit this program.
     quit   Synonym for 'exit'.
   help     Show available commands, or help on a specific command.
   version  Show the version number of this program.
   license  Show the software license for this program.


As well as help for each command:

.. code-block:: text

   tomcat-manager> help stop
   usage: stop [-h] [-v VERSION] path

   Stop a running tomcat application and leave it deployed on the server.

   positional arguments:
     path                  The path part of the URL where the application is
                           deployed.

   optional arguments:
     -h, --help            show this help message and exit
     -v VERSION, --version VERSION
                           Optional version string of the application to stop. If
                           the application was deployed with a version string, it
                           must be specified in order to stop the application.

This document does not include detailed explanations of every command. It does
show how to connect to a Tomcat server and deploy a war file, since there are
quite a few options for both of those commands. For everything else, the
built-in help should be sufficient.


Connect To A Tomcat Server
--------------------------

Before you can do anything to a Tomcat server, you need to enter the connection
information, including the url and the authentication credentials. You can pass
the connection information on the command line:

.. code-block:: text

   $ tomcat-manager --user=ace http://localhost:8080/manager
   Password: {you type your password here}

Or:

.. code-block:: text

   $ tomcat-manager --user=ace --password=newenglandclamchowder \
   http://localhost:8080/manager

You can also enter this information into the interactive prompt:

.. code-block:: text

   $ tomcat-manager
   tomcat-manager> connect http://localhost:8080/manager ace newenglandclamchowder

Or:

.. code-block:: text

   $ tomcat-manager
   tomcat-manager> connect http://localhost:8080/manager ace
   Password: {type your password here}

See :doc:`authentication` for complete details on all supported authentication
mechanisms.


Deploy applications
-------------------

Tomcat applications are usually packaged as a WAR file, which is really just a
zip file with a different extension. The ``deploy`` command sends a WAR file to
the Tomcat server and tells it which URL to deploy that application at.

The WAR file can be located in one of two places: some path on the computer
that is running Tomcat, or some path on the computer where the command line
``tomcat-manager`` program is running.

If the WAR file is located on the same server as Tomcat, we call that
``server``. If the WAR file is located where ``tomcat-manager`` is running, we
call that ``local``. If the file is already on the server, then we have to tell
Tomcat where to go find it. If it's ``local``, then we have to send the WAR
file over the network so Tomcat can deploy it.

For all of these examples, lets assume I have a Tomcat server running far away
in a data center somewhere, accessible at ``https://www.example.com``. I'm
running the command line ``tomcat-manager`` program on my laptop. We'll also
assume that we have already connected to the Tomcat server, using one of the
methods just described in :ref:`interactive:Connect To A Tomcat Server`.

For our first example, let's assume we have a WAR file already on our server,
in ``/tmp/fancyapp.war``. To deploy this WAR file to
``https://www.example.com/fancy``:

.. code-block:: text

   tomcat-manager> deploy server /tmp/myfancyapp.war /fancy

Now let's say I just compiled a WAR file on my laptop for an app called
``shiny``. It's saved at ``~/src/shiny/dist/shinyv2.0.5.war``. I'd like to
deploy it to ``https://www.example.com/shiny``:

.. code-block:: text

   tomcat-manager> deploy local ~/src/shiny/dist/shiny2.0.5.war /shiny


Sometimes when you deploy a WAR you want to specify additional configuration
information. You can do so by using a `context file
<https://tomcat.apache.org/tomcat-8.5-doc/config/context.html>`_. The context
file must reside on the same server where Tomcat is running.

.. code-block:: text

  tomcat-manager> deploy context /tmp/context.xml /sample

This command will deploy the WAR file specified in the ``docBase`` attribute of
the ``Context`` element so it's available at
``https://www.example.com/sample``.

.. note::

  When deploying via context files, be aware of the following:

  - The ``path`` attribute of the ``Context`` element is ignored by the Tomcat
    Server when deploying from a context file.

  - If the ``Context`` element specifies a ``docBase`` attribute, it will be
    used even if you specify a war file on the command line.


Parallel Deployment
-------------------

Tomcat supports a `parallel deployment feature
<https://tomcat.apache.org/tomcat-10.1-doc/config/context.html#Parallel_deplo
yment>`_ which allows multiple versions of the same WAR to be deployed
simultaneously at the same URL. To utilize this feature, you need to deploy
an application with a version string. The combination of path and version
string uniquely identify the application.

Let's revisit our ``shiny`` app. This time we will deploy with a version
string:

.. code-block:: text

  tomcat-manager>deploy local ~/src/shiny/dist/shiny2.0.5.war /shiny -v v2.0.5
  tomcat-manager>list
  Path                     Status  Sessions Directory
  ------------------------ ------- -------- ------------------------------------
  /                        running        0 ROOT
  /manager                 running        0 manager
  /shiny                   running        0 shiny##v2.0.5

Later today, I make a bug fix to 'shiny', and build version 2.0.6 of the app.
Parallel deployment allows me to deploy two versions of that app at the same
path, and Tomcat will migrate users to the new version over time as their
sessions expire in version 2.0.5.

.. code-block:: text

  tomcat-manager>deploy local ~/src/shiny/dist/shiny2.0.6.war /shiny -v v2.0.6
  tomcat-manager>list
  Path                     Status  Sessions Directory
  ------------------------ ------- -------- ------------------------------------
  /                        running        0 ROOT
  /manager                 running        0 manager
  /shiny                   running       12 shiny##v2.0.5
  /shiny                   running        0 shiny##v2.0.6

Once all the sessions have been migrated to version 2.0.6, I can undeploy
version 2.0.5:

.. code-block:: text

  tomcat-manager>undeploy /shiny --version v2.0.5
  tomcat-manager>list
  Path                     Status  Sessions Directory
  ------------------------ ------- -------- ------------------------------------
  /                        running        0 ROOT
  /manager                 running        0 manager
  /shiny.                  running        9 shiny##v2.0.6

The following commands support the ``-v`` or ``--version`` option, which makes
parallel deployment possible:

- deploy
- undeploy
- start
- stop
- reload
- sessions
- expire


Readline Editing
----------------

You can edit current or previous commands using standard ``readline`` editing
keys. If you aren't familiar with ``readline``, just know that you can use your
arrow keys, ``home`` to move to the beginning of the line, ``end`` to move to
the end of the line, and ``delete`` to forward delete characters.


Command History
---------------

Interactive mode keeps a command history, which you can navigate using the up
and down arrow keys. and search the history of your commands with
``<control>+r``.

You can view the list of previously issued commands:

.. code-block:: text

  tomcat-manager> history

And run a previous command by string search:

.. code-block:: text

  tomcat-manager> history -r undeploy

Or by number:

.. code-block:: text

  tomcat-manager> history -r 10

The ``history`` command has many other options, including the ability to save
commands to a file and load commands from a file. Use ``help history`` to get
the details.


Settings
--------

The ``show`` or ``settings`` (they do exactly the same thing) commands display
a list of settings which control the behavior of ``tomcat-manager``:

.. code-block:: text

  tomcat-manager> show
  autorun_on_edit=False       # Automatically run files after editing
  colors=True                 # Colorized output (*nix only)
  debug=False                 # Show stack trace for exceptions
  echo=False                  # For piped input, echo command to output
  editor=/usr/local/bin/zile  # Program used to edit files
  locals_in_py=True           # Allow access to your application in py via self
  prompt='tomcat-manager> '   # The prompt issued to solicit input
  quiet=False                 # Don't print nonessential feedback
  status_prefix=--            # String to prepend to all status output
  status_to_stdout=False      # Status information to stdout instead of stderr
  timeout=10                  # Seconds to wait for HTTP connections
  timing=False                # Report execution times

You can change any of these settings using the ``set`` command:

.. code-block:: text

  tomcat-manager> set prompt='tm> '
  tm>

Quotes around values are not required unless they contain spaces or other
quotes.


Configuration File
------------------

``tomcat-manager`` reads a user configuration file on startup. This file allows
you to:

- change settings on startup
- define shortcuts for connecting to Tomcat servers

The location of the configuration file is different depending on your operating
system. To see the location of the file:

.. code-block:: text

  tomcat-manager> config file
  /Users/kotfu/Library/Application Support/tomcat-manager/tomcat-manager.toml

You can edit the file from within ``tomcat-manager`` too. Well, it really just
launches the editor of your choice, you know, the one specified in the
``editor`` setting. Do that by typing:

.. code-block:: text

  tomcat-manager> config edit

This file uses the `TOML <https://toml.io/>`_ file format. Create a table called
``settings``, and use key/value pairs to set values for any of the available settings.
These settings are applied when the application first runs, and applied again after
you finish editing the config file. Here's an example of settings in the config file:

.. code-block:: toml

  [settings]
  prompt = "tm> "
  debug = true
  editor = "/usr/local/bin/zile"
  echo = false
  quiet = false
  status_prefix = "--"

.. note::

  In versions prior to 6.0.0, the configuration file used a Microsoft Windows INI file
  format, which is similar to TOML. The biggest difference apparent in our
  configuration file is that all string values must be quoted in TOML, and in INI they
  are accepted without quotes.

  When you run ``tomcat-manager`` in interactive mode it will check if the old
  configuration file is present. If it is, and if the new configuration file doesn't
  exist, it will let you know. Here's how to convert your old configuration file to
  the new format:

  .. code-block:: text

    tomcat-manager> config convert

  Everything should be converted over automatically except any comments you have in
  your file. You'll have to add those back by hand.


Server Shortcuts
----------------

In addition to settings, you can use the configuration file to define shortcuts to
various Tomcat servers. Using server shortcuts you can keep the authentication
credentials off of the command line and out of your scripts, which is more secure.
Create a table named the shortcut, and then include keys and values for ``url``,
``user``, and ``password``. Here's a simple example:

.. code-block:: toml

  [tcl]
  url = "http://localhost:8080/manager"
  user = "ace"
  password = "newenglandclamchowder"

With this defined in your configuration file, you can now connect using the
name of the shortcut:

.. code-block:: text

  tomcat-manager> connect tcl

You can also use the name of the shortcut from the command line:

.. code-block:: text

  $ tomcat-manager tcl

If you define a ``user``, but omit ``password``, you will be prompted for it
when you use the shortcut in the ``connect`` command.

Here's all the properties supported in a server shortcut:

url
  Url of the server.

user
  User to use for HTTP Basic authentication.

password
  Password to use for HTTP Basic authentication. If user is provided
  and password is not, you will be prompted for a password.

cert
  File containing certificate and key, or just a certificate, for SSL/TLS client
  authentication. See :ref:`authentication:SSL/TLS Client Authentication` for more
  information.

key
  File containing private key for SSL/TLS client authentication. See
  :ref:`authentication:SSL/TLS Client Authentication` for more information.

cacert
  File or directory containing a certificate authority bundle used to validate the
  SSL/TLS certificate presented by the server if the url uses the https protocol. See
  :ref:`authentication:Encrypted Connections` for more information.

verify
  Defaults to ``True`` to verify server SSL/TLS certificates. If ``False``,
  no verification is performed.

When using a server shortcut, you can override properties from the shortcut
on the command line. For example, if we had a server shortcut like this:

.. code-block:: toml

  [prod]
  url = "https://www.example.com/manager"
  user = "ace"
  password = "newenglandclamchowder"
  cacert = "/etc/mycacert"

You could use that server shortcut but temporarily disable verification of server
SSL/TLS certificates:

.. code-block:: text

  tomcat-manager> connect prod --noverify

Or you could override the user and password:

.. code-block:: text

  tomcat-manager> connect prod root Z1ON0101


Some of these properties make no sense when combined together. For example, if your
server authenticates with a certificate and key, it almost certainly doesn't use a
user and password. If you don't want to verify server SSL/TLS certificates, then it
makes no sense to provide a certificate authority bundle. See
:doc:`authentication` for complete details of all supported authentication
mechanisms.


Shell-style Output Redirection
------------------------------

Save the output of the ``list`` command to a file:

.. code-block:: text

  tomcat-manager> list > /tmp/tomcat-apps.txt

Search the output of the ``vminfo`` command:

.. code-block:: text

  tomcat-manager> vminfo | grep user.timezone
    user.timezone: US/Mountain

Or the particularly useful:

.. code-block:: text

  tomcat-manager> threaddump | less


Clipboard Integration
---------------------

You can copy output to the clipboard by redirecting but not giving a filename:

.. code-block:: text

  tomcat-manager> list >

You can also append output to the clipboard using a similar method:

.. code-block:: text

  tomcat-manager> serverinfo >>


Run shell commands
------------------

Use the ``shell`` or ``!`` commands to execute operating system commands (how
meta):

.. code-block:: text

  tomcat-manager> !ls

Of course tab completion works on shell commands.


Python Interpreter
------------------------------------

You can launch a python interpreter:

.. code-block:: text

  tomcat-manager> py
  Python 3.10.0 (default, Oct  7 2021, 15:03:23) [Clang 11.0.3 (clang-1103.0.32.62)] on darwin
  Type "help", "copyright", "credits" or "license" for more information.

  Use `Ctrl-D` (Unix) / `Ctrl-Z` (Windows), `quit()`, `exit()` to exit.
  Run CLI commands with: app("command ...")

  >>> self.tomcat
  <tomcatmanager.tomcat_manager.TomcatManager object at 0x10f652a40>
  >>> self.tomcat.is_connected
  True
  >>> exit()
  Now exiting Python shell...

As you can see, if you have connected to a Tomcat server, then you will have a
``self.tomcat`` object available which is an instance of :class:`.TomcatManager`.
See :doc:`package` for more information about what you can do with this object.
