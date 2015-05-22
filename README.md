# dittohead

A secure one-way file synchronizer that never forgets anything.

------------

- [Client README](src/client/README.md)
- [Server README](src/server/README.md)

------------

## About

We need a tool that is platform agnostic and secure for sending data to a locked-down final location that the user themselves may not have final read or write access to.

It needs to be a one-way file sync that does not destroy data.

If data is re-copied multiple times with the same path and name, all versions need to be conserved.

We are going to use a two-step process of a copier client and a watcher daemon. It needs to be agnostic about the file structure on both sides.

We are not planning to support simultaneous uploads from two machines to the same directory.

------


## Documentation

TODO

We need documentation for data collectors so they know how to run the tool (even though it's *way easy*), and we need documentation for the study runners so they know *how it works.*


## Acknowledgements

- Icon from http://ic8.link/901


