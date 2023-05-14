# Bachelor-Thesis-Project
Project made for Bachelor's Thesis

0.Open 1883(mqtt, tcp/udp) for mqtt, 5000(udp) for video stream

1.Clone the files,
  -Controller to any device that takes keyboard input (just use your laptop or pc)
  -SensorPlatform to RaspberryPi or adjacent device (tested on RPi 4, refer to wiring diagram for components)

2.Install missing libraries and dependencies(check docs)

3.Setup an mqtt broker

4.Set Controller and SensorPlatform to connect to the broker (.ini or mqttClient configs in code)

5.Run Controller and SensorPlatform from main.py


Mobile Sensor Platform wiring diagram
![platformWiringDiagram](https://github.com/Akakria/Bachelor-Thesis-Project/assets/43040626/5fe0d9f6-7613-4db7-bf78-5ede4c0b5988)

Simplified data flow diagram (does not cover all dataflow, but the principle is the same)
![simplifiedDataFlow](https://github.com/Akakria/Bachelor-Thesis-Project/assets/43040626/cb6bdfed-889b-4ec1-9039-cc5cfe1d4cb3)
