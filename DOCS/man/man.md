# Welcome to the official pygit++ user manual!!

## General Information

**Description:** A better way to work with git in your terminal

**Current Version:** 0.0.1

**Usage:**
```bash
pygit++ [command] [subcommand] [options]
```

## Available Commands:

### -h, --help

- **Prints the help message and exits**

**Usage:**

```bash
pygit++ -h [or --help]
```

### -man

- **Opens the user manual for pygit++**

**Usage:**

```bash
pygit++ -man
```

### -i 

- **Starts an empty git repo**

**Usage:**
```bash
pygit++ -i
```

This command will create an empty git repo in the current directory
if your directory already has some work we sugesst you to run 
```pygit++ --init``` instead


### --init

**Usage:**
```bash
pygit++ --init
```

This command will help you to set up your current
directory into a git repo


### -a, --add
    
- **A better way to add your work to the index of the repo**
    
**Usage**

```bash
pygit++ -a [or --add] [<file> <file>]
```
You can call ```pygit++ -a or <--add>```
and you will prompted to provide the rest of the  information
    
Optionally you can pass the name of the
files for example ```'pygit++ -a foo.lua foo.txt'``` will 
add those files into the index 

Optionally if you are sure that you want to add all
the modified files into the index you can just call 
```'pygit++ -a .'```

### -c, --commit

- **A better way to commit your work**

**Usage:**
```bash
pygit++ -c [ or --commit] [-commit_msg]
```

You can call ```pygit++ -c``` by itself and then you will
be promted to provide the rest of the information

Optionally, you can call ```pygit++ -c [your_commit_msg]```, 
this will automatically commit all the files that are stagedif there 
are not files staged you will be promted to add them.
