# Sensory-Transparency

This was a project to explore research of robots communicating sensor transparency to human partners. This project is meant to be deployed on the Baxter robot with a kinect camera to detect body pose, a microphone for the user, as well as Ein on the robot to display images/activate LEDs.

How the program works is you walk up to the Baxter robot, and have the ability to speak and point at the table in front of you. As you talk, an online speech-to-text parser estimates words and makes Baxter LED head ring turn on and off to indicate that it is hearing words from the human. Whenever the user lifts their arm past a certain angle threshold, the kinect will detect this and cause Baxter's screen to display a video of a robot face looking around, to indicate that the robot sees the human pointining.

These additions on top of the sensors are extremely simple, which allow them to be deployed in real-time. However, these small additions to the robot make it extremely transparent to the human when the robot is able to hear the human (if the human is speaking too softly into the mic, they won't see lights appear on the head), or if the robot is able to see where they're pointing (if the kinect has lost track of the human skeleton, the human will notice the robot doesn't see where they are pointing since the video does not play).
