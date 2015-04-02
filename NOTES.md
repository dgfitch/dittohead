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


Paramiko seems to work
