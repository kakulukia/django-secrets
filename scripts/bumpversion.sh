#!/usr/bin/env bash
while true; do
    CURRENT=`python -c "import pypugjs; print(pypugjs.__version__)"`
    echo ""
    echo "=== The current version is $CURRENT - what's the next one?"
    echo "==========================================================="
    echo "1 - new major version"
    echo "2 - new minor version"
    echo "3 - patch"
    echo ""
    read yn
    case $yn in
        1 ) bumpversion major; break;;
        2 ) bumpversion minor; break;;
        3 ) bumpversion patch; break;;
        * ) echo "Please answer 1-3.";;
    esac
done
