<!-- TOC
- Contents (p.4)
- Foreword (p.6)
- Acknowledgments (p.7)
- About the Authors (p.7)
- Who This Book Is For (p.8)
- Getting Started (p.9)
- Introducing Blackmagic Cloud (p.19)
- Creating a 3D Scene (p.20)
  - Placing Elements in 3D Space (p.21)
  - Navigating in 3D (p.27)
  - Using 3D Text  (p.33)
  - Setting Up a Camera (p.38)
  - Adding Lights  (p.45)
  - Converting 3D into a 2D Image (p.52)
  - Lesson Review (p.58)
- Exploring a Green-Screen Workflow (p.60)
  - Managing Color for Visual Effects (p.61)
  - Removing Noise (p.67)
  - Pulling a Key (p.70)
  - Adding Natural Light Spill (p.86)
  - Creating a 3D Windshield Reflection (p.91)
  - Lesson Review (p.102)
- Creating a Rainy Day (p.104)
  - Merging 2D and 3D (p.105)
  - Patching Together a Sky Replacement (p.111)
  - Magically Creating a Mask (p.116)
  - Adding Reflections (p.124)
  - Correcting Color in Fusion (p.128)
  - Generating 3D Particles (p.132)
  - Lesson Review (p.146)
- 3D Camera Tracking (p.148)
  - Masking for 3D Tracking (p.149)
  - Preparing the Camera Tracker (p.157)
  - Solving for the Camera (p.161)
  - Refining the Solve (p.163)
  - Exporting the Scene (p.166)
  - Positioning Objects in a 3D Set (p.172)
  - Matching Color and Light (p.175)
  - Lesson Review (p.178)
- Compositing 3D with USD (p.180)
  - Importing USD into Fusion (p.181)
  - Creating Surfaces with Shaders (p.185)
  - Rendering USD (p.190)
  - Making a Dragon Fly (p.193)
  - Matching Lights to a Scene (p.196)
  - Creating a Flight of Dragons (p.205)
  - Using Z Depth in Color Correction (p.209)
  - Finishing the Comp (p.216)
  - Lesson Review (p.218)
- Index (p.220)
-->
## Advanced Visual Effects in


**Advanced Visual Effects in DaVinci Resolve 20**


Damian Allen, Dion Scoppettuolo


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


(Mac) and (macOS) are registered trademarks of Apple Inc., registered in the U.S. and other countries. Windows is a

registered trademark of Microsoft Inc., registered in the U.S. and other countries.


ISBN 13: 979-8-9924874-5-9


## **Contents**

Foreword v


Acknowledgments vi


About the Authors vi


Who This Book Is For vii


Getting Started viii


Introducing Blackmagic Cloud xviii


1 Creating a 3D Scene 1


Placing Elements in 3D Space 2


Navigating in 3D 8


Using 3D Text 14


Setting Up a Camera 19


Adding Lights 26


Converting 3D into a 2D Image 33


Lesson Review 39


2 Exploring a Green-Screen Workflow 41


Managing Color for Visual Effects 42


Removing Noise 48


Pulling a Key 51


Adding Natural Light Spill 67


Creating a 3D Windshield Reflection 72


Lesson Review 83


3 Creating a Rainy Day 85


Merging 2D and 3D 86


Patching Together a Sky Replacement 92


Magically Creating a Mask 97


**Contents** **iii**


Adding Reflections 105

Correcting Color in Fusion 109

Generating 3D Particles 113

Lesson Review 127


4 3D Camera Tracking 129


Masking for 3D Tracking 130

Preparing the Camera Tracker 138

Solving for the Camera 142

Refining the Solve 144

Exporting the Scene 147

Positioning Objects in a 3D Set 153

Matching Color and Light 156

Lesson Review 159


5 Compositing 3D with USD 161


Importing USD into Fusion 162

Creating Surfaces with Shaders 166

Rendering USD 171

Making a Dragon Fly 174

Matching Lights to a Scene 177

Creating a Flight of Dragons 186

Using Z Depth in Color Correction 190

Finishing the Comp 197

Lesson Review 199


Index 201


**Contents** **iv**


## **Foreword**

**Welcome to Advanced Visual Effects in DaVinci Resolve 20.**


DaVinci Resolve 20 is the only post-production solution that combines editing, color

correction, visual effects, motion graphics, and audio post-production all in one software

tool! Its elegant, modern interface is fast to learn for new users yet powerful enough for

the most experienced professionals. DaVinci Resolve lets you work more efficiently

because you don’t have to learn multiple apps or switch software for different tasks. It’s

like having your own post-production studio in a single app!


DaVinci Resolve 20 adds editing with transcriptions from audio, film look creator and

ColorSlice six vector grading, IntelliTrack AI for panning audio to match vision, broadcast

replay for live multi-camera broadcast editing, layout and replay with speed control, and

so much more!


Best of all, Blackmagic Design offers a version of DaVinci Resolve 20 that is completely free!

We’ve made sure that this version of DaVinci Resolve includes more features than any paid

editing system. That’s because at Blackmagic Design we believe everybody should have

the tools to create professional, Hollywood-caliber content without having to spend

thousands of dollars.


I invite you to download your copy of DaVinci Resolve 20 today and look forward to seeing

the amazing work you produce!


Grant Petty

Blackmagic Design


**Foreword** **v**


## **Acknowledgments**

We would like to thank the following individuals for their contributions of media and

imagery used throughout the book:


- ActionVFX for the green screen and Dry4wet content from their practice footage at

[Actionvfx.com](http://Actionvfx.com)
## **About the Authors**


**Damian Allen** is a visual effects and animation consultant, developer, and supervisor in

Hollywood. He is the owner of the VFX company Pixerati LLC, with a focus on virtual

production, picture-lock visual effects emergencies, and VR and animation tool development.

Damian is also a core contributor to the [moviola.com](http://moviola.com) training site for filmmakers.


**Dion Scoppettuolo** is a Certified Blackmagic Design Master Trainer. He has taught classes

on DaVinci Resolve in Hollywood and New York City, as well as across Europe and Asia.

Mr Scoppettuolo has extensive industry experience in editing and visual effects, having

held the position of Senior Product Manager for Pro Applications at Apple Inc.


**About the Authors** **vi**


## **Who This Book Is For**

This hands-on training guide is designed for DaVinci Resolve editors, colorists, and visual

effects artists with some basic knowledge of DaVinci Resolve’s Fusion page. The lessons in

this book provide an introduction to advanced tools for creating 3D visual effects in the

Fusion page.


You’ll start with an introductory composite that will give you a a foundation for working in

a 3D environment within the Fusion page interface. Each subsequent lesson introduces

you to new 3D visual effects tools. You’ll cover a variety of 3D techniques, and technical

best practices including depth of field, 3D camera tracking, and integrating Universal

Scene Description content.


The majority of lessons in this guide use tools only available in DaVinci Resolve Studio 20,

which can be purchased from [www.blackmagicdesign.com.](http://www.blackmagicdesign.com)


**Who This Book Is For** **vii**


## **Getting Started**

Welcome to _Advanced Visual Effects in DaVinci Resolve 20_, an official Blackmagic Design

certified training book that teaches professionals and students the art of 3D visual effects

compositing in DaVinci Resolve Studio 20. Creators will find clear workflow-driven lessons,

while colorists will quickly learn Fusion’s powerful node-based interface to accomplish

incredible Hollywood-caliber visual effects.


As you step through the lessons, you’ll gain experience with Fusion’s 3D camera tracking,

powerful USD capabilities, A.I. based masking tools, and more! Best of all, you’ll discover

that there is no longer a need to send shots out to another application because with

DaVinci Resolve 20, fantastic visual effects are simply a click away from editing.


This guide takes a practical, hands-on approach using real-world techniques for various

compositing jobs. Each lesson provides some practical use of 3D tools even when the

composite may be primarily a 2D technique. As you complete each lesson, you’ll have

opportunities to answer sample test questions to test your comprehension of

the techniques.


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


In these lessons, you’ll work with multiple projects and timelines to learn the fundamental

3D toolset commonly used in a wide range of visual effects techniques. You’ll acquire

real-world skills that you can apply to real-world productions.


**Getting Started** **viii**


Lesson 1 is an introductory lesson that allows students who are new to 3D compositing to

explore the user interface by creating a simple but commonly requested 3D flythrough.

This lesson is meant to reintroduce you to the Fusion workflow while giving you your first

taste of a few essential 3D tools that you will use throughout this guide.


Lessons 2–5 cover the most common 3D visual effects techniques that you can use

on a broad range of jobs. You’ll discover how to combine 2D and 3D scenes in a single

composite. Using the 3D camera tracking you’ll learn how to match a live action camera to

create seamless blending of particles and set extensions. Finally, you’ll learn how to import,

manipulate, and animate Universal Scene Description elements in order to combine true

3D models with live action media.

##### **The Blackmagic Design Training** **and Certification Program**


Blackmagic Design publishes several training books that take your skills further in

DaVinci Resolve 20. They include:


- _The Beginner’s Guide to DaVinci Resolve 20_

- _The Colorist Guide to DaVinci Resolve 20_

- _The Editor’s Guide to DaVinci Resolve 20_

- _The Fairlight Audio Guide to DaVinci Resolve 20_

- _The Visual Effects Guide to DaVinci Resolve 20_

- _Advanced Visual Effects in DaVinci Resolve 20_











































Whether you want an introductory guide to DaVinci Resolve or you want to learn more

advanced editing techniques, color grading, sound mixing, or visual effects, our certified

training program includes a learning path for you.


**Getting Started** **ix**


##### **Getting Certified**

After completing this book, you are encouraged to take the 1-hour, 50-question online

proficiency exam to receive a Certificate of Completion from Blackmagic Design. The exam

questions are taken from the five lessons in this book. The link to the exam is located at

the end of this book.


The webpage also provides additional information on our official Training and Certification

Program. Please visit [www.blackmagicdesign.com/products/davinciresolve/training.](http://www.blackmagicdesign.com/products/davinciresolve/training)

##### **System Requirements**


This book supports DaVinci Resolve Studio 20 for Mac and Windows. If you have an older

version of DaVinci Resolve or the free version of DaVinci Resolve 20, you must upgrade to

the current DaVinci Resolve Studio version to completely follow along with the lessons.


NOTE The exercises in this book refer to file and resource locations that will

differ if you are using the version of software from the Apple Mac App Store.

For the purposes of this training book, if you are using macOS, we recommend

downloading the DaVinci Resolve software from the Blackmagic Design website

rather than from the Mac App store.

##### **Download DaVinci Resolve**


To download the Studio version of DaVinci Resolve 20 or later from the

Blackmagic Design website:

**1** Open a web browser on your Windows or Mac computer.

**2** In the address field of your web browser, type

[www.blackmagicdesign.com/products/davinciresolve.](http://www.blackmagicdesign.com/products/davinciresolve)

**3** On the DaVinci Resolve landing page, click the Buy Online button.

**4** After checkout, on the download page, click the Mac or Windows button, depending

on your computer’s operating system.

**5** Follow the installation instructions to complete the installation.


When you have completed the software installation, follow the instructions in the following

section to download the content for this book.


**Getting Started** **x**


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


**Getting Started** **xi**


**1** If required, you can change the language used. You can also learn more about these

and hundreds of other amazing features available in DaVinci Resolve 20 by clicking

Learn More. Otherwise, click Continue.


Next, you are invited to go through the Quick Setup process. Experienced users can

skip this process by clicking “Skip and Start Right Now,” but new users are advised to

follow this process. It will only take a couple of minutes and is useful in understanding

how Resolve is working.


**Getting Started** **xii**


**2** Click the Quick Setup button.


**3** DaVinci Resolve will check your system to ensure its operating system and graphics

card will perform well. If both pass this test, click Continue.


**Getting Started** **xiii**


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


**Getting Started** **xiv**


**5** Leave this set to the default location and click Continue.


On the next screen, you will be asked which keyboard layout you would like to use. This

is specifically relevant if you’re familiar with using another nonlinear editor; however,

throughout this Advanced Visual Effects Guide you will be introduced to keyboard

shortcuts that use the DaVinci Resolve keyboard layout. So if you change the layout at

this point, you may find those shortcuts won’t work.


**Getting Started** **xv**


**6** For now, leave the layout set to DaVinci Resolve and click Continue.


Congratulations! You have completed the Quick Setup process and have changed

precisely nothing in terms of DaVinci Resolve’s default setup. Nevertheless, you have

also gained an insight into some aspects of using DaVinci Resolve that will serve you

well as you continue learning about the application and how it uses your system.

**7** Click Start to launch and begin enjoying DaVinci Resolve 20!


**Getting Started** **xvi**


Once loaded, DaVinci Resolve will open to the cut page, which is the default starting

page for all projects. However, this is not the usual place to begin working with

DaVinci Resolve. Instead, you should now exit the application in readiness to begin the

first lesson in this book.

**8** Choose DaVinci Resolve > Quit DaVinci Resolve or press Command-Q (macOS) or

Ctrl-Q (Windows).


DaVinci Resolve 20 will close.

##### **Get the Lesson Files**


The DaVinci Resolve lesson files must be downloaded to your Mac or Windows computer

to perform the exercises in this book. After you save the files to your hard disk, extract the

file and copy the folder to your Movies folder (Mac) or Videos folder (Windows).


**To Download and Install the DaVinci Resolve Lesson Files**


When you’re ready to download the lesson files, follow these steps:

**1** Open a web browser on your Windows or Mac computer.

**2** In the address field of your web browser, type

[www.blackmagicdesign.com/products/davinciresolve/training.](http://www.blackmagicdesign.com/products/davinciresolve/training)

**3** Scroll the page until you locate _Advanced Visual Effects in DaVinci Resolve 20_ .

**4** Click the Part 1 link to download the media. The DR20 Studio Fusion 3D Training

_Media.zip_ file is roughly 3 GB in size.

**5** After downloading the zip file to your Mac or Windows computer, open your

Downloads folder and double-click DR20 Studio Fusion 3D Training Media.zip to unzip

it if it doesn’t unzip automatically. You’ll end up with a folder named DR20 Studio

Fusion 3D Training Media that contains all the content for this book.

**6** From your Downloads folder, drag the DR20 Studio Fusion 3D Training Media folder to

your Movies folder (Mac) or Videos folder (Windows). These folders can be found within

your User folder on either platform.


You are now ready to begin Lesson 1.


**Getting Started** **xvii**


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


Once created, you can access this library directly from the Cloud tab in the Project

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


**Introducing Blackmagic Cloud** **xviii**


### Lesson 1
# Creating a 3D Scene



Although this book assumes you

have some minimal experience with

the Fusion page in DaVinci Resolve,

this first lesson is a very basic and

introductory lesson on the essential

3D toolset in Fusion. The additional

lessons in this book will build on those

foundational 3D skills, diving into

more tools and techniques. The first

question you might have is, why do

we need to work in 3D? Many visual

effects are about reproducing the

characteristics of the real world, such

as perspective, atmosphere, depth

cues, and occlusion of objects in a

scene. While you could simulate these

effects using 2D compositing, they

become much easier and more realistic

in a 3D compositing environment.



Time

This lesson takes approximately
1 hour to complete.

Goals

Placing Elements in 3D Space 2

Navigating in 3D 8

Using 3D Text  14

Setting Up a Camera 19

Adding Lights  26

Converting 3D into a 2D Image 33

Lesson Review 39


This lesson introduces you to the basic construction of a 3D scene by creating a simple

“3D card”-type flythrough. Flat 2D images (or “cards”) are placed in 3D space, arranged at

varying depths, and the virtual camera moves through the scene to create a sense of

depth and perspective. You’ll learn how to navigate in 3D space and use some of the

everyday tools for 3D compositing and motion graphics.


Completed composite for Lesson 1

## **Placing Elements in 3D Space**


Fusion’s 3D compositing includes the ability to position multiple elements in 3D space. You

can position still images, videos, 3D models, text, cameras, and lights and apply various

tools designed to generate 3D visual effects and motion graphics. However, since you can

freely mix 2D and 3D in a single node graph, you begin by entering the Fusion page.


For this first lesson, instead of getting to the Fusion page from the edit page timeline, you

will create a Fusion composition in a bin. This is often appropriate when creating motion

graphics when you may not be ready to edit them into a timeline, but you need to begin

creating the graphics for a project.


NOTE The Timelines bin includes a Backups bin with Fusion comps saved at

various stages of the lesson, available for reference and reverse-engineering

the node trees.


**Lesson 1 Creating a 3D Scene** **2**


**1** Open DaVinci Resolve, right-click in the Project Manager, and choose Restore

Project Archive.

**2** Navigate to the DR20 Studio Fusion 3D Training Media folder.


This folder contains five DaVinci Resolve Archives and a separate “Fusion files” folder,

all of which we will use throughout the exercises in this guide. We’ll start with the

Fusion 20 3D archive.

**3** Select the **Fusion 20 3D.dra** (DaVinci Resolve Archive) file and click Open to add the

Fusion 20 3D Animation project to the Project Manager.

**4** Open the Fusion 20 3D Animation project from the Project Manager and then select

the edit page, if necessary.


This project has no timeline. For this lesson, you’ll create a Fusion composition

in the bin.

**5** Right-click the Fusion Comps bin and choose New Fusion Composition.


**6** In the dialog, name the clip **Wildlife Open**, keep the duration at 5 seconds, and then

click Create.


The benefit of creating a Fusion composition in a bin is that it can be opened in

the Fusion page without any media associated with it initially and without creating

a timeline.


TIP If you accidentally alter your interface and find it hard to follow along,

selecting Reset UI Layout from the Workspace menu will return the interface

to its default state, which should (mostly) match the layout used in this book.


**Lesson 1 Creating a 3D Scene** **3**


**7** Right-click the Wildlife Open clip in the bin and choose Open in Fusion Page.


For this project, you will use elements from the media pool to create a 3D scene.

**8** In the upper left corner of the Fusion page, click the Media Pool button and select

the Media >Wildlife Assets bin.


This bin contains a few graphic illustrations that you will use to create a motion

graphics flythrough.

**9** From the Wildlife Assets bin, drag the **Sunset HD graphic** into an empty area of the

Node Editor and press 2 to display it in viewer 2. Close the media pool to give yourself

room to work.


This is a stylized savannah sunset illustration that we will use as the background of our

scene. Let’s get organized right from the start by renaming each new element.

**10** In the Node Editor, select the MediaIn1 node, press F2, and rename this

image **SUNSET** .


No video clip, still image, or 2D generator can be part of a 3D scene without first

connecting to an Image Plane 3D node or a Shape 3D node.


**Lesson 1 Creating a 3D Scene** **4**


**11** With the SUNSET node selected, open the Effects Library, and from the Tools > 3D

category, scroll down and click the Image Plane 3D tool. Then press 1 to view the

sunset graphic in 3D space.


The sunset graphic now appears in a 3D viewer. It is placed on a 3D image plane and

can be rotated and viewed from any angle.

**12** In viewer 1, while holding the middle mouse button, Option-drag (macOS) or Alt-drag

(Windows) left, right, up, and down to rotate the perspective angle.


By using the modifier key and middle mouse combination when dragging, you can

rotate around the image to see it from alternate angles. To be clear, you are not rotating

the image itself; you are changing your view as if you were walking around the image.


TIP Using an Image Plane 3D instead of a Shape 3D node will retain the

aspect ratio of the image connected to it, which is especially useful for

video clips.


**13** Close the Effects Library and open the media pool.

**14** From the Wildlife Assets bin, drag the **Giraffe** graphic into an empty area of the Node

Editor. Press 1 to display it in viewer 1. Press F2, rename the image **GIRAFFE**, and then

close the media pool again.


**Lesson 1 Creating a 3D Scene** **5**


**15** With the GIRAFFE node selected, press Shift-Spacebar and type **image** to add an

Image Plane 3D to the Node Editor.

**16** Press 1 to view the GIRAFFE’s Image Plane 3D node in 3D space.


The giraffe is also displayed in a 3D viewer, but the two images are not connected and

cannot interact. Each exists in its own 3D world. However, you can combine 3D images

to exist in the same 3D world using a Merge 3D node located in the toolbar.


While the Merge node is the fundamental 2D compositing tool, the Merge 3D node is

the fundamental 3D compositing tool. And as with the Merge tool, you can create a

Merge 3D node just by connecting the output of two 3D nodes.


**Lesson 1 Creating a 3D Scene** **6**


**17** Drag the output of GIRAFFE’s Image Plane 3D node to the output of SUNSET’s Image

Plane 3D node to create a Merge 3D. Press 1 to load Merge3D1 into viewer 1.


Both images are combined in the Merge 3D node, but they overlap in exactly the same

space, which is why there may be some breakup in the composited image in viewer 1.


The viewer shows the images on top of each other, fighting for the same 3D location.

This is sometimes called “Z-fighting” for that reason. To fix the conflict, you can change

the Z position of one of the images.

**18** Select the GIRAFFE’s Image Plane 3D node, and in the Inspector’s Transform tab, drag

the Z Translation right to any small value above 0.0.


Unlike 2D compositing with a Merge node, you do not change the inputs to the Merge 3D

node to get the giraffe in front of or behind the sunset graphic. That ordering is done by

changing the Z Translation value.


A positive Z value brings an object forward in space, while a negative value moves it back.

By using a value above 0.0, you’ve moved the giraffe in front of our sunset background.


**Lesson 1 Creating a 3D Scene** **7**


## **Navigating in 3D**

Since the Z translation value determines the layer order, it is extremely important that you

understand how to move elements and change your view of them in 3D space. To build a

more interesting scene and better understand 3D positioning, let’s add three more

elements and place them on Image Plane 3D nodes.

**1** From the Wildlife Assets bin, add the Elephant, Foreground HD, and Lion graphics into

the Node Editor.

**2** Rename each element as their bin clip name: **Elephant**, **Foreground**, and **Lion** .

**3** Place each one on an Image Plane 3D and connect each Image Plane to the Merge 3D.


Similar to the Multimerge node for 2D compositing, the Merge 3D allows an unlimited

number of inputs.

**4** Enter the values listed below as new Z translation values for each image’s Image Plane

3D to create some distance between the new elements and the sunset background:

**a)** Elephant Image Plane 3D Z translation value: **0.4**

**b)** Foreground Image Plane 3D Z translation value: **0.75**

**c)** Lion Image Plane 3D Z translation value: **0.76**


**Lesson 1 Creating a 3D Scene** **8**


In Fusion’s 3D world, the origin point of the coordinate system is in the center of the

world (X = 0, Y = 0, and Z =0). Each element you add to the 3D world will start at this

0,0,0 location. X is the horizontal axis, Z is the depth axis, and Y is the vertical axis.


TIP In some other applications (e.g., 3D Studio Max, Unreal Engine), the Z axis

is the vertical axis, and the Y axis is the depth axis. Therefore, be careful if you

simply copy and paste values between applications.


To move an image in 3D space, you use the Image Plane 3D node (or other 3D object

nodes like Shape 3D), which adds 3D positioning, rotation, pivot, and scale controls

to an image.


The animals may appear too large for our sunset background, so we can quickly scale

them more appropriately.

**5** Going through each Image Plane 3D, use the Scale to resize the elements as follows:

**a)** Lion: Scale **0.1**

**b)** Foreground: Scale **0.3**

**c)** Elephant: Scale **0.3**

**d)** Giraffe: Scale **0.4**


**Lesson 1 Creating a 3D Scene** **9**


Although the actual values don’t really matter, and the current values may result in

small animals in our viewer, the values we used create a nicely dispersed group of

animals where their size and Z position give a semi-realistic appearance. We can take

that a bit further by adjusting their horizontal position.

**6** Select the GIRAFFE’s Image Plane 3D node, and In the Inspector, drag the X Translation

left to move the giraffe slightly to the left until the value is between -0.1 and -0.15.


The X Translation moves the giraffe to the left. You can perform the same transform

operation using the red arrow in the viewer. Other viewer arrow overlays move the

object up and down (the green, Y translate arrow) or toward and away from you (the

blue, Z translate arrow).

**7** Select the Elephant’s Image Plane 3D node, and in viewer 1, drag the red arrow slightly

to the right until the X translation in the Inspector is between 0.1 and 0.15.


**Lesson 1 Creating a 3D Scene** **10**


Sometimes, objects might be outside the viewer’s display or obscured by other

elements, making onscreen controls difficult to use. Although you could use the

Inspector to change parameter values, it’s essential to understand how to move your

view of the 3D scene to get a complete picture of your elements’ positioning in 3D space.

**8** In viewer 1, hold the Command key (macOS) or Ctrl key (Windows) and scroll down with

your mouse wheel to zoom in your view, and then release the modifier key and drag in

the viewer until the lion is fully visible in the viewer.


**Lesson 1 Creating a 3D Scene** **11**


**9** Select the LION’s Image Plane 3D node and drag the green Y translation down until

the lion is overlapping the foreground element


Using your mouse buttons and keyboard modifier keys together, you can zoom in and

out, pan, and rotate around a scene. Don’t confuse this with a camera’s view. We’ll get

to that in just a bit. This is your view of the scene as if you are walking around it.

Although you could render this perspective view, it is primarily used to set up

your scene.

**10** As a simple example, hold down the middle mouse button and Option-drag (macOS)

or Alt-drag (Windows) left in viewer 1 until the sunset rotates in front of the animals

and then drag right until the sunset rotates back to its original position.


It’s important to remember that changing your viewing perspective by rotating your

viewpoint can change the layer order of your elements. That’s a very different way of

working than you may be familiar with in 2D compositing.


The following key and mouse button combinations are extremely useful when working

in a 3D viewer:


 - **Pan:** Drag while holding down the middle mouse button.

 - **Rotate:** While holding down the middle mouse button, Option-drag (macOS) or

Alt-drag (Windows).

 - **Zoom in and out:** Hold down Command (macOS) or Ctrl (Windows) and scroll the

middle mouse wheel.


Now, let’s return to a default starting point and continue building our 3D scene.


**Lesson 1 Creating a 3D Scene** **12**


**11** Right-click in viewer 1 and choose Settings > Load Defaults to return the perspective

