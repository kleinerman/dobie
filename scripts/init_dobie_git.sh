#!/bin/bash

git clone jkleinerman@bitbucket.org:kleinerman/dobie.git
cd dobie
git config --global user.email "jkleinerman@gmail.com"
git config --global user.name "Jorge Kleinerman"
git config --global core.editor "vim"
git fetch origin jek_srv_bcknd:jek_srv_bcknd
git checkout jek_srv_bcknd
