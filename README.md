<h1 align="center">
  <br>
  🚀
  <br>
  Spaceship Battle
  <br>
</h1>

<h4 align="center">A multi-user input space shooting game</h4>

A single-player game where you control the spaceship using your eyes, fingers,
and mouse.<br>

**Source:** https://github.com/farisdurrani/CS6456Project <br>
**Authors:** [Faris Durrani](https://github.com/farisdurrani/),
[Rishabh Ghora](https://github.com/RishabhGhora)

## How to run

1. Create python virtual env with Python >= 3.7. `python3.7 -m venv venv`
2. Install the dependencies. `pip install -r requirements.txt`
3. Run. `python spaceship_battle.py`

Note: This project is meant to run on a Windows machine with webcam and touchscreen, please use 'windows' branch if this applies.

If you have a mac without a touchscreen and would like to run the game just for the eye tracking features please clone the
master branch.

## Main libraries (from `requirements.txt`)

1. cmake
2. dlib==19.16.0
3. numpy==1.16.1
4. opencv_python==4.5.4.58
5. pygame==2.1.0

## How to play

### Eye Gaze for Main Control

![](readme_assets/play_general.gif)
Use your eyes to move the ship around. The program tracks the coordinates of
your right eye and translates those coordinates to positions on the game screen,
where the spaceship (center, in white) will be pointed at.

Evil ships (in red) will continuously attack you until they are out of range
or until they die.

### One Finger Controls

This game also allows finger gestures (some systems detect a mouse pointer to
be equivalent to a single finger gesture).

#### Left (<)

![](readme_assets/left.gif)
Using a finger, a user can draw a "<" symbol anywhere on the screen to pull up
the settings. You can change the color of the spaceship's bullet by clicking on
the button (using your mouse or your finger). The program recognizes the shape
by employing a 9-square recognizer.

#### Right (>)

![](readme_assets/right.gif)
Using a finger, a user can draw a "<" symbol anywhere on the screen to pull up
friends to request support from. These friends are blue with the same health
as evil ships. Their behavior is random.

#### Up (^)

![](readme_assets/up.gif)
Using a finger, a user can draw a "^" symbol anywhere on the screen to pull up
the market. The market is filled with random items with random prices
(within appropriate ranges). Hence, the user can benefit from trading by buying
when prices are low and selling when high. Additionally, the market provides
shield and bullet power to upgrade the ship. Shields are temporary as
described below.

#### Shield (O)

![](readme_assets/shield.gif)
Using a finger, a user can draw an "O" symbol anywhere on the screen to make a
temporary shield around the spaceship (assuming at least one shield has been
bought). While the shield is up, no damage will be sustained.

#### Strike (/)

![](readme_assets/strike.gif)
Using a finger, a user can draw an "/" symbol over an asteroid to destroy it
before it hits the ship

### Four finger control

#### Slide to first view (or vice versa)

![](readme_assets/view.gif)
Using four fingers, a user can slide their fingers over the screen to change
the view from third-person view to first-person view, and vice versa. The
spaceship's bullets will deviate slightly to the left or to the right to
show the ship's rotation.

The first-person view depends on the third-person
view, i.e., the eye's coordinates determines where the ship points to in
first-person view and this is translated to third-person view to see if the
ship is turning right or left. The first-person view only sees the 180
degrees view in front of the ship.

## Attribution

Almost all the code are original with only a small number of borrowed code from
StackOverflow or other code-sharing platforms for less intuitive mathematical or
Pygame operations. They are included below.

1. [Calculating if ship is within the 180-degree angle of view](https://stackoverflow.com/a/12234633/11031425)
2. [Translucent Pygame Surfaces](https://stackoverflow.com/a/6350227/11031425)
3. [Translucent Pygame circle](https://stackoverflow.com/a/64630102/11031425)
4. [Calculating Euclidean distance](https://docs.python.org/3/library/math.html)
5. [Drawing with fingers on Pygame](https://www.patreon.com/posts/finger-painting-43786073?l=fr)

## Creative Commons

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.

## References

1. Inspiration: https://github.com/LukeGarrigan/spaceheir
