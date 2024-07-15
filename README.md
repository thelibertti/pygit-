# WELCOME TO THE PYGIT++ ERA!!
(WARNING: This program is not even in alpha; much of it is still incomplete work)

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/e1324c5c0c954f8da2981d702dddb344)](https://app.codacy.com/gh/thelibertti/pygit-/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)

# PYGIT++
**Pygit++ can be definde as simple as just as a better user
experience for git**

![template](https://github.com/user-attachments/assets/15d2905a-7436-406e-8fc0-0f325fccb853)

# Get this buggy thing goin!

## For user

**There is a binary options for users simple
run the following command in your terminal
and it will build and set up the binary for you**

**Please notice that you will need the following 
dependencies in your system**

- [curl](https://curl.se/)
- [unzip](https://linux.die.net/man/1/unzip)
- [wget](https://linux.die.net/man/1/wget)
- [python](https://www.python.org/)
- [python-venv](https://docs.python.org/3/library/venv.html)
- [bat](https://github.com/sharkdp/bat)

(Note: sudo permission is required in order to place
the binary into ```/opt/pygit++``` and to creare the simbolic link )

**NOTE: pygit++ binary will be in installed into
```opt/pygit++``` and a simbolic link will be created**

```bash
curl -sSL https://raw.githubusercontent.com/thelibertti/pygit-/main/father.sh | bash
```

### Manual Copilation

**Introctions comming soon**


##  For DEVS

### First clone this repo:

```bash
git clone https://github.com/thelibertti/pygit-
```

### install the dependencies with

```bash
pip install -r requirements.txt
```

**External dependencies**
- [bat](https://github.com/sharkdp/bat)

### Add it to your path!
look for your shell configuration file such as '.zshrc' or '.bashrc'
in your home directory and open it, and add the next line:
```bash
alias pygit="python [path_to_the_pygit++_dir]/main.py"
```

(Make sure to change the path to where main.py is 
located and remove the square brackets)

And that’s it, you’re good to go!

## HELP?

##### Try ```pygit -h``` or see the DOCS
