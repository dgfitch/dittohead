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

## TODO

- Pull out shared logging and yaml loading code between server/client, bleh
- Make logs go someplace less stupid

## Watcher daemon

1. Watch `inbox` directory for things that are complete (don't start with .)
2. Fork a child
3. Move it to `processing` directory
4. Copy to the correct location (probably rsync), ensuring that no files are overwritten or changed
5. Optional notification email

## Permissions required

### Watcher location

    /.../dittohead (dittohead:dittohead, 755)
      /inbox (mode 3773?)
        /.foo-{id} (copied in by user, so ends up user:dittohead)
          /eprime
          /biopac
          .
          .
          .
      /processing (mode 700)
      /done (mode 700)

### Final location

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

We may want to make the watcher notify someone about failed or even successful jobs.

We may also want to include "Hey, your study is out of space!" or "Your study is 90% full" notifications with that.


