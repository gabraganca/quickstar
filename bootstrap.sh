#!/usr/bin/env sh

mkdir -p bstar2006
wget -c http://tlusty.oca.eu/Tlusty2002/database/BGmodels_v2.tar
tar -xf  BGmodels_v2.tar -C bstar2006/
gunzip bstar2006/*
wget -c http://tlusty.oca.eu/Tlusty2002/database/atom_BS06.tar
tar -xf atom_BS06.tar
mv data atdata
gunzip atdata/*
rm BGmodels_v2.tar
rm atom_BS06.tar