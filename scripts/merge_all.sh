#!/bin/bash

git clone https://jkleinerman@github.com/kleinerman/dobie.git
cd dobie
git config --global user.email "jkleinerman@gmail.com"
git config --global user.name "Jorge Kleinerman"
git config --global core.editor "vim"
git remote rename origin github
git remote add bitbucket https://jkleinerman@bitbucket.org/kleinerman/dobie.git

read -p "git fetch github jek_srv_bcknd:jek_srv_bcknd:?"
git fetch github jek_srv_bcknd:jek_srv_bcknd

read -p "git fetch github jek_controller:jek_controller:?"
git fetch github jek_controller:jek_controller

read -p "git fetch github jek_docs:jek_docs:?"
git fetch github jek_docs:jek_docs

read -p "git fetch github ary_srv_bcknd:ary_srv_bcknd:?"
git fetch github ary_srv_bcknd:ary_srv_bcknd

read -p "git fetch github ary_controller:ary_controller:?"
git fetch github ary_controller:ary_controller

read -p "git fetch github gaf_srv_frntnd:gaf_srv_frntnd:?"
git fetch github gaf_srv_frntnd:gaf_srv_frntnd




read -p "git branch:?"
git branch

read -p "git merge jek_srv_bcknd:?"
git merge jek_srv_bcknd

read -p "git merge jek_controller:?"
git merge jek_controller

read -p "git merge jek_docs:?"
git merge jek_docs

read -p "git merge gaf_srv_frntnd:?"
git merge gaf_srv_frntnd

read -p "git push github master:?"
git push github master

read -p "git push bitbucket master:?"
git push bitbucket master




read -p "git checkout jek_srv_bcknd:?"
git checkout jek_srv_bcknd

read -p "git branch:?"
git branch

read -p "git merge master:?"
git merge master

read -p "git push github jek_srv_bcknd:?"
git push github jek_srv_bcknd

read -p "git push bitbucket jek_srv_bcknd:?"
git push bitbucket jek_srv_bcknd




read -p "git checkout jek_controller:?"
git checkout jek_controller

read -p "git branch:?"
git branch

read -p "git merge master:?"
git merge master

read -p "git push github jek_controller:?"
git push github jek_controller

read -p "git push bitbucket jek_controller:?"
git push bitbucket jek_controller





read -p "git checkout jek_docs:?"
git checkout jek_docs

read -p "git branch:?"
git branch

read -p "git merge master:?"
git merge master

read -p "git push github jek_docs:?"
git push github jek_docs

read -p "git push bitbucket jek_docs:?"
git push bitbucket jek_docs





read -p "git checkout ary_srv_bcknd:?"
git checkout ary_srv_bcknd

read -p "git branch:?"
git branch

read -p "git merge master:?"
git merge master

read -p "git push github ary_srv_bcknd:?"
git push github ary_srv_bcknd

read -p "git push bitbucket ary_srv_bcknd:?"
git push bitbucket ary_srv_bcknd





read -p "git checkout ary_controller:?"
git checkout ary_controller

read -p "git branch:?"
git branch

read -p "git merge master:?"
git merge master

read -p "git push github ary_controller:?"
git push github ary_controller

read -p "git push bitbucket ary_controller:?"
git push bitbucket ary_controller





read -p "git checkout gaf_srv_frntnd:?"
git checkout gaf_srv_frntnd

read -p "git branch:?"
git branch

read -p "git merge master:?"
git merge master

read -p "git push github gaf_srv_frntnd:?"
git push github gaf_srv_frntnd

read -p "git push bitbucket gaf_srv_frntnd:?"
git push bitbucket gaf_srv_frntnd

