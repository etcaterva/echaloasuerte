![EchaloASuerte](https://raw.githubusercontent.com/etcaterva/EchaloASuerte/master/static/img/brand/brand_es.png) / ![ChooseRandom](https://raw.githubusercontent.com/etcaterva/EchaloASuerte/master/static/img/brand/brand_en.png)
=============
Echaloasuerte/ChooseRandom is a simple website that allows people to take
decisions base on random factors.

It gives you random numbers, chose an random element from a list, flip a coin to
the air, etc... and one of the nicest features is that several people can see
the result at the same time, which make the site great to perform draws with
people that are not physically together.

This version is a rewrite of the old site.

## Deployment
- [Dev](https://dev.chooserandom.com)
- [Prod](https://chooserandom.com)

The dev version is on continuous deployment, all changes in master are
automatically deployed to dev

## DNS
 - www.echaloasuerte.com: Root domain for the spanish version
 - www.chooserandom.com: Root domain for the english version
 - prod.*: latest version deployed to the prod server
 - dev.*: latest version deployed to the dev server

All domains can be accessed through http and https and are served through
cloudflare.

## CI builds
- Travis: [![Travis Master](https://travis-ci.org/etcaterva/EchaloASuerte.svg?branch=master)](https://travis-ci.org/etcaterva/EchaloASuerte)
- CI: [![Jenkins CI](http://92.222.219.42:8080/job/Echaloasuerte-DEV-CI/badge/icon)](http://92.222.219.42:8080/job/Echaloasuerte-DEV-CI/)
- CD: [![Jenkins CD](http://92.222.219.42:8080/job/Echaloasuerte-DEV-Deploy/badge/icon)](http://92.222.219.42:8080/job/Echaloasuerte-DEV-Deploy)

## Acknowledgements
* Selenium tests running on [BrowserStack](www.browserstack.com)

## How to create a new draw
* Define a bom within server/bom and add it to the __init__
* Define a form within server/forms and add it to the __init__
* Add the draw snippet in web/templates/snippets/draws
* Add the callback to render the results dynamically in draw_manager.js
* Register the draw, form and snippet within the draw factory
  (server/draw_factory)
* Get an icon for it into static/img/draw_icons
* Add the draw to the index menu (web/template/index.html)
* if you need extra js, add a file and include it in the new and display
  templates
* Add unit and functional tests
