# Robotics and Design project - a.a. 2021-2022
Make a wearable robot able to engage interactions with third people.

<img src="Documentation/A.N.D.I..png" />

## How to run the project
1. Clone the repository
    ```bash
    git clone {repository URL}
    ```

2. Upload the [main](/main/) on your RaspberryPi.

3. Run `python3 main.py`.

## Abstract
We present you A.N.D.I., the Angel aNd Devil Interactor. This robot is our project for the Robotics and Design 2022 Polimi course, built following the assignment in which we were asked to create a wearable robot capable of interacting with the wearer and a third-party actor which we identified as a child. A.N.D.I. is based on the concept of the secondary character which is often found in comedy shows, and which plays the role of dualism fighting between the good and the evil side of the conscience. We realised this idea as a jacket, mounting two movable heads on the shoulders, the angel being on the right and the devil on the left. The robot is able to react to different types of interactions by showing different emotions through movements, mounting three servo motors per head, and completed by sound, coming from a speaker per side. In particular, it can be petted thanks to a capacitive sensor, it can recognize spoken keywords with the use of a microphone and detect the distance to the third actor through two ultrasonic sensors. It can also start acting on its own with random behaviours completed by dialogue to fill up the silence. All of these features are managed by a Raspberry Pi, placed on the back of the jacket, and powered by a portable power bank.

## Electronics organization
Here are reported the wiring schema of the robot.

Built around a `Raspberry Pi 4B`, a `Raspberry Pi Protoboard` and an `Adafruit Stereo Speaker Bonnet`.

Input:
- 1 button
- 1 microphone
- 1 capacitive sensor
- 2 sonar sensors

Output:
- 2 speakers
- 6 servo motors

<img src="Documentation/Circuit diagram.png" />

## Code organization
We wrote the code to test each electronic component independently in order to better understand their behaviour. We have programmed in Python since we are using a RaspberryPi.
The code of the tests can be seen in the folder [test](/test/).

The final code is in the [main](/main/) folder.

## Team
### Engineers

* __Giorgia Martelli__
* [__Tommaso Pozzi__](https://github.com/ToMmAzO)
* __Mehavannen Prabakaran__

### Designers

* __Erica Ceriotti__
* __Jacopo Ottaviani__
