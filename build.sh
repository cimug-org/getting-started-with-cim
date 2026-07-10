#!/bin/env bash

set -e

rm -rf docs-adoc
mkdir -p docs-adoc

for src_dir in src/*; do
    version=$(basename $src_dir)
    root_module=docs-adoc/$version/modules/ROOT

    if [ $version == "1.0" ]; then
        cp -r $src_dir docs-adoc/
        root_module=docs-adoc/$version/modules/ROOT
        continue
    elif [ $version == sandbox ]; then
        continue
    fi

    mkdir -p $root_module/{attachments,images,pages}
    mkdir $root_module/attachments/examples

    echo "name: ROOT" >> $root_module/../../antora.yml

done

npx antora ${1:-antora-playbook.yml}
touch docs/.nojekyll
