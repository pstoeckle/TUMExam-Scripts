# TUMExam Scripts

[[_TOC_]]

## TL;DR

```shell
pip3 install tum-exam-scripts --extra-index-url https://TUM:7rpYfJvEqzG3MvwN3Xfo@gitlab.lrz.de/api/v4/projects/102241/packages/pypi/simple
tum-exam-scripts install-linux-driver
tum-exam-scripts store-password-in-password-manager your-informatics-username
tum-exam-scripts open-printing-page your-informatics-username
tum-exam-scripts pdf send-all-booklets --batch-size 50 /path/to/exams
tum-exam-scripts pdf send-attendee-list /path/to/attendeelist.pdf
tum-exam-scripts pdf send-room-layout /path/to/roomplan.pdf
tum-exam-scripts pdf send-seat-plan /path/to/seatplan-a3.pdf
```

## Commands 

```shell
$ tum-exam-scripts --help
                                                                                                                                                                                                                                              
 Usage: tum-exam-scripts [OPTIONS] COMMAND [ARGS]...                                                                                                                                                                                          
                                                                                                                                                                                                                                              
 A collection of useful commands to print TUMExams. You can find the source code under https://gitlab.lrz.de/i4/software/tum-exam-scripts                                                                                                     
                                                                                                                                                                                                                                              
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --version                     Version                                                                                                                                                                                                      │
│ --install-completion          Install completion for the current shell.                                                                                                                                                                    │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.                                                                                                                             │
│ --help                        Show this message and exit.                                                                                                                                                                                  │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ install-linux-driver                This snippet downloads the Linux driver for the printers and makes them available under $driver_name This is needed as the macOS driver cannot handle the booklets. Please change the command on mac   │
│                                     for printing the exams from `-dfollowme` to `-dfollowmepdd`!!!                                                                                                                                         │
│ open-printing-page                  Open the page we need to send the PDFs to the FollowMe printer.                                                                                                                                        │
│ pdf                                 Subgroup with the PDF printing commands.                                                                                                                                                               │
│ store-password-in-password-manager  Stores the password in the password manager.                                                                                                                                                           │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### Install Linux Driver

```shell
$ tum-exam-scripts install-linux-driver --help
                                                                                                                                                                                                                                              
 Usage: tum-exam-scripts install-linux-driver [OPTIONS]                                                                                                                                                                                       
                                                                                                                                                                                                                                              
 This snippet downloads the Linux driver for the printers and makes them available under $driver_name This is needed as the macOS driver cannot handle the booklets. Please change the command on mac for printing the exams from             
 `-dfollowme` to `-dfollowmepdd`!!!                                                                                                                                                                                                           
                                                                                                                                                                                                                                              
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --driver-name  -d      TEXT  Name of the driver [default: followmeppd]                                                                                                                                                                     │
│ --password     -p      TEXT  Your user password. NOTE: The user should have 'sudo' privileges. [default: None]                                                                                                                             │
│ --help                       Show this message and exit.                                                                                                                                                                                   │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

#### Install Linux Driver: Example

```shell
tum-exam-scripts install-linux-driver
```

### Store Password in Password Manager

We need the informatics username and the corresponding password to login into the printing page.
Thus, we store it in the system's password manager.

