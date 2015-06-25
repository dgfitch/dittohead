# dittohead server

Uses:

- [watchdog](http://pythonhosted.org/watchdog/)

## Configure

1. `pip install watchdog` (in a virtualenv if you prefer)
2. Edit config.yaml

## TODO

- Actually decide what the backend should do
- Pull out shared logging and yaml loading code between server/client, bleh

## Watcher daemon

1. Watch `inbox` directory for things that are complete (don't start with .)
2. Fork a child
3. Move it to `processing` directory
4. Copy to the correct location (probably rsync), ensuring that no files are overwritten
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


