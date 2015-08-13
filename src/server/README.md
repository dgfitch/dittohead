# dittohead server

Uses:

- [watchdog](http://pythonhosted.org/watchdog/)


## Configure a virtualenv

1. `python virtualenv.py dittohead_server`
2. `source dittohead_server/bin/activate`


## Configure server

1. `pip install watchdog`
2. Edit config.yaml


## Running

1. Run `dittohead_watcher.py`
2. Wait for tasty files to arrive


## Administration

### General workflow

1. Uploader client puts stuff in inbox directory, named with a `.period` at the beginning

2. Uploader client finishes, and moves the directory so it doesn't have a period

3. Watcher daemon fires a worker process which:
    1. Moves the directory to `processing`
    2. Runs `rsync` to copy to the final location
    3. Moves the directory to `done`
   

### General upkeep

1. Check for stuff sitting in the inbox directory

2. Check for stuff sitting in the processing directory. Things should only be here when they are being actively processed

3. Clean out the "done" directory once in a while


## TODO

- Fix rsync path so it works right
- Ensure directories get g+s
- Check study name is just letters and numbers
- Make logs go someplace less stupid
- Make code less ugly


## Watcher daemon

1. Watch `inbox` directory for things that are complete (don't start with .)
2. Fork a child
3. Move it to `processing` directory
4. Copy to the correct location (probably rsync), ensuring that no files are overwritten or changed
5. Optional notification email


## Permissions required

### Watcher location

    /.../dittohead (dittohead:dittohead-grp, 755)
      /inbox (mode 3773)
        /.foo-{id} (copied in by user, so ends up user:dittohead-grp)
          files
          .
          .
          .
      /processing (mode 700)
      /done (mode 700)

### Final location

TODO: Still being determined

Everything is the same as it was for raw-data, so it can be locked down separately. We create a new directory inside /study/foo, like so:

    /study
      /foo (foo:foo-grp 3775)
        /raw-data (mri:foo-raw-data 3750)
        /raw-dittohead (dittohead:foo-grp 3750)
          /eprime
          /biopac
          .
          .
          .


## Notification

We may want to make the watcher notify someone about failed or even successful jobs in the future.

We may also want to include "Hey, your study is out of space!" or "Your study is 90% full" notifications with that.


