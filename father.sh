#!/bin/bash
#
# Father of pygit++
#
# remote builder and installer 
# of pygit++
#
# version 0.0.1

GREEN='\033[0;32m'
NC='\033[0m'

function print_message(){
  echo -e "${GREEN}$1${NC}"
}

function install_pygit(){
  echo -e "${GREEN}Building and installing pygit++${NC}"
  mkdir -p build
  cd build || exit 1

  wget -q https://github.com/thelibertti/pygit-/releases/download/pre-alpha-version-0.0.01/pygit++_source.zip
  unzip -q pygit++_source.zip

  python3 -m venv env > /dev/null
  source env/bin/activate

  cd pygit
  pip install -r requirements.txt > /dev/null
  cd ..

  pyinstaller --strip --name pygit++ pygit/main.py > /dev/null

  echo -e "${GREEN}Moving binary to local bin directory...${NC}"
  cd dist || exit 1
  cd pygit++ || exit 1

  var_prefix="$PREFIX"

  if [[ -z "$var_prefix" ]]; then
      sudo mv * /usr/local/bin
  else
      mv * "$var_prefix/bin"
  fi

  echo -e "${GREEN}Cleaning up and removing 'build' folder...${NC}"
  cd ..
  cd ..
  cd ..
  rm -rf build

  echo -e "${GREEN}Installation complete! You can now execute 'pygit++'.${NC}"
}

function uninstall_pygit() {
  var_prefix="$PREFIX"
  if [[ -z "$var_prefix" ]]; then
    sudo rm -rf /usr/local/bin/_internal 
    sudo rm /usr/local/bin/pygit++
  else
    rm -r $PREFIX/bin/_internal
    rm $PREFIX/bin/pygit++
  fi
  echo "${GREEN} Pygit++ succefully uninstalled. ${NC}"
}

function print_information(){
  print_message "Intaller Usage: father -[command]"
  echo ""
  print_message "Aviable command:"
  print_message "-I to install pygit++ in your system"
  print_message "-R to uninstall pygit++ build from your system"


}


if [ "$1" == "-I" ]; then
  install_pygit
elif [ "$1" == "-R" ]; then
  uninstall_pygit
else
  print_information
  exit 1
fi
