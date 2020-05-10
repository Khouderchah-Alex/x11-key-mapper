#!/usr/bin/env bash

pushd $(dirname $(realpath $0)) > /dev/null

# Create config directory.
if [ ! -d config ]; then
    mkdir config
    chown $(logname) config
fi

# Copy default mapping if no mappings exist.
if [ $(ls -1 config/*.py 2>/dev/null | wc -l) == 0 ]; then
    cp default_mappings.py \
       config/mappings.py
    chown $(logname) config/mappings.py
fi

# Copy git hook.
git config --unset core.hooksPath  # Ensure hooksPath is unset.
cp post-merge .git/hooks/
chown $(logname) .git/hooks/post-merge

echo ""
echo "Update success!"
echo ""

popd > /dev/null