view to the default angle.


TIP You can use the axis control in the lower right corner of viewer 1 to orient

your perspective view. When you move the Perspective view so that the green

Y line points up, the red X line points right, and the blue Z line points directly

toward you, the Perspective view is at a default front view in the 3D world.


Intuitively moving the Perspective view to different angles and moving objects in 3D space

are essential activities when compositing a 3D scene.


**Lesson 1 Creating a 3D Scene** **13**


## **Using 3D Text**

The standard 2D Text+ node cannot be connected to a Merge 3D composite; it only

connects to 2D composites. When working in a 3D composite, you must use a Text 3D

node to add text.


We’ll add some text to our scene. Although you can connect everything into a single Merge

3D, things can get tangled and unwieldy if you choose that path. We already have five

elements connected, so at this point, it might be wise to keep things more organized by

using multiple Merge 3D nodes. We’ll use a new Merge 3D to connect our 3D text. As with

standard 2D Merge tools, you can connect Merge 3D nodes together, creating a more

organized and flexible yet still singular 3D world.


NOTE Remember that the Timelines bin includes a Backups bin with Fusion comps

saved at various stages of the lesson, which are available for reference and

reverse-engineering the node trees.


**1** Select the Merge3D1 node in the Node Editor, and then from the toolbar, click the

Merge 3D button.


The new Merge3D2 is connected to the output of the Merge3D1. However, unlike

connecting 2D merge nodes, there is no layer order when connecting 3D merge

nodes—meaning that any element you add to the Merge3D2 node will still be placed in

the center of our 3D world, not in front of elements connected to the Merge3D1.


TIP The Merge 3D node contains 3D transform controls, so it is possible to

move or rotate all the elements connected to a single Merge 3D independently

of elements connected to a different Merge 3D.


**2** Select the Merge3D2 node and press 1 to see it in viewer 1.


**Lesson 1 Creating a 3D Scene** **14**


**3** From the toolbar, click the Text3D node to add it to the Node Editor, connected to the

Merge3D2 node.


**4** Select the Text3D node in the Node Editor and press 2 to see it in viewer 2.


You now have a 3D viewer with access to 3D text controls, but the Inspector shows

very similar controls to a standard 2D text node.

**5** With the Text3D node selected, go to the Inspector, and in the Styled Text field, type

**WILDLIFE CONSERVATION** using two lines of text.

**6** Click in viewer 2 and press F to fit the words into the viewer.


As with 2D text, you can assign a font, size, and other text properties to your 3D text.


**Lesson 1 Creating a 3D Scene** **15**


**7** Set the typeface to Open Sans Extra Bold and the Size to 0.03.


You also have your choice of 3D controls, position, rotation, extrusions, and bevels.

**8** In viewer 1, use the blue Z translation arrow to move the text slightly in front of the

Sunset graphic but not in front of the giraffe. This is a small adjustment of around 0.01

if you are looking at the Inspector Z translation value.


**9** Scroll to the bottom of the Inspector and click the disclosure arrow to open the

extrusion parameters.


These parameters can add depth to text and give titles a greater sense of weight and

substance.

**10** Set the Extrusion Depth to 0.1 and the Bevel Depth and Bevel Width to around 0.02.

**11** Since you decreased the text size, click in viewer 2 again and press F to fit the words

into the viewer.


The text is not lit and has no material assigned to it to improve its appearance, so the

results of your extrusion and bevel are not clearly visible. Let’s change these two

things next.


**Lesson 1 Creating a 3D Scene** **16**


##### **Applying Materials to Text3D**

In 3D animation applications, objects use illumination materials called _shaders_ to give

surfaces a more realistic appearance. You can easily build your own shaders using Fusion’s

Material nodes, but we’ll use one of Fusion’s shader templates for this

introductory exercise.

**1** Select the Text3D node in the Node Editor.

**2** Press Shift-Spacebar and type **replace** .


To apply materials to 3D text, you must add a Replace Material node where the new

materials will be connected.


TIP Fusion’s 3D shape nodes do not need the Replace Material node.


**3** Select the Replace Material 3D node and add it to the Node Editor after the

Text3D node.


**4** With the Replace Material 3D node selected, press 2 to view it in the viewer.

**5** In the Effects Library, choose Templates > Fusion >Shaders.


These are all the shader templates included with Fusion.

**6** Drag the Chrome template to an empty area of the Node Editor near the Replace

Material 3D node.


**Lesson 1 Creating a 3D Scene** **17**


**7** Drag the output of the Chrome template to the green Material input on the Replace

Material 3D.


TIP When added to the Node Editor, the Chrome node has a slightly different

appearance. This stacked node outline indicates that this is a Group node.

Groups are containers for other nodes. Since templates in Fusion are just

groups for all the individual nodes that make it up, you can open the template

to edit and modify the settings by right-clicking it and choosing Expand Group.


**8** In viewer 2, use Option (macOS)-middle mouse button or Alt (Windows) -middle mouse

button to change the Perspective view to different angles.


As you move the Perspective view, the text has a simple reflective chrome appearance with

a blue highlight. You can change some parameters in the Inspector, but these default

settings work well enough for our scene.


**Lesson 1 Creating a 3D Scene** **18**


## **Setting Up a Camera**

Looking at the scene from different angles using the perspective view is helpful for placing

your elements, but ultimately, you will want the scene framed using a camera. Adding a

camera gives you more control over how the scene is framed and allows you to animate

the view by moving the camera.

**1** Select the Merge3D2 node, press Shift-Spacebar, and add a Camera3D from the list.


We could have just as easily connected the camera to the Merge3D1 node, which

would not have made a visual difference to our composite, but to keep things more

organized, we chose to connect it here in the Merge3D2 with the 3D text.

**2** Select the Merge3D2 and press 2 to load it into viewer 2.


The Perspective view for the Merge3D2 is now displayed in both viewers, but we want

to display what the camera is seeing in one of the viewers. Your first thought might be

to select the camera and load it in a viewer. However, you need to continue viewing the

Merge 3D node and switch it from a perspective view to a camera view.


If you think about it, all the elements are connected to the Merge 3D, not the camera,

so it makes sense to view what the merge has connected through the eyes of

the camera.


**Lesson 1 Creating a 3D Scene** **19**


**3** In the lower left corner of viewer 2, right-click over the axis control and choose

Camera3D1 from the context menu.


TIP If you prefer to have the camera in viewer 1 and perspective in viewer 2, in

the lower left corner of viewer 2, right-click over the axis control and choose

Perspective from the list. Then, in the lower right corner of viewer 1, right-click

over the axis control and choose Camera3D1.


You might wonder why the camera view doesn’t display anything. Recall that we

mentioned that any object you add to the 3D scene gets placed at the center of the 3D

universe, which is X:0, Y:0, and Z:0. With the camera located at that position, it is

behind all the elements and facing away. You can see in the viewer 1 Perspective view

that the camera is at the center of the scene, and the focal plane outline is projecting

behind our scene.

**4** Select the Camera3D node in the Node Editor, and in viewer 1, drag the camera’s Z

position (blue arrow) down until you can clearly see all three animals are in the camera’s

view, but the bottom edge of the foreground element is not visible in viewer 2.


**Lesson 1 Creating a 3D Scene** **20**


It’s important to remember that if you move or rotate the view in the viewer with the

camera selected, you are changing the camera’s position. This can be a very simple

way to position or animate a camera, but it can also become a problem if you think you

are viewing the perspective view but accidentally move the camera.


NOTE In this guide, out of caution, we will always use the Inspector to move

the camera and only work in the viewer to move the Perspective view

if needed.


The Camera3D node contains familiar camera controls that you might want to adjust to

achieve the look you want.

**5** With the Camera3D node selected in the Inspector, change the focal length to **50** .


You now have a 50mm lens, which zooms in to our scene a bit more.

**6** Open the Control Visibility section and enable the Focal Plane checkbox.


Enabling the visibility of the Focal Plane displays a green rectangle in the viewer at a

specific distance from the camera where objects are in perfect focus. This only comes

into play when using depth of field (DoF) effects, which we will enable later in this

lesson, so it’s a good idea to enable it now and set the focal plane. To determine

the focal distance setting, you adjust the Focal Plane slider in the Inspector.


**Lesson 1 Creating a 3D Scene** **21**


**7** While viewing viewer 1’s Perspective view, drag the Focal Plane slider to the left until

the green rectangle is near the same location as the 3D text.


It’s very difficult to see how near or far you are from the text while in a Perspective

view. That’s why you can change the viewer from a Perspective view to common

orthographic views, including Front, Top, Left, and Right.

**8** In viewer 1, right-click over the axis control and choose Right from the pop-up menu.


Now, it will be easier to see the green line of the focal plane and the 3D text.

**9** In the Inspector, drag the Focal Plane slider until the green focal plane is directly over

the 3D text.


**10** Right-click the axis control in the lower right corner of viewer 1 and choose Perspective

to return the viewer to Perspective view.


It will be easier to view our scene if we quickly switch to single-viewer mode.


**Lesson 1 Creating a 3D Scene** **22**


**11** Above viewer 2, click the Single-Viewer Mode button.


Now that we have a better view, after scaling our animals and setting up our camera, it

appears that the animals are floating above the ground. We need to adjust our Y

position values to create a more realistic layout.

**12** Going through each Image Plane 3D, use the Y translation to position the elements

as follows:

**a)** Lion: Y **-0.04**

**b)** Foreground: Y **0.00** (no change)

**c)** Elephant: Y **-0.04**

**d)** Giraffe: Y **-0.01**


**13** Above viewer 2, click the Single-Viewer Mode button again to return to using

two viewers.


Again, as with the X position and scale adjustments you made earlier, the actual values

don’t really matter; the results should be a pleasantly laid-out scene.

##### **Animating a Camera Move**


For our animation, we’ll create a simple dolly-in move with the camera to focus more on

the sunset graphic and text.

**1** Move to the start of the render range in the Time ruler, if needed.

**2** Select the Camera3D1 node, and in the Inspector, click the Transform tab.

**3** In the Transform tab, click the Keyframe button to the right of the Z Translation parameter.


**Lesson 1 Creating a 3D Scene** **23**


**4** Move the Z translation back as far as possible without exposing the bottom line of the

FOREGROUND graphic. This will likely end up with a Z translation value of around 1.5.


This sets our starting keyframe. Now, we’ll set an ending keyframe and move the

camera forward a bit.

**5** Move to frame 80 in the Time ruler render range.


You can use the Inspector to move the camera or change its position directly in the

viewers using the translation arrows, as you have done previously.

**6** If needed, position the mouse cursor over viewer 1, hold the Command key (macOS) or

the Ctrl key (Windows), and scroll the middle mouse wheel until you can clearly see the

Camera’s blue Z translation arrow in the frame.


Like all objects in a 3D scene, the camera includes three arrows as translation controls

in the viewer. The green arrow moves the camera up and down on the Y axis, the red

arrow moves it side to side on the X axis, and the blue arrow moves the camera in and

out on the Z axis. Since we want to move the camera back a bit, we’ll drag the blue

arrow in viewer 1.


**Lesson 1 Creating a 3D Scene** **24**


TIP When a 3D object (including a camera or light) is selected, pressing W

while your mouse pointer is over a viewer will change the onscreen

translation controls for that object to rotation controls. Pressing Q will return

to translation controls. There are also buttons in the upper left corner of the

viewer to switch between translation and rotation.


**7** In viewer 1, drag the camera’s Z Translation blue arrow toward the sunset graphic until

the text fills the screen and the Inspector’s Z Translation is set around 0.55.


Moving the Z translation adds an ending keyframe for the animation.

**8** Play the comp to see the camera animation.


The animation stops suddenly at frame 80, but we’d like a softer “landing.” Just as you

can control acceleration for 2D animation, you can do the same for 3D objects.

**9** In the upper right of the Fusion interface, click the Spline button to open the

Spline Editor.

**10** To display the Camera’s Z animation curve, click the Camera3D1 Z Offset checkbox.


**Lesson 1 Creating a 3D Scene** **25**


**11** Click the keyframe at frame 80, and then in the lower right toolbar of the Spline editor,

click the Smooth button or press Shift-S.


**12** Close the Spline Editor and play the comp to see the smoother camera animation.


The result of the camera move is one of the greatest advantages of working in 3D. You can

achieve realistic parallax effects. As the camera moves closer, objects like the animals shift

perspective naturally, creating depth and a more lifelike sense of motion, even in an

obvious motion graphics scene like we have here.
## **Adding Lights**


3D scenes in the Fusion page can include lights used much like you would in the real world

to illuminate objects how you see fit. You can add as many lights as you need, use different

styles of lights, and control which objects each light illuminates.

**1** Select the Merge3D1 node.

**2** In the Effects Library, from the Tools > 3D category, select the Lights subcategory.


The Lights subcategory displays all four light types you can add to a 3D scene

in Fusion.


**Lesson 1 Creating a 3D Scene** **26**


**3** In the Light subcategory, click the Ambient Light tool to add it to the Node Editor,

connected to the Merge3D1 node.


The Ambient Light adds control for the overall brightness in our scene, but by default,

lighting is disabled in the viewers, so before we see any results and modify the

Ambient Light settings, we need to enable lights in both viewers.

**4** Above each viewer, enable lights by clicking the Lights and Shadows button.


**5** Select the Ambient Light node in the Node Editor and drag the Intensity slider

between 0.5 and 0.8 to brighten the scene.


**Lesson 1 Creating a 3D Scene** **27**


The ambient light provides overall lighting but hasn’t affected our 3D text. Unlike

cameras and image planes, lights don’t automatically pass through to other Merge 3D

nodes. By default, lights only affect the Merge 3D node they’re directly connected to

but not nodes that come after it in the chain (sometimes called _downstream_ ). To make

light affect nodes farther down the chain, you must enable the “Pass Through” option.

**6** Select the Merge3D1 node, and in the Inspector, click Pass Through Lights.


Now, our scene and text are both illuminated by the ambient light. Still, it might be nice

to highlight our text more with a spotlight.

**7** Select the Merge3D2 node, and in the Effects Library, click the Spot Light tool.


Unlike the ambient light, the spotlight is displayed in the viewer, so you can directly

adjust its position and rotation to point the light where you want it.


TIP Holding the Option key (macOS) or the Alt key (Windows) and clicking on a

connection line will add a router that allows connection lines to bend instead

of having diagonal lines overlap other nodes.


**8** In viewer 1, drag the Spot Light’s blue Z translation arrow to pull it away from the

Sunset graphic until it illuminates our text.


**Lesson 1 Creating a 3D Scene** **28**


To have the spotlight appear as if it is lighting our text from above, you can use a

combination of the Y translation and rotation.

**9** In viewer 1, drag the Spot Light’s green Y translation arrow to pull up until the light

shines just above the Wildlife text.


**10** In the upper left corner of viewer 1, click the Rotation button to switch the onscreen

controls to rotation wheels.


**Lesson 1 Creating a 3D Scene** **29**


**11** Drag the red X rotation wheel until the spotlight shines down on our text.


**12** Adjust the spotlight’s Intensity, Cone Angle, Penumbra Angle, and Dropoff to create a

softer, more localized spot on the text.


**Lesson 1 Creating a 3D Scene** **30**


Currently, our spotlight is illuminating both the background Sunset graphic and the

text equally. To make the spotlight illuminate only the text, we need to reorganize

our 3D scene. As we briefly covered earlier, lights affect all objects connected to a

Merge 3D node. If you have multiple Merge 3D nodes connected to each other, lights

will still affect objects earlier in the chain of nodes (also referred to as _upstream_ ), as if

everything were part of a single Merge3D. To restrict a light to only specific objects,

you must isolate those objects on their own separate Merge 3D node.

**13** Click the pipe between the Merge3D1 and the Merge3D2 to disconnect them.


**14** Click an empty area of the Node Editor near the MediaOut node.

**15** Press Shift-Spacebar and type **Merge** .

**16** Select Merge 3D from the list and add it to the Node Editor.

**17** Connect the Merge3D1 to the Merge3D3.


**18** Connect the Merge3D2 to the Merge3D3.

**19** Select the Merge3D3 and press 1 and 2 to display the merge in both viewers.


**Lesson 1 Creating a 3D Scene** **31**


Now, you should see the ambient light illuminate our entire scene because we’ve

enabled the Pass Through Lights checkbox in Merge3D1. However, the spotlight is only

applied to the text because Merge3D2 remains at the default setting without that

option enabled.


Your entire 3D scene is now lit using only two lights. With that in place, you can start

converting your 3D scene into a 2D image.


TIP One of the most common issues newcomers experience when working with

Fusion is an inability to see the effect of lighting in the 3D scene. First, a preview of

the lighting must be enabled for each viewer in order to preview the lighting

effects in the 3D environment. Second, lighting must be enabled in the

Renderer3D node (more on this in the next lesson). Finally, in a Merge 3D, Pass

Through Lights must be enabled to appropriately illuminate all desired objects

(more on this later in this lesson).


**Why Are There Different Light Types?**

The Fusion page includes four lights that you can add to a scene, each with its own

characteristics:


- **Ambient Light** illuminates an entire scene equally—similar to adding a gain

brightness—because it has no position or rotation. It is primarily used to fill

areas that other lights may leave too dark.

- **Directional Light** has a clear direction but lacks a specific source. You do not

control its position, but you can use rotation controls to indicate from where

in the scene the light appears to be coming. This light is akin to sunlight

because no matter how far away an object may be, there is no light fall-off.

- **Point Light** has a clear position in space that emits light in all directions;

therefore, only its position affects the light, not its rotation. A light bulb is a

good example of a point light. Unlike both ambient and directional lights, a

point light may fall off with distance.

- **Spot Light** comes from a specific point and has a clearly defined cone with

fall-off to the edges of that cone. This is the only light capable of

casting shadows.


**Lesson 1 Creating a 3D Scene** **32**


## **Converting 3D into a 2D Image**

Every 3D scene ends with a Renderer 3D node that converts the 3D environment into a 2D

image. Once you add the Renderer 3D node, additional 2D image processing can be

inserted, and you can render the output directly into the edit page timeline via the

MediaOut node. The Renderer 3D node is not just a conversion node from 3D to 2D; it also

includes several render processes that can enhance the look and quality of your comp.

The most significant of those is adding depth of field.

**1** In the Node Editor, select the Merge3D3 node, and from the toolbar, click the Renderer

3D tool to add it to the Node Editor.


TIP With smaller display resolutions, you might need to temporarily hide the

Inspector to see the Renderer 3D icon.


**2** Press 2 to see the Renderer 3D output in viewer 2.


**Lesson 1 Creating a 3D Scene** **33**


The Renderer 3D is set to render the camera by default, so you are all set there.

However, if you have multiple cameras in a scene, you can choose the camera

from a menu.

**3** In the Inspector, choose Camera3D1 from the Camera menu.


The Renderer 3D node includes two render engine options:


 - **The Software renderer** engine uses only the system’s CPU to produce the

rendered images. It is usually much slower than using your computer’s graphics

hardware but produces consistent results on all computers.

 - **The Hardware renderer** employs the GPU processor on the graphics card to

accelerate rendering. Using this method, the output might vary slightly from

system to system, depending on the graphic cards used. The increased speed of

the Hardware renderer makes it possible to customize supersampling and 3D

depth-of-field options. For these reasons, the Hardware renderer is most

commonly used.


**4** In the Renderer Type menu, choose Hardware Renderer.


You should see a difference between the Perspective view in viewer 1 and the

Renderer 3D output in viewer 2. Lighting is not initially enabled for the Renderer 3D

node as it is in the viewer. You’ll need to enable lighting to get the shading you see in

the Perspective view.

**5** In the Inspector, select the Enable Lighting checkbox to see the effects of your

directional and ambient lights.


**Lesson 1 Creating a 3D Scene** **34**


One last check is to ensure the Renderer 3D is set to output the correct resolution for

your shot. In this case, the project resolution is set to 1920 x 1080, so the Renderer 3D

should also be set to that.

**6** In the Inspector, click the Image tab and make sure the width and height values match

the project resolution of 1920 x 1080.


Your project looks nice but still a bit flat. You can remedy that by adding depth of field.

##### **Configuring Depth-of-Field Effects**


To give your project more photorealism, you can simulate a camera’s shallow depth of field

setting. _Depth of field_ (DoF) is the range before and after the focal plane that appears

acceptably sharp. Areas outside that range are increasingly out of focus.


The first step in setting up depth of field is to enable it in the Renderer 3D node. You’ll then

need to readjust the camera’s focal plane so it keeps focus even when the camera moves.

**1** In the Renderer 3D Inspector, click the Controls tab and enable both the Enable

Accumulation Effects and Depth of Field checkboxes.


The higher the quality, the better the depth of field will look, but the longer and harder

the computer will have to work to process the effect. The default amount of 32

samples is usually sufficient, but to speed up your previews in this lesson, we’ll

lower it a bit.

**2** Lower the quality to 16.


The amount of DoF blur changes the size of the in-focus area. The lower the number,

the more of the image remains in focus.


**Lesson 1 Creating a 3D Scene** **35**


**3** Decrease the amount of DoF blur to 0.005 and play through the animation to

preview it.


The scene is clearly blurred, but the focal plane should start with the lion in the front

and end on the text when the camera stops on frame 80. As with a real-world camera,

you need to change the focal point as the camera moves.

**4** When you’re finished previewing the animation, stop playback.

**5** Right-click the axis control label in viewer 1 and select the Top view.


**Lesson 1 Creating a 3D Scene** **36**


TIP If necessary, in viewer 1, hold down the Command (macOS) or Ctrl

(Windows) key and scroll the middle mouse wheel to frame the viewer so that

you can clearly see the text and camera.


The Top view will make it easier to focus the camera precisely on the lion and

then the text.

**6** Move to the start of the render range in the Time ruler.

**7** Select the Renderer3D and press 2 to make viewer 2 empty. This will speed up the

process of making adjustments since the viewer will not have to update the depth of

field with each change.

**8** In the Node Editor, select the Camera3D1 node, hold the Command key (macOS) or the

Ctrl key (Windows), and select the Lion’s Image Plane 3D node.


Selecting the Image Plane will help you see the onscreen controls in the viewer,

making it easier to align the focal plane to it.

**9** In the Inspector, adjust the Focal Plane slider until the green focal plane intersects with

the onscreen controls of the Lion in viewer 1.


Since the camera dollies in during the comp, everything will be out of focus again, so

you’ll need to keyframe the plane of focus.


**Lesson 1 Creating a 3D Scene** **37**


**10** Click the Keyframe button to the right of the Focal Plane slider.

**11** Move to frame 80 in the render range and adjust the Focal Plane slider again to be

directly over the text.


Now, you’ll need to view the Renderer3D again to see the actual results.

**12** In the Node Editor, select the Renderer3D and press 2 to see it in viewer2.

**13** Press the Spacebar to preview the now-in-focus animation.


TIP If you regularly want a node to appear with certain settings already

configured, you can right-click over the node in the Node Editor and choose

Settings > Save Default. Any time you add that node to a Node Editor, it will

come preset with the current configuration.


**14** Drag the output of the Renderer3D node to the MediaOut node.


After your Renderer3D node, your scene is a standard 2D image that can have filters

applied or continue with standard 2D composition of other elements. You can even create


**Lesson 1 Creating a 3D Scene** **38**


multiple 3D and 2D sections within a single composite, which makes complex compositing

much easier.


Completed node tree for Lesson 1

## **Lesson Review**

**1** True or False? A MediaIn node must go through a Shape 3D node or an Image Plane

3D node before it can connect to the Merge 3D node.

**2** True or False? The center of Fusion’s 3D scene uses the following coordinates: x = 0.5,

y = 0.5, z = 0.5.

**3** True or False? Lights must be added to a scene using their own Merge 3D node. They

cannot be connected to a Merge 3D node that already has objects connected.

**4** True or False? Depth of field is enabled in the Camera 3D node.

**5** True or False? The last node after any 3D compositing must be a Renderer 3D node.


**Lesson 1 Creating a 3D Scene** **39**


##### **Answers**

**1** True. A MediaIn node must go through a Shape 3D node or an Image Plane 3D node

before connecting to the Merge 3D node.

**2** False. The center of Fusion’s 3D scene uses the following coordinates: x = 0, y = 0, z = 0.

A 2D scene uses x = 0.5 and y = 0.5 as the center of the viewer.

**3** False. Lights, 3D objects, and cameras can all be connected to the same Merge

3D node, but separating them makes for better organization and flexibility.

**4** False. Depth of field is located in the Renderer 3D node.

**5** True. A Renderer 3D node is required at the end of any 3D compositing to convert the

3D scene to a 2D image.


**Lesson 1 Creating a 3D Scene** **40**


### Lesson 2
# Exploring a Green- Screen Workflow



In this lesson, you’ll take your

compositing skills to the next level

by combining keying with 2D and

3D techniques. Whether you need a

quick refresher on 2D compositing

or are ready to dive into more

advanced workflows, we’ll build on the

fundamentals and push into green
screen keying, masking, and seamless

integration techniques. You’ll use two

Delta Keyers to refine your key and

learn how to add realistic reflections

and light wraps to blend everything

more naturally.



Time

This lesson takes approximately
1 hour to complete.

Goals

Managing Color for Visual Effects 42

Removing Noise 48

Pulling a Key 51

Adding Natural Light Spill 67

Creating a 3D Windshield
Reflection 72

Lesson Review 83


By the end of this lesson, you will not only have sharpened your compositing skills, but you

will also have had a first look at how 2D and 3D can work together, unlocking new creative

possibilities in Fusion.


Completed composite for Lesson 2

## **Managing Color for Visual Effects**


Before you begin this next lesson, we must cover one of the more technical aspects of

post-production in general and visual effects compositing in particular. Color management

is a critical part of the entire post-production workflow, and the requirements for

compositing are slightly different than those for editing or color grading. You’ll start this

keying job by setting up a scene-referred color-managed workflow.


NOTE If you’re using the free version of DaVinci Resolve, you will receive a warning

when you restore the archive for this lesson. You can continue with the lesson;

