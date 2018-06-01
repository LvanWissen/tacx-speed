# tacx-speed
Use a CNY70 sensor to display bike trainer speed on webserver by raspberry pi

## Description

You bought yourself a Tacx or any other bike trainer and, because your speed hall sensor is fitted on your front wheel, you have absolutely no idea of your indoor speed. Then why not use a CNY70 (reflective IR-sensor) to measure this? 

Using a raspberry pi in combination with a python web framework is probably not the best or fastest way to measure this, but it is an easy DIY one. The speed and quality of the sensor readings are dependent on the speed of the pi (or any other board with a similar GPIO numbering I suppose). A speed reading is only triggered in a rising of the pin state. 

Every client that connects to the website (Flask ftw) is able to alter the resistance settings (through a websocket). That way, you can use your phone as a remote control and your computer monitor to display the dashboard (incl. graph). 

It maybe takes some time before you have figured out the best resistance values and distance to your rear wheel. You may find that it does not read at all. Then using a small piece of tin foil stuck to your wheel might help. 

### Schematics

### Screenshots


