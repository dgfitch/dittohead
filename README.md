# dittohead

A secure one-way file synchronizer that never forgets anything.

------------

- [Client README](src/client/README.md)
- [Server README](src/server/README.md)

------------

## About

We needed a platform-agnostic tool that can securely send data to a locked-down final location that the user themselves may not have final read or write access to.

It is a one-way file sync that does not destroy data.

If data is re-copied multiple times with the same path and name, all versions are conserved.

We use a two-step process of a copier client and a watcher daemon. It is relatively agnostic about the file structure on both sides.

We do not plan to support simultaneous uploads from two machines to the same directory.

------


# Documentation

## For data collectors

### How to upload new files

1. Launch dittohead.
2. Select your study on the left. A preview of what files will be sent will display.
3. A list of recent users will be filled in and you can select yourself or 
   type in your account name. (This is your BI account.)
4. Enter your password.
5. Click copy.

### How to hook up a new study

1. Launch dittohead.
2. Click **Add Study**.
3. Fill in the study name.
4. Click Browse by the local directory and choose where the local data files 
   for this study are collected.
5. Fill in the remote location. (Usually, /study/{NAME}/raw-data ?)
6. Hit OK. You are now ready to upload data!

### To change file locations for a study

1. Launch dittohead.
2. Select the study you want to edit
2. Click **Edit Study**

### Advanced editing

The metadata for studies is stored locally in `studies.yaml` and can be edited 
directly there if needed.

## For study runners

Dittohead is simply a tool to take local files on collection machines and 
securely upload them to locked-down study locations that cannot be edited 
later.

It operates by using the user's account credentials to copy files over SSH to 
a temporary location. Once it is done copying, it renames the temporary 
directory to notify the dittohead daemon that the sync is complete.

At that point, the dittohead watcher daemon on the server fires a copy 
procedure that moves the files into the final destination in a secure manner, 
assuring that no previous files get overridden.

The original user is notified by email when this process is complete, and 
additional users can be set per-study to be notified as well.



## Acknowledgements

- Icon from http://ic8.link/901