however, some exercises require DaVinci Resolve Studio, so you will be advised to

skip those steps.


**1** Open DaVinci Resolve, right-click in the Project Manager, and choose Restore

Project Archive.

**2** Navigate to the DR20 Studio Fusion 3D Training Media folder.


This lesson will use the Fusion 20 Delta Keyer archive.


**Lesson 2 Exploring a Green-Screen Workflow** **42**


**3** Select the **Fusion20DeltaKeyer.dra** file and click Open to add the archived project to

the Project Manager.

**4** Open the Delta Keyer project from the Project Manager and select the edit page,

if necessary.

**5** From the main menu bar, choose Workspace > Reset UI Layout.

**6** In the timeline, move the playhead to the start and play through the clip.


When you first look at this green-screen shot from Action VFX’s practice content, you

might notice that it looks a bit flat, with low contrast and low saturation. That’s

completely normal! Most modern digital film cameras capture footage this way

to preserve more detail in highlights and shadows. The cameras compress brightness

(gamma) for efficient storage, and when expanded, they reveal a wider dynamic range

with more detail.


But here’s the catch: Fusion expects images to have a linear gamma—meaning

brightness levels behave in a more natural, mathematical way. If you skip this step and

start compositing immediately, things like color corrections, blending, and keying

might not work as expected.


So before pulling the key, we need to convert the footage to linear gamma so Fusion

can process it correctly. Then, after compositing, we’ll convert it back to match the

correct color space for our final output.


Sounds complicated? Don’t worry! DaVinci Resolve makes this easy with built-in DaVinci

YRGB color management. All you need to do is enable it, and Resolve will

handle the rest.


**Lesson 2 Exploring a Green-Screen Workflow** **43**


**7** Choose File > Project Settings, and in the sidebar, click the Color

Management category.

**8** In the “Color science” menu, choose DaVinci YRGB Color Managed.


When working with Camera Raw files in DaVinci Resolve’s color management (RCM),

the default state is to have the “Automatic color management” checkbox enabled. This

results in the metadata from each camera brand being used to process the raw files

into a standard format, ensuring that all the image details are preserved for color

grading and visual effects. Because RCM takes over this process, the setup is almost

completely automatic. When the “Automatic color management” checkbox is enabled,

Resolve simplifies things down to two simple menus.


The “Color processing mode” lets you choose between Standard Dynamic Range (SDR)

processing and High Dynamic Range (HDR) processing. Your choice depends greatly

on the majority of the media you are using. If most of your content is HD, then

choosing SDR would be appropriate. If most of your content comes from digital film

cameras in a LOG format, then HDR would be a better setting.

**9** Since our content is in LOG format and we want to preserve the dynamic range,

choose HDR for the “Color processing mode.”


An output color space menu configures the final rendered gamma and gamut output

for your delivery.

**10** Choose SDR sRGB from the “Output color space” menu.


**Lesson 2 Exploring a Green-Screen Workflow** **44**


TIP If you don’t have a calibrated HD display connected to your computer

when creating visual effects, it is more common to set the output color space

to sRGB to match your computer display.


If you want more control over these settings, turning off “Automatic color

management” displays several more detailed presets for both menu options. You can

also choose Custom from those menus for more complex color management setups.

**11** Click Save to close the window.


The clip in the timeline now appears with more saturation and more contrast.

However, much more has been done behind the scenes, especially in the Fusion page.

Let’s combine our two clips in the timeline into a Fusion Composition and then enter

the Fusion page.

**12** Select both clips in the timeline, and then right-click over them and choose New

Fusion Clip.


TIP Fusion clips are limited to the timeline resolution. If your source

material is larger than the timeline resolution, you are better off entering

Fusion with just one clip and then importing additional clips into Fusion

using the media pool.


**Lesson 2 Exploring a Green-Screen Workflow** **45**


**13** Position the playhead over the Fusion clip and press Shift-5 to enter the Fusion page.


Turning on Color Management performed several processing steps automatically for

Fusion. First, it converted the MediaIn nodes to linear gamma. Second, it enabled a

LUT (lookup table) in the viewer, so you are not looking at the linear image. Images

using linear gamma are rather dark and highly saturated and therefore unpleasant to

work with. The viewer LUT makes for a more natural viewing experience while still

allowing you to composite correctly using linear gamma images.

**14** In the upper right corner of viewer 2, click the LUT button to disable it, revealing the

linear image.


A viewer LUT is a simple color adjustment applied to the viewers in the Fusion page.

The image itself is not changed, only its display in the Fusion viewers. Rather than

showing the image with linear gamma, Resolve enables the viewer LUT to convert the

linear gamma image to the output color space identified in the color

management setting.

**15** Click the LUT button again to re-enable it and thus view the corrected image.


TIP If you choose not to use Resolve color management, you can add a gamut

or Cineon Log node after every MediaIn node to convert it to linear gamma.

Then, add a gamut or Cineon Log node just before the MediaOut to convert

back to the final output gamma setting.


You are now able to composite using images that look correct and, more importantly, will

act correctly during compositing. When you switch to the edit or color pages, all the

gamma curve corrections are managed automatically based on the output color space

setting that you configured in the Color Management Project Settings.


**Lesson 2 Exploring a Green-Screen Workflow** **46**


**Lesson 2 Exploring a Green-Screen Workflow** **47**


You can see this in action when applying the same color correction to two versions

of an image—one with a LOG gamma (below left) and one properly converted to

linear (below right). As we double the exposure of each image and then double

again, the LOG version boosts midtones disproportionately, highlights are milky,

and shadows appear muddy. The highlights on the linear image remain smooth,

and shadows transition more evenly.


So what’s the solution? Convert your footage to linear gamma before

compositing. The easiest way to do this is by using a color-managed workflow,

like DaVinci YRGB Color Management or ACES. This ensures Fusion handles

everything correctly, and once you’re done, it will convert the image back to the

proper display gamma for your final output.


By working in linear color space, your keys, effects, and blends will behave

naturally, giving you better, more accurate results.

## **Removing Noise**


We will begin our keying process with noise reduction. Noise makes keying harder by

creating tiny color variations that confuse the keyer, leading to choppy edges, flickering,

and unwanted artifacts. Since extracting a matte for keying is based on clean color

separation, a noisy image makes it difficult to pull a clean key and make adjustments.

By removing noise first, you give the keyer a smooth, even image to work with—leading to

cleaner edges and better transparency.

**1** In the Node Editor, select the MediaIn2 node and rename it **GreenScreen** .


TIP When you first enter Fusion using a Fusion clip with multiple layers, you

may want to organize your nodes into a neater layout rather than the default,

which overlaps some of the nodes.


**Lesson 2 Exploring a Green-Screen Workflow** **48**


**2** Press 1 to view the GreenScreen node in viewer 1, and then click in the viewer and

press R to view the red channel.


In most digital camera sensors, green is usually the cleanest channel because the sensor’s

pattern captures twice as many green pixels as red or blue. The blue channel typically

has the weakest signal, but because we have converted this clip from a RAW file into

ProRes4444 for training purposes, the noise gets a little more redistributed across the

channels, as you can clearly see on the back seats as we view the red channel.

**3** In viewer 1, zoom in to an area where you can see the right side of the driver’s hair.


**Lesson 2 Exploring a Green-Screen Workflow** **49**


Fusion includes a Noise Reduction node that uses the same temporal, spatial, and

AI-based processes found in the Color page. We’ll pay particular attention to the

strands of hair that we don’t want to lose as we apply the noise reduction.


NOTE The Noise Reduction node is only available in DaVinci Resolve Studio.

If you are using the free version of DaVinci Resolve, skip the noise reduction

steps and continue with the next exercise, “Pulling a Key.”


**4** Press Shift-Spacebar and type **Noise** to add a Noise Reduction node after the

GreenScreen node.

**5** Select the Noise Reduction node and press 1 to view it.


The Noise Reduction node in Fusion offers temporal and spatial noise

reduction. Temporal noise reduction analyzes multiple frames to reduce flickering

noise while keeping motion details intact. Spatial noise reduction works within a single

frame to smooth noise without blurring edges. UltraNR, found in the Spatial NR menu,

is an AI-driven hybrid that applies smart temporal and spatial noise reduction before

other NR settings, preserving details more effectively.

**6** In the Inspector, from the Spatial NR menu, choose AI UltraNR.


**7** Click Analyze.


The analysis takes a second or two, and the process is completed. A small square patch

appears over the area that was used to evaluate the noise. Viewer 1 shows the

cleaned-up red channel and the retained strands of hair. If you want to improve it

further, you can increase the Temporal threshold a small amount because the greater

you increase this value, the slower the process becomes and the more potential there

is to lose detail.


**Lesson 2 Exploring a Green-Screen Workflow** **50**


**8** Increase the temporal threshold to 1.0.


To better see how much cleaner the image has become and how much of the detail

has been retained, you can easily disable the node to compare the image before

and after.

**9** With the Noise Reduction node selected, press Command-P (macOS) or Ctrl-P

(Windows) to disable it and then press the same keyboard command to enable it again.

**10** Click in viewer 1 and press C to view the three color channels again, and then press

Command-F (macOS) or Ctrl-F (Windows) to fit the image into the viewer.


TIP Having noise reduction recalculated for every frame can slow down

playback and compositing performance. Use a Saver node directly after the

Noise Reduction node to render out the clean frames as EXR, and then import

them into Fusion using a Loader node. This speeds up your workflow,

ensures smoother playback, and frees up GPU resources for other

compositing tasks.


This noise reduction did a great job using DaVinci’s Neural Engine. However, noise

reduction can also smooth out fine details, making edges too soft and reducing the

accuracy of keying, tracking, and blending. Over-aggressive noise reduction can also

create motion artifacts or remove natural film grain, making CGI elements look unnatural

when integrated. Since noise is part of the original image texture, ultimately, you

should add controlled grain back after compositing for a seamless look. We’ll leave that

part to another book in this series, _The Colorist Guide to DaVinci Resolve 20_ .
## **Pulling a Key**


With the color management correctly set up and noise reduction applied, you can begin

the actual keying process. As you more than likely know, compositing shots usually

requires a matte: a grayscale image that identifies parts of the foreground as transparent

and other parts as opaque. Unlike computer-generated images, this live-action green
screen shot does not include an alpha channel. So it is up to you to create the matte

through keying. This is often termed “pulling a key.” The Delta Keyer is the primary tool

used for green-screen and blue-screen keying in the Fusion page. We’ll start by adding one

connected to the Noise Reduction node.


**Lesson 2 Exploring a Green-Screen Workflow** **51**


**1** Press Shift-Spacebar and type **Delta** to add a Delta Keyer to the Noise Reduction node.


TIP Whenever you are keying, it is helpful to use two viewers: one where you

can see the final output, and the other where you can view the quality of

your matte.


**2** Press 1 to view the Delta Keyer in viewer 1.

**3** From the Delta Keyer’s Inspector, drag the Eyedropper into viewer 2 and select the

green color in the upper right corner. This area avoids reflections in the side window

and the defroster grid lines on the back window.


**Lesson 2 Exploring a Green-Screen Workflow** **52**


**4** To view the alpha channel or the matte created by the Delta Keyer in Viewer 1, click in

the viewer and press A.


With this selection, you are not looking to create a perfect key; you are only looking to

retain any fine detail edges.

**5** Move to the end of the render range in the time ruler, where the passenger turns his head,

and then hover your mouse pointer over viewer 1 and hold the Command key (macOS)

or Ctrl key (Windows) as you scroll the middle mouse to zoom in to the passenger’s hair.


**Lesson 2 Exploring a Green-Screen Workflow** **53**


The viewer shows what is probably the finest detailed area in the matte, the

passenger’s hair clearly overlapping with the green screen. We are also looking to

preserve the reflections in the driver’s side window.

**6** Drag the frame in viewer 1 to see the driver’s side window and the reflections that

have been retained.


Without any adjustments from you, the Delta Keyer has done a great job of keeping

the detailed edges in his hair and the subtle reflections in the window. Let’s name this

node so it is clear what the Delta Keyer is helping us do in this shot.

**7** Select the Delta Keyer, press F2, and rename it **Delta_Edge** .


This single Delta Keyer hasn’t done a great job of making the inside of the car pure

white. There are many shades of gray there, which means there is semitransparency

that needs to be removed.

##### **Using a Second Delta Keyer**


A common challenge in keying is expecting a single keyer to handle everything. However,

complex shots benefit from a multi-key approach—using an edge matte as we have

here for fine details like hair and what is often called a “core matte” for solid areas. This

technique will give you greater control, preventing the loss of detail and ultimately leading

to a more seamless composite. You can create solid-core mattes by rotoscoping polylines

or even the paint node, but you can also use another Delta Keyer.


**Lesson 2 Exploring a Green-Screen Workflow** **54**


NOTE In this exercise, we won’t provide exact values for every parameter. Keying

is an iterative process—adjustments made in one area often require you to revisit

and refine earlier settings. As you progress, don’t hesitate to return to any

parameter and tweak it based on how later steps affect the overall result. Effective

compositing is rarely linear—refinement is part of the workflow.


**1** Click in an empty next to the Delta_Edge node and add a second Delta Keyer.

**2** Select the second Delta Keyer and rename it **Delta_Core** .

**3** Drag a second output from the Noise Reduction node to the Delta Core node.


**4** Press 1 and 2 to view the Delta_Core node in both viewers.


The tabs at the top of the Inspector roughly outline the flow for working with the Delta

Keyer. You begin in the Key tab and then move through the tabs to the right. You might

skip some tabs, and you might use some occasionally. Every keying job is different, and

although we can provide a guideline here, it is by no means the only way to key.

**5** From the Inspector’s Key tab, drag the Eyedropper into viewer 2 and select a green

color from the upper right area again.


This time, we don’t care about retaining the fine details along the edges or the

reflections in the window because we have a keyer doing that. We need this keyer to

focus on filling in all the gray semitransparent areas in our matte that should be pure

white (non-transparent)

**6** Click in viewer 1 and press Command-F (macOS) or Ctrl-F (Windows) to fit the image

in the viewer.


**Lesson 2 Exploring a Green-Screen Workflow** **55**


Typically, people will instantly try to refine the matte. While that isn’t a terrible idea,

there is a large area at the bottom half of the shot that can be handled immediately

just by using a rectangular shape as a solid matte.

**7** Move to frame 100, where the driver’s hand has very little overlap with the side window.

**8** Drag a Polyline shape from the toolbar to the node graph near the Delta_Core node.

**9** Draw a very simple rectangular shape over the lower half of the screen, including the

driver’s hand, and then down across the side windowsill.


**10** Drag the output of the polyline to the bright white Solid input on the Delta_Core node.


This rectangular solid matte eliminates the need for the keyer to worry about all the

gray semitransparent area that it is covering. We can now begin refining the areas

that remain.

**11** Select the Delta_Core node.


Modern keyers are called difference keyers, as opposed to chrome keyers, because

they use a color difference method of removing the green or blue screen rather than

just a straight chroma sampling. This matters because it helps us understand that the

Delta Keyer doesn’t just sample green pixels and remove them; it compares green

pixels against red and blue. It calculates transparency based on how much stronger

the key color is compared to the other channels. Using the Gain and Balance sliders,

you can increase the key color (gain) and the influence that blue and red have on the

transparency (balance). The downside is that adjusting these two parameters too far

will often ruin your edges. You’ll see that most adjustments in the Delta Keyer are

balancing acts between maximizing the adjustment and ruining your matte.


**Lesson 2 Exploring a Green-Screen Workflow** **56**


**12** Increase the Gain slider above a quarter of the way to the right and then drag the

Balance slider slowly to the right until more of the driver’s face becomes solid white.

**13** In the Inspector, select the Matte tab and adjust the high threshold about two-thirds

of the way to the left and then increase the low threshold until it almost meets the

high threshold.


The Threshold parameters are the primary way to control the transition between fully

transparent and fully opaque areas in the alpha channel. You’ve narrowed the range,

therefore making more of the alpha channel pure black and pure white. This works well

for the inside of our matte, but by doing this you also affect the fine edges. The Erode/

Dilate parameter can shrink the matte, essentially pulling it away from the edges.

**14** Decrease the Erode/Dilate parameter slightly and increase Blur to slightly.

**15** For the lingering small dots of gray or black in the white area of our matte, increase the

Clean Foreground a small amount until the dots are gone (try not to exceed 0.0015).

**16** Drag the output of the Delta_Core node to the bright white Solid input on the Delta_

Edge node.

**17** Select the Delta_Edge node and press 1 and 2 to see it in both viewers.


Keying is often a game of Whac-a-Mole. You fix one thing with a Delta Keyer and find

that you need to fix something else with a polyline mask. Sometimes, one or even two

keying nodes aren’t enough. Don’t be afraid of using multiple tools to find the right

mix needed for any given shot.

##### **Tuning a Third Delta Keyer**


There is still one area to the right of the driver’s head where a small amount of green has

not been removed. We could endlessly try to tweak the tool in the other two Delta Keyers

to correct this, but we run the risk of destroying our otherwise nice composite. It is very

common to use multiple keyers to key different areas. A key rule in keying is: Do not try to

make a single keyer do all the work.


**Lesson 2 Exploring a Green-Screen Workflow** **57**


**1** Click in an empty area near the Delta_Edge node and add a third Delta Keyer.

**2** Select the third Delta Keyer and rename it **Delta_Window** .


**3** Drag a third output from the Noise Reduction node to the Delta_Window node.

**4** Press 1 and 2 to view the Delta_Window node in both viewers.

**5** From the Inspector, drag the Eyedropper into viewer 2 and select a green color on the

small back window to the right of the driver’s head.


**6** Increase the Gain slightly but leave the Balance alone to retain the wisps of yellow hair.

**7** To make our matte denser, select the Matte tab and drag the low threshold up a tiny

bit and the high threshold down about 20%.


**Lesson 2 Exploring a Green-Screen Workflow** **58**


Because we are only interested in working on the small window to the right of the

driver’s head, we’ll use a mask to restrict this key to that area.

**8** Click the Rectangle mask in the toolbar, adding it to the Mask input on the Delta_

Window node.


**9** Size and rotate the rectangular shape so it covers the window shape as tightly

as possible.


**Lesson 2 Exploring a Green-Screen Workflow** **59**


You can see that this hasn’t created a perfect matte for our hair and window. As with

color correction, sometimes keying calls for more precise tools than just selecting a

color and adjusting a few matte controls.


The area of hair that is most transparent are the highlights, but the parameters we

have been adjusting are affecting the entire image. As with color correction,

occasionally you need to adjust just the shadows, midtones, or highlights. That’s

exactly what the Tuning tab is for.

**10** Select the Delta_Window node, and in the Inspector, select the Tuning tab.


The graph of the Tuning tab shows how much color falls into the shadows, midtones,

and highlights areas of the image. Adjusting the spline allows you to finely control the

tonal ranges. Adjusting the Shadows, Midtones, and Highlights sliders allows you to

modify the strength of the matte for any of the regions.


**Lesson 2 Exploring a Green-Screen Workflow** **60**


**11** Adjust both viewers so you are zoomed in to the side of the driver’s head where you

are keying.


**12** Set the Midtones slider to 0.6 and the Shadows slider to 0.9.


This should give you a very good matte for that window and the wispy hair. Feel free to

experiment with the ranges to see if you can improve upon these simple adjustments.

You can always click the Smooth button to return the ranges to the default locations.

We’ll now combine this Delta_Window matte with the Delta_Edge matte.


TIP When the composite is complete, return to this Delta_Window node and

experiment with adjusting the Erode/Dilate and Restore Fringe sliders by very

small amounts to see if you can improve the wisps of hair even more.


**13** Select the Delta_Edge node and add a Matte Control node.


**Lesson 2 Exploring a Green-Screen Workflow** **61**


**14** Drag the output from the Delta_Window node to the green foreground input on the

Matte Control.

**15** Reset your viewer to see the entire image and then press 1 and 2 to view the Matte

Control node in both viewers.

**16** In the Inspector, choose Combine Alpha from the Combine menu, and then set the

Combine Op to Minimum.


The Minimum setting performs a Boolean operation where only the darkest areas of

both the Delta_Edge (previously combined with the Delta_Core) and the Delta_Window

mattes overlap. This gives us the perfect combination of both the Delta_Window keyer

and the Delta_Edge keyer.


You’ve now created a beautiful matte using three Delta Keyers in different ways. This is

not uncommon at all. In fact, you are making it much too difficult on yourself if you are

trying to use just one keyer node to get a clean composite.

##### **Handling Spill Suppression Separately**


The Delta Keyer in Fusion is primarily used to create a matte to remove the green screen,

but it also has controls to suppress the light from the green screen bouncing onto the

actors. This is commonly called “spill” when keying. While the Delta Keyer can handle both

the matte creation and the spill suppression, it’s best practice to let the keyer focus on

what it does best—pulling a clean matte—and handle spill suppression separately in

another branch of your node graph. This gives you more control over fine color

adjustments without affecting the overall key.

**1** To see how much spill suppression the Delta Keyer is actually doing, select the Delta_

Edge node.


**Lesson 2 Exploring a Green-Screen Workflow** **62**


**2** In the Mask tab, set the Solid Replace Mode to Source.


Setting the Replace Mode to Source disables any spill suppression being performed in

the Delta Keyer and instead uses the original colors from the source clip. You can now

use Fusion’s color correction tools to remove the spill with much greater control.

**3** Click to the right of the Delta Keyers in an empty area of the Node Editor.

**4** Press Shift-Spacebar and type **Hue** to add a Hue Curve node to the Node Editor.

**5** Drag an output from the GreenScreen node to the Hue Curves node.


The Noise Reduction helped us to pull them and create a clean matte, but it’s not

needed for the color correction we are about to perform. You want the image to match

the background noise and all. Not adding back the noise could also make the image

appear too clean.

**6** Select the Hue Curves node and press 2 to view it in the right viewer.


In the Inspector, the three checkboxes along the top are similar to the color page’s

Custom Curves options. They allow you to adjust the Hue, Saturation, or Luminance of

a specific color (hue) by dragging the control point under the hue you want to adjust.

In our case, we want to adjust the saturation of the green hue.


**Lesson 2 Exploring a Green-Screen Workflow** **63**


**7** Make sure Sat is the only enabled checkbox.

**8** Locate the control point under the green hue on the color bar and drag it down

two-thirds of the way to the bottom to decrease the green hue.


Because decreasing the green saturation can tangentially decrease the yellow in the

driver’s hair, you’ll need to offset that by increasing the specific yellow of the hair.

**9** At the bottom of the Inspector, drag the Eyedropper into the viewer and release it over

the bright yellow of the driver’s hair.


A new control point is added to the Saturation curve that corresponds exactly to the

yellow hair.


**Lesson 2 Exploring a Green-Screen Workflow** **64**


**10** Locate the control point under the yellow hue on the color bar and drag it up until the

yellow of the driver’s hair is restored.


The best way to evaluate all these masks and adjustments is to combine them so you

can see the composite. First, we’ll combine our Delta Keyer matte with our hue curve

spill suppression to create a foreground with an alpha channel. We can do that with a

Matte Control node.

**11** Select the Hue curves node, press Shift-Spacebar, and add a second Matte

Control node.

**12** Drag the output of the Matte Control1 node currently connected to the Merge2 node

and connect it into the green foreground input of the Matte Control2.


**13** Select the Matte Control2 and press 1 and 2 to see the Matte Control in both viewers.


Now, you can just copy the mask from the foreground to the background.


**Lesson 2 Exploring a Green-Screen Workflow** **65**


**14** In the Inspector, choose Combine Alpha from the Combine menu.


You will now use this as the foreground input to a Merge node to place over the

background. As you might recall from earlier Fusion training, Merge nodes expect

alpha channels to be pre-multiplied with their RGB image.

**15** In the Inspector, enable Post Multiply Image.


**16** Drag the Output of the Matte Control2 to the Merge2 node’s foreground input.


**17** Select the Merge2 node and press 2 to see it in the viewer.


You’ve created a strong composite, but the work isn’t done yet. Keying and spill

suppression are just the first steps in making a shot feel real. Now, it’s time to focus on the

subtle environmental cues that seamlessly blend your foreground with the background,

making the composite truly believable.


**Lesson 2 Exploring a Green-Screen Workflow** **66**


## **Adding Natural Light Spill**

When placing a subject into a new environment, one of the biggest giveaways of a

composite is a harsh, unrealistic edge where the foreground meets the background. In real

life, light doesn’t stop at the edge of an object—it naturally spills and wraps around surfaces

due to diffusion and reflection. This is where a light wrap technique comes in. By softly

blending the background’s light around the edges of the foreground, a light wrap helps

eliminate the cut-out look, making the subject appear more naturally embedded in the

scene. Without it, even a perfectly pulled key can feel disconnected from its environment.

**1** Click in an empty area of the Node Editor to the right of the Hue Curves.

**2** Press Shift-Spacebar and enter **difference** to locate and add a Difference Keyer.


There are many ways to begin creating a light wrap. For this exercise, we’ll choose a

Difference Key. We’ll use the Difference Keyer to create the matte that shows where

the green bounce spill was in the shot, and then we’ll “replace” that green spill with

color from our background image. To do this, we set the Difference Key so the original

image can be compared to the Hue Curves version, where the green spill has been

removed. The controls in the Inspector will help decide how much of that green is

retained and how much is not included in our light wrap.

**3** Drag a second output of the Hue Curves to the Difference Keyer’s yellow

background input.


**Lesson 2 Exploring a Green-Screen Workflow** **67**


**4** Drag another output from the GreenScreen clip to the green foreground input of the

Difference Keyer.


**5** Select the Difference Keyer and press 1 to see the matte in the viewer.


The matte created by the Difference Keyer is based on the change in the green hue.

The main way to control how much those differences affect the matte is via the

threshold sliders in the Inspector. The Low threshold sets the minimum

difference needed for a pixel to be considered part of the matte (transparent). Raising

the Low threshold will make more similar pixels transparent (included in the light

wrap), which isn’t what we want. So we’ll keep it at its default setting.


