# Grade: Python Module

This repository is a part of the [grade project](https://github.com/mia1024/grade). Tested on Arch Linux with Python3.9.

## Dependencies

- python 3.8+
- node 14+

## Run

```sh
git clone git@github.com:mia1024/grade-script
cd grade-script/electron
npm i 
# if you have yarn installed, you probably want to use `yarn install` instead
cd ..
python3 -m pip install -r requirements.txt 
python3 main.py
```

Example output:
```
───────────────────────────────────────────────────────────────────────────────
                               Tuesday, Feb 23                                
Homework 4 Written: hivTree.pdf (Bio 52)               11:59 PM (late)

───────────────────────────────────────────────────────────────────────────────
                              Wednesday, Feb 24                               
PreClass 9.5 (HMC Chemistry 23B SP21)                  10:00 AM
Homework 4 (HMC Chemistry 23B SP21)                    05:00 PM

───────────────────────────────────────────────────────────────────────────────
                                Monday, Mar 1                                 
Homework 5 Code: branchLen.py (Bio 52)                 11:59 PM (late +24hr)
Homework 5 Written: kaks.pdf (Bio 52)                  11:59 PM (late +24hr)

```

## Note on course list and names

A file named `courses.json` will be generated under the repository root after running 
the program for the first time. Feel free to edit it and remove courses you don't care
about. In fact, you are encouraged to remove those courses to conserve bandwidths. If 
you want to change the display name of the course in the output , simply change the 
`name` field in the json file. 

## Note on Electron

The primary purpose of electron at this stage is to determine the cookies sent by Gradescope. 
If you don't want to install it for such a trivial purpose, you can manually create a file 
named `cookies.json` with a single key-value mapping of the cookies from gradescope, which you 
can extract from your browser. The file should look like this
```json
{
    "_ga": "[REDACTED]",
    "_gid": "[REDACTED]",
    "signed_token": "[REDACTED]",
    "remember_me": "[REDACTED]",
    "_gradescope_session": "[REDACTED]"
}
```
