# TUMExam Scripts

[[_TOC_]]

## TL;DR

```shell
pip3 install tum-exam-scripts --extra-index-url https://TUM:7rpYfJvEqzG3MvwN3Xfo@gitlab.lrz.de/api/v4/projects/102241/packages/pypi/simple
tum-exam-scripts install-linux-driver
tum-exam-scripts send-all-booklets /path/to/exams
tum-exam-scripts send-attendee-list --attendee-list
  /path/to/attendeelist.pdf
```

## Commands 

```shell
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

```shell
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

```shell
tum-exam-scripts send-all-booklets --help
Usage: tum-exam-scripts send-all-booklets [OPTIONS] [INPUT_DIRECTORY]

  Send all booklets to the printing server.

  Example:     tum-exam-scripts send-all-booklets /path/to/exams/

Arguments:
  [INPUT_DIRECTORY]  The directory with the exams from the TUMExam website.
                     [default: .]

Options:
  -d, --driver-name TEXT    Name of the driver  [default: followmeppd]
  -b, --batch-size INTEGER  If you add a batch size, the process will stop
                            after so many exams and wait for you to
                            continue.You can you this so start all jobs on a
                            printer, then send the next batch, and start these
                            exams on another printer.
  --help                    Show this message and exit.
```

### Send Specific Booklets 

```shell
tum-exam-scripts send-specific-booklets --help
Usage: tum-exam-scripts send-specific-booklets [OPTIONS] [PDF_FILE]...

  Send only specific PDFs to the server. You can pass multiple files.

  Example:     tum-exam-scripts send-specific-booklets /path/to/E0007-book.pdf
  /path/to/E0009-book.pdf

Arguments:
  [PDF_FILE]...  The directory with the exams from the TUMExam website.

Options:
  -d, --driver-name TEXT  Name of the driver  [default: followmeppd]
  --help                  Show this message and exit.
```

### Send Attendee List

```shell
tum-exam-scripts send-attendee-list --help
Usage: tum-exam-scripts send-attendee-list [OPTIONS] [ATTEND_LIST]

  Send the attendee list to the server.

  Example:     tum-exam-scripts send-attendee-list /path/to/attendeelist.pdf

Arguments:
  [ATTEND_LIST]  The directory with the exams from the TUMExam website.
                 [default: attendeelist.pdf]

Options:
  -d, --driver-name TEXT  Name of the driver  [default: followmeppd]
  --help                  Show this message and exit.
```