Lowering the High threshold makes differences more transparent, which is exactly

what we need. The default is already set very low for the High threshold, so we may

actually want to make a few of those pixels more opaque.


**Lesson 2 Exploring a Green-Screen Workflow** **68**


**6** Increase the High threshold slightly to create a good balance between soft edges and

a more semitransparent, less detailed matte.


Once we have this matte, we’ll blur it so the light wrap blends smoothly around the

edges of our subject, making the composite look more natural.

**7** Increase the Blur.


This is now the mask we will use to create spill onto our actors in the car.

**8** Click in an empty area of the node graph under the Difference Keyer.


**Lesson 2 Exploring a Green-Screen Workflow** **69**


**9** Press Shift-Spacebar to add a Merge node and press 1 to see it in the viewer.


**10** Click in viewer 1 and press A again to change from viewing the alpha channel to

viewing the RGB image.

**11** Disconnect the output of the Hue Curves from the Matte Control2 and drag it into the

yellow background input of the Merge3.


**12** Drag the output of the Difference Keyer node to the blue mask input of the Merge3.


You now need a foreground, which, in our case, is the road clip since that is where the

natural spill should be coming from. However, connecting the road clip directly would

be harsh, and spill light isn’t harsh, so we need to blur it prior to connecting it to the

Merge3 node.


**Lesson 2 Exploring a Green-Screen Workflow** **70**


**13** Click somewhere near the Merge1 node, and from the toolbar, click the Blur node.


**14** Drag a second output of the Merge1 node to the Blur node.


**15** Drag the output of the Blur node to the green foreground input of the Merge3.


**16** Select the Blur1 node and increase the blur size by 20%.


The final part will be to combine the Merge3 with our clean Delta Keyer foreground

and then onto the Merge2 node for our (almost) completed composite.


**Lesson 2 Exploring a Green-Screen Workflow** **71**


**17** Drag the output of the Merge3 node to the yellow background input of the Matte

Control2 node.


You now have a very convincing composite of our actors driving along a road. In some

cases, you could send this off to the color page and grade it. However, sometimes you’ll be

asked to make it even more realistic by adding the road reflection on a front windshield.

Occasionally, this can be distracting (as in our case), but we will learn how to do it anyway.
## **Creating a 3D Windshield Reflection**


Now that we’ve refined our key, it’s time to add a realistic reflection to the car’s windshield.

To achieve this, we’ll use Fusion’s 3D environment, combining a reversed clip of our road

with a Camera3D and a Shape3D to create a reflected windshield surface. This setup allows

you to expand your newfound knowledge of Fusion’s 3D tools without going too deep

too quickly.

**1** Select the Merge2 node and add a Merge4 node directly after it.


This merge will be used to composite the windshield reflection over the top of our

existing composite. We will build the windshield reflection in 3D and integrate the 3D

composite into our 2D composite.


**Lesson 2 Exploring a Green-Screen Workflow** **72**


**2** Select Merge4 and press 2 to see it in the viewer on the right.

**3** Click in an empty place above the Merge4 and then add a Merge 3D node.

**4** After the Merge3D node, add a Renderer 3D, and then connect it to the Merge4 node’s

green foreground input.


This is a basic setup when combining a 3D scene into a 2D composite. Whatever you

build in your 3D scene, represented here by the Merge3D node, gets rendered into 2D

using the Renderer3D node. For our 3D scene, we’ll use a 3D shape to roughly match a

curved windshield shape.

**5** Select the Renderer3D and set the Render Type to Hardware Renderer.

**6** Select the Merge3D and press 1 to see it in the viewer.

**7** Press Shift-Spacebar and add a Shape3D to the node graph.


**Lesson 2 Exploring a Green-Screen Workflow** **73**


The Shape3D node can be used to create several 3D primitive shapes, such as spheres,

cubes, and cylinders. It starts as a simple plane, similar to the image plane you used in

the previous lesson. We will change that shape to a sphere and then modify the sphere

to look more like a windshield.

**8** In the Inspector, choose Sphere from the Shape menu.


Our 3D scene has no lights, so our sphere appears very flat. However, we can enable

lights in the viewer to get a sense of the sphere’s size and roundness.

**9** Select the Renderer3D node, and in the Inspector, click the Enable Lighting checkbox.

Then, above viewer 1, click the Shading button to enable default lighting and shading.


To simulate a windshield, we don’t need a complete sphere; we need a cropped section

of a sphere. The Angle and Latitude parameters can be used to crop the horizontal

(angle) and vertical (latitude) coverage of the sphere shape.

**10** Select the Shape3D node, and in the Inspector, drag the Angle Start to around 50 and

the End parameters to around 100.


The result is a half sphere, or hemisphere. We’ll use the latitude to limit the hemisphere

so it doesn’t have caps on the top and bottom, making it more like a windshield.


**Lesson 2 Exploring a Green-Screen Workflow** **74**


**11** Drag the Latitude End to -20 and the Start to 20.


The actual numbers we use will change when we composite this over our live-action

composite so that we fit the actual windshield in the clip perfectly. For now, we’ll use

these values.

##### **Auto Stabilizing in the Edit Page**


To create a realistic windshield reflection, we need to stabilize the road clip to remove any

unwanted camera shaking from affecting the reflection. Since it’s a long shot with

continuous motion, point and planar tracking methods in Fusion aren’t ideal. Instead, we

can take advantage of DaVinci Resolve’s Auto Stabilize in the edit page.

**1** Switch to the edit page.


**Lesson 2 Exploring a Green-Screen Workflow** **75**


**2** Right-click over the Fusion clip in the timeline and choose Open in Timeline.


Now that we have access to the two clips that make up our composite, we can edit a

copy of the road, stabilize it, and reverse it.

**3** Select the road clip on video track 1 and press the F key to match frame the clip to the

source viewer.

**4** Double-click the Path control in the lower left corner of the timeline to return to the

main timeline.


**5** Move the playhead farther down to an empty location in the timeline.

**6** Press F10 or click the Overwrite edit button in the toolbar.


**Lesson 2 Exploring a Green-Screen Workflow** **76**


**7** Right-click over the newly edited clip and choose Change Clip Speed.

**8** Click Reverse Speed and then click the Change button to close the window.


**9** In the Inspector, open the Stabilize parameters, increase Smooth to 1.0, and then

click Stabilize.


The stabilization takes a few seconds to analyze, and the result is a smooth, reversed

clip of driving down the road. But the trick is getting this into the Fusion page so we

can use it as a MediaIn node.

**10** Right-click over the clip again, and this time choose Render in Place.


Render in Place is typically used to render and bake in all effects that are applied to a

single clip on the edit page timeline for performance reasons. However, a side benefit

is that it also places that rendered clip in the media pool so we can access it in Fusion.


**Lesson 2 Exploring a Green-Screen Workflow** **77**


**11** In the Render in Place window, enter the clip name as **Stabilized Road** .

**12** Select either ProRes 422HQ or DNxHR HQ.


Either of these codecs is reasonable enough quality to work for our reflection.

**13** Click the Render button and select a location for the media file. Be sure to make it easy

to find so you can delete it quickly after finishing this lesson.


Once the rendering is complete, you’ll see the Stabilized Road clip in the

currently selected media pool bin. Now we can return to Fusion and use it in

our windshield reflection.

**14** Move the playhead over the Fusion clip and switch to the Fusion page.

**15** Open the media pool and drag the Stabilized Road clip you created to the Node Editor

near the Merge3D node.


You could map the Stabilized Road video directly onto the Shape3D, but using

3D projection mapping will create a more realistic windshield reflection.

##### **Projection Mapping**


3D projection mapping works like a real-world projector, making the reflection naturally

warp and bend with the glass. In Fusion, you can use either a Projector3D or a Camera3D

node for projection. While Projector3D offers more control, Camera3D is simpler to set up.

For our first introduction to projection mapping, we’ll take the easy route.


**Lesson 2 Exploring a Green-Screen Workflow** **78**


**1** Select the Merge3D node and add a Camera3D node to it.


**2** Drag the output of the MediaIn2 node to the Camera3D node’s pink image input.

**3** Select the Camera3D node, and in the Inspector, switch to the Image tab and disable

Enable Image Plane.

**4** Switch to the Projection tab and then click the checkbox to Enable Camera Projection.


**Lesson 2 Exploring a Green-Screen Workflow** **79**


The camera isn’t positioned in front of the Shape3D, so the shape will turn black since

we essentially have the “projector” behind the screen facing away.

**5** In the Inspector’s transform tab, drag the Z Translation parameter to the right until the

Shape3D is completely covered with the Stabilized Road clip in viewer 1.


At this point, we need to return to the Shape3D and make sure it covers the area where

the windshield would be in the live-action shot.

**6** Select the Shape3D node in the Node Editor.

**7** Increase the angle parameters so the reflection covers the live-action windshield area

displayed in viewer2, roughly 30-150.


**Lesson 2 Exploring a Green-Screen Workflow** **80**


**8** Change the End latitude to around -10 and the Start latitude to 25 so the height of the

reflection covers the top and bottom of the live-action windshield area.


You now should have a projection that covers a bit more than the area of the

windshield. So the final few steps in this comp will be to add a simple mask to shape

the projection to the windshield area and do some final blending. Luckily for you, we’ve

created this simple mask to save you some time.

**9** In the media pool Masks bin, drag the Windshield_roto clip into the Node Editor near

the Merge4 node.

**10** Drag the output of the Windshield Roto to the blue effect mask input on the

Merge4 node.


**Lesson 2 Exploring a Green-Screen Workflow** **81**


**11** Select the Merge4 node, change the Apply mode screen, and lower the Blend value as

low as you see fit to create a realistic reflection.


With the windshield reflection now seamlessly integrated, your composite is complete. Feel

free to go back and explore changing some of the values we’ve used. Throughout this

lesson, you’ve gone beyond basic keying by refining a core and edge matte, handling spill

suppression separately, and using 3D projection mapping to add realistic reflections.

These advanced techniques ensure your subject blends naturally into the scene, creating

a much more polished result.


Completed node tree for Lesson 2


**Lesson 2 Exploring a Green-Screen Workflow** **82**


## **Lesson Review**

**1** True or False? The Delta Keyer can handle both matte creation and spill suppression.

**2** What happens when you set the Delta Keyer’s Solid Replace mode to “Source”?

**a)** The keyer removes green spill automatically.

**b)** The original colors from the source clip are used, leaving green areas unchanged.

**c)** The alpha channel is inverted.

**d)** The brightness of the keyed subject is increased.

**3** True or False? A light wrap helps blend the foreground and background by overlapping

the edges of the keyed subject with the colors of the background.

**4** What is the advantage of using a Camera3D node or Projection3D node instead of

directly mapping a texture onto the Shape3D windshield?

**a)** It warps the reflection naturally based on the glass curvature.

**b)** It creates a sharper image.

**c)** It makes the reflection brighter.

**d)** It removes the need for a 3D scene.

**5** When setting up a Camera3D node for projection mapping, what must you enable?

**a)** Depth of Field

**b)** Ambient Occlusion

**c)** Camera Projection

**d)** Increase Z Translation


**Lesson 2 Exploring a Green-Screen Workflow** **83**


##### **Answers**

**1** True. The Delta Keyer can handle both matte creation and spill suppression.

**2** b) The original colors from the source clip are used, leaving green areas unchanged.

**3** True. A light wrap helps blend the foreground and background by overlapping the

edges of the keyed subject with the colors of the background.

**4** a) It warps the reflection naturally based on the glass curvature.

**5** c) Camera Projection


**Lesson 2 Exploring a Green-Screen Workflow** **84**


### Lesson 3
# Creating a Rainy Day

Transforming a tranquil sunny

day into an ominous rainstorm

is a quintessential challenge that

showcases the power of visual effects.

In this chapter, we’ll craft a hauntingly

atmospheric scene using a 3D camera,

Fusion’s Magic Mask node for precise

element isolation, and dynamic 3D

rain particles to breathe life into the

storm. Fusion’s ability to seamlessly

blend 2D footage and 3D elements

ensures that the process is intuitive

and flexible, allowing for natural and

cohesive results.



Time

This lesson takes approximately
1 hour to complete.

Goals

Merging 2D and 3D 86

Patching Together
a Sky Replacement 92

Magically Creating a Mask 97

Adding Reflections 105

Correcting Color in Fusion 109

Generating 3D Particles 113

Lesson Review 127


By blending technical precision with a bit of your own creative flair, you’ll begin to learn

how to blend 2D images and 3D scenes, use Fusion’s Magic Mask node to isolate objects

and integrate 3D particles that match live-action camera moves, and in the end, seamlessly

shift the mood from serene to foreboding—all while maintaining the illusion of

cinematic realism.


Completed composite for Lesson 3

## **Merging 2D and 3D**


As you discovered in the previous two lessons, compositing in 3D allows for complex

effects, like adding depth to flat images or projecting onto 3D shapes. To take that a step

further, combining 2D live action and 3D in visual effects compositing enables the creation

of seamless, multidimensional visuals that enhance the realism and impact of a scene.

Before we begin, let’s look at the shot we will work on.

**1** Open DaVinci Resolve 20 Studio, right-click in the Project Manager, choose Restore

Project Archive, select the **Fusion 20 3D Dry4Wet.dra** file, and then open the project.


**Lesson 3 Creating a Rainy Day** **86**


**2** From the Timelines bin, load the **Lesson-START** timeline and play the clip in this

timeline, which shows the man running onto the roof.


This clip was shot on a reasonably clear, sunny day, but we must turn it into a

rainstorm. One thing you should notice is the subtle camera move. When integrating

other elements into a live-action shot, as we must do here, we need to re-create the

camera’s motion and apply it to any element we integrate into the shot so it matches

the live action.


NOTE If you’re using the free version of DaVinci Resolve, you will receive a

warning when you restore the archive for this lesson. You can continue with

the lesson; however, some exercises require DaVinci Resolve Studio, so you will

be advised to skip those steps.


**3** Position the playhead over the clip in the timeline and enter the Fusion page.


This clip already has a small incomplete Fusion composition with a couple of nodes that

give us a head start.


**Lesson 3 Creating a Rainy Day** **87**


**4** Select the Merge 3D, press 1 to see it in viewer 1, and use the Time ruler to scrub

through the render range.


This scene already contains a 3D camera whose animation perfectly matches the

movement of the live-action camera. This match was achieved using Fusion’s 3D

Camera Tracker, which analyzes the live-action footage and re-creates its precise

motion using the Camera3D node. We’ll dive deeper into the 3D Camera Tracker in the

next lesson, but for now, it’s key to understand that the 3D camera in this composition

mirrors the live-action movement and allows us to seamlessly integrate a stormy sky

into the scene while maintaining perfectly synchronized motion.

**5** Disconnect the MediaIn1 node from the Camera3D node since this was only connected

as a visual aid.

**6** Open the media pool in the upper left corner of the Fusion page and select the Action

VFX Media bin.


**Lesson 3 Creating a Rainy Day** **88**


**7** Drag the StormClouds image to an empty area of the Node Editor near the Merge3D

node and rename it **StormClouds** .


As you learned in the previous lessons, to connect a MediaIn node to a Merge3D node,

we must connect it to an Image Plane first.

**8** Select the StormClouds node, press Shift-Spacebar, search for ImagePlane3D, and add

it to the Node Editor.


**9** Connect the ImagePlane3D to the Merge3D node.


When we performed the 3D camera tracking for this scene, we decided the scale

would be measured in meters. With that in mind, we can scale and position the image

plane to fit our scene.


**Lesson 3 Creating a Rainy Day** **89**


**10** Select ImagePlane3D and push the image plane back in the Inspector by -500 meters

using the Z translation parameter.


For these clouds to be truly over the town in our shot, 500 meters seems to be a

good distance.

**11** Use the scale parameter to increase the size of the clouds to 2500.


As in the previous lesson, to convert the Merge3D scene of the stormy sky back into a

2D image, we need to add a Renderer3D node.

**12** Select the Merge3D node, press Shift-Spacebar, search for Renderer3D, and add it to

the Node Editor.

**13** Select the Renderer3D and press 1 to see it in viewer 1.

**14** In the Inspector, set the Camera to Camera3D1 and the Render Type to Hardware.


You now have the stormy sky that matches the camera move found in our live-action

clip. Your job now becomes a simple sky replacement. However, this will be a rather

large comp, so before we create our sky replacement, let’s add some organization so

we can keep track of what each group of nodes is doing.


**Lesson 3 Creating a Rainy Day** **90**


**15** Drag a selection rectangle around the Camera3D, ImagePlane3D, StormClouds,

Merge3D, and Renderer3D nodes.


**16** From the Effects Library, select the Tools > Flow category.


The Flow category contains two tools that are not operational nodes that affect your

composition but rather tools that help organize the node graph or “flow.” One is a

Sticky node, which can be used as a reminder just as you would use sticky notes in the

real world. The other is an Underlay. The Underlay tool works as a visual organization

tool, especially in large node graphs. The Underlay node acts as a background layer to

visually group related nodes. It doesn’t impact the composition but helps organize

workflows by clearly delineating sections of the node tree.

**17** In the Effects Library, click the Underlay tool to add it to the Node Editor.


**Lesson 3 Creating a Rainy Day** **91**


The Underlay surrounds the selected nodes, visually grouping them together. You can

give the Underlay a name (and change its color), making it easier to see what the

groups of nodes are doing in your composite.

**18** Click in an empty area of the Node Editor to deselect all the nodes in the Node Editor.


Right-clicking over the Underlay title will select all the nodes contained within its

boundaries. This is great for moving the group around the Node Editor but not ideal

when you just want to rename the Underlay. So we must use a modifier when

renaming or setting the color for the Underlay.

**19** Hold the Option key (macOS) or the Alt key (Windows) and then right-click over the

Underlay title.

**20** Choose Rename from the menu and enter **SKY** as the new Underlay name.


The Renderer3D node is the essential step in converting your 3D scene into a 2D image,

which can now be used like any other 2D image for further compositing. We can now take

our newly moving stormy sky and composite it into our live-action clip for a sky replacement.


NOTE Backup versions are available in the Timelines > Backups bin for

different stages of the project.

## **Patching Together** **a Sky Replacement**


You may already be familiar with the basic steps for sky replacement from _The Visual Effects_

_Guide to DaVinci Resolve 20_ in this Blackmagic Design training book series. Here, we’ll use a

formula similar to the one taught in that book. First, we’ll merge the live-action shot with

the new sky and use an Apply mode to get a good blend of the two images.

**1** Drag the output of the Renderer3D node to the output of the Rooftop node to create a

Merge node.

**2** Select the Merge node and press 1 to see it in viewer 1.


**Lesson 3 Creating a Rainy Day** **92**


**3** In the Inspector, set the Apply mode to Darken.


The Darken Apply mode is particularly useful for this sky replacement because it

prioritizes darker pixels. Only the darker parts of the new sky (foreground) replace the

rooftop (background), allowing natural gradations and avoiding harsh edges. However,

it also affects our rooftop and our actor, which we need to fix.

##### **Importing with Loaders**


We will use masks to fix the problematic areas of our darkened sky replacement. These

masks are not currently linked to our media pool. Rather than switching to the media page,

linking in the masks, and then bringing them into the Fusion page, we can use Fusion’s

Loader node. If the content you are bringing in is sequential EXR files, then the Loader

node can be an efficient way of importing clips into Fusion directly, bypassing the

media pool.


TIP The content imported using Loaders in the Fusion page will not be contained

within DaVinci Resolve Archives. You must back up Loaders manually.


**1** Click in an empty area of the Node Editor to the right of the Sky underlay.

**2** Press Shift-Spacebar, type **Loader**, and add the Loader node to the Node Editor.


When you add a Loader node, it automatically opens a dialog for you to navigate to the

EXR sequence you want to import.


**Lesson 3 Creating a Rainy Day** **93**


**3** Navigate to the DR20 Studio Fusion 3D Training Media > Fusion Files > Masks > Bricks

folder, select the first **Bricks00001.exr** file, and click Open.


The Brickwall mask is loaded as a node named Bricks. A nice side benefit of using a

Loader node is that the node is renamed automatically.

**4** Add two more loaders to import the Town and Roof masks.


You can look at each mask in the viewer. There are different parts of our shot that need

to be protected from the Darken Apply mode. Instead of having you spend your time

drawing and animating masks, we’ve created these for you. You just need to learn how

to construct the node graph and put them to use.

**5** Select the Merge1 node in the Node Editor and press Shift-Spacebar to add a second

Merge node to the Node Editor.

**6** Click in an empty area of the Node Editor below the loaded mask nodes.

**7** Press Shift-Spacebar and type **MM** .


MM is the shortcut for a MultiMerge node. The MultiMerge allows us to connect more

than just a background and a foreground. As the name suggests, we can connect a

background and multiple foregrounds. Since we are just combining all the masks, it

doesn’t matter which of our masks goes into which input on the MultiMerge.

**8** Add the MultiMerge to the comp and connect the three masks to the MultiMerge node.


To embed these masks into the rooftop clip, we need to use a Matte control.


**Lesson 3 Creating a Rainy Day** **94**


**9** Click in an empty area of the Node Editor under the MultiMerge node, press Shift
Spacebar, and type **Mat** to select and add the Matte Control to the Node Editor.

**10** Drag the output of the MultiMerge to the green foreground input of the Matte Control.


We will now connect our rooftop to the background input of the Matte control.

However, to streamline and manage our growing node graph, you can add an elbow

that can make the graph easier to navigate.

**11** Midway along the pipe connecting the Rooftop to the Merge1 node, hold the Option

key (macOS) or the Alt key (Windows) and click the pipe to add a Router.


Routers allow you to bend and split node connections around other parts of the node

tree, preventing pipes from crossing over nodes or creating visual clutter.

**12** Drag the router just above and to the left of the Merge1 node.


**13** Drag a second output from the router to the yellow background input on the

Matte control.


**Lesson 3 Creating a Rainy Day** **95**


**14** Select the Matte control, press 1 to view it, and in the Inspector, set the Combine menu

to Combine Alpha.


**15** Lastly, since our Merge node expects pre-multiplied alpha channels, check the Post

Multiply Image checkbox.


You’ve now copied the alpha channel from the masks to the rooftop background image

so it can be used as the new foreground for our Merge2 node.

**16** Drag the output of the Matte Control to the foreground input on the Merge2 node.

**17** Select Merge2 and press 1 to view it.


**Lesson 3 Creating a Rainy Day** **96**


The sky replacement is starting to come together. If you look closely at the top half of our

actor, you will see some darkened sky coming through around his head. We need to create

a mask for him to prevent this bleed-through, but instead of taking the time to draw a

mask and manually rotoscope it, Fusion includes an AI alternative that we will explore next.
## **Magically Creating a Mask**


The Magic Mask node uses the DaVinci Neural Engine to quickly isolate objects or features in

a frame guided by user-drawn strokes, efficiently creating motion-tracked masks. It will save

you a lot of time creating a mask for our actor rather than using polylines and rotoscoping.

**1** Click in an empty area near the Rooftop clip in the Node Editor.

**2** From the Effects Library, choose Tools > Matte and then click Magic Mask.


NOTE Magic Mask is only available in DaVinci Resolve 20 Studio. To continue

with this lesson using the free version of DaVinci Resolve, use a Loader to add

the rendered Magic_Mask EXR sequence to the Node Editor near the Rooftop

node. Then skip to step 5 in “Finessing the Magic Mask” later in this lesson

and continue.


**Lesson 3 Creating a Rainy Day** **97**


**3** Close the Effects Library to give the two viewers more working space.


Just as with green-screen keying, it’s useful to have two viewers when using the Magic

Mask tool. We’ll set up the left side to show the original image, making it easy to draw

our strokes, while the other viewer will show our mask as it gets pieced together with

each stroke.

**4** Drag an output from the Rooftop clip to the input of the MagicMask node.

**5** Select the Rooftop clip and press 1 to see it in viewer1, and then select the Magic Mask

node and press 2 to see it in the right viewer.


The first stroke will be a single short stroke drawn down across our actor’s head and

torso. You are not tracing the subject; you are identifying what features belong to the

subject, so you want the stroke to be well within the subject’s boundaries.

**6** Press Shift-Right Arrow to move the playhead to the end of the render range.

**7** In viewer 1, draw a short stroke from the actor’s hairline down his white shirt.


**Lesson 3 Creating a Rainy Day** **98**


The area you drew over appears in viewer 2 as the start of your mask. Much of our

actor is missing, so we clearly need more strokes. Draw over areas that need to be

connected, such as his hand and his coat sleeve.

**8** Draw from the hand that is down by his side up his coat sleeve.


TIP If a stroke makes the mask worse or does nothing to add to the mask, you

can delete it by first clicking the Select button in the Inspector (or holding the

Shift key), drawing a selection rectangle around the strokes, and then clicking

the Delete button in the Inspector.


Using too many strokes will often cause more problems than it solves. Use as few

strokes as you can to get an accurate mask.

**9** Draw from the side of his coat down to his leg.


**Lesson 3 Creating a Rainy Day** **99**


**10** Our last stroke will be from his ankle to the tip of his shoe.


The frame you use to initially draw your strokes is called the _reference frame_ . The

reference frame is the starting point for the Neural Engine to understand the subject’s

shape, edges, and motion. Every frame is analyzed based on the information derived

from the reference frame.


TIP Two Neural Engine options appear at the top of the Inspector. Faster lets

you generate a lower-quality mask more quickly, suitable for garbage matting.

Better generates a higher-quality mask with more detail and softer edges, but

it is more processor-intensive.


**11** In the Inspector, click the Track Reverse button.


As the tracking proceeds, you can see the results of the mask in viewer 2. Chances are,

shortly after you begin, around frame 150 (+ or – 5 frames), tears or holes will appear

in the collar of his shirt. Strokes can be added in Magic Mask in the middle of the clip,

but it will invalidate portions of the existing track. If you notice occasional issues like

flickering, tears, or holes, you can address them by drawing a new stroke to cover the

error and tracking backward or frame by frame over those problematic sections.

**12** From the end of the render range, drag backward in the timeline ruler until you arrive

