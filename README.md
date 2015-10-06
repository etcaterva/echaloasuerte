![EchaloASuerte](https://raw.githubusercontent.com/etcaterva/EchaloASuerte/master/static/img/brand/brand_es.png) / ![ChooseRandom](https://raw.githubusercontent.com/etcaterva/EchaloASuerte/master/static/img/brand/brand_en.png)
=============
Echaloasuerte/ChooseRandom is a simple website that allows people to take decisions base on random factors.

It gives you random numers, chose an random element from a list, flip a coin to the air, etc... and one of the nicest features is that several people can see the result at the same time, which make the site great to perform draws with people that are not phisically together.

This version is a rewrite of the oldsite.

## Deployment
- [Dev](http://dev.echaloasuerte.com)
- [Prod](http://prod.echaloasuerte.com)

The dev version is on continuous deployment, all changes in master are automatically deployed to dev

## DNS
 - www.echaloasuerte.com: Root domain for the spanish version
 - www.chooserandom.com: Root domain for the english version
 - prod.*: latest version deployed to the prod server
 - dev.*: latest version deployed to the dev servier
  
All domains can be accessed through http and https and are served through cloudflare. 

## CI builds
- Travis: [![Travis Master](https://travis-ci.org/etcaterva/EchaloASuerte.svg?branch=master)](https://travis-ci.org/etcaterva/EchaloASuerte)
- CI: [![Jenkins CI](http://92.222.219.42:8080/job/Echaloasuerte-DEV-CI/badge/icon)](http://92.222.219.42:8080/job/Echaloasuerte-DEV-CI/)
- CD: [![Jenkins CD](http://92.222.219.42:8080/job/Echaloasuerte-DEV-Deploy/badge/icon)](http://92.222.219.42:8080/job/Echaloasuerte-DEV-Deploy)

## Acknowledgements
* Selenium tests running on [BrowserStack](www.browserstack.com)
