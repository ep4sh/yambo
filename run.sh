#!/usr/bin/env bash

#    Copyright (C) 2019, Pasha Radchenko, <ep4sh2k@gmail.com> 
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.

# VP is "Virtualenv path"
VP=$PWD/yamboenv
echo "Checking virtual env..."

[ ! -d $VP ] && echo "Directory ${VP} doesn't  exists.." && python3 -m venv $VP;

cd $VP;
source $VP/bin/activate

echo "Installing dependencies with pip..."
pip -V

pip3 install -r ../requirements.txt
#hotfix 
pip3 install --upgrade -e 'git+https://github.com/yammer/yam-python@master#egg=yampy'
cd -;
chmod +x $PWD/main.py;

echo "Running yAmbo..."
python3 main.py
echo "Check you yAmmer ;)"