at the first frame where you see a hole in the collar.


**Lesson 3 Creating a Rainy Day** **100**


**13** Draw two short strokes: one that runs the length of his collar and a second that follows

the back of his head across his collar, ending at his upper back.


**14** Click the Track Reverse button again.


If the collar persistently appears with holes, you can track single frames at a time to

achieve better results.

**15** Again, drag backward in the timeline ruler until you arrive at the first frame where you

see a hole in the collar.

**16** Draw the two short strokes across his collar again.

**17** Click the Track Reverse One Frame button several times to correct the errors that

you observed.


**Lesson 3 Creating a Rainy Day** **101**


**18** If a hole appears on the collar as you track backward, draw a single line over the collar

where the hole appears and continue tracking single frames backward until

around frame 35.

**19** Around frame 35, click Track Reverse to finish the clip.


TIP Adding new strokes over already tracked areas will invalidate prior

strokes and will require you to track a portion of the clip again.

##### **Finessing the Magic Mask**


After you have finished tracking the matte, the Magic Mask’s Inspector also includes

several matte-refinement parameters you may be familiar with from other keying and

matte tools in the Fusion page.

**1** In the Inspector, click the Matte tab.


Most of the controls in the Matte tab, like the Gamma, Threshold, and Restore Fringe

parameters, will be very helpful when you have (wanted or unwanted) semitransparent

edges. However, our edges have no semitransparency but do have a fringe outline,

so using the Erode Dilate parameter can help.


TIP Adjustments in the Matte tab are best made by dragging the value

display rather than the slider. The value display provides a much more

granular adjustment.


**2** Drag to a frame in the clip where you clearly see the man on the roof.

**3** Set the Erode Dilate to -0.001 to shrink the matte slightly and remove the

outline fringe.

**4** Increase the Blur amount to 0.3 to soften some of the jagged edges.


**Lesson 3 Creating a Rainy Day** **102**


**5** Drag the output of the Magic Mask to a white layer input on the MultiMerge node.


TIP Magic Mask tracking data is stored in your Cache folder to increase

performance. If you move a project from another computer and do not bring

the cache folder in the archive, you must regenerate the cache files using the

Regenerate All button in the Inspector. You can locate these files by right
clicking the Regenerate All button and choosing Show Cache Folder.


**6** If necessary, select the MediaOut node and press 2 to view your composite in

the viewer.


To finish, we will again add some organization to our node graph using

another Underlay.

**7** Drag a selection rectangle around the MultiMerge, MatteControl, and Merge2 nodes.


**Lesson 3 Creating a Rainy Day** **103**


**8** Press Shift-Spacebar, type **underlay**, and press Enter or Return to add an Underlay

around the selected nodes.

**9** Click in an empty area of the Node Editor to deselect all the nodes in the Node Editor.

**10** Hold the Option key (macOS) or the Alt key (Windows) and then right-click over the

Underlay title.

**11** Choose Rename from the menu and enter **PATCHED FOREGROUND** as the new

Undelay name.


You’ve achieved great results using Magic Mask, but as with every tool, there will be times

when the results are not perfect. In those situations, don’t be afraid to use multiple tools.

The Magic Mask might work great as a well-fitted garbage mask, and then you can resort

to rotoscoping or paint to finesse the difficult areas.


TIP If you skipped creating the Magic Mask and opted to use the rendered Magic

Mask from the Fusion Files folder, you’ll need to use a Blur and an Erode/Dilate

node to correct the mask.


**Lesson 3 Creating a Rainy Day** **104**


## **Adding Reflections**

If the ground is meant to be wet, it would have reflections on it. It’s not difficult to add

reflections with a few nodes and some quick keyframing.

**1** From the toolbar, drag a Transform node to an empty area to the right of the MultiMerge.


**2** Drag a new output from the MagicMask node to the Transform (use a router to make

the node graph more organized as you see fit).

**3** Select the Transform node and press 1 to view those points in the node graph.

**4** Move to the last frame of the render range in the time ruler.


For this particular shot, it will be easiest to begin at the end of the render range where

our actor is onscreen.

**5** With the Transform node selected, in the Inspector, click the Flip Horizontal button.


**Lesson 3 Creating a Rainy Day** **105**


**6** Set the Y parameter to around -0.1.


We’ll need to align the reflection in the transform with the original rooftop image using

a Merge node.

**7** Select the Merge2 node, press Shift-Spacebar, type **merge**, and then add the Merge

node to the node graph.

**8** Drag the output of the Transform to the foreground input on the Merge3 node.


To blend the two images, we’ll use a combination of the Darken Apply mode, which will

cause the darker parts of the flipped rooftop (foreground) to replace the original

rooftop (background), and then we’ll lower the transparency for the flipped foreground.


**Lesson 3 Creating a Rainy Day** **106**


**9** With the Merge3 selected, in the Inspector, set the Apply mode to Darken and lower

the Blend slider so it appears more like a reflection.


Now we have a slight reflection on the ground, but to make it more realistic, we should

blur the reflection.

**10** Select the Transform node, and then from the toolbar, click the Blur tool to add it to the

node graph.

**11** Increase the Blur size a small amount.


The final step is to ensure the reflection aligns with the shot as the camera and the

actor move. We’ll use a few simple keyframes to move the reflection.


**Lesson 3 Creating a Rainy Day** **107**


**12** Select the Transform node, and in the Inspector, enable keyframing for the Center X

and Y parameters.


**13** Drag backward through the clip and use the Center X and Y parameters to keep the

reflection under the actor’s feet.


This result should be some quick keyframing that takes 5 to 10 keyframes. Let’s

create an underlay that groups those three nodes together and keeps our node

graph organized.

**14** Drag a selection rectangle around the Transform, Blur, and Merge3 nodes.

**15** Press Shift-Spacebar, type **underlay**, and press Enter or Return to add an Underlay

around the selected nodes.

**16** Click in an empty area of the Node Editor to deselect all the nodes in the Node Editor.

**17** Hold the Option key (macOS) or the Alt key (Windows) and then right-click over the

Underlay title.

**18** Choose Rename from the menu and enter **REFLECTION** as the new Underlay name.


This creates a very simple reflection, and it will become more believable when we color
correct the different elements. It might be a bit strong here, but it works for this exercise.

As with most of the effects and parameter values given in this book, you will want to adjust

them based on your final comp and your professional eye.


**Lesson 3 Creating a Rainy Day** **108**


## **Correcting Color in Fusion**

Performing a sky replacement is only half the task in our dry-to-wet look. Color correcting

the foreground is also required. We’ll leave the final color-grading pass to the color page,

but in this lesson, we will cover correcting and matching the different elements to make a

cohesive, believable shot.

**1** Select the Merge3 node and press 1 to view it. Then, in the toolbar, click the Color

Correct tool.


We’ll use this color correction to set a general adjustment for the entire shot.

**2** Drag the master color slightly toward blue and lower the saturation almost by half.


**Lesson 3 Creating a Rainy Day** **109**


**3** Drag the Gain slider lower to give a darker stormy look over the shot.

**4** Drag the Gamma lower a small amount.


This creates a nice base for our wet look. Next, we should correct the bright rooftop to

darken it even more without darkening the already moody sky and our actor.

**5** With the ColorCorrect node selected, click another ColorCorrect tool in the toolbar.


For this correction, we only want to affect the rooftop and ledge, so we will reuse our

masks for those two regions to limit our correction.

**6** Click in the empty area of the node graph above the second color correction.

**7** Press Shift-Spacebar, type **matte**, and then add the MatteControl to the Node Editor.


**8** Drag an output from the Magic Mask to the green foreground input of the

Matte Control2.


**Lesson 3 Creating a Rainy Day** **110**


**9** Drag an output from the ROOF mask to the yellow background input on the

Matte Control2.


**10** Select the MatteControl2 and press 1 to see it in the viewer.


If we color-correct using just the ROOF mask, the actor’s legs will also be corrected.

To prevent that, we can reuse the MagicMask and subtract it from our ROOF mask.


We can use the MatteControl to subtract the MagicMask from the background

ROOF mask.

**11** In the MatteControls2’s Inspector, select Combine Alpha from the Combine menu.

**12** Set the Combine Op menu to Subtract.


These Combine Operator modes are Boolean operations, and they determine how

the Foreground Alpha is copied into the Background Alpha channel.


**Lesson 3 Creating a Rainy Day** **111**


**13** Drag the output of the MatteControl2 node to the blue Effect Mask input on

ColorCorrect2.


**14** In the ColorCorrect2, reduce the Saturation slightly to mute the color and then lower

the Gamma to darken the roof.


Next, since moisture can soften the darkest areas, we’ll want to adjust the Shadows.

**15** From the Range menu, choose Shadows. Increase Lift slightly and use the color wheel

to shift shadows to a cool blue-cyan tone.


Since wet surfaces tend to absorb more light, we need to help the concrete appear

more saturated.

**16** From the Range menu at the top of the Inspector, choose Midtones, then lower

Gamma by half and again add a cool shift (blue/cyan) in the Midtones.

**17** From the Range menu, choose Highlights, increase Gain by half to give the appearance

of sheen, and then shift Highlights toward a cool/neutral tone.


**Lesson 3 Creating a Rainy Day** **112**


We’ve replaced the sky, added a reflection, and color-corrected all the elements to give our

scene a moody, stormy look. Again, as with the Green-Screen lesson, composting is an

iterative process. This is a good point to revisit any of the parameters you’ve adjusted and

tweak them to create a more refined look. The final piece is to add rain. For this, we’ll use

Fusion’s Particle system.
## **Generating 3D Particles**


Particles have infinite uses in just about every project type. You can create practical effects

such as fire and smoke or create more abstract motion graphic designs. Part of Fusion’s

toolset includes particle-specific nodes to simulate physical phenomena—wind, gravity,

and bounce—as well as forces that allow particles to be attracted to or repelled by other

objects. With so many ways to build and manipulate particles, it’s easy to become

overwhelmed with the possibilities. However, in this exercise, you’ll focus on building some

simple rain for our dry-for-wet shot that will give you the foundation for exploring particles

on your own.

**1** In the Node Editor, click in the empty area to the right of the MatteControl2 node, and

then click the pEmitter tool in the toolbar.


We’ll work in 3D so the particles can have depth and follow our 3D camera move. You’ll

begin by adding the two essential nodes to create particles.


Whenever you create a particle system in Fusion, you must start with a particle emitter

node, pEmitter, that generates the particles and a particle render node, pRender, that

renders the results.

**2** With the pEmitter selected, return to the toolbar and click the pRender node to add it

to the Node Editor.


**Lesson 3 Creating a Rainy Day** **113**


TIP The names of all particle-specific nodes begin with a p: pEmitter, pSpawn,

pBounce, pTurbulance, and so on. This naming convention makes it easy to

locate and identify particle-specific nodes.


To view the particles, you view only the pRender node. All other particle nodes are

visible only through the pRender node.

**3** Select the Matte Control 2 and press 1 to remove it from the viewer, and then select

the pRender and press 2 to see it in the right viewer.


TIP You can increase performance by removing an image from the viewer you

are not currently using, even if you use single-viewer mode.


When beginning to work with particles, your first choice is whether to generate

particles for a 2D or 3D composition. For this exercise, you will create a 3D particle

system. Luckily, this is the default setting located at the top of the pRender Inspector.

Because the pRender node is set to 3D, the viewer shows a 3D scene.

**4** Right-click in viewer 2 and choose Settings > Load Defaults to start in a standard

perspective view.


Most of your actual particle setup begins in the pEmitter node.


**Lesson 3 Creating a Rainy Day** **114**


**5** In the Node Editor, select the pEmitter.


A particle system is divided into two primary parts: the particle emitter and the

particle cells.


The particle emitter is the source of the particle cells. By default, the viewer displays

this emitter as a wireframe sphere, but you can easily change it into almost any shape,

including a rectangle, a line, text, or a polygon. It defines the area that produces

the particles.


The particle cell is the object multiplied and animated by the particle emitter. By

default, it is represented by small white points within the sphere, but as with the

emitter, the particle cell can be any image or built-in particle cell object.

**6** Press Play to see the default particles being generated.


Since the rain will be falling from the sky, the default sphere shape emitting the

particles is not ideal, so we will change it to a flat plane that we can use like a sky. You

control the shape, size, and position of the emitter in the Region tab.

**7** In the pEmitter’s Inspector, select the Region tab and choose Rectangle from the

Region menu.


The rectangle must be big enough to cover the area in front of the camera. For now,

we can enter a value and then reevaluate it once we composite the rain with our

live-action clip.


**Lesson 3 Creating a Rainy Day** **115**


**8** In the Region’s Width and Height, enter **100** for each, and then click in the viewer and

press F to fit the rectangle within the viewer.


To make the rectangle more like a sky or ceiling, it must be rotated by 90 degrees

and raised up.

**9** In the X rotation, enter a value of **90** degrees.

**10** In the lower left corner of the viewer, right-click the axis control and choose Front.

**11** Click in viewer 2 and press F to fit the front view of the rectangle in the viewer.


**Lesson 3 Creating a Rainy Day** **116**


Looking at this front view, you can see the ground plane. Currently, the rectangle is at

the same level as the center of the ground plane, which means it would be in the

center of our frame. It must be repositioned higher if we want the rain to appear like it

is falling from the sky. We won’t know the exact amount until we composite it, but we

can raise it now and fine-tune it later.

**12** Drag the Y Offset Translation value to 100.


Now that we have our region defined and our particle cells generated, we can add

motion. We will save the creation of the actual look of the raindrops for later. For now,

let’s focus on getting the basic setup correct.

##### **Adding Motion**


The default tab in the Inspector for the pEmitter is the Controls tab. There, you can start

to define how many cells are generated and in which direction they move. To give your

particle cells some movement and a trajectory, you use the Velocity and Angle controls

in the Inspector. It’s easier to perform motion-based adjustments on particles while

the comp plays.

**1** Use the axis control to return to Perspective view and reposition the view to see the

rectangle above the ground plane.


**Lesson 3 Creating a Rainy Day** **117**


**2** If necessary, click the Play button to begin playing the comp.

**3** Click the Controls tab in the Inspector.


Particle cells start with no motion. They require some force to make them move. So

when you first click the Play button, the particle cells appear to fill up the rectangle

emitter shape, but they don’t go anywhere.

**4** In the Velocity section of the Inspector, set the Velocity value to about 20.


All the particle cells shoot to the right at a steady, constant rate. However, not all

raindrops fall at the same rate in nature, so we need to add some variance to make the

rain appear more realistic.

**5** Below the Velocity setting, add 5 in the Velocity Variance parameter.


The value of 5 means some raindrops will have a variable velocity between 17.5 and 22.5.


To change the angle of direction so the rain falls down, use the Angle control.

**6** Adjust the Angle to -90, causing the particles to move downward.


Now the rain is falling, but driving rain typically doesn’t fall straight down. For a more

dramatic effect, let’s adjust the angle so the rain falls in a more realistic direction.

**7** Adjust the angle to -100.


The Number setting determines the number of particles generated on each frame.

The default Number setting of 10 generates 10 particle cells on every frame, which

may be too few for rain.


**Lesson 3 Creating a Rainy Day** **118**


**8** Set the Number to 100.


In a particle system, hundreds or even thousands of particles are generated

simultaneously, which can be demanding on your computer. To optimize performance,

it’s important to avoid generating unnecessary particles—especially those that are

offscreen. One way to do this is by adjusting the Lifespan parameter, which determines

how long each particle remains active.


The duration of our composition is 178 frames long, as indicated by the Render Range

End value near the time ruler. The time it takes for a raindrop to fall from the top to the

bottom of the frame depends on its velocity. Once a raindrop leaves the visible frame,

there’s no reason to keep rendering it since it no longer contributes to the scene. By

setting an appropriate Lifespan value, you can ensure that particles disappear when

they’re no longer needed, reducing computational load. In this case, estimating a

2-second lifespan should be more than enough for a raindrop before it exits the frame.

**9** Set the Lifespan parameter to 48 so the particles only last 2 seconds.


These settings are the essential parameters for the initial setup of any particle system.

You set the number of particles, the general speed, the direction, and the lifespan, and

then you inevitably iterate a few times over the values when they are all composited.


Now it is time to create the actual look of the rain. The other essential set of controls

determines the size, position, and shape of the particle cells. You’ve been using the

emitter’s default point cells, but it’s now time to explore other options.


**Lesson 3 Creating a Rainy Day** **119**


##### **Using an Image for Particle Cells**

It’s unusual to stay with the small white points for your particle cells. In fact, the cells can

be almost any object you choose. Often, you’ll use one of the built-in shapes to get started

and later switch to an image or small movie (a _sprite_ ) file when you have completely

configured the cells’ motion. You set the cells’ appearance in the Style tab.

**1** In the Inspector, click the Style tab and choose Bitmap from the Style menu.


The Style tab’s Style menu includes a list of the objects that can be used for the

particle cells. The Bitmap option adds an input to the Emitter node where you can

connect any image or video.

**2** Open the media pool, and from the Action VFX Media bin, drag **Rain Drop.png** to the

Node Editor near the pEmitter node.

**3** Select the MediaIn1 node and press 1 to see it in the viewer.


**Lesson 3 Creating a Rainy Day** **120**


The file is a small 200 x 200-pixel PNG that resembles a water droplet. When using

an image or movie for particles, try to keep them very small. Small textures reduce

the overall bandwidth demand, enabling the GPU to handle a large number of

particles efficiently.

**4** Connect the new MediaIn to the yellow Bitmap input of the pEmitter.


We’ll need to connect our camera to the particles so the raindrops match the

camera movement.

**5** Drag an output from the Camera3D to the green camera input on the pRender node.


The viewer shows the camera in our particle setup. You can see the two together a bit

clearer by switching to a top view.

**6** Right-click over the axis controls in viewer 2 and choose Top, and then click in the

viewer and press F.


**Lesson 3 Creating a Rainy Day** **121**


**7** Select the pEmitter node.


This view clearly shows the region rectangle far from our camera, so the rain will be

falling far away. We want it falling directly over our actor, so let’s correct the region size.

**8** Select the Region tab in the Inspector and adjust the Width and Height to **500** .


With the camera in place and our particles looking as good as we can get them

without the background in place, it’s time to composite the rain into our scene.


**Lesson 3 Creating a Rainy Day** **122**


##### **Rendering and Compositing Particles**

As we did earlier in this lesson, when we have a 3D scene and want to composite it into a

2D scene, we must add a Renderer3D node, which we can connect to a 2D Merge node to

composite the particles over the background.

**1** Select the pRender node and click the Renderer3D node in the toolbar.


**2** Select the Renderer3D node and press 1 to see it in viewer 1.

**3** In the Inspector, set the Camera to Camera3D1 and the Render Type to Hardware for

better performance.


To composite the rain, we need to add another Merge node after all our color corrections.

**4** Select the ColorCorrector2 and click the Merge tool in the toolbar.

**5** Drag the output of the Renderer3D into the green foreground input of the Merge4 node.


**Lesson 3 Creating a Rainy Day** **123**


**6** Select the Merge4 node, press 2 to see it in viewer 2, and then play the comp.


Again, these particles are very small, which is good for performance, but sometimes

you’ll need to increase their size, which can be done in the Inspector.

**7** Select the pEmitter node, and in the Style tab, increase the Size to 1.0.


Since the raindrops should reflect the light of the sky, they should have a bit more

glow. We can achieve this with an Apply mode.

**8** In the Inspector, set the Apply mode to Screen.


Finally, we need to apply motion blur to make the raindrops more realistic. The

Renderer3D allows us to render additional channels beyond RGBA. We can also render

motion vectors. Motion vectors represent the direction and speed of movement for

each pixel in a rendered frame. We’ll use that data to track how our 3D particles move,

allowing us to add motion blur as a post-processing effect.


**Lesson 3 Creating a Rainy Day** **124**


**9** Select the Renderer3D node and, in the Output Channels section, enable Vector.


TIP The motion blur for our rain simulation is based on the forward motion of

the raindrops relative to the camera, so there is no need to generate

back vectors.


**10** Press Shift-Spacebar, type **vector**, and add Vector Motion Blur to the Node Editor.


**Lesson 3 Creating a Rainy Day** **125**


**11** In the Inspector, lower the Vector Motion Blur’s Scale to 0.5 to lower the amount of blur.


The Vector Motion Blur generates motion blur using the vectors we output from the

Renderer3D.

**12** Play the composite to see the results.


You’ll probably notice that the rain starts to fall at the beginning of the shot, but we

really want it to be already falling when the shot begins.

**13** Select the pRender node, and in the Inspector, set Pre-Generate Frames to 48.


Now the rain will appear on frame 1 as if it had been falling for 24 frames before that.


You have completed this dry-for-wet look with a Magic Mask, 3D camera tracking, and 3D

particles. You could take this shot further by adjusting the rain, applying color correction,

or going into the color page and grading the clip with a darker and stormier look.


Completed node tree for Lesson 3


**Lesson 3 Creating a Rainy Day** **126**


## **Lesson Review**

**1** True or False? The Magic Mask tool in DaVinci Resolve 20 Studio uses AI to create

motion-tracked masks, eliminating the need for manual rotoscoping.

**2** True or False? The Underlay tool in Fusion affects the final composition by modifying

the visual elements within the node graph.

**3** True or False? The pEmitter node in Fusion must always use the default sphere shape

for emitting particles.

**4** What is the main advantage of using the Darken Apply Mode for sky replacement?

**a)** It prioritizes darker pixels, blending the new sky without

affecting brighter foreground elements.

**b)** It brightens the entire scene to match the sky.

**c)** It only applies changes to selected layers.

**d)** It automatically adjusts color grading based on the new sky.

**5** Why should particle lifespans be adjusted in Fusion’s particle system? (Choose two)

**a)** To ensure the particles remain visible throughout the entire scene

**b)** To improve performance by eliminating unnecessary particles once they

leave the frame

**c)** To make the particles move in a random pattern

**d)** To increase the brightness of the particles


**Lesson 3 Creating a Rainy Day** **127**


##### **Answers**

**1** True. The Magic Mask tool in DaVinci Resolve 20 Studio uses AI to create motion
tracked masks, eliminating the need for manual rotoscoping.

**2** False. The Underlay tool in Fusion _does not_ affect the final composition.

**3** False. The pEmitter node in Fusion has multiple shape options for emitting particles.

**4** a) It prioritizes darker pixels, blending the new sky without affecting brighter

foreground elements.

**5** a) To ensure the particles remain visible throughout the entire scene, and b) To

improve performance by eliminating unnecessary particles once they leave the frame


**Lesson 3 Creating a Rainy Day** **128**


### Lesson 4
# 3D Camera Tracking



One of the most difficult tasks in

budget filmmaking is set design.

Without a lot of money—and a small

army of carpenters—it’s a challenge

to make your set look like ancient

Rome, the command bridge of a high
tech starship, or an alien planet with

three moons. Typically, efforts to turn

your cousin’s basement into a secret

government research lab will end up

looking like your cousin’s basement.


Fusion changes all that. Using its

powerful 3D Camera Tracker node, you

can create enhanced set designs with

surprisingly little effort.



Time

This lesson takes approximately
1 hour and 10 minutes to complete.

Goals

Masking for 3D Tracking 130

Preparing the Camera Tracker 138

Solving for the Camera 142

Refining the Solve 144

Exporting the Scene 147

Positioning Objects in a 3D Set 153

Matching Color and Light 156

Lesson Review 159


During this lesson, you’ll learn how to set up, perform, and refine a 3D track to realistically

add a pirate ship off the coastline of a simple beach shot.


NOTE This lesson requires the Camera Tracker node and Magic Mask node,

which are available only in DaVinci Resolve 20 Studio.


Completed composite for Lesson 4

## **Masking for 3D Tracking**


As you experienced briefly in the previous lessons, Camera tracking is used to re-create a

virtual 3D scene corresponding to the physical set of your live-action scene.


While the intricacies of photogrammetry used by camera tracking are far beyond the

scope of this book, here’s a simplified explanation of the process: the Camera Tracker uses

the relative speeds and movement directions of items in your scene to determine where

they are in space. When you ride in a car or train, you observe that objects closer to the car

move more quickly than objects in the far distance. The Camera Tracker can use this

motion parallax to calculate the position of each element in the physical scene and

calculate where a virtual camera should be to replicate the same parallax within

the computer.


**Lesson 4 3D Camera Tracking** **130**


This calculated parallax works convincingly as long as everything in your shot is “nailed

down.” Objects within the shot that exhibit independent motion—such as those pesky

actors who always seem to find their way into visual effects shots—can confuse the

calculations and produce poor results because their speed is not dependent solely on their

distance from the camera. Therefore, before performing a 3D camera track, you must use

mattes to identify which objects you want to track and which you want to ignore.

**1** Open DaVinci Resolve 20 Studio, right-click in the Project Manager, and choose Restore

Project Archive.

**2** Navigate to the DR20 Studio Fusion 3D Training Media folder, restore the

**Fusion20Camera tracking.dra** (DaVinci Resolve Archive) file, and open the

Camera Tracking project.

**3** From the Master bin, load the **Lesson-START** timeline and play the clip in this timeline,

which shows the beach.


**Lesson 4 3D Camera Tracking** **131**


As it plays, try to identify objects in the clip that will require garbage matting—that is,

locate the objects in the shot that exhibit independent motion with respect to the shot

(things that aren’t “nailed to the set”).


In this shot, the actors and the ocean have independent motion. The rock outcrop and

the beach move only because the camera moves. You’ll matte these elements separately.


TIP Sometimes (and this is one of those times), it’s easier to first create

mattes of the objects you’re trying to track and then subtract the objects

you’re trying to avoid tracking. Fusion’s masking tools make these subtractions

easy, as you’ll see shortly.


**4** With your mouse pointer still over the beach clip, switch to the Fusion page and move

the playhead to the start of the clip.

**5** Click in the gray space of the Node Editor to deselect any selected nodes.

**6** Press Shift-Spacebar to open the Select Tool dialog, type **Mu**, and add a MultiPoly tool.

