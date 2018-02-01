#!/bin/bash

git clone https://jkleinerman@github.com/kleinerman/dobie.git
cd dobie
git config --global user.email "jkleinerman@gmail.com"
git config --global user.name "Jorge Kleinerman"
git config --global core.editor "vim"
git remote rename origin github
git remote add bitbucket https://jkleinerman@bitbucket.org/kleinerman/dobie.git
git fetch github jek_srv_bcknd:jek_srv_bcknd
git checkout jek_srv_bcknd
