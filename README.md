# PANTONEColorRandomizer

## Demo
Demo Video: <URL>

## GitHub Repository
GitHub Repo: https://github.com/NathalieVal/PANTONEColorRandomizer

## Description

NOTE: THIS PROGRAM IS NOT AFFILIATED WITH PANTONE.

PANTONEColorRandomizer is a color randomizer program based on the actual catalogue for PANTONE Solid Coated colors.

The program is meant to be a different way to randomize colors from a well known company within the design world. It's made with digital artists in mind, taking into consideration that designers may want to get the RGB values of the color that they're actively viewing. By clicking on the name of the color on the color card (which is supposed to mimic a PATONE color card), the program opens a window on the user's default browser to the color on the official PANTONE website.

I added an intro scene that displays a stylized version of PANTONE's logo. This scene can be sped up by clicking on the screen. It wasn't really needed, and if anything it may slow down the usage of what is already a very simple program, but I personally like to hear the music start before the main menu appears.

Speaking of music, the program also has SFX and audio to accompany it. Initially there was going to be much more going on in terms of visuals and audio, but due to time constraints and a general lack of artistic direction, I ended up making everything very simple and clean. I feel like this worked for the better at the end, because now it feels like a much calmer experience. The music is also great background noise in my opinion.

The entire program is built with each scene being a different class. This allowed me to create a SceneManager class where transitions can be handled between scenes. In this case, the buttons slide to the left and the new scenes fade into the screen. Previously, I didn't even know that classes could be used like this, and was just leaving everything outside in the wild (at this point I didn't even have a Main class yet), but once I had the idea to create transitions between scenes I had to look up how to do it.

This entire program is built around PANTONE's color swatches simply because I was thinking about them when I first came up with the idea. I do prefer that I went this route instead of just making a random color generator as it allowed me to play around with exporting data outside of a csv file and into my own program. I feel like this was a much more enjoyable way to program the randomizer over simply creating random RGB values everytime. 

The program itself is really simple with one core function (select a random color out of a list) but that was intentional. It may be under scope in comparison to my original proposal, but I felt like a lot of the complexity came from the way that I ended up presenting the color through the animations, transitions, and audio. Even if it is under scope I can at least say that I had a lot of fun making it, and that I learned a lot from this experience.