**7** Create a rough outline around the rock outcropping (including the palm trees) at the

start of the render range. You might want to pan the viewer to allow you to draw the

shape beyond the left edge of the frame.


**Lesson 4 3D Camera Tracking** **132**


**8** In the Inspector, enable the Shape Animation auto keyframe by clicking the

diamond icon.


**9** Advance the playhead to the last frame of the render range: frame 125.

**10** In the viewer toolbar, click the Select All Points button.


**11** Move and reshape the polygon to fit the rocks. Once you’ve roughly moved the shape

into place, you can click away from the points to deselect all and then click and drag

individual points to reshape as needed.


**Lesson 4 3D Camera Tracking** **133**


TIP Emphasize speed over accuracy. As long as you keep the rocks mostly

within your garbage matte, the Camera Tracker algorithm can ignore stray

pixels on either side of the matte edge. Your garbage matte shape should

require no more than a dozen control points.


**12** Move to roughly the middle of the clip, around frame 60, and reshape the polygon to

fit the rocks.


Unless you need to move individual points, it’s easier to keyframe the polygon using

a Shape Box.

**13** Click the Select All Points button again, and then press Shift-B to enable the shape box

around the entire polygon. Drag the control handles on the shape box to stretch and

resize the polygon shape to encompass the rock.


**14** Press Shift-B again to dismiss the Shape Box.


Scrub through the clip to make sure the shape consistently fits the rocks. Chances are

you will need to add one or two more keyframes to ensure the shape fits well.

**15** Reshape the polygon using the Shape Box or individual control points in areas

needing refinement.


TIP Pressing the Option-Left or Right Arrow key (macOS) or Alt-Left or Right

Arrow key (Windows) will move the playhead to the previous and following

keyframes, respectively.


**16** When you’re done keyframing the shape, in the Inspector, double-click the Polygon1

shape in the Polygon list and rename it **RocksGshape** .


**Lesson 4 3D Camera Tracking** **134**


**17** Click the Polygon button under the list to add a new shape to the Polygon List.

**18** Rename the Polygon2 **BeachGshape** .

**19** Move the playhead to the start of the render range.

**20** Create a rough outline around the sandy beach. Avoid including areas where the water

overlaps the shore.


**21** In the Inspector, enable the Shape animation auto keyframe by clicking the

diamond icon.

**22** Advance the playhead to the last frame of the render range, frame 125, and reshape

the polygon to fit the beach.

**23** Move to roughly the middle of the clip, around frame 60, and reshape the polygon to

fit the beach.

**24** Scrub through the clip and adjust the polygon shape to roughly follow the beach.

**25** In the Node Editor, select the MultiPoly node, press F2, and rename the node

**SceneryGshape** .


This works for the beach and rocks because they don’t require too many keyframes.

However, that isn’t always the case, and sometimes you’ll need to add more keyframes

or use other methods.


**Lesson 4 3D Camera Tracking** **135**


##### **Creating Mattes with Magic Mask**

NOTE The Magic Mask requires DaVinci Resolve 20 Studio.


The next few items that need to be masked are the three actors since they are also not

“nailed to the set.” They run up the beach, and their movement must be excluded from the

camera tracker. You could use the MultiPoly tool again to rotoscope the actors, but as you

learned in the previous lesson, a quicker way is to use DaVinci Resolve’s AI-based Magic

Mask tool. These masks can be less accurate than the results you needed for the previous

lesson, so the Magic Mask can easily do the job.

**1** Click in the gray space of the Node Editor to deselect all nodes. Press Shift-Spacebar,

type **Magic**, and then press Enter or Return to add the Magic Mask node.

**2** Drag a second output of the MediaIn node to the yellow input on the Magic

Mask node.


**3** With the Magic Mask node selected, press 1 to see it in viewer 1.

**4** Go to frame 82, which is the last frame in which we see all three actors onscreen and is

when they are at their largest point within the frame.


**Lesson 4 3D Camera Tracking** **136**


**5** For all three actors, draw a line for the head and spine, a line for each arm, and a line

for each leg.


**6** In the Inspector, click the Track Forward button.

**7** When that track completes, click the Reference frame button in the Go To Frame area

of the Inspector and then Track backward.


The results won’t be perfect, but they should be good enough for our 3D tracking.


Currently, the Magic Mask and the SceneryGshape mask are unconnected. Since the

Camera tracker has only one mask input, you need to combine them.

##### **Combining Mattes**


To create a single mask for your camera track, you must connect all the masks and

combine them so that the actors are subtracted from the beach and rocks mask.

**1** With the Magic Mask still viewable in viewer 1, select the SceneryGshape node and

press 2 to see it in viewer 2.


**Lesson 4 3D Camera Tracking** **137**


**2** Connect the output of SceneryGshape into the blue effect mask input of MagicMask.


The result in viewer 1 is the combined masks, which we will now connect to the

Camera Tracker.
## **Preparing the Camera Tracker**


With all the manual labor out of the way, it’s time to set up the tracker and let it do all the

hard number crunching.

**1** Click in an empty place in the Node Editor, under the MediaIn node.

**2** Press Shift-Spacebar, type **cam**, and select the Camera Tracker from the list of tools.

Click OK to add the tool to the Node Editor.


NOTE The Camera Tracker requires DaVinci Resolve 20 Studio.


**3** Drag a third output of the MediaIn node to the yellow input on the Camera

Tracker node.


The Camera Tracker is added to the Node Editor with the MediaIn1 node connected to

its input. To use the mattes you created, you must connect the MagicMask to the track

mask input of the Camera Tracker.


The problem is that the Magic Mask outputs the wrong data type for the Camera

Tracker. Magic Mask is just one of those special cases we must account for. To make it


**Lesson 4 3D Camera Tracking** **138**


work for the Camera Tracker, we need to use a Bitmap node to convert the output of

the Magic Mask. The Bitmap node converts an image into a black-and-white binary.

The values are set to 0 (black) or 1 (white), depending on the threshold you set.

**4** Click in an empty area of the Node Editor near the Magic Mask.

**5** Press Shift-Spacebar, type **bit**, select the Bitmap tool from the list of tools, and click OK

to add it to the Node Editor.

**6** Drag the output of the Magic Mask to the input of the Bitmap tool and press 1 to view

the Bitmap tool in viewer 1.


You should now see that the data has changed to be a binary black-and-white matte.

**7** Connect the output of the Bitmap to the track mask input of the Camera Tracker node.


This connection uses the masks to eliminate the sky and actors from our cloud of

tracking points.

**8** Select the Camera Tracker node, and In the Inspector, enable Preview Autotrack

Locations.


**9** Press 1 to see the Camera Tracker in viewer 1.


**Lesson 4 3D Camera Tracking** **139**


The Camera Tracker starts by generating a cloud of trackers informed by areas of

contrast in the image. The first job is to tune the settings for this particular shot to get

a good set of tracks.


Although you may not see many right now, the small green dots in the viewer indicate

features that would be tracked if you were to begin tracking now, but you want to track

a lot more features to improve the tracking data. You can always delete tracking points

later if they are inaccurately tracked.

**10** In the Inspector, reduce the Detection Threshold to around 1.8 and the Minimum

Feature Separation to around 0.01.


The Detection Threshold determines how much contrast an image feature must

display to be considered trackable. Minimum Feature Separation determines how close

tracking features can be to be considered unique. By lowering these two sliders, you

should see many trackable features displayed in the viewer. However, we don’t. Notice

that the green trackers are over the water and over our actors. This means our mask is

reversed, and we need to invert it to get the trackers on the beach and rocks.

**11** Select the Bitmap node and click the Invert checkbox in the Inspector.


**Lesson 4 3D Camera Tracking** **140**


**12** Select the Camera Tracker node to see the tracking points in the viewer.


Now, we are ready to track the camera movement. The Camera Tracker uses an optical

flow-based algorithm to follow pixels from frame to frame. You can further refine the

tracking using a pattern recognition–based method similar to the normal Tracker in

Fusion: a planar tracker algorithm that works well when you have large areas of planar

transformations in a shot. Or you can continue using optical flow, which works well for

a shot like this with very few crisscrossing objects or motion blur.

**13** To potentially create better tracking results at the expense of some additional time,

click Bidirectional Tracking.

**14** To initiate the tracking, click the Auto Track button.


**Lesson 4 3D Camera Tracking** **141**


The Camera Tracker steps frame by frame, calculating the positions for all the tracking

points. Obviously, the more tracking points you create, the longer the process takes. When

it reaches the end of the render range, the Tracker moves backward frame by frame to

refine the existing points.
## **Solving for the Camera**


Once auto-tracking is completed, you can enter known camera and scene parameters to

calculate the 3D representation of your live-action set. While Fusion can estimate much of

the camera information, the more information you provide about the physical camera that

captured the scene, the better the results will be. Often, the information is logged on set,

but you can also examine a clip’s metadata in Resolve’s Metadata Inspector to see if useful

information is listed there.


This footage was shot with a Blackmagic Ursa 4K using a focal length of 12.65 mm. At a

minimum, you should enter the focal length to solve the camera track.


TIP If you don’t know the focal length, you can use trial and error, entering your

best guess for the focal length until you get a satisfactory result. Fusion will

attempt to refine the focal length from your initial guess, but you must be “in the

ballpark” with your initial guess to succeed.


**1** At the top of the Inspector, click the Camera button to switch to the Camera tab.

**2** Enter a focal length of **12.65** and set the film gate to Blackmagic URSA/Production 4K

16:9. Resolve automatically enters the correct aperture settings for that camera type.


TIP You can often ignore mild lens distortion (as in this shot), but when

working with lenses with more distortion, you should select the Refine Lens

Parameters checkbox in the Solve tab to correct the distortion automatically.


Time to solve the camera track!


**Lesson 4 3D Camera Tracking** **142**


**3** Click the Solve button to switch to the Solve tab, and click Solve.


Depending on your computer, the solve may take several minutes to calculate.


When the solve is completed, the reward for your efforts will be a list of information.

But the first line is the key: the Average Solve Error.


An average solve error of around 0.5 means that, on average, any digital environment

work should be just over a half a pixel off, at most. Typically, you want this error value

below 1 at a minimum and ideally below 0.5. No matter where your average solve error

ended up, let’s refine the solve to see whether you can get the error below 0.5.


NOTE Depending on whether you’re using the saved Rotoscope Done

composition or the composition with your animated garbage mattes, your

average solve error will be different from the value in the preceding figure.


**Lesson 4 3D Camera Tracking** **143**


## **Refining the Solve**

The average solve error is sometimes called the _reprojection error_ because it measures

how closely the computer model of your live-action set can predict and re-create 3D

locations in the physical set.


Imagine replacing your live-action camera with a digital projector placed at exactly the

same location as the camera, pointing in the same direction, and using the same lens. If

your virtual set is perfectly reprojected back onto the scene using the virtual camera

image, every projected pixel should line up perfectly with the object in the physical scene.

If the reprojected pixels miss their marks, that’s a reprojection error.


The solve error is measured in pixels and refers to, on average, how far pixels are

misaligned from the original scene.


Looking at the viewer, most tracked features appear green to indicate a reprojection fit.

You’ll also see a few of the tracked features colored red to indicate that they have an

unacceptable reprojection error. To improve the overall solve quality, you can delete the

features with high errors.


**Lesson 4 3D Camera Tracking** **144**


TIP Solving is computationally demanding and RAM-intensive, but it is also

iterative as you refine the calculation. Deleting too many tracking markers and

re-solving can cause problems when your computing power is not up to it. If you

plan on doing multiple iterations, you should make a copy of the original Camera

Tracker node after each solve.


**1** Select the Camera Tracker node.

**2** In the viewer, drag a selection over a group of red trackers.


The trackers will highlight yellow to indicate that they are selected.

**3** In the Inspector, click Delete to remove the high-error tracked features.


This shot doesn’t have many red trackers clumped together, making it very difficult to

select more than a handful at once. The Inspector provides an easier way to select

trackers when manual selection is difficult.


The Maximum Track Error determines how poorly a feature was tracked during the

solving phase. The Maximum Solve Error determines how poorly a feature reprojects

based on the final scene.


**Lesson 4 3D Camera Tracking** **145**


**4** In the Solve tab, set the Maximum Track Error to 0.2 and the Maximum Solve

Error to 3.0.


If you push these values too far, you might actually find the reprojection error

worsening. By starting with a value of 3.0, you avoid deleting too many points at once.

**5** Click Apply Track Selection Filters to select for deletion all the tracks with errors worse

than the ones you just set.

**6** Click Delete to remove the high-error tracked features.

**7** Click Solve again to re-solve the scene with a leaner, more accurate sample of features.


At this point, you’ve likely achieved the goal of reducing the solve error to a little lower than

your initial results. It’s probably not worth the effort to reduce the error further.


NOTE Your solve errors will almost certainly be different from those shown here.

For example, slight differences in the positions of your garbage matte shapes

will change the accuracy of your solve. These differences are negligible, though,

and you’ll almost certainly achieve similar or better results by following the steps

described here.


On tougher shots, you’ll often repeat the solving and error reduction process several

times, lowering the error rate a little more each time until your solve fails (and you must

return to the solve values that you previously saved as a backup) or you achieve your

desired average solve error goal of less than 0.5.


**Lesson 4 3D Camera Tracking** **146**


## **Exporting the Scene**

At this point, the Camera Tracker node has computed a virtual 3D scene that matches the

original live-action scene to within slightly less than half a pixel. But before you can play

with this new scene, you need to establish some ground rules. In fact, you need to

establish a ground.


The Camera Tracker has no access to camera accelerometer data, so it doesn’t know if the

camera was level, tilted, upside down, or on its side. Before you begin working with the 3D

scene, you must tell the Camera Tracker where the ground is located.


NOTE If you were unable to get a satisfactory track, there is a saved version of the

composition with the camera track completed. Open the Timelines > Backups bin

and use 03 Backup to continue from this point.


**1** Click the Export tab at the top of the Inspector.

**2** Click the disclosure arrow next to 3D Scene Transform.


The options for setting the ground plane aren’t made visible until you

switch to Unaligned.


**Lesson 4 3D Camera Tracking** **147**


**3** Click the Unaligned button. The option to set the ground plane becomes visible in the

Orientation section.


In Fusion’s 3D coordinate system, X is the horizontal axis, Y is the vertical axis, and Z is

the depth axis. So the default XZ plane is the typical ground plane as defined by the

horizontal (X) and depth (Z) directions.


TIP In some shots, the ground may never be visible. In such a case, it might

make more sense to use another plane to identify the ground. For example, if

a green-screen wall has clear tracking features, selecting the XY plane would

allow you to lock the camera direction to the green-screen wall, even when the

floor isn’t visible in the shot or doesn’t track well.


**4** Move to the start of the render range.


Here you have a clear view of the “ground” of the beach. To set the ground plane, you

first select all the tracking points that track features located on the beach.

**5** In the viewer, drag through the trackers on the beach to select them.


**Lesson 4 3D Camera Tracking** **148**


**6** Shift-click any beach track points you may have missed with your selection.

**7** In the orientation section, click Set from Selection. The Camera Tracker adjusts the

scene rotation to align with the selected feature tracks.


You also need to tell the Camera Tracker where the origin point—the center of our 3D

universe—should be. It can be anywhere that’s convenient. We’ll select a feature track

point from the center of the beach and set it as the origin point.

**8** Hover your mouse pointer over the viewer and notice how Fusion offers a readout of

the solve error for the specific point beneath the pointer.


**9** Click a point with a reasonably low solve error on the beach in front of the pirates.

**10** In the Origin section, click Set from Selection.


The Camera Tracker sets the center of the internal 3D scene to the selected feature.


The last detail you should define is the scale of the scene.


**Lesson 4 3D Camera Tracking** **149**


##### **Defining Scale**

Setting a scale when performing 3D camera tracking defines the real-world size of the 3D

space relative to the tracked footage. This step ensures that objects, movements, and

distances within the 3D scene correspond accurately to the physical dimensions of the

original filmed environment. 3D objects or 2D elements composited into the footage must

match the physical scale of the scene to appear realistic. For instance, a ship in our scene

must be proportionate to the rocks and the people. The scale ensures that camera

movements behave naturally, maintaining accurate depth and parallax between objects

in the scene.

**1** In viewer 2, click a green tracking point at the base of the short Canary Island date

palm tree.


**Lesson 4 3D Camera Tracking** **150**


**2** Hold the Command key (macOS) or the Ctrl key (Windows) and select a green tracking

point at the top of the same date palm tree.


The size of this tree is 18 meters. It’s helpful to get size information from someone on

set. In our case, we know Canary Island date palms grow to between 10 and 20 meters,

and we are willing to put this on the larger side. After the two points are selected, you

can define the scale.

**3** In the Inspector, click the Set from Selection button, and in the dialogue, enter **18** .


**Lesson 4 3D Camera Tracking** **151**


TIP Conventional wisdom is to use the metric system for measurements. This

will help if you eventually need to add simulations from 3D applications such

as Houdini or Maya. Whatever measurement you choose, you must remain

consistent throughout the project.


Fusion uses a normalized coordinate system, meaning the value “1.0” can represent

any unit of measurement—feet, meters, or another unit—as long as you remain

consistent when inputting object sizes. In this case, we’ll assume that “1” represents 1

meter in Fusion. Therefore, a value of “18” corresponds to 18 meters, which is the

height of our Canary Island date palm tree.


You now have a ground plane, origin, and scale defined. It’s time to export the scene.

**4** Click the Aligned button in the Inspector to lock in the adjustments.

**5** At the top of the Inspector, click the Export button.


The Node Editor automatically creates a group of five nodes representing the

created 3D scene.

**6** Drag to reposition the new nodes as desired.


**Lesson 4 3D Camera Tracking** **152**


Congratulations! You’ve performed your first 3D track.


The new nodes create a 3D scene with a Merge 3D, Camera 3D, Ground Plane, Point Cloud

3D, and a Camera Tracker renderer.


With the 3D camera track performed, it’s time to turn all that quality data into movie magic.

This will be a straightforward composite of adding a pirate ship out on the horizon.
## **Positioning Objects in a 3D Set**


To add a ship to the horizon, most of the heavy lifting is already done, and we can achieve

the result with just six more nodes.

**1** From the Clips bin in the media pool, drag **PirateShip.png** into the Node Editor.


**2** Press 1 to see the PirateShip.png in viewer 1.


To composite this ship into our 3D scene, the MediaIn node must be placed on

a 3D shape.

**3** With the MediaIn selected, use the Select Tool dialog to add a Shape3D node.


**Lesson 4 3D Camera Tracking** **153**


**4** Press 2 to view the Shape3D in viewer 2


**5** Drag the output of the Shape3D and connect it to the Merge3D node. Then select

Merge3D1 and press 1 to see it in viewer 1.


**6** Select Shape3D, click in viewer1, and press F to frame it.


**Lesson 4 3D Camera Tracking** **154**


TIP You might need to use the modifier keys plus middle mouse button

combinations that you learned in previous lessons to get the same framing

shown in our frame.


The ship is composited into the 3D scene at the origin you defined, but this graphic of

a galleon ship is not scaled correctly for our scene, so we need to scale it. Remember,

we are using the metric system, so in meters, a galleon is 50 meters long.

**7** In the Shape3D node, set the Size to 50 (meters).


Now, we need to position it offshore by about 175 meters. It is easiest to do this while

viewing the output of the CameraTracker1_Renderer node.

**8** In the Node Editor, select the CameraTracker1_Renderer node and press 2 to view the

output in viewer 2.

**9** Select the Shape3D node, and in the Inspector’s Transform tab, use the Z Translation

slider to push the ship out in Z until it’s somewhere between -100 and -200 meters.

You’ll know the right distance when the movement of the ship looks realistic.


NOTE Depending on your choice of ground plane and origin, your ship won’t

perfectly match the one pictured here. You might need to adjust the

Translation Z value to get a closer match.


**Lesson 4 3D Camera Tracking** **155**


**10** Next, adjust the X and Y Translation controls to position the pirate ship just to the right

of the rock outcropping and just below the horizon line.


TIP Depending on the ground plane you selected, the slope of the beach may

not be as flat as the ocean, so you may need to correct the Z rotation just a bit.


**11** Play the composition to see how the ship matches the camera move.


That’s all it really takes to add the ship and have it match the camera move from the 3D

track. Now comes the compositing part, where you must make it appear as if the ship fits

naturally in the beach setting. That will require some lighting and color correction.
## **Matching Color and Light**


Compositing isn’t just about placing one object on top of another. (At this point, you

probably know that.) Although the ship follows the camera motion perfectly, it still needs

work to look realistic. One of the nice things about Fusion’s 3D space is that when there are

no 3D lights in a scene, it simply passes pixel data straight through. This means we can add

a simple color correction to the ship graphic in MediaIn2 to create the illusion of sea haze

atmospherics over the ship.

**1** Select MediaIn2, press Shift-Space to open the Node Selection tool, and choose a

Color Compressor node.


**Lesson 4 3D Camera Tracking** **156**


To create a realistic blue haze, we need to sample the blue as a “sea haze” reference.

To do that, we need to load the image into a viewer.

**2** Select MediaIn1 and press 1 to load it into viewer 1 (viewer 2 should still have the

CameraTracker1_Renderer node loaded).

**3** Select ColorCompressor1 and drag its Eyedropper tool to sample the sky where the

pirate ship will be.


**4** Drag the Compress Hue, Compress Saturation, and Compress Luminance sliders all

the way to 1.0.


**Lesson 4 3D Camera Tracking** **157**


The result…is not pretty. First, the edges of the image are overcorrected. We can use a

little trick to fix that.

**5** Drag from the output of MediaIn2 to ColorCompressor1’s blue mask input.


This step uses the ship’s own alpha channel as a mask for the color correction,

preventing it from affecting the edges.


The second issue is that our initial values wash out the ship almost completely.

Let’s correct that.

**6** Lower the Compress Hue, Compress Saturation, and Compress Luminance sliders until

you have created a slight “sea haze” effect.


TIP You can use the Blend slider in the Color Compressor’s Settings tab to

blend more or less of the original image with the effect.


**Lesson 4 3D Camera Tracking** **158**


You now have a pirate ship sitting convincingly in the water off the headland.


The last step is to ensure the camera tracker renderer is connected to MediaOut so

that you can see the results in the Edit page timeline.

**7** Drag the CameraTracker1_Renderer output to the MediaOut.


You can see how easy it is to add elements to a 3D-tracked shot. Having 3D tracking built

into DaVinci Resolve 20 Studio means that with a little effort, you can transform simple sets

into grand period pieces or galactic starships. Best of all, there’s no waiting for a separate

studio to deliver the visual effects to you. As the composite progresses, you can instantly

see how it works in the scene and make changes without causing massive delays.


Completed node tree for Lesson 4

## **Lesson Review**

**1** True or False? 3D camera tracking is available only in DaVinci Resolve 20 Studio.

**2** True or False? It’s OK for the 3D Camera Tracker to follow people and moving cars since

they will help calculate the parallax.

**3** What camera information should be entered into the Camera Tracker for

solving to work?

**4** When setting the ground plane for a floor in the frame, should the coordinates be set

to XY, XZ, or YZ?

**5** True or False? Adjusting the Maximum Solve Error and the Minimum Track Length can

potentially improve a high solve error.


**Lesson 4 3D Camera Tracking** **159**


##### **Answers**

**1** True. 3D camera tracking is not available in the free version of DaVinci Resolve 20.

**2** False. You only track objects that are “nailed to the set.” All other moving objects

should be eliminated using a garbage matte.

**3** The lens focal length must be entered to solve the 3D track.

**4** XZ are the appropriate coordinates for a ground plane because X represents the

horizontal axis and Z represents depth. The other two coordinates are more

appropriate if the ground is not in the frame, such as for a wall.

**5** True. Adjusting the Maximum Solve Error and the Minimum Track Length can

potentially improve a high solve error.


**Lesson 4 3D Camera Tracking** **160**


### Lesson 5
# Compositing 3D with USD



In this last lesson of our advanced

Fusion training guide, we will slow

the pace a bit. This will be a beginner
friendly training lesson for students

new to Universal Scene Description

(USD) and with limited knowledge

of 3D workflows. If you’ve never

worked with 3D before this guide or

don’t know what USD is, don’t worry—

we’ll break it down in simple, practical

steps. USD is a powerful, industry
standard format developed by Pixar

for managing complex 3D scenes,

making it easier to work with models,

animations, and visual effects across

different software.



Time

This lesson takes approximately
1 hour to complete.

Goals

Importing USD into Fusion 162

Creating Surfaces with Shaders 166

Rendering USD 171

Making a Dragon Fly 174

Matching Lights to a Scene 177

Creating a Flight of Dragons 186

Using Z Depth in Color Correction 190

Finishing the Comp 197

Lesson Review 199


In this lesson, you’ll learn what USD is, why it’s useful in Fusion, and how to start working

with it for your own projects—all without needing 3D experience. Let’s get started!


Completed composite for Lesson 5

## **Importing USD into Fusion**


In this exercise, we will create flying dragons around a helicopter shot of the Griffith

Observatory in Los Angeles, California. We’ll start by restoring an archive that has the

helicopter clip and a 3D camera tracked for us. As you know from the previous exercise,

3D camera tracking is essential when integrating 2D or 3D objects into a shot with a

moving camera.

**1** Open DaVinci Resolve 20 Studio, right-click in the Project Manager, and choose

Restore Project Archive.

**2** Navigate to the DR20 Studio Fusion 3D Training folder, restore the

**Compositing with_USD.dra** and open the Compositing with USD project.


**Lesson 5 Compositing 3D with USD** **162**


**3** From the TImelines bin, load the **Lesson-START** timeline and play the clip in this

timeline, which shows a helicopter shot of the Griffith Observatory.


Our plan for this shot is to integrate a few dragons that circle the observatory. Let’s

look at the Fusion comp that we have started.

**4** With your mouse pointer still over the Observatory clip in the timeline, switch to the

Fusion page and move the playhead to the start of the render range.


The Fusion composition has the MediaIn node, MediaOut node, and a 3D camera,

