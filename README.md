# Self Driving Car

What do you do with a [Vaporizr 360](https://www.youtube.com/watch?v=WWDg4KFKr28) when its RC receiver dies? You rip the electronics out, replace them with a digital motor driver and a Raspberry Pi, and make a self-driving car of course!

That's the idea anyway. I know almost nothing about computer vision so it's a chance to play and learn in a fun real-life way instead of just stuff on a screen. So far I've built the drive circuit and code to provide variable-speed motor control via PWM, and I'm experimenting with contour detection in OpenCV. The idea is to recognise a shape and have the car turn and drive towards it.

Limitations so far are that the Raspberry Pi model 3 only manages 9-10 frames per second image analysis. Add in some multi-frame averaging to smooth the data and it's quite slow at reacting. But it can (sort of) follow a big blue X on a bit of paper if you hold it relatively still.