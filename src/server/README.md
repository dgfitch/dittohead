# dittohead server

Uses:

- [watchdog](http://pythonhosted.org/watchdog/)


## Installation

### Configure a virtualenv

1. `python virtualenv.py dittohead_server`
2. `source dittohead_server/bin/activate`


### Configure server

1. `pip install watchdog`
2. Edit config.yaml


### Run the daemon

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
   
If you want to re-run something, move it from `done` to `inbox`.


### General upkeep

1. Check for stuff sitting in the inbox directory

2. Check for stuff sitting in the processing directory. Things should only be here when they are being actively processed

3. Clean out the "done" directory once in a while


## Notes


### Watcher location and permissions

    /.../dittohead (dittohead:dittohead-grp, 755)
      /inbox (mode 3773)
        /.foo-{id} (copied in by user, so ends up user:dittohead-grp)
          files
          .
          .
          .
      /processing (mode 700)
      /done (mode 700)

### Final location and permissions

Everything is the same as it was for raw-data, so it can be locked down separately. We create a new directory inside /study/foo, like so:

    /study
      /foo (foo:foo-grp 3775)
        /raw-data (mri:foo-raw-data 3750)
        /raw-dittohead (dittohead:foo-grp 3750) [this name is still TBD]
          files
          .
          .
          .


### Notification

We may want to make the watcher notify someone about failed or even successful jobs in the future.

We may also want to include "Hey, your study is out of space!" or "Your study is 90% full" notifications with that.

### TODO

- Make logs go someplace less stupid
- Make code less ugly

