<!-- TOC
- Contents (p.4)
- Foreword (p.7)
- Acknowledgments (p.8)
- About the Authors (p.8)
- Who This Book Is For (p.9)
- Getting Started (p.10)
- Introducing Blackmagic Cloud (p.21)
- Getting Started: Learning the Fusion Page (p.22)
  - Exploring the Fusion Interface  (p.23)
  - Combining Images Using Nodes (p.30)
  - Adding Effects (p.34)
  - Understanding Node Flow (p.38)
  - Working with Masks (p.41)
  - Secondary Color Correction (p.43)
  - Animating with Keyframes (p.48)
  - Adding a Vignette (p.49)
  - Returning to the Timeline (p.50)
  - Lesson Review (p.50)
- Compositing Split Screens (p.52)
  - Using Layers from the Edit Page (p.53)
  - Tracking in the Fusion Page (p.58)
  - Drawing a Matte (p.65)
  - Aligning the Clips Using Nudging (p.71)
  - Restoring Camera Motion (p.74)
  - Lesson Review (p.78)
- Replacing a Sky (p.80)
  - Retaining a Clip’s Resolution (p.81)
  - Controlling a Composition’s Resolution  (p.85)
  - Compositing Using the Darken Apply Mode  (p.90)
  - Adding Effects from the Effects Library  (p.92)
  - Fixing Holes in a Key (p.95)
  - Embedding Alpha into an Image (p.96)
  - Tracking the Sky into Position (p.99)
  - Fixing Interrupted Trackers (p.103)
  - Blending In the Original Sky (p.104)
  - Lesson Review (p.106)
- Replacing Signs and Screens (p.108)
  - Tracking Planar Surfaces (p.109)
  - Painting with the Clone Tool (p.114)
  - Using Photoshop PSD Layers (p.117)
  - Combining Mattes and Images (p.123)
  - Match Moving with the Planar Transform (p.125)
  - Finalizing the Composite (p.127)
  - Lesson Review (p.130)
- Compositing Green‑Screen Content (p.132)
  - Creating a Clean Plate (p.133)
  - Fine-Tuning with the Delta Keyer (p.136)
  - Rotoscoping Auxiliary Mattes (p.141)
  - Lining Up the Background (p.150)
  - Color Correcting Elements (p.152)
  - Sending a Matte to the Color Page  (p.155)
  - Lesson Review (p.158)
- Addendum: Creating Title Animations (p.160)
  - Styling Text in the Edit Page (p.161)
  - Moving Text to the Fusion Page (p.166)
  - Creating a Background Banner (p.168)
  - Revealing Text with Mattes (p.172)
  - Animating with the Follower (p.174)
  - Adjusting Keyframe Timing  (p.178)
  - Trying Out Versions (p.182)
  - Saving a Template (p.184)
  - Lesson Review (p.188)
- Addendum: Animating with Keyframes and Modifiers (p.190)
  - Identifying a Clip’s Resolution (p.191)
  - Keyframing a Motion Path (p.192)
  - Auto-Orienting Objects (p.197)
  - Straightening Out Alpha Channels  (p.198)
  - Painting a Motion Path (p.199)
  - Linking Parameters (p.203)
  - Making Acceleration Adjustments (p.206)
  - Applying Random Animation Modifiers  (p.208)
  - Customizing Motion Blur (p.210)
  - Lesson Review (p.212)
- Index (p.214)
-->
## The Visual Effects Guide to


**The Visual Effects Guide to DaVinci Resolve 20**


Damian Allen, Tony Gallardo, and Dion Scoppettuolo


© 2025 by Blackmagic Design Pty Ltd


Blackmagic Design


