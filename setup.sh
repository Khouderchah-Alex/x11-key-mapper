#!/usr/bin/env bash

# This script can be used to set up use of key_mapper.py.

if [[ $EUID > 0 ]]; then
    echo "Please run as root. Exiting..."
    exit 1
fi

git_install() {
    if [[ $# != 1 ]]; then
        echo "$0 needs to be passed a single argument"
        exit 2
    fi

    git clone "$1" ___dependency
    cd ___dependency
    make && sudo make install
    cd ..
    rm -rf ___dependency
    return 0
}

exists() {
    if [[ $# != 1 ]]; then
        echo "$0 needs to be passed a single argument"
        exit 2
    fi

    if command -v "$1"; then
        echo "$1 already exists. Skipping."
        echo ""
        return 0
    fi
    return 1
}


pushd $(dirname $(realpath $0)) > /dev/null

exists xtitle
if [[ $? -ne 0 ]]; then
    git_install "https://github.com/baskerville/xtitle"
    echo "xtitle installed."
    echo ""
fi

exists xdotool
if [[ $? -ne 0 ]]; then
    git_install "https://github.com/jordansissel/xdotool"
    echo "xdotool installed."
    echo ""
fi

# Since we are installing from a fork, don't bother checking whether the command
# exists.
git_install "https://github.com/Khouderchah-Alex/actkbd"
echo "actkbd installed."
echo ""

echo ""
echo "Dependency installation success!"
echo ""

./update.sh

popd > /dev/null
