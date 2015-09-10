# dittohead client

Uses:

- [wxpython](http://www.wxpython.org/) for UI
- [paramiko](https://github.com/paramiko/paramiko) for SSH
- [pyyaml](http://pyyaml.org/) for simple storage
- [py2app](https://pythonhosted.org/py2app/) for OSX packaging
- [py2exe](http://www.py2exe.org/) for Windows packaging

## About

Currently, the client just stores configuration as YAML files in $PWD.

- `config.yaml`: .

  - `host`: The server to connect to
  - `input_directory`: The "inbox" directory that the watcher watches
  - `study_dittohead_raw_folder_name`: Currently we put stuff inside 
    "/study/STUDYNAME/raw-data". Change that here if you like.
  - `presets.path`: Specify where `presets.yaml lives`
  - `last_users.path`: Specify where `presets.yaml lives`

- `presets.yaml`: List of presets.
  
  Each preset has the following data:
  
  - `name`: Preset name
  - `study`: Study abbreviation for the study it uploads to
  - `subdirectory`: The subdirectory underneath raw-data where the files end up -- for example, "eprime" or "biopac". If the 
    subdirectory is blank, no subdirectory will be used.
  - `local_directory`: Local directory: the place on the local machine to upload new files from

  This file could be the same everywhere or customized per machine.
  This file also stores the time a particular preset was last ran.
  (Put here because it's easier than maintaining linkages to a separate list 
  when the preset's name could change...)
  
- `last_users.yaml`: List of recent users per preset.

  Just a quick shortcut to let people pick their name from a list, and 
  autofill the last person when a preset is selected.

### Notes

- We don't currently care that "new" files with old timestamps will get ignored in the current scheme. Clear out the `last_time` value in `presets.yaml` if you care hard enough about this. 

### Testing help

- If you want to set file mtime to "now" on windows, like touch in unix, do this in powershell: `ls | foreach { $_.LastWriteTime = date }`
- On windows, if running via EXE, it dumps a `dittohead.exe.log` in its current directory if there are warnings or errors.
- The client loads and saves presets from `presets.yaml` in the current directory, and 
  will try to create it if it doesn't exist.
- The client loads and saves the last user for each preset in `last_users.yaml` 
  -- less important than `presets.yaml`, and hopefully kind of helpful per-machine 
  for people who have been uploading frequently.


## Packaging

### Windows client

1. `pip install py2exe`
2. In `$DITTOHEAD_ROOT/src/client` run `python win_setup.py py2exe`
3. Your app is in `win_dist`

### OSX client

1. Get it running in a virtualenv first, as outlined below.
2. `pip install py2app`
3. Edit `VIRTUALENV/mac_dittohead/lib/python2.7/site-packages/py2app/recipes/virtualenv.py` 
   and change `load_module` to `_load_module` and `scan_code` to `_scan_code`.
4. In `$DITTOHEAD_ROOT/src/client` run `python osx_setup.py py2app`
5. Your app is in `osx_dist`

## Tips for running on OSX in a virtualenv

This gets real clumsy. Maybe there are better ways.

1. Download virtualenv
2. Inside virtualenv directory, `python virtualenv.py mac_dittohead`
3. `source mac_dittohead/bin/activate`
4. Download paramiko from github and run `easy_install ./` in its directory 
   (or try `pip install paramiko`)
5. `pip install pyyaml`
6. From various tips, now you need to tweak the way it runs:

  - http://wiki.wxpython.org/wxPythonVirtualenvOnMac
  - http://batok.github.io/virtualenvwxp/ 

7. Create a linkage to the base wx install (because the wxPython installer requires admin privileges and can't be installed in a virtualenv:

    ```
    echo "/usr/local/lib/wxPython-unicode-2.8.12.1/lib/python2.7/site-packages/wx-2.8-mac-unicode" >
    /home/fitch/Downloads/virtualenv-12.1.1/mac_dittohead/lib/python2.7/site-packages/wx.pth
    ```

8. Create `mac_dittohead/bin/wxpy`:

    ```bash
    #!/bin/bash

    # what real Python executable to use
    PYTHON=/usr/bin/python

    # find the root of the virtualenv, it should be the parent of the dir this script is in
    ENV=`$PYTHON -c "import os; print os.path.abspath(os.path.join(os.path.dirname(\"$0\"), '..'))"`

    # now run Python with the virtualenv set as Python's HOME and set to prefer 32 bit
    export PYTHONHOME=$ENV
    export VERSIONER_PYTHON_PREFER_32_BIT=yes
    exec $PYTHON "$@"
    ```

9. Finally, now you can go into `$DITTOHEAD_ROOT/src/client` and run `wxpy dittohead.py`.


## TODO

- Autofill combobox for user name, if possible. (This seems non-trivial with current wxPython, unfortunately.)
- YAML: we should remove the weird unicode garbage pile if possible.

