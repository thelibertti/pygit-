# Father of pygit++
#
# remote builder and installer 
# of pygit++
#
# version 0.0.1

GREEN='\033[0;32m'
NC='\033[0m'

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

pip install pyinstaller > /dev/null

pyinstaller --strip --name pygit++ pygit/main.py > /dev/null

echo -e "${GREEN}Moving binary to /opt and creating symbolic link...${NC}"
sudo mv dist/pygit++ /opt/pygit++
sudo ln -sf /opt/pygit++/pygit++ /usr/local/bin/pygit++

echo -e "${GREEN}Cleaning up and removing 'build' folder...${NC}"
cd ..
rm -rf build

echo -e "${GREEN}Installation complete! You can now execute 'pygit++'.${NC}"
