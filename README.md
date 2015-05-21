# dittohead

A secure one-way file synchronizer that never forgets anything.


------------


## TODO

- UI
  - Make the stupid `copy_gauge` size right when it shows up
  - Nice native browse box to select local directory for studies
  - Better exception handling, show error to user in wx interface and die instead of just logging
- Actually decide what the backend should do
- Pull out shared logging and yaml loading code between server/client, bleh

------------

## About

We need a tool that is platform agnostic and secure for sending data to a locked-down final location that the user themselves may not have final read or write access to.

It needs to be a one-way file sync that does not destroy data.

If data is re-copied multiple times with the same path and name, all versions need to be conserved.

We are going to use a two-step process of a copier client and a watcher daemon. It needs to be agnostic about the file structure on both sides.

We are not planning to support simultaneous uploads from two machines to the same directory.


## Copier client

(probably a little wxPython UI)

1. You select your study (top-level folder).
2. You select what thing inside there to send, if any. (eprime, eyetracker, biopac... many studies may have a default or we may script this to just do all things inside that study)
3. You enter your credentials because the local PC may be running as some local account for data gathering.
4. The copier plops new stuff in the watched location with a period at the start so it's ignored, and when done, renames without the period.
5. The folder name of what is copied also contains a unique identifier of the location, somehow. (Brogden A, etc.)

### Ways to find what to copy

- Leave inbox around, rsync into it
- maybe use rsync --dry-run somehow
- Keep a textfile with last update timestamp
- Create staging home (temp directory) and pscp -r
- Two steps: Create all directories newer than X, copy files newer than X (requires update timestamp)
- scp -r with directories if newer than X, else individual files newer than X (requires update timestamp)

------

## Watcher daemon

1. Watch `inbox` directory for things that are complete (don't start with .)
2. Fork a child
3. Move it to `processing` directory
4. Copy to the correct location (probably rsync), ensuring that no files are overwritten
5. Optional notification email

## Permissions required

### Watcher location

    /.../dittohead (dittohead:dittohead)
      /inbox (mode 3777)
        /.foo-{id} (copied in by user, so ends up user:user-grp mode 700)
          /eprime
          /biopac
          .
          .
          .
      /processing (mode 700)
      /done (mode 7000)

### Final location

Everything is the same as it was for raw-data, so it can be locked down separately. We create a new directory inside /study/foo, like so:

    /study
      /foo (foo:foo-grp 775 +s)
        /raw-data (mri:foo-raw-data 750 +s)
        /raw-dittohead (dittohead:foo-dittohead 750 +s)
          /eprime
          /biopac
          .
          .
          .
          /eyetracker


### Permissions

From Nate:

    DITTO_ROOT (dittohead:dittohead, 3777) (eg, /data-dropbox)
    DITTO_STUDY_ROOT (dittohead:dittohead, 3777) (eg, DITTO_ROOT/nccam3)
    DITTO_STUDY_INBOX (dittohead:dittohead, 3777) (eg, DITTO_STUDY_ROOT/inbox)
    Entries in DITTO_STUDY_INBOX will have group ownership set to dittohead. They'll only be *writable* by UPLOAD_USER.

    DITTO_STUDY_PROCESSING (dittohead:dittohead, 700) (eg, DITTO_STUDY_ROOT/processing)
    DITTO_STUDY_DONE (dittohead:dittohead, 700) (eg, DITTO_STUDY_ROOT/done)
    STUDY_DESTINATION (dittohead:raw-data, 775) (eg, /study/nccam3/data-dropbox)

    OK, permissions-wise, since `DITTO_STUDY_INBOX` is dittohead:dittohead, mode 3777, watcher (running as dittohead) can read there, and anyone can put things there. Watcher can move entries to `DITTO_STUDY_PROCESSING` and then to `DITTO_STUDY_DONE`. We can't delete them because they're owned by `UPLOAD_USER`, but root can purge stuff from `_DONE`. 

    We probably don't want to call directories out on /study "dittohead" because someone will be annoyed by that. Still a fine project name.


## Documentation

We need documentation for data collectors so they know how to run the tool (hopefully it's *way easy*), and we need documentation for the study runners so they know *how it works.*

## Notification

We may want to make the watcher notify someone about failed or even successful jobs.

We may also want to include "Hey, your study is out of space!" or "Your study is 90% full" notifications with that.


## Acknowledgements

- Icon from http://ic8.link/901