resulting from a 3D track we created for you. We’ve already deleted the 3D Camera

Tracker, Point Cloud, Ground Plane, and Merge3D node, leaving only the Camera3D

with the correct animation we need. Note that we’ve set the origin of the 3D track as

the center of the dome.


The next step is to import our USD Dragon. Similar to particles, USD is actually a

collection of nodes, allowing you to manipulate, re-light, and render USD files. Again,

similar to particles, where all the nodes begin with the letter _p_, USD nodes begin with

the letter _u_ . So to import a USD element, we use a uLoader node.


TIP You can also add USD elements into DaVinci Resolve using the Media tab

and then access them from the media pool when in Fusion.


**5** Click in the gray space of the Node Editor above the MediaIn node to deselect any

selected nodes.

**6** Press Shift-Spacebar to open the Select Tool dialog and type **uld** to find and add a

uLoader node.


**Lesson 5 Compositing 3D with USD** **163**


**7** In the Open dialog, navigate to the Fusion Files > USD > master_dragon_asset folder

in the DR20 Studio Fusion 3D Training folder. Then select **main_dragon.usd** and

click Open.


TIP USD elements imported into Fusion using a uLoader node

simultaneously store the USD element in the currently active bin in

DaVinci Resolve’s media pool.


**8** In the Node Editor, select the main_dragon node, press 1 and zoom out to see it in the

viewer. Then press Play to see the animation.


This dragon model includes 39 frames of animation showing the wings flapping. We

need the animation to last for the duration of our comp, which is easy to do by looping it.

**9** In the Inspector, click the loop checkbox to make the 39-frame animation loop for the

duration of our composition.


The other adjustment we can make in the uLoader is the speed of the animation. This

current speed is too quick, so let’s slow it down.

**10** In the uLoader’s Inspector, set the Time Scale to .5, which runs the animation at

half speed.


**Lesson 5 Compositing 3D with USD** **164**


While the uLoader node can make some adjustments, it mainly focuses on loading USD

assets efficiently. It can’t directly change the unsuitable glossy texture the dragon was

imported with. Creating the dragon’s look is handled by Fusion’s shading and material

tools, which give you greater flexibility in refining the dragon’s appearance.


**What Is Universal Scene Description?**

USD (Universal Scene Description) attempts to solve two big problems in 3D

animation. First, it attempts to create compatibility among the many different 3D

software packages typically involved in post-production work. Second, it

addresses the issue of keeping everything up to date as changes are made at

different stages in a development pipeline.


Imagine this scenario: You’re creating a short promotional video in Resolve using

the Fusion page for compositing. The scene features a 3D mascot—designed in

Blender with textures from Photoshop—walking through a stylized environment

built in Maya.


Partway through production, the client decides they want to change the mascot’s

shirt color and remove a tree in the background that distracts from the main

action. In a traditional pipeline, you’d have to re-export from Blender and Maya,

re-import into Fusion, and potentially redo any lighting or compositing tweaks

you’d already made—because the updated scenes could override your

local changes.


With USD, however, the Blender artist updates the mascot’s shirt, and the Maya

artist deletes the tree.


You open your Fusion scene and immediately see both changes—without losing

your carefully tuned lighting and compositing “overrides.”


Those overrides are the real magic here. They let you keep any local tweaks (for

example, new lights or color adjustments you’ve applied in Fusion) completely

separate from the core models and textures. So when artists upstream refine their

parts of the project, your scene is updated automatically without wiping out your

local modifications.


That’s USD in a nutshell: a single format that keeps everyone’s work in sync while

letting each person make their own changes independently, preserving and

stacking those changes rather than forcing endless re-imports and fixes.


**Lesson 5 Compositing 3D with USD** **165**


## **Creating Surfaces with Shaders**

To create the look of leathery dragon skin, you use shaders. A shader defines how an

object’s surface looks when light hits it. Think of it as a digital material that determines

whether something appears shiny, rough, transparent, or metallic. Fusion includes Shader

and uShader nodes, which work almost identically. Each node we add to the uShader will

build different aspects of the overall skin look, such as color, roughness, or displacement.

By connecting these types of nodes together, we can build complex surfaces. Think of it

like layering effects in Photoshop—instead of just applying a color, you combine different

properties to create realistic materials. The first piece we’ll add to the shader is just a base

texture image to replace the current glossy look.

**1** With the main_dragon node selected, press Shift-Spacebar and search for the

uReplaceMaterial tool. Then, add it to the node graph.

**2** Select the uReplaceMatieral node and press 1 to view it.


You may recall using a Replace Material node in the very first lesson of this guide to

replace material on a Text3D. We’ll use a version of that node here specifically for USD

models. With the uReplaceMaterial node in place, we can begin replacing the glossy

texture with our own material.

**3** Click in an empty area of the node graph just above the uReplaceMaterial node and

press Shift-Spacebar. Search for and add a uShader node.


**4** Drag the output of the uShader node to the green material input on the

uReplaceMaterial node.

**5** Click in an empty area of the node graph just above the uShader node and press

Shift-Spacebar. Search for and add a uTexture node.


**Lesson 5 Compositing 3D with USD** **166**


Think of a shader as the set of rules that determines how a surface looks under various

lights and angles; a texture is the actual image applied to your 3D model.

**6** To import a texture, select the uTexture node, and in the Inspector, click the

Browse button.

**7** In the Open dialog, navigate to the Fusion Files > USD > master_dragon_asset > maps

folder located in the DR20 Studio Fusion 3D Training folder. Then select dragon_

diffuse.tif and click Open.


Next, we’ll connect the texture to an input on the Shader node. However, the Shader

node has many inputs for different properties such as specular, opacity, and

displacement. For the base texture of our dragon, we want to make sure we connect

this texture to the diffuse color input.

**8** Drag the output of the dragon_diffuse node over to the uShader node, and then

release the mouse button.

**9** From the menu of inputs, select diffuseColor.


TIP Diffuse color is essentially the object’s basic color—the one you see when

light hits it evenly. It’s like choosing your base coat of paint.


The dragon now has a less glossy appearance to his skin.


**Lesson 5 Compositing 3D with USD** **167**


##### **Adding Roughness and Shading**

To make our dragon skin even more realistic, we can mix a few different ingredients with

our diffuse color. Roughness in terms of 3D shaders determines how smooth or rough a

surface appears. It is typically a grayscale image that helps define the surface as sharp and

polished (high roughness) or blurred and diffused (low roughness).

**1** Click in an empty area of the node graph to the left of the uShader node and press

Shift-Spacebar. Search for and add another uTexture node.

**2** In the Inspector, click the Browse button and from the Fusion Files > USD > master_

dragon_asset > maps folder, open Leather_roughness.png.

**3** Drag an output of the Leather_roughness node over to the uShader node and release

the mouse button.

**4** This time, from the menu of inputs, select Roughness.


Having a texture connected to the Roughness input on the uShader displays new

Roughness parameters in the Inspector. The Roughness parameters control the

tightness of the specular highlights. A positive Bias has a wider falloff, while a negative

Bias creates a glossier surface.


**Lesson 5 Compositing 3D with USD** **168**


**5** In the uShader node, lower the Roughness Scale and increase the Roughness Bias

until the dragon texture appears more leathery and less shiny.


One more common shader property is occlusion. An occlusion map is like a grayscale

overlay that tells your shader which areas of a model should look darker because

they’re less exposed to light. The darker the spot on the occlusion map, the less light

that area gets, adding depth and realism to your model without calculating every

tiny shadow.

**6** Click in an empty area of the node graph between the two texture nodes you have

added and press Shift-Spacebar. Search for and add a third uTexture node.

**7** In the Inspector, click the Browse button, and from the Fusion Files > USD >

master_dragon_asset > maps folder, open dragon_occlusion.exr.

**8** Drag the output of the dragon_occlusion node over to the uShader node and release

the mouse button. Then, from the menu of inputs, select Occlusion.


**Lesson 5 Compositing 3D with USD** **169**


The occlusion map is very heavy, making our dragon look too dark. Controls for the

occlusion are located in the uShader.

**9** Select the uShader, and in the Inspector, increase the Occlusion Bias to about 0.5 or

until the dragon is lighter but still has a fair amount of shading.


TIP If the 3D ground plane grid is distracting you from making adjustments,

you can temporarily hide it by right-clicking in the viewer and choosing

Options > Grid.

##### **Replacing Textures on Primitives**


If you look at the head of the dragon, the primitive geometric shapes for the eyes and

teeth both use the same diffuse base texture as the dragon’s body. This is because we

replaced the entire USD model and not just the body primitive. We need to find a way to

apply different materials to different primitives of our model. We use the uReplaceMaterial

node to designate which parts of the dragon geometry have their texture replaced.

**1** Select the uReplaceMaterial node.


The uReplaceMaterial node allows us to select which material on the dragon is

replaced by using a Scene tree window.

**2** In the Inspector, click the Prim Selection Pick button.


**Lesson 5 Compositing 3D with USD** **170**


TIP Prim is short for primitive, which refers to any object or element in

the USD file.


The Scene Tree window uses a simple hierarchy tree to represent the elements in a

USD scene. In certain USD tools, the tree is displayed by pressing the Pick button in the

Prim Selection box.

**3** In the Scene Tree window, select dragon_body and then click OK.


The uReplaceMaterial node gives you access to the primitives in the geometry, allowing

you to select what gets replaced and what reverts to the original material that came in with

the USD scene. Now, all the textures you applied are only assigned to the body of the

dragon, leaving the eyes and teeth to use the textures they originally came in with.
## **Rendering USD**


To composite the dragon over the live-action Observatory shot, we need to render it just

as we did in our other Fusion 3D scenes from previous lessons. Whereas we use a

Renderer3D for Fusion’s standard 3D scenes, we use a uRenderer for USD scenes. Let’s

first merge what we currently have with the camera so the dragons inherit the same

camera motion of our live-action helicopter camera.

**1** Select the uReplaceMaterial node, press Shift-Spacebar, and add a uMerge node.

**2** Drag the output of the Camera3D node into the uMerge node to combine it with

our dragon.


**Lesson 5 Compositing 3D with USD** **171**


**3** Press Shift-Spacebar, add a uRenderer node, and then press 1 to view it.


There are a few different controls in the uRender compared to the Renderer3D you are

now familiar with. However, the first is a setting you should always set, no matter

which renderer you use.

**4** In the uRenderer, set the Camera to Camera3D1 to ensure you render the

correct camera.


USD supports using different renderers just like 3D applications. Currently, Fusion

supports the Storm renderer, so although there is a menu to choose from, Storm is the

only option in the Renderer Type menu.


NOTE Storm is USD’s default rendering engine. It quickly renders your 3D

scenes so you can see them interactively.


Eventually, you’ll want to enable the uRenderer to render lights. Once we enable the

lights in the Inspector, our scene will go completely dark because we haven’t added

any lights yet. For now, we’ll just use the camera default lights until we are ready to add

our own. The output of the uRenderer renders our 3D scene as a 2D image that can be

composited over our observatory shot using a standard Merge node.

**5** Select the MediaIn1 node and click the Merge button in the toolbar.


**Lesson 5 Compositing 3D with USD** **172**


**6** Drag the output of the uRenderer node to the green foreground input of the

Merge node.


**7** Select the Merge node and press 2 to see the composite in the viewer.


TIP The uRenderer outputs a 2D image into sRGB color space by default. If

you are using Resolve Color Management, you will want to enable Linear Color

Space in the Image tab.


This is the first time we see our dragon against our background, and immediately, we can

see that the scale is wrong. The dragon is much too large. Furthermore, we need to make

the dragon circle the observatory, and we still need to correct the lighting.


**Lesson 5 Compositing 3D with USD** **173**


## **Making a Dragon Fly**

To get the dragon to circle around the observatory, we’ll use 3D transforms. Fusion’s USD

toolset has its own Transform tool for USD objects.


NOTE While most parameters in these lessons are open for experimentation,

follow these dragon animation values closely. The detailed mask we add later in

this lesson assumes the dragons fly a specific route.


**1** Select the uReplaceMaterial, press Shift-Spacebar, and add a uTransform node to the

graph between the uReplaceMaterial and the uMerge.


**2** Select the uTransform1 node and press 1 to view it.

**3** In the Inspector, change the scale to 0.3.


Viewer 2 now shows a more appropriately sized dragon for our observatory.


We now need to orient the dragon so it appears to be circling around the

observatory. We won’t actually circle it yet; we’re just setting up the initial position.

**4** Move to the start of the render range.


**Lesson 5 Compositing 3D with USD** **174**


**5** Select the uTransform1 node, and in the Inspector, adjust the Translation controls to

move the dragon along the edge of the ground plane. Make the adjustments as

follows: X: -50, Y: 10, and Z: -5.


Our dragon will circle around clockwise, so it should be facing in the opposite direction.

**6** In the Inspector, adjust the Y rotation to 180.

**7** To give the dragon a realistic tilt as it circles the observatory, adjust the Z

rotation to -45.


**Lesson 5 Compositing 3D with USD** **175**


Now for the circling part of our animation. To create a circular flight path for our

dragon, we need to add a new Transform node and rotate around a central pivot point.

**8** Select the uTransform, press Shift-Spacebar, and add a second uTransform directly

after the first one.

**9** Select the uMerge node and press 1 to view it.


When you add a second transform node in Fusion, its pivot point resets to the center

of the scene (X:0, Y:0, Z:0). This makes it easy to orbit your dragon, which is positioned

away from the center. Think of it like the solar system: the first Transform node sets the

dragon’s orientation (like the earth’s rotation on its axis), and the second Transform

node makes the dragon orbit around the observatory (like the earth’s

orbit around the sun).

**10** Make sure you are still at the start of the render range and on the uTransform2 node

click the Enable Keyframe button in the Inspector for the Y Rotation.


**Lesson 5 Compositing 3D with USD** **176**


This sets our starting position for our flying dragon. Next, we’ll have the dragon go

75% of a full rotation so it won’t completely circle the observatory, but it will be enough

to fly behind and then in front of the dome.

**11** Move to the end of the render range and then adjust the Y rotation to (negative) -270.


Our flying dragon is in place and circling the observatory dome. However, we still need to

tweak it to make this look realistic. The first tweak is to replace the default lights on our

dragon with ones we purposely set to match the live-action shot.
## **Matching Lights to a Scene**


Lighting is the secret sauce that helps blend CGI with live-action footage seamlessly. In this

exercise, we’ll work with Fusion’s USD lighting tools to replicate the natural sunlight

captured in our live shot. Using a 360-degree Dome light and supplementing it with two

carefully adjusted Disk lights, you’ll learn how to create a realistic, nuanced lighting setup

that combines digital and real-world elements.

**1** In the upper left corner of the Fusion screen, click the Effects button to open the

Effects Library.

**2** Navigate to Tools > USD > Light to view all the USD lighting options.


Just by looking at the names of these lights, the most obvious one to mimic sunlight

would be the uDistant Light. However, the uDome light captures real-world lighting

conditions by using an HDR image wrapped around your scene in 360°, simulating

light bouncing off the environment.


**Lesson 5 Compositing 3D with USD** **177**


**1** Select the uMerge node and click the uDome Light from the Effects Library.


Not much will change for two reasons: first, as you might recall, we are still using the

default camera lighting in the uRenderer rather than lights in our scene; second, we

haven’t yet loaded an HDR image for the uDome light.

**2** Select the uRenderer, and in the Inspector, select the Scene button for lighting.


The viewer on the right updates to show the new lighting, but viewer 1 still shows the

default camera light. To have the viewers also show the scene lighting, you must switch

the viewer setting.


**Lesson 5 Compositing 3D with USD** **178**


**3** Above the viewer, click the Lighting dropdown menu and choose Scene Lights.


Now, we can set up the uDome light.

**4** With the uDomeLight node selected, click the Browser button at the bottom of the

Inspector to import the texture file.

**5** Navigate back to the Fusion Files > USD > master_dragon_asset > maps folder and

open the sunset_4k.hdr image.


It’s rare that the image you import perfectly matches the sky that you are trying to

simulate, so we can give it a bit of help by sampling the color from our live-action sky,

tinting our image a bit.


**Lesson 5 Compositing 3D with USD** **179**


**6** At the top of the Inspector, drag the Eyedropper tool into the viewer to sample the

orange sky.


We can adjust the brightness of the dragon by lowering the Exposure and ensuring it

doesn’t appear too shiny and metallic by decreasing the Specular response slightly.

**7** In the Inspector, lower the Exposure until the dragon appears more naturally in the

scene, and then decrease the Specular Response to take off some of the shine (this will

be a very small amount).


The last step will be to align the texture of the dome light with the brightest part of it,

illuminating the dragon as it turns to face the sun in our live-action shot.

**8** In the time ruler, drag the playhead to around frame 170, where the dragon is turning

around on the right side of the frame.


If we assume the sun is setting on the left of the frame, this is approximately when it

would illuminate our dragon the most.


**Lesson 5 Compositing 3D with USD** **180**


**9** Select the uMerge1 and press 1 to see it in the viewer.


The viewer displays the dragon with the 360-degree dome light visible in the scene.

Don’t worry about seeing the dome light; it’s just there to help you align the area of

the dome light where you want it.

**10** Select the Dome Light, click the Transform tab, and then slowly adjust the XYZ Rotation

in the Inspector until the dragon in viewer 2 is illuminated to a greater degree. Y

Rotation should have the most significant impact.


As you make these adjustments, remember that the dome light isn’t meant to brighten

the dragon like a spotlight. The positioning of the dome light is subtle, just to get the

brightest part aligned with our dragon’s position.

##### **Faking Translucency with Area Lights**


While the dome light works for general lighting, we can use some neat lighting trickery to

make the dragon’s wings appear more translucent. By adding two disk lights, we can

illuminate the underside of the dragon’s wings so they appear lighter at appropriate times.

**1** Select the uMerge1 node and then add a uDisk Light.


A Disk Light is an area light shaped like a flat circular disk that emits light not from a

point, like a spotlight or point light, but across its surface. If you are familiar with

real-world lighting for film or photography, think of it like a softbox.


**Lesson 5 Compositing 3D with USD** **181**


**2** In the time ruler, move to frame 50.


At this point, if the sun is off to the left, a dragon’s thin wings would be semi
translucent, and they would appear a bit lighter at this point. Let’s focus the disk light

to do that.

**3** With the uDisk Light selected, in the Inspector, once again drag the Color Eyedropper

into viewer 2, but this time select the brightest areas of the dragon’s wing.


Now we need to focus the light toward the dragon. The easiest way is to use the Target

controls for the light.

**4** In the Inspector, click the Transform tab and, in the Pivot category, enable the Use

Target checkbox to reveal the target parameters. Then drag the Pick button into viewer

2 and select the dragon.


**Lesson 5 Compositing 3D with USD** **182**


The Disk light is a local light that’s not very strong by default, so we need to increase

the Exposure.

**5** Enter **15** for the Exposure value, and then use the slider to decrease the value a bit

until the wings are illuminated but not blown out.

**6** Drag the Specular Response down to 0.0 to ensure the light looks dull as if coming

through the skin.

**7** Finally, to soften the edges of the light cone, increase the Shaping Focus and lower the

Shaping Cone Angle to create a softer falloff. You can check the shape of the light by

dragging through the time ruler to view where the cone of the light ends.


Once you’ve tweaked the light, between frames 30-60 as the dragon banks around the

corner, the disk light should give the appearance of subsurface lighting for the wings.


Now we need to create a similar lighting setup for the range between frames 250 and

the end of the clip, where the dragon comes around the front of the Observatory. We

can use a shortcut by duplicating the disk light we have and repositioning it so that it

focuses on the dragon’s new location.


**Lesson 5 Compositing 3D with USD** **183**


**8** Move the time ruler to frame 275. This is a good representative frame for us to use to

set up our new light.


**9** Select the uDisk Light and copy it (Command-C on macOS, Ctrl-C on Windows).

**10** Click in an empty area of the Node Editor next to the uDisk Light node and paste the

new uDisk Light node.


**11** Connect the new uDisk Light 2.1 to the uMerge node.


To better understand where to position the new light, we can view our scene

from above.

**12** In viewer 2, right-click over the axis control and choose Top.


**Lesson 5 Compositing 3D with USD** **184**


**13** The view is zoomed in too far by default, so hold the Command (MacOS) or Ctrl

(Windows) key and scroll the middle mouse button to zoom out until you can see the

dragon from the top view.


**14** Select the uDisk Light 2.1 in the Node Editor and click the Transform tab in the

Inspector. Then drag the Z Transform dial to the right until the light moves just beyond

the dragon in viewer 2. The value will be somewhere around 60.


**Lesson 5 Compositing 3D with USD** **185**


**15** Return to any of the controls you adjusted for the first uDisk Light node and revisit

their settings until you are pleased with the results.

**16** When you are done tweaking the second uDisk Light, return viewer 1 to

Perspective view.


With our USD lights now matching the live-action sunlight, you’ve successfully bridged the

gap between digital and reality by fine-tuning the ambient lighting of our dragon and

strategically placing disk lights to enhance realism in the composite.
## **Creating a Flight of Dragons**


These days, one dragon doesn’t scare anyone—we need a group, or “flight,” to make an

impact. The easiest way to create multiple, slightly varied dragons is by using the

uDuplicate node, which makes copies of any USD element. Each copy can have its own

tweaks in position, timing, or size for a less robotic look.


However, we need to be careful where we place the uDuplicate node. If it comes after both

transforms, each dragon copy would offset away from the center, and their paths won’t

circle the observatory. By placing it between the two transforms, each dragon starts with its

own slight variation while still following a single circular path centered on the observatory.


NOTE We again suggest you follow the uDuplicate node values closely. The

detailed mask we add later in this lesson assumes the dragons fly a specific route.


**1** Select the uTransform1, press Shift-Spacebar, and search for and add a uDuplicate

node to the Node Editor.


Now we can make five dragons and offset them in time and space.


**Lesson 5 Compositing 3D with USD** **186**


**2** With the uDuplicate node selected, in the Inspector, set the Last value for the number

of copies to **5** .


**3** Set the Time Offset to 8 for an 8-frame cumulative offset between each copy. This will

ensure the first copy will move forward 8 frames into the animation at the start of our

comp, and the second copy will move 16 frames forward into the animation at the start.


TIP To delay the animation between copies, enter a negative value for the

Time Offset.


**Lesson 5 Compositing 3D with USD** **187**


**4** To offset each copy in space, set the X Offset Translation to -250 so the copies fly in

front of the original, set the Y to 5, so each copy is a bit higher in the frame, and set Z

to -250 so each copy is farther away from the observatory as they circle.


Even with all the offset parameters, the dragons’ timing and position might still seem

too evenly distributed. The Jitter tab lets you add randomness to the timing, position,

and size of the copies. By entering a Random Seed value, you generate a unique

starting point for this randomness, giving each dragon a more natural, less

calculated look.

**5** In the Inspector, click the Jitter tab and then click the Reseed button to set a

random value.


**Lesson 5 Compositing 3D with USD** **188**


**6** Set the Time Offset to 20.0.

**7** Enter X Offset: 150, Y: 10, and Z: 150.

**8** So that each copy has a slightly different Size, enter .125.

**9** Drag through or play the comp to view the animation.


The dragons never fly behind the observatory, which breaks the realism in this shot.

We’ve created a rather sophisticated mask so you don’t have to do any rotoscoping

and keyframing to create this part of the illusion. The mask will be enabled when we

want the dragons behind the building and will become transparent when they

fly in front.

**10** Open the media pool and drag the Dome mask from the Masks bin to an empty place

in the Node Editor under the Merge node.


**Lesson 5 Compositing 3D with USD** **189**


**11** Drag the output of the MediaIn2 node (the Dome mask) to the blue mask input on the

Merge1 node.

**12** Drag through or play through the composite to see the mask at work.


You’ve transformed a solitary USD dragon into a menacing group that soars with coordinated

chaos. Even though this may look great, don’t be afraid to return to lighting or textures and

try to improve them. Visual effects compositing is almost never a “set-it-and-forget-it” process.
## **Using Z Depth in Color Correction**


The live-action shot has some atmospheric haze on the mountains in the background. To

simulate the same haze effect on our dragons, we’ll use the Z channel to add fog depth.

This technique will make far-off dragons appear less saturated and more naturally

integrated into the scene. Then, we will layer some traditional color correction on top of

that to perfectly blend the live action with our dragons.

**1** Select the uRenderer node, and in the Aux Channels section, enable the Z checkbox.


In 3D graphics, the Z channel is like a map showing how far each object is from the

camera. Fusion’s uRenderer and its standard Renderer3D node can generate a Z

channel by calculating the distance from the camera to objects in the scene. The

farther away an object is, the higher the value in the Z channel. This information can be

used to create effects in conjunction with nodes that support Z channels, like Fog.


**Lesson 5 Compositing 3D with USD** **190**


**2** With the uRenderer selected, press Shift-Spacebar and add a Fog node to the

Node Editor.


Fusion actually has three methods for creating fog. The Fog node we are using here is

the simplest of the three, and it works as a 2D process, so it is relatively quick. You

begin by setting near and far planes. These planes define the range of where the fog

effect kicks in. The Z Near Plane defines the closest distance where fog starts to

appear. Anything closer remains clear.

**3** View the Fog node in viewer1 and the uRenderer in viewer2.


This viewer setup will make it easier to set properties of the fog while still seeing

the dragons.

**4** Move to frame 200 in the render range, where the dragon just finishes coming around

the observatory.


**Lesson 5 Compositing 3D with USD** **191**


**5** Drag the Z Near-plane slider to the left until the dragon is faintly seen through the fog

(around -250).


**6** Move to frame 50 in the render range, where all five dragons are seen in the frame.


This is a good frame to set the Z Far since the dragons are as far away from the camera

as they will get.

**7** Drag the Z Far-plane slider to the left until you see one dragon appear faintly,

around -500.


At this point, only the dragons farther away are deep in the fog, so the density seems

about right. Let’s now focus on the fog’s appearance.


The fog has a fairly fake, flat gray-purple color, and our scene has a warmer tone. To

