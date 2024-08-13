<p align="center">
    <img src="static/logo_pygit2.svg" width="2000" height="500"/>
</p>

> [!WARNING]
> This project was moved [here.](https://github.com/DliberttiGroup/pygit-p-p)
>
> This repo is not longer manteined because it was moved [here](https://github.com/DliberttiGroup/pygit-p-p)

# PYGIT++
**Pygit++ can be defined as simple as just as a better user
experience for git.**


# Features 

<details>
<summary  style="font-size: 1em; font-weight: bold;">Better status display of the current repo</summary>

#### So you can understand better what's going on!!

![template](static/img1.png)

</details>

<details>
<summary  style="font-size: 1em; font-weight: bold;">Better Commit and Add system</summary>

#### Commit
![template](static/img2.png)

#### Add
![template](static/img3.png)

</details>

<details>
<summary  style="font-size: 1em; font-weight: bold;">A profile system</summary>

#### so you can work with multiple github accounts 

#### Examples coming soon...

</details>

<details>
<summary  style="font-size: 1em; font-weight: bold;">Better User Experience</summary>

### Pygit++ has been designed to bring a better and modern experience when working with git in your terminal by:

- **More Verbose But Just The Necessary**:
    
    Pygit++ is general more verbose than git making it easier for you to understand what is going on.

- **A Modern Touch**:

    Pygit++ has been designed to have a colorful and modern experience.
    
- **More Abstraction = Easier To Use**:

    Pygit++ has been implemented with simpler commands this so user can have a better workflow 


</details>


# Get this buggy thing going!

Before starting make sure you have the following external
dependencies

- [bat](https://github.com/sharkdp/bat)



## Automatic installation (Linux only)

**There is a binary options for users simple
run the following command in your terminal
and it will build and set up the binary for you:**


```bash
curl -sSL https://raw.githubusercontent.com/thelibertti/pygit-/main/father.sh | bash
```


**Please notice that you will need the following 
dependencies in your system**

- [curl](https://curl.se/)
- [unzip](https://linux.die.net/man/1/unzip)
- [wget](https://linux.die.net/man/1/wget)
- [python](https://www.python.org/)
- [python-venv](https://docs.python.org/3/library/venv.html)


(Note: Pygit++ will be installed in ```usr/local/bin``` or in ```$PREFIX/bin``` in 
case you are in Termux)

## Manual Compilation (Windows and Linux users)

For manual compilation 

first clone this repo with:

```bash
git clone https://github.com/thelibertti/pygit-
```

then go into the repo and run: 

```bash
pip install -r requirements.txt
```

the you can run:

```bash
pyinstaller --strip --name pygit++ main.py
```

After that you should see a bunch of new directories 
go into `dist/` and there you should find the pygit++ directory,
inside `pygit++/` you will find the binary and the dependencies 
in `_internal/`, now you can decide where to place both the binary 
and the dependencies.


##  For DEVS (Linux and Windows users)

First clone this repo:

```bash
git clone https://github.com/thelibertti/pygit-
```

install the dependencies with

```bash
pip install -r requirements.txt
```

## Add it to your path!

**Linux:**
look for your shell configuration file such as '.zshrc' or '.bashrc'
in your home directory and open it, and add the next line:
```bash
alias pygit="python [path_to_the_pygit++_dir]/main.py"
```


**Windows**
Run in powershell:
```powershell
notepad $PROFILE
```

There add the next line:
```powershell
Set-Alias pygit "python [path_to_the_pygit++_folder/main.py]"
```

(Make sure to change the path to where main.py is 
located and remove the square brackets)

And that’s it, you’re good to go!

## HELP?

##### Try ```pygit -h``` or see the DOCS


## Contributing

In case you found a bug you can open an issue and we will try to help
you as soon as we can can. 

In case you want to contribute to this project there is a template
for the contributions in [Contributions](DOCS/contributions.md)
