# Configuration

Store in yaml:

- Mapping between machine name and "helpful human-readable locations"
- per study:
  - Where files originate
  - Where files go
  - Anyone extra to be notified on success
  - Anyone extra be notified on failure

# Helping studies out

This is likely to generate a mess sometimes if things have to be re-copied. Do 
we want to consider making the filenames rotate in reverse, so new files keep 
their names and old ones are renamed? Probably not, because then old files are 
no longer immutable.

But maybe we can give them an example command to list the "latest" of each 
file somehow? This depends on the renaming convention, which depends on rsync 
I guess...



# Mail notification

Should be easy

    echo "Dan is testing" | mail -r "fake@fake.com" -s "Does this work right to account name?" "fitch"


# Secure copying from windows

WAIT: What if we teach the users to run this process AS THEMSELVES by `shift right click -> run as different user`? Is that nasty?

The client copier is odd, because it will be running (at least from what I've seen so far) as the local `biopac` user, NOT as the user who collected the data. So it needs to prompt the user for username and password, right? I can't get the python paramiko SSH lib to install easily on windows, so I'm futzing with other options for the upload part now. Worst case, we use pscp.exe from PuTTY or we require cygwin and do some kind of ugly shelling out that prompts the user. Since we're going to be running multiple commands, I really want to have auth taken care of in the python side so the user doesn't have to re-authenticate for each step... urgh.

Options for SSH access from python:

https://github.com/jbardin/scp.py

http://www.paramiko.org/

When I try to `pip install paramiko` on windows, I get:

    Collecting pycrypto!=2.4,>=2.1 (from paramiko)
      Downloading pycrypto-2.6.1.tar.gz (446kB)
        100% |################################| 446kB 493kB/s
        Traceback (most recent call last):
          File "<string>", line 20, in <module>
          File "c:\users\fitch\appdata\local\temp\pip-build-mkasml\pycrypto\setup.py", line 43, in <module>
            from distutils.command.build_ext import build_ext
          File "C:\dantemp\dev\PsychoPy2\lib\distutils\command\build_ext.py", line 23, in <module>
            from distutils.msvccompiler import get_build_version
        ImportError: No module named msvccompiler
        Complete output from command python setup.py egg_info:
        Traceback (most recent call last):

          File "<string>", line 20, in <module>

          File "c:\users\fitch\appdata\local\temp\pip-build-mkasml\pycrypto\setup.py", line 43, in <module>

            from distutils.command.build_ext import build_ext

          File "C:\dantemp\dev\PsychoPy2\lib\distutils\command\build_ext.py", line 23, in <module>

            from distutils.msvccompiler import get_build_version

        ImportError: No module named msvccompiler

        ----------------------------------------
        Command "python setup.py egg_info" failed with error code 1 in c:\users\fitch\appdata\local\temp\pip-build-mkasml\py
    crypto



http://blog.victorjabur.com/2011/06/05/compiling-python-2-7-modules-on-windows-32-and-64-using-msvc-2008-express/

