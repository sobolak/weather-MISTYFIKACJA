import interia
import avenue
import weatherChannel
import onet
import wp
import metroprog

interia_hrefs = {'https://pogoda.interia.pl/prognoza-szczegolowa-krakow-plaszow,cId,26191':'agh'}
avenue_hrefs = {'https://www.weatheravenue.com/pl/europe/pl/krakow/plaszow-hourly.html':'agh'}
weatherChannel_hrefs = {'https://weather.com/weather/hourbyhour/l/e3172e6c71e631465847a819d8297d8cdb704d4662cb72af0699e437144d6980':'agh'}
onet_hrefs = {'https://pogoda.onet.pl/prognoza-pogody/maly-plaszow-315521':'agh'}
wp_hrefs = {'https://pogoda.wp.pl/pogoda-na-dzis/krakow/3094802':'agh'}
metroprog_hrefs = {'https://www.meteoprog.pl/pl/meteograms/Podgorzemalopolska/':'agh'}

interia.main(interia_hrefs)
avenue.main(avenue_hrefs)
weatherChannel.main(weatherChannel_hrefs)
onet.main(onet_hrefs)
wp.main(wp_hrefs)
metroprog.main(metroprog_hrefs) 