```shell
$ tum-exam-scripts store-password-in-password-manager --help
                                                                                                                                                                                                                                              
 Usage: tum-exam-scripts store-password-in-password-manager                                                                                                                                                                                   
            [OPTIONS] [USER_NAME]                                                                                                                                                                                                             
                                                                                                                                                                                                                                              
 Stores the password in the password manager.                                                                                                                                                                                                 
                                                                                                                                                                                                                                              
╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│   user_name      [USER_NAME]  The username for your informatics account, i.e., the first letters of your lastname. [default: None]                                                                                                         │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --password  -p      TEXT  The password for your informatics account [default: None]                                                                                                                                                        │
│ --force     -f            If true, we will overwrite existing passwords.                                                                                                                                                                   │
│ --help                    Show this message and exit.                                                                                                                                                                                      │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

#### Store Password in Password Manager: Example

```shell
tum-exam-scripts store-password-in-password-manager stoecklp
```

### Open the Printing Page

To print the documents via Wi-Fi with the FollowMe service, we need to open the informatics printing page.
This website has to stay open the whole time you are sending exam sheets to the printers.


```shell
$ tum-exam-scripts open-printing-page --help
                                                                                                                                                                                                                                              
 Usage: tum-exam-scripts open-printing-page [OPTIONS] [USER_NAME]                                                                                                                                                                             
                                                                                                                                                                                                                                              
 Open the page we need to send the PDFs to the FollowMe printer.                                                                                                                                                                              
                                                                                                                                                                                                                                              
╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│   user_name      [USER_NAME]  The username for your informatics account, i.e., the first letters of your lastname. [default: None]                                                                                                         │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                                                                                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

#### Open the Printing Page: Example

```shell
tum-exam-scripts open-printing-page stoecklp
```

### PDF Commands

I grouped all the PDF sending commands into a subgroup called `pdf`. 

```shell
                                                                                                                                                                                                                                              
 Usage: tum-exam-scripts pdf [OPTIONS] COMMAND [ARGS]...                                                                                                                                                                                      
                                                                                                                                                                                                                                              
 Subgroup with the PDF printing commands.                                                                                                                                                                                                     
                                                                                                                                                                                                                                              
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                                                                                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ send-all-booklets                                   Send all booklets to the printing server.                                                                                                                                              │
│ send-attendee-list                                  Send the attendee list to the server.                                                                                                                                                  │
│ send-room-layout                                    Print the room plans in A3. You have to put them at the doors of the lecture hall.                                                                                                     │
│ send-seat-plan                                      Print the seat plans in A3. You have to put them at the doors of the lecture hall.                                                                                                     │
│ send-specific-booklets                              Send only specific PDFs to the server. You can pass multiple files.                                                                                                                    │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```


#### Send All Booklets

```shell
$ tum-exam-scripts pdf send-all-booklets --help
                                                                                                                                                                                                                                              
 Usage: tum-exam-scripts pdf send-all-booklets [OPTIONS] [INPUT_DIRECTORY]                                                                                                                                                                    
                                                                                                                                                                                                                                              
 Send all booklets to the printing server.                                                                                                                                                                                                    
 Example:     tum-exam-scripts send-all-booklets /path/to/exams/                                                                                                                                                                              
                                                                                                                                                                                                                                              
╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│   input_directory      [INPUT_DIRECTORY]  The directory with the exams from the TUMExam website. [default: .]                                                                                                                              │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --driver-name  -d      TEXT     Name of the driver [default: followmeppd]                                                                                                                                                                  │
│ --batch-size   -b      INTEGER  If you add a batch size, the process will stop after so many exams and wait for you to continue.You can you this so start all jobs on a printer, then send the next batch, and start these exams on        │
│                                 another printer.                                                                                                                                                                                           │
│                                 [default: None]                                                                                                                                                                                            │
│ --help                          Show this message and exit.                                                                                                                                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

##### Send All Booklets: Example

```shell
tum-exam-scripts pdf send-all-booklets .
```

#### Send Specific Booklets 

```shell
$ tum-exam-scripts pdf send-specific-booklets --help
                                                                                                                                                                                                                                              
 Usage: tum-exam-scripts pdf send-specific-booklets [OPTIONS] [PDF_FILE]...                                                                                                                                                                   
                                                                                                                                                                                                                                              
 Send only specific PDFs to the server. You can pass multiple files.                                                                                                                                                                          
 Example:     tum-exam-scripts send-specific-booklets /path/to/E0007-book.pdf /path/to/E0009-book.pdf                                                                                                                                         
                                                                                                                                                                                                                                              
╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│   pdf_file      [PDF_FILE]...  The directory with the exams from the TUMExam website. [default: None]                                                                                                                                      │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --driver-name  -d      TEXT  Name of the driver [default: followmeppd]                                                                                                                                                                     │
│ --help                       Show this message and exit.                                                                                                                                                                                   │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

##### Send Specific Booklets: Example

```shell
tum-exam-scripts pdf send-specific-booklets /path/to/E0007-book.pdf /path/to/E0009-book.pdf
```

#### Send Attendee List

```shell
$ tum-exam-scripts pdf send-attendee-list --help
                                                                                                                                                                                                                                              
 Usage: tum-exam-scripts pdf send-attendee-list [OPTIONS] [ATTEND_LIST]                                                                                                                                                                       
                                                                                                                                                                                                                                              
 Send the attendee list to the server.                                                                                                                                                                                                        
 Example:     tum-exam-scripts send-attendee-list /path/to/attendeelist.pdf                                                                                                                                                                   
                                                                                                                                                                                                                                              
╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│   attend_list      [ATTEND_LIST]  The attendee list from the TUMExam endterm_lists folder. [default: attendeelist.pdf]                                                                                                                     │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --driver-name  -d      TEXT  Name of the driver [default: followmeppd]                                                                                                                                                                     │
│ --help                       Show this message and exit.                                                                                                                                                                                   │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
#### Send Attendee List: Example

```shell
tum-exam-scripts send-attendee-list /path/to/attendeelist.pdf
```

#### Send Room Layout

```shell
$ tum-exam-scripts pdf send-room-layout --help
                                                                                                                                                                                                                                              
 Usage: tum-exam-scripts pdf send-room-layout [OPTIONS] [ROOM_PLAN]                                                                                                                                                                           
                                                                                                                                                                                                                                              
 Print the room plans in A3. You have to put them at the doors of the lecture hall.                                                                                                                                                           
                                                                                                                                                                                                                                              
╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│   room_plan      [ROOM_PLAN]  The room plan in A3 from the TUMExam endterm_lists folder. [default: roomplan.pdf]                                                                                                                           │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --driver-name       -d      TEXT     Name of the driver [default: followmeppd]                                                                                                                                                             │
│ --number-of-copies  -n      INTEGER  The number of copies you want to print. [default: 3]                                                                                                                                                  │
│ --help                               Show this message and exit.                                                                                                                                                                           │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

##### Send Room Layout: Example

```shell
tum-exam-scripts pdf send-room-layout /path/to/roomplan.pdf
```


#### Send Seat Plan

```shell
$ tum-exam-scripts pdf send-seat-plan --help
                                                                                                                                                                                                                                              
 Usage: tum-exam-scripts pdf send-seat-plan [OPTIONS] [SEAT_PLAN]                                                                                                                                                                             
                                                                                                                                                                                                                                              
 Print the seat plans in A3. You have to put them at the doors of the lecture hall.                                                                                                                                                           
                                                                                                                                                                                                                                              
╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│   seat_plan      [SEAT_PLAN]  The seat plan in A3 from the TUMExam endterm_lists folder. [default: seatplan-a3.pdf]                                                                                                                        │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --driver-name       -d      TEXT     Name of the driver [default: followmeppd]                                                                                                                                                             │
│ --number-of-copies  -n      INTEGER  The number of copies you want to print. [default: 3]                                                                                                                                                  │
│ --help                               Show this message and exit.                                                                                                                                                                           │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

##### Send Seat Plan: Example

```shell
tum-exam-scripts pdf send-seat-plan /path/to/seatplan-a3.pdf
```

## Contact

If you have any question, please contact [Patrick Stöckle](mailto:patrick.stoeckle@tum.de?subject=GitLab%3A%20TUMExam%20Scripts&body=Hi%2C%0AI%20have%20the%20following%20question%20regarding%20the%20TUMExam%20Scripts%20library%3A).
