# TUMExam Scripts

[[_TOC_]]

## TL;DR

```bash
pip3 install tum-exam-scripts --extra-index-url https://TUM:7rpYfJvEqzG3MvwN3Xfo@gitlab.lrz.de/api/v4/projects/102241/packages/pypi/simple
tum-exam-scripts install-linux-driver
tum-exam-scripts send-all-booklets --input-directory /path/to/exams
tum-exam-scripts send-attendee-list --attendee-list
  /path/to/attendeelist.pdf
```

## Commands 

```bash
tum-exam-scripts --help
Usage: tum-exam-scripts [OPTIONS] COMMAND [ARGS]...

  :return:

Options:
  --version                       Version
  --help                          Show this message and exit.

Commands:
  install-linux-driver    This snippet downloads the Linux driver for the...
  send-all-booklets       Send all booklets to the printing server.
  send-attendee-list      Send the attendee list to the server.
  send-specific-booklets  Send only specific PDFs to the server.
```

### Install Linux Driver

```bash
tum-exam-scripts install-linux-driver --help
Usage: tum-exam-scripts install-linux-driver [OPTIONS]

  This snippet downloads the Linux driver for the printers and makes them
  available under $driver_name This is needed as the macOS driver cannot
  handle the booklets. Please change the command on mac for printing the exams
  from `-dfollowme` to `-dfollowmepdd`!!!

Options:
  -d, --driver-name TEXT  Name of the driver  [default: followmeppd]
  -p, --password TEXT     Your user password. NOTE: The user should have
                          'sudo' privileges.
  --help                  Show this message and exit.
```

### Send All Booklets

```bash
tum-exam-scripts send-all-booklets --help
Usage: tum-exam-scripts send-all-booklets [OPTIONS]

  Send all booklets to the printing server.

  Example:     tum-exam-scripts send-all-booklets --input-directory
  /path/to/exams/

Options:
  -d, --driver-name TEXT          Name of the driver  [default: followmeppd]
  -d, --input-directory DIRECTORY
                                  The directory with the exams from the
                                  TUMExam website.  [default: .]
  --help                          Show this message and exit.
```

### Send Specific Booklets 

```bash
tum-exam-scripts send-specific-booklets --help
Usage: tum-exam-scripts send-specific-booklets [OPTIONS]

  Send only specific PDFs to the server. You can pass multiple files.

  Example:     tum-exam-scripts send-specific-booklets --booklet-pdf
  /path/to/E0007-book.pdf --booklet-pdf /path/to/E0009-book.pdf

Options:
  -P, --booklet-pdf FILE  The directory with the exams from the TUMExam
                          website.
  -d, --driver-name TEXT  Name of the driver  [default: followmeppd]
  --help                  Show this message and exit.
```

### Send Attendee List

```bash
tum-exam-scripts send-attendee-list --help
Usage: tum-exam-scripts send-attendee-list [OPTIONS]

  Send the attendee list to the server.

  Example:     tum-exam-scripts send-attendee-list --attendee-list
  /path/to/attendeelist.pdf

Options:
  -a, --attendee-list FILE  The directory with the exams from the TUMExam
                            website.  [default: attendeelist.pdf]
  -d, --driver-name TEXT    Name of the driver  [default: followmeppd]
  --help                    Show this message and exit.
```
