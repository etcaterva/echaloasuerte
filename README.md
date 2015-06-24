EchaloASuerte
=============
Echaloasuerte is a simple website that allows people to take decisions base on random factors.

This version is a rewrite of the oldsite.

## Deployment
- [Dev](http://dev.echaloasuerte.com)
- [Prod](http://prod.echaloasuerte.com)

The dev version is on continuous deployment, all changes in master are automatically deployed to dev

## DNS
 - www.echaloasuerte.com: Root domain for the spanish version
 - www.pickforme.net: Root domain for the english version
 - prod.*: latest version deployed to the prod server
 - dev.*: latest version deployed to the dev servier
  
All domains can be accessed through http and https and are served through cloudflare. 

## CI builds
[![Travis Build Status](https://travis-ci.org/etcaterva/EchaloASuerte.svg?branch=master)](https://travis-ci.org/etcaterva/EchaloASuerte)
[![Jenkins Build Status](http://92.222.219.42:8080/buildStatus/icon?job=Echaloasuerte-DEV-CI)](http://92.222.219.42:8080/job/Echaloasuerte/)