correct the color and flatness of the fog, you usually generate a texture for it using a

Noise generator.


**Lesson 5 Compositing 3D with USD** **192**


**8** Click in an empty area of the Node Editor off to the right of the Fog node, press

Shift-Spacebar, and add a FastNoise node.


**9** Press 1 to see the FastNoise node in the viewer.


The FastNoise node generates random, natural-looking patterns that you can use

as textures. It’s ideal for creating varying thicknesses of fog. The default patchiness

of the noise will work for our fog, but we can enhance it by creating a color gradient in

the Inspector.


**Lesson 5 Compositing 3D with USD** **193**


**10** Click the Color tab in the Inspector.

**11** Create a pale orange color for Color1 in the Inspector and a pale gray-blue for Color 2.


This will simulate the sunlight reflecting on the cool pale blue of the fog mist.

**12** Drag the output of the FastNoise to the green Fog input on the Fog node.

**13** Select the Merge1 node and press 2 to view it.


Now we have a much more pleasing fog look, but it covers the entire screen, and we

only need it to affect our dragons.

**14** Drag a second output of the uRenderer into the Effect Mask input of the Fog node.


**Lesson 5 Compositing 3D with USD** **194**


If you scrub through or play the composition, you’ll notice that the fog nicely enhances

the distant dragons and gradually fades as the main dragon circles toward the front.

However, the fog is too dense, so we need to increase its transparency by adjusting

its opacity.

**15** Select the Fog node, and in the Inspector, lower the Fog Opacity to about 0.2.


That has made the fog less dense, but now the dragons are too bright and almost

ghost-like. Using a brightness contrast node, we can have more control over the

dragons’ tonality.

**16** With the Fog node selected, press Shift-Spacebar and add a BrightnessContrast node.

**17** In the Inspector, lower the Gain, Gamma, and Saturation. Then raise the Lift until the

dragons blend well into the scene.


**Lesson 5 Compositing 3D with USD** **195**


##### **Correcting Alpha Channels**

After making your tonal changes, you will notice you adjusted the entire image, including

the background! This happens because you’re adjusting color values on an image with a

premultiplied alpha channel, leading to what’s called an alpha premultiplication issue.


Normally, you might use the Pre-Divide/Post Multiply checkbox in a color node to fix this.

However, when you have two or more color adjustments in a row, a clearer solution is to

add explicit Alpha Divide and Alpha Multiply nodes before and after your color corrections.

**1** Select the uRenderer node and press Shift-Spacebar to add an Alpha Divide node.


This node converts your premultiplied alpha to a straight alpha, making color

adjustments cleaner around the edges. However, now you must convert the straight

alpha back to a premultiplied alpha, ensuring perfect edges for the Merge node.


**Lesson 5 Compositing 3D with USD** **196**


**2** Select the BrightnessContrast node, press Shift-Spacebar, and add an

AlphaMultiply node.


Now you have the color correction you need on the dragons with perfect premultiplied

alpha channel edges as desired by the Merge node.
## **Finishing the Comp**


There are always a few final touches you can add to the scene. Whenever you have motion,

you probably want to add some motion blur for more realism. That’s the final touch we will

add to this comp.

**1** Select the uRenderer node in the Node Editor.


**Lesson 5 Compositing 3D with USD** **197**


You might recall from the first exercise in this book that the Renderer 3D contains

Motion Blur controls. When dealing with USD scenes, motion blur is handled in the

uRenderer node.

**2** Select the Settings tab in the Inspector and enable the Motion Blur checkbox.


The initial Motion Blur settings are set to low quality. As you increase the quality, the

performance in your comp will decline. It’s a delicate balancing act between quality

and performance.

**3** In the Inspector, set the Quality level to 4.


In this final lesson, you’ve turned a single dragon into a fearsome flight of dragons using a

few of Fusion’s Universal Scene Description tools. Throughout this training guide, you’ve

explored everything from basic 3D placement and camera tracking to lighting, shaders,


**Lesson 5 Compositing 3D with USD** **198**


and particle effects. With this foundation, you now have the skills to create dynamic,

cinematic composites. Congratulations. Now go bring your creative visions to life!


Completed node tree for Lesson 5

## **Lesson Review**

**1** True or False? USD stands for “Universal Scene Description” and is used to organize

and manage complex 3D scenes.

**2** What is a “prim” in USD?

**a)** A basic unit representing an object or element in the scene

**b)** A type of shader

**c)** A color correction tool

**d)** A lighting effect

**3** True or False? You can use either a Renderer3D or a uRenderer to convert a USD scene

into a 2D image.

**4** Which node converts a premultiplied alpha image to a straight alpha image for more

accurate color adjustments?

**a)** Alpha Multiply node

**b)** Alpha Divide node

**c)** Transform node

**d)** uRenderer node

**5** True or False? A Transform node can be used to orient a USD element and set its

rotation axis.


**Lesson 5 Compositing 3D with USD** **199**


##### **Answers**

**1** True. USD stands for “Universal Scene Description” and is used to organize and

manage complex 3D scenes.

**2** a) A basic unit (or “primitive”) representing an object or element in the scene

**3** False. You can only use a uRenderer to convert a USD scene into a 2D image.

**4** b) Alpha Divide node

**5** False. A uTransform node must be used to orient a USD element and set its

rotation axis.


**Lesson 5 Compositing 3D with USD** **200**


## **Index**

**NUMBERS**

2D and 3D, merging, _86–92_

2D composite, combining 3D
scene into, _73_

2D versus 3D compositing tools, _6_

3D, converting into 2D image, _33–39_

3D camera tracking

exporting scenes, _147–153_

masking for, _130–138_

matching color and light, _156–159_

objects in 3D se, _153–156_

preparing camera tracker, _138–142_

refining solve, _144–146_

solving for camera, _142–143_

3D coordinate system, _148_

3D ground plane, hiding, _170_

3D objects, changing translation controls
for, _25_ . _See also_ _objects_

3D particles. _See also_ _particle cells_

adding motion, _117–119_

generating, _113–117_

3D scenes. _See also_ _scenes_ ; _USD (Universal_
_Scene Description)_

adding lights, _26–32_

camera setup, _19–26_

combining into 2D composite, _73_

moving views of, _11–12_

navigating in, _8–13_

panning, _12_

placing elements in, _2–7_

rotating around, _12_

zooming in and out, _12_

3D sets, positioning objects in, _153–156_

3D space, moving images in, _9_

3D text. _See also_ _Text3D_

adding depth to, _16_

fitting into viewer, _16_

moving, _16_

resizing, _16_

using, _14–18_



3D tracking, masking for, _130–138_

3D viewer, key and mouse
combinations, _12_

3D windshield reflection, Merge
nodes, _72–73_

**A**

Aligned button, _152_

alpha channel. _See also_ _Combine Alpha_

correcting, _196–197_

viewing, _70_

AlphaMultiply node, adding, _197_

Alt key. _See_ keyboard shortcuts

Ambient Light, adding, _27–28_, _32_, _34_

Angle, adjusting, _118_

Angle Start, dragging in Inspector, _74_

animating camera moves, _23–26_

animation between copies, delaying, _187_

area lights, faking translucency with,

_181–186_ . _See also_ _lights_ ; _natural_
_light spill_

aspect ratio, retaining, _5_

Auto Track button, _141_

Aux Channels section, _190_

axis control, locating, _13_

**B**

Background Alpha channel, _111_

backup versions, accessing, _92_

Backups bin, _147_

BeachGshape, _135_

bins. _See also_ _Timelines bin_

creating Fusion compositions in, _3_

Wildlife Assets, _4_

Bitmap node, _140_

Blackmagic Cloud Store, _xviii_

Blackmagic Design Training and
Certification Program, _ix_

Blend slider, _158_

Blender, _165_


**Index** **201**


Blur node, _71_

Blur size, increasing, _107_

Boolean operators, _111_

Bricks00001.exr file, _94_

brightness, controlling, _27_

BrightnessContrast node, _197_

**C**

Cache folder, _103_

camera

refining solves, _144–146_

setting up, _19–26_

solving for, _142–143_

camera move, animating, _23–26_

Camera RAW files, working with, _44_

Camera Tracker, preparing, _138–142_

Camera3D1 setting, _90_

certification, getting, _ix–x_

channels, viewing, _49_

Chrome template, using, _17–18_

Cineon Log node, adding, _46_

clip speed, changing, _77_

clouds, resizing, _90_

color, managing for visual effects, _42–48_

color and light, matching, _158–159_

color channels, viewing, _51_

color correction

in Fusion, _109–113_

using Z depth in, _190–197_

Color Management category, _44_, _46_

“Color processing mode, _44_

“Color science” menu, _44_

color space. _See_ _linear color space_

Color tab, _194_

ColorCompressor1, _157_

ColorCorrector2, _123_

Combine Alpha, _111_ . _See also_ _alpha channel_

Combine Operator modes, _111_

combining mattes, _137–138_

Command key. _See_ _keyboard shortcuts_



comp

finishing, _197_

playing, _118_

compositing. _See_ _Fusion Comps bin_

Compositing with USD.dra, _162_

compositing 3D with USD. _See also_ _USD_
_(Universal Scene Description)_

creating flight of dragons, _186–190_

creating surfaces with shaders, _166–171_

finishing comp, _197–199_

making dragon fly, _174–177_

matching lights to scenes, _177–186_

Z depth in color correction, _190–197_

Compress Hue slider, _157–158_

Compress Luminance slider, _157–158_

Compress Saturation slider, _157–158_

connection lines, adding routers for, _28_

control point, adding to Saturation curve,
64. _See also_ _Select All Points button_

Controls tab, Inspector, _117–118_

coordinate system, origin point of, _9_

Copy command, _184_

Ctrl key. _See_ _keyboard shortcuts_

**D**

Darken Apply mode, _93_

DaVinci Resolve _20_

downloading, _x_

setup, _xi–xvii_

DaVinci YRGB Color Managed, _44_, _48_ .
_See also_ _RGB image_ ; _sRGB output_
_color space_

Delete button, _99_

Delta Keyers. _See also_ _mattes_

adding to Noise Reduction node, _52–62_

use of, _62_

depth axis (Z), _148_

depth-of-field effects, configuring, _35–39_ .
_See also_ _Effects Library_ ; _visual effects_

Detection Threshold, _140_

Difference Keyer, adding, _67_

diffuse color, _167_

Directional Light, _32_, _34_


**Index** **202**


Disk Light, _181–183_

DNxHR HQ codec, _78_

DoF (depth of field), _21_

dolly-in move, creating, _23–26_

Dome mask, _189_

downloading

DaVinci Resolve, _x_

lesson files, _xvii_

dragon model, frames of animation in, _164_

dragons

creating flight of, _186–190_

flying, _174–177_

**E**

edit page, auto stabilizing, _75–78_

Effects Library. _See also_ _depth-of-field_
_effects_ ; _visual effects_

opening and closing, _5_

Underlay tool, _91–92_

Elephant bin clip, _8_

Elephant Image Plane 3D, _23_

Elephant’s Image Plane 3D node, _10_

Erode/Dilate parameter, decreasing, _57_

exporting scenes, _147–153_

Exposure, lowering, _180_

EXR, rendering out clean frames as, _51_

extrusion parameters, opening, _16_

Eyedropper tool, _157_, _180_

**F**

F keys. _See_ _keyboard shortcuts_

FastNoise node, _193_

Flow category, _91_

focal length, entering for camera
track, _141_

Focal Plane, enabling visibility for
camera, _21–22_

Fog node

adding, _191_

selecting, _195_

Foreground Alpha, _111_

Foreground bin clip, _8_



Foreground Image Plane 3D, _23_

Fusion 20 3D Dry4Wet.dra file, opening, _86_

Fusion clips, limitation to timeline
resolution, _45_

Fusion Comps bin, _3_

Fusion page, entering, _46_

Fusion20Camera tracking.dra,
restoring, _131_

Fusion20DeltaKeyer.dra file, opening, _43_

**G**

Gain slider, _57_, _110_

Gamma, lowering, _110_ . _See also_

_linear gamma_

gamut node, adding, _46_

Giraffe graphic, _5_

Giraffe Image Plane 3D, _23_

GIRAFFE’s Image Plane 3D node, _10_

GPU resources, freeing up, _51_

GreenScreen node, creating, _48_

green-screen workflow

3D windshield reflection, _72–82_

adding natural light spill, _67–72_

managing color and visual effects, _42–48_

pulling keys, _51–56_

removing noise, _48–51_

ground plane, _117_

ground plane, hiding, _170_

Group node, identifying, _18_ . _See also_

_Node Editor_

**H**

Hardware Render Type, _90_

Hardware renderer, _34_

HDR setting, _44_

hiding 3D ground plane, _170_

High threshold, using with Difference
Keyer, _68–69_

Highlights, Range menu, _112_

horizontal axis (X), _148_

hue, saturation, and luminance, _157–158_

Hue Curve node, adding to Node Editor, _63_


**Index** **203**


**I**

illumination materials, applying, _17–18_

Image Plane 3D node

adding to Node Editor, _6_

positioning elements, _23_

resizing elements, _9_

versus Shape 3D node, _5_

images

blending, _106–107_

fitting into viewer, _51_

moving in 3D space, _9–10_

removing from viewer, _114_

renaming, _5_

using for particle cells, _120–122_

importing

with loaders, _93–97_

textures, _167_

USD into Fusion, _162–165_

Inspector

Controls tab, _117–118_

Region tab, _122_

Transform tab, _7_

interface, restoring to default state, _3_

**J**

Jitter tab, _188_

**K**

key and mouse combinations, _12_

keyboard shortcuts

adding routers for connection lines, _28_

Copy command, _184_

fitting images into viewer, _51_

Fusion page, _46_

Matte Control node, _65_

Merge node, _70_

Overwrite edit button, _76_

playhead movement, _134_

rotating perspective angle, _5_

keyers. _See_ _Delta Keyers_ ; _Difference Keyer_

keyframe, setting for animation, _24_

keys. _See_ _pulling keys_



**L**

Latitude End, _75_

lens distortion, _141_

lesson files, downloading, _xvii_

Lifespan parameter, setting for
particles, _119_

light and color, matching, _158–159_

light cone, softening edges of, _183_

lights. _See also_ _area lights_ ; _natural light spill_

adding, _26–32_

matching to scenes, _177–186_

light-wrap technique, _67–72_

linear color space, using, _47–48_

linear gamma, converting footage to,

_43–44_, _46–48_ . _See also_ _Gamma_

Lion bin clip, _8_

Lion Image Plane 3D, _23_

LION’s Image Plane 3D node, _12_

Loader node, _51_

loaders, importing with, _93–97_

LOG format, _44_

LOG gamma, _47–48_

luminance, hue, and saturation, _157–158_

LUT (lookup table), enabling in viewer, _46_

**M**

macOS quick setup, _xi–xvii_

Magic Mask

creating mattes with, _136–137_

tracking data, _103_

Magic Mask node, _97–104_

magic masks, creating, _97–104_

main_dragon.usd, _164_

Mask tab, _63_

masking for 3D tracking, _130–138_

masks. _See also_ _Magic Mask node_

correcting, _104_

creating, _97–104_

embedding into rooftop clip, _94–95_

masks and adjustments, evaluating, _65_

Master bin, contents of, _131_

master_dragon_asset folder, _164_


**Index** **204**


materials, applying to 3D text, _17–18_

Matte Control node, _65_, _94–96_

Matte tab

making adjustments in, _102_

selecting, _57_

MatteControl, adding to Node Editor, _110_

mattes. _See also_ _Delta Keyers_

combining, _137–138_

creating, _132_

creating with Difference Keyer, _68_

creating with Magic Mask, _136–137_

Maximum Track Error, _145_

Maya environment, _165_

measurements, _152_

Media Pool button, _4_

merge, displaying in viewers, _31_

Merge 3D node

contents of, _14_

inputs, _8_

Merge node

adding and viewing, _70_

versus Merge 3D node, _6_

Merge tool, _6_

Merge3D1, disconnecting from
Merge3D2, _31_

merging 2D and 3D, _86–92_

metric system, _152_

MM (MultiMerge) node, _94–95_

motion, adding, _117–119_

motion blur, applying to rain
simulation, _125_

Motion Blur checkbox, _198_

mouse and key combinations, _12_

moving

3D text, _16_

images in 3D space, _9–10_

views of 3D scenes, _11–12_

MultiPoly tool, adding, _132_

**N**

natural light spill, adding, _67–72_ . _See also_

_area lights_ ; _lights_



Neural Engine, using with Magic
Mask, _97_, _100_

Node Editor. _See also_ _Group node_

adding Image Plane 3D to, _6_

adding nodes to, _15_

MediaIn1 node, _4_

Save Default setting, _38_

Node Selection tool, _156_

nodes

particle-specific, _114_

reorganizing, _48_

noise, removing, _48–51_

Noise Reduction node

adding, _50–51_

adding Delta Keyers to, _52–62_

Number setting, using with
particles, _118–119_

**O**

objects. _See also_ _3D objects_

positioning in 3D sets, _153–156_

repositioning in space, _7_

occlusion map, _169–170_

Option key. _See_ _keyboard shortcuts_

orientation, Set from Selection, _149_

Overwrite edit button, _76_

**P**

panning in 3D viewer, _12_

parallax, _131_

particle cells, using images for, _120–122_ .
_See also_ _3D particles_

particles, rendering and compositing,

_123–126_

PATCHED FOREGROUND Underlay, _104_

pBounce node, _114_

pEmitter node, _113–115_, _117_, _122_, _124_

performance, increasing, _114_

perspective angle, rotating, _5_


**Index** **205**


Perspective view

returning to, _117_

returning to default angle, _13_

Photoshop textures, _165_

PirateShip.png, _153_

Play button, _118_

playhead, moving, _134_

Point Light, _32_

polygon, reshaping, _134_

Polygon List, adding shape to, _135_

Polyline shape, _56_

pRender node, _113_, _123_, _126_

primitives, replacing textures on, _170–171_

Project Manager, adding projects to, _3_

projection mapping, _78–82_

ProRes4444 file, converting to, _49_, _78_

pSpawn node, _114_

pulling keys

adding Delta Keyers, _52–62_

beginning process of, _51–54_

handling spill suppression, _62–66_

**Q**

Quality level, setting, _198_

**R**

Rain Drop.png, dragging to Node
Editor, _120_

rainy day

adding reflections, _105–108_

creating color in Fusion, _109–113_

creating mask, _97–104_

generating 3D particles, _113–126_

merging 2D and 3D, _86–92_

sky replacement, _92–97_

Range menu

Highlights, _112_

Shadows, _112_

RAW files. _See_ Camera RAW files

RCM (Resolve’s color management), _44_

rectangle, rotating, _116_

rectangular shape, _56_



REFLECTION Underlay name, _108_

reflections, adding, _105–108_

Regenerate All button, _103_

Region tab, Inspector, _122_

renaming images, _5_

Render button, _78_

Render in Place, _77–78_

Renderer 3D Inspector, Enable
Accumulation Effects, _35_

Renderer 3D node, contents of, _34_

Renderer 3D output, displaying in
viewer _2_, _33_

Renderer3D node, _74_

Reseed button, _188_

Reset UI Layout, _3_

resizing elements, _9_

Restore Project Archive, _3_, _42_, _131_

Reverse Speed, _77_

RGB image, viewing, _70_ . _See also_ _DaVinci_
_YRGB Color Managed_ ; _sRGB output_
_color space_

RocksGshape, _134_

ROOF mask, _111_

Rooftop node, _92_

rotating in 3D viewer, _12_

rotating perspective angle, _5_

rotation wheels, switching onscreen
controls to, _29–30_

roughness and shading, adding, _168–170_

router for connection lines, adding, _28_

**S**

saturation

hue and luminance, _157–158_

lowering, _109_

Saturation curve, adding control
point to, _64_

Saver node, using with Noise
Reduction node, _51_

scale, defining for scenes, _150–153_

Scale, using to resize elements, _9_

scale parameter, _90_

SceneryGshape, _135_


**Index** **206**


scenes, exporting, _147–153_ . _See also_ _3D_
_scenes_ ; _USD (Universal Scene_
_Description)_

SDR sRGB setting, _44_

Select All Points button, _133–134_ . _See also_

_control point_

Select Tool dialog, _132_

Set from Selection button, _151_

shaders

applying, _17–18_

creating surfaces with, _166–171_

shading and roughness, adding, _168–170_

Shadows, Range menu, _112_

Shape 3D node versus Image Plane 3D, _5_

Shape Animation auto, _133_, _135_

Shape Box, _134_

Shape3D, adding to
node graph, _73–74_, _154–155_

Shaping Focus, increasing, _183_

Shift key. _See_ _keyboard shortcuts_

sky replacement, patching together, _92–97_

SKY Underlay name, _92_

Software renderer, _34_

Solid Replace Mode, setting to Source, _63_

solve, refining, _144–146_

Solve button, _142_

Spatial NR menu, displaying, _50_

Sphere, choosing from Shape menu, _74_

spill suppression, handling, _62–66_

Spline Editor

opening, _25_

Smooth button, _26_

Spot Lights, adding, _28–32_

sRGB output color space, _45_ .
_See also_ _DaVinci YRGB Color_
_Managed_ ; _RGB image_

Stabilize parameters, opening
in Inspector, _77_

Stabilized Road clip, creating, _78_

starting keyframe, setting for
animation, _24_

Storm rendering engine, _172_

StormClouds image, _89_



stroke, deleting, _99_

Sunset HD graphic, _4_

SUNSET node, _5_

surfaces

applying shaders to, _17–18_

creating with shaders, _166–171_

system requirements, _x_

**T**

temporal threshold, increasing, _50_

text. _See_ _3D text_

Text3D, applying materials to, _17–18_ .
_See also_ _3D text_

textures, importing, _167_

textures on primitives, replacing, _170–171_

Threshold parameters, _57_

Time ruler render range, moving to
frames in, _24_

Timelines bin, contents of, _2_, _14_ .
_See also_ _bins_

tools. _See_ _Select Tool dialog_

Track Reverse button, _100–101_

tracking point, selecting, _151_

Transform node, _105_, _107–108_, _176_

Transform tab, Inspector, _7_

translucency, faking with area
lights, _181–186_

typeface, setting, _16_

**U**

uDisk Light, copying, _184_

uDome light node, _179_

uDuplicate node, _186–187_

uLoader node, _164_

uMerge node, _171_

Unaligned button, _148_

Underlay, adding around nodes, _104_

Underlay tool, adding to Node
Editor, _91–92_

units of measurement, _152_

uRenderer node, _172–173_, _191_, _197_

uReplaceMaterial node, _170–171_, _174_

uReplaceMaterial tool, _166_


**Index** **207**


USD (Universal Scene Description), _161_ .
_See also_ _3D scenes_ ; _compositing 3D with_
_USD_ ; _scenes_

adding roughness and shading, _168–170_

bias, _168_

Browse button, _167–169_

creating flight of dragons, _186–190_

creating surfaces with shaders, _162–165_

finishing comp, _197–199_

importing into Fusion, _162–165_

making dragon fly, _174–177_

matching lights to scenes, _177–186_

occlusion map, _169–170_

overview, _161–162_, _165_

rendering, _171–173_

replacing textures on primitives, _170–171_

Screen Tree window, _171_

using Z depth in
color correction, _190–197_

uShader nodes, _166_, _169_

uTexture node, _166–168_

uTransform node, _174_

**V**

Vector Motion Blur, adding to Node
Editor, _125–126_

Velocity section, Inspector, _118_

vertical axis (Y), _148_

viewing perspective, changing, _12_

visual effects, managing color for, _42–48_ .
_See also_ _depth-of-field effects_ ;
_Effects Library_



**W**

WILDLIFE CONSERVATION
Styled Text, _15_, _18_

Wildlife Open clip, creating, _3_

Windows quick setup, _xi–xvii_

windshield simulation, _72–73_

Workspace menu, Reset UI Layout, _3_

**X**

X axis, _9_, _148_

X rotation, _116_

X Translation, _10_

**Y**

Y axis, _9_, _148_

Y Offset Translation value, _117_

Y translation, using to position
elements, _23_

**Z**

Z animation curve, displaying for
camera, _25_

Z axis, _9_, _148_

Z channel, 190

Z depth, using in color correction, _190–197_

Z Far-plane slider, _192_

Z Near-plane slider, _192_

Z translation values, entering, _7–8_

zooming in and out in 3D viewer, _12_


**Index** **208**


**This page is intentionally left blank ﻿** **209**


Post production, especially visual effects, is constantly evolving
with exciting new tools and techniques. Whether you’re an editor,
colorist, or motion artist, keeping up means diving into the world
of 3D compositing. With DaVinci Resolve Studio, powerful features
like 3D camera tracking and Universal Scene Descriptor (USD)
nodes make the transition from 2D to 3D easier than ever.


This training guide gives you a practical, hands on introduction to
advanced tools and techniques in the Fusion page, highlighting
its seamless 3D integration. You’ll discover how to import 3D
models, create breathtaking particle effects, and seamlessly add
realistic 3D elements to live action footage–all with the control
and precision you need. These lessons will help you unlock
Fusion’s 3D capabilities and create stunning visuals that redefine
the boundaries of 2D and 3D. It’s time to take your creativity to
the next level with the tools shaping the future of visual effects.


**What You’ll Learn**

- Proficient compositing with nodes

- Enhance live action environments with 3D particles

- Use multiple keyers for advanced green screen keying

- Use Magic Mask to save time rotoscoping

- Work seamlessly with 3D assets

- Set up 3D scenes with cameras, lights and depth of field.


**Who This Book Is For**

This book is designed for editors, colorists and artists with
some basic knowledge of Fusion in DaVinci Resolve Studio.
Although the lessons assume some knowledge of Fusion’s
node based interface, you will find clear and concise lessons
that introduce how Fusion works with 3D data as well as some
more sophisticated 2D compositing techniques.



**Advanced Green-Screen Compositing**


**3D Camera Tracking**


**Generate 3D Particles**


**Import and Integrate 3D USD Data**


