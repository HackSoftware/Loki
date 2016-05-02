#!/bin/bash

read -p "Do you want to import all cities?" -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
  python3 -W ignore manage.py loadfixtures cities.json
fi

read -p "Do you want to import all universities, faculties and subects?" -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
  python3 -W ignore manage.py loadfixtures universities_in_bulgaria.json
  
  python3 -W ignore manage.py loadfixtures sofia_university_faculties.json
  python3 -W ignore manage.py loadfixtures htmu_faculties.json
  python3 -W ignore manage.py loadfixtures ltu_faculties.json
  python3 -W ignore manage.py loadfixtures mgu_faculties.json
  python3 -W ignore manage.py loadfixtures mvr_faculties.json
  python3 -W ignore manage.py loadfixtures natfiz_faculties.json
  python3 -W ignore manage.py loadfixtures nha_faculties.json
  python3 -W ignore manage.py loadfixtures nma_faculties.json
  python3 -W ignore manage.py loadfixtures nsa_faculties.json
  python3 -W ignore manage.py loadfixtures tu_sofia_faculties.json
  python3 -W ignore manage.py loadfixtures uasg_faculties.json
  python3 -W ignore manage.py loadfixtures ubit_faculties.json
  python3 -W ignore manage.py loadfixtures unwe_faculties.json
  python3 -W ignore manage.py loadfixtures va_sofia_faculties.json
  python3 -W ignore manage.py loadfixtures vsu_sofia_faculties.json
  python3 -W ignore manage.py loadfixtures vtu_sofia_faculties.json
  
  python3 -W ignore manage.py loadfixtures subjects_in_fmi.json

fi

read -p "Do you want to import all academies?" -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
  python3 -W ignore manage.py loadfixtures academies_in_bulgaria.json
fi


read -p "Do you want to import all schools?" -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
  python3 -W ignore manage.py loadfixtures schools/schools_from_asenovgrad.json
  python3 -W ignore manage.py loadfixtures schools/schools_from_blagoevgrad.json
  python3 -W ignore manage.py loadfixtures schools/schools_from_botevgrad.json
  python3 -W ignore manage.py loadfixtures schools/schools_from_burgas.json
  python3 -W ignore manage.py loadfixtures schools/schools_from_dimitrovgrad.json
  python3 -W ignore manage.py loadfixtures schools/schools_from_dobrich.json
  python3 -W ignore manage.py loadfixtures schools/schools_from_dupnitsa.json
  python3 -W ignore manage.py loadfixtures schools/schools_from_gabrovo.json
  python3 -W ignore manage.py loadfixtures schools/schools_from_gorna_oryahovitsa.json
  python3 -W ignore manage.py loadfixtures schools/schools_from_harmanli.json
  python3 -W ignore manage.py loadfixtures schools/schools_from_haskovo.json
  python3 -W ignore manage.py loadfixtures schools/schools_from_kardzhali.json
  python3 -W ignore manage.py loadfixtures schools/schools_from_karlovo.json
  python3 -W ignore manage.py loadfixtures schools/schools_from_karnobat.json
  python3 -W ignore manage.py loadfixtures schools/schools_from_kazanlak.json
  python3 -W ignore manage.py loadfixtures schools/schools_from_kiustendil.json
  python3 -W ignore manage.py loadfixtures schools/schools_from_lovech.json
  python3 -W ignore manage.py loadfixtures schools/schools_from_montana.json
  python3 -W ignore manage.py loadfixtures schools/schools_from_nova_zagora.json
  python3 -W ignore manage.py loadfixtures schools/schools_from_pazardzhik.json
  python3 -W ignore manage.py loadfixtures schools/schools_from_pernik.json
  python3 -W ignore manage.py loadfixtures schools/schools_from_peshtera.json
  python3 -W ignore manage.py loadfixtures schools/schools_from_petrich.json
  python3 -W ignore manage.py loadfixtures schools/schools_from_pleven.json
  python3 -W ignore manage.py loadfixtures schools/schools_from_plovdiv.json
  python3 -W ignore manage.py loadfixtures schools/schools_from_razgrad.json
  python3 -W ignore manage.py loadfixtures schools/schools_from_ruse.json
  python3 -W ignore manage.py loadfixtures schools/schools_from_samokov.json
  python3 -W ignore manage.py loadfixtures schools/schools_from_shumen.json
  python3 -W ignore manage.py loadfixtures schools/schools_from_silistra.json
  python3 -W ignore manage.py loadfixtures schools/schools_from_sliven.json
  python3 -W ignore manage.py loadfixtures schools/schools_from_smolyan.json
  python3 -W ignore manage.py loadfixtures schools/schools_from_sofia.json
  python3 -W ignore manage.py loadfixtures schools/schools_from_stara_zagora.json
  python3 -W ignore manage.py loadfixtures schools/schools_from_svilengrad.json
  python3 -W ignore manage.py loadfixtures schools/schools_from_svishtov.json
  python3 -W ignore manage.py loadfixtures schools/schools_from_targovishte.json
  python3 -W ignore manage.py loadfixtures schools/schools_from_troyan.json
  python3 -W ignore manage.py loadfixtures schools/schools_from_varna.json
  python3 -W ignore manage.py loadfixtures schools/schools_from_veliko_tarnovo.json
  python3 -W ignore manage.py loadfixtures schools/schools_from_velingrad.json
  python3 -W ignore manage.py loadfixtures schools/schools_from_vidin.json
  python3 -W ignore manage.py loadfixtures schools/schools_from_vratsa.json
  python3 -W ignore manage.py loadfixtures schools/schools_from_yambol.json
fi
