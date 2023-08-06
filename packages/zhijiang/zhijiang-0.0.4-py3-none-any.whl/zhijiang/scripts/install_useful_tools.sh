sudo apt install -y tldr tmux
sudo apt install autojump; wget -O ~/.autojump.bash "https://raw.githubusercontent.com/wting/autojump/master/bin/autojump.bash"; echo source ~/.autojump.bash > ~/.bashrc
sudo apt install -y gdb cgdb 
sudo apt install -y icdiff

sudo env "PATH=$PATH" pip install  py-spy viztracer

(
cd /tmp
wget https://raw.githubusercontent.com/satanson/cpp_etudes/master/calltree.pl
wget https://raw.githubusercontent.com/satanson/cpp_etudes/master/cpptree.pl
chmod 777 calltree.pl cpptree.pl
sudo mv calltree.pl /usr/local/bin
sudo mv cpptree.pl /usr/local/bin
)