[www.blackmagicdesign.com](http://www.blackmagicdesign.com)


[To report errors, please send a note to learning@blackmagicdesign.com.](mailto:learning%40blackmagicdesign.com?subject=)


Series Editor: Klark J. Perez


Editor: Dan Foster


Cover Design: Blackmagic Design


Layout: Blackmagic Design, Danielle Foster


**Notice of Rights**


All rights reserved. No part of this book may be reproduced or transmitted in any form by any means, electronic,

mechanical, photocopying, recording, or otherwise, without the prior written permission of the publisher.

[For information on getting permission for reprints and excerpts, contact learning@blackmagicdesign.com.](mailto:learning%40blackmagicdesign.com?subject=)


**Notice of Liability**


Neither the author nor Blackmagic Design shall have any liability to any person or entity for any loss or damage

caused or alleged to be caused directly or indirectly by the information contained in this book, or by omissions

from this book, or by the computer software and hardware products described within it.


**Trademarks**


Many of the designations used by manufacturers and sellers to distinguish their products are claimed as trademarks.

Where those designations appear in this book, and Blackmagic Design was aware of a trademark claim, the

designations appear as requested by the owner of the trademark. All other product names and services identified

throughout this book are used in editorial fashion only and for the benefit of such companies with no intention of

infringement of the trademark. No such use, or the use of any trade name, is intended to convey endorsement or

other affiliation with this book.


(Mac) and (macOS) are registered trademarks of Apple Inc., registered in the U.S. and other countries. Windows is

aregistered trademark of Microsoft Inc., registered in the U.S. and other countries.


ISBN 13: 979-8-9924874-4-2


## **Contents**

Foreword vi


Acknowledgments vii


About the Authors vii


Who This Book Is For viii


Getting Started ix


Introducing Blackmagic Cloud xx


1 Getting Started: Learning the Fusion Page 1


Exploring the Fusion Interface 2


Combining Images Using Nodes 9


Adding Effects 13


Understanding Node Flow 17


Working with Masks 20


Secondary Color Correction 22


Animating with Keyframes 27


Adding a Vignette 28


Returning to the Timeline 29


Lesson Review 29


2 Compositing Split Screens 31


Using Layers from the Edit Page 32


Tracking in the Fusion Page 37


Drawing a Matte 44


Aligning the Clips Using Nudging 50


Restoring Camera Motion 53


Lesson Review 57


**Contents** **iii**


3 Replacing a Sky 59


Retaining a Clip’s Resolution 60

Controlling a Composition’s Resolution 64

Compositing Using the Darken Apply Mode 69

Adding Effects from the Effects Library 71

Fixing Holes in a Key 74

Embedding Alpha into an Image 75

Tracking the Sky into Position 78

Fixing Interrupted Trackers 82

Blending In the Original Sky 83

Lesson Review 85


4 Replacing Signs and Screens 87


Tracking Planar Surfaces 88

Painting with the Clone Tool 93

Using Photoshop PSD Layers 96

Combining Mattes and Images 102

Match Moving with the Planar Transform 104

Finalizing the Composite 106

Lesson Review 109


5 Compositing Green‑Screen Content 111


Creating a Clean Plate 112

Fine-Tuning with the Delta Keyer 115

Rotoscoping Auxiliary Mattes 120

Lining Up the Background 129

Color Correcting Elements 131

Sending a Matte to the Color Page 134

Lesson Review 137


**Contents** **iv**


6 Addendum: Creating Title Animations 139


Styling Text in the Edit Page 140

Moving Text to the Fusion Page 145

Creating a Background Banner 147

Revealing Text with Mattes 151

Animating with the Follower 153

Adjusting Keyframe Timing 157

Trying Out Versions 161

Saving a Template 163

Lesson Review 167


7 Addendum: Animating with Keyframes and Modifiers 169


Identifying a Clip’s Resolution 170

Keyframing a Motion Path 171

Auto-Orienting Objects 176

Straightening Out Alpha Channels 177

Painting a Motion Path 178

Linking Parameters 182

Making Acceleration Adjustments 185

Applying Random Animation Modifiers 187

Customizing Motion Blur 189

Lesson Review 191


Index 193


**Contents** **v**


## **Foreword**

**Welcome to The Visual Effects Guide to DaVinci Resolve 20.**


DaVinci Resolve 20 is the only post-production solution that combines editing, color

correction, visual effects, motion graphics, and audio post-production all in one software

tool! Its elegant, modern interface is fast to learn for new users yet powerful enough for

the most experienced professionals. DaVinci Resolve lets you work more efficiently

because you don’t have to learn multiple apps or switch software for different tasks. It’s

like having your own post-production studio in a single app!


DaVinci Resolve 20 adds editing with transcriptions from audio, film look creator and

ColorSlice six vector grading, IntelliTrack AI for panning audio to match vision, and

broadcast replay for live multi camera broadcast editing, layout and replay with speed

control, and so much more!


Best of all, Blackmagic Design offers a version of DaVinci Resolve 20 that is completely free!

We’ve made sure that this version of DaVinci Resolve includes more features than any paid

editing system. That’s because at Blackmagic Design we believe everybody should have

the tools to create professional, Hollywood-caliber content without having to spend

thousands of dollars.


I invite you to download your copy of DaVinci Resolve 20 today and look forward to seeing

the amazing work you produce!


Grant Petty

Blackmagic Design


**Foreword** **vi**


## **Acknowledgments**

We would like to thank the following individuals for their contributions of media used

throughout the book:


- Hasraf “HaZ” Dulull, for the sci-fi short film _SYNC_ . Produced, written, and directed by

Hasraf Dulull.

- Rafa Garcia, for the VAN clip. Directed and edited by Rafa Garcia. Property of Rafa

Garcia Films.

- Lukas Colombo, for the Steve Val: Dark Matter music video. Visual effects supervisor

Nic Torres. Property of Moai Films.

- Sherwin Lau, Creative Media Institute for the short film _Driver’s Ed_ .

- Kauai Film Academy ( _[www.kauaifilmacademy.org](http://www.kauaifilmacademy.org)_ ) for _Too Much Life_ : The Movie.
## **About the Authors**


**Damian Allen** is a visual effects and animation consultant, developer, and supervisor

in Hollywood. He is the owner of the VFX company Pixerati LLC, with a focus on virtual

production, picture-lock visual effects emergencies, and VR and animation tool development.

Damian is also a core contributor to the [moviola.com](http://moviola.com) training site for filmmakers.


**Tony Gallardo**, ever since picking up his first VHS camera, has been hooked and cut his

teeth at a very early age making short films and promo videos for his school and church.

A story editor from the start, Tony quickly expanded to all aspects of post-production and

production. From designing award-winning motion graphics to directing tear jerking

real-life stories, his passion for the craft and tools is endless. After co-running an award
winning production facility in San Antonio, Texas for a little over 14 years, he branched out

and now runs his own post boutique, Tomiga. Tomiga is a hybrid creative boutique

focusing on short form content from brand commercials to informative PSAs to

promotional media. When he’s not creating brand commercial campaigns or social media

ads, Tony is learning and educating about all his favorite creative tools—with Davinci

Resolve and Fusion at the top of his list.


**Dion Scoppettuolo** is a Certified Blackmagic Design Master Trainer. He has taught classes

on DaVinci Resolve in Hollywood and New York City, as well as across Europe and Asia.

Mr Scoppettuolo has extensive industry experience in editing and visual effects, having

held the position of Senior Product Manager for Pro Applications at Apple Inc.


**About the Authors** **vii**


## **Who This Book Is For**

This hands-on training guide is designed for DaVinci Resolve editors and colorists who

want to create visual effects and motion graphics in DaVinci Resolve 20. The lessons in this

book provide a solid foundation for creating visual effects in the Fusion page. An addendum

is provided to give you an understanding of how to begin creating motion graphics.


You’ll start with an introductory composite that will give you a quick overview of the Fusion

page interface and how nodes work. Each subsequent lesson builds your skills in the

fundamentals of visual effects. You’ll cover a variety of genres, techniques, and technical

best practices including split screens, sign replacement, and green-screen compositing.

All the lessons in this guide can be completed using the free download of DaVinci Resolve 20

from [www.blackmagicdesign.com.](http://www.blackmagicdesign.com)


**Who This Book Is For** **viii**


## **Getting Started**

Welcome to _The Visual Effects Guide to DaVinci Resolve 20_, an official Blackmagic Design

certified training book that teaches professionals and students the art of visual effects

compositing in DaVinci Resolve 20. Editors will find clear workflow-driven lessons, while

colorists will quickly learn Fusion’s powerful node-based interface to accomplish incredible

Hollywood-caliber visual effects.


As you step through the lessons, you’ll gain experience with Fusion’s green-screen keyer,

powerful planar tracking capabilities, flexible masking tools, and more! Best of all, you’ll

discover that there is no longer a need to send shots out to another application because

with DaVinci Resolve 20, fantastic visual effects are simply a click away from editing.


This guide takes a practical, hands-on approach using real-world techniques for various

compositing jobs. Along the way, you’ll find practical tricks and tips used by professional

visual effects artists to enhance the final outcome of your projects. As you complete each

lesson, you’ll have opportunities to answer sample test questions to test your

comprehension of the techniques.


After completing this book, you are encouraged to take the 50-question online proficiency

exam to receive a Certificate of Completion from Blackmagic Design. You can take the

[exam online at www.blackmagicdesign.com/products/davinciresolve/training.](http://www.blackmagicdesign.com/products/davinciresolve/training)

##### **About DaVinci Resolve 20**


DaVinci Resolve is the world’s fastest growing and most advanced editing software.


It also has a long history of being the world’s most trusted application for color correction.

With DaVinci Resolve 20, Blackmagic Design has added a complete 2D and 3D visual effects

compositing and motion graphics environment that enables you to complete even the

most challenging projects using only one piece of software!

##### **What You’ll Learn**


In these lessons, you’ll work with multiple projects and timelines to learn fundamental and

practical techniques used in a wide range of visual effects and motion graphics genres.

You’ll acquire real-world skills that you can apply to real-world productions.


**Getting Started** **ix**


Lesson 1 begins with a quick start guide that lets you explore the user interface by

creating a simple but highly realistic sci-fi composite. This lesson is meant to get you

comfortable with the interface and workflow since it touches on all the essential tools that

you will use throughout this guide.


Lessons 2–5 cover the most common 2D visual effects techniques that you can use on a

broad range of jobs. You’ll uncover various techniques using Fusion’s point and planar

tracking tools so you can realistically integrate objects into a shot. Using the flexible

vector-based Paint tool, you’ll remove objects to create hidden effects that viewers never

even know are there. Finally, you’ll learn how to approach classic green/blue-screen

compositing that epitomizes visual effects for most people.


**Addendum**


The addendum to this book introduces two lessons on creating motion graphics in the

Fusion page. It is not part of the official curriculum and is not included in the 50-question

exam. However, it does provide useful information for those who need to create more

advanced titles and motion graphics than the edit page templates provide.

##### **The Blackmagic Design Training** **and Certification Program**


Blackmagic Design publishes several training books that take your skills farther in

DaVinci Resolve 20. They include:


- _The Beginner’s Guide to DaVinci Resolve 20_

- _The Colorist Guide to DaVinci Resolve 20_

- _The Editor’s Guide to DaVinci Resolve 20_

- _The Fairlight Audio Guide to DaVinci Resolve 20_

- _The Visual Effects Guide to DaVinci Resolve 20_

- _Advanced Visual Effects in DaVinci Resolve 20_











































**Getting Started** **x**


Whether you want an introductory guide to DaVinci Resolve or want to learn more

advanced editing techniques, color grading, sound mixing, or visual effects, our certified

training program includes a learning path for you.

##### **Getting Certified**


After completing this book, you are encouraged to take a 1-hour, 50-question online

proficiency exam to receive a Certificate of Completion from Blackmagic Design. The link

to the online exam can be found on the Blackmagic Design training webpage. The

webpage also provides additional information on our official Training and Certification

Program. Please visit [www.blackmagicdesign.com/products/davinciresolve/training.](http://www.blackmagicdesign.com/products/davinciresolve/training)

##### **System Requirements**


This book supports DaVinci Resolve 20 for macOS and Windows. If you have an older version

of DaVinci Resolve, you must upgrade to the current version to follow along with the lessons.


NOTE The exercises in this book refer to file and resource locations that will differ

if you are using the version of software from the Apple Mac App Store. For the

purposes of this training book, we recommend that macOS users download and

use the DaVinci Resolve software from the Blackmagic Design website rather than

from the Mac App Store.

##### **Download DaVinci Resolve**


To download the free version of DaVinci Resolve 20 or later from the

Blackmagic Design website:

**1** Open a web browser on your Windows or macOS computer.

**2** In the address field of your web browser, type:

[www.blackmagicdesign.com/products/davinciresolve.](http://www.blackmagicdesign.com/products/davinciresolve)

**3** On the DaVinci Resolve landing page, click the Download button.

**4** On the download page, click the button corresponding to your computer’s

operating system.

**5** Follow the installation instructions to complete the DaVinci Resolve installation.


When you have completed the software installation, follow the instructions in the following

sections to launch DaVinci Resolve and download the media files used throughout this book.


**Getting Started** **xi**


##### **DaVinci Resolve 20 Quick Setup**

When DaVinci Resolve 20 is successfully installed, you can launch the application for the

first time.


**macOS** users will find the DaVinci Resolve application in their Applications folder. Double
click the DaVinci Resolve folder, and then double-click the DaVinci Resolve application.

Alternatively, you can use Launchpad or Spotlight search to locate and launch

DaVinci Resolve.


**Windows** users will find a shortcut has been added to their Desktop. Alternatively, click the

Start menu and search for “DaVinci Resolve” and press Enter to launch the application.


When DaVinci Resolve 20 opens for the first time, you’ll see a Welcome splash screen

detailing the new features available in the current version.


**Getting Started** **xii**


**1** If required, you can change the language used. You can also learn more about these

and hundreds of other amazing features available in DaVinci Resolve 20 by clicking

Learn More. Otherwise, click Continue.


Next, you are invited to go through the Quick Setup process. Experienced users can

skip this process by clicking “Skip and Start Right Now,” but new users are advised to

follow this process. It will only take a couple of minutes and is useful in understanding

how Resolve is working.


**Getting Started** **xiii**


**2** Click the Quick Setup button.


**3** DaVinci Resolve will check your system to ensure its operating system and graphics

card will perform well. If both pass this test, click Continue.


**Getting Started** **xiv**


Next, you will be asked what type of project you would like to begin. DaVinci Resolve

supports projects at different resolutions, from Standard Definition (SD) and High

Definition (HD) to Ultra High Definition and beyond.

**4** If you know the resolution you commonly work with, you can set that here. Otherwise,

leave the resolution set to 1080 HD and click Continue.


The next screen asks where you would like to store your media. This does not refer to

the video, audio, and graphics files you’ll edit and grade, but rather the ancillary files

Resolve will need to create as you’re working. This location is commonly referred to as

a “scratch disk” and by default is set to your current user’s Movies folder (macOS) or

Videos folder (Windows).


**Getting Started** **xv**


**5** Leave this set to the default location and click Continue.


On the next screen, you will be asked which keyboard layout you would like to use. This

is specifically relevant if you’re familiar with using another nonlinear editor; however,

throughout this Visual Effects Guide you will be introduced to keyboard shortcuts that

use the DaVinci Resolve keyboard layout. So if you change the layout at this point, you

may find those shortcuts won’t work.


**Getting Started** **xvi**


**6** For now, leave the layout set to DaVinci Resolve and click Continue.


Congratulations! You have completed the Quick Setup process and have changed

precisely nothing in terms of DaVinci Resolve’s default setup. Nevertheless, you have

also gained an insight into some aspects of using DaVinci Resolve that will serve you

well as you continue learning about the application and how it uses your system.


**Getting Started** **xvii**


**7** Click Start to launch and begin enjoying DaVinci Resolve 20!


Once loaded, DaVinci Resolve will open to the cut page, which is the default starting

page for all projects. However, this is not the usual place to begin working with

DaVinci Resolve. Instead, you should now exit the application in readiness to begin the

first lesson in this book.

**8** Choose DaVinci Resolve > Quit DaVinci Resolve or press Command-Q (macOS) or

Ctrl-Q (Windows).


DaVinci Resolve 20 will close.


**Getting Started** **xviii**


##### **Get the Lesson Files**

To perform the steps detailed in the exercises throughout this book, Fusion Training Media

must be downloaded to your macOS or Windows computer. After you save the files to your

hard drive, extract the file, and copy the folder to your Movies folder (macOS) or Videos

folder (Windows).


**To Download and Install the DaVinci Resolve Lessons Files**


When you are ready to download the lesson files, follow these steps:

**1** Open a web browser on your Windows or macOS computer.

**2** In the address field of your web browser, type:

[www.blackmagicdesign.com/products/davinciresolve/training](http://www.blackmagicdesign.com/products/davinciresolve/training)

**3** Scroll the page until you locate _The Visual Effects Guide to DaVinci Resolve 20_ .

**4** Click the Lesson Files Part 1 link to download the media. The file is roughly

1.5GB in size.

**5** After downloading the zip file to your macOS or Windows computer, open your

Downloads folder and double-click **DR20_Fusion_Training_Media.zip** to unzip it if it

doesn’t unzip automatically. You’ll end up with a folder named DR20 Fusion Training

Media that contains all the content for this book.

**6** From your Downloads folder, move or copy the DR20 Fusion Training Media folder to a

convenient location on your computer or an external hard drive. If in doubt, use your

User’s Movies folder (macOS) or Videos folder (Windows).


Once you have DaVinci Resolve 20 installed and the media files downloaded, you are ready

to begin Lesson 1.


**Getting Started** **xix**


## **Introducing Blackmagic Cloud**

DaVinci Resolve is the world’s only complete post-production solution that lets everyone

work together on the same project at the same time. Traditionally, post-production

follows a linear workflow with each artist handing off to the next, introducing errors and

mountains of change logs to keep track of through each stage. With DaVinci Resolve’s

collaboration features, each artist can work on the same project, in their own dedicated

page, with the tools they need.


Now Blackmagic Cloud lets editors, colorists, VFX artists, animators, and sound engineers

work together simultaneously from anywhere in the world. Plus, they can review each

other’s changes without spending countless hours reconforming the timeline.


Simply create a Blackmagic Cloud ID, log in to the online DaVinci Resolve Project Server,

and follow the simple instructions to set up a new project library—all for one low

monthly price!


Once this library is created, you can access it directly from the Cloud tab in the Project

Manager to create as many projects as you need—all stored securely online. Then invite up

to 10 other people to collaborate on a project with you. With a simple click, they can relink

to local copies of the media files and start working on the project immediately, with all their

changes automatically saved to the cloud.


Enabling Multiple User Collaboration for your project means that everyone can work on

the same project at the same time—edit assistants, editors, colorists, dialogue editors,

and visual effects artists can now all collaborate wherever they are in the world in a way

never before possible.

##### **Media Sync with Blackmagic Cloud Store**


Now you don’t need to buy expensive proprietary storage that needs an entire IT team to

manage! Blackmagic Cloud Store has been designed for multiple users and can handle the

huge media files used by Hollywood feature films. You can also have multiple Blackmagic

Cloud Stores syncing the media files with your Dropbox account so that everyone has

access to the media files for the project.


To find out more about these exciting workflows, visit

[www.blackmagicdesign.com/products/davinciresolve/collaboration.](http://www.blackmagicdesign.com/products/davinciresolve/collaboration)


**Introducing Blackmagic Cloud** **xx**


### Lesson 1
# Getting Started: Learning the Fusion Page



The Fusion page in Resolve contains all

the tools you need to create world-class

visual effects. Instead of the layers you

might be familiar with for photo editing,

Fusion uses nodes similarly to how the

color page uses nodes.


Working with nodes is no more

difficult than adding filters to layers.

It is, however, a more flexible way of

doing things. As you work through

this quick-start lesson, allow yourself a

grace period to adjust to this method

of putting images together. Once the

node‑based paradigm becomes

cemented in your understanding, the

rest of this training guide will come easily.


Throughout this book, we’ll delve into

some powerful techniques for creating

compelling visual effects (VFX), but

it all begins with a foundational

understanding of the Fusion interface

and its basic building blocks: nodes.



Time

This lesson takes approximately
60 minutes to complete.

Goals

Exploring the Fusion Interface  2

Combining Images Using Nodes 9

Adding Effects 13

Understanding Node Flow 17

Working with Masks 20

Secondary Color Correction 22

Animating with Keyframes 27

Adding a Vignette 28

Returning to the Timeline 29

Lesson Review 29


## **Exploring the Fusion Interface**

In most editing systems, you put together your rough cut and then refine your edited

versions in a timeline. If you need compositing or motion graphics work, you export

frames, open up different software, import the frames, and then render out the results for

importing back into the edit timeline. Fusion does away with this: a single click takes you

from the editing into the creation of your effects.

**1** Open DaVinci Resolve, right-click in the Project Manager, and choose Restore

Project Archive.

**2** Navigate to the DR20 Fusion Training Media folder.


This folder contains three DaVinci Resolve Archives and a separate Graphics folder, all

of which we will use throughout the exercises in this guide. We’ll start with the Getting

Started archive.

**3** Select the **GettingStarted.dra** (DaVinci Resolve Archive file) and click Open to add the

Getting Started project to the Project Manager.

**4** Open the Getting Started project from the Project Manager and then select the edit

page, if necessary.

**5** From the main menu bar, choose Workspace > Reset UI Layout.


TIP If you accidentally alter your interface and find it hard to follow along,

selecting Reset UI Layout will return the interface to its default state, which—

for the most part—should match the layout used throughout this book.


The timeline in this project includes a shot that requires some visual effects work.

**6** In the timeline, move the playhead to the start and play through the clip.

This is a scene from the sci-fi short _SYNC_ . In this scene, a robot courier receives a hard

drive directly into a drive slot embedded in its back. Your job is to add the robot’s CG

“cavity” to the live-action footage.


TIP The term _CG_ stands for “computer generated” and typically refers to

images created in a 3D animation package such as Maya or Blender. An older

form of the term is _CGI_, or “computer-generated imagery.”


**7** Position the playhead over the center of the clip.


**Lesson 1 Getting Started: Learning the Fusion Page** **2**


**8** Click the Fusion page button or press Shift-5.


That’s all it takes to bring a single shot into the Fusion page where you can apply effects.


Before you start creating those visual effects, let’s get familiar with the Fusion page.


The page is organized into four main sections: (1) The two viewers across the top

display the images you’re working on. Below the viewers, (2) a timebar for playback

and a toolbar, which includes the most-used effects (also called tools). The lower work

area, called the (3) Node Editor, is the heart of the Fusion page where you construct

your effects. Finally, the (4) Inspector is to the right.



The left and right viewers
can show different images or



In the Inspector, you can display and
manipulate the parameter of any


|Col1|Col2|Col3|Col4|Col5|Col6|
|---|---|---|---|---|---|
|||||||
|||||||



The time ruler includes a red
playhead that indicates the
currently viewed frame.



The work area can show
any combination of the
Node Editor, Keyframes
Editor, or Spline Editor.



The toolbar has buttons for
adding commonly used effects
or tools to the Node Editor.



By default, the work area displays the Node Editor. Similar to the color page, Fusion

applies effects to nodes in a node graph (sometimes called a node “tree”). Each node

in the Node Editor represents an image or effect. How the nodes are connected

determines the layering of images and the order the effects are applied.


**Lesson 1 Getting Started: Learning the Fusion Page** **3**


As mentioned at the start of this lesson, nodes aren’t hard to understand; they just

require a different way of thinking and take a little time to get used to. Before we dive

further into learning about nodes, let’s learn how to navigate around the interface.

##### **Navigating the Fusion Page**


Mouse and keyboard commands in the Fusion page are context sensitive, meaning the

same key presses or mouse clicks can produce different results depending on where your

mouse pointer is positioned in the interface. For the following exercise, pay attention to

where you’re being asked to position the mouse pointer before commencing the action.

**1** With the mouse pointer positioned over an empty gray space in the Node Editor,

hold down the middle mouse button and drag to pan the node tree into the center

of the panel.


TIP While there are workarounds when using other input devices, we strongly

recommend using a three-button mouse when working with the Fusion page.

Typically, pressing down on the scroll wheel of a standard mouse acts as a

middle mouse button click. A pen and tablet input device is also an excellent

choice for working with Fusion, although for brevity we will only cover the

mouse commands in these lessons.


The Node Editor’s infinite work area allows nodes to move outside the current window.

When this happens, the Navigator pane appears in the upper right corner of the editor

panel. Simply click in the Navigator pane to re-center the Node Editor view.


**2** To zoom the Node Editor view, hold down the left and middle mouse buttons and drag

left and right.


Because the keyboard and mouse commands are context sensitive, you can use the

same commands in the viewers.

**3** Position your mouse pointer over the right viewer and drag with the middle mouse

button down to pan, and hold the left and middle mouse buttons down and drag left

and right to zoom.


**Lesson 1 Getting Started: Learning the Fusion Page** **4**


**4** With your mouse pointer still hovering over the right viewer, press Command-F

(macOS) or Ctrl-F (PC) to fit the image into the full area of the viewer.


There are a couple more navigation keyboard commands worth learning.

**5** Press the + and – keys to zoom in to or out of the viewers or Node Editor in

discrete steps.

**6** With your mouse pointer over the right viewer, press Command-1 (macOS) or Ctrl-1

(PC) and Command-2 (macOS) or Ctrl-2 (PC) to zoom to 100% and 200% zoom,

respectively. Press Command-F (macOS) or Ctrl-F (PC) to reframe the image to fit

the viewer in its entirety.


These same navigation commands also work in the left viewer, the Spline Editor, and the

Keyframes Editor.

|Navigating in Fusion|Col2|Col3|
|---|---|---|
||**Mac**|**PC**|
|Pan around a view|Middle mouse drag|Middle mouse drag|
|Zoom the view|Left and middle mouse drag|Left and middle mouse drag|
|Zoom to 100%, 200%|Command-1, Command-2|Ctrl-1, Ctrl-2|
|Frame the view|Command-F|Ctrl-F|



**Lesson 1 Getting Started: Learning the Fusion Page** **5**


##### **Setting Up the Node Editor**

Every clip or image file that you bring into the Fusion page is represented by a MediaIn

node in the Node Editor. The current MediaIn node represents the clip from the edit page

timeline. The MediaOut node represents the final image that is sent back to the timeline on

the edit page. What flows into the MediaOut node to the timeline will be the result of

all our effects work.


NOTE If you disconnect the MediaOut node from the rest of the node tree, the

clip will appear blank in the edit page timeline, since no image data is able to travel

back to the timeline clip.


**1** In the Node Editor, click the MediaIn1 node to select it. A red highlight border appears

around the node to indicate the selection. Press the 1 key to display the image in

viewer 1 to the left.


Pressing the 1 and 2 keys loads a selected node into the left and right viewers,

respectively. If you have an external broadcast monitor connected to a Blackmagic

Decklink card, pressing 3 will load the selected node to the external display.


Notice the small dots at the base of each node. A white dot in position one indicates

that the node is currently loaded in the left viewer. A white dot in position two indicates

that the node is currently loaded in the right viewer. A third dot will only be present if

an external broadcast monitor is connected and indicates whether the node is loaded

to that monitor.


TIP The terms _node_ and _tool_ are used interchangeably to refer to an image
processing operation.


To better understand what each MediaIn node represents, we can add thumbnails to

the nodes.


**Lesson 1 Getting Started: Learning the Fusion Page** **6**


**2** Right-click in an empty space in the Node Editor and choose Force Source Tile Pictures.


When you first enable source tile pictures, you’ll often see an icon in place of the clip

thumbnail. To update the thumbnail, you simply need to drag the time ruler playhead.

**3** Click and drag along the time ruler to update the MediaIn node’s tile picture.


TIP It’s a good idea to enable Force Source Tile Pictures by default for

future projects.


**4** Select Fusion > Fusion Settings.

**5** Select the Flow section, enable Source Tile Pictures, and then click Save.


Future projects will now automatically create thumbnails for the MediaIn nodes.


In addition to adding tile pictures, you can rename nodes to describe their function

or image.


**Lesson 1 Getting Started: Learning the Fusion Page** **7**


**6** Select the MediaIn1 node. Press the F2 key and rename the MediaIn1 node

**BackgroundPlate** .


Fusion does not allow spaces in node names (for a good reason: spaces can cause

significant problems in production automation scripts written in Python and LUA).

Instead, use the underscore character, “Background_plate,” or—as demonstrated in

the previous step—use camel case, a standard form of notation where each new word

starts with a capital (the “humps” of the camel).


TIP A plate in visual effects work is simply the name given to a piece of

footage. The main source footage is commonly referred to as the _background_

_plate_ . Footage that has had elements removed (such as foreground actors or

unwanted production rigging) is commonly referred to as a _clean plate_ .


Fusion’s node-based workflow focuses almost entirely on spatial relationships

between images; it’s almost like time is an afterthought. However, as we saw when we

updated the thumbnail, the time ruler enables movement forward and backward

through the clip.


TIP By default, the time ruler and all time fields on the Fusion page display

frame numbers. To display timecode, choose Fusion > Fusion Settings, and in

the Defaults panel, configure the Fusion page to do so.


The time ruler shows the entire source clip length, and the vertical yellow lines indicate

the render range, which is the portion of that clip actually used in the edit page

timeline. In this case, the entire source media appears in the edit page sequence, so

the yellow lines appear at the far left and far right of the timeline.

**7** Drag the playhead slowly through the render range.


As you drag the playhead through the render range, the current time display (to the

right of the time ruler) displays the current frame number. To the left of the time ruler,

you can see the render range start and end frames.


As the playhead moves, a green line appears along the time ruler to indicate frames

that are cached into RAM for smoother playback. The more RAM you have in your

system, the longer the cached region for RAM playback can be.


**Lesson 1 Getting Started: Learning the Fusion Page** **8**


TIP You can assign more or less RAM for Fusion RAM playback in the

Preferences panel. The amount of RAM assigned to Fusion RAM playback is

taken from the total amount assigned to the DaVinci Resolve application.

## **Combining Images Using Nodes**


It’s time to start creating an effect! We’ll begin by adding another clip to the Node Editor.

**1** In the interface toolbar at the top of the Fusion page, click the Media Pool button to

open the media pool.


Adding new media to the Node Editor is as simple as dragging it from the media pool.

**2** Select the CLIPS bin and drag the DriveDoc clip into the Node Editor and position it

above and to the right of the BackgroundPlate node.


**3** Click the new MediaIn node to select it (the red selection highlight should appear

around it) and press 1 to load it into the left viewer.


**Lesson 1 Getting Started: Learning the Fusion Page** **9**


**4** Drag in the time ruler to preview the clip and update the tile picture.


**5** With the new MediaIn node still selected (it should have its red outline) press F2 and

rename it **DriveDock** .


To layer one image over a background, we typically use a Merge node. We’ll soon learn

how to search for and add the many nodes available in Fusion, but to start, we’ll use

the toolbar to add nodes, since it is the most obvious method.

**6** Select the BackgroundPlate.


To add a Merge node, you first select the node you want to use as the background.

**7** From the toolbar, click the Merge tool.


A Merge node automatically appears, connected to the BackgroundPlate. Next, we’ll

connect the DriveDock so it is layered on top of the BackgroundPlate.

**8** Drag the white square output of the DriveDock node to the green arrow on the

Merge node.


You’ll notice that the right viewer has updated to show the composite of the DriveDock

over the top of the BackgroundPlate. (That’s assuming you still have the MediaOut

node loaded into it. If not, select the MediaOut node and press 2 to load it into the

right viewer.)


**Lesson 1 Getting Started: Learning the Fusion Page** **10**


TIP The term _composite_ refers to the result of combining two or more images

to create a final effects shot.


Let’s talk about all those arrows and connecting lines (called _pipes_ ). First, it’s important

to understand that it isn’t the location of the connections that matter, but rather their

color. Fusion will move the positions of the various arrows around the edge of the

node to better lay out the connections. For example, dragging the DriveDock node

below the Merge node will move the green arrow to the bottom of the Merge node

and move the blue arrow to the top in its place.


In fact, you can lay out nodes however you like. As long as the connections go to and

from the same places, nothing will change in your final image (although, as we’ll soon

see, keeping nodes laid out in a logical order is important for your own comprehension

as you work).


So what do the colors of the connections mean? The green connector is the

foreground input, and the yellow connector is the background input. In other words,

the image feeding into the green, foreground input will be composited on top of the

background image feeding into the yellow input. This is the reason we now see the

DriveDock over the background plate in the right viewer.


**Lesson 1 Getting Started: Learning the Fusion Page** **11**


The blue input is for masking effects (we’ll cover those a little later), and the small white

square represents the resulting image output from the node.



Yellow, background input



Square output



Blue, mask input


TIP If you accidentally connect nodes the wrong way around (the background

clip to the foreground input and the foreground clip to the background input),

simply press Command-T (macOS) or Ctrl-T (PC) to switch them.


While Fusion automatically “wires up” nodes as you go, you’ll frequently want to

modify the pipe connections between them. Let’s look at how to disconnect the pipes.

**9** Hover your mouse pointer over the pipe connecting Merge1 to the MediaOut1 node

until the pipe highlights yellow and blue.


**10** Click the blue section of the pipe to disconnect it.


There is no longer a link between Merge1 and the MediaOut1 node. If you still have

MediaOut1 loaded into viewer 2, you’ll notice that the viewer has gone blank. There’s

no longer any image data reaching the MediaOut node. Let’s go ahead and reconnect

the nodes.

**11** Click the square output icon of Merge1, drag it to the yellow input triangle of

MediaOut1, and then release the mouse button.


The two nodes are connected once again, and you should see the composited image

in viewer 2 once again.


**Lesson 1 Getting Started: Learning the Fusion Page** **12**


## **Adding Effects**

Let’s look at the current composite.

**1** Press the Spacebar to begin playback. Press the Spacebar again to pause playback

when you’re done.

**2** Drag the playhead to a frame where you can clearly see the glowing vertical rails of

blue light on either side of the CG drive bays (around frame 65).


As the composite plays through, you’ll notice that the CG we added doesn’t seem to

fit in with the live-action footage. (There’s also the small issue of the man’s hands

disappearing—we’ll get to that a little later.) That’s because the contrast of the two

elements doesn’t match. Let’s color correct the DriveDock element to match the

background plate.

**3** Drag the DriveDock node upward to create some space. You can hold down the left

and middle mouse buttons and drag left to zoom out if you need more room in the

node view.


Remember: moving nodes around doesn’t change the composite unless we actually

rewire the connecting pipes between them.

**4** Make sure DriveDock is selected (outlined in red) and click the Color Corrector icon in

the toolbar above the node view.


As mentioned earlier, the toolbar gives you visual access to many of the most common

tools in Fusion.


Notice how the color corrector is automatically added directly after the DriveDock

node. Why there? Because we had selected the node prior to clicking the Color

Corrector button in the toolbar. New nodes are always added directly after the

selected node.


**Lesson 1 Getting Started: Learning the Fusion Page** **13**


TIP New nodes are always added directly after the selected node.


Looking at the Inspector to the right, you’ll see that the Color Corrector node offers

multiple correction tools. Right now, we’re only concerned with adjusting the black

point, white point, and contrast of the DriveDock element. Matching the black and

white points of a CG element can go a long way toward integrating them convincingly

into a shot.

**5** Toward the bottom of the Inspector, drag the Lift slider left and right to see its effect.


Something isn’t right here. We only want to color correct the DriveDock clip, but it

seems that the entire composite is changing as we adjust the controls.


This is happening because this CG element contains transparency, and transparency in

CG elements is almost always premultiplied. Premultiplied graphics must be treated a

little differently than clips without transparency before being color corrected. We’ll run

into premultiplied elements in later lessons as well. For now, just know that when

dealing with premultiplied images (and again, computer-generated images with

transparency are almost always premultiplied), you need to enable the Pre-Divide/

Post-Multiply option in the color corrector.


**Lesson 1 Getting Started: Learning the Fusion Page** **14**


**6** In the Inspector, click the Options button to switch to the options section of the color

corrector interface. Enable Pre-Divide/Post-Multiply.


The color adjustment is now limited to the DriveDock element.


Now let’s dial in the black and white points of our CG, starting with the black point.

**7** Make sure the Color Corrector node is still selected; if it is not, click it to select it. Then

click back to the Correction section in the Inspector.


The Inspector always shows the properties for the currently selected node.


Eyeballing the black and white points in an image can be a little tricky, but for this first

lesson we’ll trust our eyes and then learn to do it with more precision in later lessons.

**8** In the Inspector, adjust the Lift slider until the shadows in the CG element match the

intensity of the shadows in the live-action actor’s suit immediately adjacent to the CG.

(Don’t try to match the darker shadows around the arms; you’ll end up with too big a

mismatch due to lighting differences on set.) For greater precision, click in the numeric

entry field to the right of the slider and drag left and right to adjust. In this case, it

should be a very subtle adjustment: a value of around -0.03 should work.


**Lesson 1 Getting Started: Learning the Fusion Page** **15**


TIP In color correction, the Lift control adjusts the level of the dark pixels in an

image, while the Gain control adjusts the level of the bright pixels.


Next, we need to tame the intensity of the bright parts in our DriveDock CG element.

**9** Drag the Gain slider left until it matches the intensity of the light at the top left of the

frame, around 0.4.


We’ve set the black point and the white point (Lift and Gain), so why does the CG still

look too dark? Well, we need to adjust the contrast of pixels between the dark and the

bright areas. We use the Gamma control for this.

**10** Raise the Gamma control until the contrast of the DriveDock pixels looks natural, at a

value of around 1.4.


Things are looking much better. To see just how much better, let’s temporarily disable

the color correction to see how things looked before we started.


**Lesson 1 Getting Started: Learning the Fusion Page** **16**


**11** Make sure ColorCorrector1 is selected (outlined in red), and then click the red switch at

the top of the Inspector or press Command-P (macOS) / Ctrl-P (PC) to disable

the effect.


**12** Repeat the keyboard command to re-enable the node when you’re done.


TIP The “P” in Command-P or Ctrl-P stands for “pass-through.” This shortcut

only works on the node in the node graph that is currently selected.

## **Understanding Node Flow**


Before we move on to fixing the disappearing hand, let’s pause for a moment to better

understand how nodes work. Imagine that each source image is water under pressure.

The water coming from the BackgroundPlate node is the “background-colored” clip.

**1** Select the BackgroundPlate node and press 1 to load it into viewer 1.


One of the great things about working with nodes is that you can quickly see the state

of the composite at any point, simply by clicking through the various nodes that make

up the node graph. Here we can see the state of the composite at the BackgroundPlate

node—just the source footage with no other elements added—while still viewing the

final output at MediaOut1 in viewer 2. This makes it much easier to troubleshoot a

chain of effects in Fusion’s node graph compared to stacking and nesting effects in a

traditional timeline.


**Lesson 1 Getting Started: Learning the Fusion Page** **17**


**2** Click the DriveDock node and press 1 to load it into viewer 1.


Now we see the CG element coming out of the DriveDock node in the left viewer. If you

look carefully, you’ll see that this soloed version of the DriveDock isn’t as dark as the

final version in viewer 2. That’s because we’re looking at the footage before it passes

through the ColorCorrector node that we added in the previous section.

**3** Select ColorCorrector1 and press 1 to load it into viewer 1.


As soon as you pressed 1, you should have seen the image in viewer 1 darken.

That’s because we’re now seeing the DriveDock image after the color correction has

been applied.


TIP The viewer always shows the processed output of the loaded node, and

the name of that node is displayed above the viewer.


So the DriveDock “water” (to work with our water-under-pressure analogy) flows into

the ColorCorrector1 node. As it passes through ColorCorrector1, the “water” is made

darker by our color correction. What comes out the other side (and what we see in

viewer 1) is the darkened result. The color corrector acts like a filtration plant—in this

case, “polluting” our water, making it darker.


When it arrives at Merge1, the “DriveDock water” combines with the “Background

water” flowing in through the yellow, background input. The two streams merge

(hence the name of the node) to create a new single stream that then flows on to

MediaOut1, where it flows out and back to the edit page timeline.


And that’s really all there is to it. To strengthen your understanding, let’s try a

little experiment.


**Lesson 1 Getting Started: Learning the Fusion Page** **18**


**4** Hold down the Shift key, and in the Node Editor, drag the Color Corrector node to the

right, away from the nodes it’s connected to. Release the mouse button and then the

Shift key.


Holding the Shift key enables you to remove a selected node (or group of selected

nodes) from a connecting pipe, leaving the pipe intact. We can also use the Shift key to

insert nodes into an existing pipe.

**5** Drag the BackgroundPlate node to the left to make some room. Hold down the Shift

key and drag the ColorCorrector1 node onto the pipe connecting the BackgroundPlate

to Merge1. When the pipe turns blue, release the mouse button and then release the

Shift key.


TIP When inserting a node using the Shift key, make sure that the connecting

pipe has changed to half blue, half yellow. Otherwise, you may simply be laying

the node over the pipe without actually connecting it to the flow.


Looking at the viewer, you’ll now notice that the background looks darker, and our

DriveDock CG looks lighter. That’s because the BackgroundPlate is now upstream from

the ColorCorrector node, so it is the image being color corrected. DriveDock flows into

the main stream at Merge1. It never passes through the color corrector, so its color

remains unaffected.

**6** Continue to press either Command-Z (macOS) or Ctrl-Z (PC) to undo the previous

commands until ColorCorrector1 is re-inserted after the DriveDock.


**Lesson 1 Getting Started: Learning the Fusion Page** **19**


## **Working with Masks**

As mentioned earlier, dragging the playhead past frame 75 reveals a problem: since our

CG DriveDock is simply pasted over the top of the source footage, it obscures the

screen‑right actor’s hand as it passes into the same region of the frame. We’ll use a new

technique—masking—to solve the problem.

**1** The media pool should already be open at the top left. If it isn’t, click the Media Pool

button to reveal it.

**2** From the CLIPS bin, drag HandRoto into the Node Editor and position it just to the left

of the DriveDock.


**3** With the new MediaIn1 node selected, press the function key F2 and rename it

**HandRoto** .

**4** Press 1 to load it into viewer 1, and then drag the playhead past frame 75 to preview

the animation.


Rotoscoping, or “roto” for short, is the process of drawing outline shapes around

picture elements you want to either isolate or remove. We’ll learn about Fusion’s

built-in rotoscoping tools in later lessons. For now, we’ll work with the provided roto

element of the actor’s hand.


If you remember when we introduced the different colors of a node’s input arrows

earlier, we called the blue triangle the “mask” input. Let’s use it now.


**Lesson 1 Getting Started: Learning the Fusion Page** **20**


**5** Drag from the output square of HandRoto to the blue, mask input of DriveDock to

create a connecting pipe.


Well, that didn’t work so well. We produced the opposite result of what we were after:

instead of hiding the DriveDock CG in the area of the hand, we removed it from

everywhere else!


By default, a mask input assumes you want to keep a node’s effect in the white regions

and remove it in the black regions. And that’s exactly what’s happened. The DriveDock

image has been masked off so that it only appears where the HandRoto clip

appears white.


This is a common problem with a common solution: we can invert the roto matte so

that the blacks become white, and the whites become black.

**6** Select the DriveDock node. In the Inspector, click the Settings button to switch to the

Settings section. Enable Apply Mask Inverted. The hand is now masked out of the

DriveDock image.


**Lesson 1 Getting Started: Learning the Fusion Page** **21**


You won’t see the inverted image reflected in the thumbnail tile of HandRoto. We

selected invert in the DriveDock node; the image coming out of the HandRoto node is

still white-on-black. It’s not until the image arrives at the DriveDock node that it’s

inverted. Remember: in our water analogy, we said that the water is moving “under

pressure.” It only flows in one direction, so what happens in the DriveDock when we

enable invert doesn’t change the state of the DriveDock image “upstream” from it.

**7** Press Spacebar to view the final clip.

## **Secondary Color Correction**


Just when you think your shot is complete, notes will inevitably come back from the client.

After viewing the final composite, the client has decided that the blue light of the drive

dock should change to a red light as the drive bay doors open. The shot is due in 3 hours,

and the CG artist who created the animation has flown back home for the holidays.

What to do?


Thankfully, Fusion provides all the tools we need to customize the shot and create the

desired effect.


A Luma Key node isolates pixels in an image based on their brightness. We’ll use one to

work with only the blue lights in the CG shot.

**1** Move to frame 75 in the timeline and then click in the empty gray space of the Node

Editor to deselect any selected nodes.


So far, we’ve used the toolbar above the Node Editor to add nodes. However, the

toolbar only provides access to a handful of nodes. Just like the other pages in

DaVinci Resolve, all the tools or effects can be found in the Effects library.


**Lesson 1 Getting Started: Learning the Fusion Page** **22**


**2** At the top of the Fusion page, click the Media Pool tab to close the Media Pool panel,

and then click Effects to open the Effects Library.


**3** Click the disclosure arrow next to Tools to reveal the categories.

**4** Select the Matte category and then click Luma Keyer to add it to the Node Editor.


**Lesson 1 Getting Started: Learning the Fusion Page** **23**


**5** Drag a connecting pipe from the output square of the DriveDock and hover it over the

center of LumaKeyer1. Hold down the Option key (macOS) or Alt key (PC) before

releasing the mouse button.


If you ever get confused about which colored input is which, you can use this handy

trick to view a list of all available inputs. The Luma Key node in particular has some

unusual inputs—a Solid Matte input and a Garbage Matte input. We’re only concerned

about the main Input for our purposes.

**6** Select Input from the pop-up list.

**7** Select LumaKeyer1 and press 1 to load it into viewer 1.

**8** In the Inspector, drag the Low and High knobs in the range slider to around 0.30 and

0.80, respectively.


The range slider is the primary method for selecting the low and high end of the range

of pixels that will be isolated by the luma key. At this point, viewer 1 should display only

the blue lighting of the DriveDock element, along with faint highlights on the chassis.


We can use this to mask off the area where we want to apply color correction.


**Lesson 1 Getting Started: Learning the Fusion Page** **24**


**9** Select Merge1 in the Node Editor, and then from the Effects Library, select the

Color category.

**10** Click Color Corrector to add it to the Node Editor.


Since Merge1 was the selected node prior to clicking the Color Corrector, it is placed

directly after the Merge1 node.


**11** In the Inspector, drag the puck (the circle labeled “M”) at the center of the color wheel

all the way to the right, tinting the image red.


We’ve succeeded in turning the entire composite red. Now let’s mask off the color

correction so that it only affects the pixels we isolated with our Luma Keyer.

**12** From the output square of LumaKeyer1, drag a connecting pipe over the blue, mask

input of ColorCorrector2 and release the mouse button.


The red color correction is now isolated to only the bright portions of the robot’s back.


Let’s blur the luma key a little to create more of a glow effect.


**Lesson 1 Getting Started: Learning the Fusion Page** **25**


**13** Select LumaKeyer1 in the Node Editor.


Now let’s locate the Blur tool in the toolbar and add it directly after the selected Luma

Keyer node.

**14** In the toolbar, click the Blur tool to add it directly after LumaKeyer1.


**15** Press 1 to load the Blur node into viewer 1. (Make sure MediaOut1 is still loaded into

viewer 2. If not, select it and press 2.)


TIP Pressing 1 or 2 when a selected node is already loaded in that viewer will

“unload” the viewer, leaving a blank gray. Just press the viewer number again

to reload it.


**16** In the Inspector, set the Blur Size to around 8.


By blurring the mask, we’ve inadvertently “washed out” the strength of

ColorCorrector2. Let’s fix this by increasing the intensity of the color correction.

**17** Select ColorCorrector2 to load its properties into the Inspector. In the Inspector, drag

Saturation to 2.0 and Gain to around 1.7.


**Lesson 1 Getting Started: Learning the Fusion Page** **26**


We’re back to the same color strength, but we now have a little glow around the edges

of the light, thanks to the blur.

## **Animating with Keyframes**


We’ve taken care of half of the notes from the client. Now we need to animate the light

changing from the original blue to our new red as the drive doors open. They begin to

open at frame 55 and are completely open at frame 70.

**1** Move to frame 70 and select ColorCorrector2.

**2** In the Inspector, click the Settings button to switch to the Settings section.


At the very top of the Settings tab is a Blend slider. You’ll find these in the Settings tab

of every node. They allow you to choose how much of the node’s effect to blend in to

the incoming image. If you’re an editor, think of blend as a cross dissolve: a blend value

of 0.0 will output the unaffected source clip; a value of 1.0 will output all the “affected”

version at full strength. A value of 0.5 will output a mix: 50% unaffected source clip and

50% affected version.

**3** Drag the Blend slider to see the effect.

**4** Click the diamond to the right of the Blend slider and ensure that the slider is all the

way to 1.0. The diamond should be red.


**Lesson 1 Getting Started: Learning the Fusion Page** **27**


When you clicked the diamond button, you enabled auto keyframing, indicated by the

change of color. When keyframing is enabled, Fusion automatically sets a keyframe at

the current frame. From now on, whenever you move the Blend slider, Fusion will set a

keyframe at whatever frame your playhead happens to be set to.

**5** Move the playhead to frame 55. Drag the Blend slider to 0.0.


Notice that as soon as you dragged the slider, the diamond changed color again,

indicating that you’ve set a keyframe at the current frame: frame 55.


TIP Editing keyframes is covered in detail in the two lessons located in the

addendum. For now, if you make a mistake, just undo (Command-Z on macOS,

Ctrl-Z on PC) back to before the error.


**6** Drag the playhead from frame 55 to frame 70. The light changes from blue to red as

the Blend value animates from 0 to 1.0.
## **Adding a Vignette**


For a final “flourish,” we’ll add a vignette effect to the shot.

**1** Select ColorCorrector2.

**2** In the Effects Library, select the OpenFX category and scroll all the way down to locate

the Vignette effect.

**3** Click the Vignette tool to add it after the Color Corrector2 node.4. Drag the Size slider

up to around 0.8 and bring Softness down to about 0.4.


**Lesson 1 Getting Started: Learning the Fusion Page** **28**


## **Returning to the Timeline**

The beauty of Fusion existing as a page in Resolve is that returning from performing

effects work is as simple as clicking back to the edit page. For the smoothest playback from

the timeline, let’s enable smart caching.

**1** Click the Edit button at the base of the interface or press Shift-4 to return to the

edit page.

**2** Select Playback > Render Cache > Smart to enable smart caching.


When smart caching is enabled, Resolve will take advantage of idle CPU cycles to

render a cache file of the Fusion effects work. As you watch, the bar at the top of the

timeline will turn blue, indicating that the clip is fully cached and ready to be played

back smoothly (assuming your cache directory is set to a sufficiently speedy drive—

you can set its location in the Media Storage section of System Preferences).

## **Lesson Review**

**1** In the Fusion page, how can you display the output of a node in viewer 1?

**2** When adding a new node, where is the node added?

**3** What node would you use to combine two images?

**4** What is the yellow input on a Merge node?

**5** True or False? When you’re on the Fusion page, you can disconnect the MediaOut node

because you have no use for it.


**Lesson 1 Getting Started: Learning the Fusion Page** **29**


##### **Answers**

**1** In the Fusion page, to display the output of a node in viewer 1, select the node and

press the 1 key.

**2** The new node is added directly after the selected node in the Node Editor.

**3** A Merge node is used to composite two images.

**4** The yellow input on a Merge node is for the background input.

**5** False. The MediaOut node is always the last node connected, and it renders the

Node Editor results back to the edit page timeline.


**Lesson 1 Getting Started: Learning the Fusion Page** **30**


### Lesson 2
# Compositing Split Screens



The Fusion page excels at creating

photorealistic visual effects

composites. Creating a visual

effect composite is primarily about

combining multiple distinct images

to make a believable new whole. The

goal is to convince the audience that a

single live-action camera recorded the

resulting shot live, regardless of how

fantastical the subjects.



Time

This lesson takes approximately
45 minutes to complete.

Goals

Using Layers from the Edit Page 32

Tracking in the Fusion Page 37

Drawing a Matte 44

Aligning the Clips Using Nudging 50

Restoring Camera Motion 53

Lesson Review 57


One of the most critical aspects when compositing is to have all the different elements

follow the same camera motion. These are often called _match moves_ because you analyze

the background clip’s movement and apply it to a foreground clip or vice versa. The Fusion

page provides four primary techniques for extracting the camera’s motion: point tracking,

planar tracking, surface tracking, and 3D camera tracking. In the course of this book, you’ll

learn about the two methods provided in the free version of DaVinci Resolve 20: the point

tracker and the planar tracker.


This first visual effects lesson will analyze the motion in two shots using the standard point

tracker to create a split-screen effect. A split screen in visual effects terms is a technique in

which different takes are combined to make one better overall take. For instance, suppose

we have two actors in a shot. One actor might deliver an excellent performance in take 1,

while the other actor delivers their best performance in take 2. The director might want to

combine the two performances and make them appear as a single take.


Original clip and completed split screen for Lesson 2.

## **Using Layers from the Edit Page**


The next four lessons of this book use a new project. You’ll start by restoring a new archive

that includes all the media, bins, and timelines you’ll need.

**1** Open DaVinci Resolve 20, and in the Project Manager, right-click and choose Restore

Project Archive.

**2** In the navigation window, go to the DR20 Fusion Training Media folder and

open **DR 20 Fusion VFX lessons dra** .

**3** In the Project Manager, double-click the DR20 Fusion VFX Lessons project to open it,

and then click the Edit button or press Shift-4 to return to the edit page if you’re still on

the Fusion page.


**Lesson 2 Compositing Split Screens** **32**


**4** From the Timelines bin, double-click **Fusion VFX Lessons -START** .

**5** Move the playhead over the first red marker in the timeline. Use Command + (macOS)

or Ctrl + (PC) to zoom the timeline in once.


This first edit consists of a driver and a passenger in a car. The passenger is listening

to the driver, nodding with encouragement. Video track 1 has a much better view of

the driver speaking but not of the passenger’s reaction.

**6** In the timeline, select the clip on video 2, press D to disable it, and view the driver

speaking and the less affirming passenger on video track 1.


**Lesson 2 Compositing Split Screens** **33**


**7** Press D a second time to enable the video track 2 clip again.


Your job is to perform a split-screen effect. The goal is to combine the driver speaking

from V1 with the nodding passenger’s better reaction from V2.


To start the split-screen effect, you must bring both takes into the Fusion page.

To bring more than one clip from the edit page into the Fusion page, you must create

a Fusion clip.

**8** Select both clips in the timeline. Right-click the selected clips and choose New Fusion

Clip at the top of the menu.


A Fusion clip is created in the timeline and added to the selected bin. The two layers

are collapsed into the container.


**Lesson 2 Compositing Split Screens** **34**


TIP You can display all the layers of a Fusion clip in the edit page timeline by

right-clicking the Fusion clip and choosing Open in Timeline.


**9** With the playhead still positioned over the clip, click the Fusion page button or

press Shift-5.


The two layers are brought into the Node Editor and combined in a Merge node.


A Background node is also added and combined with a separate Merge node. The

Background node is added as a sort of canvas to set the resolution size and duration

when you have clips of different resolutions or durations within the Fusion clip. We’ll

delve more into this topic with a great example in the next lesson. For now, just be

aware that a Background node will show up in a Fusion clip, and there is a reason, so

we will keep it, but we will clean up the layout of the nodes a bit.

**10** Move Background1, Merge1, and Merge 2 as the bottom row of the node graph. Then

position the MediaIn 1 directly above the Merge1 and the MediaIn2 directly above

the Merge2.


This creates a more “readable” layout and sets us up for adding additional nodes.


NOTE Feel free to spread out the nodes within the Node Editor as you

continue to add nodes in this lesson. In the screenshot above, we’ve already

added some extra space so additional nodes won’t overlap.


The MediaIn1 node represents the clip from video track 1, and the MediaIn2 node

represents the clip from video track 2. The Background node acts as a virtual canvas

and sets the resolution by connecting to the Merge1 background input. MediaIn1 is

the foreground for Merge1. The output of Merge1 is used as the background input on

Merge2, and MediaIn2 connects to the foreground input of Merge2. This setup

identically matches the timeline layering.


**Lesson 2 Compositing Split Screens** **35**


To better keep track of each MediaIn node, you can change their default names to be

more descriptive of the contents.

**11** Rename MediaIn1 to **Driver** and MediaIn2 to **Passenger** .


TIP Node names cannot contain spaces, but you can use the underscore

character to separate words.


Now, you’ll continue with this split-screen composite by tracking the PASSENGER clip and

using that tracking data to stabilize it.











**Lesson 2 Compositing Split Screens** **36**


## **Tracking in the Fusion Page**

The easiest way to create a split-screen effect is to remove all camera motion from both

the PASSENGER and the DRIVER clips. You want to eliminate the camera motion so that

later you can re-apply camera motion to the new composite from whichever take you

prefer. To remove camera motion or stabilize a clip, you must track the clip using a Tracker

node in Fusion.

**1** Select the PASSENGER node.

**2** In the previous lesson, you learned to add effects using the toolbar and the Effects

library. Now, let’s learn what very well might be the most common (and quickest) way

you can add effects to the Node Editor: the Tool Selection window.

**3** Press Shift-Spacebar to bring up the Select Tool dialog and type **TRA** because you are

looking for the Tracker tool.


**4** As you type the letters, Fusion begins to isolate all tool names that contain those

letters. You can use the Up and Down Arrow keys to highlight different selections,

although in this case the node we want—Tracker—is already the default selection.


**Lesson 2 Compositing Split Screens** **37**


**5** Press Return/Enter to add the selected Tracker tool. It is added after the selected

PASSENGER node.


When you know the name of the tool you’re looking for, the Select Tool dialog will be

the quickest way to add it to your Node Editor.


The point tracker you just added is a sophisticated tracking tool that has the option to

use DaVinci Resolve’s AI Neural Engine in the Studio version. However, even in the free

version of the application the point tracker is a real workhorse because it works on the

broadest range of shots.

**6** Select the Tracker node and press 1 to see it in the viewer.


The first step in setting up the tracker is to position the tracker over a high-contrast

pattern in the frame that includes the motion you want to track. Because you want to

remove the camera motion, you identify objects in the frame that move only because

of camera moves.

**7** Move the playhead to the start of the render range.


TIP You can press Command-Left Arrow (macOS) or Ctrl-Left Arrow (PC) to

move the playhead to the start of the render range.


If you’re using DaVinci Resolve 20 Studio, the tracker defaults to using DaVinci’s Neural

Engine-powered IntelliTrack. Positioning the tracking point is all you have to do.


If you’re using the free version of DaVinci Resolve, a point tracker is the default, and

there is a bit more setup required. When the mouse pointer is over the point tracker

outline in the viewer, the tracker displays two boxes: the pattern box and the search box.


TIP The tracker automatically chooses the clip connected to its background

input as the clip to track.


**Lesson 2 Compositing Split Screens** **38**


**8** In viewer 1, drag the handle in the upper left corner of the pattern box to position the

tracker over the lock on the back door.


TIP For the IntelliTrack, there is no handle; you can just drag the center point.


The point tracker’s pattern box expands and displays a magnified view of the area you

are over so you can be precise with your selection. The door lock is a high-contrast,

well-defined area that stays in the shot the entire time. This makes it a good

tracking point.

**9** When the door lock is centered in the magnified view, release the mouse button.


The outer box of the point tracker is the search box. As the tracker moves frame by

frame through the clip, it looks for the pattern you have identified in the pattern box.

The larger the search area is, the longer the tracking analysis takes. On slow-moving

objects, the pattern probably won’t move far from one frame to the next, so you can

usually create a relatively small region for the search box. When you have a fast
moving object, you might need to increase the search box size.


TIP IntelliTrack, like other AI tools, doesn’t use predetermined rule sets or

heuristics like the search box size. Instead, it is trained on real-world examples.

This makes it less likely to fail in scenarios like tracking a subject behind brief

occlusions. For most cases, it will be more precise and more robust than the

normal point tracker. However, for the remainder of this lesson we will use the

point tracker, since it is available to all users.


**Lesson 2 Compositing Split Screens** **39**


Because the camera does not move very quickly in this shot, the tracked objects will

not move very far from one frame to the next. So we can leave the search box at its

current size.


When stabilizing a shot, a single point stabilizes only the translation movement (up/

down and side-to-side) of that pattern in the frame. The pattern can still scale and

rotate. You need at least three points to prevent an image from moving, scaling,

and rotating.

**10** In the Inspector, click the Point button to add two additional tracker points to the

tracker list.


TIP You can double-click a tracker in the Tracker List and rename it for

organizational clarity.


**11** In viewer 1, drag Tracker 2 over the highest-contrast area of the seatbelt attachment to

the right of our passenger’s head.


**Lesson 2 Compositing Split Screens** **40**


The high-contrast parts of the car are good tracking points. They are “nailed to

the set,” meaning they do not move except for the fact that the camera moves.

The passenger and driver are not nailed to the set, so they would make a poor

choice for tracking in this shot.


Selecting a third tracking point gets trickier. There are not too many other high‑contrast

points in the car. Because details outside the car (looking through the window) are at a

distance, tracking anything in the window could be impacted by camera parallax. So

we are limited to picking a point inside the car. Although in most cases shadows are a

last resort when tracking, since they _can_ move independently of the camera, the

shadows on the door to the left of our passenger will work in this clip.


TIP _Parallax_ occurs when camera movement reveals one object behind

another that was previously obscured by the foreground object.


**12** Drag Tracker 3 over the sharp triangular shadow on the door.


To begin the tracking process, you use the tracking analysis buttons along the top of

the Inspector.

**13** Click the Track Forward button to begin the tracking process.


Viewer 1 displays the progress of the trackers until the analysis is complete.


**Lesson 2 Compositing Split Screens** **41**


You now have three reliable trackers that follow the camera movement. However, tracking

is not the effect; it is only the means to an end. The next step is to put that tracking data to

use in stabilizing this clip.

##### **Using a Tracker for Stabilization**


After the tracking analysis completes, you can then change the tracker’s operation mode

to utilize the tracking data.

**1** In the tracker’s Inspector, click the Operation tab.


The Operation tab is where you determine how the tracking data is used. The

Operation menu at the top of the Inspector contains all available options.

**2** From the Operation menu in the Inspector, choose Match Move.


The Operation menu options depend on the inputs connected to the Tracker node. To

stabilize a clip, you must have the clip connected to the background input, as we have

done here. Then you set the match move operation to apply to the background.

**3** From the Merge menu, choose “BG only.”


**Lesson 2 Compositing Split Screens** **42**


**4** Play the clip to view the stabilized clip in viewer 1.


As the clip plays in viewer 1, notice that it reveals some of the checkerboard

background on the left side of the frame. Stabilization works by taking the camera

motion from the tracker, inverting that motion, and applying it to the same clip. For

instance, if the camera moves down, the tracker pushes the entire frame up to

offset the move.


However, this exposes the background because the clip has the same resolution as the

output. You’ll have to fix this at some point, but for now you just want a very steady clip.

##### **Stabilizing the Driver**


There are many methods you could use to perform this split screen, but the most

straightforward is to make sure both clips are stabilized. This makes it much easier to

combine the two clips. Now that you have some experience stabilizing with the tracker,

you can repeat the same steps to stabilize the DRIVER clip.

**1** In the Node Editor, select the Driver node, press Shift-Spacebar to access the Select

Tool dialog, type **TRA**, and add the tracker to it.

**2** Select the Tracker 2 node and press 1 to see it in the viewer.

**3** Position the playhead at the start of the render range.

**4** In the Inspector, add two more trackers to the tracker list and then position all three

trackers in roughly the same locations as you did for the PASSENGER clip.


**Lesson 2 Compositing Split Screens** **43**


**5** Once the trackers are correctly positioned, click the Track Forward button.

**6** In the Inspector, click the Operation tab, and from the Operation menu choose Match

Move, and then from the Merge menu, choose “BG only.”


You now have two perfectly stable clips. With the camera motion removed, you can draw

a simple mask shape to isolate the halves of each clip you want to use.
## **Drawing a Matte**


A considerable part of compositing has to do with drawing mattes, sometimes called

_rotoscoping_ . Mattes help you isolate specific areas of your image so that effects are applied

only where they are needed.


In the “Getting Started” project, we were working with a CG element that had an alpha

channel—a special, hidden channel of image data that defines which parts of an image are

solid and which parts should be transparent. (We cover alpha channels in more detail in

the addendum.)


Since there is no alpha channel in either of these pieces of footage, we need to create a

matte that will define which parts of the Passenger clip should be solid and which parts

should be cut away to reveal the Driver clip.

**1** Select the Merge2 node and press 2 to view it in viewer 2.


The Merge2 node has the Passenger clip connected as the foreground, so viewing the

merge will only display that clip until we apply the mask.

**2** Drag the playhead to the start of the render range.


It’s best to add the polygon mask shape while you’re positioned at the start or end of a

render range because the polygon mask shape auto-animates—meaning, if you later

change the shape on any other frame, the shape interpolates (changes shape over

time, morphing from the start shape to the new, changed shape). This makes it very

quick to rotoscope a moving object but can be confusing if you’re unaware of

the behavior.


TIP To disable auto-keyframing on spline shapes in the Inspector, click the red

animation diamond at the bottom of the Inspector labeled “Right-click here for

shape animation.”


**Lesson 2 Compositing Split Screens** **44**


**3** Drag the Polygon shape tool from the toolbar just below Merge2 for better organization.


When a Polygon mask tool is selected, drawing tools appear above the viewer, and you

can begin to draw a shape even before connecting the node into your composite.

**4** To increase the size of the viewer and see more detail around the area you’re

rotoscoping, position the mouse pointer on the line between the transport controls

and the toolbar, and then drag down to increase the viewer’s size.


We won’t need two viewers for this task, so we can gain more working space by

viewing a single viewer for the Merge node.

**5** With the Merge2 node still shown in viewer 2, click the Single Viewer button located in

the upper right corner of viewer 2.


Now, viewer 2 takes up the entire top half of the screen to give you a good canvas on

which to draw your matte.


NOTE The terms _matte_ and _mask_ are often used interchangeably. In this

book, matte refers to a grayscale image that identifies transparent and

opaque pixels. A mask is the application of a matte. That is, you use a matte to

mask off part of an image.


**Lesson 2 Compositing Split Screens** **45**


**6** To ensure that you draw the matte around the frame, move the mouse pointer over

the viewer. Hold down the Command (macOS) or Ctrl key (PC) and scroll the middle

mouse wheel to zoom in until you are able to see around the entire frame.


To draw a polygon shape around the left side of this image, you’ll need no more than

10 to 15 control points. You want to use as few points as possible but as many as

needed to cover the area correctly.


TIP You can always add and subtract points later, but the more points you

add, the more you’ll have to manage.


**7** With the Polygon node still selected in the Node Editor, click in the upper left corner of

the frame to add a control point. Then, move your pointer down to the lower left

corner and click to create a spline running down the left side of the frame.


**Lesson 2 Compositing Split Screens** **46**


You don’t need to add many points along the straight edges of the frame, because

they are straight. However, you’ll want to be more detailed as you continue the shape

between the characters.

**8** Move the mouse pointer across the bottom of the frame until you reach the driver’s

blue shirt, and then click to add a point under his blue shirt.


TIP Holding the middle mouse button and dragging in the viewer will pan the

viewer, making it easier to see various parts of the frame while you are

zoomed in and drawing your matte.


**9** Move your pointer between the passenger’s yellow top and the driver’s blue shirt, and

then click to add a new control point just before they separate.


**10** Add another point along the Driver’s shoulder just past the sun patch on the back seat.


**Lesson 2 Compositing Split Screens** **47**


**11** Move your mouse pointer up and over to the left to the lower left corner of the back

door window.


**12** Move your mouse pointer halfway up the window frame between the front and back

door and click to add a control point just before the driver’s hair overlaps with the

window frame.


**Lesson 2 Compositing Split Screens** **48**


**13** Move your mouse pointer up and into the center of the window frame to avoid the

driver’s hair.


**14** Add a point at the top of the frame and then move your mouse pointer over the first

point you started with.

**15** When the mouse pointer displays a circular icon, click the first point you added or

press Shift-O to close the shape.


TIP Many problems occur when you assume that you have closed a shape, but

it is still open. Making sure you close the shape by either using the keyboard

shortcut (Shift-O) or clicking directly on the first control point will save you a

considerable amount of troubleshooting time later.


Now that you have a shape to create a mask, you need to connect the polygon node

into the composite.

**16** Drag the output of the Polygon1 node to the blue mask input on Merge2.


Your new polygon matte is now “choosing” to merge only the passenger (the screen
left actor) from the Passenger clip over the top of the passenger in the Driver clip. Let’s

switch back and forth so you can see the results more clearly.


**Lesson 2 Compositing Split Screens** **49**


**17** Select Merge1, and then press 2 to load it into viewer 2.


Now let’s switch back to Merge2 to view the split screen.

**18** Select Merge2, and then press 2 to load it into viewer 2.


You just confirmed that the split screen is working: the screen-right driver actor stays

the same in both Merge nodes, but the passenger clearly jumps between when

switching between the two Merge nodes.


It’s worth pausing for a moment here to get a better understanding of what’s going

on. We’ve drawn a matte using the Polygon node that essentially decides where

Merge1 will “do its job” and where it won’t. In the white area of Polygon1, Merge2 will

“work.” In other words, it’ll do its job of compositing the pixels of Merge2’s foreground

input—PASSENGER—over the top of the pixels of Merge1’s background input—Merge1

(which is essentially just showing the DRIVER node). But where the matte is black,

Merge2 will not apply any effect. In other words, it will leave the pixels coming into its

background input unchanged. The result is that we get the screen-left actor of

PASSENGER composited over the top of the existing version of her in the DRIVER take,

but the screen-right actor remains unchanged.
## **Aligning the Clips Using Nudging**


At this point, we could call the shot “final” and send it on for review. However, there are a

few final touches we can do to make this shot more realistic.

**1** Make sure Merge2 is loaded into viewer 2. Press the Spacebar to play through

the sequence.


There are two remaining problems: First, we’ve removed all motion from the frame by

stabilizing both shots. Directors like motion in the frame, so the director won’t be

happy with us removing it. Second, there’s no guarantee that each take started with

the camera in exactly the same position, so there’s a slight misalignment in the

positioning of the two stabilized shots. Look carefully at the border between the two

actors, and you’ll notice a “tear” resulting from the misalignment.


**Lesson 2 Compositing Split Screens** **50**


Let’s start by fixing the latter issue: aligning the starting position of the two shots.

**2** Click the connecting pipe between Polygon1 and Merge2 to disconnect it.


We’re just temporarily disconnecting Polygon1; when we’re done aligning the clips,

we’ll reconnect it.

**3** Move the playhead back to the start of the timeline. Select Merge2, and then in the

Inspector, change the Apply Mode to Difference.


Sometimes you’ll find that you need to “break” a shot to perform useful adjustments.

Here, we’ve changed the method by which Fusion composites the foreground and

background. That’s what apply modes do: they blend foreground and background in

different (and often artistically interesting) ways. In Difference apply mode, whenever

overlapping foreground and background pixels are the same, they’ll appear black.

Wherever they’re different, they’ll appear as light. Now we should expect the actors to

stand out, since they’ll be in different positions in the two different takes. But all things

considered, the background of the car should be identical in both shots.


**Lesson 2 Compositing Split Screens** **51**


**4** In the Inspector, click and drag in the Center X and Center Y numeric entry fields to

nudge the alignment of the images until the majority of the car background turns

black. For fine adjustments, hold down the Command key (macOS) or Ctrl key (PC)

while dragging. For extremely coarse adjustments, hold down the Shift key (though in

the case of this shot, such large adjustments should not be necessary).


TIP Due to lens distortion and subtle light changes between takes, you’ll

never get perfect alignment of the shot throughout the frame. Focus instead

on getting alignment where it counts. In the case of this shot, that’s toward

the center of the shot where the split screen divides between the two actors.


You’ll find that you’ll need to go back and forth between X and Y, since adjustments in X

will negatively impact the alignment in Y, and vice versa. Alternately adjusting X then Y

will allow you to home in on a final optimal alignment. Final values of around 0.49 and

0.51 should produce the desired alignment.


**5** With alignment complete, return Merge2’s Apply Mode to its Normal blend state and

reconnect Polygon1 to the blue mask input of Merge2.


For the most part, the tear between the actors is fixed. We’ll add a little blur to the

matte to soften the transition and hide any remaining mismatch due to shadows and

lighting differences between the takes.


**Lesson 2 Compositing Split Screens** **52**


**6** Select Polygon1. In the Inspector, drag Soft Edge to around 0.02 to smooth the border

between the two takes.


If you notice that the screen-left actor is bleeding into the split-screen border, move

back to the start of the sequence (where you initially created the shape) and drag the

border points of the shape to eliminate the problem.
## **Restoring Camera Motion**


Let’s address the other issue now: reintroducing movement to the frame. Restoring

camera motion is done by reapplying the tracking data, but instead of steadying the clips

as we did to stabilize them, you will now unsteady the composite.

**1** Choose Workspace > Reset UI and click the single viewer icon to return to a dual

viewer setup.

**2** In viewer1, load Tracker 2, and in viewer 2, load the Merge2 node.


**Lesson 2 Compositing Split Screens** **53**


**3** Select the Merge2 node, press Shift-Spacebar to open the Select Tool dialog, type **TRA**,

and then select Transform (Xf).


The Transform node is added directly after Merge 2 and will be used for two final

steps. First, the Transform node will be used to reapply the tracking data, and second,

it will allow us to scale up the final composite a tiny bit to hide some imperfections

around the edges.

**4** Select the Transform node and press 2 to see the results in viewer 2.


When you have tracked an image with a Tracker node, the data from the tracker is

published. This allows other nodes to reuse the same data without you having to copy

and paste the Tracker node multiple times throughout a composition. You access this

published tracking data by right-clicking over a parameter in the Inspector or the

onscreen control in the viewer and using the Connect To menu.

**5** In the viewer, right-click over the transform’s center point control.


**Lesson 2 Compositing Split Screens** **54**


**6** At the bottom of the contextual menu, choose Tranform1: Center > Connect To >

Tracker2 > Unsteady Position.


The Connect To submenu is used to link various published parameters or data to other

parameters. Since we added a tracker to the PASSENGER clip and a second tracker to

the DRIVER clip, both trackers’ published data is shown in the menu. This allows you

to reapply the camera motion from either clip.


Choosing Tracker 2 takes the camera motion from the DRIVER clip, and choosing

Unsteady Position applies the tracked motion data to the transform.

**7** Play the composite to view the split screen.


TIP For optimal quality, it’s best to try to construct your node trees so that

nodes that transform images are placed next to each other in the node tree.

Specific nodes that transform (scale, position, rotate) an image will maximize

quality by performing the transforms from adjacent nodes in one pass. This is

called _concatenation_ . The Transform, Tracker, DVE, and Merge nodes all

concatenate as long as a mask is not connected to any of the nodes.


**Lesson 2 Compositing Split Screens** **55**


The last piece of the puzzle in finishing this composite is to scale the final result so the

image fills the frame. Because of the stabilization, you can see that the lower right

corner of the frame reveals a tiny sliver of the background. The way to correct this is to

scale the final composite to fill the image.


**8** In the Inspector, increase the Size control to around 1.01 to fill the frame with the

finished composite.


**9** Play the composite to view the final shot.


Your split-screen composite now has a better overall look with the added camera motion.

You’ve taken these two shots from the edit page timeline into a completed composite,

using a couple of Tracker nodes, a simple Polygon mask, and a Transform.


Completed node tree for Lesson 2.


**Lesson 2 Compositing Split Screens** **56**


## **Lesson Review**

**1** True or False? A Fusion clip is used to take multiple timeline layers from the edit page

into the Fusion page.

**2** True or False? Green is the color of the Effect mask input on a Matte control node.

**3** True or False? You must click the Keyframe button in the Inspector to animate a

Polygon matte.

**4** True or False? The Tracker is used to stabilize clips in the Fusion page.

**5** True or False? In the Merge menu of the Tracker’s Operation tab, choosing “BG only”

will stabilize the clip that is connected to the yellow background input of the

Tracker node.


**Lesson 2 Compositing Split Screens** **57**


##### **Answers**

**1** True. A Fusion clip is used to take multiple timeline layers from the edit page into the

Fusion page.

**2** False. The green input on any node is the foreground input.

**3** False. No button needs to be enabled. Polygon mattes auto-animate by default.

**4** True. The Tracker is used to stabilize clips in the Fusion page.

**5** True. In the Merge menu of the Tracker’s Operation tab, choosing “BG only” will

stabilize the clip that is connected to the yellow background input of the Tracker node.


**Lesson 2 Compositing Split Screens** **58**


### Lesson 3
# Replacing a Sky



One of the most common problems

with shooting outdoors is the sky.

Either the location or time of day you

are shooting lacks the mood your

scene calls for, or your camera lacks

the dynamic range to expose the

foreground without overexposing

the sky. The good news is, as far as

visual effects go, sky replacement isn’t

that difficult once you know the basic

node structure.



Time

This lesson takes approximately
45 minutes to complete.

Goals

Retaining a Clip’s Resolution 60

Controlling a Composition’s
Resolution  64

Compositing Using the
Darken Apply Mode  69

Adding Effects from
the Effects Library  71

Fixing Holes in a Key 74

Embedding Alpha into an Image 75

Tracking the Sky into Position 78

Fixing Interrupted Trackers 82

Blending In the Original Sky 83

Lesson Review 85


In this lesson, you’ll learn an indispensable node structure for a sky replacement.

During the process of learning how to perform a sky replacement, you’ll also look closer

at compositing images of different resolutions.


Completed sky replacement for Lesson 3.

## **Retaining a Clip’s Resolution**


This lesson will continue with the same project you restored in the previous lesson. We’ll

open the same timeline and begin with the clips located at the second red marker.

**1** Open DaVinci Resolve 20 and, from the Project Manager, open the

**DR20 Fusion VFX lessons** project.

**2** In the Timelines bin, double-click the **Fusion VFX Lessons - START** timeline.

**3** Move the playhead over the second edit and the second red marker.


**Lesson 3 Replacing a Sky** **60**


DaVinci Resolve in general, and the Fusion page specifically, are resolution

independent. You can efficiently work with any number of elements at different

resolutions. But knowing what resolution independence means and dealing with it

in your node tree are two very different things. When constructing composites with

mixed resolutions, you must be aware of how images are handled, not only between

the edit and Fusion pages but also within the Fusion page itself.


Like the clips you worked with in Lesson 2, this second edit in the timeline also includes

two layers.

**4** Select the foreground clip on video track 2 and press D to disable this clip in the viewer

and reveal the Sky with Rainbow image on video track 1.


In this two-layer composite, the Sky with Rainbow is a still photo with a resolution of

3888 x 2187, and the foreground clip on video track 2 is 1920 x 1080. The timeline is

also set to 1920 x 1080 HD.


As you can see, the wide blue sky has a nice rainbow and clouds, which we want to see

in the sky replacement composite. Since this is a high-resolution photo, we can scale

and reposition it without losing quality.


**Lesson 3 Replacing a Sky** **61**


**5** Select the Sky with Rainbow clip on video track 1 in the timeline, and then in the

Inspector, use the zoom controls to scale up the clip to about 1.5 and drag the X

position to around 400.


Because Fusion is fully integrated into DaVinci Resolve, the layering and transforms

you perform on the edit page timeline carry over to the Fusion page.

**6** Select the foreground clip on video track 2 and press D to enable this clip in the viewer.

**7** Select both clips in the timeline, and then right-click and choose New Fusion Clip

from the menu.


As you saw in Lesson 2, a new Fusion clip is created in the timeline and added to the

selected bin. The two layers are collapsed into a container and can be brought into

the Fusion page.

**8** Position the playhead over the new Fusion clip, and then click the Fusion page button

or press Shift-5. Rearrange the nodes similar to how you rearranged them in the

previous lesson: Background node > Merge1 > Merge2, and then MediaIn1 directly

above Merge1, MediaIn2 directly above Merge2.


**Lesson 3 Replacing a Sky** **62**


NOTE This lesson uses dual viewers. If your workspace is using a single

viewer, click the Dual Viewer button in the upper right corner of the viewer.


**9** Select MediaIn1 and press 1 to view it in the left viewer.


The two layers are brought into the Node Editor and are combined via a Merge node

while the background node is used to define the resolutions, matching the timeline

resolution. The MediaIn1 node represents the sky clip from video track 1, and the clip

from video track 2 is represented as the MediaIn2 node.

**10** Hover your mouse pointer over viewer 1 and drag the middle mouse button down and

to the left until you can see the resolution in the top right corner of the frame.


When using a Fusion clip, the resolutions of the nested clips are set to timeline

resolution. This is the working resolution of the composite.

**11** Select the MediaIn1 node, and then click the Transform tool in the toolbar. Press 1 to

see the Transform node in viewer 1.


The Transform node is added to the sky clip. Since this is a large-resolution image in a

1920 x 1080 frame, we should be able to scale it back a considerable amount and see

the remaining image that falls outside the frame boundary.


**Lesson 3 Replacing a Sky** **63**


**12** Select the Transform node and, in the Inspector, drag the Size slider down to around 0.5.


As you scale back the image, it reveals transparency around the edges as if the

background clip has a resolution of 1920 x 1080. The beauty of a Fusion clip is that it allows

you to use the intuitive tools of the edit page to layer, trim, and align your clips before

bringing them into the Fusion page. However, the new Fusion clip is created at the timeline

resolution. If your source clips and timelines have the same resolution, as you had in

Lesson 2, then the Fusion clip is the most efficient way to set up your composite. However,

if you are dealing with clips larger than the timeline resolution, a Fusion clip will resize all

the sources to fit. This is not the best setup for dealing with a large photo of the sky for

which we only want to use a small area. Let’s look at a different technique that will allow

us to work with clips at mixed resolutions.
## **Controlling a Composition’s** **Resolution**


Unlike a Fusion clip, bringing a single clip from the edit page to the Fusion page maintains

the clip’s original resolution, regardless of the timeline resolution setting. This means

you’re always using the highest-quality compositing in the Fusion page when dealing with

a single layer from the edit page.

**1** Return to the edit page and choose Edit > Undo to undo the Fusion clip in the timeline.


With the clips returned to individual layers in the edit page, we can disable video track

2 and bring the sky image into the Fusion page.


**Lesson 3 Replacing a Sky** **64**


**2** Select the clip on video track 2 and press D to disable the clip.

**3** Select the Sky image on video track 1 and reset the scale you applied in the Inspector.

**4** Switch to the Fusion page.


If a clip or track is disabled, clicking the Fusion page button takes the first enabled clip

under the playhead. In this case, it switches to the Fusion page with only the sky image

from video track 1.


There is also no background node in the composition, so the resolution seen above

the frame is now defined by the original source image resolution (3888 x 1518). Now

you’re compositing with the highest-quality sky image, but you still need to bring in the

video track 2 clip.

**5** Open the media pool, and from the Clips bin, click the metadata badge in the lower

right corner of the Blackmagic URSA clip.


**Lesson 3 Replacing a Sky** **65**


The metadata badge reveals a pop-up with some basic metadata about the clip. One

piece of the metadata is the resolution, which is 1920 x 1080. Dragging this clip from

the media pool into the Node Editor retains the clip’s native resolution.

**6** Drag the Blackmagic URSA clip to an empty place in the Node Editor and close the

media pool.

**7** With the MediaIn 2 node selected in the Node Editor, press 1 to see it in viewer 1.


Above the frame, the clip displays its resolution as 1920 x 1080.


Just like single elements brought in from the edit page, elements from the media pool

always retain their original resolution.


To keep the media organized, let’s rename the nodes so that the names are more

descriptive.

**8** Rename the MediaIn1 node to **Sky** and the MediaIn2 node to **Actors** .


With all the media at its highest resolution and our nodes named appropriately, we can

begin by merging the Actors over the Sky. However, since the Merge node is used so

often, this time we will learn a special quick method of adding one to our composition.

**9** Drag the output of the Actors node onto the output of the Sky node to automatically

create a Merge node.


A Merge node automatically appears, connecting the Actors as the foreground and the

Sky as the background.


**Lesson 3 Replacing a Sky** **66**


**10** Select the Merge node and press 2 to see it in viewer 2.


Viewer 2 shows a composition that uses the resolution of the larger sky image with a

small 1920 x 1080 HD foreground in the middle.


A fundamental concept in Fusion is that the background input of a Merge node

determines the resolution of the Merge node’s output. This is how you can control the

resolution when mixing footage of different sizes. In our case, the background input is

the large sky image, not the full HD resolution of the foreground clip and timeline. To

correct the resolution of our composite, we will manually add a Background node that

was automatically created when we used the Fusion clip.


TIP The Resize and Crop nodes also modify the resolution of a clip.


**11** Drag the Background tool (the first tool at the far left of the toolbar) from the toolbar

to an empty place in the Node Editor.

**12** In the Inspector, click the Image tab.


The Background tool’s Image tab in the Inspector includes controls for the background

image resolution.


**Lesson 3 Replacing a Sky** **67**


**13** Click the Auto Resolution button to disable the automatic resolution setting and

enter **1920** as the width value and **1080** as the height.


The background input of the Merge tool determines the resolution of the Merge tool’s

output. So by connecting a 1920 x 1080 HD image to the Merge’s background input,

we can set the composite’s resolution. The easiest technique to accomplish this is to

create a new Merge node to connect the Background node.

**14** Select the Background node, and from the toolbar, click to add a Merge node.


**15** Select the Merge2 node and press 1 to see the solid black color of the Background

node in the viewer.


The Merge node now uses a resolution of 1920 x 1080. If we connect the larger Sky

node to the foreground, it will be cropped (not resized) by the Merge2’s resolution.

**16** Click the connection line near the input of Merge1 to disconnect the Sky node.


**17** Drag the output of the Sky node to the green foreground input of the Merge2 node.


As soon as the connection is made, viewer 1 shows the Sky node at its full resolution

but cropped by the 1920 x 1080 Merge2 node.

**18** Drag the output of the Merge2 to the background input of the Merge1 node.


**Lesson 3 Replacing a Sky** **68**


TIP Click in the viewer and press Command-F (macOS) or Ctrl-F (PC) to fill the

viewer with the image.


The MediaOut1 loaded in viewer 2 shows exactly what we had on the edit page. One layer

lies over another without any transparency. That’s because the Merge1 places the

Sky foreground over the Actors (green foreground input over yellow background input),

and since there is no mask or alpha channel in the Actors, there is no transparency.
## **Compositing Using the** **Darken Apply Mode**


Compositing typically requires an alpha channel or matte, as we used in Lessons 1 and 2.

Mattes or alpha channels are used to tell the software which areas of the foreground it

needs to cut away to reveal the background. In our case, we have two elements, the

live-action scene of the actors and our sky picture, neither of which has an alpha channel.

When starting a sky replacement, some people might be inclined to reach for a Luma

Keyer immediately. A Luma Keyer is a tool that creates a matte based on the luminance

in an image, like an overexposed sky. However, it is usually not the right tool for sky

replacement. At least it’s not the right tool to handle the edges of a sky replacement. A

much better choice is to start with an apply mode located in the merge you already have.

**1** Select Merge1 and, in the Inspector, set Apply Mode to Darken.


**Lesson 3 Replacing a Sky** **69**


The Darken apply mode shows the darkest pixel wherever the foreground and

background overlap. Since the sky image is darker than the overexposed sky in the

actors’ clip, most of the sky image displays. However, there are lots of issues we

need to deal with before getting a good-looking sky replacement.


TIP The Channel Booleans node also contains a Minimum mode and can be

used in place of a Merge.


**2** Select the Sky in the Node Editor, and in the toolbar, click the Transform node.


Even though the larger sky image is cropped (not resized), you still have access to the

entire sky image. You are just looking at it through a 1920 x 1080 window. The

Transform node will allow you to reposition the larger sky frame within the crop window.

**3** In viewer 2, drag the center onscreen control slightly to the right to include more of

the rainbow. (The Center X control in the Inspector can be set anywhere from 0.6–0.7.)


**Lesson 3 Replacing a Sky** **70**


## **Adding Effects from** **the Effects Library**

Although switching to Darken mode in the previous section took care of the edges, we’ll

still make use of a Luma Keyer to handle the transparency we see over the actors and

water. Since the actors’ clip has no alpha channel built into it, a Luma Keyer can create

one for us.


Since we know the name of the effect we want to add, instead of using the toolbar or the

Effects Library, we can search for it using the Select Tool dialog.

**1** Click in an empty area of the Node Editor, to the right of the Actors node.


By clicking in an area of the Node Editor, you are identifying the location of the next

node you add using the Select Tool dialog.

**2** Press Shift-Spacebar to open the Select Tool dialog and type in **luma** to locate the

Luma Keyer.

**3** With the Luma Keyer highlighted in the dialog, press Return (macOS) or Enter (PC) to

add the tool to the Node Editor.


**4** Drag a second output from the Actors node and connect it to the yellow input of the

Luma Keyer.


**Lesson 3 Replacing a Sky** **71**


Nodes can have multiple outputs without causing any reduction in quality or

duplicating layers.

**5** Press 1 to see the Luma Key in viewer 1.


Right away, we can see a semitransparent checkerboard pattern that represents

transparency from the Luma Keyer settings. Because you will create a matte, it can

be helpful to view the alpha channel in the viewer instead of the RGB image that is

currently visible.


TIP An _alpha channel_ is a fourth channel that accompanies the red, green,

and blue channels of an image. Alpha channels determine which parts of an

image are opaque and which parts are transparent.


**6** In viewer 1’s toolbar, click the Color controls button and select the alpha channel (or

click in the viewer and press the A key).


The viewer displays a grayscale image that represents the transparency based on the

Luma Key. Areas that are pure white will be transparent, and areas of pure black will be

opaque. Areas of semitransparency will be some shade of gray.


**Lesson 3 Replacing a Sky** **72**


**7** In the Inspector, drag the High threshold slider to the left until the majority of the sky

appears solid white. The High threshold should end up at around 0.9.


An important thing to understand about mattes is that they need to contain pure black

and pure white. Gray areas, as mentioned above, will be a semitransparent mix of

foreground and background. That’s OK for glass objects, but most of the time, areas

will be either all foreground or all background. Right now, the sky is completely white,

but the foreground of the actors isn’t pure black.

**8** Drag the Low threshold slider slightly to the right to darken as much of the actors and

rock as you can without darkening the sky. The Low threshold should end up at

around 0.9.


**9** To smooth the harsh edges, drag the Blur slider to about 0.5.


We now have areas of mostly pure black and pure white. Unfortunately for us, there are

many highlights on the actors and some darker areas in the upper left of the sky that will

cause problems in our matte.


**Lesson 3 Replacing a Sky** **73**


## **Fixing Holes in a Key**

The remaining problems we have are the areas where white still shows through due to the

very bright highlights on our actors’ foreheads and clothes. Instead of laboriously drawing

a matte or painting out the holes, we will use an easier method. Enter the Erode/Dilate

node. An Erode/Dilate node expands or shrinks the edges of a matte.

**1** In the Node Editor, select the Luma Keyer, press Shift-Spacebar to open the Select Tool

dialog, and type **erode** .

**2** With the Erode/Dilate node selected in the dialog, press Return (macOS) or Enter (PC).


**3** Press 1 to view the added node in viewer 1.

**4** In the Inspector, in the Amount slider, type **-0.003** .


Moving the Amount slider left (negative) expands the edge of the matte covering up

the holes. Unfortunately, it also expands the border around the hillside edges. How

do we fix that? We’ll add another Erode/Dilate node and set the amount in the

opposite direction.

**5** Using the Select Tool dialog, add a second Erode/Dilate node directly after the

first Erode/Dilate.


**6** Press 1 to view the second Erode/Dilate in the viewer.


**Lesson 3 Replacing a Sky** **74**


**7** In the Inspector, in the Amount slider, type **0.007** .


TIP If a slider in the Inspector does not reach the value you want, you can often

type in the number to extend the slider’s range.


The Erode/Dilate has brought us closer to having a clean black-and-white matte, but visual

effects are often a game of whack-a-mole, where you fix two problems and reveal another.

The Erode/Dilate has not removed a few white spots in the actors that we will have to fix.

We also need to combine this newly generated matte with the actual RGB image of the

actors to get an idea of our finished shot.
## **Embedding Alpha into an Image**


The matte you created with the Luma Keyer must now be combined with the RGB image of

our actors. When combining mattes with RGB images, one of the most useful nodes is a

Matte Control node. One of its primary functions is to take the alpha channel from the

image connected to foreground input and copy it into the image connected to the

background input.


**Lesson 3 Replacing a Sky** **75**


**1** From the toolbar, drag the Matte Control tool to the Node Editor near the Erode/

Dilate2 node.


**2** Drag a third output from the Actors node to the yellow background of the

Matte Control.


The background input on a Matte Control is used to connect the destination image

where you want to embed the alpha.

**3** Press 1 to view the Matte Control in the viewer.

**4** Click the Color button above viewer 1 or press the C key to view the RGB channels

instead of the alpha channel.

**5** Drag the Erode/Dilate 2 node output to the green foreground input of the

Matte Control.


**6** To embed the alpha channel created by the Luma Keyer into the Actors image, in the

Inspector, set the Combine menu to Combine Alpha and enable Post Multiply Image at

the bottom of the Inspector properties.


**Lesson 3 Replacing a Sky** **76**


By choosing Combine Alpha, we’re telling Fusion to copy the alpha channel from our

Luma Key (entering the node on the foreground input) into the alpha channel of our

Actors image (coming in on the background input).


OK, but why did we check the Post Multiply Image option? The short answer is that

there are two types of alpha channels. Premultiplied alpha channels are typically

created by computer graphics in combination with the RGB image. Straight alpha

channels are commonly created by image processing separate from any RGB image, as

we have done here with the Luma Key. The Merge node in Fusion always assumes that

the incoming foreground image with alpha is premultiplied. Since ours isn’t yet, we

need to perform the premultiplication.


TIP The checkbox is called Post Multiply simply because it’s happening after

(post) the alpha channel has been added to the main RGB image. The result is

a premultiplied image.


You now have the actors with an embedded alpha channel, but if you look in the

viewer, all you’ll see is the washed-out sky we’re trying to replace. Typically, in a matte,

the white areas are opaque, and black areas are transparent. That is the opposite of

what we have. So we’ll invert the matte.

**7** In the Matte Control’s Inspector, click the Invert Matte checkbox (just above the Post

Multiply Image checkbox).


**Lesson 3 Replacing a Sky** **77**


Before going any further, it helps to view the composite of the foreground with the sky.

The Matte Control output forms our new foreground with alpha, while the output of

Merge1 contains the nice clean edges for our composite. Now you’ll merge the

two together.

**8** Select the Merge1 node and click the Merge tool in the toolbar to add a third Merge.

**9** Drag the output of Matte Control to the green foreground input on the Merge3 node.


**10** Select the MediaOut node and press 2 to view it in viewer 2.

**11** Click the Play button to review the composite.


The results are displayed in viewer 2. The image is much closer to what we want, but the

sky appears very flat and fake, so fixing that will be your next task.
## **Tracking the Sky into Position**


As you play the composite, it looks fine when the image is still, but as soon as it plays and

the camera moves, the illusion falls apart. For this sky replacement to work, the sky must

move as the camera moves. Instead of using the Tracker node as you did in the previous

lesson, you’ll apply the Tracker as a modifier.

**1** Select the Merge2 node that is connected to the Sky node in the Node Editor.


**Lesson 3 Replacing a Sky** **78**


You’ll need to apply the Tracker modifier to a node that contains position controls.

The Merge tool includes center X and Y controls that can be used to reposition the

clip connected to the foreground input.

**2** In viewer 2, right-click over the Merge’s center onscreen control, and from the menu,

choose Merge 2: Center > Modify With > Tracker position.


TIP Alternatively, you can right-click over the center control in the Inspector to

attach the Tracker.


The Tracker modifier is attached to the Merge’s center X and Y controls. Although the

process of tracking is the same as the Tracker node, the Tracker modifier is a single
point tracker that tracks up and down and side to side movement, so it is more limited

than the multipoint tracker you used in the split screen. Still, it is perfect for quick,

simple tracks, as we have here.


**Lesson 3 Replacing a Sky** **79**


Adding a Tracker modifier displays the tracker pattern and search rectangles over the

center position in the viewer. Since it is a modifier, the tracker controls are displayed in

the Merge2’s Modifiers tab.

**3** At the top of the Inspector, click the Modifiers tab to display the tracker controls.


The Tracker modifier assumes that you want to track the background of the Merge

node. In our case, however, we want to track the Actors node.

**4** From the Node Editor, drag the Actors node to the Tracker source field at the top of the

Inspector.


NOTE As you drag a node from the Node Editor into an Inspector source field,

the node will appear to move at first but will snap back into its original location

once the mouse pointer leaves the Node Editor.


**5** Move the playhead to the start of the render range.


Just as you did in the previous lesson, you need to position the Tracker over a high
contrast pattern that moves precisely how you want the sky to move. For this shot, the

ridge in the background has a few rocks that stick out. These would make good

high-contrast tracking points that we can use for the Tracker.


**Lesson 3 Replacing a Sky** **80**


NOTE As in Lesson 2, this lesson describes using the Point tracker found in

DaVinci Resolve and DaVinci Resolve Studio. When using DaVinci Resolve 20

Studio, the default is to use the new Intellitrack. The steps are identical in

this lesson except for step 6. If you are using Intellitrack, you reposition the

tracker by dragging the center of tracker point, not the handle as described

and shown in step 6. All the remaining steps work for both the Point tracker

and Intellitrack.


**6** In viewer 2 drag the handle in the upper left corner of the pattern box to position the

Tracker over the very small, sharp rock sticking up from the ridge between the

two actors.


Unlike when viewing the Tracker node, the pattern box does not expand to show a

magnified view of the area you are over. However, the Inspector does contain a small

preview of the selected area.


Since this camera does not move very fast, we can leave the search rectangle at its

default size.

**7** In the Inspector, click the Track Forward button to begin the tracking process.


The viewer displays the progress of the track even though it clearly jumps around frame 90

when the actor’s head obscures the rock. You’ll need to find a way to continue the tracking

for the remainder of this clip. Although the rock you initially selected is fine for the first half

of the clip, it won’t be the solution for the second half.


TIP If the tracker is interrupted prior to frame 90, try repositioning the pattern

box or making the pattern box slightly smaller, and then track the clip again.


**Lesson 3 Replacing a Sky** **81**


## **Fixing Interrupted Trackers**

You now have a solid track for the first 90 frames or so, but you’ll need another solution for

the remaining 70 frames. Instead of giving up hope, you can keep the tracking data of the

initial rock you selected for the first half of the shot and now identify a new tracking point

for the remainder of the shot.

**1** In the render range, drag the playhead to frame 90.


This is the last good frame of tracking data from the first rock you tracked. At this

point, you need to locate a new high-contrast object to track.

**2** If the Track1 section of the Modifiers tab has closed, double-click the label Track1 to

re-open it.

**3** In the Inspector, set the Path Center menu to Track Center (Append).


**Lesson 3 Replacing a Sky** **82**


The Track Center (Append) setting allows you to move the pattern box over a new

object and continue the tracking based on this new point.

**4** In viewer 2, drag Tracker2’s handle in the upper left corner of the pattern box to place

the tracker over the sharp rocks on the right side of the actress.


**5** Click the Track Forward button to pick up the tracking process from frame 90.


Fusion automatically blends the two analyses for Tracker1 to create one seamless motion

path. You now have a steady track that follows the position of the camera movement. Since

you applied the tracker as a modifier to the Merge center X and Y, the motion of the sky

automatically follows the tracker.


TIP If you notice black at the edge of the frame, it might be that the tracking data

is pulling in black from outside the sky image’s frame. To fix this, simply readjust

the sky positioning using Transform1.

## **Blending In the Original Sky**


If you leave the sky replacement as it appears now, it just looks like a pasted-on sky.

By color-correcting the Sky clip, we can adjust how it blends with the original sky, creating

a more natural composite.

**1** Select the Sky clip and add a Color Corrector node using the Select Tool dialog

(Shift-Spacebar).


**Lesson 3 Replacing a Sky** **83**


**2** Adjust the Gamma up to blend back some of the original sky. A value of around 1.5

should work.


Some sky replacements require a few mattes, and some require none. Some might require

a bit of color correction to get the foreground and background to match better. The goal of

this lesson was to give you a basic structure you can build on for any sky replacement you

may come across.


Completed node tree for Lesson 3.


**Lesson 3 Replacing a Sky** **84**


## **Lesson Review**

**1** True or False? Clips from the media pool use the timeline resolution when added to the

Fusion Node Editor.

**2** True or False? The Merge node contains apply modes such as Screen, Multiply,

and Darken.

**3** True or False? To offset a tracking point when a pattern becomes obscured, you must

create a new tracking point.

**4** True or False? Tracker modifiers have all the same controls and functionality as the

Tracker node.

**5** True or False? A Luma Keyer is used to create a mask from the brightness in an image.


**Lesson 3 Replacing a Sky** **85**


##### **Answers**

**1** False. Adding a clip from the media pool to the Node Editor uses the clip’s native

resolution.

**2** True. The Merge node contains apply modes such as Screen, Multiply, and Darken.

**3** False. To offset a tracking point, you must set the Path Center menu to Track

Center (Append).

**4** False. Tracker modifiers track only a single tracking pattern, while a Tracker node

can track multiple patterns.

**5** True. A Luma Keyer is used to create a mask from the brightness in an image.


**Lesson 3 Replacing a Sky** **86**


### Lesson 4
# Replacing Signs and Screens



You’ve learned how to match move

using the standard Tracker; now it’s

time to learn a more sophisticated

method that is ideal for replacing

tablet screens, billboards, or signage

on the sides of vehicles. This type of

match move is most efficiently done

using a Planar Tracker. Planar tracking,

as the name suggests, relies on

there being a flat, planar surface for

it to work.



Time

This lesson takes approximately
40 minutes to complete.

Goals

Tracking Planar Surfaces 88

Painting with the Clone Tool 93

Using Photoshop PSD Layers 96

Combining Mattes and Images 102

Match Moving with the Planar
Transform 104

Finalizing the Composite 106

Lesson Review 109


In this lesson, you’ll add a new sign to the side of a moving van. The process of adding a

new sign to a moving vehicle (or a screen to a tablet) is made up of three parts. First, you’ll

need to track the flat surface as it moves. Then, using Fusion’s Paint tool, you’ll remove any

tracking markers to create a clean surface. Once that is complete, you can composite a new

logo using the tracking data.


Completed composite for Lesson 4.

## **Tracking Planar Surfaces**


As you have experienced so far, the single-point tracker is the simplest tracker in the

Fusion page. Although it works well on many shots, it’s not the most optimal tracker in

some specific cases. For instance, what happens if the camera changes perspective? No

matter how many point trackers you use, they are still independent 2D points that can only

process limited camera motion. A Planar Tracker tracks multiple points across a defined

flat surface, such as a billboard, TV screen, or as in the case in this lesson, the side of a van.

In doing so, it calculates a more accurate 2.5D track that can contain more complex

motion. Let’s take a look at our clip.

**1** Open DaVinci Resolve 20 and, from the Project Manager, open the

**DR20 Fusion VFX Lessons** project into the edit page.

**2** In the Timelines bin, double-click the **Fusion VFX Lessons-START** timeline.


**Lesson 4 Replacing Signs and Screens** **88**


**3** Move the playhead over the third edit and the third red marker, and press Shift-5 to

switch to the Fusion page.


**4** Press the Spacebar to view the clip.


This shot of the van will ultimately need a sign added as it drives off. However, the first

part of the composite is to track the van’s movement, so when you ultimately add the

new logo, it will move across the shot as the van moves.

**5** In the upper left of the user interface toolbar, click the Effects Library button to reopen

the panel.

**6** Select the Tools > Tracking category and insert the Planar Tracker tool between the

MediaIn1 and the MediaOut1 nodes.


**7** Close the Effects Library to give yourself more space.

**8** Press 1 to see the Planar Tracker in the viewer.


It’s important to start planar tracking on a frame where the area you are tracking is

clear and large in the frame. In this case, frame 65 is ideal because the side of the van

is large in the frame but moving slowly, effectively eliminating motion blur.


**Lesson 4 Replacing Signs and Screens** **89**


**9** Move to frame 65 in the comp.


Unlike the tracker that you used in the previous exercise, the Planar Tracker does

not use one or two tracking patterns. Instead, it tracks the motion, scaling, and

perspective distortions of an entire planar surface in a background clip. So the next

step is to identify the planar surface you want to track.


When the Planar Tracker is added, the polygon shape toolbar appears above the viewer.

The same functionality you used previously to create polygon shapes applies here.


TIP If a clip has any significant lens distortion, it should be removed using a

Lens Distort node before performing a planar track.


**Selecting a Good Area for Planar Tracking**

When drawing a shape around the area for planar tracking, keep the following

guidelines in mind:


 - Select as large an area as possible.

 - Select an area that stays in frame as much as possible.

 - Select an area that is clear of obstruction from moving foreground objects.

 - Start your track when the area you are tracking is at its maximum size.

You want as much detail in the area as possible when you begin the track.

 - Make sure everything included in the selection is part of the same rigid body.

That is, make sure you don’t include any area with independent motion, such

as, in this example, the background behind the van or even the rotating tires.

 - Start your track on a frame in which the area is the least distorted.


**Lesson 4 Replacing Signs and Screens** **90**


**10** In viewer 1, draw a very simple shape that fits around the side of the van. Do not go

outside the van, and do not include the wheels.


The area inside your shape is the pattern that will be tracked over time.


TIP When defining the area to track, include only pixels inside the shape that

belong to the plane being tracked (in this case, the side of the van). Do not

include any of the background area.


**11** At the top of the Inspector, click the Set button.


The current frame is set as the reference frame for the rest of the track.


TIP If you stop before the tracking is completed, you must re-click the Set

button before resuming the tracking process.


**Lesson 4 Replacing Signs and Screens** **91**


**12** At the bottom of the Inspector, click the Track to Start button.


The viewer shows the tracking as it progresses backward to the start of the shot.

When it is done, a series of dots appears in the render range to indicate that the

track is completed.

**13** When the first half of the track is done, return to the Inspector and click the Go button

to move the playhead back to frame 65. Then click the Track to End button.


Despite the majority of the van disappearing offscreen, the Planar Tracker continues to

track right to the end of the clip.

**14** To test the track, in the Inspector, change the Operation Mode pop-up menu to Steady

and play the clip. (Make sure you have the Planar Tracker node and not the MediaIn

node displayed in a viewer.)


The side of the van should stay locked in place throughout the timeline playback.

**15** Reset the Operation Mode pop-up menu to Track.


The Steady setting is obviously not what you’re trying to accomplish for the shot, but it’s a

good way to evaluate a track and ensure that there’s no drift or bumps in the tracking data.

If you do see errors, readjust your tracking shape at frame 65 and try again.


**Lesson 4 Replacing Signs and Screens** **92**


## **Painting with the Clone Tool**

With the tracking done, we can now focus on removing the tracking markers. You will

create a clean side of the van using the Paint tool to clone white areas of the van over

each marker. You just need to freeze a single frame to paint over, and then cut out the

clean side of the van and composite it over the live full-motion shot. Let’s start by freezing

the frame we want to paint over.

**1** In the Effects Library, navigate to the Tools > Miscellaneous category, and drag the

Time Speed tool into an empty part of the Node Editor.


The first part of this job is to freeze the van on a clear frame. Freeze frames from the

edit page do not transfer into the Fusion page, but it is easy enough to create a freeze

frame using Fusion’s Time Speed node.

**2** Drag from the MediaIn1 output to the yellow input on the TimeSpeed1 node.


Dragging a second output from the MediaIn node is similar to duplicating a clip in

a timeline.

**3** Press 1 to load the Time Speed node into the viewer.

**4** Go to frame 65 and then in the Inspector click the Freeze Frame button.


**Lesson 4 Replacing Signs and Screens** **93**


A freeze frame is created for frame 65, which holds for the duration of the clip.


The frame number used for the freeze frame is displayed in the Delay parameter value.


TIP The Time Speed frame numbers are based on the entire clip length, not

the duration of the clip in the timeline.


Now, you’ll paint out the markers on this freeze frame.

**5** In the Node Editor, select the Time Speed. In the toolbar, click the Paint tool to connect

it after the Time Stretcher.


**6** Press 1 to see the Paint tool in the viewer.


With the Paint tool selected, the Inspector changes to show various paint controls, and

a viewer toolbar is displayed above the viewer with the various paint stroke types.


The Paint tool offers several stroke and paint styles suitable for motion graphics or

retouching shots. In this exercise, you’ll use a simple stroke brush in Clone mode to

copy white areas of the van and paint over the markers.

**7** In the viewer toolbar, click the Stroke tool.


The Stroke tool is the most versatile of paint tools and the one you will use for most

paint tasks.


**Lesson 4 Replacing Signs and Screens** **94**


**8** In the Inspector, click the Clone Apply Mode button to switch from painting with color

to painting with a clone brush.


The clone brush works by selecting a source area from a frame and a destination area.

The source area is the area in the frame you want to duplicate as you paint. The

destination area is the area you will paint over using the content of the source area.

**9** Option-click (macOS) or Alt-click (PC) to the left of the first black marker in the upper

left of the van to select the source area offset for the clone brush.


**10** Once you’ve selected the source area offset for the clone brush, paint over the

first marker.


As you paint, the source area offsets by the same amount. For instance, when you

paint upward, the source area selection also moves up. It is often good to keep the

source selection near the area you will paint over, because doing so keeps the texture

and color of the two areas as similar as possible.


TIP You can hold down the middle mouse button and drag in the

viewer to pan.


**Lesson 4 Replacing Signs and Screens** **95**


**11** If necessary, Option-click (macOS) or Alt-click (PC) a new offset for the next marker and

paint over it. Command-drag (macOS) or Ctrl-drag (PC) to resize the brush. Continue

choosing a new offset and painting over each marker until all the markers

are removed.


You now have a clean van, perfect for compositing a new logo. In the next exercise, you’ll

import a logo and learn how to blend it onto the side of the van.
## **Using Photoshop PSD Layers**


DaVinci Resolve can use various still-image formats for graphics, including TIFF, JPEG, and

PNG. It can also use layered Photoshop files, allowing you some flexibility when it comes to

selecting the layer you want to use from the PSD graphic.

**1** Go to frame number 65 and ensure that nothing is selected in the Node Editor by

clicking in an empty area.


**Lesson 4 Replacing Signs and Screens** **96**


**2** From the Fusion menu, choose Import > PSD. Then, navigate to the DR20 Fusion VFX

Training Media folder > Graphics, and import the **PIZZA SIGN.psd** file.


Once it’s imported into the Node Editor, you will get a node representing each layer in the

file and two Merge nodes, labeled Normal and Normal1, that combine the three layers

together. The Merge nodes are renamed to identify the blend mode used in Photoshop.


TIP Layered Photoshop files brought into Fusion through the media pool do

not display as multiple nodes. They are displayed as a multilayer MediaIn node,

which provides access to the individual layers from the Inspector.


**3** With the Normal1 node selected, press 1 to see it in the viewer.


**Lesson 4 Replacing Signs and Screens** **97**


This photoshop image is 1920 x 1080 resolution and includes three layers. One layer is

the company name, another is the logo, and the third layer is the phone number. Using

the output of Normal1, you can composite it over the van.

**4** Connect the output of the Normal1 node to the output of the Paint1 node to create a

Merge node.


TIP This graphic was created by exporting a reference frame (frame 65) to

create the graphic with the correct perspective. If a graphic does not have the

correct perspective, you can use a Corner Pin node in Fusion.


**5** With Merge1 selected, press 2 to view it in the viewer on the right.


This looks just like what it is: a photoshop document placed on top of the van clip.

However, with some blending you can make it appear much more realistic.


**Lesson 4 Replacing Signs and Screens** **98**


**6** In the Inspector, set the Apply Mode to Soft Light.


The Soft Light apply mode is a good choice because it softly lightens the logo based on

the white van color, giving the logo a nice diffused look, However, since the crease lines

in the van are darker than much of the logo, the logo is darkened in those areas. The

result is good but maybe a bit too light and diffused. We can improve it a bit using

some simple color correction.

**7** Select the Normal1 node and, from the toolbar, insert a Brightness/Contrast node.


**8** Adjust the Lift down to darken the black part of the logo and increase the Contrast

slider until the logo appears less diffused.


**Lesson 4 Replacing Signs and Screens** **99**


Although it’s looking much better, the edges of the graphic have become a bit ragged.


This is a common problem that occurs when you perform color correction on an image

with a premultiplied alpha channel. To correct this problem, you can enable the

Pre-Divide/Post-Multiply checkbox in the Color Corrector.


To correct this, we must pre-divide before the color correction and post-multiply after

it. We can do both with just one checkbox in the Brightness Contrast node.

**9** With the Brightness Contrast node selected, click the Pre-Divide/Post
Multiply checkbox.


You now have a great-looking logo that just needs a bit of positioning to appear as if it is

actually painted on the side of the van.


**Lesson 4 Replacing Signs and Screens** **100**


**Lesson 4 Replacing Signs and Screens** **101**


## **Combining Mattes and Images**

So far, you have a freeze frame of the entire shot, but you need to isolate the side of the

van with the logo to composite it. This is where the rotoscoping technique you learned

earlier comes in handy. You’ll create a matte that isolates just the side of the van.

**1** Go to frame 65, and then, from the toolbar, drag the Polygon tool into an empty area

of the Node Editor near the Merge tool.


**2** With the Polygon tool selected, draw a shape around the side of the van using the

creases by the door and roof to guide your matte. Be sure to close your matte by

connecting the last and first control points or by pressing Shift-O to connect

them automatically.


**Lesson 4 Replacing Signs and Screens** **102**


You now have a matte, but you have nowhere to connect it into the node tree. None of

the available blue effect mask inputs are the type of mask input you need. An effect

mask limits the area of an effect. What you are doing is combining an image with a

matte, effectively cropping the image. This type of mask is often called a _garbage_

_matte_ . You need to add a node that can accept a garbage matte input. The most

commonly used node for this purpose is called a Matte Control node.

**3** In the Node Editor, select the Merge1 node and, from the toolbar, add a Matte Control.

**4** Press 1 to see the Matte Control in the viewer.


The Matte Control is typically used to copy or combine mattes from a foreground to

a background. In this situation, you’ll use it to copy a matte to the background freeze

frame. However, because the Matte Control has several possible inputs, you need a

way to ensure that you select the correct one.

**5** Option-drag (macOS) or Alt-drag (PC) from the Polygon output to the Matte Control

node and release the mouse button.


When you release the mouse button, a pop-up menu appears listing all the possible

inputs of the matte control. This menu makes it easier to select the correct input.


For this task, you want to use a garbage matte.

**6** In the pop-up menu, click the Garbage Matte to connect the Polygon.


The viewer now shows a hole where the side of the van used to be. Your matte is used

to cut out the side of the van rather than isolating it. You can use the Inspector to

reverse this operation.


**Lesson 4 Replacing Signs and Screens** **103**


**7** With the Polygon node selected, in the Inspector, click the Invert button.


The side of the van with the logo is the only part seen from the freeze frame. You can now

composite this still image over the top of the moving image using the Planar Tracker data

to move it in sync with the full-motion shot.
## **Match Moving with the Planar** **Transform**


For simple corner-pinning images, you can connect directly into the Planar Tracker.

However, when you’re working with irregular polygon matte shapes or anything other than

images of the same aspect and resolution of the composition, the more appropriate

method is to use the Planar Transform.

**1** In the Node Editor, select the Planar Tracker node.

**2** At the bottom of the Inspector, click Create Planar Transform.


A Planar Transform node is created that contains all the transform and perspective

distortion data captured by the Planar Tracker. You can apply this data to any input

image or matte, thereby saving lots of time compared to rotoscoping objects.


**Lesson 4 Replacing Signs and Screens** **104**


**3** Connect the output of the Matte Control to the yellow input of the Planar Transform.


**4** Press 1 to view the Planar Transform in the viewer.

**5** Drag through the render range to preview the match-moved side of the van.


The freeze frame of the van’s side now follows the driving motion. The next step is a

simple merge to composite the van side over the moving van shot.

**6** Select the Planar Tracker and press Delete.


Once you have the Planar Transform, there is no need to keep the Planar Tracker. All

the data captured from the tracking is now stored in the Planar Transform.

**7** From the toolbar, drag a Merge node over the connection line between the MediaIn1

and the MediaOut1 nodes to insert it.


**8** Drag the output from the Planar Transform node to the green foreground input of the

Merge2 node.


**9** Select the MediaOut node and press 2 to see it in the viewer.

**10** Press the Spacebar to play the entire shot.


You now have fairly convincing results. In the next exercise, you’ll address a few little

cleanup areas to finish this shot.


**Lesson 4 Replacing Signs and Screens** **105**


## **Finalizing the Composite**

If you look carefully at later frames (such as frame 90), you’ll see a clear shift in the

shadows between the masked region and the moving van.

**1** Move the playhead to frame 90.


Looking at the back end of the van, you’ll notice a common problem resulting from the

shadows changing in the live shot. Your freeze-frame lighting is baked in and doesn’t

update with the moving shot. A simple blur could disguise the seam. However, because

the clean van goes right to the top of the roof, you’ll use the variable soft-edge on the

Polygon tool only where needed, toward the base and back of the van.

**2** Move to frame 65.


TIP It’s important to always perform changes to a matte on the original frame

where the adjustments were made. Doing so will avoid accidentally adding

keyframes and interpolating between adjustments.


**Lesson 4 Replacing Signs and Screens** **106**


**3** Select the Polygon node and, at the top of the viewer, click the Make Double

Poly button.


**4** Right-click over one of the control points on the back end of the van and choose

Controls > Select > Polygon 1: Outer Polygon.

**5** Drag the middle control point along the right edge of the shape to create a soft

transition edge.


TIP If you need to move a second control point, first click off into the gray

area of the viewer to deselect the initial control point. Then hold Command

(macOS) or Ctrl (PC) as you drag the second control point.


**6** Select the MediaOut1 node to hide the onscreen controls for the Polygon node, and

play the clip to preview the results.


The matte now looks clean. The final touch to make our logo appear more natural is to

fix the “strobed” motion that the logo appears to have. This is due to the original

camera footage having motion blur as the van gathers speed and our graphic having

no motion blur.


**Lesson 4 Replacing Signs and Screens** **107**


**7** With the Planar Transform node selected, in the Inspector, click the Settings tab.

**8** Click the checkbox for Motion blur.


The default blur seems a little strong for the shot, so you’ll dial back the shutter angle.

You’ll also increase the quality of the blur to remove any visible stepping.

**9** Adjust the Shutter Angle down to 130.0 and the Quality up to 5.


With that, the shot is complete. The technique you learned here can be used to replace

many different objects in a shot, from simple street signs to touchscreens and even

tattoos. Creating the clean surface with the Time Stretcher, Paint tool, and Polygon Spline

gives you a very simple but powerful recipe for common problems that may arise in a shot.


Completed node tree for Lesson 4.


**Lesson 4 Replacing Signs and Screens** **108**


## **Lesson Review**

**1** True or False? You must click the Set button before you begin planar tracking.

**2** True or False? When drawing a shape around a surface for planar tracking, you should

include as much of the background as possible.

**3** Which of the following make for good planar tracking surfaces:

**a)** Side of a building

**b)** Billboard

**c)** A bouncing ball

**d)** All of the above

**e)** None of the above

**4** True or False? The Planar Transform can be used to track planar surfaces and

composite the results.

**5** True or False? When cloning with the Paint tool, you hold the Option (macOS) or Alt

(PC) key and click to select the clone offset source, and then keep the Option or Alt key

pressed while you paint over the destination.


**Lesson 4 Replacing Signs and Screens** **109**


##### **Answers**

**1** True. Clicking Set identifies the reference frame for the planar tracker.

**2** False. When drawing a shape around a surface for planar tracking, you should not

include any of the background.

**3** a) and b) are ideal for planar tracking. c), the bouncing ball, is not a planar surface and

therefore not a good option.

**4** False. The Planar Transform uses the tracking data from a Planar Tracker and applies

its input image to it. The Planar Transform has no compositing capabilities.

**5** False. When cloning with the Paint tool, you hold the Option (macOS) or Alt (PC) key

and click to select the clone offset source, and then release the Option or Alt key when

you begin painting over the destination.


**Lesson 4 Replacing Signs and Screens** **110**


### Lesson 5
# Compositing Green‑Screen Content



Green- or blue-screen keying is the

classic visual effects work that comes

to mind for most people. A foreground

subject is shot against a bright blue or

green screen, which is then keyed to

make it transparent, thereby allowing

the subject to be placed on a new

background.



Time

This lesson takes approximately
90 minutes to complete.

Goals

Creating a Clean Plate 112

Fine-Tuning with the Delta Keyer 115

Rotoscoping Auxiliary Mattes 120

Lining Up the Background 129

Color Correcting Elements 131

Sending a Matte to the
Color Page  134

Lesson Review 137


The keying process is a procedural method of generating a matte, rather than the

manually drawn mattes you used in previous lessons. The process of compositing with

green screen is really an art in itself, but a simple workflow can be followed for most keys.

The trick is not to try to do everything with a single keying node. Focus the keyer on the

fine detailed edges of your foreground subject, and then you can manage other areas with

other tools. In the end, combining multiple mattes together will always get you better

results quicker.


Completed composite for Lesson 5.

## **Creating a Clean Plate**


We’ll start this lesson by opening the same project we’ve been using throughout the last

three lessons.


NOTE The Timelines bin includes a Backups bin with timelines saved at various

stages of the lesson and a Completed Projects bin with finished compositions.

These bins are both available for reference and reverse-engineering the

node trees.


**Lesson 5 Compositing Green‑Screen Content** **112**


**1** Open DaVinci Resolve and, in the Project Manager, open the **DR20 Fusion VFX**

**Lessons** project that you have been using for the previous three lessons.

**2** From the Timelines bin, double-click the **Fusion VFX Lessons-START** timeline. Then go

to the last red marker, which is over the green screen of our musician.

**3** Click the Fusion page button.


This shot from a Steve Vai music video is typical of a professional green-screen shoot.


Unlike computer-generated images, this live-action green-screen shot does not

include an alpha channel. So it is up to you to create the matte through keying similar

to how you used the Luma Keyer in Lesson 3. However, unlike the Luma Keyer, Fusion

provides a handy tool called a _clean plate_ that makes extracting a subject from a blue

or green screen so much easier.


NOTE In this lesson, the shot you will work on uses a green screen, but the

keying process works the same for blue-screen content.


**4** In the Node Editor, select the MediaIn1 node, and rename it **GreenScreen** .

**5** In the upper left corner of the interface, click the Effects Library button. All the tools

for keying are located in the Tools > Matte category.


**Lesson 5 Compositing Green‑Screen Content** **113**


**6** Click the tools disclosure arrow and select the Matte category. Click the Clean Plate

and then press 1 to see it in the viewer on the left.


Because the Green Screen node was selected in the Node Editor, the Clean Plate is

connected to the Green Screen output.


The Clean Plate tool is a node used before you do anything else with the green screen.

It is used to generate an image of pure green or blue color as if the subject (in this

case our musician) was never there. The output of the Clean Plate is later connected to

the Clean Plate input on the Delta Keyer so it can refine the matte with less effort.


You begin similarly to using a keyer, by selecting the screen color in the viewer.

**7** From the Inspector, drag the background color Eyedropper and move it over the green

screen in viewer 2.


You end up with a transparent cutout that represents everything that is not part of the

green screen.


NOTE In this exercise, we won’t provide exact values for every parameter.

Keying is an _iterative_ process—adjustments made in one area often require

you to revisit and refine earlier settings. As you progress, don’t hesitate to

return to any parameter and tweak it based on how later steps affect the

overall result. Effective compositing is rarely linear— _refinement is part of_

_the workflow_ .


**Lesson 5 Compositing Green‑Screen Content** **114**


The next step is to remove any errant non-green edge pixels from the cutout with the

green screen. To do this, you’ll use the Erode control to expand the pre-matte, and

then use the Grow Edges control to fill in the cutout.

**8** In the Inspector, increase the Erode slider by a small amount, just enough to expand

the edges of the guitarist silhouette, and then increase the Grow edges by a

similar amount.

**9** Click the Fill checkbox to fill in the remaining cutout with green. Feel free to refine

either the Erode or Grow edges value to achieve a cleaner green screen.


You will still see some varying shades of green where you filled in the cutout, but all of

that gets covered up by our musician. We are only interested in filling in the cutout

with shades of green. Now you can use the results to feed the Delta Keyer to get a

clean key.
## **Fine-Tuning with the Delta Keyer**


Whenever you are keying, it is helpful to use two viewers: one where you can see the final

output, and the other where you can view the quality of your matte.

**1** Click in an empty area of the Node Editor, just below the Clean Plate node.

**2** From the Matte category in the Effects Library, click the Delta Keyer to add it to the

Node Editor, and then close the Effects Library.


The Delta Keyer is the primary tool used for green-screen and blue-screen keying in

the Fusion page. As powerful as it is, it is also very simple to use now that we’ve done

most of the heavy work with the Clean Plate.


**Lesson 5 Compositing Green‑Screen Content** **115**


TIP The term _chroma key_ represents a specific, simplified process of

extracting a matte based on a range of hue and saturation in an image.

Modern keyers like the Delta Keyer use a more sophisticated color difference

method to extract the matte.


**3** Select the Delta Keyer node and press 1 to display its output in viewer 1.


Your first step will be to connect the Green Screen node and the Clean Plate to the

Delta Keyer.

**4** Drag a second output from the Green Screen node into the yellow background input

of the Delta Keyer.


**5** Drag the output of the Delta Keyer to the input of the MediaOut node to replace the

existing connection.

**6** Hold the Option key (macOS) or Alt key (PC) and drag the output of the Clean Plate

node over the Delta Keyer node and then release the mouse button.


The pop-up menu that appears shows you all the inputs to the Delta Keyer so you

don’t have to remember which colored inputs are for which tools.

**7** Select Clean Plate from the list.


For convenience, Fusion draws an underlay pattern to indicate transparency. When

keying, however, it’s best to use one of the viewers to view your matte.


**Lesson 5 Compositing Green‑Screen Content** **116**


**8** Above viewer 1, click the Color Controls button, or click the mouse button in viewer 1

to make it the active window and press the A key.


The matte for your live-action shot is displayed in viewer 1. A single click of the

Eyedropper typically produces a matte with lots of gray (semitransparency).

**9** With the Delta Keyer selected, drag the Balance slider to the left until it is around 0.3.

The Balance slider takes more or less information from the colors other than the

screen color—in this case, red or blue.


Dragging it to the left causes blue to be more transparent, while dragging it to the

right causes red to be more transparent. Since there is a lot of red in this foreground

subject, dragging it to the left removes some of the transparency from the foreground.


Even with the cleanest green-screen keys, such as you have here, you must refine the

matte a bit to ensure that areas intended to be opaque appear as solid white, and the

areas intended to be transparent appear as solid black.

**10** Select the Matte tab at the top of the Inspector.


**Lesson 5 Compositing Green‑Screen Content** **117**


The Matte tab in the Delta Keyer contains parameters for modifying the density and

edges of the matte. It is arguably the most important tab in the Delta Keyer because

the quality of your matte determines the quality of your key. By adjusting the

Threshold sliders at the top of the Matte tab, you clamp the black and white cutoff

points. Values that fall below the Low Threshold setting are considered pure black

(transparent), and values that fall above the High Threshold setting are considered

pure white (opaque).


TIP As you make adjustments to the matte, zoom in to and/or expand the

viewer size to get a clearer look at the matte, especially around the fine

hair details.


**11** To clamp the darker gray areas, increase the Low Threshold slider by a very small

amount, and then clamp the brighter gray areas by decreasing the High Threshold

by roughly 25%.


Adjusting these sliders too high or too low can cause the fine details to merge

together. Don’t try for perfection at this point. Just get a solid black-and-white matte

without losing hair detail.


TIP When refining the key, you are primarily concerned with getting good

quality edges for your subject. The black transparent areas and the core of

your foreground subject can be handled using various types of mattes.


**Lesson 5 Compositing Green‑Screen Content** **118**


The next steps are very subtle adjustments using the Clean Foreground and Clean

Background controls. You generally apply these with an extremely light touch because

they tend to cause harsh matte edges, but they can also “fill in” the small holes that

appear in the black and white parts of the matte. As you adjust them, you’ll use a

combination of the keyboard and the slider to make very small-scale adjustments.

**12** To fill in any black holes in the white areas of the matte, hold the Command key

(macOS) or the Ctrl key (PC) and drag the Clean Foreground slider to around 0.00075.

**13** Drag the Clean Background slider to around 0.0004.


**14** Lastly, drag the Erode/Dilate down a tiny bit.


The Erode value is a perfect example of a parameter that you will want to return to and

refine after compositing in the background.


NOTE This content is compressed with a 4:2:2 chroma subsampling. As a

training exercise it works well, but the chroma subsampling will impact how

clean your results can be. Focus on the process and less on the

actual outcome.


It will be impossible to refine the matte to the point where it fixes every pixel of the frame

without also sacrificing some of the hair detail. You’ll find that for every shot, compositing

with green screen requires multiple tools that work together. However, the basic Clean

Plate and Delta Keyer combination is always a useful starting point for any key.


**Lesson 5 Compositing Green‑Screen Content** **119**


## **Rotoscoping Auxiliary Mattes**

Your matte still has unwanted areas such as the gray or semitransparent areas around

the lower legs. Sometimes, you won’t be able to key out everything, so you will need to pull

out the digital duct tape, more formally known as _auxiliary mattes_ .


Auxiliary mattes are mattes other than the main core matte created by the key. These

auxiliary mattes help to patch matte holes that are impossible to patch otherwise. Two

auxiliary mattes are used regularly on every keying job. One is the garbage matte that

removes areas of the set not covered by the green screen. The second is a holdout matte.

The holdout matte covers up unwanted semitransparent areas in the foreground that the

keyer didn’t catch. Let’s start with creating a garbage matte.

**1** Drag the playhead to the start of the render range.

**2** From the toolbar, drag a B-Spline tool into the Node Editor under the Delta Keyer.


**3** Select the B-Spline node and rename it **gMatte** .


When drawing a matte, it is sometimes easier to use a B-Spline tool rather than Bézier

splines as you have been doing. B-Splines produce smooth, curved edges without the

need to manage handles. For consistently smooth curved shapes (when you’re not

concerned with making extremely detailed shapes with lots of corners), B-Splines can

be easier to work with.


Let’s use the B-Spline tool to draw around the area you want to keep. We’ll first give

ourselves more drawing room by using only one viewer.


TIP When you draw a shape with a B-Spline curve tool, the control points you

set influence only the shape of the curve. The control points do not define the

location of the actual spline curve. That being the case, it is best to start by

drawing a very loose shape, and then adjust the control points to create the

curve you need.


**Lesson 5 Compositing Green‑Screen Content** **120**


**4** In the upper right corner of viewer 1, click the Single Viewer button and drag down on

the divider line between the transport controls and the toolbar to expand the viewer.


TIP To increase the viewer and give yourself additional drawing space, you

can drag down on the divider line between the transport controls and the

toolbar or click the Nodes button at the top of the screen to hide the Node

Editor completely.


**5** In viewer 1, draw a wide, rough shape around the guitarist.


TIP Similar to drawing a polygon spline, remember to close the matte by

clicking the first control point you added or by pressing Shift-O.


**6** Once you finish drawing the matte, Option-drag (macOS) or Alt-drag (PC) from the

gMatte output to the Delta Keyer node.


**Lesson 5 Compositing Green‑Screen Content** **121**


**7** Release the mouse button and, in the Input pop-up list, choose Garbage Matte.


TIP You can adjust the smoothness of a B-Spline’s curve by holding down the

W key, selecting the control point for the curve, and dragging left or right to

increase or decrease the smoothness.


Because you drew this garbage matte around the subject, the guitarist’s silhouette is

removed from the shot. You need to invert it.

**8** Select the gMatte node and, in the Inspector, click the Invert checkbox.


This matte is done only for a single frame, and this guitarist likes to move as he plays.

The drawing of polygon or B-Spline mattes and animating them over a series of frames

is called _rotoscoping_ . A basic rotoscoping technique is called _divide and conquer_ . The

divide and conquer technique bifurcates the clip with keyframes and continually

divides each section with keyframes until the motion of the object is covered. This

ensures that you only add keyframes when absolutely necessary.

**9** Move to the end of the render range.


By default, after you close a polygon shape, any change you make to a control point

adds a keyframe. Changes to the shape on different frames are interpolated. This

behavior makes it incredibly efficient to animate small changes to your matte as the

subject in your clip moves.

**10** Refine the shape to better fit around the guitarist by adjusting any of the control

points along the B-Spline.


**Lesson 5 Compositing Green‑Screen Content** **122**


TIP When animating a spline, you can move the entire shape by clicking the

Select All Points button in the viewer toolbar and then dragging the points to a

new area in the viewer. Moving the Center X and Y parameters or the onscreen

Center control will not add a keyframe.


When using the divide and conquer technique, the idea is to set keyframes at the

start, end, and middle of your animation. You then continue to divide those

segments by adjusting the shape to fit at halfway points between keyframes until the

shape’s movement in each segment accurately matches the object that you’re trying

to rotoscope.

**11** Move to the middle of the render range, around frame 255.

**12** Adjust the control points to fit around the guitarist.

**13** Repeat the process by dividing the keyframed sections from frame 231 through frame

255 so that the animated shape fits the guitarist throughout the moving shot.


TIP Pressing Option -] and Option-[ (macOS) or Alt-] and Alt-[ (PC) will move

the playhead to the next and previous keyframe, respectively, to help you

more quickly refine the polygon matte.


**14** Once you finish with the first half of the shot, divide the second half starting at frame

255 through frame 279. Adjust the shape wherever you feel a keyframe is needed,

continually dividing sections as you go.


Rotoscoping is a balancing act. The tighter your garbage matte fits around the subject, the

less you’ll need to push the Delta Keyer’s matte controls, which helps preserve fine details

like hair. But tighter mattes come at a cost—they require more keyframes and control

points, making them slower and more complex to animate. The key is to strike the right

balance between precision and efficiency.

##### **Rotoscoping a Holdout Matte**


Another auxiliary matte you will typically create does the opposite of the garbage matte.

A holdout matte fills in any holes that appear in the white matte of the foreground subject.

Some bright parts of the guitarist’s leather pants have caught green bounce light from the

screen, thereby creating holes in our matte. To correct this area, you’ll draw two polygon

shapes, one for each leg, that will cover up the dark gray holes in your matte.


**Lesson 5 Compositing Green‑Screen Content** **123**


**1** Move to the end of the render range, where you can clearly see the leg on the left

completely in the frame.


**2** From the toolbar, add a MultiPoly node into the Node Editor, next to the gMatte node,

and rename it **HoldOut** .


The MultiPoly node is a tool that allows you to draw multiple independent mask shapes

within a single node. This makes it much easier when rotoscoping body parts or any

complex mask that requires individual shapes to be created for a single object. We’ll

use this node to draw two different polygon shapes, one for each of his legs.

**3** In the Inspector, double-click the Polygon1 label in the Polygon list and rename

it **LegLeft** .


**Lesson 5 Compositing Green‑Screen Content** **124**


The MultiPoly node doesn’t auto-animate like the B-Spline node you used earlier

unless you enable animation.

**4** At the bottom of the Inspector, click the gray diamond to the right of the label “Right
click here for shape animation.”


NOTE Although we highly encourage you to attempt rotoscoping both legs, if

you are adamant about not doing any rotoscoping, you can load the Backup 3

timeline from the Backups > Green Screen bin, which has the rotoscoping

completed.


**5** In viewer 1, zoom in to the lower half of the musician’s body and draw a rough boot-like

shape for the leg on the left.


Starting with a rough shape and refining as you go is a good way to approach

rotoscoping. It can help you support a balance between shape precision, animation,

and speed.

**6** Move to the center of the render range around frame 255.


**Lesson 5 Compositing Green‑Screen Content** **125**


**7** Move the points of the shape to match the leg position, and then move to the start of

the render range and reposition the points again.


**8** Use the divide and conquer technique you learned earlier with the gMatte to adjust

the shape to fit the leg at halfway points between keyframes until the shape’s

movement in each segment accurately matches the leg on the left.


TIP You can click the Modify Only button in the toolbar above the viewer or

press Shift-M to move only the points that exist and not accidentally create

new points.


Once you are satisfied with the rough shape and motion on the LegLeft, you can begin

roughly outlining the leg on the right.

**9** In the Inspector, click the Polygon button to add a new polygon shape to the list.


**10** Double-click the Polygon name in the list and rename it **LegRight** .


**Lesson 5 Compositing Green‑Screen Content** **126**


**11** Once again, draw a very rough shape and then use the divide and conquer technique

to adjust the rough shape to fit the leg on the right.


With both legs roughed out, you can now go back and start refining the shapes. This

involves adjusting the edges, adding new points where needed, and correcting any

inaccuracies in your original rough pass.

**12** Press Shift-I or click the Insert and Modify button from the toolbar above the viewer.


**13** Go through each keyframe you have added and add new points to your shapes where

they are needed to better fit the rough shapes to the legs.


**Lesson 5 Compositing Green‑Screen Content** **127**


TIP Pressing Shift-S will smooth corners of the selected point, while pressing

Shift-L will create hard corners.


The hard edge of the mattes should be softened just a tiny bit. Each matte you create

has its own set of controls. You can access each one by selecting the matte in the

Polygon list.

**14** In the Inspector, select the LegLeft polygon from the Polygon list and then set the

LegLeft Soft Edge slider to 0.001. Then select the LegRight from the list and set its

Soft Edge with the same value.


When you have completed both legs, the holdout matte must be connected to a

different input of the Delta Keyer than your garbage matte. A holdout matte is

connected to the Solid input on the Delta Keyer.

**15** Option-drag (macOS) or Alt-drag (PC) from the HoldOut output to the Delta Keyer

node and, in the Input pop-up menu, choose Solid.

**16** Above viewer 1, click the Color Controls button, or click the mouse button in viewer 1

to make it the active window, and press the A key to return to viewing the full
color image.

**17** Click the Single Viewer button in the upper right corner of the viewer to return to

seeing two viewers.


TIP You can reset the zoom status of the viewers to show the full image by

clicking in the viewer and then pressing Command-F (macOS) or Ctrl-F (PC).


A note about garbage mattes and holdout mattes: Often people unaccustomed to creating

green-screen composites attempt to do everything in the keyer. Let me dispel that myth

right now. Using auxiliary mattes is not an admission of a failed key. The use of auxiliary


**Lesson 5 Compositing Green‑Screen Content** **128**


mattes means that you are being smart about your time and are aware of the entire

process. Use a keyer for what it’s good at: creating soft edges and extracting fine hair

detail. Use the auxiliary mattes to avoid wasting time fiddling with keyer controls for items

easily done with a spline shape.
## **Lining Up the Background**


You can only go so far adjusting the matte against a black background. Eventually, you

must view the foreground over the actual background clip to get a complete picture of

the matte quality.

**1** In the upper left corner of the interface, click the Media Pool button, and from the Clips

bin, drag the BKGD HD clip into an empty area of the Node Editor.


**2** Close the media pool to make more room for your viewers.

**3** Press 1 to see the clip in the viewer.


The viewer shows the background clip. By default, when adding a clip from the media

pool into the Fusion Node Editor, it brings the clip in at the start of the composition. If

you want to slide the clip to begin earlier or later, you can use the Keyframes Editor.

**4** In the upper right corner of the window above the Inspector, click the Keyframes

button to open the Keyframe panel.

**5** Click the Zoom To Fit button to center all the timeline tracks.


**Lesson 5 Compositing Green‑Screen Content** **129**


The Keyframes Editor shows all the tracks, including the Background node, which is

currently labeled MediaIn1. The Background node clip begins at frame 231 which is the

starting frame of the comp, and ends at frame 304. This is a full 25 frames after the

comp ends. You can use the Global In/Out controls in the Inspector to slide the

background clip so that the end of the clip aligns with the end of the comp.

**6** Select the MediaIn1 node in the Node Editor.

**7** At the top of the Inspector, position the mouse pointer between the two Global In/

Out handles.


**8** Drag the Global In/Out bar to the right until you get 280 on the Global Out.


Now you are using a later section of the Background clip in the comp.

**9** With the MediaIn1 node selected, press F2 and rename the clip **BackGround.**


To view the key over the background, you’ll use a Merge node.

**10** In the upper right corner of the window, click the Keyframes button to close the panel.

**11** Drag the output of the Delta Keyer to the output of the BackGround node to create a

Merge node.


**12** Drag the output of the Merge node to the MediaOut node to replace the

existing connection.


**Lesson 5 Compositing Green‑Screen Content** **130**


**13** Select the MediaOut node and press 2 to display it in viewer 2 to see the initial

composite.


Although this looks good for the amount of work we’ve done so far, the foreground and

background still look like very different images. The next step is to color correct both

elements so they appear as if they are in the same location.
## **Color Correcting Elements**


Color correcting the background and foreground is done for two reasons. The first is to

remove any green color that remains on the foreground subject, and the second is to

match the foreground and background so they realistically appear to exist in the same

setting. Let’s tackle the green tint issue first. The Replace Color at the bottom of the Matte

tab in the Inspector already includes a fair amount of spill suppression.

**1** Select the Delta Keyer and, in the Inspector, select the Matte tab.


Spill is created from bounced light reflecting off the green screen that spills onto the

foreground subject. Since removing that green spill is inextricably linked to the process

of extracting a matte, you will sometimes create holes in your foreground matte. This

is due to the Replace Color attempting to remove the green-screen color that has

spilled onto your foreground. You inevitably must balance the quality of the spill

suppression with the generation of the matte. A way around this dilemma is to set the

Replace Mode to Source.


**Lesson 5 Compositing Green‑Screen Content** **131**


**2** At the bottom of the Inspector, set the Replace Mode dropdown menu to Source.


Setting the Replace Color to Source reintroduces an amount of the original green
screen pixels instead of trying to remove them. However, you are now left with green

spill on the musician.


You can remove spill fairly easily using a Color Corrector node directly after the

Delta Keyer.

**3** From the toolbar, insert a Color Corrector node between the Delta Keyer and the

Merge1 node.


The Color Corrector node includes several modes for correcting highlights, midtones,

and shadows, as well as spill suppression.


**Lesson 5 Compositing Green‑Screen Content** **132**


**4** At the top of the Color Corrector Inspector, choose Suppress from the menu.


TIP Zoom in to the viewer as far as needed to view the changes as you reduce

the spill colors.


The Suppress wheel allows you to drag the control point for the desired spill color

toward the center, thereby reducing its saturation.

**5** To reduce the green and some of the bright yellow tint around the edges of the

foreground, drag the green and yellow control points toward the center of the

color wheel.


TIP In many cases, spill suppression can produce a noticeable reduction in

image brightness. You can counteract this effect by slightly raising luminance.


**Lesson 5 Compositing Green‑Screen Content** **133**


**6** With the Color Corrector node selected in the Node Editor, press Command-P (macOS)

or Ctrl-P (PC) to disable the spill correction. Then, press that keyboard shortcut again

to re-enable the spill suppression.


Now you can focus on matching the foreground and background. You can choose to

perform the foreground color correction in the Fusion page by adding additional Color

Corrector nodes, or, since you have the world’s best color grading tools on the color page,

you can perform the color correction there.
## **Sending a Matte to the Color Page**


As you have experienced, the Delta Keyer is an amazing tool for green-screen shots.

And although the Fusion page also includes extremely adept Color Correction nodes,

DaVinci Resolve offers world-renowned color grading tools on the color page. So in some

cases you may want to use the two pages together for compositing a shot. In this exercise,

you’ll use the matte from the Delta Keyer to color match the foreground and background

in the color page. It’s a simple process to show you how easy it is to bring mattes from

Fusion into the color page.

##### **Adding a Second MediaOut Node**


The main requirement in sending the matte from the Fusion page to the color page is

adding a MediaOut node.

**1** Click in an empty area in the Node Editor above the Delta Keyer node.


Clicking in an area of the Node Editor is a way of pinpointing where a node should be

placed when you add the next node.

**2** Press Shift-Spacebar, type **MediaOut**, and then press Return/Enter to add the node to

the Node Editor.

**3** Drag the output of the Delta Keyer to the input of the MediaOut2 node.


The first MediaOut node in the Node Editor always goes to the edit page. Additional

MediaOut nodes go to the color page. You can add as many MediaOuts as needed for

sending multiple mattes.


**Lesson 5 Compositing Green‑Screen Content** **134**


##### **Setting Up the Color Page**

Most of the time that you use nodes in the color page, you are processing color data.

Occasionally, you may add an external matte from the media pool. In our case, we need to

add a source from the Fusion page.

**1** Click the color page.


The green-screen clip you were working on in Fusion is now the currently selected clip

in the color page. You need to add a source that represents the MediaOut2 node (the

matte) from the Fusion page.

**2** In the Node Editor, right-click in an empty gray area and choose Add Source.


The source is added as a green icon on the left side of the Node Editor, directly under

the RGB source from the edit page. This second source is from the MediaOut2 in the

Fusion page. You can use it as either RGB data or an alpha channel since it includes

both. For this exercise, we’ll use the second source as an alpha matte source.

**3** Drag the output of the second source to the key input of node 1.


You now have a mask connected to node 1 so that any color correction you do will be

limited by the mask from the Fusion page.


**Lesson 5 Compositing Green‑Screen Content** **135**


**4** Using the color page Gamma color wheel, lower the master wheel, push the color

toward yellow/green, and lower the overall saturation to better match the guitarist

with his background.


TIP You can view the results of the color page corrections in the Fusion page

by selecting the MediaOut1 and clicking Color in the Inspector.


The main point of this green-screen lesson is not only to teach you the steps in setting up a

green-screen key, but perhaps more importantly to show you that keying a foreground

subject is almost never completed using only one tool. It’s far more common to employ

multiple techniques to address separate areas. In the end, if you learn to break down the

foreground into its own small problematic areas, you can address each area with different

tools to get the best possible results.


Completed node tree for Lesson 5.


**Lesson 5 Compositing Green‑Screen Content** **136**


## **Lesson Review**

**1** In the Fusion page, what is the primary tool for pulling a green-screen key?

**2** True or False? A solid matte connects to the Delta Keyer in order to fill any holes

that appear in the white matte of the foreground subject.

**3** True or False? Removing spill or bounce light coming from the screen onto the

foreground subject requires that you add a Color Corrector node.

**4** True or False? Adjusting Threshold in the Delta Keyer suppresses spill on the

foreground.

**5** True or False? A second MediaOut node is used to send a matte from the Fusion page

to the color page.


**Lesson 5 Compositing Green‑Screen Content** **137**


##### **Answers**

**1** The Delta Keyer is the primary tool for green-screen keying.

**2** True. A solid matte connects to the Delta Keyer to fill holes in the foreground subject.

**3** False. Removing spill or bounce light coming from the screen onto the foreground

subject can be done in the Delta Keyer or additionally in a Color Corrector node.

**4** False. Adjusting Threshold can clip only the black or white levels in a matte. It cannot

modify the RGB levels for spill suppression.

**5** True. Adding a second MediaOut node will send a matte and RGB image to the color

page. A second Source node must then be added on the color page to access

the matte.


**Lesson 5 Compositing Green‑Screen Content** **138**


### Lesson 6
# Addendum: Creating Title Animations



The next two lessons are not part

of the End User certification exam.

However, they do provide valuable

insight into the motion graphics

capabilities of Fusion.


DaVinci Resolve includes dozens of

useful title templates, both static and

animated, that you can customize to fit

your projects. Many of those templates

are created in Fusion using advanced

text and shape tools but are accessible

from the edit page’s Effects Library or

the cut page’s Title Library.


Although Fusion is primarily a visual

effects compositing tool, it includes

some very powerful and unique 2D

and 3D motion graphics tools as well.

Fusion’s Text+ tool provides a fantastic

amount of control over the look, layout,

and animation of your title designs.



Time

This lesson takes approximately
60 minutes to complete.

Goals

Styling Text in the Edit Page 140

Moving Text to the Fusion Page 145

Creating a Background Banner 147

Revealing Text with Mattes 151

Animating with the Follower 153

Adjusting Keyframe Timing  157

Trying Out Versions 161

Saving a Template 163

Lesson Review 167


In this lesson, you’ll create different versions of an animated lower third and then save it as

a template that you can reuse directly in the edit page or cut page.


Completed title for lesson 6.

## **Styling Text in the Edit Page**


To start, you’ll restore a new archive that will be used for the two lessons that make up the

addendum of this book.


NOTE The Timelines bin includes a Backups bin with timelines saved at various

stages of the lesson and a Completed bin with finished compositions. Both bins

are available for reference and for reverse engineering the node trees.


**1** Open DaVinci Resolve. In the Project Manager, right-click and choose Restore

Project Archive.


**Lesson 6 Addendum: Creating Title Animations** **140**


**2** Navigate to the R20 Fusion Training Media folder you downloaded at the start of this

book and restore the **DR20 Fusion Animation.dra** project. Open the project and,

from the Timelines bin, load the **Motion Graphics-START** timeline into the edit page.


**3** Open the Effects Library and, from the Titles category, drag the Text+ template into

the timeline directly above the first clip, which contains our interview.


**4** Select the Text+ clip and open the Inspector.


The Text+ template in the edit page is the same Text+ tool located in the Fusion page.

You can begin creating titles in the edit page and then move to the Fusion page when

you want to expand on the title animation.

**5** In the Inspector’s Styled Text field, replace Custom Title with **FULL NAME** as the text

we’ll use in our template.


**Lesson 6 Addendum: Creating Title Animations** **141**


**6** Set the font to Open Sans and set the font typeface to Extrabold.


**7** Change the text Size slightly larger to around **0.1** .

**8** To make the text left justified instead of the default center justified, scroll down the

Inspector and click the H Anchor Left button.


**9** At the top of the Inspector, click the Layout tab.


TIP Similar controls (such as rotation) appear multiple times in the various

tabs of the Text+ tool. As you’re learning, pay careful attention to which tab

section the steps are being performed in.


Beyond the familiar text formatting options on the Text tab, the Layout tab is used to

position the person’s name as a lower third title.


**Lesson 6 Addendum: Creating Title Animations** **142**


**10** In the Inspector, drag over the Center X and Y fields to move the text to the left lower

third of the frame.


TIP From the overlay menu in the lower left corner of the viewer, you can

select Fusion Overlay to display Fusion’s onscreen controls instead of

positioning the text in the Inspector.


**11** Click the Shading tab.


The Shading tab is for styling the appearance of the text. Instead of using a single solid

color, you can convert the fill type to a gradient.

**12** In the Type options, choose Gradient.


**Lesson 6 Addendum: Creating Title Animations** **143**


In the gradient bar, you can assign the various colors that fill the text. The first white

color stop sets the lower color of the gradient, the white color stop on the right sets

the upper color, and you can add color stops along the bar to create multi-point

gradients. The first color stop is selected by default, so you can set its color just

by selecting it in the color swatch.

**13** Open the color swatch and select a light teal color to set the lower gradient color.


**14** To set the upper gradient color, click the white color stop on the right end of the

gradient bar and, in the color swatch, choose a pale yellow.


TIP You can drag any color stop to reposition the spread of the

gradient colors.


To rotate the gradient angle so it spreads from left to right instead of top to bottom,

you can use the Mapping controls under the color swatch.

**15** Scroll down the Inspector and drag the Mapping Angle to the left until it reaches -90

so the gradient travels horizontally across each letter.


**Lesson 6 Addendum: Creating Title Animations** **144**


**16** From the Mapping Level menu, choose Line so the gradient is spread across the entire

line of text, rather than each letter.


You can add the Text+ title in both the edit and cut pages. Consider it the go-to title for

designing lower thirds and main titles because it has so many options. Here, it allowed you

to correctly size and roughly position the text against a background video track. The other

benefit of the Text+ title is that you can move it into Fusion and add some other elements

along with some animation.
## **Moving Text to the Fusion Page**


Moving text from the edit page into Fusion is the same as moving a video clip or the Fusion

Composition effect: just position the playhead and click the Fusion button.

**1** Position the playhead over the Text+ title clip and click the Fusion button to go to the

Fusion page.


As in Lesson 2, you’ll use a single-viewer layout.

**2** Click the Single Viewer button located in the upper right corner of viewer 2.


The title appears in the Fusion viewer precisely as you had it designed in the edit page.

The node is labeled Template so you know it is a title template from the edit page. Let’s

add a second line of text with the same attributes as our existing text.

**3** Select the Template node and choose Edit > Copy or press Command-C (macOS) or

Ctrl-C (PC).

**4** With the Template node still selected, choose Edit > Paste or press Command-V

(macOS) or Ctrl-V (PC).


A second Template node (Template_1) is created, and the two nodes are automatically

merged. The original Template is connected to the background input on the Merge,


**Lesson 6 Addendum: Creating Title Animations** **145**


and the new Template node is connected to the foreground input. Rearrange the

nodes so that Template_1 appears above Merge1.


We’ll use a second Text node as a placeholder for the job title text in our lower-third

template. This will also allow us to animate the person’s name and their job title

independently.


TIP The Multitext tool in the Effects Library can be used to create multiple

lines of text in the edit and cut pages and then can be brought into Fusion as a

single multitext node for additional effects.


**5** Select the new Template 1 node and, in the Inspector’s Styled Text field, enter **TITLE** .


TIP As a general rule, a change in font usually implies a change in meaning.

However, too many typefaces are distracting and can confuse your audience.

Restrain yourself to using only one or two fonts in a single project. Use

typefaces such as bold, light, or italics (as we have done here) to inject variety.


**6** Change the Font to Open Sans Regular.


The two text elements are seen in the viewer, but you still need to position the TITLE

text under the FULL NAME text.

**7** At the top of the Inspector, click the Layout tab and drag the Center Y field to lower the

text below the FULL NAME text.


**Lesson 6 Addendum: Creating Title Animations** **146**


**8** At the top of the Inspector, click the Shading tab and click Solid for the fill type. Then

select a dark gray color.


**9** To make sure you stay organized, rename each node based on the text you’ve entered:

Template becomes **NAME**, and the new copied Template_1 becomes **TITLE** .


This is the general layout of the lower-third title. The next steps will be to create some

visual interest by animating the text.
## **Creating a Background Banner**


The creation of graphical elements like background banners uses a slightly different

approach than most motion graphics applications. You use a color generator as fill and a

matte to cut the shape you want. We’ll create a pill shaped background banner for our text.

This makes the title stand out more when placed over video.

**1** From the toolbar, drag a Background node into an empty area of the Node Editor.


The Background node is a color generator. It will create the background color of the

banner background.


**Lesson 6 Addendum: Creating Title Animations** **147**


**2** Press 2 to see the default black color in the viewer.


The Background node allows for both solid color and gradient backgrounds. For this

banner, you will create a radial gradient.

**3** In the Inspector, select Gradient from the Type menu, and then choose Radial from the

Gradient Type menu.


The radial gradient has center color and an outer color represented on the gradient

bar. It also has a thin green line in the viewer.

**4** Open the color swatch and select a vibrant fuchsia color located in the center of the

color swatch.


**Lesson 6 Addendum: Creating Title Animations** **148**


**5** Select the far-right color stop on the gradient bar and assign a creamy yellow color

from the color swatch.


Next, you can add a mask to form the shape of the banner.

**6** With the Background node selected, click the Rectangle mask tool in the toolbar.


Clicking any matte tool connects the matte into the blue effect mask input of the

selected node. The Rectangle mask trims the background into a smaller rectangle

centered in the frame.

**7** In the Inspector, set the width to **0.9** and the height to **0.3** .


**Lesson 6 Addendum: Creating Title Animations** **149**


**8** Drag the corner radius slider to 1.0 to create a rounded pill shape.

**9** Rename the background node **BANNER** .


To position this correctly behind our text, you need to merge the banner using the text

as the foreground.

**10** Drag the output of Merge1 to the output of the BANNER node.


**11** Select the newly created Merge2 and press 2 to see it in the viewer.


Now that you can finally see all the elements in the viewer, you’ll need to position the

banner under the text. You can do this by positioning the Rectangle mask.

**12** Select the Rectangle1 node and use the onscreen controls in the viewer to position it

directly behind the text.


**13** To make sure the new Merge2 is connected to the MediaOut, drag the output of

Merge2 to the input on the MediaOut and replace the existing connection.


With the banner in place, we can now start our animation.


**Lesson 6 Addendum: Creating Title Animations** **150**


## **Revealing Text with Mattes**

Static text implies “move along, nothing to see here,” and the audience tunes out. Even

minimal text motion adds interest to flat type to help keep an audience focused long

enough to read the message. You can animate text in many different ways in Fusion, but

you’ll explore two of the most popular methods in this lesson. The first technique you will

use is revealing the text with the use of a matte.

**1** In the Node Editor, select the TITLE node and, from the toolbar, click the

Rectangle tool.


The rectangle is added to the center of the frame, acting as a window of sorts. Since

the text is positioned outside the rectangle, it is hidden from our view. We’ll use this

rectangular window as a way to reveal our text through keyframing.


To start, the rectangle should be positioned lower to reveal the TITLE text, and it

needs to be large enough to cover any potential title someone may enter into

the template.

**2** In the Node Editor, select the Rectangle2 node and drag its red transform controls in

the viewer until the top line of the rectangle is aligned with the bottom of the FULL

NAME text.


You can now animate the Title text so that it begins outside the rectangle and then

slides into place.


**Lesson 6 Addendum: Creating Title Animations** **151**


**3** Move to the start of the render range in the timeline.

**4** Select the TITLE node and, in the Inspector, click the Layout tab.

**5** To the right of the Center X and Y fields, click the Keyframe button.


**6** Drag the Center Y parameter to the right until the TITLE text disappears above the

rectangle mask.


**7** Move the playhead to frame 15.


Here is where the TITLE text will reappear onscreen.

**8** Drag the Center Y parameter to the left until the TITLE text appears back in position

below the FULL NAME text.

**9** Move to the start of the render range.

**10** Click the Play button to view the animation.


The TITLE text slides in, revealed only within the rectangular matte. Using a combination of

position keyframes and mattes, you can create very complex animations with a

straightforward setup.


**Lesson 6 Addendum: Creating Title Animations** **152**


## **Animating with the Follower**

You can animate words using keyframes as you did to move the text in and out of the

mattes, but you also have access to a special modifier designed specifically for animating

text character by character. The _follower_ is a sequential animation modifier that applies

keyframe animation to your text with a custom delay between each character. For our

animation, we will have each letter in the FULL NAME text rotate into view.

**1** Select the NAME node, and then select the Text tab in the Inspector.


To apply the Follower modifier, you use the Styled Text box in the Inspector.

**2** Right-click the Styled Text box and choose Follower.


The Follower is a modifier and, as with other modifiers, its controls appear in the

Modifiers tab. What actually _is_ a modifier? Modifiers are special add-on tools that help

you change an element or parameter without a lot of effort. They are applied by

right-clicking the parameter you want to modify and choosing the appropriate

modifier. The Follower modifier allows you to easily sequentially animate titles letter

by letter.

**3** At the top of the Inspector, click the Modifiers tab.


To animate the follower, you keyframe the text how you want. You can keyframe

position, rotation, size, or even color. Then, once you have designed the animation,

you can decide how much delay to place between characters so that the animation

ripples through your entire text string.


TIP Many of the sections in the Follower Modifiers tab match those in the

Tools tab. For the following steps, make sure you are making changes to the

section in the correct tab—in this case, the Modifiers tab.


**Lesson 6 Addendum: Creating Title Animations** **153**


**4** In the Follower section of the Inspector, click the Transform tab.


We want the text to slide in from the bottom of the screen.

**5** Move the playhead to the start of the render range.

**6** Click the Keyframe button next to the Y Offset control.


Fusion adds another modifier for the motion path you are creating and switches to

show you the path controls.


TIP When using the Follower, you must enable keyframing on a parameter

before any changes will be visible in the viewer.


**7** At the top if the Inspector, double-click the Follower1 label to reopen the

follower controls.


**Lesson 6 Addendum: Creating Title Animations** **154**


**8** Drag the Y Offset value left to around -0.2.


The viewer now shows the text offscreen at the bottom. We’ll make this a slide-in that

lasts only 15 frames.

**9** Move the playhead to frame 15 and drag the Y Offset slider back to its default of 0.

**10** Play the animation to see the results so far.


You’ve created a 15-frame animation in which the text slides in from the bottom

of the screen. Now, using the Timing tab, you can delay the slide-in for each letter in

the sentence.

**11** Click the Timing tab and drag the Delay slider to 2.


Because you set the delay to two frames, the first letter begins to slide in, and two

frames later, the second letter begins to follow. Each subsequent letter animates two

frames after the one before it.


TIP The effects of the Follower modifier can be quite confusing when you’re

first getting used to it. It’s usually a good idea to set keyframes first (as we’ve

done here), and then apply a delay. If you want to set further keyframes, it’s

often helpful to first remove the delay, set the additional keyframes, and then

apply the delay again. In doing so, you’ll keep your sanity intact.


**Lesson 6 Addendum: Creating Title Animations** **155**


**12** Play the animation to review it and then stop playback.


The animation ripples through the text starting from the character on the left.

However, at the start of the animation, you can still see the text onscreen. You can add

additional parameter animations to the Follower—for instance, to fade each character

in as it slides.

**13** Move the playhead to the start of the render range.

**14** Click the Shading tab and then click the Keyframe button to the right of the

Opacity slider.


**15** Drag the Opacity slider to 0.


The viewer now shows the text completely faded.

**16** Move the playhead to frame 15 and drag the Opacity slider back to 1.0.

**17** Play the animation to see the added fade.


As the Name text slides in, it overlaps the title text. We can use the same Rectangle

mask trick we see on the title text to limit the visibility of the Name text to within the

boundary of the rounded rectangle.

**18** Drag the output of the new Rectangle2_1 node into the blue mask input of the

Name node.


Now the masked Background node is used as the mask for the Name text.


**19** Play the animation to see the added mask.


Almost all the controls in the Text tools tab of the Inspector can be animated using the

Follower, including position, size, shearing, and color. By playing around for only a few

minutes, you can see why this modifier is a fantastic tool for motion graphics.


**Lesson 6 Addendum: Creating Title Animations** **156**


## **Adjusting Keyframe Timing**

The Fusion page has incredible Keyframe and Spline Editor tools for refining animation.

The Keyframes Editor is an easy way to modify the timing of animations. The Keyframes

Editor can be used when you are not as concerned about the interpolation between

keyframes, but about the timing between them.

**1** In the upper right of the Fusion window, click the Keyframes button.


To open more room for the Keyframes Editor, you can temporarily hide the

Node Editor.

**2** In the upper left of the Fusion window, click Nodes to hide the Node Editor.

**3** In the upper right corner of the Keyframes Editor, click the Zoom to Fit button to fill the

panel with the keyframe tracks.


TIP Dragging in the timeline ruler at the top of the Keyframes Editor will

expand the tracks horizontally so you can zoom in to a specific area.


The Keyframes Editor shows tracks much like a multilayered timeline on the edit page.

However, the track stacking order in the Keyframes Editor has no bearing on the

arrangement of images in the viewer. The tracks only adjust the timing of elements

and keyframes.


The nodes in the Node Editor are listed to the left in the header, and you can choose to

view all nodes or only nodes with keyframes applied.


**Lesson 6 Addendum: Creating Title Animations** **157**


**4** From the Sort menu in the upper right corner of the Keyframes Editor, choose

Animated from the bottom of the menu to show only tracks with keyframes applied.


Thin vertical lines represent the keyframes on each node, but you can expand each

track to show individual tracks for each parameter with keyframes.

**5** In the header area to the left of the Keyframes Editor, click the disclosure arrows next

to the NAME track to display the individual keyframe tracks for the Follower.


TIP Selecting a tool’s name in the header also displays its controls in the

Inspector and selects its node in the Node Editor.


Let’s have the FULL NAME animation last five frames longer. To do this, you’ll move the

last two keyframes on the two tracks a few frames later in the timeline.

**6** Drag the red playhead to frame 20.

**7** In the NAME track, drag a selection rectangle around the two ending keyframes on

each track.


**Lesson 6 Addendum: Creating Title Animations** **158**


TIP When a keyframe is selected in the Keyframes Editor’s timeline, you can

press Command-Delete (macOS) or Ctrl-Backspace (PC) to delete

the keyframe.


These keyframes represent the last keyframes for the Follower’s Character Offset and

Styled Text Opacity animation. Dragging a selection rectangle around the keyframes

selects them, as indicated by the yellow selection color.

**8** With the keyframes selected, drag them to line up with the red playhead.


As you drag, a tooltip in the lower left corner of the window displays the current

frame number.


TIP You can click in a gray area of the timeline to move the playhead by

holding down Command-Option (macOS) or Ctrl-Alt (PC) and clicking where

you want the playhead to move.


Now, you can improve the timing of the TITLE text.

**9** In the header area, click the disclosure arrows next to the TITLE track.


TIP When selecting MediaIn nodes, you can use the Keyframes Editor’s

timeline tracks to trim and slide the start and end points, much as you would

trim them in the edit page timeline.


Instead of just dragging keyframes, you can enter an exact frame number or an offset

value to move them. Let’s move the TITLE text so it begins 10 frames later.

**10** Select the two keyframes on the TITLE track Layout Center : Path : Displacement track.


**Lesson 6 Addendum: Creating Title Animations** **159**


**11** With the keyframe selected, in the lower right of the Keyframes Editor, from the Time

dropdown menu, choose T Offset.


Entering a value in the T Offset field will move the selected keyframes forward or

backward by the number of frames entered.

**12** In the T Offset field, type **10.0** and then press Enter to move these two keyframes

10 frames forward.


**13** Click the Play button to view the results.

##### **Changing Interpolation in the Keyframes Editor**


Although the Keyframes Editor doesn’t have the flexibility of a Spline Editor, you can still

make some interpolation changes to smooth animations.

**1** In the Keyframes Editor, right-click over the last TITLE keyframe on frame 25.


**Lesson 6 Addendum: Creating Title Animations** **160**


**2** From the contextual menu, choose Smooth.


This applies a smooth interpolation to the last keyframe to give it a softer landing.

Although you cannot change it as you can in the Spline Editor, sometimes the default

setting is all you need.

**3** Click the Play button to view the results.

**4** When you’re done reviewing, close the Keyframes Editor and open the Node Editor.
## **Trying Out Versions**


When designing the look of your title, you’ll often go through a few iterations of font, color,

and layout. Fusion can help with these iterations by using versions. Each node can have up

to six saved states, called _versions_ . Each version saves a snapshot of the Inspector that you

can return to at any time during your project. It’s a great way to try out different node

settings without losing your previous work.

**1** Move to the middle of the render range where all the elements are onscreen.

**2** Select the Banner node.


**3** In the Inspector header, click the Versions button.


The versions are numbered starting with the default selection, Version 1. Clicking

another number selects that version. Any changes you make from that point on will

be saved for the selected version.

**4** Click the Version 2 button.

**5** Change the gradient color stop on the right side to white.


You now have two different versions. You can switch back to version 1 at any time by

clicking the Version 1 button.

**6** Select the Version 1 button at the top of the Inspector to see the initial

outline gradient.


**Lesson 6 Addendum: Creating Title Animations** **161**


**7** Click back on the Version 2 button to return to the updated look.


TIP Versions are saved only for the current node in the project. Adding a

second node of the same type will not include the saved versions. However,

you can save the current configuration as the default setup for a node by

right-clicking it and choosing Settings > Save Default.


Any node can take advantage of versions as you work out your design or composite.

It makes for quick design changes if you or your client decide that you/they like an

earlier look you created. It’s just one click away.

##### **Timeline Versions**


If you intend to make a more fundamental change to the composition—such as changing

the entire layout or adding nodes to the comp—you may want to make a _timeline version_ .

Timeline versions are entire compositions that are saved for each clip that enable you to

make minor or major changes in a composition while retaining access to previous versions.

**1** In the upper left of the user interface toolbar, click the Clips button.


The Clips button displays a thumbnail timeline at the bottom of the Node Editor that

shows every edit in the currently loaded timeline.

**2** Right-click the currently selected thumbnail, which is the currently selected clip, and

choose Create New Composition.


The previous animation is now saved as Composition 1, and Composition 2 is currently

loaded. You can change the look of each element in this comp, and it will be saved as

Composition 2.


**Lesson 6 Addendum: Creating Title Animations** **162**


**3** Select the Merge2 node and, in the Effects Library, choose the Tools: Blur category,

and then click the Soft Glow tool.


The Soft Glow node adds a nice halo effect.

**4** Press 1 to see the Soft Glow effect in the viewer. Move the playhead to frame 50 to see

the completed title build.

**5** In the Inspector, drag the Gain slider down to 1.0.


You can switch between timeline versions at any time.

**6** In the Clips timeline, right-click the selected thumbnail and choose

Composition 1 > Load.

**7** Load the composition you prefer to use for the template.


Now you have two clip versions saved: one with the Soft Glow and one without. The

current version you have loaded is the one without the Soft Glow, which we’ll use to make a

template that we can reuse in the edit page.
## **Saving a Template**


After going through the effort of creating this lower-third design, you may want to reuse it

with small tweaks to fit different interview subjects. Rather than opening this entire comp

over and over, you can save it as a single template in the edit page Effects Library. The first

part of creating this template is to use Fusion’s macro creation feature to collapse all the

nodes into one single node that displays only the parameters you want to be able to tweak.

**1** Click in an empty area of the Node Editor and then select the NAME node.

**2** Hold the Command key (macOS) or the Ctrl key (PC) and select the TITLE node.

**3** Now, press Command-A (macOS) or Ctrl-A (PC) to select all the remaining nodes.


**Lesson 6 Addendum: Creating Title Animations** **163**


The order you select the nodes is the order they appear in the macro list, making it

easier to place the most important nodes at the top of the list.

**4** Right-click over any of the selected nodes and choose Macro > Create Macro.


The Macro Editor window shows every node and every parameter in the node

tree. There is a field at the top to name the macro.

**5** In the Macro Name field at the top of the window, name the macro **2D TRAINING**

**LOWER THIRD** .


The list of nodes and parameters can be a bit daunting at first, but you are really only

interested in the top two text nodes. We’ll only want the template to provide controls

for changing the text and size.

**6** In the macro list, click the disclosure arrow next to Image to hide those parameters.


**Lesson 6 Addendum: Creating Title Animations** **164**


**7** Click the checkbox to the right of the StyledText field, and then replace the Styled Text

with the SUBJECT NAME.


By clicking the checkbox next to StyledText, you have selected it to be displayed in the

edit page Inspector. The label that will show next to this text field will be Subject Name.

**8** In the macro list, click the disclosure arrow next to NAME to hide all those parameters.

**9** Click the disclosure arrow next to TITLE, close the Image section, and then enable the

checkbox for StyledText.


So that this styled text is not confused with the previous settings related to the TITLE

text, let’s rename this parameter.

**10** Change the StyledText name to **JOB TITLE** .

**11** Click the Close button and click Yes in the warning dialog to save the template.


A Save window appears, allowing you to choose where on your hard drive the macro

will be saved. The default location saves it for access through the Fusion page only.

To get it to show up in the edit page, you ‘ll need to change the location.

**12** In the Save window, select:


 - **On macOS:** Library > Application Support > Blackmagic Design > DaVinci Resolve >

Fusion >Templates folder and then select the Edit > Titles folder.

 - **On Windows:** AppData > Roaming > Blackmagic Design > DaVinci Resolve >

Fusion > Templates folder and then select the Edit > Titles folder.


TIP If any of the folders don’t yet exist, you may need to create them.


This location saves the template so it will show up in the edit page Effects Library.

**13** Click Save in the window, and then quit and relaunch DaVinci Resolve.


**Lesson 6 Addendum: Creating Title Animations** **165**


**14** Open the **DR20 Fusion Animation** project and switch to the edit page.

**15** In the Effects Library, select the Titles category and scroll down to locate the 2D

TRAINING LOWER THIRD template.

**16** Drag the template to the timeline and place it over the existing title.

**17** Select it to view the controls in the Inspector.


Completed node tree for lesson 6.


You’ve completed this lesson on type and title animation by animating in multiple ways,

modifying those animations, and designing a look. You started with the Text+ tool in the

edit page and then brought it into the Fusion page to build a more complex animation

using keyframes and the Follower, using both node versions and timeline versions to save

different looks and animations of your composition. Finally, you saved the title animation

as a template that can be accessed in the edit page.


**Lesson 6 Addendum: Creating Title Animations** **166**


## **Lesson Review**

**1** True or False? Timeline versions save only the appearance of text.

**2** True or False? You apply the Follower to text by right-clicking in the Styled Text box

where you type the text.

**3** True or False? Only one word can be entered into a Text+ node.

**4** True or False? Adding a keyframe to a parameter in the Inspector will cause that

keyframe to appear in both the Keyframes Editor and the Spline Editor.

**5** True or False? Clicking a version button in the Inspector for a selected node will also

save the settings for any node connected to the selected node.


**Lesson 6 Addendum: Creating Title Animations** **167**


##### **Answers**

**1** False. Timeline versions save the entire composition in its current state.

**2** True. You apply the Follower to text by right-clicking in the Styled Text box where you

type the text.

**3** False. A single Text+ node can include multiple lines of text.

**4** True. The Keyframes Editor and the Spline Editor show all keyframes on all parameters.

**5** False. Clicking a version button in the Inspector saves only the settings for the

selected node.


**Lesson 6 Addendum: Creating Title Animations** **168**


### Lesson 7
# Addendum: Animating with Keyframes and Modifiers



In this lesson, you’ll move beyond

title animations into full-motion

graphic design. A motion graphics

designer creates every animated

logo, infographic, and design element

in a commercial, TV show, or web

video. When you take on the role of

motion designer, you aim to convey

a message by animating graphics.

Although that often includes text,

as we have explored in the previous

lesson, now you’ll work on more

general animation techniques.



Time

This lesson takes approximately
45 minutes to complete.

Goals

Identifying a Clip’s Resolution 170

Keyframing a Motion Path 171

Auto-Orienting Objects 176

Straightening Out
Alpha Channels  177

Painting a Motion Path 178

Linking Parameters 182

Making Acceleration
Adjustments 185

Applying Random
Animation Modifiers  187

Customizing Motion Blur 189

Lesson Review 191


The motion design you’ll create in this lesson borrows a lot from major Hollywood movies.

You will create a vintage travel map look, complete with a plane and animated travel line.

You’ll use different animation techniques—including a mixture of keyframes, simple

expressions, and modifiers—as you sharpen your animation skills.


Completed composite for Lesson 7.

## **Identifying a Clip’s Resolution**


To start this Fusion composition, you’ll use the same project and timeline you used in the

previous Title animation lesson. This project and timeline contain a vintage map, which you

can use as the background for your plane and painted flight path line.


NOTE The Timelines bin includes a Backups bin with timelines saved at various

stages of the lesson and a Completed Projects bin with finished compositions.

Both bins are available for reference and for reverse-engineering the node trees.


**1** From the edit page in the **DR20 Fusion Animation** project, load the

**Motion Graphics-START** timeline and move the playhead to the vintage map clip.


This map is a simple 4K image in an HD timeline. You’ll use it as the background behind

your animated plane. Because a project’s resolution in the edit page uses the master

timeline settings, clips brought into a project are usually scaled automatically to fit

the timeline’s resolution.


**Lesson 7 Addendum: Animating with Keyframes and Modifiers** **170**


**2** Click the Fusion page tab or press Shift-5.

**3** If you are using dual viewers, click the Single Viewer Mode button in the upper right

corner of viewer 2 to return to single viewer mode.

**4** Hold the Command key (macOS) or the Ctrl key (PC), position the mouse pointer over

viewer 1, and scroll the middle mouse wheel until you see the resolution in the upper

right corner of the frame.


The resolution displayed in the upper right corner of the Fusion viewer shows a UHD

resolution (3840 x 2160). Although your timeline resolution in the edit page is 1920 x 1080,

the Fusion page sets its composition size based on the original clip’s size. Therefore, you

are always compositing with the highest resolution, direct from the source. On returning

to the edit page, the MediaOut node scales down the final result to fit the edit page

timeline’s resolution.
## **Keyframing a Motion Path**


With your project set, you’ll keyframe a plane across the map to create a motion path that

you can then reuse for other elements in the project. To keyframe the plane’s position,

you’ll first import the graphic and then apply a Transform node. The plane graphic you

can use in this composition is already in the media pool.

**1** In the upper left corner of the DaVinci Resolve window, click the Media Pool button

to open the media pool.

**2** From the Clips bin, drag the biplane with the alpha.tif file into an empty area of the

Node Editor.


**Lesson 7 Addendum: Animating with Keyframes and Modifiers** **171**


**3** With the MediaIn2 node selected, press 2 to display it in viewer 2, then press F2, and

rename the node **BIPLANE** .

**4** Select the MediaIn1 node and rename the node **MAP** .


For this lesson, you’ll use viewer 2 in a single-viewer layout to give yourself a good

amount of design space.

**5** Drag the output of the BIPLANE node to the output of the MAP node to create a Merge

node with the biplane as the foreground.


**6** Select the Merge node and press 2 to see the composite in the viewer.


The biplane is displayed over the background map, but it is clearly too large to fit

within the vintage map background.


**Lesson 7 Addendum: Animating with Keyframes and Modifiers** **172**


**7** Select the BIPLANE node and, in the toolbar, click the Transform tool.


TIP While the Merge node contains transform controls—and we could use

those to animate the plane and adjust its size—it’s usually considered better

form to explicitly add a Transform node. This makes the node graph more

readable: coming back to the project several days later, you can immediately

identify that the Transform is doing the moving of the plane. It would be far

less easy to intuit that it’s the merge performing the movement just by looking

at the nodes in the graph.


**8** In the Inspector, adjust the plane’s size to 0.20.


The plane is now more proportional to your map. We can begin keyframing it across

the map to simulate a flight path.

**9** Drag the playhead to position it at the start of the render range.

**10** Hold the Command key (macOS) or the Ctrl key (PC), position the mouse pointer over

viewer 2, and scroll the middle mouse wheel until you have a bit of room around the

frame. You’ll use this space to position the plane out of the frame.


**Lesson 7 Addendum: Animating with Keyframes and Modifiers** **173**


**11** Using the plane’s center control in the viewer, drag the plane offscreen left, just off the

coast of Mexico.


**12** As you would in the edit page, click the Keyframe button for the Center X and Y

controls in the Inspector.


You have now set a keyframe for the first frame of this composition. As you move the

playhead and drag the plane to a new location on the map, a keyframe will be added

automatically, and you will begin to create a motion path.

**13** Move the playhead to frame 25, and then drag the plane in the viewer to the

northernmost part of Canada to add a second keyframe.


As you drag the plane, a line representing the motion path is drawn in the viewer.

**14** Move the playhead to frame 50 and drag the plane to the southern tip of Africa.

**15** On frame 75, move the plane over China.


**Lesson 7 Addendum: Animating with Keyframes and Modifiers** **174**


**16** Finally, move to frame 100 and drag the plane offscreen, somewhere near

New Zealand.


TIP Each control point along the path represents a keyframe. Command-click

(macOS) or Alt-click (Windows) on the path in the viewer to add a control point

that does not correspond to a keyframe. This allows you to change the spatial

shape of the path without having to manage temporal adjustments.


With the basic flight path of the plane created, you’ll quickly smooth the path so it is

less linear.

**17** In the viewer toolbar, click the Select All Points button.


**18** Click one of the points (all points should remain selected), and then press Shift-S or

click the Smooth button in the viewer toolbar to smooth the plane’s path.


The path for the plane now has smooth curves as it travels across the map.

**19** Press the Play button to review the animation.


Like the Follower that you used in previous lessons, the spline shape created by keyframing

includes a modifier that converts the spline into a path.


You can use that path modifier to drive the animation of other elements.


**Lesson 7 Addendum: Animating with Keyframes and Modifiers** **175**


## **Auto-Orienting Objects**

This animation would be better if the nose of the plane followed the direction of the plane’s

path. Instead of keyframing the angle of rotation for the plane, you can connect the angle

to the path modifier and have Fusion dynamically animate the orientation of the plane.


Then, as the plane moves along the path, the plane’s angle also changes accordingly,

making it “turn” at each bend of the path. In the future, if you adjust the path in the viewer,

the plane’s angle also adjusts according to the path curvature.

**1** Select the Transform node in the Node Editor.

**2** In the Inspector, right-click the angle parameter and choose Connect To >

Path > Heading.


The Connect To menu is used to link a parameter to an existing modifier. In this case,

the modifier is the path you created by keyframing the plane. Connecting the angle

parameter to the path modifier auto-orients the parameter.

**3** Return to the start of the render range and play the animation.


The path modifier changes the angle of the plane dynamically, based on its movement

along the path.


**Lesson 7 Addendum: Animating with Keyframes and Modifiers** **176**


## **Straightening Out Alpha Channels**

To better integrate the plane with the map, let’s give the plane a more weathered,

vintage look.

**1** Select the Transform node and, in the toolbar, click the Color Correction tool.

**2** In the Inspector, use the color wheel to tint the plane to better match the background

and increase the lift to about 0.25 to give the plane a faded, sepia-tone appearance.


As you adjust the lift on the plane, the background map also brightens. You’ve been in

this situation before. It’s the problem that occurs when you perform color correction

on an image with a premultiplied alpha channel. Just as we did with the DriveDoc in

Lesson 1 and the Pizza graphic in Lesson 4, you can enable the Pre-Divide/Post
Multiply checkbox in the Color Corrector to fix the issue.


TIP If you increase the gamma instead of the lift, you’re more likely to see a

white halo around the image instead of a brightened background. However,

the root cause of this behavior and its solution are the same.


**Lesson 7 Addendum: Animating with Keyframes and Modifiers** **177**


**3** In the Inspector, click the Options tab and then select the Pre-Divide/Post
Multiply checkbox.


TIP Alternatively, you could deselect the checkbox and insert an Alpha Divide

node before the color correction and an Alpha Multiply after the color

correction.


With the airplane looking good, you can enhance this project by having a classic, red
dotted line animate along with the plane, highlighting its flight path.
## **Painting a Motion Path**


In Fusion, you can use paint strokes for visual effects and animated motion graphics.


No matter what the task, painting always starts with a Paint tool. Unlike using multiple

brush and shape tools to achieve the painting style you want, Fusion includes a single

versatile Paint tool that incorporates many brush types and paint styles. To paint the path

across our map, you’ll add a Paint node directly after the MAP node.

**1** Select the MAP node and, in the toolbar, click the Paint tool.


The Paint tool is added directly after the MAP node. At the top of the viewer is a toolbar

for the selected Paint node. The toolbar offers several strokes and paint styles suitable

for motion graphics or retouching shots. The paint stroke style that is comparable to

drawing a spline path is the Polyline Stroke brush.

**2** In the viewer toolbar, click the Polyline Stroke.


Unlike other paint stroke styles with which you could _paint_ out the path using one

continuous brushstroke, the Polyline Stroke functions similarly to a Bézier-style

drawing tool: you click to add control points that create a _painted_ stroke.


**Lesson 7 Addendum: Animating with Keyframes and Modifiers** **178**


For your plane path, you’ll only need to add two points to create a line of any length,

anywhere on the screen. Once you have a polyline stroke, you can modify it to use the

plane’s path to define the stroke shape.

**3** Click over Brazil and then click again over Australia.


Where you click doesn’t really matter; as you’ll see, we’re about to replace this initial

stroke entirely.


You now have a polyline paint stroke that you can modify with the path modifier.

However, the path modifier currently exists only on the Transform node where you

created the keyframes. You’ll need to make it available to all other tools.

**4** Select the Transform tool and click the Modifiers tab.


**Lesson 7 Addendum: Animating with Keyframes and Modifiers** **179**


The Modifiers tab shows the Path 1 that you created when you keyframed the plane.


Modifiers are just optional extensions to a tool’s main feature set. For instance, you

used the Transform tool to create a spline through position keyframes. Creating a

spline using position keyframes automatically creates a path modifier. That modifier

can then be published and made available to any object that can make use of a path.

Therefore, the first step is to publish the path so the paint stroke can use it.

**5** At the bottom of the Modifiers tab, right-click over the label “Right-click here for shape

animation” and choose Publish.


At the top of the Inspector, the Modifiers tab shows the path: polyline, which is now

published and available for other tools.

**6** Select the Paint node and then select the Modifiers tab if it isn’t already selected.

**7** At the bottom of the Inspector, expand the stroke controls section. From here, you can

connect to the published path polyline.

**8** At the bottom of the stroke controls, right-click over the label “Right-click here for

shape animation” and choose Connect To > Path 1: Polyline > Value.


The simple polyline paint stroke you created now takes the shape of the motion path.

Once you have a paint stroke, any changes are made in the Modifiers tab.


**Lesson 7 Addendum: Animating with Keyframes and Modifiers** **180**


**9** At the top of the Modifiers tab in the Inspector, expand the brush controls (you might

need to double-click the PolylineStroke1 section to expand it first). Change the Size to

about 0.01 and drag the Softness slider all the way to the left.


**10** In the apply controls, change the color to a vibrant red.

**11** In the stroke controls, drag the spacing slider all the way to the right to create a

dotted line.


Sliders in the Fusion page can only go so far, but that does not mean the parameter’s

value is restricted. You can enter values larger than the limit of the slider. Doing so will

scale the slider’s range to allow for the new larger value.


**Lesson 7 Addendum: Animating with Keyframes and Modifiers** **181**


**12** In the spacing numeric field, enter **1.5** and press Enter.


The dotted line in the viewer now has more spacing between dots, but more importantly,

the slider range has grown so that you can drag to 1.5 and even a bit beyond. Almost every

slider in the Fusion page includes this extended-range capability.
## **Linking Parameters**


To add more visual interest, you’ll animate the dotted line so that it follows the plane. The

hard way to do this is just to keyframe the line, but if you change the plane’s speed, you’ll

then need to go back and adjust the paint stroke’s animation as well. Fusion allows you to

link the animation of one parameter to any other parameter, even if the parameters are

completely different.

**1** In the Modifiers tab, drag the Write On End slider back and forth to see the results in

the viewer.


The Write On control has Start and End values that you can change by dragging the

sliders. Dragging the End slider changes the end of the paint stroke, creating a


**Lesson 7 Addendum: Animating with Keyframes and Modifiers** **182**


paint-on effect. You can animate this control by connecting it to the path’s

displacement property so that it writes on at the same rate as the plane’s position

along the path.

**2** Right-click the Write On’s End handle and choose Connect To > Path1 > Displacement.

**3** Drag the playhead through the render range to watch the path write on, following

the plane.


The Connect To menu provides a very easy way to connect two parameters, but it

doesn’t allow much flexibility. For instance, what if we wanted the paint stroke to lead

the plane by just a few frames instead of following the exact same position as the

plane? The Connect To menu has no way to do that, but you can link parameters in

other ways. These alternatives may require a bit more work but give you much greater

flexibility. First, you’ll remove the connected displacement from the End handle of

the write on.

**4** Right-click the Write On’s End handle and choose Remove Path1 Displacement.


Now, the displacement parameter you want to link to is located on the Modifiers tab of

the Transform node, since this is where the path was generated.

**5** In the Node Editor, select the Transform node and click the Modifiers tab. If Path1 isn’t

already expanded, double-click it to expand it.


The Transform’s path modifier includes the displacement and heading parameters that

you connected to earlier.

**6** Drag the playhead back and forth to see how the displacement parameter animates

based on the time in the composition.


As you drag through the render range, the displacement parameter is animated to

move the plane along the path. This is the control to which you want the End slider of

the paint Write On to link.

**7** With the Transform node selected, from the upper right corner of the Path1

Inspector’s section, click the Pin button to prevent Path1 from closing when you select

another node.


By pinning the Path1 Inspector, you can select another node and see the two nodes’

controls at the same time. This setup makes it possible to link the two parameters from

different nodes.


**Lesson 7 Addendum: Animating with Keyframes and Modifiers** **183**


**8** In the Node Editor, select the Paint node and then select the Modifiers tab in

the Inspector.

**9** In the Write On End field (under Stroke Controls) type **=** (equals sign) and press

Return or Enter.


Typing an equals sign in any numeric field opens a simple expression field. This

expression field gives you the option of linking two parameters by typing the name of

the parameter you want to link or by linking the two parameters using a pick whip.


TIP A _pick whip_ is a graphic line that you draw between two parameters as a

shortcut method of creating an expression.


**10** In the Inspector, drag from the plus icon on the left of the expression field up to the

Displacement label in the Path1 controls.


**11** Play the composition to see the linked animated paint stroke.


These animated elements look good so far, but as we said, this method offers some

flexibility over the Connect To menu. You can customize the speed or position of the

dotted path by modifying the expression that you added with the pick whip.

**12** In the expression field, insert **+.1** at the end of the expression. By adding +.1 to the

expression, you are offsetting the displacement by 10%, moving it ahead of the

plane’s displacement.


**Lesson 7 Addendum: Animating with Keyframes and Modifiers** **184**


**13** Play the composition to see the offset paint stroke.


Since you won’t be linking any more parameters right now, you can unpin the Path1

from the Inspector.

**14** In the Node Editor, select the Transform node.

**15** In the upper right corner of the Inspector, click the Pin button to release the Path1

controls in the Inspector. The Path1 controls will close when you select another node.


This simple pick whip example animates one parameter based on the value of another.


If you modify the speed or acceleration of the plane, the paint stroke inherits the

same adjustment.
## **Making Acceleration Adjustments**


Unless you’re trying to create a very robotic animation, you’ll seldom use linear motion as

we have here. Controlling how quickly and smoothly elements move from one state to

another is a crucial step in motion graphics. By default, the Fusion page applies a linear

interpolation between keyframes, so animations move at a constant rate. However, we can

return to the Spline Editor and have the plane slowly accelerate as the path dips into

southern Africa and then slow it down again when it reaches the top of the path on

the right.


As we make the change, the linked paint stroke follows along, inheriting the same

acceleration changes.

**1** In the upper right of the Fusion window, click the Spline button to open the Spline

Editor. The Spline Editor header on the left side of the panel shows all the animated

parameters.

**2** Select the checkbox next to the Transform Center (Path1) Displacement parameter.


**Lesson 7 Addendum: Animating with Keyframes and Modifiers** **185**


**3** In the upper right corner of the Spline Editor, click the Zoom to Fit button to fill the

graph area with the selected displacement spline.


Changing the acceleration of the plane along the path consists of smoothing the spline

between keyframes and then adjusting the spline handles to increase or decrease the

rate of acceleration.

**4** Drag a selection rectangle around all the keyframes in the Spline Editor.


**5** In the lower left corner of the Spline Editor, click the Smooth button or press Shift-S to

smooth all the keyframes.


**6** Right-click one of the keyframes and choose Flat.


This will slow the animation just before and just after the keyframe.

**7** Play the animation to see the results.


You produced a more realistic animation just by smoothing the interpolation and flattening

the rate of change on specific keyframes.


**Lesson 7 Addendum: Animating with Keyframes and Modifiers** **186**


## **Applying Random** **Animation Modifiers**

Modifiers can do so many amazing things for your animations, like converting splines to

paths, creating rippling animations for text, and even animating any parameter using

randomly generated values. Random animation can come in very handy when trying to

create a wiggling position animation or flickering lights using brightness controls.


To complement this vintage animation, you’ll use one of DaVinci Resolve’s built-in filters to

create a flickering old-style film look.

**1** Close the Spline Editor and select the Merge1 node in the Node Editor.


You’ll add a filter effect to the entire composition by placing it directly after the

Merge1 node.

**2** In the upper left of the interface, click the Effects Library and, from the OpenFX

category, open the Resolve FX Film Emulation subcategory of filters.


**3** Click the Film Damage tool to add it to the Node Editor and then press 2 to see the

results in the viewer.


**Lesson 7 Addendum: Animating with Keyframes and Modifiers** **187**


**4** Play the composition to review the newly added filter.


The Film Damage filter adds some film scratch lines, a slight vignette, and a sepia tint

to the composition. With all the parameters in the Inspector, you have a great deal of

control for customizing the effect. One addition that would make it more realistic

would be a bit of flickering light simulating an old film projector bulb on its last bit of

energy. Instead of animating this effect, we can use the Perturb modifier to

automatically generate random animation.

**5** In the Inspector, right-click over the Focal Factor label.


The Focal Factor parameter adjusts the strength of the vignette. If you apply a random

animation to this slider, it will give the appearance of a weakening light bulb.

**6** Choose Modify With > Perturb from the contextual menu.


**7** Play the composition and let the animation cache to RAM to review the flickering

animation.


The effect is less a flickering projector bulb and more a slow pulse. As with many

modifiers, you can control several properties to get the look you want.

**8** Click the Modifiers tab at the top of the Inspector.


At the top of the Modifiers tab is the Value setting. The Perturb Value setting uses the

current focal factor setting as a starting point. Dragging the Value slider is similar to

dragging the Focal Factor slider.


**Lesson 7 Addendum: Animating with Keyframes and Modifiers** **188**


Other controls—such as strength, wobble, and speed—control how far the focal factor

parameter varies from the initial value, setting how erratic the motion is and the speed

of the motion. Keeping the Strength setting at a lower value keeps the flickering from

getting too dark or too bright. Keeping the Wobble and Speed higher creates a faster,

more chaotic energy to the animation.

**9** Lower the Strength to 0.5 to make the change in brightness less drastic.

**10** Increase both Wobble and Speed to 10 and play back the animation.


The Perturb modifier is extremely flexible; you can add it to polylines, grid meshes, and

even color gradients to wiggle or randomize almost any parameter you want to animate.
## **Customizing Motion Blur**


As we did with the text in the previous lesson, the last refinement you’ll make to this

animation is to increase its photorealism with some motion blur.

**1** Move the playhead to the middle of the timeline where the plane is onscreen.


**2** Unlike in the previous lesson, where the Text+ node created the motion, here the

Transform1 node is creating the motion. So start by selecting the Transform1 node

connected to the biplane.


**Lesson 7 Addendum: Animating with Keyframes and Modifiers** **189**


**3** In the Inspector, select Tools, and then click the Settings tab and select the Motion

Blur checkbox.


The quality and shutter angle of the motion blur are the two most commonly used

controls for improving the look and spread of the blur; however, increasing these two

controls also increases rendering time.

**4** Increase the Quality to 6 and the Shutter Angle to 200.


The Quality parameter increases the number of times the image is replicated to create

blur. The Shutter Angle simulates the shutter angle in a camera. Higher numbers

create a smoother “smear” between samples. Setting this parameter to 360 is similar

to having the shutter in a camera open for an exposure of one whole frame.


**Lesson 7 Addendum: Animating with Keyframes and Modifiers** **190**


TIP Right-clicking to the right or left of the transport controls allows you to

disable motion blur for the entire composition.


Now you can return to the edit page and use DaVinci Resolve’s smart cache to render

and view your animation.

**5** Click the edit page, and then choose Playback > Render Cache > Smart. Once the cache

is complete, play back the animation.


You have completed your vintage biplane animation and are ready to show your clients

your design.


Completed node tree for Lesson 7.

## **Lesson Review**

**1** True or False? You cannot connect the output of a MediaIn node directly to the input of

a Paint node.

**2** True or False? To attach a paint stroke to a path, you must publish the path.

**3** True or False? When using an image with a premultiplied alpha channel, you must

divide the alpha prior to color correcting it. Then it must be multiplied again before

being connected to a Merge node.

**4** True or False? To auto-orient an object along a motion path, you right-click over the

Center X and Y parameter and choose Connect To > Path > Heading.

**5** True or False? The Displacement parameter controls an object’s position along a

motion path.


**Lesson 7 Addendum: Animating with Keyframes and Modifiers** **191**


##### **Answers**

**1** False. You can connect the output of a MediaIn node directly to the input of a

Paint node.

**2** True. To attach a paint stroke to a path, you must publish the path.

**3** True. When using an image with a premultiplied alpha channel, you must divide the

alpha prior to color correcting it. Then it must be multiplied again before being

connected to a Merge node.

**4** False. To auto-orient an object along a motion path, you right-click over the Angle

parameter and choose Connect To > Path > Heading.

**5** True. The Displacement parameter controls an object’s position along a motion path.


**Lesson 7 Addendum: Animating with Keyframes and Modifiers** **192**


## **Index**

4:2:2 chroma subsampling, _119_ .
_See also_ _chroma key_


**A**

acceleration adjustments, making, _185–186_

aligning clips, _50–53_

alpha channels
defined, _72_
embedding into images, _75–78_
straight and premultiplied, _101_
straightening out, _177–178_

animating
dotted line for plane, _182–185_
with Follower, _153–156_
with keyframes, _27–28_
splines, _123_
Title text, _151–152_

animating with keyframes and modifiers.
_See also_ _keyframes_ ; _modifiers_
auto-orienting objects, _176_
customizing motion blur, _189–191_
with Follower, _153–156_
identifying clip’s resolution, _170–171_
keyframing motion paths, _171–175_
linking parameters, _182–185_
making acceleration
adjustments, _185–186_
painting motion paths, _178–182_
straightening out alpha
channels, _177–178_

animation modifiers, applying, _187–190_ .
_See also_ _modifiers_

Apply Mode, changing to Difference, _51_

arrows and connecting lines, _11_

Auto Resolution button, _68_ .
_See also_ _resolution_

auto-keyframing, disabling on spline
shapes, _44_ . _See also_ _keyframing motion_
_paths_

auxiliary mattes, rotoscoping, _120–129_ .
_See also_ _mattes_



**B**

background, lining up, _129–131_

background banner, creating, _147–150_

Background node, adding, _35_ .
_See also_ _nodes_

background plate, _8_

Background tool, Image tab, _67_

backgrounds. _See also_ _Clean Background_
_slider_
layering images over, _10_
lining up, _129–131_

Backups bin, _112_, _140_

banner. _See_ _background banner_

bins. _See_ _Timelines bin_

biplane, dragging from Clips bin, _171_

black at edge of frame, fixing, _83_

black point, setting, _16_

Blackmagic Cloud Store, _xx_

Blackmagic Design Training and
Certification Program, _x–xi_

Blackmagic URSA clip, _65–66_

blank clips, _6_ . _See also_ _clips_

Blend slider, _27_

Blur slider, _73_ . _See also_ _motion blur_

Blur tool, _26_

brightness, impact of spill
suppression on, _133_

B-Spline tool, _120–122_


**C**

caching clips, _28_

camera motion, restoring, _53–56_

Center X and Center Y fields, _52_, _123_, _143_

certification, getting, _xi_

CG (computer generated), _2_

Channel Booleans node, _70_

chroma key, defined, _116_ . _See also_ _4:2:2_
_chroma subsampling_


**Index** **193**


Clean Background slider, _119_ .
_See also_ _backgrounds_

Clean Foreground slider, _119_

clean plate, _8_

creating for green screen, _112–116_

Clean Plate tool, _114_

clips. _See also_ _blank clips_ ; _Fusion clips_

aligning using nudging, _50–53_
caching, _28_
disabling and enabling, _33–34_
previewing, _10_
undoing in timeline, _64_
viewing, _22_

Clips button, _162_

clip’s resolution. _See also_ _resolution_

identifying, _170–171_
retaining, _60–64_

Clone Apply Mode button, _95_

clone brush, _95–96_

Clone tool, painting with, _93–96_

Cloud. _See_ _Blackmagic Cloud Store_

Color Controls button, _117_

color correcting elements, _131–134_ .
_See also_ _secondary color correction_

Color Corrector node
adding, _83_
tools, _14–15_

Color Corrector
Pre-Divide/Post-Multiply checkbox,

_14–15_, _100_
Suppress wheel, _133_

Color page, sending mattes to, _134–138_

color swatch, opening, _148_

colored input, listing, _24_

colors of connections, _11–12_

Combine Alpha option, _77_

Command key. _See_ _keyboard shortcuts_

commands, undoing, _19_, _28_

Completed Projects bin, _112_

composite
defined, _11_
finalizing, _106–108_



compositing

match moves, _32_

using Darken Apply mode, _69–70_

compositing using Darken apply
mode, _69–70_

compositions, controlling
resolution, _64–69_

concatenation, defined, _55_

Connect To menu, _54–55_, _176_, _183_

connections, colors of, _11–12_

control points, moving, _107_ . _See also_ _points_

Copy command, _145_

Crop node, impact on clip’s resolution, _67_

Ctrl key. _See_ _keyboard shortcuts_

cutout, filling in for green screen, _115_


**D**

dark pixels, adjusting level of, _16_

Darken apply mode, using for
compositing, _69–70_

DaVinci Resolve _20_

downloading, _xi_

quick setup, _xii_

DaVinci Resolve pages, image processing
across, _36_

deleting keyframes, _159_

Delta Keyer

fine-tuning green screen with, _115–119_

fine-tuning with, _115–119_

Matte tab, _131–132_

Difference mode, _51_

downloading

DaVinci Resolve, _xi_

DaVinci Resolve lesson files, _xviii–xix_

drawing mattes, _44–50_ .
_See also_ _rotoscoping_

DRIVER clip, removing motion from, _37–44_

dual viewer setup, returning to, _53_ .
_See also_ _viewers_


**Index** **194**


**E**

edges, smoothing, _73_

Edit page

styling text in, _140–145_

using layers from, _32–36_

effects

adding, _13–17_

disabling, _17_

Soft Glow, _163_

Effects Library

adding effects from, _71–73_

OpenFX category, _28_

opening, _23_

Erode/Dilate node, _74–75_, _119_

expression field, _184_


**F**

F keys. _See_ _keyboard shortcuts_

Film Damage tool, _187_

Focal Factor parameter, _188_

Follower, animating with, _153–156_

fonts

changing, _146_

setting, _142_

Force Source Tile Pictures, Node Editor, _7_

foreground. _See_ _Clean Foreground slider_

frames, creating room around, _173_

framing views. _See_ _reference frame_

Fusion

framing views, _5_

panning around view, _5_

zooming, _5_

Fusion clips, creating, _34_ . _See also_ _clips_

Fusion interface, exploring, _2–4_

Fusion Overlay, selecting, _143_

Fusion page. _See also_ _pages_

button, _62_

keyboard shortcuts, _3_

mouse and keyboard commands, _4_

moving text to, _145–147_



navigating, _4–5_
Node Editor, _3_
sections, _3_
tracking in, _37–44_


**G**

Gain slider, _16_

gamma and lift, increasing, _177_

Gamma control, _16_

Garbage Matte, _103_, _122_

Global In/Out bar, _130_

glow effect, creating, _25–26_

Gradient type. _See also_ _text_

choosing for text, _143–144_
using for background banner, _148_

graphic line, drawing between
parameters, _184_

graphics. _See_ _signs and screens_

green-screen content
adding MediaOut node, _134_
color correcting elements, _131–134_
creating clean plate, _112–115_
fine-tuning with Delta Keyer, _115–119_
lining up background, _129–131_
rotoscoping auxiliary mattes, _120–129_
setting up color page, _135–136_

Grow Edges control, _115_


**H**

High threshold slider, _73_

holdout mattes, rotoscoping, _123–129_ .
_See also_ _mattes_

holes in keys, fixing, _74–75_


**I**

image processing, _36_

images
combining mattes with, _102–104_
combining using nodes, _9–12_
embedding alpha into, _75–78_
filling viewer with, _69_


**Index** **195**


images ( _continued_ )
fitting into viewer, _5_
layering over backgrounds, _10_
showing in viewers, _3_

input devices, _4_

Inspector, displaying, _3_

installing DaVinci Resolve lesson
files, _xviii–xix_

IntelliTrack AI tool, _39_

interface, resetting, _2_

interrupted trackers, fixing, _82–83_ .
_See also_ _trackers_

Invert Matte checkbox, _77_


**K**

key, fixing holes in, _74–75_

keyboard commands, context sensitivity, _4_

keyboard shortcuts
closing mattes, _121_
closing shapes, _49_
Copy command, _145_
disabling effects, _17_
enabling and disabling, _33–34_
fitting images into viewer, _5_
Fusion page, _3_, _62_
inserting nodes, _19_
moving playhead to start of
render range, _38_
moving points, _126_
navigating in Fusion, _5_
Paste command, _145_
removing nodes, _19_
renaming nodes, _8_
Select tool, _83_
switching nodes, _12_
undoing commands, _19_, _28_, _64_

keyframe timing, adjusting, _157–161_

keyframes. _See also_ _animating with_
_keyframes and modifiers_
animating with, _27–28_
deleting, _159_
moving playhead to, _123_



Keyframes Editor
changing interpolation in, _160–161_
displaying tracks in, _130_, _157_
selecting keyframes in, _159_
selecting MediaIn nodes, _159_
Sort menu, _158_
T offset field, _160_

keyframing motion paths, _171–175_ .
_See also_ _auto-keyframing_ ;
_motion paths_

keying
foreground subject, _136_
as iterative process, _114_

keys, fixing holes in, _74–75_


**L**

layers. _See also_ _Photoshop PSD layers_

displaying for Fusion clips, _35_
using from Edit page, _32–36_

lens distortion, removing, _90_

lesson files, getting, _xviii–xix_

lift and gamma, increasing, _177_

Lift control, _16_

Lift slider, dragging, _14_

line, drawing between parameters, _184_

logo, fixing “strobed” motion in, _107–108_

Low threshold slider, _73_

lower-third rule, using with text, _147_ .
_See also_ _TRAINING LOWER THIRD_
_template_

luma key, blurring, _25–26_

Luma key node, _22_ . _See also_ _nodes_

Luma Keyer, _23_, _69_, _71–72_

luminance, raising, _133_


**M**

macOS users, _xii_

Macro Editor window, _164_

macro list, _165_

map clip, _170–171_

mask and matte, _45_

masks, working with, _20–22_


**Index** **196**


match moves, _32_

match moving with Planar
transform, _104–105_

matte and mask, _45_

Matte category, choosing from Tools, _23_

Matte Control, displaying in viewer, _103_

Matte Control node, _75–78_

matte edges, expanding or
shrinking, _74–75_

mattes. _See also_ _auxiliary mattes_ ;

_holdout mattes_

closing, _121_

combining with images, _102–104_

combining with RGB images, _75–78_

drawing, _44–50_

filling in black holes in, _119_

performing changes to, _106_

revealing text with, _151–152_

rotoscoping, _120–129_

sending to color page, _134–136_

softening edges of, _128_

Media Pool button, _171_

Media Pool panel, closing, _23_

MediaIn node

adding thumbnails to, _6–7_

Keyframe Editor, _159_

selecting and loading, _9_

MediaOut node, disconnecting, _6_

Merge node

creating and adding, _68_

displaying, _66_

dragging, _67_

transform controls in, _173_

Merge node, adding, _10_

Merge tool, _10_

Minimum mode, _70_

modifiers. _See also_ _animating with_
_keyframes and modifiers_

adding to motion paths, _153–154_

linking parameters to, _176_

Transform path, _182_



Modify Only button, _126_

motion blur. _See also_ _Blur slider_

customizing, _189–191_

disabling, _191_

motion paths

adding modifiers to, _153–154_

keyframing, _171–175_

painting, _178–182_

mouse commands, context sensitivity, _4_

MultiPoly node, _124–125_

Multitext tool, _146_


**N**

Node Editor

adding media to, _9_

Force Source Tile Pictures, _7_

nodes in, _3_

setting up, _6–8_

source tile pictures, _7_

work area, _4_

zooming, _4_

node flow, understanding, _17–19_

node names, restriction, _36_

node trees

constructing, _55_

reverse-engineering, _112_

nodes. _See also_ _Background node_ ; _Luma_
_key node_

adding, _14_

enabling and disabling, _17_

inserting, _19_

reconnecting, _12_

removing, _19_

renaming, _8_

selecting, _163_

switching, _12_

and tools, _6_

using to combine images, _9–12_

viewing, _157_

nudging clips, _50–53_


**Index** **197**


**O**

objects, auto-orienting, _176_

Operation tab, using with tracking data, _42_

Options button, _15_

overlay menu, _143_


**P**

“P” in Command-P/Ctrl-P
(“pass‑through”), _17_

pages, image processing across, _36_ .
_See also_ _Fusion page_

painting
with Clone tool, _93–96_
motion paths, _178–182_

panning viewers, _5_, _47_, _95_

parallax, occurrence of, _41_

parameters
linking, _182–185_
linking to modifiers, _176_

PASSENGER clip, removing motion
from, _37–44_

Paste command, _145_

Path Center menu, _82_

pen and tablet input devices, _4_

Perturb option, _188_

Photoshop PSD layers, using, _96–101_ .
_See also_ _layers_

pick whip, defined, _184_

pipes
described, _11_
disconnecting, _12_

pixels, selecting ranges of, _24_

planar surfaces, tracking, _88–92_

Planar Tracker, displaying in viewer, _89_

planar tracking, selecting area for, _90_

Planar transform, match moving
with, _104–105_

plate, defined, _8_

playhead
dragging through render range, _8_
moving to keyframes, _123_
moving to start of render range, _38_



Point tracker, _81_

point tracker. _See also_ _tracker points_

adding, _38_
search box, _39_

points. _See also_ _control points_

moving, _126_
smoothing corners of, _128_

Polygon button, _126_

polygon matte, refining, _123_

Polygon shape tool, _45–46_

Polygon tool, _102_

Polyline Stroke brush, _178–182_

Post Multiply Image option, _77_

Pre-Divide/Post-Multiply option, color
corrector, _14–15_, _100_

premultiplied alpha channel, _101_

previewing clips, _10_

Project Manager, Restore Project
Archive, _140_

PSD layers, using, _96–101_ . _See also_ _layers_

puck, identifying, _25_


**Q**

Quality parameter, _190_


**R**

radial gradient, _148_

RAM, assigning for Fusion, _9_

range slider, _24_

Rectangle tool, _151_

reference frame
exporting, _98_
setting, _91_

Render Cache option, _29_

Replace Color, setting to Source, _132_

Reset UI Layout, _2_

Resize node, impact on clip’s resolution, _67_

resolution. _See also_ _Auto Resolution button_ ;

_clip’s resolution_
controlling for compositions, _64–69_
retaining for clips, _60–64_

Restore Project Archive, _140_


**Index** **198**


RGB images, combining mattes
with, _75–78_

rotoscoping. _See also_ _drawing mattes_

auxiliary mattes, _120–129_
balancing, _123_
holdout mattes, _123–129_
process of, _20_


**S**

saving templates, _163–166_

screens and signs. _See_ _signs and screens_

secondary color correction, _22–26_ .
_See also_ _color correcting elements_

Select tool, _37_, _71_, _83_

Settings button, _27_

Shading tab, using with text, _143_

shapes
closing, _49_
moving points of, _126_

Shift key. _See_ _keyboard shortcuts_

shots
“breaking,” _51_
stabilizing, _40_

signs and screens
combining mattes and images, _102–104_
finalizing composite, _106–108_
match moving with Planar
Transform, _104–105_
painting with Clone tool, _93–96_
tracking planar surfaces, _88–92_
using Photoshop PSD layers, _96–101_

sky
blending in, _83–84_
fixing interrupted trackers, _82–83_
tracking into position, _78–81_

sky replacement
adding effects, _71–73_
composition’s resolution, _64–69_
Darken Apply mode, _69–70_
embedding alpha in image, _75–78_
fixing holes in key, _74–75_
metadata badge, _65–66_
retaining clip’s resolution, _60–64_



smoothing edges, _73_

Soft Glow effect, _163_

Soft Light apply mode, _99_

spill suppression, _133_

spline shapes, disabling
auto‑keyframing on, _44_

splines, animating, _123_

split screens, compositing, _31–32_

split-screen effect
aligning clips, _50–53_
creating, _34–36_
drawing mattes, _44–50_
nudging clips, _50–53_
restoring camera motion, _53–55_
tracking in Fusion page, _37–44_

stabilization, using trackers for, _42–44_

stabilizing shots, _40_

Steady setting, _92_

straight alpha channel, _101_

Stroke tool, _94_

system requirements, _xi_


**T**

tablet and pen input devices, _4_

Template node, creating for text, _145_

templates, saving, _163–166_

text. _See also_ _Gradient type_ ; _words_

lower-third rule, _147_
moving to Fusion page, _145–147_
revealing with mattes, _151–152_
styling in Edit page, _140–145_

Text+ tool, _142_

three-button mouse, recommendation, _4_

time ruler
contents, _8_
locating, _3_

Time Speed tool, _93_

timeline
returning to, _29_
undoing clips in, _64_

timeline ruler, dragging in, _157_

timeline tracks, centering, _129_


**Index** **199**


timeline versions, _162–163_

Timelines bin, contents of, _112_, _140_, _170_

Title text, animating, _151–152_

toolbar, locating, _3_

tools

Background, _67_

Blur, _26_

B-Spline, _120–122_

Clean Plate, _114_

Clone, _93–96_

Film Damage, _187_

Merge, _10_

Multitext, _146_

and nodes, _6_

Polygon, _102_

Polygon shape, _45–46_

Rectangle, _151_

revealing categories, _23_

Select, _37_, _83_

Stroke, _94_

Text+, _142_

Time Speed, _93_

Tracker, _37_

Track Center (Append) setting, _82–83_

Track Forward button, _83_

Tracker modifier, _79–80_

tracker points, adding, _40_ . _See also_ _point_
_tracker_

Tracker tool, _37_

trackers. _See also_ _interrupted trackers_

renaming, _40_

using for stabilization, _42–44_

tracking

in Fusion page, _37–44_

planar surfaces, _88–92_

sky into position, _78–81_

tracking data, Operation tab, _42_

tracking points, selecting, _41_

tracking process, resuming, _91_



tracks
expanding horizontally, _157_
testing, _92_

TRAINING LOWER THIRD template, _166_ .
_See also_ _lower-third rule_

Training Media folder, contents of, _2_

Transform node, adding, _54_, _63_

Type options, choosing for text, _143_


**U**

undoing commands, _19_, _28_, _64_


**V**

Val, Steve, _113_

versions, trying out, _161–163_

view status, resetting for viewers, _128_

viewer setup, changing, _53_

viewers. _See also_ _dual viewer setup_

filling in with image, _69_
increasing, _121_
panning, _47_
resetting view status of, _128_
resizing, _45_
zooming in and out of, _5_

viewing clips, _22_, _26_

views, framing, _5_

vignettes, adding, _28_


**W**

white point, setting, _16_

Windows users, _xii–xviii_

words, animating, _153–156_ . _See also_ _text_

work area, locating, _3_

Write On End slider, Modifiers tab, _182–183_


**Z**

Zoom To Fit button, _129_

zooming
in and out of viewers, _5_
in Node Editor, _4_


**Index** **200**


**This page is intentionally left blank ﻿** **201**


The Fusion page in DaVinci Resolve 20 features hundreds of
advanced tools for visual effects compositing. This official
hands on training guide introduces you to a core set of tools in
five easy lessons.


The lessons will let you experience how to create visual effects
directly inside DaVinci Resolve, without importing or exporting
large media files between applications.


You’ll learn how its node based interface makes it easy to
quickly build commonly requested visual effects and quickly
make changes.


**What You’ll Learn**

- Fundamentals of compositing using nodes

- Combining optimal takes with the split screen technique

- Tracking objects using the point tracker and planar tracker

- Compositing with multi layer PSD files

- Advanced sky and sign replacement

- Green screen compositing with the delta keyer and clean plate

- Rotoscoping to produce clean traveling mattes

- Two addendum chapters on how to create motion graphics.


**Who This Book Is For**

This book is designed for editors and colorists wanting to learn
how to create visual effects, as well as artists transitioning from
other visual effects applications. Beginners will find clear and
concise lessons that introduce how the Fusion page integrates
with the other pages as well as core concepts and user interface
navigation. If you’re a professional switching from another
application, you’ll find lessons that cover the fundamentals for
keying, sky replacement, and tracking, as well as dozens of tips
and tricks that will transform how you work!



**Key and Composite Green Screens**


**Replace Signs Using Planar Tracking**


**Use Nodes to String Effects Together**


**Create Believable Split-Screen Shots**


