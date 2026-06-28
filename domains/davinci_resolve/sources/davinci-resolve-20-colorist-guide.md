<!-- TOC
- Contents (p.4)
- Foreword (p.8)
- Acknowledgments (p.9)
- About the Author (p.9)
- Who This Book Is For (p.10)
- Getting Started (p.10)
- Interface Review (p.21)
  - Color Page Layout (p.21)
  - Viewer (p.23)
  - Primaries Color Wheels (p.24)
  - Palette Panel (p.25)
  - Introducing Blackmagic Cloud (p.26)
- Part I – Color Correcting a DaVinci Resolve Timeline (p.27)
- Balancing Footage (p.29)
  - Opening a DaVinci Resolve Archive (p.30)
  - Setting Up Project Backups (p.32)
  - Understanding the Grading Workflow (p.34)
  - Primary Grading with Color Wheels (p.37)
  - Precision Grading with Curves (p.46)
  -  Comparing Color and Log Wheels (p.54)
  - Self-Guided Exercises (p.68)
  - Lesson Review (p.69)
- Creating Color Continuity (p.71)
  - Building a Shot-Matching Strategy (p.72)
  - Organizing Shots Using Flags and Filters (p.74)
  - Applying Shot Match (p.78)
  - Matching Shots Using Stills (p.80)
  - Comparing and Matching Shots Manually (p.87)
  - Self-Guided Exercises (p.96)
  - Lesson Review (p.97)
- Correcting and Enhancing Isolated Areas (p.99)
  - Controlling the Viewer’s Eye (p.100)
  - Sharpening Key Elements (p.110)
  - Fixing Overcast Skies (p.118)
  - Warping Color Ranges (p.134)
  - Enhancing Skin Tones with Face Refinement (p.144)
  - Adjusting Skin Tones Manually (p.155)
  - Self-Guided Exercises (p.164)
  - Lesson Review (p.165)
- Part II – Managing Nodes and Grades (p.167)
- Conforming an XML Timeline (p.169)
  - Importing an XML Timeline (p.170)
  - Syncing an Offline Reference (p.177)
  - Conforming a Timeline (p.179)
  - Maximizing the Dynamic Range (p.194)
  - Lesson Review (p.205)
- Mastering Node Trees (p.207)
  - Understanding Node-Based Grade Compositing (p.208)
  - The Importance of Node Order (p.209)
  - Creating Separate Processing Branches with a Parallel Mixer Node (p.224)
  - Compositing Color Effects with the Layer Mixer Node (p.231)
  - Using External Mattes (p.242)
  - Self-Guided Exercises (p.248)
  - Lesson Review (p.249)
- Managing Grades Across Clips and Timelines (p.251)
  - Working with Versions (p.252)
  - Appending Grades and Nodes (p.261)
  - Saving Node Tree Templates (p.265)
  - Saving Stills for Other Projects (p.272)
  - Migrating Timeline Grades Using ColorTrace (p.277)
  - Copying Grades Using the Timelines Album (p.282)
  - Self-Guided Exercises (p.284)
  - Lesson Review (p.285)
- Part III – Optimizing the Grading Workflow (p.287)
- Using Groups (p.289)
  - Preparing Media Using Scene Cut Detection (p.290)
  - Creating a Group (p.299)
  - Applying Base Grades at the Pre-Clip Group Level (p.303)
  - Making Clip-Specific Adjustments at the Clip Group Level (p.314)
  - Automatically Tracking People and Objects (p.321)
  - Creating a Unifying Look Using the Post-Clip Group Level (p.339)
  - Working with Lookup Tables (p.347)
  - Using the Timeline Level (p.359)
  - Self-Guided Exercises (p.366)
  - Lesson Review (p.367)
- Adjusting Image Properties (p.369)
  - Understanding Timeline Resolutions and Sizing Palette Modes (p.370)
  - Using Keyframes to Animate Grades (p.381)
  - Applying Noise Reduction (p.388)
  - Optimizing Performance with Render Cache (p.395)
  - Self-Guided Exercises (p.404)
  - Lesson Review (p.405)
- Setting Up Raw Projects (p.407)
  - Adjusting Raw Settings at the Project Level (p.408)
  - Adjusting Raw Settings at the Clip Level (p.415)
  - Grading High Dynamic Range Media (p.419)
  - Setting Up a Render Cache for Raw Media Projects (p.432)
  - Self-Guided Exercises (p.434)
  - Lesson Review (p.435)
- Delivering Projects (p.437)
  - Using Lightbox to Check Timelines Before Delivery (p.438)
  - Reviewing Projects with Clients (p.442)
  - Understanding the Render Workflow and Presets (p.449)
  - Creating Custom Renders (p.455)
  - Configuring a Timeline for Digital Cinema (p.457)
  - Exploring Advanced Render Settings (p.464)
  - Lesson Review (p.473)
- Appendix A – Using the DaVinci Resolve Panels (p.475)
- Appendix B – Setup and Delivery on Macs (p.481)
- Index (p.483)
-->
## The Colorist Guide to


**The Colorist Guide to DaVinci Resolve 20**


Daria Fissoun, CSI


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


ISBN 13: 979-8-9924874-1-1


## **Contents**

Foreword vii


Acknowledgments viii


About the Author viii


Who This Book Is For ix


Getting Started ix


Interface Review xx


Color Page Layout xx


Viewer xxii


Primaries Color Wheels xxiii


Palette Panel xxiv


Introducing Blackmagic Cloud xxv


Color Correcting a DaVinci Resolve Timeline 1


1 Balancing Footage 3


Opening a DaVinci Resolve Archive 4


Setting Up Project Backups 6


Understanding the Grading Workflow 8


Primary Grading with Color Wheels 11


Precision Grading with Curves 20


Comparing Color and Log Wheels 28


Self-Guided Exercises 42


Lesson Review 43


2 Creating Color Continuity 45


Building a Shot-Matching Strategy 46


Organizing Shots Using Flags and Filters 48


**Contents** **iii**


Applying Shot Match 52


Matching Shots Using Stills 54


Comparing and Matching Shots Manually 61


Self-Guided Exercises 70


Lesson Review 71


3 Correcting and Enhancing Isolated Areas 73


Controlling the Viewer’s Eye 74


Sharpening Key Elements 84


Fixing Overcast Skies 92


Warping Color Ranges 108


Enhancing Skin Tones with Face Refinement 118


Adjusting Skin Tones Manually 129


Self-Guided Exercises 138


Lesson Review 139


Managing Nodes and Grades 141


4 Conforming an XML Timeline 143


Importing an XML Timeline 144


Syncing an Offline Reference 151


Conforming a Timeline 153


Maximizing the Dynamic Range 168


Lesson Review 179


5 Mastering Node Trees 181


Understanding Node-Based Grade Compositing 182


The Importance of Node Order 183


Creating Separate Processing Branches with a Parallel Mixer Node 198


**Contents** **iv**


Compositing Color Effects with the Layer Mixer Node 205


Using External Mattes 216


Self-Guided Exercises 222


Lesson Review 223


6 Managing Grades Across Clips and Timelines 225


Working with Versions 226


Appending Grades and Nodes 235


Saving Node Tree Templates 239


Saving Stills for Other Projects 246


Migrating Timeline Grades Using ColorTrace 251


Copying Grades Using the Timelines Album 256


Self-Guided Exercises 258


Lesson Review 259


Optimizing the Grading Workflow 261


7 Using Groups 263


Preparing Media Using Scene Cut Detection 264


Creating a Group 273


Applying Base Grades at the Pre-Clip Group Level 277


Making Clip-Specific Adjustments at the Clip Group Level 288


Automatically Tracking People and Objects 295


Creating a Unifying Look Using the Post-Clip Group Level 313


Working with Lookup Tables 321


Using the Timeline Level 333


Self-Guided Exercises 340


Lesson Review 341


**Contents** **v**


8 Adjusting Image Properties 343


Understanding Timeline Resolutions and Sizing Palette Modes 344


Using Keyframes to Animate Grades 355


Applying Noise Reduction 362


Optimizing Performance with Render Cache 369


Self-Guided Exercises 378


Lesson Review 379


9 Setting Up Raw Projects 381


Adjusting Raw Settings at the Project Level 382


Adjusting Raw Settings at the Clip Level 389


Grading High Dynamic Range Media 393


Setting Up a Render Cache for Raw Media Projects 406


Self-Guided Exercises 408


Lesson Review 409


10 Delivering Projects 411


Using Lightbox to Check Timelines Before Delivery 412


Reviewing Projects with Clients 416


Understanding the Render Workflow and Presets 423


Creating Custom Renders 429


Configuring a Timeline for Digital Cinema 431


Exploring Advanced Render Settings 438


Lesson Review 447


A Using the DaVinci Resolve Panels 449


B Setup and Delivery on Macs 455


Index 457


**Contents** **vi**


## **Foreword**

**Welcome to The Colorist Guide to DaVinci Resolve 20.**


DaVinci Resolve 20 is the only post-production solution that combines editing, color

correction, visual effects, motion graphics, and audio post-production all in one software

tool! Its elegant, modern interface is fast to learn for new users yet powerful enough for

the most experienced professionals. DaVinci Resolve lets you work more efficiently

because you don’t have to learn multiple apps or switch software for different tasks. It’s

like having your own post-production studio in a single app!


DaVinci Resolve 20 adds editing with transcriptions from audio, film look creator and

ColorSlice six vector grading, IntelliTrack AI for panning audio to match vision, broadcast

replay for live multicamera broadcast editing, layout and replay with speed control, and so

much more!


Best of all, Blackmagic Design offers a version of DaVinci Resolve 20 that is completely free!

We’ve made sure that this version of DaVinci Resolve includes more features than any paid

editing system. That’s because at Blackmagic Design we believe everybody should have

the tools to create professional, Hollywood-caliber content without having to spend

thousands of dollars.


I invite you to download your copy of DaVinci Resolve 20 today and look forward to seeing

the amazing work you produce!


Grant Petty

Blackmagic Design


**Foreword** **vii**


## **Acknowledgments**

I’d like to express my deepest gratitude to Patty Montesion and Dion Scoppettuolo for

their mentorship in the early days of developing the Blackmagic Design training series. I

also want to acknowledge and give special thanks to Marc Wielage, Jim Robinson, Dwaine

Maggart, and every specialist who provides invaluable online support to colorists and

filmmakers worldwide.


I appreciate Peter Chamberlain and the entire DaVinci Resolve developer team for creating

incredible software that is a pleasure to teach. Thank you to Kaur Hendrikson for his

independent support and to every developer contributing to DaVinci Resolve’s third-party

plug-in and DCTL community.


A shout-out to Danielle Foster for her patience during layout and Dan Foster for keeping

the books fresh with every subsequent edit. And extra super special thanks to former

editor Bob Lindstrom for his attention to detail, patience, humor, and friendship

throughout the writing process.

##### **Video Materials**


Garth de Bruno Austin (Banovich Studios) for _Disunity_


Kauai Film Academy for _Too Much Life_ ( _[www.kauaifilmacademy.org](http://www.kauaifilmacademy.org)_ )


Sherwin Lau (Creative Media Institute, co-director) and Chris Lang (Organ Mountain

Outfitters, co-director) for Organ Mountain Outfitters promo materials


Aaron Walterscheid (Awal Visuals) and Nathan LeFever (LeFever Creative) from Organ

Mountain Outfitters ( _organmountainoutfitters.com_ )
## **About the Author**


**Daria Fissoun** is a colorist and compositor based in East London. She specializes in

commercial video projects (past clients include Microsoft, Nike, and Konami) and has

worked on US and UK feature productions, including a role as post-production engineer

on several Disney+ films.


Alongside industry work, Daria is also involved in the educational sector. She has been a

staff member (or guest lecturer) at film and media schools throughout London, including

SAE Institute London, MET Film School, Central Film School, The National Film and


**About the Author** **viii**


Television School (NFTS), and London South Bank University. She wrote a training series

for Nobe Omniscope and is a contributing author on Mixing Light. In her spare time, she

records and uploads video tutorials on post-production techniques in DaVinci Resolve on

her YouTube channel.
## **Who This Book Is For**


This hands-on training guide is designed for colorists at every stage of their grading

career. It is for newcomers who want to learn the fundamentals of technical and creative

color correction, users who want to become more familiar with professional workflows,

freelancers who wish to fill the gaps in their knowledge, and professional colorists who are

either switching to DaVinci Resolve or adding it to their arsenal of grading tools.


The book is divided into three parts:


- **Part I:** Color Correcting a DaVinci Resolve Timeline

- **Part II:** Managing Nodes and Grades

- **Part III:** Optimizing the Grading Workflow


You’ll start by going over the fundamentals of primary and secondary grading adjustments

with a focus on normalization, balancing, matching, and building a scene that draws the

viewer’s eye. You will then learn how to load a timeline edited in another NLE and correctly

color manage the footage to ensure it is appropriate for professional deliverable standards

like broadcast, cinema, streaming, and the web. Finally, you will look at the various

methods professionals use to optimize their grading workflow and the special

considerations that must be taken when working with raw media. Each subsequent lesson

builds on your understanding of these tools and workflows, with the intention that you will

be empowered to develop your own signature grading style by the end. Most of the

exercises in this guide can be completed on the free version of DaVinci Resolve 20 from

[blackmagicdesign.com.](http://blackmagicdesign.com)
## **Getting Started**


Welcome to **The Colorist Guide to DaVinci Resolve 20**, an official Blackmagic Design–

certified training book that teaches students and professionals how to get the most out of

color grading when using DaVinci Resolve 20. All you need is a Mac, Windows, or Linux

computer, the free download version of DaVinci Resolve 20, and a passion for learning

about the art of color grading.


**Getting Started** **ix**


This guide blends practical, hands-on exercises with the aesthetic and technical aspects of

the colorist’s art. You’ll learn how to use the program’s many grading tools and workflows

and gain an in-depth understanding of advanced techniques and creative industry

practices. Some exercises will even take you into the realm of compositing, which is an

increasingly required skill of contemporary colorists.

##### **About DaVinci Resolve 20**


DaVinci Resolve is Hollywood’s most trusted application for color correction. It has also

become the world’s fastest-growing and most advanced editing software. It features a

complete set of professional audio editing and mixing tools in the Fairlight page and a

2D and 3D visual effects compositing and motion graphics environment in the

Fusion page. Together, these powerful tools enable you to complete even the most

challenging projects using only one piece of software!

##### **What You’ll Learn**


In these lessons, you will load multiple projects to learn fundamental and advanced

techniques used in various post-production workflows and varying magnitudes of project

types. You’ll acquire practical skills that you can apply to real-world productions.


**Part I**


Part I of the book will have you restoring a documentary edit from a DaVinci Resolve

archive file. The three lessons within this section focus on fundamental grading theory and

practices. You will normalize and balance footage with the primary grading tools in Lesson

1, match shots for continuity in Lesson 2, and use secondary grading tools to target

specific elements in Lesson 3.


**Part II**


Part II looks at more advanced approaches to color management and the grade node tree

structure in a feature film sequence. In Lesson 4, you will migrate the project to

DaVinci Resolve using an XML file. In Lesson 5, you will more fully explore the importance

of node order and consider incorporating mixer nodes to ensure optimal visual results. In

Lesson 6, you will practice different methods of managing and copying grades to develop

efficient, quick workflows.


**Getting Started** **x**


**Part III**


Part III focuses on optimizing grading workflows to ensure quick, accurate deliveries and

looks at the unique properties of high dynamic range footage. In Lesson 7, you will

examine media reframing and changing resolutions mid-project, advanced keyframing,

compositing, and noise-reduction techniques. Lesson 8 incorporates the classic grading

workflow into a group-based pipeline that will allow you to grade entire timeline segments

in one node tree. Lesson 9 teaches how to set up an ACES project with raw media and

emphasizes its extended grading potential in the HDR grading palette. Finally, Lesson 10

covers project delivery from basic preset setup to custom renders and DCP workflows.


The appendix at the end of the book provides additional information about the Davinci

Resolve panels, with an extended overview of the DaVinci Resolve Mini Panel.

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

[training program offers a learning path for you. Please visit www.blackmagicdesign.com/](http://www.blackmagicdesign.com/products/davinciresolve/training)

[products/davinciresolve/training to find the rest of the books in our training series.](http://www.blackmagicdesign.com/products/davinciresolve/training)


**Getting Started** **xi**


##### **Getting Certified**

After completing this book, you are encouraged to take a 1-hour, 50-question online

proficiency exam to receive a Certificate of Completion from Blackmagic Design. The link

to the online exam can be found on the Blackmagic Design training webpage. The

webpage also provides additional information on our official Training and Certification

Program. Please visit [www.blackmagicdesign.com/products/davinciresolve/training.](http://www.blackmagicdesign.com/products/davinciresolve/training)

##### **System Requirements**


The exercises in this book were written for DaVinci Resolve 20.0 for Mac, Windows, and

Linux. If you have an older version of DaVinci Resolve, you must upgrade to the current

version to follow along with the lessons.


NOTE The exercises in this book refer to file and resource locations that may

differ if you’re using the software version from the Apple Mac App Store. For the

purposes of this training manual, if you are using macOS, we recommend

downloading the DaVinci Resolve software directly from the Blackmagic Design

website rather than the Mac App Store.

##### **Download DaVinci Resolve**


To download the free version of DaVinci Resolve 20.0 or later from the Blackmagic

Design website:

**1** Open a web browser on your Windows, Linux, or Mac computer.

**2** In the address field of the web browser, type:

[www.blackmagicdesign.com/products/davinciresolve.](http://www.blackmagicdesign.com/products/davinciresolve)

**3** On the DaVinci Resolve landing page, click DaVinci Resolve – Free Download Now.

**4** On the download pop-up page, choose whether you will work in the free version of

DaVinci Resolve 20 (left) or purchase DaVinci Resolve Studio 20 (right), and then click

the button that corresponds to your computer’s operating system. The free version

of DaVinci Resolve features most of the tools you will need to produce and deliver

a professional grade. You can complete the lessons in this book and pass the

certification exam using the free version of DaVinci Resolve, although some

exercises may display a watermark.

**5** Follow the installation instructions.


**Getting Started** **xii**


When you’ve completed the software installation, follow the instructions in the following

section to download the content for this book.

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


**Getting Started** **xiii**


**1** If required, you can change the language used. You can also learn more about these

and hundreds of other amazing features available in DaVinci Resolve 20 by clicking

Learn More. Otherwise, click Continue.


Next, you are invited to go through the Quick Setup process. Experienced users can

skip this process by clicking “Skip and Start Right Now,” but new users are advised to

follow this process. It will only take a couple of minutes and is useful in understanding

how Resolve is working.


**Getting Started** **xiv**


**2** Click the Quick Setup button.


**3** DaVinci Resolve will check your system to ensure its operating system and graphics

card will perform well. If both pass this test, click Continue.


**Getting Started** **xv**


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


**Getting Started** **xvi**


**5** Leave this set to the default location and click Continue.


On the next screen, you will be asked which keyboard layout you would like to use. This

is specifically relevant if you’re familiar with using another nonlinear editor; however,

throughout this Colorist Guide you will be introduced to keyboard shortcuts that use

the DaVinci Resolve keyboard layout. So if you change the layout at this point, you may

find those shortcuts won’t work.


**Getting Started** **xvii**


**6** For now, leave the layout set to DaVinci Resolve and click Continue.


Congratulations! You have completed the Quick Setup process and have changed

precisely nothing in terms of DaVinci Resolve’s default setup. Nevertheless, you have

also gained an insight into some aspects of using DaVinci Resolve that will serve you

well as you continue learning about the application and how it uses your system.

**7** Click Start to launch and begin enjoying DaVinci Resolve 20!


Once loaded, DaVinci Resolve will open to the cut page, which is the default starting

page for all projects. However, this is not the usual place to begin working with

DaVinci Resolve. Instead, you should now exit the application in readiness to begin the

first lesson in this book.


**Getting Started** **xviii**


**8** Choose DaVinci Resolve > Quit DaVinci Resolve or press Command-Q (macOS) or

Ctrl-Q (Windows).


DaVinci Resolve 20 will close.

##### **Get the Lesson Files**


The DaVinci Resolve lesson files must be downloaded to your Mac, Windows, or Linux

computer to perform the exercises in this book.


**To Download and Install the DaVinci Resolve Lesson Files**

**1** Open a web browser on your Windows, Linux, or Mac computer.

**2** In the address field of your web browser, type:

[www.blackmagicdesign.com/products/davinciresolve/training.](http://www.blackmagicdesign.com/products/davinciresolve/training)

**3** Scroll the page until you locate _The Colorist Guide to DaVinci Resolve 20_ .

**4** Click the Lesson Files Part 1 link to download the media for the first section of the

book. The BMD 20 CC - Project 01.zip file is roughly 2 GB.

**5** Click the Lesson Files Part 2 link to download the media for the second section of the

book. The BMD 20 CC - Project 02.zip is roughly 1.5 GB.

**6** Click the Lesson Files Part 3 link to download the media for the third section of the

book. The BMD 20 CC - Project 03.zip is roughly 2.2 GB.

**7** After downloading the zip files to your computer, open your Downloads folder and

double-click to unzip them (if they haven’t unzipped automatically).

**8** In your chosen storage location—for example, the Movies folder (macOS) or Videos

folder (Windows)—create a new folder called **BMD 20 - The Colorist Guide** .

**9** From your Downloads folder, drag the BMD 20 CC - Project 01, BMD 20 CC - Project 02,

and BMD 20 CC - Project 03 folders into the BMD 20 - The Colorist Guide folder you

created in the previous step.

**10** You are now ready to begin Lesson 1, “Balancing Footage.”


After you have completed an exercise, you have the option to review the completed

timeline that is included in every project file provided with the media. Remember that color

grading is a subjective practice, and your results will often differ from the completed

timelines. Rather than attempting to match your work exactly, use them for general

comparison and troubleshooting.


**Getting Started** **xix**


# Interface Review

_“No matter how much post experience you have, there’s always something new to learn_

_about DaVinci Resolve. I sometimes find that going back and reviewing the basics helps_

_give you perspective on finding a new way to give clients the look they want quickly and_

_efficiently. Highly recommended for newcomers and veteran colorists alike.”_


**Marc Wielage**, Senior Colorist - Chroma | Hollywood


This section provides an overview of the color page interface, covering its key

functions and establishing the terminology that will be used throughout the book.

## **Color Page Layout**


The default layout of the color page contains the following panels:



|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|
|---|---|---|---|---|---|---|---|
|||||||||
|||||||||


Primaries color wheels



Curves



Node Editor


Mini-timeline Keyframe Editor



**Gallery** contains stills that can be used for visual comparison or for copying grading

data. Stills can be generated from the color page or imported from an external source

and organized into albums.


**Interface Review** **xx**


**Viewer** displays the selected clip with playback controls and offers additional

interface tools.


**Node Editor** allows grades and effects to be structured to maximize each clip’s

visual quality.


**Thumbnail timeline** represents each clip as a single frame, making it easy to navigate

and find individual clips.


**Mini-timeline** more closely resembles the track structure of the edit page.


**Primaries color wheels** control the tonal and chromatic values of an image based on

three luminance ranges (lift, gamma, and gain).


**Curves** give precise control over the tone-based values of the luminance and

RGB channels.


**Keyframe Editor** allows you to animate color grades, sizing parameters, and effects.


At the top of the color page, the interface toolbar features buttons that allow you to show

and hide panels as needed. Hiding panels (for example, the Mini-timeline or the Gallery)

will create more space for the viewer and the remaining panels.


NOTE If your screen resolution is less than 1920 x 1080 HD, there may be some

differences in the interface layout. For example, your left and central palettes will

be combined into a single list on the left side of the screen. In some palettes,

parameters such as the Matte Finesse may be presented on two pages rather than

one. Regardless, you will still have access to all the same tools described in this

training manual.


**Interface Review** **xxi**


## **Viewer**

The viewer shows the frame that the playhead is currently on. By default, images are

represented as they will appear upon final render. Additional features allow you to

temporarily bypass grades, see clip mattes, and compare clips to one another.


Some additional controls at the top and bottom of the viewer maximize the tools’

functionality in the color page.


TIP You can position your mouse pointer over any tool in the color page to

see its name.


**Image wipe** enables you to wipe between a still, a clip in the timeline, or a reference

movie frame for visual comparison and matching.


**Split screen** places clips alongside one another for review and comparison.

It features several modes to compare clips on a timeline, clips in the same group,

or even versions of grades within the same clip.


**Highlight** is enabled to reveal the matte associated with a selected node.


**Onscreen control menu** is a pop-up menu in the lower left of the viewer that features a

selection of UI controls associated with some of the palettes and effects of the color page.


The bottom of the viewer contains a scrubber and transport controls that allow you to

navigate the clip as you would in the edit page.


**Interface Review** **xxii**


## **Primaries Color Wheels**

The Primaries color wheels (and the corresponding color bars and log wheels) allow

you to affect the brightness and hue of the image by targeting specific tonal ranges.

Adjustments to the color wheels are made by dragging the color balance indicators at

the center.


**Lift** targets the shadows of the image.


**Gamma** targets the midtones of the image.


**Gain** targets the highlights of the image.


**Offset** affects the image uniformly.


**Master wheels** are the dark horizontal sliders below the color wheels that control the

YRGB values of those respective ranges. Y represents luminance, and RGB represents

the red, green, and blue channels of the image.


Clicking the Reset arrows in the upper right corner of each wheel will neutralize the color

and master wheel of that range. You can also reset the entire palette by clicking the Reset

All button in the upper right corner.


The adjustment controls at the top and bottom of the Primaries palette give additional

control over image features such as contrast and saturation, temperature and tint,

and so on.


**Interface Review** **xxiii**


## **Palette Panel**

A series of buttons under the timelines allow you to navigate the palettes of the color page.

From left to right, these palettes are:


**Left palettes** —Camera Raw, Color Match, Primaries, High Dynamic Range, RGB Mixer,

Motion Effects


**Central palettes** —Curves, ColorSlice, Color Warper, Qualifier, Window, Tracker,

Magic Mask (Studio version only), Blur, Key, Sizing, 3D


**Keyframe Editor** —Keyframes, Scopes, Info


Use these buttons to navigate between palettes when prompted during the exercises.

The name of each palette appears in the upper left corner when clicked, as well as over the

button itself when your mouse pointer hovers over it.


**Interface Review** **xxiv**


## **Introducing Blackmagic Cloud**

DaVinci Resolve is the world’s only complete post-production solution that lets everyone

work together on the same project at the same time. Traditionally, post-production follows

a linear workflow with each artist handing off to the next, introducing errors and

mountains of change logs to keep track of through each stage. With DaVinci Resolve’s

collaboration features, each artist can work on the same project in their own dedicated

page with the tools they need.


To begin using the Blackmagic Cloud, simply create a Blackmagic Cloud ID, log in to the

online DaVinci Resolve Project Server, and follow the simple instructions to set up a new

project library—all for one low monthly price!


Once created, you can access this library directly from the Cloud tab in the Project

Manager to create as many projects as you need—all stored securely online. Then, invite

up to 10 other people to collaborate on a project with you. With a simple click, they can

relink to local copies of the media files and start working on the project immediately, with

all their changes automatically saved to the cloud.


Enabling Multiple User Collaboration for your project means that everyone can work on

the same project simultaneously—edit assistants, editors, colorists, dialogue editors, and

visual effects artists can now all collaborate wherever they are in the world in a way never

before possible.

##### **Media Sync with Blackmagic Cloud Store**


Now you don’t need to buy expensive proprietary storage that requires an entire IT team

to manage! Blackmagic Cloud Store has been designed for multiple users and can handle

the huge media files used in Hollywood feature film productions. You can also have

multiple Blackmagic Cloud Stores syncing the media files with your Dropbox account so

that everyone can access the project’s media files.


To find out more about these exciting workflows, visit:

[www.blackmagicdesign.com/products/davinciresolve/collaboration.](http://www.blackmagicdesign.com/products/davinciresolve/collaboration)


**Introducing Blackmagic Cloud** **xxv**


### Part I
# Color Correcting a DaVinci Resolve Timeline
## **Lessons**


- Balancing Footage

- Creating Color Continuity

- Correcting and Enhancing Isolated Areas


Part I of _The Colorist Guide to DaVinci Resolve 20_ focuses on establishing a strong practical

foundation of primary and secondary grading techniques with the aim of balancing and

matching media in preparation for creative grading.


This book is divided into three distinct parts, each devoted to a different film genre and

using three different project setup and color management methods. In Part I, the project

is a documentary that is accessed using DaVinci Resolve’s archiving feature.


**Project File Location**

You will find all the necessary content for this section in the BMD 20 CC - Project 01

folder. Follow the instructions at the start of every lesson to find the necessary

project, timeline, and media files. If you have not yet downloaded the first set of

content files, go to the “Getting Started” section of this book for more information.


NOTE Although you can use DaVinci Resolve 20 for most of this guide, some

exercises will require DaVinci Resolve Studio 20. If you don’t have DaVinci Resolve

Studio 20, you can still complete such exercises with a watermark overlay and are

encouraged to do so to learn these advanced tools and techniques.


**Color Correcting a DaVinci Resolve Timeline** **1**


**This page is intentionally left blank** **2**


### Lesson 1
# Balancing Footage



The first project you will grade is

a documentary about protecting

endangered rhinos. The workflow

described is applicable to

virtually all types of video project

grading, but documentary

cinematography is particularly

dependent on the following actions:


- **Balance footage** Documentary

videographers often quickly change

positions and locations during a shoot,

which means they have less shot-to
shot control over lighting conditions.

- **Match shots** Scenes, interviews, and

B-roll can be shot over many days with

different cameras, requiring you to

visually match all content to create a

cohesive narrative.

- **Improve imagery** A variety of

techniques are used to confine grading

to specific portions of a shot to

enhance skies, skin tones, and

visual framing.



Time

This lesson takes approximately
2.5 hours to complete.

Goals

Opening a DaVinci Resolve
Archive 4

Setting Up Project Backups 6

Understanding the
Grading Workflow 8

Primary Grading with Color Wheels 11

Precision Grading with Curves 20

Comparing Color and Log Wheels 28

Self-Guided Exercises 42

Lesson Review 43


You wouldn’t color grade a somber documentary about rhinoceros sanctuaries as you

would grade a 30-second perfume ad featuring the latest Hollywood A-lister, even if

both projects were shot on the same type of camera. So in addition to addressing the

technical requirements of the footage, you will also consider the documentary’s narrative.


In this lesson, you’ll familiarize yourself with the primary grading tools used to adjust the

tonal range and color balance of clips on a timeline, learn to read waveforms and parade

scopes for optimal matching, and employ secondary grading selection methods to

enhance your final look. You will do so in the context of an overall grading workflow that

addresses the needs of each timeline clip.
## **Opening a DaVinci Resolve Archive**


The timeline for this project was edited and archived in DaVinci Resolve 20 to create a

DaVinci Resolve archive (.dra) folder. This is one of the most efficient methods for sharing

and launching timelines because it includes the original project file and all its associated

media. By restoring a .dra folder, you can be certain that you are seeing the timeline

exactly as intended by the editor, with all its tracks, transitions, graphics, effects, and

retiming intact.


**Blackmagic Design Mini Panel Operations**

DaVinci Resolve control panels are designed to give you fluid, hands-on control

over multiple parameters at the same time, so you can work faster and be more

creative. See the Appendix A, “Using the DaVinci Resolve Panels,” for an overview

of how a control panel can optimize your workflow in DaVinci Resolve. Throughout

this book, lesson notes will show how exercise workflows can be incorporated and

enhanced using a Mini Panel.


NOTE For a quick refresher on the DaVinci Resolve interface, see the

“Interface Review” section earlier in this book.


**Lesson 1 Balancing Footage** **4**


**1** Open DaVinci Resolve 20.

**2** Right-click in the Project Manager window and choose Restore Project Archive.

**3** On your hard disk, locate the BMD 20 CC - Project 1 folder.

**4** Select the **Project 01 - Disunity Documentary.dra** file and click Open.

**5** In the Project Manager, double-click the **Project 01 - Disunity Documentary**

thumbnail to open the project.


**6** To enter the color page, click the Color button at the bottom of the interface or

press Shift-6.


The name of the timeline is visible above the viewer. You can select the active timeline

by clicking the disclosure arrow next to the timeline name and choosing from the

dropdown list.

**7** Verify that you are on the **01 Main Timeline** .


TIP You can archive projects by right-clicking a project thumbnail in the Project

Manager and choosing Export Project Archive. Doing so will consolidate your

project file, timelines, and media into a single folder for sharing or future retrieval.


You’re almost ready to start grading! However, before you begin, you should check that

your project is being backed up correctly.


**Lesson 1 Balancing Footage** **5**


## **Setting Up Project Backups**

As soon as you create or load an existing project, it is good practice to ensure that

DaVinci Resolve’s Live Save feature is running in the background. Performing incremental

background saves will keep track of every change you make to your project, as well as

retain older variants of your project for future recall.

**1** Open DaVinci Resolve > Preferences.

**2** At the top of the Preferences pop-up window, switch from System to User.

**3** Click “Project Save and Load” to the left to access Save Settings.


By default, Live Save is enabled, meaning DaVinci Resolve will overwrite your active

project file every time you make a change, no matter how small. Enabling this setting is

crucial for minimizing the risk of losing project changes in the event of unexpected

system or program shutdowns.

**4** Select the “Project backups” checkbox.


Enabling this option saves a new copy of your project file (.drp) at regular intervals to a

designated backup location.


Below, you can see backup intervals spaced by minutes, hours, and days.

**5** Leave the first setting to continue backing up your project every 10 minutes, which will

produce 6 backup files every hour.


After the first hour, older projects will be cleared from project storage, except for

occasional files that extend over hourly and daily intervals. This behavior can be

extremely helpful when working on long-form projects because it allows you to return

to a project’s state from a specific period (such as two weeks ago, for example) without

sorting through thousands of backed-up project files.


**Lesson 1 Balancing Footage** **6**


**6** Increase the hourly backups to 24 hours. That means that at the start of every hour, a

new backup file will be generated, allowing you to return to the state of your project at

any point in the day. Remember, backups aren’t generated unless you are actively

working, so an average workday will only produce as many backups as the amount of

hours that you work.

**7** Increase the daily backups to 180 days. This will generate a new backup of your project

at the start of every day going back roughly 6 months. Again, this will only produce the

number of backups that equate to the number of days you actively work on the

project, but this style of backing up can be invaluable when returning to a project a

few months after completion to perform additional work/deliverables without the risk

of overwriting your older backups.

**8** To select the backup location, click Browse and specify a save destination on your

workstation or external drive.

**9** Select the “Timeline backups” checkbox.


This option will generate a copy of all your active timelines (.drt) at the same backup

location and time intervals. Backup timeline files are helpful because they are

substantially smaller than the project files and can be used to restore an edit to an

earlier version without needing to reconstruct the entire project.


Project and timeline backups are generated only when there has been some activity

within the shortest time interval. So if you have 30 timelines in your project, only the

timeline(s) you’ve worked on in the last few minutes will be backed up.

**10** Click Save to commit the change and close the Preferences window. You may continue

working on your project, knowing that every change will be saved and backed up.


NOTE To open a backed-up project file, you can access the DaVinci Resolve

project (.drp) file at the designated backup location on your drive, or you can open

the Project Manager, right-click the thumbnail of the project you wish to restore,

and choose Project Backups. From the window that opens, you can select from a

list of all the backups associated with the project.


With the project loaded and Live Save enabled, you can proceed with color grading. But

where to begin? When approaching an ungraded timeline, it’s not always obvious where

your starting point should be. The next section provides a general overview of the

grading process.


**Lesson 1 Balancing Footage** **7**


## **Understanding the** **Grading Workflow**

It is good practice to have a clear idea of what your workflow is before beginning a grade.

Your workflow is informed by a variety of factors, including the color space and format of

your footage, the way the timeline was shared with you, the content of the scenes, and the

aesthetic/emotional intention behind the project. Let’s review the most common phases of

a grading workflow.

##### **Balancing and Shot Matching**


Before you can grade footage creatively, you must adjust shot luminance and chromaticity

to create a level starting point for your grade. This process is akin to laying down a primer

on a canvas before painting to ensure that the pigment is applied to a consistent surface.


A single grade applied to five balanced and matched shots will establish a visual continuity

that flows naturally from one shot to the next, whereas the same grade applied to

unbalanced and mismatched shots will continue to reflect each shot’s differences.


This stage of grading is often referred to as _color correction_ and is achieved by means of

primary grading tools, in which the entire frame of the image is adjusted. Color correction

is performed using techniques such as _normalization_, _balancing_, and _shot matching_ .


Normalization and balancing creates a neutral starting point for clips in the timeline by

consistently adjusting their tonal distribution and neutralizing any issues with their

color balance.


Shot matching involves comparing clips and matching their contrasts and colors exactly.

This technique is particularly advantageous when most of your clips already have a similar

look, and you need to tweak only a few exceptional shots to create a smooth starting point

for your scene grade.


**Lesson 1 Balancing Footage** **8**


##### **Secondary Grading**

_Secondary grading_ refers to any part of the grading process in which only a part of the

image is altered. The potential for secondary grading is limitless, but it is mainly achieved

by two means: _keying_ and _masking_ .


Keying targets a portion of an image based on a hue, saturation, or luminance range. In

DaVinci Resolve, the main tool for key extraction is the Qualifier palette, although other

tools also rely on this method of selection, including HSL curves, the Color Warper, and

some Resolve FX.


Masking employs geometric vector shapes to isolate a portion of an image.

DaVinci Resolve’s masking interface, the Window palette, features adjustable Power

Windows in the form of preset shapes (linear, circle, polygon, and gradient), and a

customizable curve window that enables you to generate garbage mattes and rotoscopes

(animated masks). The Magic Mask palette performs a similar task by automatically

detecting and tracking objects and people to generate masks.


Like the qualifier, windows cannot alter the appearance of an image directly but act as

selectors for the grading tools.


Secondary grading is most powerful when qualifiers and Power Windows are used in

tandem. While the qualifier focuses on extracting an element with a clean edge, a window

can confine the qualifier’s influence to a specific portion of the frame. In this way, it’s

possible to target an object in areas of the shot that are of a similar key range.

##### **Creating a Look**


Once your clips are balanced and shot matched, and any individual secondary grading

needs are met, your creative process, often referred to as _color grading_, can begin.


When performing creative grading, you should carefully consider the emotional and

narrative implications of the scene. You can apply both primary and secondary grading

techniques to influence an audience’s emotional perception of an environment by

tweaking the scene’s color temperature to indicate positive (warm) or negative (cold)

moods and evoke a wide range of psychological color and tone associations. Additionally, a

creative grade can communicate practical narrative elements such as a change in location

or time (for nonlinear stories).


**Lesson 1 Balancing Footage** **9**


NOTE The grading workflow described here does not rigidly dictate the order in

which these grades should be performed by the colorist. Although balancing and

shot matching is a common first step, some workflows might begin with the

application of a creative show Lookup table (LUT) or color management node and

follow with corrective tweaks to the primaries. As you gain more experience as a

colorist, you will develop an intuition for the appropriate approach when grading.

##### **Visualizing the Grading Workflow** **in the Node Editor**


The following chart represents a traditional grading workflow in the Node Editor in

DaVinci Resolve’s color page.


This graph is not intended as a literal guideline to how nodes should be structured in every

clip, but rather an interpretation of the traditional grading workflow in node form. In fact,

as noted previously, grading workflows will not always be linear, and you might start by

applying looks at the end of the pipeline (closer to the Output node) before moving

upstream (toward the Input node) to make primary corrections. Because of this, it is

helpful to think of this chart as a live signal flow rather than an order of operations.


**Lesson 1 Balancing Footage** **10**


## **Primary Grading** **with Color Wheels**

When you first launch DaVinci Resolve’s color page (or reset its UI layout), the first grading

palettes you see are the Primaries color wheels and Custom Curves. This is because they

are among the most fundamental grading tools used for color grading, and you will need

to master them to become a skilled colorist.


TIP To reset a page to the default layout, choose Workspace > Reset UI Layout.

You may want to do this at the start of every new project in this book to match the

layout shown in the screenshots. Additionally, you can choose Workspace > Full

Screen Window to dynamically resize DaVinci Resolve to fit your computer screen.


In the following exercises, you will learn how to set contextual luminance and balance with

the color wheels while monitoring your adjustments in the waveform scope for unwanted

clipping and color dominance.

##### **Setting Tonal Range with Master Wheels**


The human eye is particularly sensitive to light sources, shadows, and contrast, which is

why it makes sense to begin the color correction process by establishing the tonal range

of an image.

**1** Select clip 02, which shows an image of a rhinoceros behind a wooden gate.


**Lesson 1 Balancing Footage** **11**


By default, the palette in the lower right corner of the DaVinci Resolve interface is set

to the Keyframes palette. You will switch it to display scopes so you can analyze your

footage while you color correct it.

**2** Click the Scopes palette button on the right side of the page.


**3** At the top of the Scopes palette, click Parade to reveal a scopes dropdown menu and

select Waveform.


The waveform scope displays the luminance and color channel values of the video at

the timeline position of the playhead.


The vertical axis of the scope represents the entire potential luminance range of the

image. The bottom of the display represents black (an RGB pixel value of 0, 0, 0) and

the top represents white (a pixel value of 1023, 1023, 1023 in a 10-bit depth signal).

Between the two values is a vertical black-to-white grayscale gradient that conveys the

full range and distribution of values in the image.


**Lesson 1 Balancing Footage** **12**


The horizontal axis scans the image itself and produces a readout (also known as a

_trace_ ) that directly correlates between the viewer and waveform graph. You can think

of the waveform display as showing the distribution of pixels across their respective

vertical columns based on their luminance levels, with darker areas of the footage

appearing toward the bottom of the graph and lighter areas toward the top.


Each color channel is overlaid in the resulting trace. A prominent section of color

usually indicates an environment or object with a dominant hue, or an unbalanced

image. When channels overlap perfectly as a result of equal intensity, they produce a

white trace, which implies a neutral (gray) surface in the scene.


When adjusting tonality in an image, you can disable the RGB channels in the

waveform to focus only on luminance.

**4** In the upper-right corner of the Scopes palette, click the Settings button.


**5** Click the Y (luma) channel button at the top to display only the luminance of the image.

**6** Deselect the Colorize option to display the trace with solid white pixels.


**7** Drag the Waveform brightness slider to the right to increase trace visibility and help

make the more subtle areas stand out.


**8** Click anywhere in DaVinci Resolve to close the waveform settings window.


Any part of the trace that goes below 0 (black point) and above 1023 (white point) in

the luminance range will be clipped, which will result in a loss of image detail.

_Normalization_ describes the process of expanding the luminance of a video signal in

order to best represent the original lighting in a scene.


**Lesson 1 Balancing Footage** **13**


When normalizing footage, a good starting point is to ensure that the shadows are

floating at around 5–10% above the black point (0) on the scope, while highlights stop

well under the white point (90%). This leaves the remaining 10% as headroom for

super-white elements such as blown-out headlights, windows, or metallic specular

highlights that can extend up to and beyond the white point.

**9** Ensure that the Primaries palette is active in the left palettes of the color page.


If you’ve already completed the book _The Beginner’s Guide to DaVinci Resolve 20_ or read

the “Interface Review” section earlier in this book, you know that the Lift wheel affects

the image shadows, the Gamma wheel affects the midtones, and the Gain wheel

affects the highlights. The Offset wheel impacts the entire luminance range of the

image uniformly.


The horizontal wheels located under the color wheels are called master wheels and

impact the brightness of their respective ranges.

**10** Drag the Lift master wheel to the left to darken the shadows. Because this image has

detail in the darkest areas of the wood, aim to place the lowest parts of the waveform

trace above 0 but below the 128 line.


Notice the three areas of the graph where the trace of the waveform dips toward the

black level. Try to locate their respective positions in the viewer.


**Lesson 1 Balancing Footage** **14**


Those three dark areas correspond to places where the barrier is visible behind the

wooden poles in the rhino enclosure. The darkest areas of the barrier are represented

by a pronounced dip in the graph.

**11** You can use the Gain master wheel to affect the lighter areas of the image. The image

has no chart or reference for pure white, but you could use the thumb in the image as

a luminance guide. The highlights on skin should rest between 50–75% on the

waveform graph. Drag the Gain master wheel so the tallest traces do not go higher

than three-fourths of the waveform graph.


This is an example of using image context for balancing and grade adjustment. In

future exercises, you will continue to identify elements that you could use as guides

for grading decisions.


With the shadow and highlight levels set, you may opt to adjust the brightness of

the midtones.

**12** Drag the Gamma master wheel to the right to brighten the overall scene and enhance

the details of the rhino’s wrinkled skin.


After establishing the tonal range, you can further enhance the image details. The

master wheels affect the luminance too broadly at this stage, so you could use the

contrast control to refine the distinction between the darker and lighter areas.


**Lesson 1 Balancing Footage** **15**


**13** At the top of the Primaries palette, in the adjustment controls, drag the Contrast

setting to the right to increase the level of detail in the skin and the wooden poles.


Your image might start to look a little dark, but that’s OK. At this stage, you should only

focus on establishing the depth of the shadows and revealing details in the midtones.

**14** To adjust brightness while maintaining the same level of contrast, drag the Pivot

control next to the Contrast parameter.


The Pivot controls the contrast balance by placing more or less priority on either side

of the tonal range. By pivoting to the left, you will increase the overall brightness and

clarity of the image.

##### **Balancing Colors with Master Wheels**


Finally, you will address the color imbalance in the image. This can be accomplished in

several ways in DaVinci Resolve, with one of the most common being the color balance

indicator within the color wheels. To help with balancing the image, you’ll bring back the

color channel readouts in the waveform scope.

**1** In the upper right corner of the Scopes palette, click the Settings button.

**2** Click the RGB channel button at the top and re-enable the Colorize option.


If necessary, activate the three RGB channel indicators.


**Lesson 1 Balancing Footage** **16**


**3** Click anywhere outside the Settings window to close it.


In the RGB waveform scope, there is a red section running across the top of the trace.

This typically indicates a color imbalance. Since it is in the upper half of the graph, you

will use the Gain wheel to correct it.

**4** Drag the Gain color wheel indicator away from red to reduce the red dominance in

the waveform.


Notice that when you drag the indicator too far, the image starts to turn cyan. One of

the fundamentals of color balancing is that you neutralize colors by adding their

complementary hue (in this case cyan to neutralize red). With correct balancing, the

addition of the complementary color will produce neutral tones. But if pushed too far,

the complementary color will start to show.

**5** Press Command-Z (macOS) or Ctrl-Z (Windows) to undo the Gain color wheel

adjustment but keep the recent Gain luminance adjustment.


NOTE The undo function is stacked to each clip in the timeline. When you

undo, only the changes from the selected clip are removed, and not from any

other clips on the timeline, even if you graded them more recently.


**Lesson 1 Balancing Footage** **17**


One of the unique challenges of this shot is that there are many naturally red elements

in it—the wood posts and fence, and the earthy ground in the back. This can create the

perception of color imbalance in the waveform. To balance the image without being

distracted by these red elements, you need to find neutral surfaces in the waveform

and focus on balancing them only. You’ll use the Qualifier Focus to help you find

these surfaces.

**6** Click the Scopes palette options menu.

**7** Select Display Qualifier Focus.


**8** Ensure that the viewer’s onscreen control menu is set to Qualifier.


When you move your mouse in the viewer, you should now see red, green, and blue

circles traveling around the waveform, showing the values of the pixels directly under

your mouse pointer.


Find a surface that you would reasonably expect to be neutral in the image and find its

corresponding position in the waveform. In this case, the underside of the rhino’s ear

is a safe choice.


**Lesson 1 Balancing Footage** **18**


**9** Drag the Gain color wheel indicator away from red until the channels in that section of

the waveform overlap to produce a white trace.


**10** Press Command-D (macOS) or Ctrl-D (Windows) to toggle the grade on and off.

Compare your before and after results to evaluate how the primary tonal adjustment

and balance affected the image. Tweak the values if the grade appears overpowering.


Bypassed Graded


TIP Another way to disable/enable node grades is by pressing the number of a

node in the Node Editor.


The grading process usually requires some back-and-forth tweaking of palette values while

monitoring the waveform. Some changes will offset the effects of prior adjustments—like

how dragging the Gain master wheel raised the lower midtones—while others might

require an occasional reset while you find the optimal reference points for tonal

distribution and balancing. Iteration is a completely natural part of the grading process,

and you will find that you get faster as you get more practice.


**Lesson 1 Balancing Footage** **19**


## **Precision Grading with Curves**

Curves are another major grading tool used to perform primary and secondary adjustments.

Whereas the wheels target the tonal ranges of an image, the curves affect the intensity of

an image’s luminance or RGB color channels. The application of custom control points also

means you can manipulate the image with far greater precision and flexibility.


**Lesson 1 Balancing Footage** **20**


##### **Setting Contrast with Increased Flexibility**

As in the previous exercise, you will begin by setting the tonal range and contrast of the

image. Curves will allow you to do this with finer control over the luminance range and

allow for customizable contrast.

**1** Select clip 03, which shows an image of a scale.

**2** Open the Waveform settings and click the Y button to view the luma waveform.

**3** Disable Colorize for a clearer view of the luminance values of the image.


Because the colors in the image are flat, most of the waveform trace is condensed in

the lower midtones. A significant elevation appears to the left, where there is a window

behind the scale, and to the right there is a short peak where the light reflects off the

plastic rim.

**4** Choose Workspace > Viewer Mode > Enhanced Viewer or press Option-F (macOS)

or Alt-F (Windows) to enlarge the viewer.


The Clips timeline and surrounding palettes collapse, dynamically enlarging the size

of the viewer panel. The image is now much easier to see for grading work.

**5** Ensure that the Curves palette is active in the central palettes of the color page.


**Lesson 1 Balancing Footage** **21**


The lower left of the curve graph represents the blackest potential point of the image,

and the upper right represents the whitest.


The horizontal axis allows you to target any luminance (or hue or saturation, in other

HSL curve configurations) section of the image, while the vertical axis allows you to

offset that section. By raising or lowering the two control points at either extreme of

the curve, the black point and the white point, you can manipulate the luminance

distribution of the image.

**6** For finer point control, turn the Curves palette into a floating window by clicking the

Expand button in the upper right corner.


To move the window, drag the header. To resize the window, drag the sides

and corners.


By default, the luminance curve (Y) is ganged to all three color channels (R, G, B). When

working with a YRGB curve, as well as affecting the brightness of the image, you will

also be impacting saturation.

**7** Click the Y channel button to ungang the channels.


Now you will only be altering the image luminance.

**8** Drag the black point of the Y curve across the floor to the right.


Doing so lowers the waveform of the image linearly, darkening the shadows more than

the highlights.

**9** Stop dragging the control point when the bottom of the trace is still above the 0 line

of the waveform graph.


**Lesson 1 Balancing Footage** **22**


**10** To raise the top of the waveform, drag the white point across the top of the graph.


Normally, you’d stop when the top of the trace touches the second horizontal line in

the waveform graph (around 90%), but because this part of the trace represents a very

bright window in the video clip, it makes sense to continue raising it until the trace is

about halfway between the top horizontal lines on the graph.


You can add more control points to the curve to manipulate the midtones of the

image. Let’s tackle the lower midtones that appear too dark after performing that

black point adjustment.

**11** Click the lower half of the curve to create a new control point that will target the

lower midtones.


TIP When creating a control point, Shift-click to prevent the curve from

moving to the position of the mouse pointer.


**12** Drag the control point up to raise the lower midtones and brighten the face of

the scale.


**Lesson 1 Balancing Footage** **23**


Many colorists prefer setting the tonal range using curves because curves offer much

finer control over luminance and allow for customizable contrast.


Bypassed Graded

##### **Color Correcting with Curves**


You can use custom curves with dedicated control points to individually manipulate the

three color channels at precise levels of the channel intensity.

**1** Open the Waveform settings and click the RGB button.

**2** Select the Colorize checkbox to review the individual color channels in the

Waveform trace.


The red channel appears elevated above the other channels, which gives the image a

slightly warm appearance.

**3** In the Curves palette, click the red (R) button to isolate the red channel curve.


**Lesson 1 Balancing Footage** **24**


**4** Click the top of the red curve and drag it downward. Pay attention to the waveform and

drag until the red highlight overlaps the blue and green channels, resulting in a white

trace along the upper edge of the graph.

**5** Create a second point on the red curve to perform the same action in the midtones.

Drag downward until the lower half of the trace appears white.


Although the red tint is corrected, the image now has a mild yellow tint because the

blue channel has less presence in the highlights and midtones.


**Lesson 1 Balancing Footage** **25**


**6** Click B to isolate the blue channel.

**7** Click the center of the blue curve line to add a control point and drag it up until the

midtones in the waveform are aligned.


**8** Press Command-D (macOS) or Ctrl-D (Windows) to disable the color adjustments and

then re-enable them to review the corrected image.


With the luminance of the overall image altered, you could opt to return to the Y curve

and further adjust the tonal range and contrast of the image, if necessary. When

you’re satisfied with your work, press the X in the upper left corner of the expanded

Curves palette to collapse it.

**9** Choose Workspace > Viewer Mode > Enhanced Viewer or press Option-F (macOS) or

Alt-F (Windows) to collapse the viewer back to its original size.


You have now learned how to operate the two most essential primary grading tools in

the colorist’s arsenal. Throughout the remainder of this book, you will refine your

understanding of these tools and their variants, combine them with secondary tools

and effects, and further hone your primary grading skillset.


**Lesson 1 Balancing Footage** **26**


**Lesson 1 Balancing Footage** **27**


## **Comparing Color and Log Wheels**

Before working on the next clip, let’s take a slight detour to understand another function

that can be a fundamental part of primary grading and balancing: the log wheels.


It’s easier to grasp the difference between the Primaries color and log wheels by observing

a graphic example. Let’s use the simple gradient at the end of the timeline and manipulate

its brightness to compare how the two adjustments differ.

**1** Select the last clip in the timeline (the grayscale image).


In the standard Primaries color wheels that you are familiar with, the Lift, Gamma, and

Gain wheels target the luminance range as seen in the following figure:


A wide overlap occurs between the segments. When you try to manipulate the

highlights of the image using the Gain color or master wheels, the change also

substantially affects the midtones, and even the darker sections of the image.


The waveform scope displays the gradient graphic as a flat diagonal line extending

from left to right from 0 to 1023, indicating its linear transition from black to white.


**Lesson 1 Balancing Footage** **28**


**2** Drag the Gain master wheel to the left to darken the upper ranges of the gradient.


In the waveform, the top of the line moves freely while the bottom of the diagonal line

remains connected to the black point. In the viewer, the lightest part of the gradient is

affected most severely, with tapered, but still substantial, impact visible on the

remainder of the luminance range.

**3** Reset the Gain master wheel.

**4** Drag the Lift master wheel to the right to brighten the lower ranges of the gradient.


**Lesson 1 Balancing Footage** **29**


In contrast to the Gain wheel, most of the Lift wheel’s impact is on the darkest portion

of the gradient, with the effect tapering off linearly as it reaches the top of

the waveform.


This symmetry of motion and broad overlap allows for nice, smooth application and

transition of colors, even when working on dramatic grades. These tonal ranges are

ideal for the “filmic” treatment of footage and organic-looking color changes.

**5** Reset the Lift master wheel.


When working with log wheels, the tonal ranges are more restricted to their

respective sections:

|Shadows Midtones Highlights|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|Col13|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||||||||||||||



Low Range High Range


Manipulating the image highlights will have very little impact on the rest of the

luminance because of the small amount of overlap between the highlights and the

midtones ranges.

**6** In the upper right of the Primaries palette, press the rightmost icon in the list of

primaries tools to launch the log wheels.


On the surface, this interface looks almost identical to the color wheels. However,

adjustments to the shadows, midtones, and highlights react very differently.


**Lesson 1 Balancing Footage** **30**


**7** Drag the Highlight master wheel to the left to darken the highlights of the gradient.


The upper half of the waveform bends until it is horizontal, but this has no impact on

the shadows. This behavior is reflected in the viewer, in which the lightest portions of

the gradient are darkened, while the midtones and shadows remain the same.

**8** Drag the Shadow master wheel to the right to brighten the dark ranges.


This time, the lower third of the line rises until it is parallel to the horizon.


With the waveform in this position, it’s easy to see how you can affect the overlap

between the shadows and midtones (low range) and the midtones and highlights

(high range).


**Lesson 1 Balancing Footage** **31**


**9** In the log adjustment controls, drag the Low Range value left to move the shadow

segment of the waveform lower, thereby extending the midtones range.


**10** Drag the High Range value right to narrow the highlight section at the top.


You can also use this gradient image to explore the behavior of color among the

different wheel modes.

**11** Press the global Reset All button in the upper right of the Primaries palette.

**12** In the Primaries color wheels palette, drag the Lift color indicator toward blue and the

Gain toward red to create a dual-tone gradient.


This produces a pleasing transition from the black to the white point of the gradient.

**13** Reset the Primaries palette.


**Lesson 1 Balancing Footage** **32**


**14** In the Primaries log wheels palette, drag the Shadow color indicator toward blue and

the highlight toward red.


In this case, there is a clear separation between the adjustments made within the tonal

ranges, with a still unaffected segment in the middle that describes the midtones.

**15** Reset the Primaries palette.


The Offset wheel affects the luminance of the image uniformly, no matter which

Primaries palette mode you are in.

**16** Drag the Offset wheel to the right to lighten the gradient evenly.

**17** Switch from the log wheels to the color wheels palette and note that the Offset values

have remained the same.


The tool is not only identical in both modes but is actively linked, so any change you

make will be visible in the Offset wheel of either mode.

**18** Reset the Primaries palette.


You can also explore the Contrast parameter and gain a better understanding of what

the Pivot does.


**Lesson 1 Balancing Footage** **33**


**19** Drag the Contrast parameter to the right until you reach the maximum value of 2.0.


This will practically diminish the gradient to just two values: black and white.

**20** Drag the Pivot parameter to redefine the contrast balance.


When looking at this simplified interpretation of contrast, it’s easier to understand

what the Pivot is doing—it is defining the central or “middle gray” value for the

Contrast tool. When Contrast is reset to 1.0, the Pivot parameter does nothing because

the highlights and shadows of the image have not been inversely affected.


For now, we will use it as a creative grading adjustment, but in later lessons, we will

start to look at the importance of understanding and maintaining true middle gray.


TIP Gradients and color bar graphics can be useful for checking the behavior of

various tools and effects in DaVinci Resolve. They can be added to the timeline

from the edit page’s Effects panel. Open Toolbox > Generators, drag any

generator graphic onto the timeline, and then turn it into a compound (right-click >

New Compound Clip) to see it in the color page timeline.


Log wheels can be extremely useful when you’re attempting to change the brightness or

hue of a narrower tonal range. The next exercise will demonstrate a practical use of

switching between color wheels and log wheels.


**Lesson 1 Balancing Footage** **34**


##### **Restoring Shadows Using Log Wheels**

With a better understanding of how you can target different tonal ranges, you can now

combine the different techniques for effective tonal management and balance.

**1** In the Scopes palette, open the Settings and change the waveform back to Y mode

with Colorize deselected.

**2** Switch the Primaries palette back to color wheels mode.

**3** Select clip 07, which shows an image of a mountain range.


The luma waveform indicates there is some room for adjusting the image’s highlights.

**4** Drag the Gain master wheel right to increase brightness until the trace reaches the

second horizontal line from the top.


Even though the waveform appears to be intact, the sunset on the horizon might start

to appear “blown out.” To understand why this is happening, let’s check the Parade

scopes to determine the distribution of color in the image.


**Lesson 1 Balancing Footage** **35**


**5** Switch the Scopes palette to Parade.


Waveform Parade


The Parade scope has a similar function to the Waveform, but it focuses on displaying

the intensities of the individual color channels. You should recognize that the shape of

the trace remains the same as the one in the Waveform but multiplied (and

horizontally condensed) for each channel.


In this instance, although the luma waveform accurately displays the combined

luminance of the image, it does not convey instances of clipping within individual

channels as a result of pronounced chromatic brightness (such as this sunset).

**6** Reset the Gain wheel.


With reliable white and black references in an image, standard procedure is to

neutralize the three channels to achieve balance. Without references, context is

important. In this case, the context is the sunset with its accompanying red skyline,

which requires an exception to the balancing rule.

**7** Switch the scopes back to Waveform. With the highlights analyzed, you can focus on

the overall brightness of the image and the balance of the dark foreground elements.

**8** To brighten the image without clipping its highlights, drag the Gamma master wheel to

the right until you have raised the bottom of the trace between the 128 and 256

graticule lines. By avoiding the Gain master wheel, you’re more likely to prevent the red

highlight from clipping.


The image shadows appear to be compressed along a narrow luminance range, which

is causing loss of detail in the foreground. Adjusting the Lift master wheel will not

sufficiently expand the compressed shadows.


**Lesson 1 Balancing Footage** **36**


**9** To confirm this, drag the Lift master wheel to the left to see how dramatically it affects

the foreground. The compressed shadows are pulled down until the entire image

becomes too dark.


**10** Reset the Lift wheel.

**11** Switch the Primaries palette to log wheels mode.


TIP Press Option-Z (macOS) or Alt-Z (Windows) to toggle between the

Primaries color and log wheels.


**12** Drag the Shadow master wheel to the left to lower the black point without clipping it.

Note that the tree details begin to pop out against the mountains and ground.

**13** In the adjustment controls, drag the Low Range parameter to the left to redefine the

shadow range. Because of this narrower range, adjustments to the Shadow wheel will

be more concentrated to the compressed trace at the bottom of the image.

**14** Drag the Shadow master wheel to the left to further expand the compressed shadows.

Keep adjusting the Low Range and Shadow master wheel controls until you see a good

amount of detail in the foreground of the mountain clip in the viewer.


Because the Shadow wheel is more dedicated to the lower ranges of luminance, it is

not affecting the midtones as dramatically as the Lift wheel did. With the contrast

adjusted, you can now address the colors. This image is particularly tricky because of

the conditions under which it was captured. The sun is still rising, resulting in beautiful

peach, purple, and blue gradients throughout the sky. You will strive to retain these


**Lesson 1 Balancing Footage** **37**


striking hues while balancing the colors in the foreground—most notably, the

magenta in the shadows.

**15** Switch the Primaries palette back to color wheels.

**16** Gently drag the Gamma color balance indicator away from magenta and toward

green/yellow. Stop dragging before the green in the shadows becomes overpowering.


Bypassed Graded


You have successfully brought back a lot of detail to the image foreground, but this came

at the expense of the beautiful gradient in the sky, which now appears a little washed out.

In the next exercise, you will isolate this log grade to the foreground of the image while

reducing its impact on the sky in the background.

##### **Isolating a Grade to a Depth Plane**


Resolve FX are a collection of effects and filters that enable you to adjust the physical or

visual properties of footage in creative ways that are often not possible using common

grading tools. You will learn secondary grading techniques in Lesson 3, but this clip is ideal

for an early demonstration of the restorative power of secondary selection via an effect

called AI Depth Map.


The AI Depth Map effect can automatically analyze and produce a 3D map of a scene,

which can be used to isolate a grade to a specific plane of an environment, such as the

foreground.


NOTE The following exercise requires DaVinci Resolve Studio to complete.


**Lesson 1 Balancing Footage** **38**


**1** In the interface toolbar, click the Effects button to open the Effects panel library.


**2** Scroll down the Effects Library until you find the Resolve FX Refine section.

**3** Drag the Depth Map effect onto corrector node 01 until a + (plus sign) appears and

then release.


The Effects panel switches to the Settings tab, which features the AI Depth Map effect

parameters.


**4** Wait a few moments for the AI Depth Map to run its analysis and output a black-and
white image (called a _matte_ ) of the scene.


**Lesson 1 Balancing Footage** **39**


NOTE If you’re not using DaVinci Resolve Studio, a watermark will appear over

the image. You can dismiss the warning dialog and complete this exercise with

the watermark.


The resulting matte resembles the mountain clip, with the foreground plane appearing

light gray, the mountains a darker gray, and the sky almost completely black. In

addition to mapping the spatial environment of the scene, the matte also represents

the area that a grade or effect will impact. White indicates full opacity, or a selected

region, whereas black indicates transparency, or the lack of selection in that area. Gray

implies semi-opacity and partial selection.


You will adjust the AI Depth Map parameters for a more pronounced selection of

the foreground.

**5** Click the Resulting Map Adjustment header to expand its parameter controls.

**6** Under Resulting Map Adjustment, select the Adjust Map Levels checkbox to gain

access to the Limit and Gamma controls.

**7** Decrease the Near Limit (0.200) to brighten the foreground of the matte.


**Lesson 1 Balancing Footage** **40**


**8** Decrease the Gamma (0.750) to offset the background range.


With the depth map modified to meet the needs of the image, you can now disable the

matte preview in the viewer and review the final result.

**9** Deselect Depth Map Preview at the top of the settings.


The Depth Map tool can be invaluable for quickly and accurately separating

foreground subjects from a scene—such as in interviews or outdoor shoots with

limited lighting. In these cases, you’ll want to soften the result to help blend the

foreground grade into the background.

**10** Expand the Map Finesse header and select Postprocessing to reveal the matte
refining controls.

**11** Increase the Blur (0.750) to soften the edges of the depth map planes.

**12** Drag Contract/Expand left (-1.000) to reduce the resulting halo around the trees.


**Lesson 1 Balancing Footage** **41**


**13** Press Command-D (macOS) or Ctrl-D (Windows) to disable the corrector node and

then re-enable it to compare the corrected image to the original clip. Review and

adjust, if necessary.


Bypassed Graded


As seen in this exercise, you can use Primaries color and log wheels together very

effectively. Color wheels can be used to set an initial tonal range and contrast, while log

wheels can behave like a secondary adjustment that can further refine the three

luminance ranges.


Log wheels are particularly effective when working on underexposed or overexposed

footage. They allow for restorative work in the high and low luminance ranges, as well as

minor tweaks to the brightness and hues of those areas, without majorly altering the

remainder of the image. In cases where unwanted change does occur, you can make use of

secondary tools, like the Depth Map effect, to isolate the grade to the desired area.
## **Self-Guided Exercises**


Complete the following exercises in the 01 Main Timeline to test your understanding of the

tools and workflows covered in this lesson.


**Clip 01** —Use the YRGB curve to normalize the clip and then ungang the channels to

balance. Increase the Saturation parameter in the adjustment controls to bring out the

natural colors in this underlit shot.


**Clip 03** —Use the Contrast and Pivot controls to enhance the details of the scale.


**Clips 05, 06, 09, and 10** —Use the Primaries color wheels and the Waveform scope

to establish the tonal range and contrast on these clips. Balance their colors

where necessary.


**Lesson 1 Balancing Footage** **42**


**Clips 4, 12, 16, and 17** —Use the Curves palette and the Parade scope to establish the

tonal range and contrast on these clips. Balance their colors and increase saturation

where necessary.


When you’ve completed these exercises, open the 04 Completed Timeline to compare your

work to the Lum and Balance nodes in this “solved” timeline.
## **Lesson Review**

**1** Does a DaVinci Resolve archive (.dra) contain the original project media?

**2** What does the Y in YRGB represent?

**3** What does the Pivot parameter in the adjustment controls do?

**4** How do you add additional control points to curves?

**5** What is the difference between the Primaries color and log wheels?


**Lesson 1 Balancing Footage** **43**


##### **Answers**

**1** Yes. Archived projects (.dra) consolidate all related project media within a single folder

that can be restored through the Project Manager.

**2** The Y in YRGB refers to luminance.

**3** The Pivot sets the contrast balance, or “middle gray” point.

**4** Click directly on a curve to add a new control point. Shift-click to add a new control

point without adjusting the curve’s position.

**5** The Primaries color and log wheels target different tonal ranges of the image. Primary

wheels tend to have a broader impact on the image, while log wheels are more

restricted to their respective tonal ranges.


**Lesson 1 Balancing Footage** **44**


### Lesson 2
# Creating Color Continuity



When editing footage for a video

project, the end goal is often to create

a single running narrative that appears

to be happening in real time. Much

of the time—even in documentary

filmmaking—this unity of time is

an illusion. Materials for a single

scene can take days or even weeks

to photograph, which can result in

fluctuations in light, temperature, and

color cast as both environmental and

technical factors influence the footage

from one day to the next.


The goal of shot matching is to assess

how multiple clips compare to one

another when placed on a timeline

and to ensure that they maintain color

continuity. When shots don’t match,

the audience becomes aware of their

artificial sequencing, which breaks the

illusion of cinema and compromises

the viewer’s suspension of disbelief.



Time

This lesson takes approximately
2 hours to complete.

Goals

Building a Shot-Matching
Strategy 46

Organizing Shots Using Flags
and Filters 48

Applying Shot Match 52

Matching Shots Using Stills 54

Comparing and Matching
Shots Manually 61

Self-Guided Exercises 70

Lesson Review 71


In the previous lesson, you looked at the most common tools and workflows for

normalizing and balancing shots in preparation for a grade. In this lesson, you’ll examine

the shot-matching process using many of the same tools.
## **Building a Shot-Matching** **Strategy**


Your approach to shot matching will usually depend on the nature of the footage.


On a narrative production that was shot by an experienced cinematographer and camera

crew, the quality of the raw content can have a reliable consistency throughout and require

minimal balancing and matching.


For documentaries, fluctuation in locations, light sources, and temperatures (not to

mention the use of multiple different cameras) may require much more diligent

footage preparation.


It is normal to incorporate both balancing and shot matching during the first primary

grade pass. You may opt to treat these as separate jobs and apply them to independent

nodes, or you can forgo balancing on shots that you are matching to a single “hero” shot

in a scene.


Your shot-matching strategy can be narrowed down to the following approaches and

considerations:


- **Balance all shots in a sequence.** The workflow assumes a shot-by-shot approach to

normalization and balancing in order to produce a visually uniform sequence. This

time-consuming method is best applied to projects with vastly mismatched media

sources or lighting conditions (archival documentaries, festival promo videos,

and so on).


Every clip balanced individually


- **Adjust only mismatched shots in a sequence.** If only one or two shots in a sequence

are mismatched, it makes sense to adjust only those shots to create an even starting

point for the scene grade. This approach is more common to standard


**Lesson 2 Creating Color Continuity** **46**


grading practices and usually applies to pick-up shots captured on a different day or

stock footage captured by a third party.


Mismatched clips graded to match the rest of the sequence


- **Select a single reference shot (a hero) in a mismatched sequence.** Sometimes you

will have more than one clip that is a good candidate for a reference (for example,

when working with footage from a three-camera shoot, or from a 2-day outdoor

production). In those cases, you may opt to use a hero shot that will have the least

extreme impact on the color tone of the other clips.


Clips adjusted to a hero shot that causes the least color distortion


Or you might consider settling on the clip that is closest in appearance to your

intended grade. In doing so, any further creative grading you perform will aim to

enhance the colors and not undo them.


Clips adjusted to a hero shot that is closer to the final intended look


TIP When choosing a hero shot, it’s best to select an establishing shot or any

wide or long shot of the scene and match all other angles to it. A wide shot is

likely to have the best overall representation of light sources and shadow

tones, as well as include most of the physical elements in the scene, such as

actors, costumes, set design, walls, and so on. In contrast, a close-up might

contain less reliable data for balancing and might share few elements with

other shots.


**Lesson 2 Creating Color Continuity** **47**


The exercises in the following lessons will focus on the practical implementation of shot

matching based on these methods. Understanding the variety of matching methods

available in DaVinci Resolve 20 will enable you to construct grading workflows that are

best suited to your coloring abilities and project type.
## **Organizing Shots Using Flags** **and Filters**


In the previous lesson, you scrolled, searched, and clicked individual clips throughout the

timeline. This is generally not an issue in small projects, but if the edit had several hundred

clips, you might find this method time-consuming and prone to errors/missed clips.


DaVinci Resolve features many organizational tools that will help you filter your timeline

based on a variety of technical and narrative specifications. One of those tools, called a

_flag,_ can help you manually define and search for clips based on any criteria you choose.

For example, you might flag clips that have overexposed skies, clips that require green
screen keying, or clips that need narrative-specific dynamic grades.

**1** In the timeline menu above the viewer, open the **02 Balanced** Timeline.


The timelines in this project already include some flags. You’ll add a few more to

identify the clips you will use for the matching exercises in this lesson.

**2** In the timeline, right-click clip 04 and select Flags > Green.


A green flag appears in the upper left corner of the clip thumbnail to indicate that the

clip is flagged.


Another method for applying flags is to use a keyboard shortcut.


**Lesson 2 Creating Color Continuity** **48**


**3** Select clip 05.

**4** Press G on your keyboard to add a flag.


While this is a faster technique for applying flags, in this case it applied the wrong

color flag.

**5** To change the flag to green, double-click the blue flag on the thumbnail to open the

Flags dialog.


Notice that the Flags dialog allows you to add notes to flags, which is very handy for

detailing future grading intentions or identifying technical issues.

**6** Select the green-colored flag and click Done to close the dialog.


The keyboard shortcut is configured to apply the default blue flag. To change the

default color, you’ll need to change the flag color in the toolbar of the edit page.

**7** Go to the edit page.

**8** In the toolbar, next to the flag icon, click the disclosure arrow

and choose Yellow.


TIP When setting a new default flag color, make

sure that none of the clips on the timeline are

selected. If a clip is selected while a new color is

picked, that clip will be flagged.


**9** Return to the color page.


**Lesson 2 Creating Color Continuity** **49**


**10** Select clip 04 and hold Command (macOS) or Ctrl (Windows) to select clip 06 at the

same time.

**11** Press G to apply yellow flags to both clips.


TIP You can apply a flag to a sequential range of clips by selecting the first

clip, holding the Shift key, and then clicking the last clip. You can then use any

of the methods described to apply the desired flag to the selected clips.


The green flags in the timeline now identify the clips you will be working on

throughout this matching lesson. You’ll find it easier to locate and navigate between

them if you filter the timeline to show only the green-flagged clips.

**12** In the interface toolbar at the top of the color page, click the disclosure arrow next to

the Clips button and choose Flagged Clips > Green.


TIP When a filter is applied to a timeline, the Clips button is underlined in red

to serve as a visual reminder that some clips in the timeline might not be

visible due to the filter.


**Lesson 2 Creating Color Continuity** **50**


You have temporarily hidden all clips that do not have a green flag. The result is a

significantly simplified timeline that will help you focus on those clips without the need

to navigate around your timeline and locate them.


TIP As with flags, you can also use markers for filtering purposes. The

difference is that flags identify an entire clip (and its source media), whereas

markers identify a specific frame or range of time. Adding a flag to a clip

applies it to every appearance of the source clip in all the timelines of the

project, whereas markers will appear only in that single instance of the clip in

the timeline. Markers can be applied using a keyboard shortcut (M), and their

default colors can also be set in the toolbar of the edit page.


**13** To add to your filter selection, click the disclosure arrow next to the Clips button and

choose Flagged Clips > Yellow.


As you likely noticed in the previous steps, clips can be assigned more than one flag

color. As a result, media classifications can overlap, allowing you to filter clips that have

several workflow roles.

**14** In the Clips dropdown menu, choose Yellow again to remove the yellow flags from

the clip filter.


TIP To reset the Clips filter, choose All Clips at the top of the list.


In DaVinci Resolve, flags and filters can perform a wide variety of functions. You can use

different flag colors to identify clips that must be reframed due to a visible boom

microphone, single out clips that need white balancing, or isolate clips that require a

flashback look. When the timeline is filtered based on flag color, you can focus on

addressing just one category of clips at a time.


**Lesson 2 Creating Color Continuity** **51**


## **Applying Shot Match**

The Shot Match function in DaVinci Resolve analyzes the colors in one image and

reconfigures the primaries of another image (or multiple images) to match it.


The results of any automatic grading function should be carefully evaluated because an

algorithm is unable to recognize the environmental factors behind scene colors. Even so,

the Shot Match function can be a great starting operation when matching clips and can

enable you to quickly prepare shots for on-set review or when processing dailies.

**1** In the green flag-filtered timeline, select clip 01.


You will match the colors in this clip to the ones in clip 02 directly after it. In the interest

of organization and preservation of the video signal, you will keep the balance and

color match on separate nodes.

**2** In the Node Editor, create a new serial node by right-clicking node 01 (Balance) and

choosing Add Node > Add Serial or by pressing Option-S (macOS) or Alt-S (Windows).


It is good practice to label your nodes to keep track of their function and your

overall workflow.


**Lesson 2 Creating Color Continuity** **52**


**3** Right-click the new node and choose Node Label. Name the node **Shot Match** .


**4** Without leaving clip 01, right-click clip 02 and choose “Shot Match to This Clip.” It will

take a few moments for the shot match analysis to be performed and applied to the

active clip 01.


NOTE If you cannot see “Shot Match to This Clip” in the contextual menu of a

clip, it is possible that you are right-clicking the active clip and not the clip you

are trying to match to.


**5** Press Command-D (macOS) or Ctrl-D (Windows) to disable and enable the Shot Match

node to review the adjustment.


TIP Press Shift-D to bypass the entire node tree and compare your work to

the source footage. You can also bypass entire color pipelines by pressing the

Bypass Color Grades and Fusion Effects button in the upper right of

the viewer.


The result is a much better match between the two images. Clip 01 becomes warmer

and less contrasted to match the environment in clip 02. However, the shadows could

be darkened to better match the mountains and the details in the animals, and the

gamma could be brightened and cooled to remove the strong red tones.

**6** Drag the Lift master wheel left until the shadows of the waveforms in clips 01 and 02

match more closely.


**Lesson 2 Creating Color Continuity** **53**


**7** Drag the Gamma master wheel right to brighten the image and increase contrast in

the details.

**8** Drag the Gamma color wheel indicator away from red until the rhinos appear more

neutral in color.


Before match


After match


Automatic shot matching can be helpful for creating a starting point for manual matching

and to quickly resolve mixed camera issues in front of clients. But ultimately, you should

still learn how to assess images using the video scopes and manually match them with the

primary grading tools. This will give you greater confidence when working with media that

automatic tools struggle with, such as scenes with unconventional lighting or

environments with context-dependent visual cues.
## **Matching Shots Using Stills**


Stills have a variety of functions in DaVinci Resolve, as you will learn in lessons throughout

this book. One of the most direct uses of stills is for visually comparing clips in the viewer.


By superimposing a still, or snapshot, of a previous clip onto a current clip, you can visually

assess their differences in contrast, saturation, and color dominance.


In this exercise, you will use stills to manually match clips.


**Lesson 2 Creating Color Continuity** **54**


**1** In the green flag-filtered timeline, select clip 05.


In the 02 Balanced Timeline, this clip already has its tonal range and balance set via the

Primaries color wheels.

**2** Right-click in the viewer and choose Grab Still.

**3** Double-click under the still that appears in the gallery and label it **Match Reference** .


NOTE The numbers under the stills refer to the timeline track, the clip

number, and the number of stills generated for that clip.


**Lesson 2 Creating Color Continuity** **55**


**4** In the timeline, select clip 06. You will use the Primaries color bars and the Parade

scope to match this shot to the still.


**5** In the Scopes mode pop-up menu, choose Parade.

**6** In the Gallery window, double-click the Match Reference still.


You should now see the two clips in the viewer, separated by a wipe line that

you can drag.


**Lesson 2 Creating Color Continuity** **56**


A set of controls appears in the upper left corner of the viewer, allowing you to change

your wipe style.


TIP You can invert a wipe using the keyboard shortcuts Option-W (macOS) or

Alt-W (Windows).


The shot of the man by the fence is much cooler than the still with the men and the

horse. The Parade scope, which is also split in half, objectively shows this difference.


The reference still’s blue channel trace appears substantially lower, indicating an

absence of blue in the highlights and upper midtones. As blue’s complementary color

is yellow, this results in the reference image looking warmer.


When shot matching, the goal is not to fully match the parades to each other. That is

usually impossible because of the different contents of the frames. Instead, you must

study how the three channels relate to each other and try to re-create their respective

proportions in the clip that you’re matching.

**7** In the node graph, change the label of node 01 in clip 06 to **Match** .


**Lesson 2 Creating Color Continuity** **57**


TIP Labeling nodes has many benefits. Labels clarify the grading workflow by

specifying each node’s task, which enables you to make faster adjustments as

you grade.

To label nodes more quickly, consider creating a custom keyboard shortcut.

Open DaVinci Resolve > Keyboard Customization. Find the Label Selected

Node command in the Commands list (use the search field, if necessary),

select the Keystroke field, and press the keyboard shortcut you wish to

associate with the command. The Tab key is a good option because it is not

assigned to any default command.


**8** In the Primaries palette, switch the mode to Color Bars.


The bars are an alternative representation of the color wheels, and changes in either

mode will reflect in both modes. The bars offer greater precision over the individual

color channels of the image than the wheels.

**9** To match the shadows, drag the Lift Y (luma) bar down until the shadows of clip 06

match the shadows in the reference still. Keep your eye on the green parade and aim

to set the lowest point of clip 06’s trace (the man and dog) to a similar level as the

shadow in clip 05 (the men and horse).


TIP Use the scroll wheel of your mouse to adjust the Primaries color bars with

more precision.


**Lesson 2 Creating Color Continuity** **58**


**10** Drag the Gain Y bar down until the arc in the green highlights matches across the

two shots.

**11** Drag the Gamma Y up slightly to match the midtone section of the green parades.


The reason you are using the green channel as the starting point for the overall

balance is because the green channel has the most substantial impact on the

combined luminance of the image (over 70%), with red having significantly less

influence (20%) and blue having even less (under 10%). Therefore, adjustments to

the green channel will have a nearly global impact on the signal, while red and blue

changes will be more confined to their respective channels.


The next step is to address the overall balance to match the reference.

**12** Drag the Red and Blue Lift bars to match their respective shadows to the

reference parade.

**13** Drag down the Blue Gain bar until the tops of the blue parades align.

**14** Drag up the Red Gain bar to match the warmer reference look.

**15** Finally, drag up the Red Gamma bar to match the trace pattern in the middle of the red

parade. If needed, return to the Red Lift and Gain bars to compensate for changes in

the red parade spread.


The result is a quick matching of the two clips using the Primaries color bars.


**Lesson 2 Creating Color Continuity** **59**


**16** To turn off the reference wipe, in the upper left of the viewer, click the Image Wipe

button or open the viewer options in the upper right and choose Show

Reference Wipe.


**17** Disable and enable the match grade to compare clip 06 before and after the manual

matching adjustment.


Before match


After match


With the clips matched, you can now apply creative grades to them and continue to

see consistent results.

**18** Select clip 05.

**19** In the Node Editor, locate the Contrast node and click the number 02 in the lower left

corner to enable it. The image in the viewer will shift to display deeper shadows and

more detailed midtones.

**20** Select the Contrast node and choose Edit > Copy or press Command-C (macOS) or

Ctrl-C (Windows).

**21** Select clip 06.

**22** Right-click the Match node and choose Add Node > Add Serial.


**Lesson 2 Creating Color Continuity** **60**


**23** Select the newly created node and choose Edit > Paste or press Command-V (macOS)

or Ctrl-V (Windows).


Clip 06 adopts the same level of contrast because of the successfully matched tonal

ranges and colors in the first node.


NOTE The Y (luminance) bar of the Primaries color bars affects the image

differently than the master wheel. Like the YRGB curve, the master wheel

affects all RGB channels, which impacts saturation, whereas the Y bar targets

only luminance.


When using stills for shot matching, your grading becomes even more precise when used

in conjunction with video scopes. This is because scopes display an objective measure of

the luminance and color values of each frame, allowing you to make informed adjustments.


Stills have the additional benefit of containing the grading data of the clips they were

generated from. In later lessons, you will use this data as a starting point for grading other

clips or for applying grades across entire scenes.
## **Comparing and Matching** **Shots Manually**


You don’t always need to generate a reference still in the gallery for wiped-shot matching.

In this exercise, you will extract a reference directly from the timeline and match the

images using custom curves.

**1** In the green flag-filtered timeline, select clip 04. You will match this clip to the

previously balanced clip 03.

**2** Review the Parade scope for clip 04.


**Lesson 2 Creating Color Continuity** **61**


You can see distinct differences in the shapes of the three channels. The red channel

has the widest spread, extending beyond the green and blue channels in both the

shadows and highlights. The blue channel’s highest point is almost level with the green

channel’s highest point, although it is far more compressed in the midtone range.

**3** Select clip 03 and review its parade.


The most obvious difference is in the overall spread and contrast of the three color

channels. The shadows extend to the bottom of the scopes graph, with the red and

blue shadows even touching the black point line (0).


In this situation, visual evaluation of the frame is vital. By understanding the context of

the image, you can choose to ignore certain properties of the graph. Clip 03 contains a

variety of elements that are not visible in the close-up in clip 04. The trees and field

silhouetted against the mountains appear as bunching at the bottom of the parades

and can be safely ignored. You can choose to omit such elements from the scopes

when shot matching.

**4** Select clip 04.

**5** Right-click clip 03 and choose Wipe Timeline Clip.


Both clips become visible in the viewer at the same time, divided by the wipe line.


TIP Quickly toggle the wipe on and off by pressing Command-W (macOS) or

Ctrl-W (Windows). Some colorists move the wipe to the edge of the viewer in

order for the reference to fill up the whole screen and toggle the wipe

continuously as they match the grade in the active clip.


**Lesson 2 Creating Color Continuity** **62**


In the timeline, a blue highlight indicates that clip 03 is currently being used as a

reference.


One way to help you focus on the relevant elements of the parade is to reframe the

reference clip within the viewer. Clip 03 is a much wider shot than clip 04, so you can

zoom in and reposition it for a better representation in the Parade scope.

**6** In the middle palettes, click the Sizing button to open the Sizing palette.


**7** In the palette’s upper right corner, choose Reference Sizing mode.


**Lesson 2 Creating Color Continuity** **63**


The Reference Sizing tool applies the transform changes only to the reference image in

the viewer, not to the actual clip in the timeline.

**8** Use the Sizing controls to zoom in to the reference image (by a factor of about 9.000).

**9** Pan the image to the left and tilt the image down until the framing starts to match that

of clip 04.


These transform changes place the reference image into a much better position for

both visual evaluation and for a more usable Parade scope trace.


The side-by-side parade comparison reveals that the reference image has some minor

discrepancies, such as the stronger presence of red in the upper midtones and a lower

blue channel trace.


When matching, remember that it’s generally impossible to re-create the exact shape

of the graphs themselves. Instead, you should focus on matching the height, depths,

and the midtone distributions of the traces.


**Lesson 2 Creating Color Continuity** **64**


**10** In the Node Editor, label node 01 **Match** .

**11** Open the Curves palette.


Let’s perform a few adjustments to see how curves affect the parades.

**12** Isolate the R curve and drag the white point left and the black point right until the red

channel in both parades has an equal spread.

**13** Isolate the G curve and drag the black point to the right.


As you drag the green control point, the two other channel parades begin to shift,

affecting the output of the entire image. This happens because, by default,

DaVinci Resolve tries to keep the luminance of the image constant when you adjust the

individual RGB channels in the Curves and Primaries palettes. Because each channel

contributes to the overall brightness of the image, changing the strength of one

channel forces the other two channels to compensate for the shift in luminance.


This behavior is usually advantageous when performing creative color grading

because it allows you to focus on designing a look for your scene without offsetting

the brightness or contrast. However, when shot matching, this behavior can be

counterproductive. To manipulate each channel independently, you need to indicate to

DaVinci Resolve that you do not wish to maintain constant luminance.

**14** Open the Primaries palette and set the mode to Color Wheels.

**15** In the lower right corner of the adjustment controls, drag Lum Mix down to 0.


TIP In the Project Settings, you can set Lum Mix to default to a value of 0 on

every clip. Click the gear icon in the lower right corner of the workspace to

open the Project Settings window and go to General Options > Color and

choose “Luminance mixer defaults to zero.”


With the channels behaving independently, you can attempt to match the curves

once again.

**16** Reset the Curves palette.


**Lesson 2 Creating Color Continuity** **65**


**17** Isolate the R curve again and drag the black and white points until the red channel in

both parades has an equal spread.


**18** Isolate the G curve and reposition the black and white points to align the

green parades.


**19** Isolate the B curve and reposition the black and white points to align the blue parades.


It appears that the parades now equally match each other, but the colors in clip 04 still

do not match the reference in the viewer. This is because you have focused only on the

highlights and shadows of the images. The midtones are equally important and can

have a profound impact on image appearance.


Notice the bunching in the lower midtones of the channels. It represents the

mountains in the image. Although the red and blue channels are aligned, the green

channel is mismatched between clips 04 and 05.


**Lesson 2 Creating Color Continuity** **66**


**20** Add a control point to the green curve and drag until the midtones of the

green channel line up more accurately. Adjust the green curve’s black and white

points if necessary.


The match between the two parades results in a satisfactory visual similarity in the

mountains and the sky. However, you can now continue to assess the match by eye

and further refine the result.


The close-up shot could use some contrast to create greater depth between the

mountain ranges in clip 04. This difference in contrast is represented by much finer

discrepancies in the clips’ parades that are too minor to target with primary

grading tools.

**21** In the adjustment controls, tweak the Contrast to complete the match between

the clips.

**22** Open the Sizing palette. In Reference Sizing mode, click the reset arrow to return the

reference image to its original placement.


If you do not perform this reset, all future reference images, including wiped stills from

the gallery, will have the same transform placement in the viewer.

**23** Disable the image wipe.

**24** Toggle between clips 03 and 04 to verify that the match is successful.


When matching clips using the scopes, aim to equalize the heights and depths of the

pixel spread and then detect any apparent bunching or mismatching in the midtones

to address any remaining color issues. By displaying an exact readout of the RGB

values of each clip, scopes can help you remove the guesswork that might accompany

the minute tweaking of midtone ranges and allow you to approach the image from a

more empirical yet creative mindset.


**Lesson 2 Creating Color Continuity** **67**


##### **Using Split-Screen Views to Compare Clips**

An alternative method of visually comparing clips within the viewer is by using a split
screen display. Instead of overlaying and wiping the still of a single image, you can display

the media from multiple clips side by side. The media you use could be from other clips in

the timeline, stills in the gallery, different versions of grades (Lesson 6), or other clips in the

same group (Lesson 7).


This comparison method is especially effective when you already have a collection of

clips that are similar in appearance and you need a wider visual reference of a scene

or environment.

**1** In the green flag-filtered timeline, select clip 07. This clip is already balanced with

custom curves.

**2** Shift-click clip 10 to highlight clips 07 to 10.


**3** In the upper left of the viewer, click the Split Screen button or open the viewer options

in the upper right and choose Split Screen > On.



**Lesson 2 Creating Color Continuity** **68**


**4** In the upper left dropdown menu, choose Selected Clips to display all four clips.


**5** In the viewer, click the upper right image to select clip 08 on the timeline. The selection

is indicated by a white outline in the viewer and an orange highlight in the timeline.


Changes made to the color page palettes will impact whichever clip is actively selected

in the split-screen view. You can perform approximate grade matching by switching

between clips in split-screen view, visually comparing them, and making quick

adjustments in the Primaries color wheels and curves.


Reading scopes and evaluating their data can be a straightforward process, but it still

requires a lot of practice to develop a critical eye and grade with finesse. Over time, you

will gain a better intuition for which sections of the trace should be used and which can be

ignored for better adjustment of highlights, midtones, and shadows. Shot matching is a

highly valued skill set that requires plenty of patience and experience, so keep at it!


**Lesson 2 Creating Color Continuity** **69**


## **Self-Guided Exercises**

Complete the following exercises in the green flag-filtered 02 Balanced Timeline to test

your understanding of the tools and workflows covered in this lesson.


**Clips 08, 09, and 10** —Match these clips to clip 07 using any of the methods covered in this

lesson. For an added challenge, try matching each clip using every method covered in this

lesson (Auto Shot Match, Primaries color bars, and Curves) to gain a better understanding

of their usage and to develop your personal grading preferences.


When you’ve completed these exercises, open the 04 Completed Timeline to compare your

matching to the Match nodes in this “solved” timeline.


**Lesson 2 Creating Color Continuity** **70**


## **Lesson Review**

**1** How can you filter a timeline to show only clips with a flag?

**2** When performing an automatic shot match, you might right-click the clip you have

selected and _not_ see “Shot Match to this Clip” in the contextual menu. Why?

**3** True or False? It is possible to use a timeline clip as a reference in the viewer without

first creating a still.

**4** How do you prevent changes made to one color channel from affecting the waveform

trace of the other two channels?

**5** Which viewer mode allows you to see multiple clips in the viewer at the same time?


**Lesson 2 Creating Color Continuity** **71**


##### **Answers**

**1** Click the disclosure arrow next to the Clips button and choose Flagged Clips.

**2** The clip you have selected is the one that will be receiving the automatic shot match

adjustment, so “Shot Match to this Clip” cannot be an option. Right-click any other clip

on the timeline and “Shot Match to this Clip” will appear in the contextual menu.

**3** True. To do so, right-click a clip in the timeline and choose “Wipe Timeline Clip.”

**4** In the Primaries palette, set Lum Mix to 0.

**5** Split Screen mode allows you to see multiple clips in the viewer at once.


**Lesson 2 Creating Color Continuity** **72**


### Lesson 3
# Correcting and Enhancing Isolated Areas



After balancing and shot matching,

you might need to target details in the

shots for more specific enhancement.

This is the secondary color
grading stage.


Secondary color grading is not a

standardized phase of the color

grading process. Instead, it is a needs
driven component of the workflow

that is utilized only when a shot

requires it. It enables you to achieve

a wide variety of goals that improve

the overall aesthetic and creative

quality of the footage, as well as to fix

continuity errors.


In the first part of this lesson,

you’ll review some of the common

applications of secondary grading

using qualifiers and windows.

Your goal will be to isolate areas

of the image for color and effect

enhancement with the purpose of

attracting the viewer’s eye.



Time

This lesson takes approximately
4 hours to complete.

Goals

Controlling the Viewer’s Eye 74

Sharpening Key Elements 84

Fixing Overcast Skies 92

Warping Color Ranges 108

Enhancing Skin Tones
with Face Refinement 118

Adjusting Skin Tones Manually 129

Self-Guided Exercises 138

Lesson Review 139


In the second part of this lesson, you will use more nuanced tools to clean up overcast (or

overblown) skies, adjust regions of an image based on hue, and calibrate skin tones to

produce smoother, more natural results for the subject. Throughout the lesson, you will

also employ some of the tools available in the Effects panel to see how subtle adjustments

can exert an enormous effect on the emotional impact of an image.
## **Controlling the Viewer’s Eye**


A film’s musical score and sound effects can have a resounding impact on audience

perception. Similarly, color and light play a critical role in manipulating the way an audience

interprets a scene. In this lesson, you will focus on the fine art of shaping light to control

the viewer’s eye.

##### **Drawing Attention Using** **Windows and Saturation**


A simple alteration can dynamically reimagine the composition and mood of a shot. In this

exercise, you’ll enhance the saturation in the vibrant, sunlit area of a field to give a scene a

more dramatic feel.

**1** In the Project 01 - Disunity Documentary project, open **03 Matched** Timeline.

**2** In the Clips pop-up menu, choose All Clips to remove the green filter in the timeline.

**3** Filter the timeline to show only those clips with yellow flags.


**4** In the yellow flag-filtered timeline, select clip 07. The clip already has a first node

labeled Lum.


**Lesson 3 Correcting and Enhancing Isolated Areas** **74**


**5** Create a second node and label it **Sunlight** .

**6** In the central palettes toolbar, click the Window palette button. You’ll use a Power

Window to specify the region of the image you will grade.

**7** Click the Linear window button to activate it. It’s the square-shaped window at the top

of the preset windows list.


When activated, the button has an orange outline, and you will see the onscreen

window controls in the viewer.

**8** Double-click to the right of the window button thumbnail and enter the name

**Sunlight Area** .


**9** Use your mouse scroll wheel in the viewer or press Command-- (minus sign) in macOS

or Ctrl-- (minus sign) in Windows to zoom out. This will allow you to maneuver the

window’s control points beyond the image frame.


TIP In addition to using your mouse scroll wheel to zoom in and out of the

viewer, you can click your middle mouse button and drag to pan. If you do not

have a middle-mouse button, hold Ctrl (macOS) or Command (Windows) and

scroll to move vertically in the viewer and hold Shift-Command (macOS) or

Shift-Ctrl (Windows) and scroll to move horizontally. To reset the viewer, press

Z on your keyboard.


**10** In the viewer, move the four edges of the window to select the entire horizontal middle

of the image where the sun hits the ground. Make sure to adjust the shape to mimic

the path of the sunlight.


**Lesson 3 Correcting and Enhancing Isolated Areas** **75**


**11** In the viewer, drag the red points of the window outline to increase the softness

around its upper and lower edges.


**12** To review your Power Window selection, click the Highlight button in the upper left

corner of the viewer.


The viewer shows the part of the image that will be affected when you begin grading

in this node and turns the area outside of this selection gray.


**Lesson 3 Correcting and Enhancing Isolated Areas** **76**


**13** Click the Highlight button again to disable highlight mode and return to your

full frame.


With the secondary selection created, you can begin to grade the image.

**14** In the Primaries palette, increase the Sat to 65 and the Contrast to 1.1.


TIP Toggle the onscreen window controls in the viewer by pressing Shift-~

(tilde) on your keyboard. You can use this keyboard shortcut to hide the outline

and better see the impact of your grade on the image.


This small change dramatically amplifies the golden sunlight in the scene and draws

the viewer’s eye to the ranger in the foreground and the rhinos he is protecting. Next,

you will reduce focus on the non-essential details around them.

**15** With the Sunlight node still selected in the Node Editor, right-click it and choose Add

Node > Add Outside or press Option-O (macOS) or Alt-O (Windows). This inverse

selection will allow you to grade the environment around the Sunlight Area window.

**16** Label node 03 **Outside** .


One of the greatest benefits of working with nodes is the live nature of their video and

key signal connections. The Outside node is directly using the previous node’s key

(selection) data, so if you were to make changes to the Sunlight Area window in the

Sunlight node, it would immediately reflect on the key of the Outside node.

**17** Drag the Gamma master wheel (-0.05) to decrease the brightness and reduce the

Contrast (0.900).


**Lesson 3 Correcting and Enhancing Isolated Areas** **77**


Doing so creates a dark framing effect around the figure of the man and further draws

the eye toward the sunlight on the field.


Before


After


**Lesson 3 Correcting and Enhancing Isolated Areas** **78**


##### **Mimicking a Shallow Depth of Field**

The Tilt-Shift Blur in the Effects panel imitates the look of a shallow-focus lens to direct the

audience’s attention. With it, you can achieve effects that a lens could not—such as

reducing the focus of elements contained within the same focal field and selecting the blur

type, amount, and angle.


NOTE The following exercise requires DaVinci Resolve Studio to complete.


You will continue to work on clip 07 in the yellow flag-filtered timeline.

**1** Create a new serial node (node 04) and label it **T** ilt Shift.

**2** In the interface toolbar, click the Effects button.

**3** In the Effects Library panel, under Resolve FX Stylize, locate the Tilt-Shift Blur effect.

**4** Drag the Tilt-Shift Blur effect onto the empty Tilt Shift node.


The Effects Library switches to the Effects Settings panel in which you can tweak the

Tilt-Shift Blur effect controls.

**5** In the Settings panel, in the Depth of Field category, select Depth Map Preview to

review the matte map.


You encountered a Depth Map previously in Lesson 1. As a reminder, the matte

represents the area where an effect is applied. White indicates full opacity, black

indicates complete transparency, and grayscale is the range of semi-opacity

between the two values.


Currently, the map is level with the horizon and is successfully targeting the rhinos in

the background. However, it is not an entirely realistic composite. The depth of field is

too extreme at the top and bottom of the image, while still maintaining focus on both

the man in front of the camera and the rhinos hundreds of yards in front of him.


**Lesson 3 Correcting and Enhancing Isolated Areas** **79**


TIP Repeatedly select and deselect Depth Map Preview to visually assess the

position of the Tilt-Shift Blur matte in relation to the image when determining

the placement of the Tilt-Shift effect.


**6** Adjust the matte spread by dragging the In-Focus Range pointer to the right (0.330) to

include more of the man in the focused range of the shot.

**7** Adjust the vertical position of the matte by dragging the Center Y value down (0.460) to

ensure that the area directly behind the rhinos goes softly out of focus.

**8** Deselect Depth Map Preview.

**9** Slightly decrease the Near Blur Range (0.590) and Far Blur Range (0.590) values to

reduce the severity of the blur and produce a more realistic result.


Before


After


**Lesson 3 Correcting and Enhancing Isolated Areas** **80**


##### **Focusing Attention with Vignettes**

In filmmaking, a _vignette_ refers to the darkened edges of a film frame that are usually

created as a result of the matte box casting a shadow on the camera lens. With the

advancement of camera and lens equipment, natural vignettes are no longer an issue.

However, their absence has caused an appreciation for the framing service they provided,

and vignettes are now sought after for both creative and compositing purposes as an

effective method of directing the viewer’s eye.


In this simple exercise, you will apply a circle window to a shot and reduce the brightness

of the area around it to create a vignette around the central subject. You will continue to

work on clip 07 in the yellow flag-filtered timeline.

**1** Create a new serial node (node 05) and label it Vignette.

**2** In the Window palette, click the Circle window button.

**3** Ensure that the viewer’s onscreen controls pop-up menu (in the lower left

of the viewer) is set to Power Window.


Vignettes are usually elliptical since that reduces their visibility and makes it easier to

seamlessly blend them into the footage, as compared to shapes with straight lines

and corners.

**4** Double-click the layer name field next to the circle window and type **Vignette Frame** .

**5** Use the onscreen transform controls to reposition and rescale the circle to completely

fill the viewer frame.

**6** In the onscreen controls, drag one of the red points to create a wide, soft edge around

the selection.


In the Node Editor, the Vignette node thumbnail preview shows that you have selected

the subjects in the center of the frame. To use the node as a vignette, you will need to

invert this selection.


**Lesson 3 Correcting and Enhancing Isolated Areas** **81**


**7** In the viewer’s Window palette, on the right side of the circle window row, click the

invert icon.


**8** In the onscreen controls pop-up menu, choose Off to hide the window outline.

**9** With the vignette shape created, you can proceed to use the primary grading tools to

create a vignette effect on the image. Reduce the brightness of the selected area by

dragging the Gamma master wheel to the left (-0.05). Using the gamma tonal range

will ensure that you are not darkening overly bright areas of the footage, such as the

overcast sky, which would make the vignette too obvious.


TIP Vignettes are most effective when they are subtle. If you’re concerned

that your vignette may be too prominent, review the thumbnail of the clip in

the timeline to determine whether the vignette is overly pronounced in the

corners. If so, raise the Gamma back up to reduce its strength or further

soften the Power Window’s edges to blend it more seamlessly into the image.


You can also save the vignette you just generated for future use as a preset.

**10** In the Window palette, ensure that the appropriate window (Vignette Frame) is

selected in the window list.

**11** In the upper right corner of the palette, click the Options button and choose Save as

New Preset.

**12** Enter the preset name as **Vignette** .


From now on, when you want to apply this exact shape to a node in any other clip, you

need only access the Window palette option menu and choose the preset Vignette.


TIP A Vignette Effect is also available in the Effects Library (in the Resolve FX

Stylize category) for quick application of a simple, customizable vignette.


It takes careful consideration and assembly of secondary grading to draw the eye of the

audience without calling attention to the image manipulation. When an audience becomes

aware of the colorist’s handiwork, it can break the illusion of realism and compromise

immersion in the narrative.


**Lesson 3 Correcting and Enhancing Isolated Areas** **82**


**Lesson 3 Correcting and Enhancing Isolated Areas** **83**


## **Sharpening Key Elements**

The Blur palette in the central palettes of the color page contains a Sharpen mode. It

works best when used sparingly and when applied at the end of a grading pipeline. Too

much artificial sharpening can introduce image artifacts and stand out for the wrong

reasons. When used precisely, sharpening can make details look more dynamic and draw

the viewer’s eye to a desired object.

**1** In the yellow flag-filtered timeline, select clip 06.


The clip begins with a man’s hand obscuring the shot. In such cases, it’s a good idea to

play through the clip until you find a better starting point for grading and

adding effects.

**2** In the viewer jog bar, drag the playhead to the center of the clip.


**Lesson 3 Correcting and Enhancing Isolated Areas** **84**


**3** Create a second node and label it **Sharp** .

**4** In the central palettes, open the Blur palette.


**5** In the upper right corner of the palette, press the second icon to activate the

Sharpen mode.


The main control in the Sharpen palette is the Radius. Dragging it upward will blur the

image, while dragging it down will sharpen the edges of any high-contrast detail.

**6** Reduce the Radius by dragging down any of the three channel sliders. The RGB

channels are ganged by default, so adjusting one will equally alter the other two.


Although it’s easy to see that the engravings become more detailed with this

adjustment, the severity of the impact that sharpening has on the rest of the image is

more difficult to determine by eye.

**7** Above the viewer, click the Highlight button, and then click the A/B Highlight Difference

button in the upper left corner.


A/B Highlight Difference shows you the change that has occurred in an image within

an active node. If color grading, A/B will display the areas of the image that have

changed hue and tone. If there have been pixel-based changes, like sharpening, A/B

will display the object edges affected by the adjustment.

**8** Adjust the Radius to about 0.40 for a satisfactory level of detail on the shotgun

engraving but without overly emphasizing the barrel and the smoke coming out of it.

**9** In the Sharpen palette, increase the Scaling to 0.5. Doing so will multiply the result of

the Radius adjustment.


**Lesson 3 Correcting and Enhancing Isolated Areas** **85**


With the sharpening affecting the image uniformly, you might see some unwanted

artifacts, like the increased noise pattern throughout the frame. You can limit the

sharpening effect using the Coring Softness and Level controls at the bottom

of the palette.

**10** Increase the Level (to around 10–15) until the fine noise in the image is removed. The

Level determines the size of the details that are impacted by the Sharpen tool. As you

increase it, smaller detail is omitted from the sharpening effect.

**11** Increase the Coring Softness (to around 5) to gently recover some of the sharpening

lost after the Level threshold adjustment. You can think of the Coring Softness as

similar to the red control points in the Power Windows that determine the softness of

the matte edge.


To see the results in the image, you can disable the highlight.

**12** Click the Highlight button above the viewer or press Command-Shift-H (macOS) or

Ctrl-Shift-H (Windows).

**13** Toggle Command-D (macOS) or Ctrl-D (Windows) to bypass the Sharp node and

compare your results to the original image.


Although the sharpness looks very nice on the engravings, it appears overly sharp on the

left hand at the end of the clip, and on the shotgun shell at the start. You can use a window

to limit this sharpening effect to a specific area in the shot.


**Lesson 3 Correcting and Enhancing Isolated Areas** **86**


##### **Tracking Obscured Objects**

Adding a simple circular window to the Sharp node will allow you to confine the sharpening

to the decorative engravings on the shotgun breech (handle).

**1** In the Sharp node of clip 06, create a circle window and name it **Bree** ch Detail.

**2** Make the circle smaller and narrower, and rotate it so it confines the sharpening effect

to just the engravings on the breech.


**3** Drag the red control point on the window to soften the edges of the mask.


The sharpening is now successfully isolated to the detail on the breech. However,

scrubbing through the clip will reveal that this is a handheld camera shot, and the

shotgun is moved as it is loaded. You’ll need to track the window for the effect to follow

the engravings.

**4** In the central palettes toolbar, click the Tracker button next to the Window button.

**5** With the playhead still in the center of the shot and your circle window placed on the

detail just under the barrel, click the Track Forward and Reverse button. This action will

trigger an analysis of motion within the clip, resulting in the window moving together

with the shotgun.


**Lesson 3 Correcting and Enhancing Isolated Areas** **87**


As the analysis runs forward, the window disconnects from the shotgun detail due to

the interference from the man’s hand. This occasionally happens when performing a

difficult or obstructed track, and it is useful to know how to fix the issue.


After the forward analysis, the playhead automatically jumps back to the starting

frame and runs a backward analysis too. This analysis features no obstacles and

successfully produces a clean track.


TIP It is common practice to track from the center or the end of a clip when

doing so will provide more reliable tracking data than tracking from the

first frame.


**6** In the upper right corner of the tracker graph, click the right Keyframe navigation

arrow to return the playhead to the central keyframe.


In the Tracker palette, you can see a visual representation of the amount of motion

detected in each transformation parameter. Each colored line corresponds to the

colored parameter label above the Tracker palette. Based on the sudden and erratic

movement on the pan and tilt graph lines in the second half of the graph, the tracking

data has become distorted. To fix the track, you must first remove the unusable

“bad” track data.


**Lesson 3 Correcting and Enhancing Isolated Areas** **88**


**7** Drag within the tracker graph to draw a dotted selection outline around the bad

track data.


**8** In the Tracker palette, in the options menu (…), choose Clear Selected Track Data.


The track data in the selected area of the tracker graph is removed. Knowing that the

track cannot be analyzed with the obstruction, you’ll need to manually adjust the

movement of the window during the time that the hand is in the shot.

**9** Switch the Tracker to Frame mode.


In Frame mode, any changes you make to the window in the viewer will be recorded as

a keyframe, as opposed to the Clip mode, which applies a global change to the

window’s position in the entire clip.


**10** In the viewer, drag the playhead to a point in time where the obstruction has passed,

and the area appears to be trackable again.


**Lesson 3 Correcting and Enhancing Isolated Areas** **89**


**11** Manually reposition the window to the area of the breech that you were previously

tracking. Use the anchor point in the center of the window as a visual guide, if necessary.


A new keyframe appears in the tracker graph, and movement is automatically

interpolated (mathematically calculated) between it and the last tracked moment.

**12** Click the Track Forward button to perform the rest of the track analysis.


**Lesson 3 Correcting and Enhancing Isolated Areas** **90**


**Using the Mini Panel—Tracking**

You can use the Mini Panel to track Power Windows without using your mouse by

pressing the Tracker button in the upper left of the panel.


By enabling Frame mode, you can also keyframe and manually animate windows.

Pressing the Left Arrow and Right Arrow keys will display more advanced keyframe

controls in the viewers.


Due to the unsteady motion of the shotgun, you may choose to make further

corrections to the manual window track to produce a smoother result.

**13** Drag the playhead to the last frame where the breech is visible before the hand passes

in front of it.

**14** With the Tracker palette still in Frame mode, drag the window to the correct position.


NOTE When in Frame mode, the window anchor turns red. This acts as a

helpful visual reminder that any changes made to the window will be logged as

keyframes and animated.


**15** Play through the clip a few times to review the motion of the window track and make

necessary adjustments until you are satisfied with the result.


TIP Click the Loop button in the viewer playback controls to continuously

replay the clip you’re working on.


**Lesson 3 Correcting and Enhancing Isolated Areas** **91**


**What About the Hand?**

You have completed this exercise, but the man’s hand continues to pass under the

tracked window. Is it not affected by the sharpening adjustment? The short answer

is yes; if you were to analyze the footage frame-by-frame, you would find that the

pixels in his hand are affected by the secondary grade. However, due to the speed

of the hand motion and the mildness of the window adjustment, the result is

barely visible and can be left in place.


If you had increased/decreased the gamma or applied a stronger visual effect, the

result would have been obvious, in which case you would have needed to make

further manual adjustments to hide the effect when the hand passes under it. One

solution would be to change the opacity of the window from 100.00 to 0.00 (in the

Window palette), animating the change using two subsequent keyframes in the

Tracker palette the moment the hand obstructs the view, and then adding another

two keyframes to bring the opacity back up after the obstruction is gone. Another

common solution would be to introduce and track a second window to mask out

the obstruction, which you will learn how to do later in this lesson.

## **Fixing Overcast Skies**


Capturing footage with skylines in-camera can sometimes be problematic. Due to the wide

dynamic range of light involved, subjects in the foreground usually require substantially

different exposure levels compared to the sky. Opening the aperture or raising the ISO

may be optimal for capturing the foreground but often results in a blown-out sky. On

professional film productions, this is remedied with a lower ISO and additional lighting on

the talent or by using controlled skylines in a sound stage, but on small productions and

documentary shoots, these are rarely options. Thus, the footage is usually captured with

the sky blown out, and it is up to the colorist to correct the shot.


With the advent of high dynamic range digital film formats (known as raw formats),

cinematographers can capture and retain detail in a wider range of exposure levels than

ever before. We will look at such formats and workflows in Lesson 9, “Setting Up Raw

Projects.” However, you may still often find yourself working on media with compromised

highlights, and it is vital to understand how to adjust them effectively.


**Lesson 3 Correcting and Enhancing Isolated Areas** **92**


There are several approaches to correcting or matching a sky when working with standard

dynamic range footage. The fastest is to apply a gradient window and blend color into the

top of the shot. A higher-precision approach involves first isolating the sky with a keying

tool, such as the qualifier, and then tweaking the color values using the standard

grading tools.

**1** In the yellow flag-filtered timeline, select clip 01. This clip was previously balanced and

matched, and now needs secondary grading to address the overcast sky.


**2** Create a third corrector node called **Sky** .

**3** With the Sky node selected, in the central palettes, open the Qualifier palette.


**4** In the viewer, using the Qualifier tool, click and drag across the sky. The Sky node

thumbnail will update to show the initial qualifier selection.


To refine the qualifier values, you must change the viewer mode to display

only this selection.


**Lesson 3 Correcting and Enhancing Isolated Areas** **93**


**5** Switch the viewer to Highlight mode. Ensure that the mode on the row below is set

to Highlight.


When a selection is first made using the qualifier, it will often miss necessary sections

or include unwanted areas. It is up to you to refine the selection using a variety of

methods. To begin, you will use the HSL Qualifier palette to fine-tune the RGB selection

by dragging the Hue, Saturation, and Luminance sliders to define exactly what those

values should be.

**6** Toggle the Highlight button to compare the original image with the selection. You will

see that areas of sky between the branches of the trees need refinement.


A good starting point to refining the HSL selection is to disable each parameter one by

one to determine whether its absence would improve the qualifier.

**7** Click the orange toggle next to Hue to disable it.


Doing so has a positive effect on the selection. The horizon becomes refined, and

more areas of sky in the trees are included in the qualifier result. This makes sense

because the blown-out white sky is mostly made up of luminance data, not hue. Leave

the Hue range disabled.


Toggling the Saturation and Luminance parameters reveals that they are vital to the

selection, so you will leave them enabled.


The next step is to adjust the values of the parameters to ensure the cleanest edge

selection. You may want to zoom in on the horizon in the viewer to better see the

result of these adjustments.

**8** Drag the right side of the Saturation range, or drag the High field beneath the

Saturation bar, to remove the qualifier selection from the mountain treetops, if

there is any.


**Lesson 3 Correcting and Enhancing Isolated Areas** **94**


**9** Drag the left side of the Luminance selection (Low) to further refine the selection. Aim

to include the darker areas of sky between the trees.


The focus is on ensuring the cleanest possible selection along the horizon, so, for now,

you can ignore any other regions of the image that are also being selected, such as

the horses.


**10** In the upper left of the viewer, click the Highlight B/W button to switch to a black-and
white representation of the matte.


**Lesson 3 Correcting and Enhancing Isolated Areas** **95**


You will use the Matte Finesse controls in the Qualifier palette to further clean up this

matte. Unlike the HSL parameters, which targeted the original image’s pixel color and

luminance data, Matte Finesse impacts only the values of the resulting black-and
white matte.


**Using the Mini Panel—Qualifiers**

After making an initial qualifier selection, you can use the Mini Panel to refine it.

When you press the Qualifier button in the upper left section of the panel, the two

5-inch screens and their surrounding buttons and knobs become the controls

you’ll use to continue making adjustments.


At first, you’ll see the controls for Hue on the left screen and Saturation on the

right. In the upper left section of the panel, press the Right Arrow button to

navigate to the Luminance controls. In certain tools, you must use the Left Arrow

and Right Arrow buttons to access all the functions that a specific tool offers.


One more push of the Right Arrow button will bring you to the Matte Finesse tools.


**11** The Pre-Filter parameter performs some minor cleanup of the original image by

reducing compression artifacts like macropixels. Increase the pre-filter (1.0) to soften

the edges of the trees.


**Lesson 3 Correcting and Enhancing Isolated Areas** **96**


**12** The Clean Black and Clean White parameters eliminate noise by shrinking very small

selection areas of the matte. Adjusting Clean Black will reduce some of the minor

spill-off in the trees under the horizon. A setting of 5.0 should be enough for a

satisfactory reduction.

**13** Likewise, tweaking Clean White (5.0) will amplify the white matte between the

tree branches.

**14** The Post-Filter cleans up the resulting key by reintroducing some of the finer detail

from the original image back into the selection. Increase the Post-Filter (1.0) to see

branch and leaf details return to the trees.


The accuracy of the qualifier often depends on the nature and quality of the footage.

In this case, you might experience some difficulty in getting a clean extraction from

both mountain tops due to the difference in depth of field between them. When one

mountain has a clean key, the other appears too soft and vice versa. In such cases, the

best approach is to break up the keying process into several nodes and combine them

using a key mixer.


NOTE You can see the results of using a key mixer to clean up the sky selection on

this clip in the 04 Completed Timeline. Open the timeline, right-click the clip, and

under Local Versions, choose Mixed Key to see the version of the node pipeline

with the key mixer.

##### **Using Windows to Limit Qualifiers**


If the HSL qualifier has selected areas beyond the edge that are not needed, you can

quickly exclude them using windows. In this exercise, you’ll remove the horses from the

selection so that your secondary grade will only impact the sky.

**1** Open the Window palette.

**2** Activate the Linear window button, and label it **Sky Window** .


**Lesson 3 Correcting and Enhancing Isolated Areas** **97**


**3** Drag its corners around the sky selection to exclude the lower regions of the matte.


The sky should now be successfully selected and ready for color adjustment.

**4** Click the Highlight button to disable the matte preview.

**5** Drag the Gain master wheel to the left (0.95) to reduce the brightness of the sky.

By turning the white pixels gray, you will make them more receptive to hue and

saturation changes.

**6** Drag the Gain color wheel toward cyan/blue to introduce blue into the sky.


**Lesson 3 Correcting and Enhancing Isolated Areas** **98**


Making luminance and color adjustments within a qualifier selection sometimes

reveals issues that were hard to spot in the original matte. In the case of this image,

the horizon might adopt a dark border, which indicates that the grade is impacting

the trees.

**7** In the Qualifier palette, increase the Clean Black (20.0) until the selection retracts from

the treetops.


Finally, to soften the grade along the horizon, you can gently blur the edge between

the black and white portions of the matte.

**8** In the Matte Finesse Controls, increase the Blur Radius (5.0).


A gentler edge will ensure a more organic-looking grade and hide any remaining

imperfections in the selection.

##### **Adding Atmosphere**


When you look into the distance through several miles of air, you see the atmosphere

slowly building up over trees, buildings, and mountains until it forms a solid color in the

sky. In an air-polluted city, the atmosphere may have a hazy white, brown, or orange look;

on a clear day, you would see a soft blue. This concept is known as atmospheric

perspective and can be observed in real life and on film. The farther away an object is, the

more its saturation and contrast is reduced and the more it adopts the color of the

atmosphere.


When enhancing a sky, or replacing it altogether, you need to blend an equivalent hue into

the shot’s horizon to replicate this atmospheric perspective. Otherwise, the replacement

sky might look fake against the horizon.

**1** In the Node Editor, right-click the Sky node and choose Add Node > Add Outside or

press Option-O (macOS) or Alt-O (Windows). This inverse selection will allow you to

blend the color of the sky into the horizon of the image.

**2** Label node 04 **Outside** .


TIP In the Node Editor, drag your middle mouse button to pan and adjust the

slider at the top of the panel to increase or decrease the size of the nodes.


**Lesson 3 Correcting and Enhancing Isolated Areas** **99**


**3** At the bottom of the Window palette’s preset list, activate the Gradient window button

and label it **Atmosphere** .


An outline of the gradient controls appears in the viewer in the form of a line with a

perpendicular arrow extending from it.


The gradient window works a bit differently compared to the other windows you have

created. Instead of defining a shape, you position a starting point and then drag the

arrow in the direction of the gradient fall-off. The farther you drag the arrow, the softer

the gradient will be.

**4** Adjust the top of the gradient (the horizontal line) to the top of the distant mountain

and drag the arrow to taper the gradient off toward the bottom.


**5** Drag the Offset color wheel in the direction of cyan blue to give the distant mountain

a slight blue tint.

**6** Press Command-D (macOS) or Ctrl-D (Windows) to compare the results before and

after your atmosphere addition.


The gradient looks good in the distance but covers too much of the foreground

mountain. You will want to create a new window to mask out anything you don’t

want affected by the atmosphere grade.

**7** In the Node Editor, disable the Outside node. Doing so will allow you to continue

working without being distracted by the blue grade.

**8** While still in the Window palette, activate the Curve (pen icon) button and label

it **Foreground** .


**Lesson 3 Correcting and Enhancing Isolated Areas** **100**


**9** In the viewer, click around the foreground hill and the lower half of the frame to create

a custom shape. To close the loop and define the shape, click the first point that

you created.


TIP When creating custom windows, click to create linear points and drag to

create rounded Bézier curves. To delete a point, select it and press the Delete

or Backspace key, or middle-click the point with your mouse.


**10** Enable the Outside node to see the result.


The atmosphere grade now affects both the background mountain and the entirety of

the custom shape. This is because, by default, all windows are additive. You will need to

indicate that you wish to subtract the selection from the final result.

**11** In the Curve window row, next to the label, click the Mask button to extract this custom

shape from the final key of the node.


**Lesson 3 Correcting and Enhancing Isolated Areas** **101**


**12** To the right of the Window palette, adjust the Softness parameters to feather the edge

of the curve. Drag the Inside and Outside fields to make the border of the Foreground

window less aggressive between the two mountains.


You have successfully fixed the overcast sky in this clip using a technique practiced by

thousands of colorists on millions of film and television clips around the world. This

technique can be employed aesthetically to add color and beautify a scene but is also often

used to match clips with mismatched sky hues.

##### **Performing Sky Replacement**


More advanced approaches to fixing an overcast sky involve replacing the sky altogether,

usually with a still photo, video, or computer-generated image. The Sky Replacement effect

allows you to quickly perform such advanced compositing and even track the sky to a

moving shot while integrating it to the camera’s lens properties.


In this exercise, you’ll use the sky key and atmospheric perspective that you generated

earlier in the lesson to integrate a new artificial sky into the shot.


NOTE This exercise requires DaVinci Resolve Studio to complete.


**1** Open the Effects Library.

**2** Click the magnifying glass at the top of the panel to reveal the search bar.


**Lesson 3 Correcting and Enhancing Isolated Areas** **102**


**3** Type **sky** to filter the library contents.


**4** Drag the Sky Replacement effect onto an empty space in the Node Editor near the Sky

and Outside nodes.


TIP Click the magnifying glass in the Effects panel to remove the effect

search bar.


**5** Connect the Sky node’s RGB output (green square) to the Sky Replacement’s top RGB

input (green triangle). This will be the video signal used as a backplate (background

layer) for the sky replacement composite.

**6** Connect the Sky node’s key output (blue square) to the Sky Replacement’s top key

input (blue triangle). This will feed the sky key data to the Sky Replacement node and

determine the area of the image where sky replacement occurs.


**7** Finally, connect the RGB output of the Sky Replacement node to the RGB input of the

Outside node. This will continue the signal flow and incorporate the Sky Replacement

effect into the clip pipeline.


**Lesson 3 Correcting and Enhancing Isolated Areas** **103**


Note that the key connection between the Sky and Outside node remains. This ensures

that the Outside node will continue superimposing the atmospheric grade to the

mountaintop.

**8** Select the Sky Replacement node to open its settings in the Effects panel.


The settings are divided into categories that support a variety of sky replacement

workflows. Click a category header to expand or contract its list of parameters.


**Sky Mask Adjustments** allow you to preview and adjust your incoming key mask.

**9** Click Preview Mask to review the Sky node key.


As you have taken care to extract the overcast sky precisely with the Qualifier palette,

you will not need to adjust the incoming mask. However, if your artificial sky blends

seamlessly enough with the original background hue, you can opt to retract the mask

to re-introduce more of the edge detail at a later stage.

**10** Click Preview Mask again to disable the matte preview mode.


**Source Sky Appearance** features the parameters you’ll need when working with

external sky images or videos.


To introduce a sky image or video into the clip composite, drag the media from the

color page media pool into the Node Editor. The media will appear as an external

matte with four key outputs and one RGB output. Connect the RGB output of the Ext.

Matte node to the second RGB input of the Sky Replacement node to see the sky

media in the keyed area of the clip. You can even opt to use the second key input to

isolate a portion of the incoming image or video.

**11** Since you will not use any external media for this composite, leave the parameters in

the Source Sky Appearance category as they are.


**Lesson 3 Correcting and Enhancing Isolated Areas** **104**


**Artificial Sky** allows you to generate your own sky using a variety of color and

gradient parameters, as well as controls for cloud and sun detail.

**12** Click Preview Artificial Sky and increase Sky Opacity to 1.000 to see the default sky

gradient in the viewer.


**13** Deselect Preview Artificial Sky to review how the gradient appears when masked.


**14** Change the Sky Color to match the saturation levels more closely in the scene.


**Lesson 3 Correcting and Enhancing Isolated Areas** **105**


When working with larger sky areas or designing more intricate sky hues, adjust the

Horizon parameters to determine the softness, height, and angle of the sky gradient.


Next, you will introduce some cloud detail to make the sky more dynamic.

**15** Increase Cloud Opacity to 1.000.

**16** Reduce the Cloud Scale to 0.300 to place the clouds at a greater distance.

**17** Adjust the Cloud Time (0.800) to change the distribution of the clouds.


The Hotspot parameters help imitate the look of the sun in the sky. This element might

be necessary when matching the light and shadows in certain shots. However, since

the foreground in this environment does not have direct sunlight, it will not be

necessary to activate it.

**18** Leave the Hotspot Brightness at 0.000.


With the contents of the sky set, you can revisit the mask adjustments to fine-tune the

incoming key.

**19** Under Sky Mask Adjustments, drag up the Shift Edge (0.050) to reintroduce tree details

across the edge of the matte.


This adjustment works because the sky replacement is close to the original sky hues.

When working with more dramatic composites (like a dark stormy sky or a red Mars

atmosphere) you may want to leave the incoming key as is.


**Sky Position** controls allow you to track the sky to the environment and to adjust the

sky’s final position and size. Auto-Size for Motion ensures that the entirety of the

incoming matte is filled with the sky image.


**Lesson 3 Correcting and Enhancing Isolated Areas** **106**


**20** Since there is a slight camera wobble in this locked-off shot, click Track Foreground to

analyze the footage outside the input key. This will result in the artificial sky moving

together with the rest of the shot.

**21** **Sky Integration** is used for final sky preview and to adjust the composite based on the

camera’s lens properties. Because there is no obvious lens distortion or change in

focal distance, these settings can be left as they are.

**22** **Foreground Appearance** allows you to adjust the image foreground, based on the

inverse of the sky key. Your goal in this exercise is to create a sky that matches the

environment, not the other way around, so you can leave these parameters as they are.

**23** If your artificial sky has strong hues, you can use the **Global Blend** parameter to fade

it into the original environment, producing a more natural result.


Before


After


**Lesson 3 Correcting and Enhancing Isolated Areas** **107**


TIP As well as a method of correcting blown-out or overcast skies, Sky

Replacement can help you match the sky color and detail between shots captured

on different cameras or at different times of the day.


To shoot fast and travel light, documentary filmmakers might sometimes need to

compromise on best technical practices such as good lighting and consistent exposure.

Secondary grading allows us to get the best possible image out of every shot!
## **Warping Color Ranges**


The Color Warper allows you to adjust two parameters at once, producing quick results in

an interface that encourages intuitive grading. It features three modes: Chroma Warp,

Hue-Saturation, and Chroma-Luma. Its mesh interface ensures a smooth transition

between hues, which reduces image artifacts. The Color Warper helps enhance the

appearance of objects or areas with a distinct hue and can be combined with other

secondary selection methods for optimal results.

##### **Chroma Warping in the Viewer**


The simplest way to interact with the Color Warper is through the color page viewer. This

method works best on areas with well-defined color ranges, such as for vehicles, clothing,

or the sky. In this exercise, you will adjust the color of the dry grass on the ground to give it

a healthier, greener appearance.


You will continue to work on clip 01 in the yellow flag-filtered timeline.

**1** Create a new serial node at the end of the pipeline and label it **Grass** (node 06).

**2** In the central palettes, open the Color Warper palette.


**Lesson 3 Correcting and Enhancing Isolated Areas** **108**


The Color Warper’s Chroma Warp tool features a chromaticity diagram that represents

all the potential hues you can target and adjust. A white trace showing the distribution

of the current frame’s colors and their saturation levels is projected onto the diagram

to guide your selection.


The right side of the palette contains tools and pinning options that can be used to

achieve optimal precision when warping. Under the Tools header, you’ll find two

primary options for the warping method:


 - **Normal mode**  - selects a range of colors for a smooth, consistent change across a

broad spectrum of hues. This is ideal for achieving organic-looking results as a

range of similar hues is pushed toward a single target.

 - **Point-to-point mode**  - selects a specific color for more precise adjustments to

individual objects or surfaces. This is ideal for more refined results, similar to those

achieved by the Qualifier tool.


**3** Click the Expand button in the upper right corner to turn the palette into a

floating window.


Drag the corners and edges to resize the window to your liking and drag the

palette header to reposition it. The larger interface will make it easier to make

precise adjustments.


**Lesson 3 Correcting and Enhancing Isolated Areas** **109**


**4** In the sidebar, under Tools, ensure that Add Stroke - Normal Mode is selected.


**5** Hover your mouse pointer over the image in the viewer.


An orange crosshair appears in the Chroma Warp diagram, corresponding to the hue

over which your mouse pointer is placed.


The Color Warper features the same hue layout as the color wheels and offers the

same saturation control. Moving a point closer to the center will desaturate a hue,

while moving a point outward will increase color intensity. Moving a point in a circular

fashion will change the color of the selected hue.

**6** In the viewer, click a patch of grass under the left rhino and drag diagonally toward the

lower left.


TIP Hold Option (macOS) or Alt (Windows) and click in the viewer to preview

which areas of the image will be affected by the warper.


**Lesson 3 Correcting and Enhancing Isolated Areas** **110**


This results in more saturated greens, but the effect overpowers other regions of the

frame. Several factors might contribute to this when using the Color Warper: the image

may have many shared color properties (yellows/greens), the image may be

desaturated (resulting in the hues being clustered together in the trace), or the

chroma warp may be operating within too broad a chroma range.


One of the simplest ways to refine your chroma warp selection is to pin areas of the

image that you wish to exclude from the warp.

**7** Under Tools, select Add Pin Point.


**8** In the viewer, click a cloud in the sky to omit white areas from being warped.


A pin appears in the Chroma Warp diagram, indicating the location of the cloud in the

trace. This significantly clears up the selection in the viewer.

**9** With the Pin Point tool still active, click a part of the rhino that’s being warped green.


Another pin appears on the trace, and the result in the viewer is further improved.


**Lesson 3 Correcting and Enhancing Isolated Areas** **111**


**10** If necessary, choose the Select tool and refine the hue and saturation of the grass

points directly in the Chroma Warp diagram.


Observe the surrounding environment in the scene to ensure that you reach a realistic

shade of green.


Finally, you can use additional secondary tools to isolate your grade to the bottom of

the frame.

**11** In the Window palette, create a linear window and label it **Grass Matte** .

**12** Drag the corners of the window around the grassy field in the foreground of the image.


The adjustment is isolated to the grass, while keeping other elements, like the dirt on

the ground, unaffected.


**Lesson 3 Correcting and Enhancing Isolated Areas** **112**


The Color Warper enables intuitive adjustment of color, hue, and saturation directly within

the viewer. As you likely noticed, the adjustment is optimal when the hue is kept close to

the source color. If pushed too far, the warp mesh can overlap itself, resulting in visual

artifacts. In such cases, consider switching the Chroma Warp to Point-to-Point mode or

using an alternative hue correction method, such as HSL curves or the qualifier.

##### **Using the Grid Interfaces**


The Color Warper also contains two grid interfaces for changing either Hue and Saturation

or Chroma and Luma. The Hue-Saturation grid is similar to the Chroma Warp’s Normal

mode but features far greater flexibility when warping. The grid interface enables you to

adjust the mesh resolution, providing a clearer visualization of the color vectors and

neutral white point.


The Color Warper’s Chroma-Luma grid allows you to adjust the hue and luminance of a

selected range simultaneously. This opens up some creative and practical applications

when working with bright areas, such as skies, lights, and windows.

**1** In the yellow flag-filtered timeline, select clip 03.

**2** Create a new serial node called **Sky** (node 02).

**3** In the upper right corner of the Color Warper, press the Chroma-Luma button.


**Lesson 3 Correcting and Enhancing Isolated Areas** **113**


The Chroma-Luma panel features a pair of mesh grids that depict the cross sections of

a 3D chroma-luma cube. A trace is projected behind the grids, representing the

distribution of the chroma and luma data of the current frame in the viewer from two

perspectives.


The horizontal axis of the grid represents hues, while the vertical axis maps the

luminance. You will use control points on these grids to enhance the vibrant colors of

the sky. The right side of the palette features advanced selection and pinning tools,

which are used to achieve optimal precision when warping.

**4** In the viewer, click a light area of the sky and drag down.


In color grading, changing luminance based on a hue can often lead to distortion.

Therefore, it is essential to maintain precise Chroma-Luma selections and make

subtle adjustments.


**Lesson 3 Correcting and Enhancing Isolated Areas** **114**


**5** Reset the Color Warper by clicking the reset arrow in the upper right corner of

the palette.


TIP Right-click a control point to reset its position in the grid.


**6** In the lower left corner of the Color Warper palette, click the Chroma resolution

dropdown menu and set the resolution to 12.


The Color Warper grid now features 12x12 divisions, allowing for much more precise

selection. By default, the chroma and luma resolutions are linked, although this behavior

can be disabled by clicking the link icon next to the resolution dropdown menus.


Next, you will lock the darker regions of the image to protect them from adjustments

made to the sky.

**7** In the viewer, hover over the hill in the foreground and the mountains in the

background.


The orange crosshair indicates that the luminance range of those regions lies in the

bottom two rows.

**8** Select any point on the row directly above the bottom of the grid.


**Lesson 3 Correcting and Enhancing Isolated Areas** **115**


**9** In the Tools sidebar, click the Select Row button to expand the selection to the

entire row.


**10** Click the Convert Selected to Pin button to lock all the control points on that row.


A black outline indicates pinned points. Adjustments made near a pinned point will not

affect it, and the surrounding grid mesh will warp around it.

**11** Repeat steps 8–10 in Grid 2 (the grid on the right) to protect the shadows in those

chroma regions too.

**12** At the bottom of the palette, drag the Axis Angle parameter (20.00) to determine the

hues that you will introduce to the sky. The aim is to reach a more yellow tone in the

left grid and a magenta tone in the right grid.


As you do this, the waveform trace in the grid will rotate, revealing its 3D nature.

**13** At the top of the Tools sidebar, select Grid 2.

**14** In the viewer, click the region between the orange and blue gradients in the sky and

drag right and slightly upward to push a vibrant pink hue into the sky.


**15** At the top of the Tools sidebar, switch to Grid 1.


**Lesson 3 Correcting and Enhancing Isolated Areas** **116**


**16** In the viewer, click the orange region right above the mountains and drag left and

upward to brighten the sky and give the sunrise a warmer, more pronounced glow.


Notice that when you finish adjusting a point in the grid, it also becomes pinned, as

indicated by the black outline. This means that you can adjust multiple control points in

the Color Warper grids without them offsetting each other.


Before


After







**Lesson 3 Correcting and Enhancing Isolated Areas** **117**


**17** When finished, copy the Sky node and paste it into a new node in clip 04 to keep the

look of the sky consistent.


Before


After


As you continue to work with the Color Warper, explore the remaining selection and

pinning tools in the sidebar to gain a fuller understanding of how selections can be made

faster and with more precision.
## **Enhancing Skin Tones** **with Face Refinement**


Whether watching a fictional film or a documentary, audiences will pay the utmost

attention to the actions (and therefore the faces) of the people on the screen. Colorists and

makeup artists share the common job of “protecting the talent.” This means we need to do

our best to make skin look clear and natural.


**Lesson 3 Correcting and Enhancing Isolated Areas** **118**


In DaVinci Resolve, this is achieved with a combination of primary adjustments aimed at

ensuring skin is well exposed and balanced, and secondary grading methods and effects

to reduce minor imperfections.


NOTE This exercise requires DaVinci Resolve Studio to complete.


In this exercise, you’ll start with a well-framed and properly exposed shot. The only issue is

that the speaker is wearing a wide-brimmed hat on a sunny day, resulting in harsh

shadows on her face. Your goal is to make her face stand out more and then address

general imperfections using the AI Face Refinement effect.

**1** In the yellow flag-filtered timeline, select clip 02. In the Node Editor, you can see that it

has already has a luminance adjustment on the first node.

**2** Create a new serial node and label it **Face** .

**3** Open the Effects panel.

**4** In the Resolve FX Refine category, drag the Face Refinement effect onto the Face node.


**Lesson 3 Correcting and Enhancing Isolated Areas** **119**


NOTE If you are not using DaVinci Resolve Studio, a watermark will appear

over the image. You can dismiss the warning dialog and complete this exercise

with the watermark.


When activated, Face Refinement automatically detects and tracks faces, giving you

the option to add side lighting, enhance the skin, and adjust individual features such as

the eyes, lips, teeth, forehead, cheeks, and chin.

**5** In the AI Face Refinement settings, click Detect Faces In Frame.


A green box appears around the subject’s face. If there had been more than one

subject in the frame, red boxes would have appeared around the other faces, and you

would have had the option to select the subject that you wished to track. In cases

where you might want to track multiple faces, you will need to create dedicated Face

Refinement nodes for each subject.

**6** Press Track Forward Then Reverse. Processing will take some time as the software

tracks the face and constructs a traveling matte.


**Lesson 3 Correcting and Enhancing Isolated Areas** **120**


When the analysis is complete, you will see a collection of green trackers outlining the

woman’s facial features.


To ensure the highest quality of the selection, you should check the matte of the face

before proceeding with any adjustments. The matte quality can be compromised when

analyzing a subject whose skin tones closely match their hair, clothes, or surroundings.

In this example, the subject fits all three of these criteria.

**7** In the AI Face Refinement settings, click the Skin Isolation header to expand it, and

then select Show Mask.

**8** Deselect Show Overlay at the top of the settings to hide the green trackers in

the viewer.

**9** Zoom inside the viewer to get a clearer view of the subject’s face.


The selection appears clean overall. However, the upper segment of the mask has included

part of the tan hat that the woman is wearing, which you will remove in the next exercise.


**Lesson 3 Correcting and Enhancing Isolated Areas** **121**


**Lesson 3 Correcting and Enhancing Isolated Areas** **122**


##### **Combining Windows with Face Refinement**

To remove the unnecessary hat selection from Face Refinement, you will use a window to

exclude the top of the matte.

**1** Move the playhead to the last frame of the clip, where the subject’s head appears

more level.

**2** With the Face node still selected, open the Window palette.

**3** Create a new circle window and place it over the woman’s face.

**4** In the upper right options menu of the Window palette, choose Convert to Bezier to

transform the circle’s points into Bézier curves.


**5** Label the resulting curve window **Face Window** .

**6** In the viewer, adjust the points to fit around her face, paying extra attention to

excluding the hat.


**7** In the AI Face Refinement settings, deselect Show Mask.

**8** Enter the Tracker palette.


**Lesson 3 Correcting and Enhancing Isolated Areas** **123**


**9** Click the Track Reverse button to track the motion of her face backward

through the clip.

**10** When tracking is completed, refine the shape of the Face window throughout the clip

in Frame mode, if necessary.

**11** Use the viewer’s onscreen controls menu in the lower left corner to turn off the

window outline.


The face matte has now been prepared for optimal grading and compositing. At times, you

may find that a matte or key _appears_ correct until you start grading, at which point you

may notice rough edges, holes, or poorly selected regions. In those cases, you can always

return to your matte controls and secondary selection tools (like the qualifier and windows)

to continue refining the matte.

##### **Improving Skin Quality**


There are a variety of reasons why skin might need adjustment:


**General skin imperfections, such as variations of color, spots, dryness, oiliness, and**

**so on** —By applying the appropriate brightness, contrast, and blurring, you can reduce

these issues and put the focus back on the performance.


**Some skin undertones are prone to reflecting light with unpredictable tints** —The

most common variants are skin tones that appear magenta or green under harsh artificial

lighting, such as from fluorescent office lights. The purpose of grading in this case is to

remove the tint and bring the performer’s skin tone to a neutral position that more closely

resembles their skin under natural light.


**Overpowering primary grade** —When a shot has been strongly graded at the primary

stage to look a certain way (for example, to make the environment look cold), the skin can

end up looking overpowered or washed out as a result. This type of dominant grade can

drain the life out of a shot and make it look dull. By bringing back the skin tone, the shot

develops chromatic contrast (also known as “color separation”) and once again

becomes vibrant.


In this exercise, you’ll look at some of the commonly used settings of the AI Face

Refinement tool with a focus on reducing minor imperfections and achieving a natural

result, known in the industry as “beauty work.”


**Lesson 3 Correcting and Enhancing Isolated Areas** **124**


**1** In the Workspace menu, choose Full Screen Viewer or press Shift-F to expand the

viewer to fill your screen while still giving you access to the Effects panel to the right.

**2** In the AI Face Refinement Settings, under Skin Texture, adjust the Amount to 0.200.

Doing so will gently blur the skin to soften minor wrinkles and imperfections.


Be careful not to push this setting so far that skin starts to look plastic. You should not

aim to remove wrinkles but merely soften them.


TIP To see a wider range of skin-smoothing options, change the Skin Texture

Operating Mode to Smoothing or Beauty Advanced. These modes break up

the smoothing process into individual steps in which you can define texture

detail, size, and diffuse lighting.


**3** Scroll down to the Skin Grading section to begin work on the woman’s skin tone.


The Midtone parameter is responsible for the overall brightness of the skin. You can

use it to lighten the shadows on her face.

**4** Drag the Midtone slider to the right (0.030) to brighten the skin, but don’t drag it so far

that the results become distracting.


TIP For more precision, drag within the numeric field of a parameter instead

of the slider.


Color Boost enhances saturation in areas of the skin that are undersaturated.


**Lesson 3 Correcting and Enhancing Isolated Areas** **125**


**5** Drag the Color Boost until you reach 0.020.


Tint is responsible for undoing the green or magenta color cast that some skin

tones reflect.

**6** Drag Tint to -0.100 to reduce the redness in the skin.


With the shadows lightened and the skin more balanced, you can return to the

Contrast parameter to give her face more depth.

**7** Raise the Contrast (0.100) to return some details into the shadows of her face.


There is a prominent highlight on her chin where her hat no longer casts a shadow.

The Shine Removal parameter is ideal for handling strong highlights on skin.

**8** Raise Shine Removal (1.000).


Most of the highlights are successfully reduced, but there is an area on the lower right

of her chin that is not included in the mask matte. You’ll need to expand the mask to

include this area.

**9** Return to the Skin Isolation section and select Show Mask.

**10** Increase the Region Size (0.200) to expand the mask matte.

**11** Increase the Region Softness (0.200) to ensure that the matte’s edge remains

undetectable in the viewer.

**12** Deselect Show Mask.

**13** Return to the Skin Grading section and adjust Shine Removal (0.600) to remove the

light glare on her chin while keeping the highlight natural.


The next category in the list is Side Lighting. Use these settings if your subject was

captured next to harsh directional lighting or if they did not have a fill light to counter a

strong light source. In this case, the subject is evenly exposed, so an adjustment will

not be necessary.


After that, the Eyeshadow category allows you to artificially apply eye makeup to a

subject. The detailed parameters give you control over hue, saturation, size, gamma,

and so on across the upper and lower lids. The project narrative does not call for this

type of adjustment, so you can skip these settings too.


**Lesson 3 Correcting and Enhancing Isolated Areas** **126**


**14** Scroll down to the Eyes category and click the header to expand it.


The controls in this section allow you to enhance details in the irises of the speaker, as

well as brighten and soften the skin around the eyes.

**15** Set Sharpening to 0.200 to refine the iris, eyelashes, and eye shape.

**16** Set Eye Light to 0.050 to gently increase the brightness around the eye area.

**17** Adjust Eyebag Removal to 0.100 to soften and lighten the area directly under her eyes.


The Lips category allows you to saturate and change the hue of a subject’s lip color

and to smooth upper lip wrinkles in close-up shots. As usual, context is key. The park

ranger in question is not wearing lipstick, nor do you have a justifiable reason to

glamorize her as she talks about the issue of rhino poaching in South Africa. In this

case, the Lips tool is necessary only to add minor contrast to her skin tone.

**18** In the Lips section, raise Saturation to 0.100 to better define her lips against her skin.


The same guidelines apply to Teeth and Blush Retouching.

**19** In the Teeth section, slightly increase the Gamma (1.050) to make her teeth more

visible, which might help some viewers better follow what she is saying.

**20** In the Blush Retouching section, set Saturation just high enough (0.100) to define her

face shape without making it look like makeup.

**21** Additionally, expand the Size to 0.500 to spread the blush across either side of her face

without concentrating it to the apples of her cheeks.


Other features, like the forehead, cheeks, and chin, all have their own categories for

dedicated correction. These can be valuable when you are dealing with unusual

lighting or patchy skin tones.


**Lesson 3 Correcting and Enhancing Isolated Areas** **127**


You have completed the work required on this clip. If you are generally happy with the

result but find that it’s a little too overpowering, you can scroll up to the Face Location

controls at the top and reduce the Effect Strength slider.


Before After


With just one node, you have successfully enhanced your subject’s skin tone, made it

more pronounced by brightening and warming it, and added chromatic detail to her

features. In the original clip, it now becomes apparent how much the shadow of her

hat was affecting the visibility of her face and facial expressions.


TIP Another tool designed for professional-level skin touch-ups is Beauty

Resolve FX. Its Ultra Beauty operating mode smooths rough skin textures

while recovering finer details to produce natural results that complement

the subject.


**22** When you’re done with the adjustments, choose Workspace > Full Screen Viewer or

press Shift-F to exit Full Screen mode.


TIP To remove a Resolve FX plug-in from a node, right-click the node and

choose Remove OFX Plugin or click the bin icon in the upper right corner of

the Effects Settings panel.


The AI Face Refinement tool is ideal when working with interview subjects, portrait

compositions, or fashion shoots. When handling profile shots, or subjects with a lot of

motion, more appropriate solutions might be tools such as the Beauty Resolve effect or

the primary grading palettes combined with secondary grading selection techniques.


**Lesson 3 Correcting and Enhancing Isolated Areas** **128**


## **Adjusting Skin Tones Manually**

The Curve palette’s HSL curves allow you to make rapid, targeted secondary adjustments

to an image based on hue, saturation, or luminance ranges. This makes the HSL curves a

popular tool for skin hue and saturation correction.


In this exercise, you will remove the magenta tint from the subject’s skin.

**1** In the yellow flag-filtered timeline, select clip 05.


This clip has already been normalized with Primaries color wheels in node 01.

**2** Create a new serial node and label it **Skin Hue** (node 02).

**3** Open the Curves palette, and in the upper right corner, choose the Hue Vs Hue curve.


TIP The naming convention of the hue curves describes the selection method

followed by the change type. _Hue Vs Sat_ implies that you are targeting a

specific range of color (hue) in order to adjust its saturation (sat), whereas Sat

Vs Lum suggests that you are targeting a certain saturation range (sat) with

the aim of adjusting its brightness (lum).


**Lesson 3 Correcting and Enhancing Isolated Areas** **129**


The Hue Vs Hue palette displays the full range of colors in a linear fashion, looping

around the red hue. It enables you to sample a specific color and shift it toward

another hue.


One method of hue selection is to use the swatch buttons at the bottom of the curve

graph. Another method is to click in the viewer to sample pixel values.

**4** In the viewer, click an evenly exposed patch of the man’s face.


Three control points are added to the Hue Vs Hue curve. The center point identifies

the selected hue, and the control points on either side act as anchors that limit the

range of hue that is affected.


TIP If a hue selection lands near the left or right edge of the palette, the

anchors might appear on opposite ends as the hue range cycles around.


**5** Drag the center control point down slightly to remove some of the red tint in the man’s

skin tone. Be careful not to introduce too much green. If necessary, drag the two

control points on either side farther apart to define a wider hue range for the

skin tone.


**Lesson 3 Correcting and Enhancing Isolated Areas** **130**


TIP For more precision when moving a control point, use the Input Hue

and Hue Rotate fields in the lower right corner of the palette.


This might feel a bit like a guessing game. What is the right hue for his skin? For more

certainty, you can open the vectorscope and check what the adjustment is doing

to the skin.


First, you will get a clearer view of the face by using a window to remove

interfering elements.

**6** Open the Window palette.

**7** Create a circle window and label it **Face Window** . Position it over the man’s face to

isolate a clean patch of skin.


**8** Reduce the window’s Softness Soft 1 parameter to 0.00 to get a sharp edge on

the selection.

**9** Click the Highlight button.


This temporary window will aid in providing a clean readout of the skin values

to the vectorscope.


**Lesson 3 Correcting and Enhancing Isolated Areas** **131**


**10** In the Scopes palette, choose Vectorscope as the scope type.


A vectorscope distributes visual data on a circular graph to represent hues and their

saturation levels. A well-balanced image will generally appear as a cloud of pixels in the

center of the vectorscope. Scenes with prominent colors will appear with broader

traces and deviations toward specific hues. You encountered a vectorscope previously

when working with the Color Warper tool.

**11** In the upper right corner, click the settings icon to adjust the appearance of the scope

for easier readability.

**12** Select Show 2x Zoom to increase the size of the trace.


NOTE When 2x Zoom Is enabled in the vectorscope settings, you will no

longer get an accurate representation of saturation values. However, the

setting is still helpful for checking hue distribution in low-saturation images.


**Lesson 3 Correcting and Enhancing Isolated Areas** **132**


**13** Select Show Skin Tone Indicator to display a line that indicates the angle for skin

tone hues.


When working with skin tones, the vectorscope can be helpful for determining

whether a subject’s skin is deviating toward unflattering hues. However, the skin tone

indicator line itself is not meant as a strict determiner of all skin hues. Some skin tones

have cool undertones, which naturally lean toward red, or warm undertones, which

lean toward yellow. When grading, focus on any obvious arcs or distortions in the trace

that might indicate an incorrect color cast on the skin.

**14** Click anywhere in the color page to close the settings pop-up window.

**15** Drag the center control point in the Hue Vs Hue palette up and down to observe the

movement in the vectorscope.


A significant part of the man’s skin is in shadow, where it appears to have a prominent

magenta tint.


**Lesson 3 Correcting and Enhancing Isolated Areas** **133**


**16** Add additional control points in the Hue Vs Hue curve and aim to place the man’s skin

vectorscope trace parallel to the Skin Tone Indicator line.


**17** When you are happy with the skin tone hue, turn off Highlight mode.


With the highlight off, the HSL grade is still confined to the circle window.

**18** Go to the Window palette and deactivate the window by clicking the circle icon.


While the Color Warper allows you to intuitively adjust two values at once, the HSL curves

are ideal for single-purpose precision, such as for working on skin tones. These tools

should be your first choice when you’re trying to quickly adjust the hue, saturation, or

luminance of an object. If the result is not immediately satisfactory, you can then switch to

working with more advanced tools like the qualifier or Magic Mask, which offers a greater

degree of control over your matte selection. Also, keep in mind that you can use the Color

Warper and HSL curves in combination with secondary selection tools for an even more

refined selection.


**Lesson 3 Correcting and Enhancing Isolated Areas** **134**


**How Do We Color Grade Skin?**

With light meters, color charts, skin tone indicator lines, and more than a century

of filmmaking, you would think that there would be a well-established standard for

color correcting skin tones to produce an “optimal” result. And although a set of

recommended values can be found for portrait and fashion photography, they

tend to be absent when working with moving images. Why? Because there are too

many variables to allow for a single working standard.


There are far too many skin tones and undertones to categorize people, thereby

eliminating a set of standards on a geographical or racial basis. Modern films tend

to feature a lot of camera and subject movement, causing the lighting to be in

constant flux, which means any corrections applied to a single frame are undone

as the scene progresses. Many scenes make use of dramatic lighting and shadows

or bright color gels that artificially distort a subject’s skin tone, all of which results

in imagery that cannot be corrected in a consistent fashion.


The subject in this exercise is a perfect example of these factors: he is

simultaneously overexposed by direct sunlight and underexposed in the shadows,

and there is even a faint lens reflection near his hat, casting a slight green hue on

his forehead.


Ultimately, the best practice is to correctly color manage or balance footage to

bring out the most natural skin hues, ensure that the skin is not overexposed in

the scopes, and maintain the middle grays as captured by the cinematographer.

Creatively, you should grade your subject in a way that will produce the most

aesthetically pleasing result on your grading monitor. If the result is satisfactory

to you, then the grade can be considered successful.


TIP As you balance, match, and work on skin, you may find yourself often

switching between scopes. Click the Expand button in the upper right of the

Scopes palette to turn the scopes into a floating window. Set single, dual, and

quad views (enlarging the window if you are unable to change the view amounts)

and use the upper right settings to specify each scope type and adjust its settings.

You can save your configuration as a preset for future grading sessions by going

to Workspace > Layout Presets > Save Layout as Preset.


**Lesson 3 Correcting and Enhancing Isolated Areas** **135**


##### **Setting Skin Tone Saturation**

With the skin hue adjusted, you can make use of another HSL curve to address skin

saturation.

**1** Create a new serial node, and label it **Skin Sat** (node 03).

**2** Change the Curves palette mode to Hue Vs Sat.


You can use the Hue Vs Sat palette to make undersaturated items pop or make

oversaturated colors less distracting. When dealing with skin tones, saturation can

be subjective and dependent on factors like lighting and project genre. For example,

colors naturally appear less saturated on overcast days, and more pronounced in

comedy films. In this image, the saturation in the man’s skin needs very

little adjustment.

**3** In the viewer, click the man’s face to drop the three control points in the Hue Vs

Sat curve. Aim for the desaturated skin near his ear to focus saturation on the areas

that need it.

**4** Drag the two surrounding anchor points in opposite directions to widen the selected

hue range.

**5** Drag the central point up slightly to increase the saturation of the skin, taking care to

keep the colors natural.


In the vectorscope, ensure that the section of the trace you are affecting does not

extend farther than any other hue region. Even if it is within safe saturation and RGB

channel scope limits, an area that is more saturated relative to the rest of the image

will appear oversaturated on the screen.


**Lesson 3 Correcting and Enhancing Isolated Areas** **136**


Be careful not to get too aggressive when adjusting skin tones. The aim is not to produce a

magazine-cover look but to reduce minor imperfections and enhance the visibility of the

face. Getting too aggressive with the Resolve FX or HSL controls can result in plastic
looking or overly saturated skin that is even more distracting than the original

imperfections.


**Memory Colors**

Memory colors are colors for which human beings have an instinctive reference.

The most common of these are sky, grass, and skin tones that tend to be closely

imprinted in our perception of the world. As you grade, try your best to keep skin

hue and saturation natural to ensure audience immersion, unless the narrative

specifically calls for distortion. Man-made objects tend to have less color memory

associated with them, so you have more freedom to tweak the hue of a car or the

saturation of a character’s dress.


Continue using these techniques in new ways and combining qualifiers/Power Windows

with your own footage. If you’re uncertain how to proceed with a certain shot, write out a

workflow to help determine how you want the final output to look, and then work

backward to choose the tools and adjustments that will realize your goals. You’ll always

have several possible workflow options, so with experimentation and experience you will

learn which are the most visually successful and time efficient for you.





**Lesson 3 Correcting and Enhancing Isolated Areas** **137**


## **Self-Guided Exercises**

Complete the following exercises in the unfiltered 03 Matched Timeline to test your

understanding of the tools and workflows covered in this lesson.


**Clip 01** —Use Lum vs Sat in the HSL Curves to increase the saturation of the deer in the

center of the shot but keep the saturation of the blue gate the same.


**Clip 02** —Apply a window to isolate the rhino’s face between the bars, and then apply the

Contrast Pop effect (Resolve FX Color category) to increase the contrast in that portion of

the frame. The effect should immediately guide the eye without being overpowering.


**Clip 03** —Apply a window and use any sharpening method (Blur palette, Sharpen Edge

effect, or Soften & Sharpen effect) to enhance the numbers on the scale and make them

more readable. Track the window to the movement of the scale.


**Clip 04** —Apply a subtle circular vignette at the end of the pipeline in the shot with the

rhinos and horses. Create another node _before_ the vignette and increase the brightness

and contrast of the shot to enhance the color and detail.


**Clip 05** —Use the Color Warper’s Chroma Warp to tint the ground green, matching the

overall look of the scene to clip 04. Apply a window to limit the correction to the field.


**Clip 11** —Use the Tilt-Shift Blur effect to create an artificial shallow depth of field in the shot

with the man and his dog. Consider the composition of the clip—you might want to rotate

the angle of the Depth of Field.


When you’ve completed these exercises, open the 05 Completed Effects Timeline to

compare your work to the “solved” timeline. If you’re working in the free version of

DaVinci Resolve, open the 04 Completed Timeline to review the solutions without any

Studio effects.


**Lesson 3 Correcting and Enhancing Isolated Areas** **138**


## **Lesson Review**

**1** How are secondary color corrections different from primary color corrections?

**2** In the Window palette, which setting would you use to subtract the area of one window

from another window?

**3** What does the Hue Vs Lum HSL curve do?

**4** Which tool can you use to create a vignette?

**5** True or False? Track data generated in the Tracker palette can be copied and pasted

onto another window or node.


**Lesson 3 Correcting and Enhancing Isolated Areas** **139**


##### **Answers**

**1** Secondary color corrections affect only a part of the image, whereas primary

corrections affect the whole frame.

**2** The “mask” setting found to the right of the “invert” property in the individual window

controls allows you to subtract one window from another.

**3** The Hue Vs Lum HSL curve increases or decreases the brightness of a selected color.

In the naming convention of HSL curves, the first word prompts the selection, and the

second word effects the change.

**4** A circle Power Window can be used to create a custom vignette, or you could use the

Vignette effect from the Resolve FX Stylize category of the Effects Library.

**5** True. The function to copy and paste track data is found in the options menu of the

Tracker palette.


**Lesson 3 Correcting and Enhancing Isolated Areas** **140**


### Part II
# Managing Nodes and Grades

## **Lessons**


- Conforming an XML Timeline

- Mastering Node Trees

- Managing Grades Across Clips and Timelines


In Part II of _The Colorist Guide to DaVinci Resolve 20_, you’ll look at workflows beyond primary

and secondary color correction to improve your speed and consistency when grading.

Along the way, you’ll learn how to conform timelines from other applications, build grading

node structures with purpose, and use stills and versions to copy and retain grade data.


**Project File Location**

You will find all the necessary content for this part of the book in the folder

BMD 20 CC - Project 02. Follow the instructions at the start of every lesson to

find the necessary folder, project, and timeline. If you have not downloaded the

second set of content files, see the “Getting Started” section of this book for

instructions on how to do so.


**Managing Nodes and Grades** **141**


**This page is intentionally left blank** **142**


### Lesson 4
# Conforming an XML Timeline



XML (eXtensible Markup Language) is

one of the file types commonly used

to migrate timelines between different

editing applications.


However, XML migration can partially

fail due to variances in software design.

Migration inconsistencies can cause

problems when you receive content

edited in an external application

and want to grade and finish it in

DaVinci Resolve 20. Upon import,

you may find that some areas of

the timeline contain incorrect clips,

changed trims, or missing transform

changes and effects.



Time

This lesson takes approximately
2.5 hours to complete.

Goals

Importing an XML Timeline 144

Syncing an Offline Reference 151

Conforming a Timeline 153

Maximizing the Dynamic Range 168

Lesson Review 179


To ensure that an imported timeline is an exact replica of the editor’s work, you must use a

verification process known as _conforming_ to compare the reconstructed edit with a

reference video and confirm that every cut and effect is reproduced within

DaVinci Resolve. When an element is mismatched or missing, you must manually correct it

in the timeline.


In this lesson, you’ll look at the most common issues and practices associated with the

conforming workflow. You will also look at more advanced project setup practices using

DaVinci Resolve’s color management to produce optimal grading conditions.
## **Importing an XML Timeline**


The project you will be working on is a film trailer for a film called _Too Much Life_ .


You will start by reconstructing the trailer timeline from an XML file exported from the

editor’s software. You would ordinarily do this in a new DaVinci Resolve project, but for

the purposes of the upcoming lessons in Part II, you will import a .drp file that has been

prepared for you.

**1** Open DaVinci Resolve 20.

**2** Right-click within the Project Manager window and choose Import Project.

**3** On your hard disk, locate the BMD 20 CC - Project 02 folder.

**4** In the folder, select and import the **Project 02 –Too Much Life Trailer.drp** file.

**5** In the Project Manager, double-click the **Project 02 –Too Much Life Trailer** thumbnail

to open the project.


The project is already set up with bins but contains no media or timelines. You’ll import

the timelines and link the media required for the exercises in this section.

**6** In the edit page, select the empty 03 Timelines bin as the destination for the XML

timeline and choose File > Import > Timeline.


**Lesson 4 Conforming an XML Timeline** **144**


**7** In the BMD 20 CC - Project 02 folder, navigate to the XMLs subfolder. Locate the

**01_TooMuchLife_Trailer.xml** file and import it.


The Load XML dialog that appears allows you to set how your XML timeline and

associated media are imported.


The default settings can be left as they are because you want the project settings to

match that of the timeline and for DaVinci Resolve to automatically import the source

clips associated with the XML file into the media pool.


TIP Selecting “Ignore file extensions when matching” will allow you to choose

media that is in a different file format from the original timeline media,

provided that the filenames have remained the same. This option can be

extremely useful when switching between offline and online workflows, which

you will learn about later in this lesson.


**Lesson 4 Conforming an XML Timeline** **145**


**8** Click OK to close the dialog.


DaVinci Resolve will search for the files based on their last known locations in relation

to the XML file. Most often, drives and paths change during transfer, and a dialog will

ask for help in locating the missing files.

**9** If this dialog appears, click Yes to locate the missing clips.


You will indicate the specific location of the various media files in this timeline.

**10** Navigate to the BMD 20 CC - Project 02 folder and select the Video subfolder. Click OK

at the bottom of the dialog.


This action should reconnect most of your media. However, the dialog will appear

again, suggesting that some remaining clips (15 of 46) have not been located. This is

because you’ve specified the location of the video clips only.

**11** Click Yes again to locate the audio.

**12** In BMD 20 CC - Project 02, select the Audio subfolder and click OK.


The dialog will again state that some clips (12 of 46) are missing. The number of clips is

smaller this time, suggesting that successful links are being established, but you are

still missing the graphics and VFX clips.

**13** Click Yes to return to the storage dialog.

**14** Expand the Other folder and repeat steps 12–13 for the Graphics subfolder and then

the VFX subfolder.


Two remaining clips will not be found. This sometimes occurs when media in

the timeline is renamed, changed, or moved after the XML file has been generated.

Because of this change, DaVinci Resolve cannot establish a connection with the

missing media. You will resolve this during the conforming stage.


**Lesson 4 Conforming an XML Timeline** **146**


**15** Click No to indicate that you do not wish to keep searching for media and want to

proceed with the timeline import.


Another window appears. The log displays a summary of the migration process,

including a confirmation of the imported timeline and a list of migration issues

(translation errors). This summary can help eliminate some of the guesswork from

the conforming process.

**16** Read the log to see the name of the missing clips and click Close when you are done.


The timeline should now appear in the edit page and its media in the media pool.


TIP You can view the log of an imported timeline at any time. With the timeline

open in the edit page, click the media pool options menu in the upper right

corner and choose Show Import Log.


As long as the filenames of media files are not changed, relinking is a straightforward

process. For this reason, it’s highly advisable never to rename media and to work with the

original camera filenames throughout the entire post-production process.


**Lesson 4 Conforming an XML Timeline** **147**


##### **Project Housekeeping**

For easier project management, you will organize the imported files into bins and color

code your tracks.

**1** The timeline thumbnail is identified by a white timeline symbol in the lower left corner

and indicated as the active timeline by an orange tick in the upper left corner. It can

remain in the Timelines bin.


**2** The video clips all feature their original camera filenames, which start with the camera

angle letter followed by three digits, such as A009. Drag all 35 video clips into the 01

Video bin.

**3** The audio clips are all in the WAV format and feature a waveform in the thumbnail.

Drag the three audio files into the 02 Audio bin.

**4** Drag the remaining six titles and graphic clips into the 04 Graphics bin.


Among the graphics is a PNG file that appears to be offline. Most likely, the image was

moved or renamed after the XML was generated. However, the XML file provided


**Lesson 4 Conforming an XML Timeline** **148**


enough metadata to still represent the image in the timeline and media pool without

a link to the actual file asset. You will replace the file source to re-establish a link with

the renamed image.


NOTE In some operating systems, the **Chyron.png** may be absent from the

media pool when the XML timeline is imported in this exercise. If so, you will

import the graphic at a later stage. For now, skip to step 7 of this exercise.


**5** In the 04 Graphics bin, right-click **Chyron.png** and choose Clip Operations > Replace

Selected Clip

**6** In BMD 20 CC - Project 02 > Other > Graphics, select **Chyron_graphic.png** .


The red thumbnail and Media Offline placeholder in the timeline update to display the

graphic with the updated name.


**Lesson 4 Conforming an XML Timeline** **149**


You can further organize your media by separating the VFX composites from the

general video clips. This is easy to do when all the clips have a consistent naming

convention. In this case, all the VFX clips feature __vfx_ as a suffix.

**7** Open the 01 Video bin and click the Search magnifying glass icon in the upper right of

the Media Pool panel.

**8** Type **vfx** in the search field to filter the VFX clips.


**9** Drag the five VFX clips into the 05 VFX bin.

**10** Click the Search icon to disable the filter.


The timeline features three audio stems that contain the dialogue, sound effects, and

music on separate tracks. You can improve project navigation by labeling and color
coding these tracks.

**11** If you are working with short track heights, drag the A1 track header to expand it. This

will give you access to the customizable track label.


**12** In the A1 header, click Audio 1 and enter the new name **DIA** for “dialogue.”


**Lesson 4 Conforming an XML Timeline** **150**


**13** Repeat steps 11-12 for Audio 2 (new name **SFX** for “sound effects”) and Audio 3 (new

name **MX** for “music”).

**14** Right-click the SFX audio track header and choose Change Track Color > Navy.

**15** Right-click the MX audio track header and choose Change Track Color > Violet.


By labeling and color-coding video and audio tracks, you can more easily distinguish which

tracks to bypass during playback or where to drag new assets.
## **Syncing an Offline Reference**


With the XML timeline imported, you should now check the edit to ensure that every clip,

cut, and effect has successfully migrated. To aid in this stage of the conforming process,

the editor should provide a reference movie: a single exported video file of the final

timeline that you can use for visual verification of the imported timeline.


In this exercise, you’ll associate a reference movie with a timeline and ensure that it is sync’d.

**1** Go to the media page.

**2** In the media pool, select the 06 References bin as the target for the new media you are

about to import.

**3** In the media storage browser, navigate to the BMD 20 CC - Project 02 folder.

**4** In the Other subfolder, right-click **Too_Much_Life_REFERENCE.mov** and choose “Add

as Offline Reference Clip.”


The reference movie appears in the bin with a checkerboard icon in the lower left

corner, which indicates its status as an offline reference clip.


**Lesson 4 Conforming an XML Timeline** **151**


**5** Open the edit page.

**6** In the 03 Timelines bin, right-click 01_TooMuchLife_Trailer and choose Timelines > Link

Offline Reference Clip > Too_Much_Life_REFERENCE.mov.


**7** In the lower left corner of the source viewer, open the mode dropdown menu and

choose Offline. Doing so will switch the source viewer from showing source materials

to displaying the offline reference clip associated with the active timeline.


However, the viewer currently shows the red Media Offline frame. One of the most

common reasons a reference clip would appear offline is because its timecode does

not align with the timeline timecode.

**8** Open the 06 References bin and click the List View icon at the top of the media pool to

view the media metadata.

**9** In the Start TC column, look at the start timecode of the reference clip and compare it

to the start timecode of the timeline.


In editing programs, timelines tend to begin at the one-hour timecode (01:00:00:00) to

allow for leaders, color bars, and 1-kHz test tones before the broadcast starts.

Rendered video clips, as seen in video players and online video sites, tend to begin at

00:00:00:00, as is the case with this reference. You can easily correct this by changing

the start timecode of the reference clip to match the timeline.

**10** Right-click the reference clip in the media pool and choose Clip Attributes.


**Lesson 4 Conforming an XML Timeline** **152**


**11** In the Clip Attributes window, click the Timecode tab and enter **01** as the Current

Frame hour. Click OK to close the window.


If the reference movie does not immediately appear in the source viewer, check the

source viewer mode dropdown menu to ensure that Offline is still selected and jiggle

the timeline playhead to refresh the frame.

**12** Drag the timeline playhead to verify that the timeline and reference movie are linked.


TIP You can also drag and drop regular clips into the source viewer (when in

Offline mode) to link them to the active timeline.


You have likely noticed that the contrast and saturation of the clips in the two viewers

appear different. This is because the reference clip was rendered in the Rec.709 color

space, while the source media is still encoded with its original log curve. You will address

this with the help of DaVinci Resolve’s color management at the end of this lesson.
## **Conforming a Timeline**


With the reference movie in place, you can now inspect the timeline to address any visual

inconsistencies. Your primary task will be to ensure that the correct clips are on the

timeline and to check that their cuts are occurring at the right time. To accomplish this, you

must review the edit, cut by cut.


First, you will address the missing end credits graphic at the end of the timeline.

**1** Go to the media page.

**2** In the media storage browser, navigate to the BMD 20 CC - Project 02 folder > Other >

Additional_Media.

**3** Drag **05 End Card.mov** into the 04 Graphics bin of the media pool.


**Lesson 4 Conforming an XML Timeline** **153**


NOTE If your **Chyron.png** graphic was missing during the “Project

Housekeeping” exercise, navigate to the BMD 20 CC - Project 02 folder >

Graphics and drag **Chyron_graphic.png** into the 04 Graphics bin of the

media pool.


**4** Return to the edit page.


The end card media file is automatically recognized and assigned to the missing media

clip at the end of the timeline. Whenever source media maintains the same name as

the file path in an XML file, it will immediately appear in the timeline, even if imported

after the XML reconstruction.

**5** To prevent being distracted by the timeline audio during conforming, click the Mute

button to the right of the timeline toolbar.


**6** Move the playhead to the start of the 01_TooMuchLife_Trailer timeline.

**7** Press the Down Arrow on your keyboard until you navigate to the first video cut.


It’s obvious that the timeline clip does not match the clip in the reference video. The

text rendered with the reference video (called a _burn-in_ ) tells you that the clip should

be A205_C010, whereas the clip in the edit page timeline is A209_C015. This mismatch

could be caused by a clash in the tape/reel name or the editor making a change after

exporting the XML file.


To resolve this, you can manually import and assign the correct clip to the timeline.

**8** Enter the media page.

**9** In the media storage browser, return to the Additional_Media subfolder.


**Lesson 4 Conforming an XML Timeline** **154**


**10** Drag all the remaining video clips ( **A205_C010_0527Q2.mov**,

**A011_C001_0306HG.mov**, and **A012_C048_0227XG.mov** ) into the 01 Video bin of the

media pool.

**11** Return to the edit page.

**12** In the 01 Video bin of the media pool, click the **A205_C010_0527Q2.mov** thumbnail to

highlight it.

**13** In the timeline, right-click the second clip and choose “Conform Lock with Media

Pool Clip.”


Doing so replaces the clip in the timeline with the selected media pool clip, which now

matches the clip in the reference movie.


NOTE If the **Chyron.png** graphic is still offline on the timeline, perform

“Conform Lock with Media Pool Clip” with the **Chyron_graphic.png** you

recently imported.


If the clip in the media pool and the clip in the timeline have the same available timecode

range, the conform action will place the incoming clip using the same In and Out points as

the original cut. If the incoming clip does not have the necessary timecode range, the first

frame of the incoming clip will be aligned to the cut point.

##### **Fixing Translation Errors**


Continue to navigate down the timeline and look at the reference movie to check the clips,

edit points, transitions, and effects.

**1** Press the Down Arrow until you reach the video transition between clips 4

( **A213_C021_0609DF.mov** ) and 5 ( **A054_C019_0911Z** D_01.mov).


**Lesson 4 Conforming an XML Timeline** **155**


In the reference movie, the transition is a bright flash, mimicking the camera flash and

sound effect at that point in the trailer. Many transitions and effects are unique to their

respective applications, which means they are not retained when an XML is generated.

Instead, the code in the XML file will replace them with their nearest generic

equivalent. In this case, the transition in the timeline was swapped for a basic

cross dissolve.


NOTE When effects, transitions, or speed changes are lost during the XML

creation process, some applications will generate a “translation report” that

lists all the elements that could not be included in the XML metadata file. This

report usually appears alongside the XML and can be shared with you to assist

you with the conforming process.


DaVinci Resolve has a bright transition available in its effects library, so you will be able

to replace the generic dissolve with one that better matches the trailer.

**2** In the interface toolbar at the top of the edit page, open the Effects panel.

**3** In the panel sidebar, open the Video Transitions folder.

**4** Under the Fusion Transitions header, find the Brightness Flash transition and drag it

directly over the Cross Dissolve overlay in the timeline.


The Brightness Flash transition adopts the properties of the Cross Dissolve, such as

duration and alignment, and now better emulates the camera flash effect.

**5** Drag the playhead across clip 5 ( **A054_C019s_0911ZD_01.mov** ) to review it past

the transition.


In addition to checking the timeline clips and their edit points, your conforming

process should ensure that all frame transforms and speed changes are present. A

simple side-by-side comparison cannot always achieve this, so DaVinci Resolve

provides the option to superimpose the reference movie on the timeline viewer. This

can help you check whether clips are identically framed.


**Lesson 4 Conforming an XML Timeline** **156**


**6** Right-click the timeline viewer and choose Horizontal Wipe.


The timeline clip is displayed to the left, while the reference clip is displayed to the right.


**7** Drag the wipe line left and right to compare the placement of the timeline clip to

the reference.


Using the wipe for comparison reveals a mismatch in the shot framing. To fix it, you

can switch to a composite mode that directly overlays the images.

**8** Right-click the timeline viewer and choose Difference to highlight where the clip is

misaligned.


**Lesson 4 Conforming an XML Timeline** **157**


**9** In the timeline, click clip 5 and open the Inspector panel in the upper right corner of

the edit page.

**10** In the Transform controls, increase the Zoom value until the size appears similar to the

reference movie (1.100).

**11** Using the faces and shirt stripes as guides, drag the X Position left (-100.00) and the Y

Position down (-50.00) until the timeline clip completely overlaps the reference. When

performing these matches visually, you may need to go back and forth between the

position parameters to get a perfect fit.


TIP You can use the Inspector’s Anchor Point parameters to simplify the

process of matching a reframed clip. First, click the Transform button in the

lower left of the timeline viewer to activate onscreen controls. Then, drag the

anchor over a distinct object (like a window frame or the edge of a building).

When you now adjust the Inspector’s Transform controls, the zoom will

expand from the new anchor position, simplifying the process of lining up the

shot scale and position.


When you no longer see a “double effect” on the actors in the viewer, the framing is

successfully matched. If you were working on images with identical colors, the viewer

would become black to signify that no visual differences remained between the clips.


**Lesson 4 Conforming an XML Timeline** **158**


**12** Right-click the timeline viewer and choose No Wipe to return to the standard viewer.

**13** Close the Inspector. If you are working on a 1920 x 1080 resolution (or smaller)

monitor, this action will bring back the source viewer.

**14** Press the Down Arrow to navigate to the next video cut. This is the clip that was

missing when the XML timeline was imported.

**15** Press Command-+ (plus sign) in macOS or Ctrl-+ (plus sign) in Windows to zoom in to

the offline clip in the timeline.

**16** Right-click the clip and choose Conform Lock Enabled to disable the conform lock. The

clip is now receptive to all media that contains similar metadata to the one specified

in the XML.


In the lower left corner of the timeline clip, a red attention badge icon <!> indicates a

potential metadata clash with another clip in the media pool.

**17** Double-click the attention badge on the clip.


The Conflict Resolution window appears, displaying all the clips in the bin that

potentially match the clip in the XML timeline. You can now select the correct clip

according to the reference movie and burn-in.


**Lesson 4 Conforming an XML Timeline** **159**


**18** In the Conflict Resolution window, select the clip of the boy in the classroom

( **A012_C048_0227XG.mov** ) and click Change.


The correct clip is placed in the timeline and matches the reference movie. To remove

the now black-colored resolved badge and confirm the new clip as correct, you can

lock the conformed selection.

**19** In the timeline, right-click the clip and choose Conform Lock Enabled.


In addition to conforming clips with clashing metadata, the Conflict Resolution window

is also popular with VFX workflows. When bringing in new versions of rendered VFX

clips, instead of manually editing them into the timeline, you can opt to disable the

conform lock, open the conflict resolution window, and choose the latest version of

the VFX clip.

##### **Trimming Media**


As you continue conforming the timeline, make sure to keep an eye on the exact

occurrence of cut points and the timing of the content within the clips.

**1** Press the Down Arrow until you reach the cut between clips 10 and 11 at 01:00:25:11.


The image in the timeline viewer does not match the reference movie.


**Lesson 4 Conforming an XML Timeline** **160**


**2** Press the Right Arrow until you reach the cut in the reference movie, which should be

at 01:00:25:15.

**3** Drag the trim point between clips 10 and 11 until it matches the cut in the

reference movie.


TIP For finer trim control, select the cut point and press the Comma (,) and

Period (.) keys to nudge the cut one frame at a time.


**4** Press the Left and Right Arrow keys to verify that the cut now lines up between the

two clips.


Though the cut now matches, the content of clip 11 is not accurate. It appears to be a

few frames ahead of the reference. You can use the trim editing tool to slide the

content of the clip.

**5** In the timeline viewer, enable Mix Wipe mode to blend the reference and timeline clips.

**6** In the timeline toolbar, change the edit mode to Trim Edit mode.


This will allow you to perform rippling, trimming, slipping, and sliding functions that

are not possible in the default Selection mode.

**7** Click the center of clip 11 ( **A054_C019_0911ZD_02.mov** ) and drag in either direction to

see the change in the timeline viewer.


By slipping the clip, you keep its place in the edit while changing the range of media

that appears between the In and Out points.


**Lesson 4 Conforming an XML Timeline** **161**


**8** Slip the clip right until the mixed images in the timeline viewer are lined up, and then

release the mouse button.


Before After


**9** Turn off the Mix Wipe mode and compare the frames in the two viewers.

**10** In the timeline toolbar, change the edit mode back to Selection mode.

**11** Press the Left Arrow and Right Arrow keys to ensure that the actors’ movements

remain consistent with the reference clip.

**12** Continue to press the Down Arrow to check the remainder of the clips.


When finished, the last remaining element to match will be the frame itself. You may

have noticed that most of the timeline clips have a 2:1 aspect ratio (with baked-in

letterboxing), while some of the graphics and clips are full frame. Changing the aspect

ratio of footage within a standardized frame (in this case, 1.77:1, also known as 16:9) is

called _blanking_ . You will apply blanking to make the timeline framing consistent.

**13** Choose Timeline > Output Blanking > 2.0.


TIP When changing a project’s aspect ratio, it’s usually advisable to apply

blanking to a timeline rather than setting a custom resolution. This is because

most projectors and professional deliverable formats anticipate a

standardized resolution, such as HD (1920 x 1080), 2K DCI Scope (2048 x 858),

4K DCI Flat (3996 x 2160), and so on. Setting a custom resolution carries the

risk of your project being rejected or incapable of playback on a device.


**Lesson 4 Conforming an XML Timeline** **162**


You have now successfully conformed this timeline. Although it’s natural to feel that

something has gone wrong with your workflow when the timeline presents issues during

XML migration, it’s important to remember that this is a completely normal and anticipated

stage of post-production. It is encountered in projects of all calibers and stems from the

fact that each of the dozens of applications that you may use when collaborating on a film

has a different interpretation of the XML tags.


**Tips for Preparing Timelines for XML Export**

You can reduce the amount of conforming you need to do by asking your

collaborators to follow a few rules before generating an XML file from their

editing software:


**1** Flatten the timeline to one video track, if possible. If there are graphics and

overlays, reduce to the lowest possible number of tracks. Delete all

empty tracks.


**2** Remove all audio clips and provide a final stereo or 5.1 mixdown.


**3** Decompose, flatten, or render any compound clips, subsequences, or nested

timelines.


**4** Remove software-specific effects, grades, adjustment layers, and plug-ins.

If they must be incorporated in the grade, video media should be rendered

with the effects already baked in.


**5** Break up feature-length projects into 20-minute timeline reels.


In recent years, a new format called OTIO (Open Timeline IO) has been created by the

Academy Software Foundation to act as a single standard for importing and exporting

timelines between applications without the need for extensive conforming. The format

uses consistent tagging and offers greater compatibility between platforms and

applications than XML, AAF, or any other migration format. If it is available to your

collaborators, request that they send you their timelines in the OTIO format.


One of the major advantages of performing your entire post-production workflow in

DaVinci Resolve is the substantial reduction of migration and project management issues.

An edit can be ingested, edited, graded, mixed, and delivered without ever needing to

be conformed.


**Lesson 4 Conforming an XML Timeline** **163**


TIP When sharing a timeline with someone who is also working in DaVinci Resolve,

you have several options:

 - Export the **timeline** (from the media pool) in the native DaVinci Resolve

Timeline ( **.drt** ) format for conform-free migration.

 - Export the entire **project** (from the Project Manager) as a DaVinci Resolve

Project ( **.drp)** file to share all project metadata, bins, and timelines.

 - Export the project **archive** (from the Project Manager) as a DaVinci Resolve

Archive ( **.dra** ) to share the entire project and all its media contents.

##### **Offline and Online Workflows**


In post-production, media generally undergoes two phases: the offline stage and the

online stage.


When editors and their assistants receive the original camera footage (rushes) from

production, it is typically in a raw camera format that is far too processor-intensive to play

back in real time. Since playback speed is of the utmost importance to editors, they will

usually compress it into a format that is much lighter on the workstation, with the intention

of relinking it to the camera originals after editing is completed. Compression of camera

footage for editing is called _transcoding_ and typically employs intermediary codecs such as

ProRes or DNxHD/HR. Working with transcoded (also known as _proxy_ ) media is referred to

as _offline editing_ .


When the final edit is locked, it will typically be forwarded to the colorist and/or finishing

artists. Unlike the editors, their priority is not in the playback performance of the media

but rather its visual fidelity. They will meticulously relink all the proxy media to the camera

originals to allow for optimal quality when grading and delivering the film in a process

known as _online editing_ .


The media in this project’s timeline is encoded in the intermediary DNxHD 115 1080p

codec, which is commonly used for editing but not typically for grading or deliverables. It

will act as a stand-in for the camera originals in this project, as the raw files would be far

too large to share with you. If you are curious, the trimmed camera footage for this

2-minute trailer is over 100 GB!


**Lesson 4 Conforming an XML Timeline** **164**


##### **Swapping Transcoded Media** **for Camera Originals**

If you receive a timeline that is edited with transcoded media, you can link it to the camera

originals using the Reconform function in DaVinci Resolve.


NOTE You do _not_ need to complete this exercise for the 01_TooMuchLife_Trailer

timeline. This section is designed to familiarize you with the process of swapping

proxy media with camera originals for your own future projects.


It’s a good idea to make a copy of your timeline before you attempt to make major changes

to its structure.

**1** Right-click the transcoded timeline and choose Duplicate Timeline. Rename the new

timeline according to your preferred naming convention.

**2** Double-click the new timeline to launch it in the edit page.

**3** Drag to select all the video clips on the timeline.

**4** Right-click any clip in the timeline and deselect Conform Lock Enabled. Doing so will

disable the clips’ lock on their media file paths and prompt them to acknowledge all

media that shares similar metadata.

**5** From the File menu, choose Reconform from Media Storage.


**Lesson 4 Conforming an XML Timeline** **165**


The Conform from Media Storage window allows you to refine the media that is

associated with the clips in the timeline.


TIP In cases where your camera originals have already been imported into

the media pool, you can select “Reconform from Bins.”


**6** Under Timeline Options, choose “Attempt to reconform Selected Clips in timeline.”

**7** Under Choose Conform Folders, select the location of the camera originals.

**8** Under Conform Options, deselect Timecode if you know the transcodes didn’t retain

the original camera timecode. Otherwise, leave this option enabled.

**9** Next, select File Name and choose “Loose filename match.”


This allows you to replace proxy files with camera originals (or vice versa) if only the

extension of the filename has changed during transcoding.

**10** Click OK.


The camera originals will populate the media pool and replace the clips in the

active timeline.

**11** To lock the clips to the timeline, select them, right-click, and choose Conform

Lock Enabled again.


This method of swapping source files gives you full control over the media used in the

timeline without the need to import additional XMLs or change the file paths of the clips in

the media pool. An important component of this workflow is a well-organized and

consistently labeled file system, which is a practice recommended across all post
production workflows.

##### **Exploring DaVinci Resolve Proxy Workflows**


If you are using DaVinci Resolve for the entirety of your post-production, you can opt for

some faster and more efficient options when switching between transcoded proxy media

and original camera footage in your timeline.


**Lesson 4 Conforming an XML Timeline** **166**


**Generate Proxy Media in the Media Pool**


You can generate proxy media directly in the media pool after importing your source clips.

Select the necessary clip(s) in the bin, right-click, and choose Generate Proxy Media. This

will prompt proxy media to be generated in the location specified in the Working Folders

(“Proxy generation location”) of the Project Settings. If you already have transcoded media

on hand, you can link it to the camera originals in the media pool by selecting the clips,

right-clicking, and choosing Relink Proxy Media.


**Blackmagic Proxy Generator**


DaVinci Resolve comes with a stand-alone application that can generate proxies in the

background while you continue to work on your project. The Blackmagic Proxy Generator

features a Watch Folders list, which creates a live link between a location on your drive and

its respective proxy folder. As soon as you drag media from each day’s shoot into the

watch folder, the proxies will automatically begin generating and will then link to the

camera originals as soon as those are added to the media pool.


**Switching Between Proxy Media and Original Camera Footage**


In both instances described above, the proxies and camera originals will occupy the same

space in the media pool. This enables you to edit and grade with just one set of media and

choose which version you wish to see at any given time. To switch between the versions, go

to the Playback menu and navigate to Proxy Handling. Selecting Disable All Proxies will

force only the camera originals to be visible in the timeline. If the original media is absent,

you will see a red Media Offline frame in the viewer. This is optimal for final grading and

delivery when you want to be certain that you’re only working with the original media.

Selecting Prefer Proxies will switch all media to its associated proxy clips, where available. If

any clips have no proxies, the original camera footage will be used. The same applies to

Prefer Camera Originals, which will display proxy media in instances where the original

camera footage cannot be found. These last two options are optimal if you want to avoid

the red Media Offline frame from appearing in your timeline and final render. You can also

quickly access all these proxy controls in the upper right corner of the viewers in the

media, cut, edit, color, and deliver pages.


**Lesson 4 Conforming an XML Timeline** **167**


## **Maximizing the Dynamic Range**

The grading potential of an image is determined primarily by its dynamic range, which is

the range from its darkest point to its brightest point, and the method with which that

range is encoded in the digital video file.


HD consumer and broadcast video cameras tend to record using a standard dynamic

range and encode it with a gamma curve that mimics human vision. This ensures that the

image looks as close to real life as possible and displays as such on an HDTV or computer

monitor. However, high-end prosumer and professional digital film cameras can capture

and encode higher dynamic range footage along a logarithmic curve that prioritizes

preservation of detail (especially in the highlights) over a realistic depiction of the original

colors and contrast. This curve gives you greater flexibility for manipulating brightness and

contrast in post-production without distorting the image.


Ungraded video with a 2.4 gamma curve


**Lesson 4 Conforming an XML Timeline** **168**


Ungraded footage within a log curve


A byproduct of encoding footage with a log curve is that footage initially appears flat and

desaturated.


One method of addressing this is by using the primary grading tools to increase the

contrast and saturation of the image until it starts to look “correct” in the viewer (as you did

in Part I of this guide). This manual process of correcting log footage is called _display-_

_referred color management_ . Because DaVinci Resolve receives no direction on how the

source media is meant to look, configuring its luminance and saturation is left to the

colorist and their color grading _display_ . This process can also involve using lookup tables

(LUTs) to convert the footage from log to the intended deliverable output, such as Rec.709

Gamma 2.4.


Another method of processing log-encoded media is by having DaVinci Resolve

automatically map the colors from the original camera color space to the intended

deliverable standard. This is known as _scene-referred color management._ DaVinci Resolve


**Lesson 4 Conforming an XML Timeline** **169**


interprets the color profile of the camera sensor used to capture the media and precisely

calibrates the luminance and saturation levels to replicate how the _scene_ appeared on the

day of the shoot. This adjustment is far more accurate because every camera

manufacturer will have a unique RGB channel configuration and a unique log curve shape

that cannot easily be replicated using standard primary grading adjustments. Another

advantage of this method is that you can color manage media from different sources to a

single output for quick and consistent project setup.

##### **Setting Up Color Management**


In this exercise, you will color manage the log-encoded media of the _Too Much Life_ project

to output to a more visually accessible and grade-friendly color space.

**1** Open the Project Settings by clicking the gear icon in the lower right corner of the

workspace.


**2** Click Color Management in the Project Settings sidebar.

**3** In the Color Space & Transforms section, set the “Color science” menu to DaVinci YRGB

Color Managed. Doing so will activate scene-referred color management and reveal

the color processing modes and output color space options.


With “Automatic color management” enabled, the color processing mode is simplified

to just two working environments: SDR (standard dynamic range) and HDR (high

dynamic range). When you select a preset in this dropdown menu, a brief description

underneath will summarize the preset’s intended use.


**Lesson 4 Conforming an XML Timeline** **170**


**4** Deselect “Automatic color management.”


The color management options have mostly stayed the same, but you now have a

wider selection of color processing modes and output color spaces for more precise

setup. By default, the project is set to operate in SDR Rec.709, which is the ideal

environment when working with SDR footage with the intention of delivering

to the web.


As your footage is log-encoded, it makes sense to operate in a wider gamut and

with a higher dynamic range to allow for greater grading potential and a multitude

of deliverable options (both SDR and HDR).

**5** Set the “Color processing mode” to Custom to unpack the full list of color

management parameters.


**6** Set the “Input color space” to REDWideGamutRGB/Log3G10, which is the original

camera color space designed to encompass all colors that can be recorded by RED

cameras without clipping.


The timeline color space is your working environment and determines the behavior of

the color page grading tools and nodes.


**Lesson 4 Conforming an XML Timeline** **171**


**7** Set the “Timeline color space” to REDWideGamutRGB/Log3G10 too.


In addition to being a camera color gamut, REDWideGamutRGB is also a great working

environment that ensures accurate mapping of RED footage. DaVinci Resolve features

several wide gamut standards, including ARRI WideGamut and Blackmagic Design’s

Davinci Wide Gamut, allowing you to work with any camera source.


The timeline working luminance affects how high dynamic range images are mapped

to the timeline color space. The default setting, HDR 1000, will map a 1000-nit HDR

signal to be viewable on an SDR monitor while gently rolling off highlights to prevent

clipping or bunching at the top of the waveform. If you are uncertain of the number of

stops (or the nit count) in your incoming footage, you can maximize this value to

ensure that all highlights are rolled off, no matter how high.

**8** Set the “Timeline working luminance” to Custom and enter **10000** nits.


The output color space determines the deliverable standard that the Timeline color

space is mapped to. This should generally be the color space of your computer or

grading monitor or your intended deliverable format.

**9** If you’re working on a standard computer monitor, leave the “Output color space” set

to Rec.709 (Scene). This is an appropriate setting for most web deliverables and will

emulate the appearance of SDR broadcasts with the gamma function baked directly

into the image. If you’re new to color grading or if your output is mainly web content,

this setting is perfect for you.


TIP If you’re using a Mac display, you’ll need to choose an output color space

based on your ICC display profile. To find the display profile in your macOS, go

to System Preferences > Displays > Color tab. On newer displays, the profile

will usually be Display P3. To set the correct output color space for Display P3

in the Project Settings, select “Use separate color space and gamma” under

“Color processing mode,” and in the “Output color space” field, set the left

parameter as P3-D65 and the right parameter as sRGB.


**Lesson 4 Conforming an XML Timeline** **172**


If you are working with a grading monitor, change your output color space to match

the monitor’s settings. On a broadcast monitor, this will typically be Rec.709 Gamma

2.4. An additional benefit of working with the output color space set to Rec.709

Gamma 2.4 is access to the RED IPP2 tone mapping option in the Output DRT

parameter.


The Input and Output DRT parameters inform how gamuts and highlights are rolled

off during video signal processing to ensure that the primaries and tonal ranges of

media from different sources are better matched when mapped to a single timeline

and output standard. This is particularly noticeable when mapping between

dramatically different gamut sizes and dynamic ranges (such as mapping HDR source

media to an SDR deliverable).


The default DaVinci option ensures smooth luminance roll-off in the shadows and

highlights, and controlled desaturation of image values in the very brightest and

darkest parts of the image. When working with RED footage, the RED IPP2 option also

performs careful gamut and highlight management, as well as providing additional

settings for output tone map type, highlight roll-off intensity, and HDR peak nits.


TIP Hold Option (macOS) or Alt (Windows) when pressing Save to commit

changes while keeping the Project Settings window open. This way, you can

quickly experiment with parameters without needing to constantly relaunch

the Project Settings window.


**10** Click Save to close the Project Settings.


Color management is now set up in the project, but you might not see an immediate

change in the viewer. This is because video media automatically adopts the default

Rec.709 (Scene) input color space when it is first imported. You will need to override

the input color space of the clips on the project for the color management to

take effect.

**11** In the media pool, open the 01 Video bin.

**12** Press Command-A (macOS) or Ctrl-A (Windows) or drag to select all the clips

in the pool.


**Lesson 4 Conforming an XML Timeline** **173**


**13** Right-click any of the selected clips and choose Input Color Space > Project 
REDWideGamutRGB/Log3G10. This will not only indicate the input color space of the

clips but also link their behavior to the Project Settings.


By correctly setting up the input color space of the media, the colors of the timeline

clips will shift from the REDWideGamutRGB color gamut and Log3G10 log curve to

Rec.709 with the standard 2.4 gamma curve. As a result, the clips will appear more

vibrant and with more pronounced contrast.


DaVinci YRGB color management applies to all the clips in a project. If certain clips

come from different sources, you can reassign their individual input color spaces

through the media pool’s contextual menu (or the color page’s clip timeline).

**14** In the media pool, open the 05 VFX bin.


The VFX clips with the _vfx suffix that you filtered earlier were rendered out with no

gamma (or transfer function), making them _linear_ . VFX artists and post-houses will

commonly work with and render composites in this way.

**15** Select the five VFX clips.

**16** Right-click any of the selected clips and choose Input Color Space > Linear > Linear.


The VFX media and its corresponding timeline clips will now more closely match the

rest of the footage in the project.


The graphics elements were all rendered in Rec.709 or sRGB, so you will not need to

change their input color spaces.


TIP You can use a smart bin to filter clips based on their sources and then set

their input color spaces in batches to save time.


**Lesson 4 Conforming an XML Timeline** **174**


With project-wide color management set up, you are ready to begin grading. In later

lessons, you will see other methods of color management within DaVinci Resolve, like

node-based Color Space Transforms (CSTs), ACES, and LUTs.


**Using DaVinci Resolve with Mac Displays**

The macOS internal color management utility, ColorSync, uses metadata to match

colors between its applications. As third-party software, DaVinci Resolve is not

impacted by ColorSync, which is why the videos rendered out of DaVinci Resolve

might look different when viewed in Safari or QuickTime. To avoid this, you can

choose to include DaVinci Resolve in ColorSync’s internal matching. Go to

DaVinci Resolve > Preferences > System, and in the General category, select “Use

Mac Display Color Profile for Viewers.” This will enable DaVinci Resolve to use

whichever color profile you have selected in the macOS Color preferences,

including custom color profiles and calibration software profiles. Please note that

this will only affect the appearance of the footage in the viewers. In Lesson 10,

“Delivering Projects,” you’ll find additional instructions on how to correctly render

videos to appear the same across all applications and web browsers.


DaVinci YRGB color management offers a structured, solid foundation for color grading by

mapping the starting point of video media (from any number of sources) to a single,

grade-appropriate color standard. Its advanced tone mapping ability means that

highlights are gently rolled off, preserving maximum quality. Compare the treatment of the

highlights in the reference movie (which underwent standard log-to-Rec.709 conversion) to

the DaVinci YRGB color management tone remapping.


This method of color management results in higher-quality visual output, more

consistency in the performance of the color page grading tools, and an easier delivery

process in which the project output color space can be remapped to any number of

professional deliverable standards.


**Lesson 4 Conforming an XML Timeline** **175**


Note that color management does not eliminate the need for balancing and matching.

Although the color mapping process takes the guesswork out of normalization and

saturation adjustment, it does not account for the internal color balance/temperature

setting of the camera, over/underexposure, and the differences in lighting conditions

between shots. It is standard practice to balance and match shots even when employing

color management.


**When You Don’t Know the Camera or Format**

DaVinci YRGB color management operates at its best when you know and indicate

the correct input color space data. But identifying that data can be tricky when the

origins of the footage are unknown or when the color space details were not

included during file transfer. You can derive some useful data by examining clip

properties, but that will not always provide information about the camera model

or log curve. You can acquire the most definitive information by contacting the

filmmakers directly and requesting this information. If all else fails, you can bypass

DaVinci YRGB color management altogether and manually normalize the clips

using the primary grading palettes.


NOTE Due to the size of the project, the video clips were compressed to allow for

sharing via the web. As a result, you will see some compression artifacting, such as

posterization and macro blocking, in the viewer and scopes. When working on

actual projects, you should aim to work only with camera originals or high-quality

(10- and 12-bit depth) compression formats like ProRes 4444 and DNxHR to avoid

such artifacts.

##### **Changing the Output Color Space**


One of the most powerful aspects of using a color-managed workflow in DaVinci Resolve

is that you can change the output color space at any time. Doing so is particularly helpful

when you need to output multiple masters to different destinations. For example, you

might need one master for broadcast/web (Rec.709), another for UHD television

(Rec.2020), and yet another for digital cinema (DCI-P3). DaVinci Resolve manages these

color transformations without the need to regrade the timeline.


**Lesson 4 Conforming an XML Timeline** **176**


**1** Open Project Settings > Color Management.

**2** Set the Output Color Space to P3-D65 ST2084 4000 nits.


**3** Click Save.


The color space is changed, and the viewer reflects the updated results. On a standard

computer monitor, the colors will now appear flat. However, if you had a calibrated

HDR P3-D65 monitor capable of displaying 4000 nit luminance, the clips would look

nearly identical to their appearance on your HD Rec.709 display with the previous

output settings. This is how you can use color management to effortlessly switch

between different monitoring and deliverable standards.


**Accurate Color Monitoring in DaVinci Resolve**

DaVinci Resolve was designed to work with industry-standard calibrated external

displays connected via video output interfaces for critical color evaluation.


Most computer monitors are incapable of displaying the color gamut and dynamic

range required for broadcast and theatrical distribution. Additionally, most

computer displays have their own color and contrast calibration as determined by

the manufacturer, which is further altered by the operating system’s internal color

management. For this reason, their color accuracy cannot be guaranteed upon

delivery, and the resulting video could even shift in appearance when viewed in

different video players on the same machine.


Ideally, you should use an external monitor and video interface if color accuracy is

important to you. Alternatively, you could use a color calibration probe to analyze

your computer display and generate a LUT that will map the display to the

correct standard.


**4** Open Project Settings > Color Management.

**5** Set the Output Color Space back to the default Rec.709 (Scene) or your

preferred display.

**6** Click Save.


**Lesson 4 Conforming an XML Timeline** **177**


TIP If you know in advance that you will deliver content in multiple standards, you

should start your workflow in the widest gamut and then work your way down. For

example, if delivering for web (Rec.709 (Scene) or Gamma 2.2), digital cinema

projection (DCI-P3), and HDR broadcast (Rec.2100 ST2084), the best option would

be to grade your project for HDR first. Then, duplicate the project and calibrate the

output color space to DCI-P3. Review the timeline, make the necessary highlight

adjustments, and render the cinema grade. Finally, repeat the process for the web

deliverable.


NOTE You will continue to work on the timeline created in this lesson over the

next two lessons. If you would like to verify that your timeline is correct or are

uncertain of the accuracy of your conforming, import the **01_TooMuchLife_**

**Trailer.drt** trailer (BMD 20 CC - Project 02 > Timelines) into the media pool. If any

media appears offline, click the red Relink Media button in the upper left corner of

the media pool and specify the location of the Project 02 media on your

workstation.


To ensure the project management is set up correctly, right-click the imported

timeline and choose Timelines > Timeline Settings. Select Use Project Settings in

the lower left of the settings panel to link it to the project-wide color management

settings. Set up color management as described in the “Maximizing the Dynamic

Range” exercise in this lesson.


You can then use this ungraded, conformed timeline to complete the next two

lessons in this book.


**Lesson 4 Conforming an XML Timeline** **178**


## **Lesson Review**

**1** During project migration, what is a translation error?

**2** How do you assign an offline reference movie to a timeline?

**3** When loading an XML file, why would you opt to “Ignore file extensions

when matching”?

**4** How do you apply letterboxing in the edit page?

**5** Where do you activate DaVinci YRGB Color Management?


**Lesson 4 Conforming an XML Timeline** **179**


##### **Answers**

**1** Translation errors are inconsistencies that appear when reconstructing timelines

between applications.

**2** Right-click a timeline and choose Link Offline Reference Clip to assign a reference

movie to it. You can also drag and drop any clip from the media pool into the source

viewer while it is in Offline mode to associate it with the active project timeline

**3** You would choose to ignore file extensions to link to media in a different format during

timeline reconstruction. This is commonly used when switching from offline to online

editing or vice versa.

**4** Timeline > Output Blanking features a list of standard letterbox ratios. You can also

create custom letterboxes using a couple of Solid Color generators!

**5** In Project Settings > Color Management, set Color Science to DaVinci YRGB

Color Managed.


**Lesson 4 Conforming an XML Timeline** **180**


### Lesson 5
# Mastering Node Trees

The Node Editor is a powerful feature

of the color page that enables you to

maintain precise control over the final

appearance of images. You can use

it to separate the different stages of

grading while ensuring an enhanced

color output with minimum quality

degradation. Additionally, the Node

Editor allows for some truly advanced

secondary grading configurations, the

foundations of which you will explore in

this lesson.



Time

This lesson takes approximately
2.5 hours to complete.

Goals

Understanding Node-Based
Grade Compositing 182

The Importance of Node Order 183

Creating Separate Processing
Branches with a Parallel
Mixer Node 198

Compositing Color Effects
with the Layer Mixer Node 205

Using External Mattes 216

Self-Guided Exercises 222

Lesson Review 223


## **Understanding Node-Based** **Grade Compositing**

Node-based compositing differs from the layer-based system familiar to many post
production software users. Unlike layers, in which the visuals are compounded based on

their order in the layer stack, nodes process a single RGB signal, modifying it

along the way.


As each node affects the image, it outputs the altered signal via an RGB connection line

until the final RGB data reaches the output node of the Node Editor. This output node

presents the image in its final state to the viewer and determines how the media will look

when rendered.


Nodes are capable of reusing information generated in earlier nodes, substantially

reducing the amount of processing power required to assemble and output a final image.

This capability is particularly useful when working with keys, such as those generated by

qualifiers and Power Windows.

##### **The Anatomy of a Node**


The color page’s node graph is read from left to right. The RGB signal that constitutes the

image begins at the leftmost green node—the source input—and travels through the

connection lines that link the corrector nodes until it reaches the node tree output to the

right. The RGB signal must be uninterrupted for the node grades to be correctly compiled

and output.


**Lesson 5 Mastering Node Trees** **182**


Standard corrector nodes have two inputs and two outputs.

|Col1|Col2|Col3|
|---|---|---|
||||
||||



The green triangle and square shapes at the top of either side are the RGB inputs and

outputs. These carry the pixel data of the image, which is manipulated within the node

using the grading tools and effects of the color page. Corrector nodes can accept only

one RGB input but can output multiple RGB signals to other nodes.


The blue shapes are the key inputs and outputs. These enable you to transfer the key

data generated by the secondary grading palettes and tools (or external mattes) to be

used by other nodes.
## **The Importance of Node Order**


The RGB signal output of each node incorporates all the adjustments made within that

node and directly affects how subsequent nodes interact with it. The following set of

exercises demonstrates how nodes impact one another.


NOTE The node structures of every exercise in this segment can be found in the

Node demos album of the gallery in the color page.

##### **Influence of Color and** **Saturation Across Nodes**


You can see how a node placed at an early stage of the grading pipeline influences the

following nodes by removing its saturation and observing the results.

**1** Open the Project 02 – Too Much Life Trailer project.

**2** Enter the color page.

**3** Select clip 13 (A009_C015) in the 01_TooMuchLife_Trailer timeline.


**Lesson 5 Mastering Node Trees** **183**


**4** Label the first node **BW** .

**5** In the left palettes, open the RGB Mixer palette.

**6** Select Monochrome (at the bottom of the palette) to convert the image to black

and white.


The RGB Mixer allows you to remix different amounts of red, blue, and green data from

one channel to another for creative and practical purposes. When in monochrome

mode, it gives you complete control over the strength of the individual RGB channels

and can be used for tweaking black-and-white images to create an aesthetically

pleasing balance of natural elements such as skin, sky, and trees.

**7** Drag up the Red Output’s R bar to increase the strength of the red channel in the

image. This change will brighten the performers’ faces and darken some of the

clothing, giving the image a satisfying contrast.

**8** Create a second node and label it **Sepia** .

**9** Open the Primaries color wheels palette and drag the Offset color wheel toward

orange–yellow to give the image a sepia tint.


**10** Click node 01 (BW) and return to the RGB Mixer palette.

**11** Drag the Blue Output’s B bar up and down to increase and decrease the strength of

the blue channel in the image.


The effect on the final sepia grade shows that the contrast created in the first node

continues to impact the final image even after a second node dramatically changes

its appearance.


For an even clearer visualization of how node order impacts the grade, you can swap

the two nodes.


**Lesson 5 Mastering Node Trees** **184**


**12** Click node 02 (Sepia) and press E to extract it from the node tree.

**13** Drag the disconnected node onto the connection line to the left of node 01 until the

line turns yellow and a + (plus sign) appears.


TIP A quick way to swap two nodes is to hold Command (macOS) or Ctrl

(Windows) and drag one node over another.


When reconnected, the image becomes black and white. Although the sepia grade still

performs its function in the first node, it appears to be overridden by the BW node.


NOTE Nodes that follow the active node in the node tree are referred to as

being downstream. Nodes that precede the active node are upstream.


**14** To further demonstrate upstream nodes’ continued impact on downstream nodes,

select node 01 (Sepia) and drag the Offset color wheel toward blue.


Once again, there is a change in the viewer despite no visible blue hues in the final

image. This is because you initially boosted the red channel output in the BW node’s

RGB Mixer, making it sensitive to changes in the red channel. Dragging the Sepia

node’s Offset wheel toward a cooler shade directly impacts the brightness achieved by

the RGB Mixer in the BW node.


**Lesson 5 Mastering Node Trees** **185**


**What If You Made Both Adjustments in One Node?**

The order in which the RGB signal is impacted by the tools in the color page is

determined by a predefined order of operations:


In the preceding example, the image would first be impacted by the sepia Lift/

Gamma/Gain operation followed by the monochrome Channel Mix, resulting in the

same elevated black-and-white image you saw at the end of the exercise.


If you were to memorize this pipeline, you could technically perform multiple

operations within a single node with a clear idea of how the tools affect one

another. However, this approach could lead to needlessly slow and complex

grading workflows. Having separate nodes for every stage of the grade helps keep

the workflow light, intuitive, and consistent.


**Lesson 5 Mastering Node Trees** **186**


##### **Visualizing Node Processing**

While it’s good to see how grading tools operate in practice, using DaVinci Resolve’s

generators can sometimes help develop a clearer understanding of tool mapping and

node processing. In this exercise, you will analyze hue selection with the help of color bars.

**1** Enter the edit page.

**2** Open the Effects Library.

**3** Within the Toolbox > Generators, locate the EBU Color Bar.


**4** Drag the EBU Color Bar generator to the end of the timeline.


To work on a generator in the color page, you must first transform it into a compound

clip so that it can take on video properties.


**Lesson 5 Mastering Node Trees** **187**


**5** In the timeline, right-click the generator and choose New Compound Clip.

**6** Name the compound clip **Color Bars** .

**7** Enter the color page.

**8** In the Curves palette, change the mode to Hue Vs Hue.


The color bars are represented by distinct spikes in the curves histogram.

**9** Click the yellow bar in the viewer to drop a control point and two anchors in the

Curves palette.

**10** In the lower right of the palette, drag the Hue Rotate parameter to turn the bar in the

viewer green.


You will also adjust the luminance to get a better match on the other green bar in

the generator.

**11** In the Curves palette, change the mode to Hue Vs Lum.


**Lesson 5 Mastering Node Trees** **188**


**12** Click the newly green (previously yellow) bar in the viewer.


Despite the bar appearing green in the viewer, the control points still land on the

yellow vector of the HSL curves. This is because a corrector node will continuously

process the incoming signal, no matter how many changes you make. Disabling a node

(Command-D on macOS or Ctrl-D on Windows) is a good way to evaluate the state of

the image you are actively working on.

**13** In the lower right of the palette, drag down the Lum Gain parameter until the bar

matches the other green bar in the generator.

**14** Create a new node.

**15** In the Curves palette, change the mode to Hue Vs Hue. Notice that there is no longer a

spike on the yellow vector.


**Lesson 5 Mastering Node Trees** **189**


**16** In the viewer, click either of the green bars.

**17** Drag Hue Rotate to turn both bars in the viewer pink.


The second corrector node is now processing the video signal as it appears after its

node 01 adjustment, meaning that both bars are registered and treated as green.

**18** Disable node 01.


The pink hue correction in node 02 no longer affects the yellow bar.


Understanding this behavior is fundamental when working with nodes. When you alter the

brightness, color, or contrast of your image, it will impact how downstream nodes process

and interact with the video signal. This has huge implications for keying, too—the qualifier

will respond differently to an image based on the accuracy and vibrancy of the colors in the

signal it receives.


NOTE When designated in the Project Settings, the qualifier becomes a “color

space aware” tool. That means that in a color-managed project, its behavior will be

mapped to the tonal range of the incoming video signal to produce high-quality

keys. Functionally, this means that log footage is treated more like Rec.709 and

does not require additional processing prior to keying.


**Lesson 5 Mastering Node Trees** **190**


##### **Adjusting Contrast and Luminance on Nodes**

With a clearer understanding of the function of RGB inputs and outputs, you can now

check how adjustments to luminance and contrast can impact node tree signal quality.

**1** Return to clip 13 and press Command-Home (macOS) or Ctrl-Home (Windows) to reset

the grade.

**2** Label the first node **Crush** .

**3** In the Primaries palette, drag the Lift master wheel to the left until it reaches -0.20.


The clip loses a great amount of detail in the shadows, and the bottom of the

waveform trace appears crushed along the floor of the scopes graph.

**4** Create a new node and label it **Restore** .


You will first attempt to restore the shadow data using the Curves palette.

**5** Open the Curves palette and ensure that the YRGB channels are linked.


You can use the palette itself to read how the tool interprets the incoming signal.

**6** Click node 01 (Crush) and review the Curves palette histogram trace.

**7** Click node 02 (Restore) to compare the histogram trace in the same graph.


01 Crush node RGB input histogram 02 Restore node RGB input histogram


**Lesson 5 Mastering Node Trees** **191**


The histogram changes to show the state of the video signal entering the selected

node. This can be useful for determining where to click in the curves graph to target

specific luminance and chromaticity ranges. The histogram readout in node 02

signifies that most of the data is crushed against the lower left of the graph.


TIP You can set the Curves palette histogram to react to your node

adjustments as you make them. To do so, open the Curves palette options

menu in the upper right of the palette and choose Histograms > Output.

The histogram now represents the outgoing RGB signal of the node instead

of the input.

This is a useful feature if you need to consistently reach certain targets while

grading (such as when matching clips), but it is also a processor-intensive

setting, and the histogram will no longer represent the active video signal as

soon as you make your first change.


**8** Drag the black point of the YRGB curve upward along the left side of the curves graph.

Stop dragging when you are halfway between the second and third horizontal lines

from the bottom.


**Lesson 5 Mastering Node Trees** **192**


Although the waveform distribution appears similar to the original, ungraded signal, the

resulting image appears distorted. The shadows appear lifted and flat, and the skin

tones patchy and oversaturated. This demonstrates a “destructive” workflow in which

the changes made in one node restrict the RGB data available to subsequent nodes.


NOTE The Curves palette black point is functionally identical to the Color

Wheels’ Lift. However, when you enabled color management in this project,

you kept the default “Use color space aware grading tools” parameter, which

modifies the behavior of certain palettes based on the tonal range of the

incoming signal. This means that the Color Wheels and Curves palettes have

unique interpretations of and impact on image luminance. Disabling “color

space aware” in the Project Settings would result in the Curves black point

behaving like the Lift again, meaning you could restore the video signal to its

original configuration using the Curves palette.


Regardless, it is generally a good idea to keep “color space aware” enabled, as

it allows for better keying with the qualifier and a more tailored approach

when grading high dynamic range media with the Curves palette.


Thankfully, you cannot truly destroy RGB pixel data in the pipeline. By using a tool with

the same tonal mapping as the original adjustment, you can restore the shadows of

the image.

**9** Right-click node 02 and choose Reset Node Grade.

**10** Drag the Lift master wheel right to restore data.


The tonal range mapping is identical in nodes 01 and 02, so this correctly restores the

video. The Lift values of the two nodes are different since you will have impacted

different ratios of the overall luminance.


Although you were ultimately able to restore the image in this instance, you can imagine

how subtler changes to the brightness and contrast of an image in upstream nodes can

impact the quality of adjustments made to the shadows and highlights in downstream

nodes. Most palettes and adjustment tools have different tonal distributions across the

video signal, and a change made in one cannot easily be undone in another.


It’s important to keep in mind this potential for destructive grades. As a rule, balancing,

matching, and secondary grades should come before bold contrast adjustments and

dynamic creative grades. It is far more acceptable to distort and crush data in the final

nodes because no other nodes rely on them for RGB info.


**Lesson 5 Mastering Node Trees** **193**


##### **Impact of Dominant Color Grades** **on Surrounding Nodes**

Another consideration when grading is choosing the order in which to apply color changes

to an image. In this exercise, you will try to create a clip with a distinct blue cast while

retaining control over the subjects’ skin tones.

**1** Reset the grade on clip 13.


**Lesson 5 Mastering Node Trees** **194**


**2** To save time, a Balance node for this clip has already been created. Open the gallery

and click the Still Albums icon to reveal a side panel with a list of available albums.


**3** Open the Base grades album.

**4** Right-click the **1.13.1 Balance** still and choose Apply Grade.

**5** Create a new serial node called **Blue look** (node 02).

**6** In the Primaries palette, drag the Gain and Gamma wheels toward blue and cyan,

respectively, to cool down the image.

**7** Use the Contrast and Pivot parameters to deepen the shadows and create more

pronounced detail in the image.

**8** Finally, reduce Saturation to 30 to lessen the blue vibrancy and end up with a cold,

desaturated look.


This look has a strong, purposeful design. It effectively conveys a somber mood or

suggests a different point in time in a nonlinear narrative. However, its impact on

the performers’ skin tones reduces its effectiveness and could end up tiring the

viewer’s eyes.


**Lesson 5 Mastering Node Trees** **195**


For a more dynamic look, you will aim to create _color separation_ between the

performers and the overall scene hue. Color separation occurs when the vectorscope

trace lands in two separate (usually opposite) vector quadrants for great visual impact

and appeal. This can be achieved with set design, lighting, and primary and/or

secondary grading.

**9** Create a new serial node called **Skin** (node 03).


The performers’ faces are awash in blue, so using HSL curves might not be the most

effective choice for secondary grading. A qualifier selection would give you a better

chance of isolating the skin in this shot.

**10** Open the Qualifier palette and drag across the lead performer’s face to grab a

sample range.


Due to the RGB signal passing through the Blue look node, the qualifier is forced to

work with overbearingly cool and desaturated values. This is not an ideal point in the

node tree for keying or grading skin.

**11** Select the Skin node and press E to extract it from the node tree.

**12** Drag it onto the connection line between nodes 01 (Balance) and 02 (Blue look).


**Lesson 5 Mastering Node Trees** **196**


**13** Reset the qualifier on the Skin node and drag to select the skin again. In the Qualifier

palette, adjust the HSL and Matte Finesse controls to get the best extraction.

Remember to turn on the Highlight mode in the viewer to best observe the result of

the selection.


This time, the qualifier produces a much cleaner result.

**14** In the viewer, turn off the Highlight mode.

**15** In the adjustment controls, raise the Sat value of node 02 (Skin) to 60 and drag the

Offset wheel slightly toward orange.


**Lesson 5 Mastering Node Trees** **197**


The resulting grade is much more appealing. You were able to produce a clean key for

the skin tone and adjust it to act as chromatic contrast to the blue grade. However,

because Blue look is the final node to impact the image before the node tree output,

you know that the original skin tone hues and luminance will always be tinted blue no

matter how much you grade the Skin node.


This exercise demonstrates how you might determine the placement of nodes based on

your RGB needs. For example, when using a qualifier, you almost always want to process

the ungraded or balanced version of the image, free of any dominant color or

contrast impact.


In the next exercise, you will learn how to further finesse the placement of nodes and

improve the clarity of the resulting RGB signal with the help of mixer nodes.
## **Creating Separate Processing** **Branches with a Parallel** **Mixer Node**


Mixer nodes allow you to combine multiple nodes into a single RGB output. The two mixer

node types, parallel and layer, have identical structures but process the incoming node

data differently.


The parallel mixer combines grades by blending them to an equal degree. The result

appears similar to when working on a linear node tree, with the difference being that

corrector nodes can extract RGB data from the same point in the node tree, optimizing

input signal quality.

**1** Continue to work on clip 13.


Before making major changes to your grade, save it as a still in the gallery.

**2** Right-click the viewer and choose Grab Still.


Next, you will place the Blue look and Skin nodes parallel to each other for optimal

routing of the RGB signal.


**Lesson 5 Mastering Node Trees** **198**


**3** Right-click node 03 (Blue look) and choose Add Node > Add Parallel or press Option-P

(macOS) or Alt-P (Windows) to add a parallel mixer node.


A new corrector node (node 05) is created, as well as a parallel mixer node that

combines the RGB outputs of the two upstream nodes.

**4** To reuse the qualifier skin tone selection, select node 02 (Skin) and press Command-C

(macOS) or Ctrl-C (Windows) to copy the node data.

**5** Select node 05 and press Command-V (macOS) or Ctrl-V (Windows) to paste the Skin

node data.

**6** With the qualifier copied, you can delete the old node 02 (Skin) by selecting it and

pressing the Delete or Backspace key.


You now have a node structure in which both the Blue look and Skin nodes use the

same RGB data from the optimal Balance node. Their respective grades are combined

in the parallel mixer node, which sends a single RGB signal to the node tree output.


**7** In the gallery, hover over the still you grabbed. If you have Live Preview enabled in the

gallery options, you should see the still grade projected onto the active clip in

the viewer.


TIP To enable, disable or change Live Preview behavior in the gallery, click the

options menu (…) in the upper right corner. Select Live Preview to enable it, or

move your mouse pointer over Hover Scrub Preview to choose if the image will

scrub in the Thumbnail and Viewer, Thumbnail only, or neither.


**Lesson 5 Mastering Node Trees** **199**


In the viewer, you should notice a subtle change in skin saturation. This is because the

Skin node is now impacting the neutral colors of the Balance node rather than

countering the blue hues of the Blue look node, resulting in greater color fidelity.


**Skin tone adjustment using linear nodes (left) and mixer nodes (right)**


**8** Select the Skin node and reduce the saturation to 55.00 for a more natural look.


The parallel mixer is perfect for organic and natural-looking adjustments, such as when

performing skin tone correction or when subtly pushing colors into a scene based on a

tonal range (i.e., creating warm shadows or magenta highlights).

##### **Morphing Mixer Nodes**


An alternative to the parallel mixer is the layer mixer. Over the next few exercises, you

will explore the differences between the two in more detail. Meanwhile, you will morph

the current clip’s parallel mixer into a layer mixer node to see the impact it will have on

the image.

**1** Continue to work on clip 13.


**Lesson 5 Mastering Node Trees** **200**


**2** In the Node Editor, right-click the parallel mixer node and choose “Morph into Layer

Mixer Node.”


This change has a jarring effect on the image. The skin tones appear far less realistic,

and the edge around the face keys is harsh and solid. This is because node 03 (Skin) is

now treated as an RGB image layer. The keyed faces have 100% opacity and are

overlaid onto the node 02 (Blue look) image underneath.


In its current state, the grade is unusable. However, by adjusting the opacity of the

Skin layer, you can still blend it into the Blue look.

**3** Select node 03 (Skin).

**4** In the central palettes, open the Key palette.

**5** Enter the Key Output Gain as **0.300** to reduce the opacity of the skin tone node.


The faces now blend much more naturally into the blue background. However, the

result is not identical to that of the parallel mixer version. If you were to compare the

two grades, you would see less contrast in the layer mixer composite, as evidenced by

the lighter shadows on everyone’s faces. This is neither good nor bad; it merely

demonstrates that the two mixers have different methods of combining node signals.


Now that you have seen how the two mixers affect the same image, let’s take a closer look

at how they operate.


**Lesson 5 Mastering Node Trees** **201**


##### **Visualizing Mixer Nodes**

You will create a basic RGB graphic setup that will clearly demonstrate the operation of

both mixer nodes. Understanding their behavior will help you determine when to choose

one mixer over another.


First, you will need a plain grayscale background.

**1** Enter the edit page.

**2** Open the Effects Library, and inside Toolbox > Generators, find the Grey Scale

generator.

**3** Drag the Grey Scale generator to the end of the timeline.

**4** Right-click the generator and choose New Compound Clip. Name it **Grey Scale** .

**5** Enter the color page.


To help with visualization, you’ll bypass the project color management on this clip to

operate in the generator’s native Rec.709 color space.

**6** Right-click the Grey Scale clip in the timeline (clip 48) and choose Bypass Color

Management.

**7** Create a new serial node (02).

**8** Right-click node 02 and choose Add Node > Add Layer or press Option-L (macOS)

or Alt-L (Windows) to add a layer mixer node.

**9** With node 02 still selected, create another layer node to produce a stack of three

layer nodes.

**10** Label the nodes (from top to bottom) **Red**, **Green**, and **Blue** .


**Lesson 5 Mastering Node Trees** **202**


Leaving a blank node before the layer stack makes it easier to add upstream

(“serial before”) nodes and navigate the node tree when needed.

**11** Select the Blue node at the bottom of the stack.

**12** Open the Window palette and create a circular window.

**13** Open the Custom Curves palette and isolate the blue channel.

**14** Drag the lower left control point (black point) to the top of the graph to turn the

circle blue.


**15** Move the circle window to the lower right of the viewer. Your goal is to create three

intersecting circles (red, green, and blue).


**16** Select the Green node and create a circle window in it.

**17** In the Curves palette, make the circle green by dragging up the green channel’s

black point.

**18** Move the Green node window to the lower left of the viewer.

**19** Finally, repeat these actions to create a red circle in the Red node.


**Lesson 5 Mastering Node Trees** **203**


The result demonstrates how nodes interact when combined in a layer mixer node.

Their behaviors are reminiscent of layer-based systems in which the uppermost RGB

input of the layer mixer constitutes the lowest layer and is compounded by each

subsequent RGB input. By default, the nodes are at full opacity until a Power Window,

qualifier, or other secondary tool introduces transparency.

**20** Right-click the layer mixer node, navigate to the Composite Mode submenu, and hold

Option (macOS) or Alt (Windows) while hovering over the list of blending options.


Doing so allows you to preview how the nodes interact under the different hue and

luminance blending methods. Note that all the top nodes are blended into the bottom

layer (Red), which remains at full opacity.

**21** Select Lighten to apply the composite mode.


**22** To remove the color blending, return to the Composite Mode submenu and

choose Normal.


NOTE Standard corrector nodes also feature blend modes in their

contextual menu. In their case, the RGB output of the video signal is

blended with the RGB input.


Next, you’ll change the order of the node layers.

**23** Move your mouse pointer over the connection line between the Red node and the

layer mixer until you see a blue highlight. Drag the connection to the bottom input of

the layer mixer to change the Red node order and disconnect the Blue node from the

layer mixer.


**Lesson 5 Mastering Node Trees** **204**


**24** Drag the RGB output of the Blue node to the top input of the layer mixer.


The red circle now overlaps the green and blue. This further demonstrates how the

RGB input order in the mixer node works. Additionally, it emphasizes that the physical

location of the nodes within the Node Editor has no impact on the grade or the results

in the viewer.

**25** To compare the interaction of the color circles in the parallel mixer, right-click the layer

mixer node and choose “Morph into Parallel Node.”


This operation changes the behavior of the three circles. Instead of displaying the

layers at full opacity, it blends them equally into one another.


The composite modes in the corrector and layer mixer nodes can help produce dynamic

looks. You can use them to emphasize certain areas of a scene, imitate lighting effects and

natural shadows, or even composite graphic design elements.
## **Compositing Color Effects** **with the Layer Mixer Node**


In this exercise, you will use a layer mixer to construct an image that has several secondary

grading needs. Unlike the previous example with the blue look, the focus is not on

seamlessly blending the colors of the image into each other but to work on each distinct

element separately.


**Lesson 5 Mastering Node Trees** **205**


**1** Select clip 03 in the 01_TooMuchLife_Trailer timeline.

**2** In the viewer, drag the playhead to the last frame of the clip, where you can clearly see

the jacket, desk, and background.


The client for this project requested that the jacket in this sequence be emphasized

to communicate the protagonist’s motivations to the audience. The editor applied a

preliminary grade to the clip to visualize what that might look like and included it in the

reference video.

**3** To bring up the reference video in the color page, go to the viewer options in the upper

right corner and choose Reference Wipe mode > Offline. Doing so will set the Image Wipe

mode to use the reference clip associated with the timeline instead of the gallery stills.

**4** In the upper left corner of the viewer, click the Image Wipe icon to compare the current

clip to the one in the reference video.


**Lesson 5 Mastering Node Trees** **206**


As you can see, the client’s vision is to enhance the red elements, especially the jacket

on the chair, to stand out against the clutter in the shot. There are several ways to

approach this secondary grade. You could use HSL curves or the qualifier together

with the RGB mixer, color wheels, or custom curves. When confronted with a specific

grade challenge, it’s common to cycle through several options until you find the

optimal grading solution. In this instance, you will use a combination of techniques,

including primary grading tools, layer mixer nodes, and the 3D qualifier.

**5** With the review complete, disable Image Wipe.

**6** Leave the first node (01) empty for easier node tree management.

**7** Create a second node and label it **BG** . You will use this node to set the overall look

of the room.

**8** For now, set the saturation of this node to 0 to more easily review your keying in the

other nodes. You will return to this node toward the end of the process.


**9** Press Option-L (macOS) or Alt-L (Windows) to add a layer mixer and a new node

(node 04). Label the new node **Jacket** .

**10** Open the Qualifier palette and, in the upper right corner, change the mode from

HSL to 3D.


**Lesson 5 Mastering Node Trees** **207**


Whereas the other qualifier modes are linear, the 3D qualifier features a radial

distribution of the color vectors, making it optimal for complex color selections. It was

originally designed for chroma key work because of its ability to intuitively include hue

and shadow fluctuations commonly found on green screens. It even features a Despill

slider for removing chroma spill from performers.

**11** In the viewer, drag the qualifier across the red section of the coat, ensuring that you

include both highlights and shadows in the stroke.


**12** Enable Highlight mode in the viewer and change it to B/W mode to review the initial

selection.


To get a more accurate result, you will add more strokes to build a reliable color

reference.

**13** Select Picker Subtract in the Qualifier palette.


**Lesson 5 Mastering Node Trees** **208**


**14** Drag in the viewer to remove the qualifier selection from the wooden paneling

behind the desk.


Before


After


**Lesson 5 Mastering Node Trees** **209**


Every time you create a stroke (additive or subtractive), a swatch is added to the 3D

qualifier stroke list to document the hues that are sampled for the key.


Depending on the image, sometimes a selection can be improved when made in an

alternative color model. Color models refer to the different methods used to

geometrically map and represent colors in digital environments, with the most

significant distinction usually being in how they approach image luminance. The four

models available in the 3D Qualifier palette are YUV, HSL, HSP, and LAB.


There are no strict rules for when you should use one model over another. Generally,

the default YUV produces optimal results, but in this case, you need a model that can

better differentiate between the desaturated red of the wood and the bright red of

the jacket.

**15** Set Color Space to LAB.


The 3D Qualifier modes to the right of the Color Space parameter determine the

tolerance of your hue selection. The default, Flat, will result in a 100% selection of the

hue, allowing for minor variations in color. To the left, Soft will result in a softer key that

accounts for greater variation in color, and to the right, Tight will only select the colors

you click. Luma features the same tolerance level as Tight but ignores chroma data,

making it ideal for white-only selections, such as when working with overexposure.

**16** Leave the 3D Qualifier mode on the default Flat.


Underneath, you will see the Color Space box that represents your 3D hue selection,

surrounded by the Chroma and Luma Adjustments fields. Use these parameters to

control the chroma tolerance and softness of the selection, manually move the

selected sample within the Color Space box (X, Y, Angle), and adjust the selection

based on hue luminance (Low, High, Low Soft, High Soft). When enabled, Adaptive

Chroma Softness ensures that the selection is consistent regardless of saturation.

**17** Drag the High parameter up (100.00) to increase the selection in the bright sections of

the image. The white matte becomes more pronounced on the bright red letter “S” and

the flowers on the wall.


To ensure a clean key throughout, scrub the playhead to review the selection in

the viewer.


**Lesson 5 Mastering Node Trees** **210**


**18** Drag the playhead to the first frame and use the Picker Add and Picker Subtract tools

to further clean up the matte. Ensure that you remove the selection of the chair and

desk to the right of the jacket.

**19** When finished, adjust the Matte Finesse controls to cover up any remaining

unselected areas.


A few rough edges are not a big issue when it comes to moving objects (such as the

jacket at the start), but the final frame of the composition should look clean.

**20** In the viewer, disable the Highlight mode.

**21** In the Qualifier palette, deselect Show Paths to hide the selection lines.


You have successfully extracted the red objects in the scene.


**Lesson 5 Mastering Node Trees** **211**


**22** Return to node 02 (BG), raise the saturation (35.00), and cool the Temp (-100.00) in the

Primaries palette.


Rather than going with a direct interpretation of the reference movie grade, which is

stylistically inconsistent with the remainder of the project, you’ll instead focus on

getting the red elements to pop while toning down the background hues.

**23** Click node 04 (Jacket), raise the saturation (55.00), and lower the gamma (-0.02) for

denser red hues.

##### **Reusing and Refining Keys Between Nodes**


In this clip, the greatest emphasis is meant to be on the jacket. You have successfully

isolated the red objects in the scene, but the background elements still draw too much

attention. You will create a new layer and use Power Windows to refine which objects are

emphasized and which are flattened.


First, you will remove the pink ticket on the right side of the desk from the original selection.

**1** Drag the playhead to the last frame of clip 03.

**2** Select the Jacket node.

**3** Open the Window palette and create a circular window. Label it **Pink ticket** .

**4** In the viewer, resize the circle to the pink ticket on the right side of the screen.


**5** Toggle the Highlight mode on and off to ensure that your window selection affects the

whole ticket and no other red elements.


**Lesson 5 Mastering Node Trees** **212**


**6** In the Window palette, click the Invert icon to remove the pink ticket selection from the

Jacket node key.


This clip has too much foreground interference to allow for a clean track. You will

manually animate the window to follow the camera motion.

**7** Open the Tracker palette and switch the mode to Frame.

**8** Click the diamond shape in the center of the keyframe navigation controls in the upper

right corner of the Tracker graph.


Doing so places a keyframe in the current position of the circle window.

**9** Drag the playhead to the start of the clip and reposition the circle window to the

estimated position of the ticket outside the viewer frame.

**10** Scrub through the clip timeline to ensure that the window is following the ticket’s

motion with the camera.


You have removed the red saturation adjustment from the ticket. Next, you will use a

separate layer node to reduce the intensity of the red background elements

above the desk.

**11** Press Option-L (macOS) or Alt-L (Windows) to create a new layer node, and

label it **Reds** .


**Lesson 5 Mastering Node Trees** **213**


**12** To reuse the matte data of the keyed Jacket node, drag the key output square of the

Jacket node toward the key input triangle of the Reds node.


**13** Drag the playhead to the last frame of clip 03.

**14** In the Window palette, create a gradient window and label it **Upper reds** .

**15** Position the gradient so that it separates the top half of the screen from the

jacket below.


**16** Reduce the saturation (35.00) and lower the gamma (-0.03) for less pronounced colors

compared to the jacket.


The jacket’s position changes between the start of the shot and the end. You will use

the same custom tracker method to animate the gradient.

**17** Open the Tracker palette, set it to Frame mode, and create a keyframe at the end

of the clip.


**Lesson 5 Mastering Node Trees** **214**


**18** Scrub through the clip and change the gradient position and rotation until the

secondary grade is undetectable in the viewer.


Next, to simplify your node tree and prepare it for new grading nodes, you can

combine all the layer mixer nodes into a single compound node.

**19** Drag in the Node Editor to select all the nodes except node 01.


**20** Right-click any selected node and choose Create Compound Node.


This is an effective organizational tool when working on clips with large node trees.

You can quickly disable a compound node to bypass all the color composites within it

without having to make complex selections or affecting other nodes in the tree.


And you still have access to the original layer mixer structure within the compound node.


**21** Double-click the compound node, or right-click and choose Show Compound Node.


The nodes appear just as they did before you turned them into a compound node.


**Lesson 5 Mastering Node Trees** **215**


**22** To navigate back to the main Node Editor, double-click Project 02 – Too Much Life

Trailer in the breadcrumb navigation path at the bottom of the panel.


**23** If you want to bring back the original node structure of the compound node to the

main Node Editor, right-click it and choose Decompose Compound Node.


TIP Another method for decluttering the Node Editor is to hide node

thumbnails. In the upper right corner of the Node Editor, click the options

menu (…) and deselect Show Thumbnails. Doing so will collapse the nodes to

just their labels, numbers, and palette icons.

## **Using External Mattes**


In previous lessons, you saw that the keys generated by secondary grading tools can also

be expressed as black-and-white mattes, as seen in the Highlight B/W mode of the viewer.

Keying relies fundamentally on this graphic dynamic, meaning that any image or video that

is black and white (or grayscale) can technically be treated as a matte. This includes

externally generated media that is imported purely for compositing or secondary

grading purposes.


In this exercise, you will use a premade matte to refine the look of a tricky-to
select element.

**1** Select clip 35 in the 01_TooMuchLife_Trailer timeline.


This VFX shot features composited rainbows in the background. For optimal results,

you’ll want to use dedicated mattes to control the intensity of the rainbows in the

scene. Thankfully, the compositing artist has shared the rainbow mattes with you so

that you do not have to spend time making this selection yourself.

**2** Enter the media page.

**3** In the Media Storage panel, find the BMD 20 CC – Project 02 folder and navigate to

Other > Mattes.


**Lesson 5 Mastering Node Trees** **216**


**4** Drag **Rainbow_matte.png** into the 05 VFX > 05.01 Mattes bin of the media pool.


This black-and-white matte was generated in an sRGB graphic environment, meaning

that it will perform optimally when mapped from sRGB rather than the default project

color space.

**5** Right-click **Rainbow_matte.png** and choose Input Color Space > sRGB > sRGB.

**6** Enter the color page.

**7** Increase the contrast (1.200) in clip 35 for easier viewing. Label the node **Contrast** .

**8** Right-click and choose Add Node > Add Serial Before, or press Shift-S. Label the new

node **Rainbows** .

**9** Click the Media Pool button in the interface toolbar at the top of the color page.

**10** From the 05.01 Mattes bin, drag **Rainbow_matte.png** into the Node Editor.


The matte PNG appears in a dedicated external matte node in the Node Editor. Notice

that the node has no inputs and contains multiple outputs.


The uppermost blue square is the standard luminance, or alpha output. The three blue

squares under it are RGB outputs that enable you to work with each channel

independently. The green square at the bottom outputs a standard RGB signal of the

black-and-white matte.

**11** Drag the uppermost key output to the Rainbows node’s key input.


The key is imposed in the Rainbows node thumbnail.

**12** Select the Rainbows node and raise the saturation (75.00) to create more

prominent rainbows.


**Lesson 5 Mastering Node Trees** **217**


When working on projects that feature a lot of CGI and 2D composting, it is standard for

colorists to receive such matte assets from post houses since these mattes are generally

more easily available to the people behind the VFX. Alternatively, in cases where complex

grading is required, some colorists use dedicated rotoscope artists or assistant colorists

who will exclusively create mates while the lead colorist focuses on grading.

##### **Working with Image Sequence Mattes**


It is also possible to work with animated keyed elements, known as _traveling mattes_ . In this

shot, a person in the background is disrupting the emotional scene playing out on the

beach. You will use a pre-generated traveling matte to remove them.


NOTE The following exercise requires DaVinci Resolve Studio to complete.


**1** Enter the media page.

**2** In the Media Storage panel, navigate to Other > Mattes > Beach_coverup.


Traveling mattes are usually exported as a series of still images. You have the option of

changing how DaVinci Resolve interprets images with sequential naming. This is

because, depending on your workflow, you will sometimes want these images to be

compiled into a moving sequence (such as in the case of this matte), and sometimes

you will want to keep the images individual (such as when working on a project with

image assets labeled pic_1, pic_2, pic_3, etc.).


**Lesson 5 Mastering Node Trees** **218**


**3** From the options menu (…), choose Frame Display Mode > Sequence.


**4** Drag the **Beach_coverup.png** image sequence into the 05 VFX > 05.01 Mattes bin of

the media pool.

**5** Right-click **Beach_coverup.png** and choose Input Color Space > sRGB > sRGB.

**6** Enter the color page.

**7** Create a new node after Rainbows and label it **Coverup** .

**8** Open the Effects panel.

**9** Under Resolve FX Revival, find the Object Removal effect and drag it onto the

Coverup node.


Object Removal analyzes the content of a moving shot to build a clean backplate of an

environment. It can then use key data to paint out specific objects from a scene.

Ordinarily, you would use a Power Window to select and track the object you wish to

remove. In this case, you can connect the external matte to provide the key data.

**10** From the 05.01 Mattes bin, drag **Beach_coverup.png** into the Node Editor.

**11** Drag the uppermost key output to the Coverup node’s top key input.

**12** In the Object Removal settings, select Show Mask Overlay.


This will allow you to preview what the external matte looks like and verify that it suits

the content of the shot.


**Lesson 5 Mastering Node Trees** **219**


**13** Zoom in to the viewer to review the external matte overlay. Scrub the playhead to

check the timing.


It’s close, but something appears off. In the last few frames, the matte appears to jump

to a different position in the viewer. Depending on the timecode and duration of the

clip and its associated matte, their playback may not sync. You can offset the matte’s

playback in the Key palette.

**14** Open the Key palette.

**15** Select the beach coverup matte node in the Node Editor. The Key palette’s mode in the

top right corner switches to External Matte.


The beach coverup matte was created specifically for the movement of the person on

the beach. That means you need to sync the start time of the matte to the video clip.


**Lesson 5 Mastering Node Trees** **220**


**16** Click the Loop parameter checkbox to disable looping.


Clip 35 has 12-frame trims, meaning there is additional footage on either side of its In

and Out points. The matte is lining itself up to the first frame of the source clip, which

results in it being 12 frames too early for the edit.

**17** Enter the Offset value as **-12** .


With the matte sync’d to the video, you can proceed with the object removal.

**18** Select the Coverup node to bring back the Object Removal settings in the

Effects panel.

**19** Turn off Show Mask Overlay.

**20** Click Scene Analysis.


The effect will use the DaVinci Neural Engine to interpret the content of the shot and

gain the necessary data to reconstruct a clean background. When complete, the

walking person will temporarily be replaced with gray pixels.

**21** Select Assume No Motion. When working with a locked-off shot such as this one, this

setting will ensure less intensive processing and produce cleaner results.

**22** Click Build Clean Plate.


The person on the beach disappears.

**23** Scrub the playhead to review the coverup throughout the clip.


**24** If you see any artifacts in the viewer, increase the Search Range parameter.


**Lesson 5 Mastering Node Trees** **221**


The exercises in this lesson gave you an advanced overview of the potential of the Node

Editor. Although you’ve practiced a variety of workflows, there is ultimately no single

correct way to utilize nodes when grading. Continue to practice using nodes for more

complex grading, and you will soon arrive at your own preferred style. Above all, aim for

the dual goals of workflow efficiency and the preservation of image quality.
## **Self-Guided Exercises**


Complete the following exercises to test your understanding of the tools and workflows

covered in this lesson.


**Clips 01-02** —To create a cohesive opening sequence, transfer the node tree from clip 03

and refine the result. Make the outdoor clips warm.


**Clip 04** —Use a layer mixer to darken the red bag and saturate the blue shirt. Apply the

same warm look as clips 01 and 02.


**Clips 13-18** —Transfer clip 13’s blue look (with the parallel mixer) to the remainder of the

clips in this scene and ensure the contrast, colors and skin look consistent throughout.


**Clips 33-34** —Use a parallel mixer to create a look for these clips in the principal’s office.

Aim for a cold, clinical feel to convey the negative nature of the interaction between the

characters while keeping their skin tones natural.


When you’ve completed these lessons, you can import **01_TooMuchLife_Trailer_**

**COMPLETED.drt** to compare your work with the “solved” version of this timeline. If any

media appears offline, click the red Relink Media button in the upper left corner of the

media pool and specify the location of the Project 02 media on your workstation.


To ensure that the project management is set up correctly, right-click the imported

timeline and choose Timelines > Timeline Settings. Select Use Project Settings in the lower

left of the settings panel to link it to the project-wide color management settings.


**Lesson 5 Mastering Node Trees** **222**


## **Lesson Review**

**1** True or False? A corrector node can have multiple RGB inputs.

**2** What are the blue symbols on either side of a node?

**3** True or False? A node key can be connected to the input of a node that is in the same

parallel or layer node stack.

**4** In the Key palette, what does the Key Output Gain affect?

**5** How would you import an image sequence into the media pool as a single video file?


**Lesson 5 Mastering Node Trees** **223**


##### **Answers**

**1** False. A corrector node can have only a single RGB input, although it can have multiple

RGB (and key) outputs.

**2** The blue symbols represent the key input and key output.

**3** True. A node output (both RGB and key) can be connected to any downstream input, as

well as to other nodes in a mixer stack.

**4** Key Output Gain affects the opacity of a selected node.

**5** In the Media Storage panel, click Options > Frame Display Mode and select Sequence

to force an image sequence to display (and import) as a single video file.


**Lesson 5 Mastering Node Trees** **224**


### Lesson 6
# Managing Grades Across Clips and Timelines



Grading a film or video project requires

considerable attention to detail and

the use of a variety of tools throughout

both primary and secondary stages.

However, once a look is established,

a project often makes repeated use

of existing grades that propagate

throughout the timeline. An obvious

example is when you’re working on

multiple clips that came from the same

source file or clips used from different

takes of the same scene.


DaVinci Resolve 20 offers multiple

solutions for reproducing and refining

grades across clips. These include

a straightforward copy and paste,

extracting individual nodes for isolated

adjustments, and even migrating

grades across whole timelines. In this

lesson, you’ll examine the workflows

that will enable you to efficiently copy

and manage grades within a single

node, clip, timeline, and beyond.



Time

This lesson takes approximately
2.5 hours to complete.

Goals

Working with Versions 226

Appending Grades and Nodes 235

Saving Node Tree Templates 239

Saving Stills for Other Projects 246

Migrating Timeline Grades
Using ColorTrace 251

Copying Grades Using the
Timelines Album 256

Self-Guided Exercises 258

Lesson Review 259


## **Working with Versions**

Versions enable you to associate multiple grades with a single clip in a timeline. You can

use versions to preserve a grade at earlier stages of the grading process or when creating

look variants to share with a creative supervisor for review and approval. Each version

remains intact and can be recalled when needed. Versions are easily accessible in the

contextual menu of each clip and can be created, deleted, bypassed, and switched

between local and remote.


In this exercise, you will begin by creating a new grade on a clip, after which you’ll apply

preexisting grades from the gallery to quickly build a set of grade versions.

**1** In the 01_TooMuchLife_Trailer timeline, click clip 05.

**2** Drag the playhead to the start of the clip.


**3** The start of clip 05 is in mid-dissolve with clip 04. To disable transitions and effects on

the edit page timeline, click the Unmix button in the lower left corner of the viewer.


**Lesson 6 Managing Grades Across Clips and Timelines** **226**


**4** In the gallery, open the Base grades album and apply the **1.5.1 Balance** still to

balance clip 05.


TIP If you have a three-button mouse, you can click the middle button (scroll

wheel) to quickly apply grades from stills.


**5** Create a second node and label it **Split tone** .

**6** Open the Curves palette. To create a split-tone look, you can push opposing

complementary colors into the image highlights and shadows. This tends to

result in a retro film look.

**7** Click the YRGB link to ungang the channels.

**8** Isolate the blue channel and drag the black point up to turn the shadows blue.

Then, drag the white point down to turn the highlights yellow.

**9** Isolate the red channel, create a new control point in the lower midtones, and drag

upward to add a slight red tint to the midtones.


**Lesson 6 Managing Grades Across Clips and Timelines** **227**


To address the vibrant blues in the shot, you’ll use the ColorSlice. This palette features

predefined, customizable vectors with which you can make adjustments that mimic the

photometric properties of film. Because of its blended mapping of the color ranges, it

tends to produce more seamless results compared to the Qualifier palette.


**10** Click the Highlight button next to the Blue vector header to review the hue range in

the viewer. If a vector fails to capture the exact hue range you wish to target, you can

use the Center slider to redefine the vector range in the RGB circle at the top. In this

case, the default selection is satisfactory.


At the bottom of each vector are two bar sliders. The left bar is the Density parameter,

which affects both the luminance and saturation of the hue. When raised, it produces

darker, more saturated colors, as commonly seen in film stock.

**11** Raise the Density (20.00).


The right bar is the Saturation parameter, which uses a subtractive color model to

affect midtones and shadows more than highlights. This prevents highly saturated

colors from becoming unnaturally bright.

**12** Lower the Saturation (0.75).

**13** Create a new serial node 03 and label it **Contrast** .

**14** In the Primaries palette, raise the midtone detail (25.00) to increase the contrast in the

midtones of the clip. This improves detail clarity, resulting in a sharper-looking image.

**15** Increase the Highlights parameter (25.00) to brighten the highlights on the

performers’ faces.


**Lesson 6 Managing Grades Across Clips and Timelines** **228**


TIP The Highlights and Shadows parameters in the adjustment controls feature

unique tonal ranges designed for better retrieval of detail from the highlights and

shadows of an image. To study their impact, go to the compounded grayscale

generator at the end of the timeline and drag these ranges to identify their range

and overlap.

##### **Creating New Local Versions**


You have now successfully created the first look for this shot. By default, every clip begins

as Local Version 1. You can rename clip versions to identify a specific look or purpose

of a grade.

**1** In the timeline, right-click clip 05, and under Local Versions, choose Version 1 > Rename.

**2** In the Version Name dialog, enter the name **Split tone** and click OK.


You will apply several grades to this clip, each of which will be designated as a new

version. To save time, you will use some preexisting grades in the Clip 05 grades

gallery album.

**3** Right-click clip 05 and choose Local Versions > Create New Version.


**4** Enter the name **Bleach bypass** .


**Lesson 6 Managing Grades Across Clips and Timelines** **229**


**5** Reset the split-tone grade by choosing Color > Reset > All Grades and Nodes or press

Command-Home (macOS) or Ctrl-Home (Windows).


This is a necessary step if you want to start with an ungraded clip every time you

design a new look. Otherwise, you can continue tweaking the image using the

previous grade’s settings.

**6** In the Clip 05 grades album, middle-click the **1.5.2 Bleach bypass** still to apply

the grade.


This look emulates another physical film practice in which filmmakers would skip (or

“bypass”) the final chemical (bleach) bath of the film development process, resulting in

a high contrast, low saturation look. Digitally, this look has been re-created with the

help of a layer mixer, an Overlay composite mode, and two separate nodes handling

color and contrast.

**7** To make another version, right-click clip 05 and choose Local Versions > Create New

Version. Enter the name **Sitcom** .


TIP You can also press Command-Y (macOS) or Ctrl-Y (Windows) to create a

new version in a clip.


You could reset the grade again, but because you are simply overwriting the current

grade with the still grade, that won’t be necessary.

**8** In the Clip 05 grades album, middle-click the **1.5.3 Sitcom** still to apply the grade.


This look is more suited for a light-hearted narrative, such as a comedy, romance, or

television sitcom. It prioritizes bright, cheerful colors and a warm overhead glow.


TIP Double-click repeatedly under a clip thumbnail to change the metadata

on display. You can opt to see the media codec, clip name, or version label

(local version 1 will always appear blank).


In the next exercise, you will create one final look using the Film Look Creator

Resolve effect.


**Lesson 6 Managing Grades Across Clips and Timelines** **230**


##### **Designing Grades with the Film Look Creator**

The Film Look Creator is a collection of tools that emulate the appearance of film stock.

When applied, it remaps the tonal distribution of the image to react photometrically to

properties such as exposure and balance. It also allows you to add elements associated

with physical film properties, such as halation, bloom, flickering, and gate weaving.


NOTE The following exercise requires DaVinci Resolve Studio to complete.


**1** Create a new local version called **Film loo** k creator.

**2** Delete all the nodes except node 01 (Balance).

**3** Create a new node 02 and label it **Film look** .

**4** In the Effects Library, under Resolve FX Film Emulation, drag Film Look Creator

onto node 02.


The clip’s appearance instantly shifts to reflect the new tonal processing and preset

film look. The contrast is more pronounced, and the colors appear denser.


At the top of the settings, you can use the Presets parameter to set a starting point for

your look. The Blend modes underneath determine the relative strength of the Color

(Color Settings and Split Tone categories) and Effects (every category after Split

Tone) controls.

**5** Leave the Presets set to Default 65mm.


Under Film Look, use Core Look to determine the treatment variant of the video signal

and how it is impacted by the tool’s parameters. Film Look Blend adjusts the strength

of this base look, and Skin Bias tweaks skin tones relative to the base hues.

**6** Leave the Core Look set to Cinematic.


**Lesson 6 Managing Grades Across Clips and Timelines** **231**


Use the Color Settings to affect the photometric properties of the footage. Notice that

dragging certain parameters, such as Exposure, feels more like changing the exposure

on a physical camera rather than a digital adjustment.

**7** Raise the Highlights (1.000) for a brighter sky in the background.

**8** Lower the White Balance (5500) to cool the scene. A unique property of this parameter,

when compared to the Temp setting in the Primaries palette, is that it mimics how

unbalanced cameras capture light and color. With a lower temperature, instead of the

image turning blue uniformly, the skin tones shift at a slower pace, meaning you still

see natural skin colors in a cool environment.

**9** Raise the Tint (20.0) to remove the green undertone.

**10** The Split Tone category allows you to quickly emulate the appearance of color-timed

film stock. As you have already made a curves-based split tone look, you can leave this

category unselected.

**11** Leave the default Vignette settings for a subtle, darkened frame.

Halation and Bloom refer to distinct lighting artifacts commonly found in film. _Halation_

presents as a soft, usually red, glow around very bright areas of the frame. _Bloom_

refers to the light spill that occurs when an image is projected, resulting in a slight

brightening of areas close to light regions.

**12** Leave the default Halation and Bloom settings for a subtle filmic effect.

**13** Under Grain, change the Preset to 35mm for more pronounced film grain. Lower

values will result in larger grain because when a smaller film stock is projected on a

large screen, small imperfections, like scratches and grain, are blown up more than

those on larger film stock.


Flicker, Gate Weave, and Film Gate refer to the physical properties of film projection.

_Flicker_ is caused by the rotating shutter, _Gate Weave_ is the horizontal and vertical shift

seen as the film is mechanically pulled through the camera’s gate, and _Film Gate_ refers

to the blanking of the edges as seen in various projection or telecine alignments.

**14** Leave the default Flicker, Gate Weave, and Film Gate settings for a gentle flicker and

shake of the frame.


TIP Select 3D LUT Compatible at the top of the settings to eliminate any

parameters that cannot be retained when generating a look-up table (LUT).

This will allow you to generate LUTs for monitoring and post-production

collaboration based on the looks you create in the Film Look Creator.


**Lesson 6 Managing Grades Across Clips and Timelines** **232**


Having created four distinct looks for this scene, you can now compare them in the

viewer using the split-screen display.

**15** In the upper left corner of the viewer, click the Split Screen button.

**16** In the dropdown menu below, make sure Version is selected.


The split-screen view is enabled, displaying all four grades in a grid.


Comparing the versions might be difficult now because they have been scaled down to

fit the small viewer window. You can resize the viewer for full-screen playback and

optimal viewing.

**17** Choose Workspace > Viewer Mode > Cinema Viewer or press Command-F (macOS) or

Ctrl-F (Windows).


**Lesson 6 Managing Grades Across Clips and Timelines** **233**


TIP To remove the white outline around the active version, go to the viewer

Options menu and choose Split Screen > Show Outline.


In the next few exercises, you will apply the split-tone look to other clips in the timeline.

**18** In the upper left corner of the split-screen view, double-click the “Split tone” version to

select it.

**19** Press Esc to exit the full-screen mode.

**20** Disable Split Screen in the viewer.


TIP Press Command-B or Command-N (macOS) or Ctrl-B or Ctrl-N (Windows) to

cycle through the versions of a clip in the viewer.


**Remote Versions**

In the contextual menu, under the Local Versions options, you might have noticed

a similar section for Remote Versions. This area offers another method of retaining

multiple grades in a clip.


Remote versions are different from local versions in two ways. First, when a grade

is remote, it affects all other timeline clips derived from the same source media.

Second, the grade appears on all subsequent uses of the source clip in all other

timelines of the active project (provided that the clips in those timelines are also

set to use remote versions).


One popular application for remote grading is when working with master

timelines. After importing the footage from a shoot, you can place all the media on

a remote timeline and apply preliminary grades to the clips. When you eventually

create a cut in the edit page or import the editor’s timeline, those remote grades

will automatically transfer to the new remote timeline, saving you time with the

grade. You can then use the clip timeline’s contextual menu to Copy Remote

Grades to Local and continue to grade locally without affecting the

master timeline.


In short, local grades are applied on a clip basis, whereas remote grades are

applied on a project basis.


**Lesson 6 Managing Grades Across Clips and Timelines** **234**


## **Appending Grades and Nodes**

Having created a look on the key shot of this sequence, you will now transfer the grade to

the clips that follow it. Most of the footage was captured at different locations and times of

day, so you will have to pay extra attention to keep the montage cohesive.


Previously, you applied still grades by choosing the Apply Grade contextual menu option or

by pressing the middle button of your mouse. Doing so overwrites the existing grade on a

clip and replaces it with the entire node tree of the copied grade. Sometimes, you will want

to add the node tree _after_ a clip has been matched or apply only parts of that node tree.


The following exercises show you how to be selective when copying grades.

**1** Select clip 06. You will apply the previously created split-tone look to this clip.


Clip 06 is unbalanced and has a slightly warm temperature. You could balance it, but

that would not necessarily optimize it for the split-tone grade. As you learned in Lesson

2, clips must be matched to share grade data accurately. Without matching, grading

tools will behave less predictably, and the differences between the clips will be

preserved even if the same creative grades are applied.


To save time, a match grade for this clip has already been created for you.

**2** Open the Base grades album and apply the **1.6.1 Match** still to the clip. To more closely

match clip 05, the clip has been darkened and cooled.

**3** Open the Clip 05 grades album.


A split-tone grade is already prepared in the gallery. If you directly apply the split-tone

still from the gallery, it will overwrite the Match node you just applied to the clip.

Instead, you will _append_ the split-tone grade to the current node tree.


**Lesson 6 Managing Grades Across Clips and Timelines** **235**


**4** Right-click the **1.5.1 Split tone** still and choose Append Node Graph.


TIP You can also drag a still from the gallery onto a connection line in the

node graph to append it to an existing grade.


The Clip 02 Match node is now followed by the Split tone node tree. However, the

grade still does not look entirely right—its shadows look more cyan compared to clip

05. By appending the grade, you added all the nodes from the original split-tone

grade, including the original Balance node that was created specifically for clip 05. This

Balance node is not necessary for clip 06 and should be deleted.

**5** Select node 02 (Balance) and press the Delete or Backspace key.


You now have a clean split-tone look that more closely resembles the one in clip 05. Next,

you’ll apply this same look to the upcoming clip but without the Balance or Contrast nodes.


TIP Window tracking data is reset when applying grades from stills in the gallery,

which allows you to run new tracks based on the unique content of each clip.

However, when _appending_ nodes, window tracking data is preserved.


**Lesson 6 Managing Grades Across Clips and Timelines** **236**


##### **Copying Individual Nodes**

So far, you’ve used all the grading data stored in the stills. You copied and appended an

entire node tree to the Node Editor and tweaked the nodes based on the clips’ needs.

However, you can also access and extract individual nodes from a still or timeline clip.

**1** Select clip 07.


This clip looks relatively neutral but has a distinct color and contrast compared to the

starting looks of clips 05 and 06. As in the previous exercise, you will apply a still to

prepare it for the split-tone look.

**2** Open the Base grades album and apply the **1.7.1 Match & Contrast** still to the clip.


Doing so creates a good base for the incoming grade. The Match node mimics the

temperature of the balanced clip 05, while the Contrast node addresses the tonal

distribution and detail for more consistent luminance.


You can now apply the split-tone grade. Because the clip is balanced and has the

correct contrast, you only need to transfer the Split tone node itself.


**Lesson 6 Managing Grades Across Clips and Timelines** **237**


**3** Open the Clip 05 grades album, right-click the **1.5.1 Split tone** still, and choose Display

Node Graph.


The node graph appears in a floating window displaying the node tree of the grade as

it appeared in the Node Editor when the still was generated. On the right side of the

window, you can choose to isolate and apply only the color or sizing adjustments

(PTZR: pan, tilt, zoom, rotation). Tabs at the top allow you to switch to a node-based

refinement of the parameters that will be included when copying node data.

**4** From the still’s node graph window, drag node 02 (Split tone) to the Node Editor of clip 07

and position it over the connection line between node 01 (Match) and node 02 (Contrast).


A + (plus sign) will appear over the line to signify that you can release the mouse

button and attach the Split tone node to the connection line.

**5** In the still’s node graph window, click Close.


The three clips in this sequence are now matched and carry the same split-tone look.


Having access to the node structure of every still allows for more precise copying workflows.

You can separate the primary balance and match nodes from the contrast and creative look

nodes and copy only what is necessary. As with all grading, you should continue to tweak

and refine the grades to ensure color consistency and maximum visual quality.


**Lesson 6 Managing Grades Across Clips and Timelines** **238**


**Shared Nodes**

In this exercise, you copied the same split-tone look across three clips while

retaining their individual balance and contrast adjustments. Should you decide to

tweak the creative look of the sequence, you might find the task of copying the

grade across the clips time-consuming. Shared nodes are a grading optimization

function that allows you to link and lock a single node across multiple clips.


To turn a standard corrector node into a shared node, right-click the node and

choose Save as Shared Node. Two blue arrows in the label indicate the node’s new

status, and a lock symbol in the lower right corner prevents unwanted changes

from being made to the grade. Label the shared nodes the same way you would

regular nodes. When you right-click and choose Add Node in the Node Editor of

any clip in the current project, you will now see the shared node at the bottom of

the node list.


This method allows you to quickly migrate grades between clips and even make

global tweaks by disabling Lock Node in the shared node’s contextual menu. Note

that because the Undo function is stacked per clip in the color page, changes to

shared nodes cannot be undone.

## **Saving Node Tree Templates**


So far, you have built node trees based on the individual needs of each clip. But realistically,

you will not want to create and label new nodes every single time you work on a new clip. It

is more efficient to build an ungraded (but labeled) node tree template to give you a quick

start when grading.


In this exercise, you will create a template still and use it to ripple grades across clips in

a sequence.

**1** Select clip 37.

**2** Build a node tree based on your preferred approach to color grading. Label the nodes,

but do not make adjustments in the color page palettes.


Node trees tend to be unique to each colorist. This book is designed to help you

understand the color page and its tools well enough to build your own grade

structures with confidence. Node trees tend to vary based on media type, project

genre, color management method, and so on. You will likely modify your preferred

node tree template throughout your entire professional career as you gain experience,

acquire more tools, and develop your own grading techniques.


**Lesson 6 Managing Grades Across Clips and Timelines** **239**


Generally, you will want to start with corrector nodes aimed at addressing luminance,

color balance, and saturation. You will then want to address the secondary needs using

various keying and selection tools and finish off with the look and photometric

“texture” of each shot.


A sample template can be found in the Templates album in the gallery. It follows the

broad rules of a grading workflow and, due to the prevalence of memory colors in the

film, features dedicated skin, sky, and grass parallel nodes.

**3** Once you have built your template, right-click in the viewer and choose Grab Still.

**4** In the gallery, label the still **TEMPLATE** .

**5** Select clips 36-45 (excluding the graphic clips 42 and 43) and apply the TEMPLATE still.


All the clips in the beach sequence will now have the same node tree.


Next, you will learn how to quickly transfer grade changes across clips.

**6** Return to clip 37.

**7** In the Node Editor, select the Look node (node 20, if working on the sample template).

**8** Open the RGB Mixer palette.

**9** Next to Red Output, select Auto Normalize.


**Lesson 6 Managing Grades Across Clips and Timelines** **240**


This setting forces the channels to maintain constant luminance as you mix their red,

green, and blue values.

**10** Drag up the red channel (1.5) of the Red Output.


Before


After


The red elements in the viewer become brighter, while the blues become denser and

more cyan.

**11** Select all the clips in the sequence (36-45), including the graphic ones.


**Lesson 6 Managing Grades Across Clips and Timelines** **241**


**12** In the Color menu, choose Ripple Node Changes to Selected Clips.


Every instance of the Look node across the sequence adopts the normalized RGB

Mixer adjustment. The graphics clips are unaffected, as they do not have a node with

that number in their ungraded node trees. This demonstrates that rippling is based on

node number, not node position.


Rippling works well in stable template node trees but can fall apart if you create a new

node mid-tree, which will cause all downstream nodes to be renumbered in an effort

to keep them sequential. A DaVinci Resolve setting allows you to preserve node

numbers when creating new nodes.

**13** In DaVinci Resolve > Preferences, navigate to the User controls and open the

Color settings.

**14** Under General Settings, check “Preserve node numbers when adding nodes.” Now,

when you add new nodes, the original node numbers will be maintained. With this

setting, rippling is more effective since new nodes will not throw off the numbering

convention upon which it relies.

**15** In the same Preferences section, next to “Switching clips,” choose “Selects same node.”

This will ensure that when you are performing a grading pass (like when balancing or

adjusting secondary selections), you will automatically land on the same node in

every clip.

**16** Click Save.

**17** In the node tree, select a secondary node (node 11 in the sample template).

**18** Use the Color Warper to reduce the saturation of the pink shirt and drag it left toward

a slightly warmer hue.

**19** Ripple the Color Warper change to all the clips that feature the pink shirt.


TIP You can assign a custom shortcut to the ripple commands in the

Keyboard Customization interface.


As with most secondary adjustments, you will need to make tweaks based on the

individual lighting and shadow conditions in every shot.

**20** Go through the clips in the sequence and adjust the Color Warper to match the shirt

color and saturation.


**Lesson 6 Managing Grades Across Clips and Timelines** **242**


##### **Activating Node Stacks**

While some colorists love having every stage of the grade under their fingertips, others

find a busy node tree hard to navigate and counter-productive. Neither view is wrong; it

comes down to how one personally uses the software and the structures that best

facilitate their workflow.


In DaVinci Resolve, you have the option of breaking up your node tree into a _node stack_

composed of multiple Node Editor segments called _layers_ . In this exercise, you will create a

node stack and copy grades based on layers.

**1** Select clip 28.

**2** Build a node tree specific to primary color correction only.


You can use the same nodes as in the previous exercise or apply the sample template

from the Templates album.

**3** Go to Project Settings > General Options, and in the Color section, change the amount

of Node Stack Layers to 3.

**4** Rename the layers **PRIMARY**, **SECONDARY**, and **LOOK** .


**5** Click Save.


The Node Editor now has the label “Clip – PRIMARY” in the upper right corner.


**Lesson 6 Managing Grades Across Clips and Timelines** **243**


**6** Click the dropdown arrow next to the label.


The Node Editor comprises three layers, followed by the Timeline Node Editor. You can

think of a node stack as a segmented node tree. The output of one layer is the input of

the layer that follows it.

**7** Open the SECONDARY layer.


**8** Build a node pipeline dedicated to secondary color correction.


**9** Open the LOOK layer.

**10** Create nodes for Look and Contrast.

**11** Add a third node for Halation.


Halation is a natural analog film artifact that occurs when light travels through the

emulsion layer and bounces off the film’s base layer, resulting in a chromatic edge

around bright objects and light sources.


You encountered a halation tool when working with the Film Look Creator effect, but

this stand-alone version gives you much more control over the final look.


**Lesson 6 Managing Grades Across Clips and Timelines** **244**


**12** Open the Effects panel and drag the Halation effect onto the node.


You can preemptively adjust the effect to suit the project style in the template.

**13** In the Halation settings, under Dye Layer Reflections, reduce Strength (0.200) and

Saturation (0.500).

**14** Add a fourth node to the LOOK node tree for the vignette.


**15** Open the Window palette and apply the Vignette preset you generated in Lesson 3, or

create a new one.

**16** Right-click in the viewer and choose Grab Still. Label the still **NS TEMPLATE** .

**17** Select clips 27-31, right-click the template still, and choose Apply Grade. This will

transfer all the layers of the node stack to all the selected clips. Middle-clicking will

transfer only the active layer.

**18** With the PRIMARY layer active in the Node Editor, go through the clips and perform a

primary pass. Ensure the clips are well exposed with matched contrast and saturation.

**19** Open the SECONDARY layer and perform a secondary pass. Focus on matching the

skies and skin tones, particularly in clips 29 and 30.

**20** Open the LOOK layer.

**21** Using clip 28 as the hero shot, design a look for the sequence.

**22** Select clips 27-31 (excluding clip 28).

**23** Right-click clip 28 and choose Apply Active Layer to copy the node tree from the active

LOOK layer **only** .


Applying a look grade will sometimes accentuate the differences between mismatched

clips, requiring another primary or QC (quality control) pass. Depending on the source

and quality of the footage, some colorists opt to apply a look first before doing

primary and secondary passes.


**Lesson 6 Managing Grades Across Clips and Timelines** **245**


Node stacks can help keep your workflow manageable by reducing the complexity of the

tree in the Node Editor.


Another use for node stacks is for color management. In the next project, you will use the

Color Space Transform effect to color manage footage within the Node Editor. With node

stacks, you can have dedicated layers for end-to-end image treatment or for alternative

outputs when needing to quickly switch between SDR and HDR standards.
## **Saving Stills for Other Projects**


The stills in gallery albums are usually only available in the active project. A different kind

of gallery album, the PowerGrade album, makes stills accessible to all projects in the active

project library.

**1** Open the Clip 05 grades album.

**2** Click the **1.5.2 Bleach bypass** still to highlight it. Then Hold the Command (macOS) or

Ctrl (Windows) key and drag to the PowerGrade 1 album near the bottom of the Stills

Albums list.


This will move a copy of the still to the PowerGrade album.

**3** Click the PowerGrade 1 album to view its contents. This copy of the bleach bypass

grade will now appear in the PowerGrade 1 album of all the projects you create in the

same project library.


TIP Double-click a PowerGrade still to append the grade to a selected clip on

the timeline. Middle-clicking will apply the grade, just as it does with regular

album stills.


Another way of preserving commonly used grades and node structures is

with _memories_ .

**4** Click the Memories button in the upper left of the gallery.


**Lesson 6 Managing Grades Across Clips and Timelines** **246**


This reveals a section of the Gallery panel that can retain stills for quick access. You will

create a memory still for converting footage into black and white.

**5** Select any ungraded clip on the timeline.

**6** Set Saturation to 0.00.

**7** Right-click in the viewer and choose Grab Still. Label it **BW** .


You can drag the still into a memory slot or expand the Gallery panel for

additional features.

**8** In the upper right corner of the gallery, click the Gallery View button.


A separate window opens, displaying the full contents of the Gallery View.


The Stills sidebar in the upper left features a collection of DaVinci Resolve looks and

provides access to stills from other projects and project libraries. The Group Stills

panel at the top right shows the contents of the selected project’s gallery.


The bottom of the window shows the current project’s gallery, and to the left is the

Project Memories panel.

**9** Drag the BW still into the Project Memory A slot.


**Lesson 6 Managing Grades Across Clips and Timelines** **247**


**10** Close the Gallery View window.


You can now apply grades and active layers directly from the Memories panel. You can

also assign a shortcut to the memory for even quicker application.

**11** Open DaVinci Resolve > Keyboard Customization.

**12** Enter **memory** in the Commands search field, expand the Color > Memories list, and

enter a shortcut keystroke for Load Memory A.


When assigning memory keystrokes, use numbers that correspond to the letter of the

memory as expressed numerically (A = 1, B = 2, etc). A good choice for memory A

would be Command-Option-Shift-1 (macOS) or Ctrl+Alt+Shift-1 (Windows).

**13** Click Save to close the Keyboard Customization window.

**14** Select clips 21-26 (excluding the graphic clip 24) and press your BW memory

shortcut keystroke.


Storing stills in PowerGrade albums is convenient when working with established looks,

such as when working on episodic projects or when retaining node tree templates for

quick setups of new grading jobs. Memories can make for faster workflows when you need

rapid and repeated application of specific grades. Couple them with keyboard shortcuts to

significantly reduce the time you spend managing and applying stills.


**Lesson 6 Managing Grades Across Clips and Timelines** **248**


##### **Exporting and Importing Stills**

Outside of using project libraries and PowerGrade albums, you can also share grades

across different workstations by exporting them from the gallery.

**1** Open the Clip 05 grades album.

**2** Right-click the **1.5.1. Split tone** still and choose Export.


The still’s visual and grading information is exported and contained in two files. The

DPX file is a high-quality image format used for visual comparison and review. The DRX

file contains the node tree and grading data. You need both files to migrate stills with

grade information.


NOTE If you have loaded a display LUT in the Project Settings (Color

Management > Video monitor lookup table), selecting Export With Display LUT

will generate the DPX and DRX files after LUT signal processing.


**3** Indicate a location in your storage and create a new subfolder for the two files.

**4** Name the export **Split_tone.dpx** and click Export.


**Lesson 6 Managing Grades Across Clips and Timelines** **249**


**5** Open the file browser on your workstation and locate the two files.


You can share the DPX file as you would any regular image across applications that

support the format. The DRX file is a DaVinci Resolve exchange format used to retain

grading (and effects) data that can only be processed together with the DPX image file.

To import a still grade into DaVinci Resolve, both files must be in the same folder or

directory.


Next, you’ll import a grade that was created for one of the clips on the timeline.

**6** Open the PowerGrade 1 album.

**7** Right-click in the Gallery panel and choose Import.

**8** In the file browser, locate the BMD 20 CC – Project 02 folder and navigate to

Other > Stills.

**9** Select **Broadcast_Techs.dpx** and click Import.


Notice that you only need to select and import the DPX file. The DRX file is bound to

the DPX, and its grading data will be included automatically upon import.

**10** Apply the **Broadcast_Techs** still grade to clip 21 ( **A020_C015** ) in the timeline.


**Lesson 6 Managing Grades Across Clips and Timelines** **250**


Here are some additional still options that colorists use for organizational and

practical purposes:


- **Right-click in the viewer and choose Grab All Stills.** Doing so will generate a gallery

still for each clip in the timeline (from either the first or middle frame). Colorists use

this option to keep track of their grading process over time (day 1 album, day 2 album,

and so on) or to separate the stills based on passes (balance pass album, secondary

pass album, and so on).

- **Right-click in the gallery and choose One Still Per Scene.** This choice restricts the

number of stills you can generate from any given clip to a single still. This option is

popular among colorists who frequently grab stills of their clips and do not wish for

their galleries to become cluttered with thumbnails.
## **Migrating Timeline Grades** **Using ColorTrace**


ColorTrace is a DaVinci Resolve feature that allows for transferring grading information

across timelines. It is a much faster and more organized method of copying mass grade

data than using stills.


You may use ColorTrace when multiple project types use the same source materials (film,

trailer, teaser, behind-the-scenes, and so on). Another scenario is when an external editor

creates changes in a timeline that a colorist has already begun grading. In both cases,

manually transferring the grades could be a mammoth task: a still would need to be

generated for each clip and then carefully reapplied to each corresponding clip on the

new timeline. The workflow would be slow and would have a high potential for error since

the overworked colorist would have to generate, organize, and retrack dozens (if not

hundreds or thousands) of stills in the gallery.


ColorTrace bypasses all that by presenting two timelines side-by-side and helping the

colorist identify their common media. The colorist needs only to accept (or reject) the

match, and the grading data is transferred instantaneously.

**1** Enter the edit page, and in the media pool, open the 03 Timelines bin.

**2** Choose File > Import > Timeline.

**3** Navigate to the BMD 20 CC – Project 02 folder, open the XMLs subfolder, and import

**02_TooMuchLife_30sec.xml** .


**Lesson 6 Managing Grades Across Clips and Timelines** **251**


**4** In the Load XML window, deselect the option “Automatically import source clips into

media pool” and click OK.


A pop-up window will prompt you to indicate the bins where the timeline’s media is

located. All the video media necessary to reconstruct this timeline was imported

during the initial XML setup. Only the audio track has changed.

**5** Click the disclosure arrows to expand the bin structure and deselect the 02 Audio

bin. Click OK.


The 02_TooMuchLife_30second_Trailer edit appears in the Timeline panel of the edit

page. The log window informs you that the audio track, TML_CT_bounce.wav, has

failed to link.

**6** Enter the media page and navigate to BMD 20 CC - Project 02 > Audio in the Media

Storage panel.

**7** Drag the missing audio file **TML_CT_bounce.wav** into the media pool’s 02 Audio bin.


In the edit page, the timeline will now be fully imported and linked.

**8** Enter the color page to check the grade status of the clips.


None of the grades created in 01_TooMuchLife_Trailer are visible in this newly imported

timeline. Each clip has a blank Node Editor with only the default ungraded node 01.

**9** Return to the edit page.

**10** In the media pool, right-click the 02_TooMuchLife_30second_Trailer timeline and

choose Timelines > ColorTrace > ColorTrace from Timeline.


NOTE The ColorTrace option will only be visible in the contextual menu if the

timeline you are right-clicking is the active timeline in the edit page.


**Lesson 6 Managing Grades Across Clips and Timelines** **252**


**11** In the ColorTrace Setup’s Project List window, expand the project library folder and

locate the Project 02 - Too Much Life Trailer project.


**Effects and Definitions**

The Effects and Definitions panel under the Project List allows you to define a set

of naming conventions for clips whose names have changed between

timeline versions.


A common example where this may happen is in VFX workflows. Assume that the

original filenames of two timeline clips were **car.mov** and **sky.mov** . Both clips were

sent to the VFX department for some compositing work. The VFX department

returns the finished composites under the names **car_vfx.mov** and **sky_vfx.mov**,

and they are inserted into a new version of the timeline. When ColorTrace is used

to transfer the grading data from the original timeline, the two VFX clips are not

recognized because of their new filenames. By entering _*_vfx_ in the Effects and

Definitions panel, DaVinci Resolve can exempt the suffix when associating media

between timelines.


**12** Select the 01_TooMuchLife_Trailer timeline and click Continue to launch the

ColorTrace tool.


At the top of the interface, you’ll find tabs for switching between the Automatic and

Manual modes.


**Automatic** attempts to locate the same clips used in both timelines based on source

name, timecode, and other metadata, regardless of changes in position or trim.


**Manual** allows you to identify and match clips yourself. Using this method, you can

assign grades when the original filenames or metadata were changed between edits.


**Lesson 6 Managing Grades Across Clips and Timelines** **253**


The bottom of the interface provides additional information and control over the copy

parameters. To the left is a table that compares the metadata of the source and target

clips, which is useful when verifying that two clips are derived from the same take. To

the right is a list of criteria that will be included or ignored during the grade transfer.


The clips in the Target Timeline have colored outlines that indicate their grade

match status:

 - **Green** —An exact match was found

 - **Blue** —Multiple matches were found

 - **Red** —No match was found


You will need to review the Target Timeline to ensure the matches are accurate and any

conflicts are resolved.


TIP Select Hide Matching Clips at the bottom of the interface to remove all

clips that are successfully matched in the timeline. Doing so will allow you

to focus on the clips with multiple or no matches.


**13** In the Target Timeline, the graphic on clip 07 has a blue outline. Select it to see which

clips are proposed as possible options in the Matching Source Clips list above it.


**Lesson 6 Managing Grades Across Clips and Timelines** **254**


Clip 07 clearly corresponds to the clip numbered 24 in the Matching Source Clips

window. You can verify this by looking at the table at the bottom left of the ColorTrace

interface and checking the Name property of the Source and Target clips.


NOTE If timelines in the ColorTrace interface feature blank thumbnails or

missing clips, it may be due to missing thumbnail metadata. To fix this, open

the affected timeline in the color page and briefly navigate around the timeline

to prompt a thumbnail cache render.


**14** Double-click clip 24 to approve the match. Both clips’ outlines will turn magenta as

confirmation.

**15** Clip 11 also has a blue outline. Select it and double-click the corresponding clip 30

above to confirm the correct match.

**16** Scroll down the Target Timeline and confirm the matches for remaining blue-outlined

clips: 18, 19, and 20.

**17** Clip 01 has a red outline and offers no options in the Matching Source Clips list. You

will address this clip manually after committing the automatic matches.


NOTE You can choose Set As New Shot to define clips with no links to the

original timeline. They will appear ungraded after the ColorTrace is performed.


**18** At the bottom of the window, click Copy Grade to transfer the grade data between the

green and magenta clips.

**19** To resolve the red clips, click the Manual tab at the top of the window.

**20** In the Target Timeline, select clip 01.


**Lesson 6 Managing Grades Across Clips and Timelines** **255**


The source timeline does not contain this clip. However, it features a similar clip 01,

which was captured outdoors in a similar location, with the performer wearing the

same clothes.

**21** In the source timeline, select clip 01 and click Paste to confirm the grade transfer.

**22** Click Done to exit ColorTrace.

**23** Enter the color page to verify that all the clips that were graded in 01_TooMuchLife_

Trailer were successfully copied to 02_TooMuchLife_30second_Trailer.


NOTE Keying and tracking data is preserved when copying grades using

ColorTrace.


Just as migrating timelines requires conforming, the ColorTrace workflow also calls for

some manual review to ensure that all grades have transferred correctly. Regardless,

ColorTrace is still a substantially faster and more accurate process compared to manual

color migration and will greatly reduce your grading workload.
## **Copying Grades Using the** **Timelines Album**


One of the quickest ways to transfer a single grade between clips in different timelines is

by using the Timelines album in the gallery.


In this exercise, you will perform a quick grade on a clip in the active 02_TooMuchLife_

30second_Trailer timeline and transfer it to the original timeline using the Timelines album.

**1** In 02_TooMuchLife_30second_Trailer, select clip 06.

**2** Reset the grade.

**3** In the ColorSlice palette, drag the Magenta vector’s Density up to deepen the pink

background.

**4** Drag the Hue parameter to change the background color from pink to purple.

**5** Enable Highlight mode in the viewer to preview the vector’s range.


**Lesson 6 Managing Grades Across Clips and Timelines** **256**


**6** Drag the Magenta Center parameter to adjust the vector range. You want the selection

to focus more on the background and furniture and less on the pink flowers in the

foreground.

**7** Disable Highlight mode.


Before


After


**8** Use the pop-up menu above the viewer to return to the 01_TooMuchLife_

Trailer timeline.

**9** In the gallery’s Still Albums side panel, open the Timelines album.


**Lesson 6 Managing Grades Across Clips and Timelines** **257**


**10** Use the pop-up menu at the top to access the 02_TooMuchLife_30second_Trailer

grade contents.


The gallery now displays the current state of all the clips in the 02_TooMuchLife_

30second_Trailer timeline. Note that even the ungraded graphics clips are included.

This helps you keep track of both graded and ungraded clips in various timelines.

**11** In the 01_TooMuchLife_Trailer timeline, select clip 23.

**12** In the gallery, middle-click clip 06 to transfer the graded interview clip.


The exercises in this lesson presented a broad list of options for grade setup and

duplication. When copying grade data, it’s important to consider your needs on a project
by-project basis. In most cases, a combination of one or more of these copying techniques

is ideal; in other cases, a mix of methods could be less efficient than employing a more

global solution such as ColorTrace or remote timelines.
## **Self-Guided Exercises**


Complete the following exercises in the 01_TooMuchLife_Trailer timeline to test your

understanding of the tools and workflows covered in this lesson.


**Clips 08-11** —Transfer the montage grade (from clips 05-07) to the remainder of the clips in

the sequence.


**Clip 20-26** —Remove the black-and-white grade from the clips. Then, using the

**Broadcast_Techs** grade on clip 21 as a starting point, transfer the vibrant purple-and
yellow look across the rest of the broadcast studio sequence.


**Lesson 6 Managing Grades Across Clips and Timelines** **258**


When you’ve completed these lessons, you can import **01_TooMuchLife_Trailer_**

**COMPLETED.drt** and **02_TooMuchLife_30second_Trailer_COMPLETED.drt** to compare

your work with the “solved” versions of these timelines. If any media appears offline, click

the red Relink Media button in the upper left corner of the media pool and specify the

location of the Project 02 media on your workstation.


To ensure the project management is set up correctly, right-click the imported timeline and

choose Timelines > Timeline Settings. Select Use Project Settings in the lower left of the

settings panel to link it to the project-wide color management settings.
## **Lesson Review**

**1** How do you create a new local version of a grade?

**2** How many layers are in a node stack?

**3** True or False? You can access stills saved in other projects and project libraries.

**4** How do you copy just one node from the node tree of a still in the gallery?

**5** True or False? You can create keyboard shortcuts for your favorite grades and stills.


**Lesson 6 Managing Grades Across Clips and Timelines** **259**


##### **Answers**

**1** Right-click and choose Local Versions > Create New Version or press Command-Y

(macOS) or Ctrl-Y (Windows).

**2** You can choose to have up to four layers in a node stack.

**3** True. Click the Gallery View button to launch the expanded gallery and access the

galleries of other projects and project libraries in the Stills sidebar.

**4** Right-click the still in the gallery and choose Display Node Graph. Then, drag the

necessary node into the Node Editor of the active clip.

**5** True. You can create keyboard shortcuts for grades in the form of Project Memories.


**Lesson 6 Managing Grades Across Clips and Timelines** **260**


### Part III
# Optimizing the Grading Workflow

## **Lessons**


- Using Groups

- Adjusting Image Properties

- Setting Up Raw Projects

- Delivering Projects


Welcome to Part III of _The Colorist Guide to DaVinci Resolve 20_ . This section covers more

advanced image-processing efficiency and DaVinci Resolve processes that manipulate and

render image data. You will create group grading workflows based on shared criteria,

adjust common optic image properties, set up raw materials in the industry standard

ACES framework, and deliver the final project.


**Project File Location**

You will find all the necessary content for this part of the book in the folder

BMD 20 CC - Project 03. Follow the instructions at the start of every lesson to

find the necessary folder, project, and timeline. If you have not downloaded the

third set of content files, see the “Getting Started” section of this book for

instructions on how to do so.


**Optimizing the Grading Workflow** **261**


**This page is intentionally left blank** **262**


### Lesson 7
# Using Groups



In this lesson, you will focus on an

organizational feature of the color

page that enables clip grouping based

on shared contextual or visual criteria.


Although generating and organizing

groups is incredibly simple, the time
saving and future-proofing benefits

can lead to much more efficient

workflows and advanced grading

techniques. In addition to applying

group-wide color management

and grades via the Node Editor, the

grouping feature allows timeline

filtering based on group name and

the use of the split screen to quickly

compare clips in the same group.



Time

This lesson takes approximately
4.5 hours to complete.

Goals

Preparing Media Using
Scene Cut Detection 264

Creating a Group 273

Applying Base Grades at the
Pre-Clip Group Level 277

Making Clip-Specific Adjustments
at the Clip Group Level 288

Automatically Tracking
People and Objects 295

Creating a Unifying Look Using
the Post-Clip Group Level 313

Working with Lookup Tables 321

Using the Timeline Level 333

Self-Guided Exercises 340

Lesson Review 341


## **Preparing Media Using** **Scene Cut Detection**

The first video project in this section is a single self-contained video file. Placing the video

directly onto a timeline in DaVinci Resolve would result in it being treated as a single clip,

and all grading changes on the color page would affect it uniformly. To avoid this, you can

place cuts throughout the timeline to separate the individual shots and allow for content
specific grading. Doing this manually can be extremely time-consuming and prone to

human error.


Fortunately, the Scene Cut Detection feature automates this process. It analyzes edited

video files before import and splits their content into subclips to facilitate clip-by
clip grading.

**1** Open DaVinci Resolve 20.

**2** In the Project Manager, click the New Project button.


When you create a new project, a dialog will prompt you to enter the project name and

specify a storage location for all media generated within DaVinci Resolve, such as

voiceovers and ADR (automated dialogue replacement) that are recorded directly to

the audio track.


**3** Enter the name **Project 03 - The Long Workday Commercial** .

**4** If necessary, click Change Location and select an optimal folder for your

generated media.

**5** Enter the media page.

**6** Create two new bins in the media pool labeled **Video** and **Timelines** .

**7** Select the Video bin as the destination for the media you are about to import.

**8** In the media storage browser, locate the BMD 20 CC - Project 03 folder.


**Lesson 7 Using Groups** **264**


**9** In the folder, right-click the **Project 03 - The Long Workday SCD.mov** file and choose

Scene Cut Detection.


Scene Detect graph Cut List


You will use this interface to run the edit analysis and import the resulting subclips. At

the top of the window, three viewers display the current frame (middle), the previous

frame (left corner), and the next frame (right corner). Below the viewers, the Scene

Detect graph displays the location of the video’s cut points after the analysis. To the

right, the Cut List identifies the scene cuts and their timecodes.

**10** In the lower left corner of the window, click Auto Scene Detect.


As the analysis runs, the assumed edit points are marked with green lines in the Scene

Detect graph, and their timecodes are recorded in the Cut List.


**Lesson 7 Using Groups** **265**


TIP The height of the vertical green cut lines indicates DaVinci Resolve’s

confidence that a cut has been correctly identified. Cuts that fall under the

horizontal magenta “confidence line” are omitted from the cut list and appear

gray on the graph.

When a video has many jump cuts and whip pans, the Scene Cut Detection

tool might place many cuts beneath this confidence line. To include less
confident cuts in the final Cut List, drag down the magenta line until the

vertical lines turn green.


**11** To review the edits, scrub through the timeline by dragging the orange playhead or

click inside the Cut List and press the Up and Down Arrow keys to navigate and verify

the identified cut points.


TIP You can also press P (previous) and N (next) to jump between the cut

points in the Scene Detect graph.


A correctly identified cut will display a unique image in the left corner viewer, followed

by two similar images in the center and right corner viewers.

**12** Navigate through the edits in the Cut List until you reach scene 12.


**Lesson 7 Using Groups** **266**


Although DaVinci Resolve detected a cut here, it is actually part of the same take. The

false detection occurred because of a headlight lens flare that created enough of a

visual change in the frame to make DaVinci Resolve identify it as the start of a new shot.

**13** With the cut already selected, in the lower left of the Scene Cut Detection window, click

Delete to remove it.

**14** Press the Down Arrow key to continue navigating through the Cut List and ensure that

all the remaining cuts are correctly identified.


Toward the end of the timeline, you’ll find a large cluster of cut points. Dissolves and

transitions are prone to misidentification and will sometimes be marked as a series

of rapid cuts.

**15** Drag the playhead to the left of this cluster and press I to create an In point in the

Scene Detect graph.


TIP Drag the scroll bar under the Scene Detect graph to zoom in and out.


**16** Drag the playhead to the right of the dissolve cluster and press O to place an Out point.


**17** On the right side of the toolbar, click the Prune icon to delete this batch of false

cut points.

**18** Ensure that no other cut points from the transition area remain. If one is still present,

drag the playhead over it and press Delete.

**19** Press the Left and Right Arrow keys to move through the video frame-by-frame and

identify the exact cut point between the last clip and the solid white color matte at the

end of the timeline.


**Lesson 7 Using Groups** **267**


**20** Click Add to add the edit to the Cut List.


A green line appears under your playhead to indicate an edit point. A new item also

appears on the Cut List with the frame number (2352) and start timecode (01:01:38:00)

of the cut point.


You have now reviewed all the cut points on this timeline. At this point, you should

have 26 scenes in your Cut List.

**21** In the lower right corner, click Add Cuts to Media Pool.


NOTE When importing media, if a dialog appears informing you that your

clips’ frame rates don’t match the project’s frame rates, click Change to update

the project settings to accommodate the media. However, you shouldn’t

change a project’s frame rate if you have set it up with a specific deliverable in

mind. In that case, the media will automatically be retimed to accommodate

the timeline frame rate.


When working on longer films or with edits featuring frequent jump cuts, reviewing

scene cut detection can be a time-consuming process. You can choose to break up this

task into several sessions, backing up your progress as you go.

**22** To back up this completed scene cut, go to the Options menu at the upper right of the

window and choose Save SceneCut.

**23** Choose a location to save the .sc file.

**24** When finished, click X in the upper left corner to close the Scene Cut Detection

interface.


The commercial now appears in your media pool as a series of subclips in the

Video bin.


TIP In DaVinci Resolve Studio, scene cut detection can be performed on

media after it has been imported and added to a timeline. In the edit page,

click to select a clip on a timeline, or use In and Out points to indicate a range

of clips, and then choose Timeline > Detect Scene Cuts. The resulting cuts can

be edited via the rolling trim tool or deleted using the Delete (Backspace) key.


**Lesson 7 Using Groups** **268**


Although colorists ordinarily prefer to work with raw camera materials, flattened video

renders are still popular for their lighter file size and faster transfer speed. This method of

content migration is particularly popular when working on short-form projects such as

commercials, music videos, and mini-documentaries. It simplifies project sharing when

working with remote clients who don’t have access to servers or fast internet connections.

Additionally, this workflow is often necessary when working on older projects for which the

original media no longer exists and only the master render is available. In both cases, it’s

crucial to use the highest-quality codec and file format possible and to avoid overlaid

text, effects, or transitions that cannot be disabled in the rendered video file.

##### **Creating a Timeline from** **Selected Media Pool Clips**


Before you can start grading, you must arrange these subclips in a timeline. To ensure that

the clips populate the timeline in the correct order, you will organize your media pool

by timecode.

**1** In the upper right of the media pool, click the List View button to access the

metadata columns.

**2** Click the Start TC column title to sort the clips by their start timecodes.


With the clips listed in their correct order, they are now ready to be placed into

a timeline.


TIP Clicking any column title will sort the contents of a bin by that criterion.

Clicking the column title again will toggle the order from ascending

to descending.


**Lesson 7 Using Groups** **269**


**3** Enter the edit page.

**4** Select all the media in the Video bin by clicking one clip and pressing Command-A

(macOS) or Ctrl-A (Windows).

**5** Right-click any of the selected clips and choose Create New Timeline Using

Selected Clips.

**6** Name the new timeline **Project 03 - The Long Workday** and click Create.


A new timeline appears on the edit page containing the 27 selected clips in the

media pool.

**7** Drag the timeline into the Timelines bin.


Your import process is now essentially complete. At this stage, you can set up color

management and start grading.


However, let’s look closer at another factor that may impact your work and set up the

timeline for more seamless grading.

**8** Navigate to the last cut in the timeline, where the shot of the man fades to white.


This might prove difficult to grade because you will need the final look of the shot to

fade to white as the commercial ends. Normally, you’d apply a video transition to

facilitate this, but that is not possible on a subclip. Instead, the color will abruptly shift

to white as the playhead reaches the cut point.


**Lesson 7 Using Groups** **270**


This is why clients should be advised not to leave transitions in self-contained video

renders and, preferably, to include handles (extra media frames) around the media trims to

allow for later transition application. If you were to attempt to add a dissolve to the timeline

right now, it wouldn’t take because of the lack of trim data in the subclips. In the timeline,

this is indicated by red trim lines.


By changing how the media is conformed on the timeline, you can alter the behavior of cut

points while maintaining control over the individual clip properties.

##### **Importing Pre-Conformed EDLs**


In this exercise, you will rebuild the same timeline using a pre-conformed EDL process to

ensure a smoother overall workflow. With this method, your clips will have trimmable cut

points and unique attributes (which are necessary for inputting metadata, adding flags,

and assigning input color spaces).


You’ll start by returning to the Scene Cut Detect interface in the Media Storage panel.

**1** Go to the media page.

**2** In the Media Storage panel, right-click **Project 03 - The Long Workday SCD.mov** and

choose Scene Cut Detection again.


If DaVinci Resolve has not been closed since the last exercise, the Scene Detect window

will appear with all the previous cuts loaded in the Scene Detect graph and cut list.

If the window is empty, go to Options > Load SceneCut and import the .sc file you

generated earlier (or rerun the entire Auto Scene Detect exercise).

**3** In the Options menu in the upper right, choose Save EDL.

**4** When the Conform Settings dialog appears, click OK and choose a location to save

the EDL file.


In the second part of the book, you conformed a timeline from an XML file. An EDL

serves the same function, although with significantly less metadata. It’s usually

insufficient for sharing timelines with collaborators but works very well when the only

data you need are the edit points in a self-contained video file.


**Lesson 7 Using Groups** **271**


**5** Click X in the upper left corner to close the Scene Cut Detection interface.


To reconstruct the timeline with trim data, you’ll need to work with a non-trimmed

version of the video file.

**6** Delete the timeline in the Timelines bin and all the subclips in the Video bin.

**7** Drag **Project 03 - The Long Workday SCD.mov** into the Video bin.

**8** Click the Timelines bin and choose File > Import > Pre-conformed EDL.

**9** Navigate to the location of the EDL file you had generated and import it.

**10** In the “Parse preconform options” dialog, click OK.

**11** A pop-up will prompt you to indicate where the media for the timeline is located. Since

the self-contained video file is already in the Video bin, you can click OK to confirm.


The timeline Project 03 - The Long Workday SCD appears in the Timelines bin.

**12** Double-click the timeline to launch it in the edit page.

**13** Navigate to the last cut in the timeline, where the shot fades to white.


The cut point now highlights green when you click it. This means you can add a video

dissolve to it.


To test this, you will grade the penultimate clip and ensure it fades to the white solid

at the end.


**14** In the edit page, open the Effects panel.

**15** From Toolbox > Video Transitions, drag Dip to Color Dissolve onto the cut point.

**16** Select the dissolve on the timeline and open the Inspector.

**17** Double-click the Color swatch box and change the color to white.

**18** Set the Alignment to Right.


**Lesson 7 Using Groups** **272**


**19** Go to the color page.

**20** Select clip 26.

**21** Drag the Gain color wheel toward orange.

**22** With looping disabled in the viewer, play the end of the timeline to watch the vibrant

orange look dissolve seamlessly into the white matte at the end.

**23** Reset the grade on clip 26.


The additional steps you took to create this timeline after the original Scene Cut import will

not always be necessary but will be invaluable when working with limited media trims that

require dissolves. This solution is particularly helpful when working with dissolves between

two video clips, where a simple solid matte would not solve the issue.

##### **Enabling Smart Caching**


Caching is a process in which a clip is rendered while it is still in the timeline so you can

play it back in real time when reviewing it. It’s similar to exporting, except the rendered clip

is automatically viewable as part of the timeline media.


Some of the tools you will use in the upcoming exercises will be processor-intensive and

might impact playback speed. You will enable Smart caching to automatically render

certain clips as you work on them.


- Choose Playback > Render Cache > Smart.


Using the Smart Cache option leaves it up to DaVinci Resolve to determine which

media or nodes are computationally intensive enough to require caching.


You’ll learn about caching in much more detail in Lesson 8, “Adjusting Image Properties.”
## **Creating a Group**


When incorporating groups into a grading workflow, your first task is to choose a grouping

strategy for your timeline. Depending on the project, you can base groups on source

cameras, locations, scenes, color schemes, or any criteria of your choice.


In the commercial project in this lesson, you will create groups to differentiate between

scenes based on their locations and times of day.


**Lesson 7 Using Groups** **273**


**1** Select clip 06 and Shift-click clip 13 to select the eight consecutive garage clips in

the timeline. Ignore for now that clip 13 is a highway clip.


**2** Right-click any of the highlighted clips and choose Add into Current Group.


A green link symbol appears in the lower right corner of the clips to indicate their

group status. These clips will now react uniformly when you utilize the group-level

Node Editors in later exercises.

**3** Right-click any of the grouped clips and choose Groups > Group 1 > Rename.

**4** Enter the group name **Garage** .


Upon closer inspection, it appears that clip 13, the highway shot, does not belong in

this scene and should not be included in this group.

**5** Right-click clip 13 and choose Remove from Group.


You can also use groups for filtering purposes.

**6** In the timeline, Command-click (macOS) or Ctrl-click (Windows) clips 02 and 13.

**7** Right-click one of them and choose Add into a New Group.

**8** Enter the group name **Highway** .


The link symbols on the Garage group disappear and are now visible only on the

Highway group clips. From now on, the green link symbols will appear only for the

actively selected group clips.


The two Highway clips are relatively far apart on the timeline, so matching them could

become tedious as you navigate up and down the timeline to compare them.


**Lesson 7 Using Groups** **274**


**9** In the interface toolbar, choose Clips > Grouped > Highway.


The filter hides all media except the two highway clips, which now appear side by side.

You can quickly compare and match them using the Up and Down Arrow keys.


**10** Select Clips > All Clips to remove the timeline filter.


You’ll need to create three more groups to prepare for the exercises in this lesson.

**11** Scroll down the timeline, select clips 19 to 24, and add them to a new group

called **Home** .


Note that the final clips 25 and 26 were shot outdoors, meaning their lighting

conditions are different from the indoor sequence. It is advisable to grade clips with

different light sources separately.

**12** Add clips 03 to 05 to a new group called **Office** .

**13** Add clips 16 to 18 to a new group called **Morning** .


**Lesson 7 Using Groups** **275**


##### **Adopting Groups in a Classic** **Color Grading Workflow**

With your clips sorted into groups, you can now choose how their grading will be targeted.

You can continue to make individual adjustments or apply group-wide changes. Doing so

will result in a faster workflow in which you’ll no longer need to duplicate and reapply

grades or nodes to individual clips. Reducing this duplication of effort will also lessen the

chance that mistakes will creep into your workflow. Instead of readjusting specific nodes

on multiple clips or keeping track of dozens of stills, you can tweak a group grade to adjust

all a scene’s clips at once.


The following figure shows how the classic color grading workflow, previously expressed

as a node tree in Lesson 1, can be represented in a group-based node structure.


IDT and ODT refer to Input and Output Display Transforms such as
CST (Color Display Transform) and ACES Transform.


As with node stacks, you can think of groups as segmented node trees. Although in this

case, the two group levels (pre-clip and post-clip) will impact all the clips in the group.

These are all the available grading modes in the Node Editor and their

recommended usage:


- **Group pre-clip** is intended for preparatory grading adjustments such as node-based

color management (CSTs), gamut and gamma mapping, and color chart auto
correction.

- **Clip** mode enables you to address the individual needs of each clip in a group,

including balancing, matching, and secondary grade adjustments.


**Lesson 7 Using Groups** **276**


- **Group post-clip** is best utilized for creative scene grading. By this stage, your clips

should be matched, and their individual secondary requirements met. This will ensure

the uniform application of the creative grades and will require only minimal tweaking

on a clip-by-clip level. This mode is also commonly used for node-based color

management.

- **Timeline** will affect every clip on the timeline. Color correction and creative grading

are not recommended at this stage, but you could use this mode to implement

artificial grain and film effects, apply vignettes to short-form projects, or remap the

color space of a timeline to a single deliverable standard.


This breakdown suggests the signal order in which the visual data is processed, but you

should not see it as a strict order of grading operations. As with any grading workflow, it’s

entirely acceptable (and expected) to jump between group levels throughout the grading

process. Note that the output of earlier group modes is the direct input of later modes (for

example, the pre-clip output leads to the clip input). When considering node order, think of

the group modes as being one long node tree, the signal impact of which was explored

in Lesson 5.
## **Applying Base Grades at the** **Pre-Clip Group Level**


At the pre-clip group level, you can make adjustments that will uniformly affect the RGB

input signals of all the clips in a group.


The content of each clip in a scene will still vary due to differences in framing and lighting,

so this level is not advised for achieving a perfectly neutral starting point. Instead, use this

level to set up a scene with the help of broad color management tools, such as Color Space

Transform (CSTs), ACES Transform, Lookup Tables (LUTs), color charts, Gamut and Gamma

Mapping, and others.

##### **Setting Up Node-Based Color Management**


In this project, you will use node-based color management. Rather than transforming clips

on a project level, you will use the Color Space Transform (CST) effect to map clips

individually. This will allow you to quickly set up and ripple the color spaces of clips from

different sources and choose the precise point in the processing pipeline when the colors

are mapped. With project color management, the output color space is the definite last

step of the signal pipeline, whereas with CSTs, you can add more grade adjustments and

effects after the color map, such as vignettes, halation, and grain.


**Lesson 7 Using Groups** **277**


There is no limit to how you employ CSTs in your workflow, but two common

approaches are:


- Using a single CST node to map from the camera input color space to the deliverable

output color space. In such a setup, the CST would usually be among the last

operations in the node tree. In a group structure, it should be placed in the Group

Post-Clip layer (or Timeline layer), and all grading operations should be performed on

upstream nodes.


Grading operations Input > Output


- Using two CST nodes to first map the footage to a working timeline color space at the

start of the node tree and then to the output color space near the end of the node

tree. In a group structure, these nodes would usually be placed at a Group Pre-Clip

and Post-Clip layers, respectively, with most grading operations placed in between.

|Col1|Col2|Col3|Col4|
|---|---|---|---|
|||||
|||||



Input > Timeline Timeline > Output


In this exercise, you will use two CSTs to map the footage to the optimal HDR-ready DaVinci

Wide Gamut working color space.

**1** Select clip 01.

**2** Label node 01 **INPUT CST** .


**Lesson 7 Using Groups** **278**


**3** Open the Effects panel and drag the Color Space Transform effect onto the node.


Some of the settings will look similar to those found in the Resolve Color Management

section of the Project Settings. Additionally, there are Tone and Gamut Mapping

controls for dedicated per-clip management.

**4** Set the Input Color Space to Blackmagic Design 4K Film Gen 1. This was the camera

model, data level, and firmware version used to capture the footage.

**5** Set the Input Gamma to Blackmagic Design 4K Film to map the transfer function

correctly. This will set up the image’s luminance and contrast.


Since the intention is to use two CSTs to color manage this clip, the output settings of

this first CST node should map the signal to a working color space, not to the

deliverable output.

**6** Set the Output Color Space to DaVinci Wide Gamut.


**Lesson 7 Using Groups** **279**


**Lesson 7 Using Groups** **280**


**7** Set the Output Gamma to DaVinci Intermediate.


With the footage mapped to a working color space, you can now add a second CST to

map it to your monitoring standard.

**8** Select the INPUT CST node and press Command-C (macOS) or Ctrl-C (Windows)

to copy it.

**9** Create a new node (02).

**10** Press Command-V (macOS) or Ctrl-V (Windows) to paste the INPUT CST node. Change

the label to **OUTPUT CST** .

**11** In the Effects panel Settings, click Swap under the Color Space Transform parameters

to swap the inputs and outputs. This saves a little time in having to re-input the

working color space.


**12** Set the Output Color Space to Rec.709 or your preferred monitoring gamut.

**13** Set the Output Gamma to Rec.709 or your preferred monitoring transfer function.


Rec.709 as a Gamma setting is equivalent to the Rec.709 (Scene) option in the Project

Settings. Visually, it achieves the look of Rec.709 Gamma 2.4, but rather than applying

the OOTF (opto-optical transfer function) as metadata in the rendered file, it bakes it

into the final image to ensure it looks the same when uploaded to the web as it does in

your DaVinci Resolve viewer.


Even if you do not enable project-wide color mapping (as we did in the last project), the

Color Management controls in the Project Settings still impact the behavior of the

color page and output of your media.

**14** Open the Project Settings and go to the Color Management section.


With “Color science” set to DaVinci YRGB, the only two color management options will

be the Timeline and Output color space dropdown menus.

**15** The Timeline color space will impact the operation of your grading tools and effects.

Since some effects benefit from operating in a wider gamut, set the Timeline color

space to DaVinci WG/Intermediate.


**Lesson 7 Using Groups** **281**


**16** The Output color space will determine the color space metadata encoded in your

rendered video file. This should match your deliverable standard when you export

your final project. Leave the Output color space as Rec.709 (Scene).


Note that because there is no project-wide color management enabled in the Project

Settings, even if you were to change the output color space, no change would occur in

the viewer.


This is an example of how a single clip can be color-managed with CST nodes. The majority

of the grading and effects can be applied on the connection line between the two CSTs,

but you can also add nodes before and after the CST nodes. When used with node

templates, CSTs can be pre-emptively set up within a larger node tree to accommodate a

wide range of workflows and media sources.

##### **Using CSTs in Groups**


In this exercise, you will apply CST color management to a group.

**1** In clip 01, select the INPUT CST node and press Command-C (macOS) or Ctrl-C

(Windows) to copy it.

**2** Select clip 08, which is in the Garage group.

**3** In the dropdown menu in the upper right of the Node Editor, switch to Group

Pre-Clip mode.


In this mode, all adjustments you make will apply to the whole group. Note that the

node’s outline has changed to yellow, which will act as a visual reminder that you are

not working on the clip level.

**4** Select node 01 and press Command-V (macOS) or Ctrl-V (Windows) to paste the INPUT

CST node.


A different camera was used to capture this footage.


**Lesson 7 Using Groups** **282**


**5** Select INPUT CST and change the Input Color Space to Blackmagic Design 4.6K Film

Gen 1 and the Input Gamma to Blackmagic Design 4.6K Film.


Next, you will apply the CST mapping from the timeline to the output color space at the

end of the group node tree.

**6** In the dropdown menu at the top of the Node Editor, switch to Group Post-Clip mode.

**7** Select node 01 and press Command-V (macOS) or Ctrl-V (Windows) to paste the CST

node again. Change the label to **OUTPUT CST** .

**8** As with the previous exercise, swap the input and output parameters and then change

the both outputs to Rec.709 or your preferred output standard.


To save time, you can save Group grades as stills and apply them to other groups in

the timeline.

**9** Right-click in the viewer and choose Grab Still. This will create a POST still in the gallery.

**10** Switch to Group Pre-Clip mode and grab another still. This will generate a PRE still in

the gallery.


**11** With clip 08 (or any clip that is currently in a group) still selected, press Command-A

(macOS) or Ctrl-A (Windows) to select all the clips in the timeline.

**12** Middle-click the PRE still or right-click it and choose Apply Grade.


This applies the input CST node to all clips with a pre-clip mode. Non-grouped clips are

ignored. The same principle applies when rippling node changes within group

node trees.

**13** Switch to Group Post-Clip mode, and with all the clips still selected, apply the POST

still grade.


All the timeline groups (Highway, Office, Garage, Morning, and Home) should now be

color-managed in their Pre- and Post-Clip Node Editors.


**Lesson 7 Using Groups** **283**


TIP To remove a clip from a group but retain all the nodes you created in the

pre-clip and post-clip levels, right-click a clip and choose Collapse Group

Grades. All the nodes will be moved onto a single clip mode node tree in the

correct operational order.


All the remaining ungrouped media on this timeline is in the Blackmagic Design 4.6K

Film Gen 1 color space.

**14** Select clip 14.

**15** Middle-click clip 01 to apply the input and output CST nodes to the node tree.

**16** In the INPUT CST node, correct the Input Color Space and Gamma to

Blackmagic Design 4.6K Film Gen 1.


You need to apply these CSTs to all the ungrouped clips in the timeline. To save time,

you can use a filter.

**17** Grab a still of clip 14 and label it **CST** .

**18** Change the Clips timeline filter to display Ungraded Clips.

**19** Select the remaining four clips (including the white matte at the end of the timeline)

and apply the clip 14 CST still to them.

**20** Remove the timeline filter to show all clips.

**21** Right-click any clip and choose Update All Thumbnails to refresh the images in the

Thumbnail timeline.


With all media now mapped from the source camera color profile to the output color

space, its appearance in the thumbnails and viewer is now more naturally saturated

and has deeper contrast.


This timeline features multiple locations and times of day, requiring more frequent

grouping classifications. Depending on the nature of the projects you work on, you may

find that you need to use fewer or broader groups. This exercise aimed to show you how to

quickly address node-based color management, even when dealing with many groups and

occasional ungrouped clips. Other workflow options for CSTs include using them in node

stack layers, in versions, and even in shared nodes.


**Lesson 7 Using Groups** **284**


##### **Using a Color Chart to Balance a Group**

One method of balancing a sequence of clips is to use the calibration charts that are

typically captured at the start of the scene shoot. Calibration charts can produce more

accurate color correction than regular balancing because of their meticulously designed

color swatches that extend beyond just fixing the white balance.


NOTE The remaining exercises in this lesson require you to have imported,

grouped, and color-managed the timeline based on the previous exercises. If you

have not done so, open BMD 20 CC – Project 03 > Timelines and import the

**Lesson 07 Timeline SETUP.drt** timeline. In the media pool, relink (or replace) the

**Project 03 - The Long Workday SCD.mov** video file (if necessary) and set the

Timeline Settings to Use Project Settings.


**1** Change the Clips timeline filter to display only the Home group.


When using a color checker, a new shot of the chart should be captured at the start of

every new scene, light change, or location during filming.

**2** Select clip 01.

**3** In the Node Editor, switch to Group Pre-Clip mode.

**4** Create a new node (02) after the INPUT CST and label it **Color Match** .

**5** In the left palettes, open the Color Match palette.


**Lesson 7 Using Groups** **285**


**6** In the viewer’s onscreen controls dropdown menu, choose Color Chart.


**7** Drag the corners of the color chart overlay to the corners of the chart in the image.

Ensure that the small squares within the color chart outline are filled with the colors

they are meant to be analyzing. Any interference with the black borders or the man’s

fingers will affect the quality of this analysis.


**8** At the top of the Color Match palette, verify that X-Rite ColorChecker Classic - Legacy is

chosen. This selection is based on the manufacturer and version of the chart captured

in the shot.


**Lesson 7 Using Groups** **286**


**9** Set the Source Gamma to DaVinci Intermediate.


If color management is not enabled, Source Gamma must be set to the encoded

gamma (or log or PQ curve) of the source footage. This allows Color Match to map the

tonal encoding of the image to the timeline gamma.


If color management is enabled (whether via the Project Settings or nodes), Source

Gamma must match the timeline gamma of the project or whichever transfer function

is currently being applied to the signal at that point in the node tree.

**10** Set the Target Gamma to DaVinci Intermediate.


It may feel counterintuitive to use the same setting for both source and target, but it

makes sense when you consider that the Color Match palette in this instance is not

being used for the purpose of mapping the tonal range of the footage. This has

already been accomplished with the CST nodes. Right now, you are only interested in

calibrating the colors of the scene based on the source lighting.

**11** Set the Target Color Space to DaVinci Wide Gamut to keep the result consistent within

the CST-defined timeline color space.

**12** The Color Temp parameter lets you manually adjust the image’s target color balance.

The default 6500K will produce a neutral result. Leave it as it is.

**13** At the bottom of the Color Match palette, click Match. You will see a shift in color and

luminance as the waveform and parades are raised and balanced according to

the chart.


TIP The numbers that appear under the color boxes in the Color Match

palette indicate the percentage that a value needed to be adjusted to match

the color patch samples to the precalculated color chart targets. A change of

less than 10% is ideal, implying a clean starting point with a distortion-free

adjustment.


**14** Set the viewer’s onscreen controls to Off to remove the Color Match overlay.

**15** Navigate down the timeline to verify that the rest of the clips in the Home group have

been calibrated. Since these were captured in the same location, under similar lighting

conditions, the automated color balance benefits them equally.


With this chart, you have quickly created a better starting point for all the clips in the scene

while retaining the full dynamic range and color quality to perform individual corrections

and creative grading later.


**Lesson 7 Using Groups** **287**


## **Making Clip-Specific Adjustments** **at the Clip Group Level**

When working with groups, you continue to have access to the standard Node Editor in

Clip mode. It remains the ideal way to color correct, match footage, and make secondary

amendments on a clip-by-clip basis.

##### **Matching Shots at the Clip Group Level**


To ensure creative grades look consistent when applied to groups, it’s important that all

the group clips have matching color balance and equal luminance distribution.

**1** Filter the timeline to show only the Garage group clips.

**2** Switch the Node Editor to Clip mode.

**3** Select clip 01. At first glance, the shot appears to be substantially brighter than the

other clips in the scene.


**Lesson 7 Using Groups** **288**


**4** Drag the viewer playhead to the end of clip 1.


However, after the man enters the garage, the shot appears to be exposed similarly to

others in the sequence and does not require matching.

**5** By default, the images in the Thumbnail timeline show the first frame of every clip.

Click and drag within the thumbnail to change the frame.


When comparing clips, remember that the first frame is not always the most reliable

for matching. You should always play through the entire clip before making a grading

decision. In this case, you can leave clip 01 as it is.

**6** Select clip 04. This shot is definitely darker than the rest of the sequence.

**7** Right-click clip 05 and choose Wipe Timeline Clip to enable the Wipe mode in

the viewer.


**Lesson 7 Using Groups** **289**


**8** Open the Sizing palette in Reference Sizing mode and pan and zoom clip 05 to see the

man more clearly in the wide shot.


**9** Press Option-F (macOS) or Alt-F (Windows) to expand the viewer and see the

differences between the clips more clearly.

**10** Open the waveform scope (in RGB mode with Colorize enabled) to view a graphic

representation of the chromatic differences between the clips. Just as in the viewer, the

waveform is split along the wipe line.

**11** Label node 01 in clip 04 **Match** .

**12** Drag the Gain master wheel right to brighten the highlights. Aim to match the

waveform spikes that represent the light sources reflected on the garage floor of the

reference image.

**13** Drag the Lift master wheel right slightly to brighten the shadows. Keep an eye on the

man’s suit to ensure a good match in the viewer and waveforms.

**14** Finally, drag the Gamma master wheel right to match the overall waveform distribution

in the lower midtones. Use the green channel of the RGB waveform as a match

reference.


While the image’s tonal distribution looks accurate, there is now a strong green cast

throughout. The color bars can more accurately be used to fix this color imbalance.

**15** Switch the Primaries palette mode to color bars.

**16** Drag down the green Lift bar to neutralize the suit and garage shadows.


**Lesson 7 Using Groups** **290**


**17** Drag the red Gamma and Gain bars down to address the resulting red tint.


**18** Press Option-F (macOS) or Alt-F (Windows) to exit the Enhanced viewer mode but leave

the Wipe mode on.

**19** Reset the Reference Sizing mode of the Sizing palette.

**20** Select clip 07.


The clip colors are already a good match for the rest of the timeline, but the shot is

too bright overall, which will affect the consistency of the post-clip grade.


**Lesson 7 Using Groups** **291**


**21** Label node 01 **Match** .

**22** Drag the Offset master wheel left to darken the shadows to the same level as the

reference clip. A good area to watch as you adjust the image luminance is the garage

ceiling, which should match in all shots.













**Lesson 7 Using Groups** **292**


##### **Intermediary Matching Between Clips**

At times, you’ll want to grade shots to show a gradual change in color or brightness

between clips. Doing so is not strictly a color match but rather an intermediary grade

designed to transition between clips with different looks without jarring a viewer’s

perception of the scene.


In this exercise, two clips captured at sunrise are intercut with media captured later in the

day. You will match the daylight clip between them and then grade the preceding clip to

suggest a natural change in sunlight throughout the sequence.

**1** Remove the timeline filter to show all clips.

**2** Shift-click clips 22 to 25 to select them.

**3** In the viewer, enable Split Screen mode.

**4** From the dropdown menu in the upper left of the viewer, choose Selected Clips.

**5** Press Option-F (macOS) or Alt-F (Windows) to expand the viewer.


**6** In the split-screen viewer, ensure that clip 24 (lower left) is selected.

**7** Open the Node Editor and label node 01 **Match** .

**8** Drag the Gain wheel toward yellow until the color of the sky matches the skies in the

surrounding clips 23 and 25.


**Lesson 7 Using Groups** **293**


**9** Reduce the contrast in the adjustment controls until the window frames and furniture

have the same flat shadows.

**10** Copy the Match node grade from clip 24 and paste it into the first node of clip 22

(upper left).


To ensure a smooth transition between clips 21 and 23, you will reduce the severity of

the grade in clip 22.

**11** Open the Key palette and change the Key Output Gain to 0.600. The grade intensity is

nearly halved, and the original colors of the image now show through for a smooth

transition between the first and second halves of the scene.


**12** Press Option-F (macOS) or Alt-F (Windows) to exit the Enhanced viewer mode.

**13** Exit the split-screen viewer.


TIP You can use the Split Screen mode to review the contents of an entire

group by changing the mode dropdown menu to Current Group. Clicking any

grouped clip in the timeline will immediately display all other clips from the

same group in the viewer.


**Lesson 7 Using Groups** **294**


## **Automatically Tracking** **People and Objects**

The Magic Mask is a DaVinci AI Neural Engine-powered selection tool that can identify and

track human figures, physical features, objects, and surfaces based on user clicks in the

viewer. Additional track, paint stroke, and matte finesse controls allow for the refinement

of initial selections to achieve optimal results. The resulting masks can then be graded

using the standard primary palettes.


NOTE The following exercises require DaVinci Resolve Studio to complete.

##### **Tracking a Person**


When the AI Magic Mask 2 palette is active, the tool is primed to analyze the first thing you

click in the viewer. It primarily focuses on the immediate object or physical feature you

select and then broadens its interpretation as you provide it with more data.


In this exercise, you will familiarize yourself with the AI Magic Mask 2 palette interface and

track a person to grade the environment around them.

**1** Select clip 25.

**2** Create a new node after INPUT CST and label it **BG** .

**3** In the central palettes, open the AI Magic Mask 2 palette.





Adjustment Controls

|Col1|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
||||||
||||||



Matte Finesse


**Lesson 7 Using Groups** **295**



Click List


The AI Magic Mask 2 palette is made up of three areas:


 - **Toolbar** features tracking controls, click and paint stroke tools, and mask overlay.

 - **Click List** catalogs additive and subtractive clicks and displays their

collective tracks.

 - **Adjustment Controls and Matte Finesse** in the sidebar are used to refine the

resulting mask. Most of the matte finesse controls operate similarly to those in

the Qualifier palette.


**4** In the viewer, click the back of the man’s head.


NOTE If the blue click dot is not visible in the viewer, ensure that the AI Magic

Mask 2 palette is active and the onscreen control in the lower left corner of the

viewer is set to Qualifier.


**Click 1** is catalogued in the Click List of the AI Magic Mask 2 palette.

**5** On the right side of the Magic Mask toolbar, click Toggle Mask Overlay to review the

initial selection in the viewer.


**Lesson 7 Using Groups** **296**


With only a single click to guide it, the Magic Mask has highlighted the man’s hair.


To track his entire body, you will use another click to expand the Magic Mask’s analysis.

**6** In the viewer, click the man’s trousers. This will indicate to the Magic Mask that you

want it to focus on the full height of the man’s body (rather than just the head or

upper torso).


The mask overlay now includes the man’s entire body. With the subject identified, you

can now track the mask.


**Lesson 7 Using Groups** **297**


**7** In the Magic Mask toolbar, click Track Forward.


A blue line in the Overall Track row indicates a successful track.


To grade the scene around the man, you will need to invert the selection.

**8** In the Magic Mask toolbar, click Invert Mask.


**9** Click Toggle Mask Overlay to remove the red highlight from the viewer.

**10** In the Primaries palette, increase the Midtone Detail (100.00) to sharpen the beach and

enhance the ripples in the water.

**11** Use the Offset master wheel to brighten the background and drag the Offset color

wheel toward orange to emphasize the warm sunrise.


**Lesson 7 Using Groups** **298**


**12** Use Contrast and Pivot to create a dynamic look with enhanced shadows

and highlights.


Before


After


The Magic Mask has been trained on hundreds of video references of people and physical

features, making it exceptionally adept at reading the motion of the human body. In this

case, it was able to recognize a man as he walked into the shot, revealing his legs and arm.

In clips with multiple people, you can use additional clicks to mask and track each person

or use dedicated nodes for each individual.


**Lesson 7 Using Groups** **299**


##### **Masking Physical Features**

Often, you will want to focus on a specific feature of a person—for example, to correct the

color of a shirt or to perform skin/beauty work. This exercise demonstrates how you can

quickly isolate a face for grading and how you can improve the selection with the Magic

Mask’s adjustment controls.

**1** Select clip 06.

**2** Play the clip to review it.


Because of the dark environment and rapidly changing light in the garage, the man’s

face is underlit. You will use the Magic Mask to track and brighten his face.

**3** Return to the start of the clip.

**4** Label node 01 as **Face** .

**5** Open the AI Magic Mask 2 palette.

**6** In the viewer, click the man’s cheek.


**Lesson 7 Using Groups** **300**


**7** Click Toggle Mask Overlay to review the selection.


The selection is immediately successful—it has isolated the skin on his face, ear, and

neck while avoiding his hairline and clothes.


Let’s look closer at the mask edge to see if the selection can be further improved.

**8** Zoom in to the viewer to more closely observe the mask around his hairline

and forehead.


Although accurate, the edge is harsh and might stand out when you start grading.


**Lesson 7 Using Groups** **301**


The Magic Mask adjustment controls feature a Quality parameter that determines the

accuracy of the mask analysis. In cases where a garbage matte or rough

approximation will suffice, the Faster option will provide a quick result at the expense

of quality. When precision is crucial, Better is the preferred option, but it comes at the

expense of processing time and computational power.


**9** Click Better and wait a moment while the Magic Mask re-analyzes the subject.


The resulting mask is much improved. The edge of the mask is softened around the

hairline, ensuring a smooth blending of the grade. Even the eyelashes are included!


With the face successfully selected, you can proceed with the track.

**10** In the Magic Mask toolbar, click Track Forward.


When the track is finished, review the traveling mask.


**Lesson 7 Using Groups** **302**


**11** On the last frame of the clip, enable Highlight mode in the viewer.


Toward the end of the shot, the mask picks up too much of the man’s hair.


The Smart Refine parameter allows you to expand or contract a mask based on the

internal image analysis. Smart Refine will prioritize preserving edges that it is certain

are part of the subject while reducing/expanding areas in which it has “low

confidence.”

**12** Reduce Smart Refine (15.0) and retrack the Magic Mask.


The resulting mask is contracted around the hair, while preserving the “high

confidence” edge around the rest of the face.


**Lesson 7 Using Groups** **303**


**13** Disable Highlight mode in the viewer.

**14** Click Toggle Mask Overlay to hide the mask in the viewer.


TIP To remove the blue dot from the viewer, choose Off from the onscreen

dropdown menu, or press Shift-~ (tilde) or the key to the left of 1 on

your keyboard.

Another quick method for removing the Magic Mask onscreen overlays is to

open a different tool in the central palettes, such as the Curves or

Color Warper.


**15** To brighten the man’s face, drag the Gamma master wheel (0.02) to the right.


TIP Another unique parameter in the Magic Mask’s finesse controls is

Smoothing, which is designed to reduce mask edge jitter in areas of low

confidence. Jitter is most likely to occur in masks with rapid movement or a

high volume of edge detail, such as loose clothes blowing in the wind or

curly hair. Increase Smoothing to analyze the surrounding frames of a mask

and produce a more static average of the selection on any given frame.

##### **Tracking an Object**


In addition to people, the Magic Mask has been trained on thousands of objects and

surfaces—from vehicles, buildings, and skylines, to animals, clouds, and flames—it boasts

an extraordinary recognition rate. You can use the Magic Mask to emphasize products in

commercials, perform sky replacement, enhance production design, or any number of

creative applications that we haven’t even thought of yet!


In this exercise, you will track an object with a high level of detail and use the matte finesse

controls to refine the result.

**1** Select clip 15.

**2** Create a new node after the INPUT CST and label it **Balance** . Use the Primaries palette

to brighten the image and remove the magenta tint from the highlights.


**Lesson 7 Using Groups** **304**


**3** Create a new node after the Balance node and label it **Car** .

**4** Open the AI Magic Mask 2 palette.

**5** In the viewer, click the car’s rear wheel.

**6** In the Magic Mask toolbar, click Toggle Mask Overlay.


The wheel alone is highlighted. To indicate that you wish to capture a whole object, you

should click a surface on the opposite side of it.

**7** In the viewer, click the car hood.


**Lesson 7 Using Groups** **305**


**8** If satisfied, click Track Forward.


Otherwise, click the bin icon in the click list and try again with another click. If needed,

make additional clicks to further improve the car selection in the viewer.


The resulting mask is satisfactory but features hard edges. As in the previous exercise,

you can opt to change the Quality parameter to Better to instantly improve the result.

However, due to the computational intensity of the Better setting, you may opt to

enhance the Faster quality mask with the help of the matte finesse tools instead.

**9** In the Matte Finesse controls, drag the Blur Radius (10.0) to soften the edge

of the mask.

**10** Drag the In/Out Ratio (20.0) to slightly expand the mask blur outward.

**11** Increase Post Filter (5.0) to reintroduce some of the edge detail from the original

video source.


**12** Click Toggle Mask Overlay to remove the red highlight from the viewer.


With the selection complete and the overlay hidden, you can resume the

grading process.


**Lesson 7 Using Groups** **306**


**13** In the Primaries palette, drag the Gamma master wheel right (0.02) to brighten the car.

**14** Increase the Contrast (1.100) and drag the Pivot left (0.100) to emphasize the shine on

the car body.

**15** Raise the Midtone Detail (50.00) to sharpen the headlights, rims, and reflections.


Before


After


With a few clicks, you were able to isolate the car and emphasize it against its environment

using standard primary grading controls. Notice how the Magic Mask tracked the car even

with dramatic fluctuations in light. The Magic Mask goes beyond chroma and luma keying

when identifying a selection and can follow objects through dynamic changes in

environments, strong shadows, and even motion blur.


**Lesson 7 Using Groups** **307**


NOTE You may have noticed that the colors and contrast in the viewer are

dimmed when viewing the Magic Mask overlay. This is because the Magic Mask

operates independently from any color management or upstream node grades.

This allows it to produce consistent results regardless of how the image signal is

treated, ensuring that it does not need to be re-analyzed and re-tracked when

adjustments are made to upstream nodes.

##### **Blurring the Background to Draw Attention**


Another way to draw attention to an object or person in the foreground is by blurring, or

defocusing, the background. The Defocus Background effect produces a blurring pattern

reminiscent of an optical lens, making it more aesthetically pleasing than a standard blur

effect when used in shot composition.


Gaussian Blur


Defocus Background effect


**Lesson 7 Using Groups** **308**


**1** Select the Car node.

**2** Press Option-O (macOS) or Alt-O (Windows) to create an Outside node, and label it

**Defocus BG** . The Defocus Background effect relies on matte data to apply the focus

blur. Reusing the Car’s track key gives you a quick starting point for the scene matte.

**3** In the Effects panel, under Resolve FX Stylize, find the Defocus Background effect and

drag it onto the Defocus BG node.


The Defocus Background effect classifies the white sections of the matte as the

foreground and the black sections as the background. To apply the effect correctly,

you must invert these values.

**4** Under Adjust Mask, select Mask Invert.

**5** In the Defocus Background settings panel, under Effects, reduce the Blur to 0.400.


Due to the motion blur on the road, the result already looks satisfactory, but if you

wish to be more precise with the focal length of the shot, you can isolate the blur to

just the skyline in the background.

**6** Open the Window palette.

**7** Create a Linear window and label it **Skyline** .

**8** Place the linear window on the top half of the frame, ensuring that the bottom line

matches the slant of the wall in the background.

**9** Open the Tracker palette.

**10** Change the Tracker to Frame mode and manually keyframe the linear window to raise

slightly with the wall toward the end of the clip.


As with other tools and effects that generate mattes, you can reuse the tracked Magic

Mask key data as much as needed throughout the node tree, modifying the key to suit the

needs of specific grades and effects as you do so.

##### **Fixing Difficult Tracks**


Despite its great accuracy and intuition, the Magic Mask is also designed to work with

difficult-to-track data. It’s possible to exclude sections with subtractive clicks, track one

frame at a time, and use paint strokes to add or remove mask sections in a frame. This

exercise requires you to combine some of these techniques to produce a clean mask.

**1** Select clip 09.


This clip has been successfully matched to the rest of the Garage sequence, but

there is still a green dominance in the darker elements on the man—specifically,

his hair and suit.


**Lesson 7 Using Groups** **309**


**2** Create a new node and label it **Masks** .

**3** Open the AI Magic Mask 2 palette.

**4** In the viewer, click the man’s hair.

**5** Click Toggle Mask Overlay to review the selection.


As expected, the Magic Mask has identified and selected his hair.

**6** Click the man’s shoulder to include his suit.


With this broader input, the Magic Mask assumes that you want to track the entire

man. You will use subtractive clicks to fine-tune the selection.

**7** In the Magic Mask toolbar, select Subtract Click.

**8** Click the man’s white shirt.

**9** Click the man’s face.


**Lesson 7 Using Groups** **310**


The highlight is removed from his shirt and face, resulting in clear selections on just his

hair and suit. Note that subtractive clicks are indicated with red dots.

**10** In the toolbar, click Track Forward.

**11** When the tracking is complete, drag the playhead to review the accuracy of the mask.


The mask is mostly successful but may appear incomplete around his sideburns

halfway through the clip.


As this only affects a few frames, it makes sense to paint in the missing data manually.

**12** Zoom in on the man’s face in the viewer.

**13** In the Magic Mask toolbar, select Add Paint Stroke.


In the viewer, your cursor will adopt a green paintbrush overlay.


**Lesson 7 Using Groups** **311**


**14** Hold Command (macOS) or Ctrl (Windows) and drag in the viewer to resize the brush.

Alternatively, use the Brush Size slider in the Magic Mask toolbar. Aim to match its

diameter to the detail of the area you will select.

**15** With the brush size set, click in the viewer to select the man’s sideburns.


**16** When finished, press the Left Arrow and Right Arrow keys to navigate to previous and

following frames and fill in the same area in every frame.

**17** Click Toggle Mask Overlay to remove the red highlight from the viewer.

**18** Use the Primaries palette to slightly darken the shadows with the Lift master wheel

and gently raise the blue Lift bar to match the color of the suit in the preceding clip.


Masking a person’s motion using traditional vector shape-based methods can take hours

or days. Typically, this involves breaking up the human figure into a dozen dedicated

windows and animating them to match the person’s movement. The Magic Mask produces

traveling mattes instantly, allowing you to focus more of your time on the color

grading process.


NOTE An earlier version of the Magic Mask allows you to select objects, people,

and physical features with the use of strokes. It is still accessible in the AI Magic

Mask 2 palette via Options > Legacy Object Mask.


**Lesson 7 Using Groups** **312**


## **Creating a Unifying Look Using** **the Post-Clip Group Level**

The post-clip group level is the point in the video pipeline where you will design and apply

creative grades on a scene-by-scene basis. This can occur after corrections have been

made on the pre-clip and clip group levels or, inversely, at the very start of the grading

process to establish the final look of the project before tweaking the upstream

corrector nodes.


When developing looks, other members of the creative process, such as the director and

cinematographer, usually get involved to discuss the film’s aesthetic and narrative needs.

##### **Applying a Post-Clip Grade with** **an External Reference**


In this exercise, you will work with a reference image that a client has shared with you. You

will import it into the gallery as a still and use it for visual comparison.

**1** Filter the timeline to show only the Garage group clips.

**2** Switch the Node Editor to Group Post-Clip mode.

**3** Select clip 07. This is the hero shot you will use to grade the rest of the group.

**4** To import an external reference image, right-click in the Gallery and choose Import.

**5** In your file browser, navigate to the BMD 20 CC - Project 03 folder and open the

References subfolder.


If you don’t see any images in the folder, ensure that your browser window is set to

identify all files rather than just the default .dpx format files.

**6** Select the **FK_Bridge_Reference.png** image and click Import.


**Lesson 7 Using Groups** **313**


**7** Double-click the still to wipe it in the viewer.


Clients often use visual references from existing film and television properties, as well

as other art forms, such as photography and painting, to communicate their desired

looks for a project. In this case, the highly stylized reference image points toward a

high-contrast, saturated scene with neutral shadows and cool midtones.


First, let’s match the contrast and cold look of the reference.

**8** Create a serial node before OUTPUT CST and label it **Dark Blue** .

**9** In the Curves palette, drag the master curve black point across the bottom of the

graph until the shadow under the car is almost pitch black. Add control points to gently

increase contrast by raising the upper midtones.


**Lesson 7 Using Groups** **314**


Recall the message about breaking rules in Lesson 5. When designing a look, it’s

perfectly acceptable to make more aggressive grading adjustments since your primary

focus is no longer the total preservation of the video signal but rather the creation of a

look you find aesthetically pleasing.


Still, to prevent the shadows from being crushed completely, you can offset the lowest

point of the signal while gently rolling off the bottom of the waveform trace.

**10** In the Curves palette, drag the Low Soft slider until you can see a small gap between

the bottom of the trace and the waveform graph. This will allow you to achieve deep

shadows and high contrast without losing actual detail.

**11** In the Primaries palette, drag the Gamma wheel toward cyan-blue to create a strong,

cool tone that matches the reference image.


You can address the oversaturated blue headlight reflections on the floor using the

Lum Vs Sat curve.

**12** In the Curves palette, open the Lum Vs Sat HSL curve.

**13** Click the white swatch under the curve grid to generate an anchor next to the

rightmost point of the saturation graph. The area between the two points represents

the most saturated areas of the frame.

**14** Drag down the rightmost point until the reflections are not overly saturated.

**15** Drag the white swatch anchor point left to expand your target region. If necessary,

create a new adjustment point and use it to refine the section of the frame you

are desaturating.


**Lesson 7 Using Groups** **315**


The overall look of the scene is set. You can now place a second node to enhance the

garage’s red columns and pipes.


It’s uncommon to create secondary grades in post-clip group node graphs, but it can

work when a scene has a consistent color scheme or frame composition.


Previously, you saw that you could get a better secondary grade result if you used the

original RGB signal of a clip instead of a heavily graded and contrasted one, like the

Dark Blue node. However, in this instance, the graded node is helping to contrast the

red pipes against the originally warm scene. Making a secondary selection based on

the cool grade will produce a cleaner red key with minimal impact on the walls and the

actor’s skin tone.

**16** Create a new serial corrector node and label it **Red Pipes** .

**17** In the HSL curves, open the Hue Vs Sat HSL curve.

**18** Click the red swatch at the bottom of the palette and increase the Sat by 50% to

enhance the reds.

**19** Open the Hue Vs Lum HSL curve, click the red swatch, and reduce the Lum by 50%.

This makes the reds denser, matching them more closely to the dark environment.


**Lesson 7 Using Groups** **316**


**20** Create a Vignette node after the Red Pipes node for a moodier environment and to

draw attention to the action in the center of each shot.


TIP To bypass the entire node tree within a specific grade level, press

Option-D (macOS) or Alt-D (Windows). Doing so will leave your other node

levels active so you can assess the changes you’ve made within the

current clip level.


In addition to importing still images, you can export a frame in various image formats

for client reference and review.

**21** Go to File > Export > Current Frame as Still and export the frame from clip 07 in the

PNG format.


Occasionally, a post-clip grade will emphasize or reveal tonal and color inconsistencies in a

sequence of clips. In such cases, you should return to the Clip mode of the Node Editor to

make further adjustments.


**Lesson 7 Using Groups** **317**


##### **Adjusting Clips After a Post-Clip Grade**

In this exercise, you will return to the Clip mode to apply an effect to the hero shot and

then fix a discrepancy that was revealed in one of the shots on the timeline.

**1** With clip 07 still selected, return the Node Editor to Clip mode. You will apply an effect

to make the headlights more dramatic.

**2** Create a second node and label it **Headlights** .

**3** Open the Effects panel.

**4** Find the Resolve FX Light category and drag the Aperture Diffraction effect onto the

Headlights node.


The result is an optical effect that mimics the diffraction around light sources. The

settings in the Effects panel allow you to refine the pattern, intensity, and color of

the diffraction.


**5** Under Aperture Controls, change the Iris Shape to Square.


TIP In the Output category of the Aperture Diffraction settings, change Select

Output to Diffraction Patterns Alone to get a clearer view of the light patterns

as you adjust the settings. Change the output back to Final Composite to see

the result superimposed on the original image.


**6** Under Compositing Controls, increase the Brightness to 0.600.


**Lesson 7 Using Groups** **318**


**7** Increase the Colorize value to 0.200 and use the swatch underneath to change the

color to purple.

**8** To reduce the effect intensity, expand the Global Blend parameter at the bottom of the

settings and set Blend to 0.700.


This simple effect dramatizes the sequence’s final shot as the car drives away. A variety

of light-based plug-ins in the Effects panel can similarly help you stylize your shots and

make features “pop” in subtle or exaggerated ways.


Next, you will check the remainder of the garage sequence to ensure that all

shots match.

**9** Navigate the timeline and check the clips for consistency.


You can see that the lower midtones in clip 06 are substantially bluer when compared

to the environments in clips 05 and 07. Clip 06 is also darker, making it difficult to see

the man’s face.

**10** Select clip 06.


**Lesson 7 Using Groups** **319**


**11** Right-click clip 07 and select Wipe Timeline Clip.


**12** Label node 01 **Match** .

**13** Switch the Primaries palette to Log Wheels mode and drag the Shadow master wheel

right to reveal more detail in the background and on the man’s face.

**14** Drag the Shadow wheel control point toward orange.


The overall blue dominance of the shot is reduced, and the man’s face is more visible.


**15** Disable Wipe mode in the viewer.


The convenience of the group grading workflow is that no single stage or node is

permanent. It’s easy to jump between different group modes and tweak them as

needed, all while continuously seeing the final output in the viewer.


**Lesson 7 Using Groups** **320**


## **Working with Lookup Tables**

A Lookup table, or LUT, is a digital file containing a number array for image processing

operations. In color grading, these operations are most commonly used to process an

image’s incoming tone and color pixel data to return a set of new, precalculated values.


LUT application ranges from media color management and monitor calibration to dailies

processing and creative grading. On the surface, LUTs may appear to behave similarly to

stills, CDLs, and grade plug-ins. However, rather than using formulas or tools to transform

colors, the values in LUTs are predetermined. The reliability of their results and their

near-universal software (and hardware) support make LUTs very popular industry-wide for

on-set monitoring, calibration profiles, and show looks.


1D LUTs (commonly .lut) control a single value of the image and are generally utilized as

gamma transformers. 3D LUTs (commonly .cube) map hue, saturation, and brightness

while offering varying levels of precision based on point value. 17 x 17 x 17 cubes are

recommended for monitoring and calibration, while 33 x 33 x 33 (and 65 x 65 x 65) cubes

are more appropriate for grading.


In the next set of exercises, you will import and apply a LUT, generate and export your own

LUT, and learn to work with emulation LUTs.

**1** Change the Clips timeline filter to display only the Highway group.

**2** Select clip 02. You will apply a look to these outdoor shots using a LUT.


**Lesson 7 Using Groups** **321**


NOTE A LUT designed to encapsulate the look of a project (or sections of it) is

known as a show LUT. They can be used for generating dailies, as a starting

point for the grade, or as part of the final grade composition.


**3** In the Node Editor, switch to Group Post-Clip mode.

**4** Create a serial node before the OUTPUT CST and label it **LOOK** .


For a LUT to be accessible in DaVinci Resolve, it must first be placed in a folder that is a

recognized LUT location. DaVinci Resolve features a default LUT folder, but you can

specify custom LUT locations in the Preferences.

**5** Open the Project Settings.

**6** In Color Management, scroll down to the Lookup Tables section.


The Lookup Tables parameters allow you to load LUTs to different points of the signal

processing pipeline. You can map videos before and after they enter the Node Editor

pipeline, load a color calibration profile for your video monitor, and change the

operating color space of the viewer and scopes.

**7** Click Open LUT Folder to reveal the default Davinci Resolve LUT folder location in your

file browser.

**8** In the LUT folder, create a new subfolder called **Colorist Guide** . (You can delete it after

you have completed the exercises in this book.)

**9** Open another file browser window, and in BMD 20 CC - Project 03, find the LUTs subfolder.

**10** Drag **Highway_DWGtoDWG.cube** into the Colorist Guide subfolder.


LUTs only work correctly when their specific input and output conditions are met. In

some cases, these conditions are specified in the LUT text when viewed in a word

processor; in others, the conditions are indicated in the LUT name. The suffix

“DWGtoDWG” in this filename indicates that the LUT was created in a DaVinci Wide

Gamut environment (input to output).


**Lesson 7 Using Groups** **322**


**11** Return to the Project Settings window and click Update Lists to refresh the LUT folder.


NOTE You can load your own LUT storage locations for more precise LUT

management. In DaVinci Resolve > Preferences, open the System controls and

select the General settings. Use the Add and Remove buttons under the LUT

Locations table to load custom LUT folders.


Before leaving the Project Settings, you can also address how LUTs handle

interpolation. Due to the finite number of values represented in a LUT, parts of a

source signal might be approximated during conversion, which can limit the final

grade. When a LUT is generated in a lower bit-depth format and applied to high

bit-depth (or raw) media, it can result in posterization (banding) in areas with soft

gradients. Changing the interpolation method can reduce such artifacts in the image.

**12** Set “3D lookup table interpolation” to Tetrahedral. This will ensure that unsupported

values in the LUT array are smoothly interpolated.


**13** Click Save to close the Project Settings.

**14** In the interface toolbar, open the LUTs panel.


The panel’s sidebar features the contents of the DaVinci Resolve LUTs folder, including

the Colorist Guide subfolder you just created. When you mount custom LUT locations,

these will also appear in the sidebar. If Live Preview is enabled, hovering over the LUT

thumbnails will give you a preview of their operation.


**Lesson 7 Using Groups** **323**


Notice that many of the LUT names indicate their color mapping. If you check the

Blackmagic Design folder, the LUTs have names like “Blackmagic 4.6K Film to Rec709,”

indicating these are transform LUTs intended for raw or log BMD footage for

conversation to the Rec709 viewing and deliverable standard.

**15** Open the Colorist Guide subfolder.

**16** Drag Highway_DWGtoDWG.cube onto the LOOK node.


This alters the appearance of both clips in the Highway group, giving them a densely

saturated evening look.


You also have access to LUTs in each node’s contextual menu.

**17** Right-click the LOOK node and navigate to LUT. Here, you can see the same list of files

as in the LUTs panel. Custom LUT locations will also appear in this contextual menu.


Now that you understand how to upload and apply LUTs that have been shared with you,

you will next learn how to generate your own LUTs to share with others for use in

DaVinci Resolve, third-party applications, and monitoring hardware.


**Lesson 7 Using Groups** **324**


##### **Developing a Monitoring LUT**

Generating a LUT file is a straightforward process. However, ensuring the LUT operates

correctly in the intended media color space and looks consistent across all shots is a

different matter.


First, you must decide on the color space transform of the LUT. If you create a look with

active input and output CST nodes, that transform data will be baked into the resulting

LUT, and you will not need those CSTs when applying the LUT. Common starting points for

LUTs include camera color space profiles, wide gamut working spaces, and Cineon Log.

**1** Remove the timeline filter to show all clips.

**2** Select clip 03.

**3** In the Node Editor, switch to Group Pre-Clip mode.


The INPUT CST maps the signal from Blackmagic Design 4.6K Film Gen 1. If you leave

this enabled, this transform will be baked into the LUT, making the LUT applicable only

to other Blackmagic Design 4.6K Film Gen 1 profile clips. This is ideal if you are creating

a monitoring LUT or you anticipate that all the media in a project will come from the

same camera.


If you wanted to generate a LUT for another source color space (for example, Cineon

Film Log or ARRI Wide Gamut), you would need to change the input color space

mapping in this CST from the camera color profile to that standard.

**4** Leave the INPUT CST as it is.

**5** In the Node Editor, switch to Group Post-Clip mode.


Similarly, the OUTPUT CST determines the color space to which your footage will be

transformed. If you aim to create looks that can be output to a specific monitor or a

wider gamut than Rec.709, you’ll want to change the CST’s output color space.

**6** Leave the OUTPUT CST as it is. It will operate correctly in a Rec. (Scene) project and

produce results consistent with your DaVinci Resolve viewer on a Rec.709 monitor with

a gamma 2.4 curve. This is due to the OOTF transformation occurring in the Rec.709

(Scene) gamma within the CST.


You are now ready to create a Rec.709 monitoring LUT for Blackmagic Design

4.6K footage.


**Lesson 7 Using Groups** **325**


**7** Create a new serial node before the OUTPUT CST node and label it **Contrast** .

Technically, this node can be placed at any point in the node tree between the input

and output CSTs. The benefit of placing it here is that it will also apply a group grade to

the other clips in the Office group.


The next factor in creating a LUT is identifying and maintaining the middle gray.


Every camera sensor and working color space has its own middle gray value around

which you can consistently adjust contrast. Middle gray is important in photography

because it tends to be the value to which cinematographers expose the scene’s

subject, which is usually a person, though it can also be an environment or inanimate

object. Maintaining middle gray ensures that the subject looks its best no matter how

dramatic the contrast and colors in the grade are.


Skin tone and middle gray swatch on the ColorChecker chart


One parameter that allows you to work directly around middle gray is the Pivot control

in the Primaries palette. If you know the middle gray value of a color space on the

1.000 index, you can enter it into the parameter’s numeric field and drag the Contrast

parameter to manipulate the dynamic range around it.


Another method of identifying middle gray is to remove the contrast and saturation in

a shot in the active color space and mark the resulting spike in the Curves palette.


**Lesson 7 Using Groups** **326**


**8** In the left palettes, open the High Dynamic Range Color Wheels palette. You will

examine this palette more closely when you start working with RAW media in Lesson 9.

For now, you will use its internal color management (by default set to the project’s

timeline color space, DaVinci Wide Gamut) to identify the clip’s middle gray.


**9** Under the Global wheel, set the Sat parameter to 0.00.


**10** In the Adjustment Controls at the bottom, set the Contrast to 0.000.


The Contrast pivots around DaVinci Intermediate’s middle gray, meaning that reducing

it to 0 produces the project’s middle gray. This applies to the Blackmagic Design 4.6K

Film media because it is sandwiched between two CSTs that are mapping to and from

DWG. If you wanted to change the middle gray standard that you are trying to extract,

you could do so by clicking the HDR palette Options menu and choosing a different

Gamma, such as ARRI LogC4.


**Lesson 7 Using Groups** **327**


The middle gray value is reflected in the scopes, but you can also reveal it in the Curves

histogram graph.

**11** In the Curves palette options, choose Histograms > Output. The Curves histogram will

display the output signal of the node, meaning you will now only see the gray frame

represented as a spike in the graph.


DaVinci Intermediate middle gray in the Curves palette histogram


DaVinci Intermediate middle gray in the waveform scope


**Lesson 7 Using Groups** **328**


NOTE The middle gray may appear a little brighter than expected in the

scopes due to the OUTPUT CST at the end of the node tree. If you were to

(temporarily) disable the CST node, you would find the middle gray around

0.336 for Davinci Intermediate. In the scopes graph, the spike will be in the

correct position whether you have the CST node enabled or not.


**12** Hold Shift and place a control point on the custom curve directly over the middle

gray spike.


Having marked the middle gray, you can now remove the gray frame.

**13** In the HDR palette, click the Reset All arrow in the header to bring back the

original image.


You can now build contrast around the middle gray control point.

**14** In the Curves palette, click the Options menu and choose Editable Splines.

**15** Use the Bézier handles on the control points to build custom contrast in the image.

Drag down the white point if the highlights get overpowered and pivot (but don’t

move) the middle gray point to raise visibility in the upper midtones.


**Lesson 7 Using Groups** **329**


NOTE In the industry, this is known as an s-curve and is commonly used as a

shorthand for Bézier-based contrast.


Ordinarily, you could build satisfactory contrast with just these two points and a

constant middle gray, but if you are working with consistently light or dark footage,

you can also opt to offset the overall luminance of the signal.

**16** In the Primaries palette, drag the Offset master wheel right to lighten the scene to

your liking. Keep tweaking the curve’s control points to refine the contrast.


NOTE Another way to find the middle gray of a color space is in the Fusion

page. Create a Background node with Red, Green, and Blue values set to 0.18,

and use a Color Space Transform to map it from linear to any camera or color

space standard you need. Hovering over the gray frame in the viewer will give

you numeric readouts in the status bar at the bottom of the page, which you

can input into the pivot parameter in the color page.


Third-party plug-ins can also help you quickly determine middle grays in

DaVinci Resolve. Another common approach is to use the middle gray swatch

in color charts as a reference point.


To adjust the colors, you can continue to work in the Curves palette around the same

middle gray or create a new node for a different approach to the signal treatment.

When generating a LUT, all your primary color grades will be compounded, no matter

how many nodes you use. Secondary and keyframed grades (like the qualifier, Power

Windows, tracker, Magic Mask, etc.) will be ignored during LUT generation.

**17** Create a new serial before the Contrast node and label it **Look** .


This node order will result in less saturated shadows.

**18** Drag the Gain color wheel toward red for dramatically warm light with a wide overlap.

**19** Drag the Lift color wheel toward cyan for a cooled office look.


**Lesson 7 Using Groups** **330**


**20** Go to the ColorSlice palette and increase the global Density parameter for deeper,

more saturated hues.


Before


After


If necessary, return to the Contrast node and further tweak the final look.

**21** When finished, right-click clip 03 and choose Generate LUT > 33 Point Cube.


**22** Save it as **Office_BMDtoRec709.cube** .


TIP You can generate looks in the Film Look Creator effect and export them

as 3D LUTs. At the top of the settings, select 3D LUT Compatible to ensure only

parameters that can be retained in a lookup table remain available.


**Lesson 7 Using Groups** **331**


**23** In your file browser, place the Office_BMDtoRec709.cube file in the Colorist Guide

folder you created earlier. If you no longer have the folder open, you can find it in the

Project Settings, within the Color Management section, by clicking the Open LUT

Folder button.

**24** Click clip 14.


Your office-look LUT was developed with the two CST conversions already in place.

That means they will be baked into the LUT values, and applying them between the

two existing CSTs will result in a double-mapping of those values.

**25** Disable (or delete) the two CST nodes in the Node Editor.

**26** Create a new node.

**27** Right-click the node and choose LUT > Colorist Guide > Office_BMDtoRec709.cube.


In the viewer, the image is transformed from Blackmagic Design 4.6K Film to Rec.709

with the baked-in red/cyan look. This is how you can generate monitoring LUTs for

cinematographers to act as guides for the final grade while shooting or convert

entire timelines of raw media to a preliminary look when generating proxies for

online workflows.


Before


After


**Lesson 7 Using Groups** **332**


NOTE LUTS can also be applied to clips in the media pool via the contextual menu.


In addition to using LUTs to modify individual clips or groups, you can apply them on a

timeline basis when you have an overarching show look, to review different color

management deliverable options, or to assess how the project will look after printing.
## **Using the Timeline Level**


The Timeline level is available in the Node Editor whether or not you use group workflows.

As the name implies, adjustments made at this level affect every clip on the timeline

uniformly. This function can be useful for broad image property or optical changes such as

color space transforming, gamma/gamut mapping, halation, vignettes, inserting film grain/

analog video effects, and so on.


In the next few exercises, you will apply an emulation LUT, develop an analog video look,

and overlay data burn-ins that will make it easier to keep track of timecodes and clip names

during project review and feedback.

##### **Applying an Emulation LUT**


So far, you have worked with creative and monitoring LUTs. Another common application

for LUTs is film stock emulation. In the beginning, film emulation LUTs were almost

exclusively used by colorists to check how a project would look after it was printed on film

stock. Over time, film emulations LUTs also began being used creatively to replicate the

look of film in digital deliverables.

**1** In the LUTs panel, open the Film Looks folder.

**2** Change the LUTs panel to List view so you can more easily read the LUT names.


**Lesson 7 Using Groups** **333**


The folder contains a list of popular Fujifilm and Kodak film stocks. Their naming

convention describes their output color space, the film stock variant, and the white

balance. Rec709 Kodak 2383 D65 is an emulation of the Kodak 2383 film stock with the

standard D65 white balance intended for Rec.709 monitoring/delivery. As can be

observed in the text of the LUT file, all these LUTs anticipate Cineon Film Log as the

input transfer function.


**3** Select clip 18.

**4** Switch the Node Editor to Timeline mode.


By default, the Timeline Node Editor appears without node 01, which serves as a useful

visual reminder that this stage of the grading workflow is optional and, if used

unintendedly, can significantly impact the entire timeline.

**5** Press Option-S (macOS) or Alt-S (Windows) to create a new serial node already

connected to the source input and node tree outputs.


The blue outline around the node is another visual reminder that you are not in any of

the standard Node Editor levels.


To prepare the signal for the emulation LUT, you need to first convert it to

Cineon Film Log.

**6** Add a Color Space Transform effect to the node.

**7** Set the Input Gamma as Rec.709. This is the gamma (transfer function) the signal was

mapped to in the Group Post-Clip layer.


**Lesson 7 Using Groups** **334**


NOTE The gamma has been remapped several times at this point. This is

acceptable for demonstrative purposes, but you should strive for cleaner

workflows in your own projects. If you are aware that you will be using a LUT

(emulation or otherwise) in an upcoming project, you should build a workflow

that accommodates it without compromising the video signal. This can mean

incorporating the LUT into the working color space section of the node tree or

using a single output CST to configure the entire project to the deliverable

standard in the Timeline Node Editor with the LUT placed before it.


**8** Set the Output Gamma to Cineon Film Log.

**9** Add a new node after the CST.

**10** From the LUTs panel, drag the Rec709 Kodak 2383 D65 emulation LUT onto the node.

**11** Select both nodes and turn them into a compound node called **KODAK LUT** .


You can now navigate up and down the timeline and preview how the emulation LUT

affects the footage. You will notice that some clips look better than others. This is

because you had already started grading some of the scenes without considering how

they would look after printing. This is why emulation LUTs (and any LUTs that will be

retained in the final grade) are usually applied before primary passes.

**12** Bypass (or delete) the KODAK LUT node to prepare for the next exercise.


TIP You can combine film emulation LUTs with the Film Grain effect (in the Resolve

FX Film Emulation category) to achieve the physical look of celluloid film. It comes

with a variety of film stock presets (8 mm, 16 mm, 35 mm) as well as a collection of

grain parameters for optimal customization on a timeline or clip-by-clip basis.

In the Advanced Controls, you can enable “Animate on Every Refresh” to force the

grain to move as you grade, giving you an even more accurate representation of

the final look as you work on each clip.


Next, you will look at another form of emulation that re-creates the look of analog video.


**Lesson 7 Using Groups** **335**


##### **Creating an Analog Video Look** **on an Entire Timeline**

Artificial film grain and analog video artifacts can be added to digital media for a variety of

reasons. In some cases, the film should look outdated as a component of the storyline

(such as flashbacks, home movies, found footage, and so on). Film grain and damage can

also add realism to shots with artificially imposed elements or CGI graphics by making

them appear to have been captured on tape or celluloid film. Finally, film grain and

damage are often an aesthetic choice.


NOTE This exercise requires DaVinci Resolve Studio to complete.


You will continue to work in the Timeline mode of the Node Editor.

**1** Create a new node and label it VHS.

**2** Open the Effects panel.

**3** Find the Resolve FX Texture category and drag the Analog Damage effect onto

the VHS node.

**4** Press Shift-F to expand the viewer and improve access to the Analog Damage

settings panel.


The top of the panel features a preset menu with a collection of common analog

looks—B&W and color television transmissions through the decades, VHS, and so on.

Beneath, individual parameter controls allow you to adjust a wide variety of damage


**Lesson 7 Using Groups** **336**


components, such as vignetting, noise, scan lines, screen curvature, foot jitter, and

many others.

**5** Set the preset to Old VHS.

**6** Under Broadcast Signal, reset Detail Loss to 0.000 for a clearer image.

**7** Under Scan, deselect Adjust CRT Framing to remove the horizontal and vertical

frame lines.


Before


After


**8** Click Play to review the result.


All the clips on the timeline are impacted by the VHS look.

**9** Press Shift-F to exit the full-screen viewer.

**10** Before moving on to the next exercise, bypass the VHS node. The Analog Damage

effect is processor-intensive, so it’s advisable to disable it until you are ready to export

the project.


**Lesson 7 Using Groups** **337**


##### **Adding Data Burn-In to the** **Viewer and Final Video**

Another common feature usually applied on a timeline basis are data burn-ins, which can

include timecodes, clip metadata, or any variety of customized text and watermark

overlays. This feature works independently from the Node Editor and can be used in
program for editorial purposes, as well as in the render of a video for review and feedback.

**1** Choose Workspace > Data Burn-In.


The left side of the Data Burn-In window features a list of metadata elements that you

can superimpose over the video in the viewer. The right side of the interface changes

according to the selected parameter and allows you to adjust the text placement, font,

color, and so on.


The Project and Clip buttons at the top of the Data Burn-In window allow you to apply

data across the length of a timeline or on a single instance of a clip. This option can be

helpful for leaving instructional comments—for example, when communicating with

the audio or VFX departments about what needs to be done on specific shots.

**2** Select Record Timecode to display the timeline’s timecode in the viewer.

**3** Select Source Clip Name to display the name of each clip as it plays. Note that in this

case, because all the clips are sourced from a single flattened video file, they will all

have the same source clip name.


**Lesson 7 Using Groups** **338**


**4** Select Custom Text1, and in the Custom Text field on the right, type **PLEASE DO NOT**

**DISTRIBUTE** .

**5** In the Data Burn-In options, deselect Gang Render Text Styles. This will enable you to

modify the appearance of the data burn-in fields individually.


You will use the Custom Text field as a form of distribution protection for your video.

**6** Remove the black box behind the text by reducing the Background Opacity to 0.00.

**7** Increase the Text Size (140) to expand the warning to the width of the viewer.

**8** Reduce the Text Opacity (0.20).

**9** Reposition the text to the center of the viewer using the Position Y parameter.


The Data Burn-In window features around 30 default parameters. However, you can

access an even wider range of metadata elements via the Custom Text fields.

**10** Select Custom Text2.

**11** Type **%** . A dropdown list of fields appears, showing the contents of the Metadata panel.

**12** Start to type **codec** and press Enter to select Video Codec when it appears in the filter.

**13** Use the Position parameters to place the codec metadata to the right of the record

timecode under the source clip name.


TIP To apply an image watermark over a video, use one of the Logo options in

the Data Burn-In interface. You can import a custom image file and adjust its

opacity using the transform controls on the right.


**14** Close the Data Burn-In window.


**Lesson 7 Using Groups** **339**


TIP A quick way to remove data burn-ins from the viewer is to press the Reset All

icon in the upper right corner of the Data Burn-In window.


Data burn-ins can be extremely useful for quick and accurate communication between

departments and clients. Instead of describing clips visually, exact clip source names can

be used in feedback. Likewise, the precise timecodes ensure that your collaborators are

not using the generic timecodes of their video players (which usually lack frame data).

Frequently used burn-in layouts can be saved as presets in the Data Burn-In options menu.
## **Self-Guided Exercises**


Complete the following self-guided exercises in the Project 03 - The Long Workday SCD

timeline to gain more experience with groups, primary and secondary grading, and

creative grade construction. Note that these exercises are designed foremost for group

grading practice and not necessarily to produce a single cohesive color narrative on

the timeline.

##### **Home Group**


- In clip 02 of the Home group, use the Magic Mask to track the man while excluding his

coat. Invert the mask selection and use Lum Vs Sat to desaturate his surroundings.

- Create a post-clip group grade on the Home group. Import the **GC_Island_**

**Reference.png** image from the BMD 20 CC - Project 03 > References subfolder into

the gallery as a reference. Aim to create a light, warm look. Use HSL Curves to

emphasize the blue of the sky and water outside the windows.

##### **Highway Group**


- Match the shadows in clip 01 to clip 02.

- From the Resolve FX Light category, add the Lens Reflections effect to clip 01, and in

the Global Controls, change the reflection preset to Bokeh. Adjust the reflecting

elements until you have a string of faint, out-of-focus white bokehs at the bottom of

the screen. Then, append this node to clip 02.


**Lesson 7 Using Groups** **340**


##### **Office Group**


- Match the brightness of clip 03 to the other clips in the Office group.

- In clip 02, use the Magic Mask to track the man’s face and hands, and then use

adjustment controls to add contrast and detail to the man’s skin.

##### **Morning Group**


- Perform contrast and color matching on the clips in the Morning group using clip 02 as

the hero shot.

- In clip 01, use the Magic Mask to select the sea, and increase the contrast and midtone

detail to emphasize the ripples in the water.

- Create a post-clip group grade in the Morning group. Darken the shadows slightly to

add depth. Then use the Color Warper to gently tint the mountains red and warm the

atmosphere. Experiment with achieving this look in both the Chroma Warp and

Hue-Saturation grids. Compare them using versions and keep your favorite.


When you’ve completed these exercises, open the **Project 03 - The Long Workday**

**Commercial COMPLETED.drp** and review Lesson 07 Timeline COMPLETED to compare

your work with this “solved” timeline. If the media appears offline, click the red Relink

Media button in the upper left corner of the media pool and specify the location of the

Project 03 media on your workstation.
## **Lesson Review**

**1** True or False? A clip can belong to more than one group.

**2** Which group level is ideal for performing shot matching?

**3** Which Magic Mask parameter is ideal for removing matte jitter on flowing clothing?

**4** Where can you find the anticipated input color space of a LUT?

**5** How is data burn-in enabled?


**Lesson 7 Using Groups** **341**


##### **Answers**

**1** False. A clip can have only one pre-clip and post-clip Node Editor mode. Adding a clip

to a new group will remove it from any previous group it was in.

**2** Clip mode is ideal for performing shot matching since it will be unique to every clip.

**3** The Smoothing parameter analyzes the surrounding frames of a mask to produce a

more consistent matte when working with jitter-prone surfaces, such as flowing

clothing or hair.

**4** The input and output data of a LUT can sometimes be discerned from the naming

convention of the LUT file or from the text of the LUT itself.

**5** Choose Workspace > Data Burn-In.


**Lesson 7 Using Groups** **342**


### Lesson 8
# Adjusting Image Properties



Although the grade tends to be the

primary focus for a colorist, there are

also many optical and transformative

changes that can impact the narrative

and aesthetics of a project. Such

changes can include alterations to the

scaling and positioning of the frame,

noise reduction, and the animation of

grades over time.


Some of the tools required to achieve

these transformations can impact the

speed at which your computer is able

to play back the media on the timeline.

For this reason, it’s helpful to leverage

the automated (Smart) and manual

(User) render cache methods to get the

most efficient processing of clips and

nodes across the multiple cache levels

in DaVinci Resolve.



Time

This lesson takes approximately
2.5 hours to complete.

Goals

Understanding Timeline
Resolutions and
Sizing Palette Modes 344

Using Keyframes to
Animate Grades 355

Applying Noise Reduction 362

Optimizing Performance
with Render Cache 369

Self-Guided Exercises 378

Lesson Review 379


## **Understanding Timeline** **Resolutions and Sizing** **Palette Modes**

In the following set of exercises, you will address the variety of ways in which you can

impact the frame of your project in DaVinci Resolve 20. Specifically, you will change the

project resolution, reframe individual shots, and sample portions of an image at the

node level.

##### **Changing Timeline Resolutions**


In this exercise, you will change the project resolution to evaluate how secondary grades in

your timeline are impacted.

**1** Select clip 05 on the Project 03 - The Long Workday SCD timeline.


**2** In the Node Editor’s Clip mode, create a new node called **Vignette** .

**3** In the Window palette, apply the Vignette preset from Lesson 3 or create a new one.

Resize and reposition it to the man at the window.


**Lesson 8 Adjusting Image Properties** **344**


**4** Drag the Gamma master wheel left to darken the edges of the frame and then drag

the color wheel control point toward blue/cyan to give the room a cool atmosphere.


**5** Open the Project Settings and choose the Master Settings tab.


**6** Change the Timeline resolution to 3840 x 2160 Ultra HD, a standardized 4K resolution

with the same aspect ratio (1.77:1, aka 16:9) as 1920 x 1080 HD.


TIP When rescaling media to a higher resolution (for example, converting

1080p content to a 4K timeline), you can activate a high-quality upscaling

feature called Super Scale. To do so, select and right-click the lower-resolution

clips in the media pool and choose Clip Attributes. Within the Video tab, in the

Super Scale menu, choose 2x (or higher) to double the resolution. Doing so

will substantially improve the method by which the image is upscaled in

higher-resolution projects, though it is a processor-intensive operation that

may compromise real-time playback.


**Lesson 8 Adjusting Image Properties** **345**


**7** Click Save to exit the Project Settings.

**8** If the video appears zoomed in, press Shift-Z to fit the video frame to the viewer panel.


1920 x 1080


3840 x 2160


Note that the clip’s frame and positioning in the viewer have not changed. Additionally,

the vignette window is rescaled to the new resolution while maintaining its placement

relative to the clip frame. The only change is the new anchor handle length in the

center of the Power Window.


**Lesson 8 Adjusting Image Properties** **346**


This behavior is one of the most invaluable features of DaVinci Resolve when grading

and applying effects. The program is resolution-independent, allowing you to change

a project’s frame size and aspect ratio without affecting the positions of clips, images,

secondary grades, effects, and generators created on the cut, edit, Fusion,

or color pages.


TIP When working on vertical resolutions (for web deliverables), click “Use

vertical resolution” under the timeline resolution settings. In addition to

maintaining the positions of your timeline assets, this setting will reconfigure

the layout of the pages in DaVinci Resolve to optimize the panels for a

vertical viewer.


**9** Open the Project Settings and reset the Timeline resolution to 1920 x 1080 HD.

**10** Delete the Vignette node.


**Custom Resolutions and Aspect Ratios**

Under the Timeline resolution presets of the Project Settings, you may enter a

custom resolution with the aspect ratio of your choosing. Be aware that changing

the resolution or aspect ratio to a non-industry standard could mean that the

rendered video may not be playable on some projectors or video players. When

outputting to equipment that only recognizes standard video formats, it’s safer to

use a common (preset) resolution and apply custom blanking to change the aspect

ratio. In either case, the custom blanking will appear as black bars during playback.

##### **Reframing Individual Clips**


The Sizing palette becomes an increasingly versatile tool when you take advantage of

its sizing modes. These modes allow you to switch the sizing focus from clips to entire

timelines to individual nodes. In this exercise, you will rescale and reposition clips on

an individual and timeline basis.

**1** Continue to work on clip 05.

**2** Enter the Sizing palette and set the Zoom value to 1.500 to scale up the image.


**Lesson 8 Adjusting Image Properties** **347**


**3** Select clip 03.


Notice that clip 03 was not affected by the reframing of clip 05. In fact, every clip in the

timeline has remained unchanged because clip 05 was changed at the clip level (Input

Sizing) in the Sizing palette.

**4** Return to clip 05 and reset the Zoom parameter.

**5** In the upper right of the Sizing palette, choose Output Sizing.


**6** Set the Zoom value to 1.500 again.

**7** Click the other clips in the timeline to verify that they are affected by this change

in timeline scale.


Sometimes, rescaling makes sense on a timeline basis, such as when adapting media

to a different resolution. However, clip reframing still needs to be performed to

account for the visual content of each shot.


Let’s reframe shots 03 and 05 based on content.

**8** Change the Sizing palette mode back to Input Sizing.

**9** In clip 05, change Pan to 40.00 and Tilt to -30.00.

**10** In clip 03, change Pan to -240.00 and Tilt to 40.00.


**11** Switch between the clips to verify that they have retained their Output Sizing zoom but

adopted different pan and tilt values.


TIP When copying grades or stills, you can indicate if you want to include

color data, sizing data, or both in Mark > Keyframe Timeline Mode. This

setting can help streamline your workflow if you frequently copy clip data but

want to exclude resizing from the color grade (or vice versa).


**Lesson 8 Adjusting Image Properties** **348**


**12** Reset the Input and Output sizing data on clips 03 and 05.


NOTE Output sizing is also commonly used to adapt footage with a different

aspect ratio to a new standard—for example, 4K DCI will appear to have

horizontal blanking (black bars) in a 4K UHD timeline. Output sizing can be

used to quickly fill the frame of the video.


These changes used two Sizing palette modes—Input and Output. Previously, you also

rescaled and reframed a wiped still using the Reference Sizing mode.


The full list of sizing modes and their impact on the image is as follows:


 - **Edit Sizing** reflects the transform changes applied to a clip in the Inspector of the

edit page.

 - **Input Sizing** applies transform changes to a clip in the color page. It targets clips

on the same level as Edit Sizing but the two modes are distinct to their respective

pages, allowing the editor and colorist to adjust transforms without interfering

with each other’s settings.

 - **Output Sizing** applies to the entire timeline.

 - **Node Sizing** applies to the selected node in the Node Editor.

 - **Reference Sizing** applies to the reference movie or still that is active in the

viewer’s wipe mode.


**4K to 1080p to 4K Workflow**

Switching the timeline resolution is an effective method for optimizing workstation

performance during editing. It ensures that clips are rendered and played in real

time without lag and without altering the quality of the final film. A common

workflow for 4K footage is to set the timeline to 2K or 1920 x 1080 during the

editing process and then reset it to 4K before rendering.


Be aware that the grading potential and accuracy of key-dependent secondary

grading tools (such as the qualifier) are reduced at a lower image resolution.

Therefore, you are advised to change the timeline to the full media resolution

before grading and compositing.


**Lesson 8 Adjusting Image Properties** **349**


##### **Sampling Visual Data with Node Sizing**

The ability to change a clip’s sizing data at the node level allows for some practical

solutions and interesting creative applications. For example, you could clone an image to

display multiple versions of itself within the viewer or fix continuity errors by sampling

portions of the image for cover-up work.


In this exercise, you will remove some signage from a shot by sampling the video data

around it. Practically, this is done for various reasons. Perhaps the filmmakers wish to

replace the signs with street markers that reflect the city the film is based in, or it may

need to be done for localization purposes—not everyone measures height in feet!

**1** Select clip 02.

**2** In the Node Editor’s Clip mode, create a new serial node called **Coverup** . If you have

completed the previous lesson’s self-guided exercises, this node should be between

the Match and Lens Reflections nodes.


**3** Open the Window palette.

**4** Create a curve window and click around the _M1(W) 041F_ sign near the top of the frame.

You are selecting the area you will “remove” from the scene. Label the window

**Left sign** .


**5** In the Window palette, change the Softness > Soft 1 parameter to 0.20 for a slight

edge blur.


**Lesson 8 Adjusting Image Properties** **350**


**6** Open the Sizing palette and set it to Node Sizing mode.


One way to perform the cover-up is to move the window above the sign and then use

the Sizing Tilt parameter to lower that section down, covering the sign. Another

method reverses this operation—you move the clip frame while keeping the Power

Window static.

**7** In the Sizing palette, select Key Lock.


**8** Drag down Tilt until the empty section of the paneling covers up the sign.


**9** Return to the Window palette.

**10** Create a new curve window and label it **Right sign** .

**11** Click around the second sign on the right side of the frame.


Because you have already applied a key lock and moved the placement of the frame,

the right sign will disappear as soon as you finish creating the curve window. To refine

the window’s control points, you can disable the node to see the sign as you work on

the window overlay.


TIP You can create a new node for every cover-up instance if the areas you

wish to clean up are not aligned as in this example.


This simple cover-up works for various reasons: the shot is locked off, the lighting is

consistent, and there is enough content around the signs to cover them up cleanly. In the

next exercise, you will use a more advanced solution to cover up an object in a moving shot

with changing light.


**Lesson 8 Adjusting Image Properties** **351**


##### **Creating Cover-Ups with** **the Patch Replacer Effect**

In this exercise, you will use the more sophisticated Patch Replacer effect to perform a

quick cover-up and automatically adjust the grade of the sampled area to match the region

of the frame it is applied to.


NOTE DaVinci Resolve Studio is required to complete the following exercise.


**1** Select clip 05.


This is a visually interesting shot with a good set design and a great choice of

location. However, one minor element is distracting from the luxurious office: the

wall thermostat. You will remove it by covering it with a sample of the wall.

**2** Create a new serial node and label it **Coverup** .

**3** Open the Effects panel.

**4** From the Resolve FX Revival category, drag the Patch Replacer effect onto the

Coverup node.


Two oval outlines appear in the viewer. The left oval represents the source patch,

which is actively sampling the portion of the video under it. The right oval is the target

patch, which is receiving visual data from the source and actively grading it to match

its surroundings.


**Lesson 8 Adjusting Image Properties** **352**


**5** Drag the target patch over the wall and resize it to outline the thermostat (including

its shadow).

**6** Drag the source patch over an empty area of the wall near the target.

**7** Zoom in to the viewer to refine the patch placements.


**8** In the Patch Replacer settings, select Keep Original Detail to assess the thermostat’s

position behind the target patch overlay. Ensure that the circle outline completely

encompasses the thermostat and its shadow.

**9** Press Shift-Z to fit the video frame to the viewer panel.


The cover-up is successful, but only in the first frame of the clip. As soon as you play

the video, the thermostat moves with the camera while the source and target patches

remain static. To complete the composite, you will need to track the motion of

the camera.

**10** Drag the playhead to the first frame of the clip.

**11** Open the Tracker palette, and, in the upper right corner, set the mode to FX.


In the lower right of the palette, you can choose between two types of trackers:


 - **Point Tracker** is a classic tracker that uses pixel pattern recognition to detect the

motion of an object over time. It works best on high-contrast, in-focus reference

points without visual interruptions.

 - **AI IntelliTrack** is a DaVinci AI Neural Engine–powered tracker that is trained on

real-world examples and identifies the essence of an object or surface to more

accurately follow it, even in footage with low contrast, motion blur, and

busy visuals.


**Lesson 8 Adjusting Image Properties** **353**


NOTE When working in Window mode, you also have the Cloud Tracker

option, which follows the motion of the pixel data within a Power Window.


**12** If you are working in DaVinci Resolve Studio, choose the AI IntelliTrack tracker type.

Otherwise, continue to work with the Point Tracker.


To perform motion tracking, you must place at least one tracker point in the viewer.

Ideally, you want to place this point on the element you are tracking or on a trackable

area that is on the same plane as that element. For this clip, the thermostat itself is an

ideal tracking point.

**13** In the lower left corner of the Tracker palette, click the Add Tracker Point button.


Blue crosshairs appear in the center of the frame. These crosshairs indicate the area

of the image that will be analyzed for tracking.

**14** Drag the crosshairs over the thermostat on the wall.


The crosshairs turn red when the default tracker position is altered.

**15** In the Tracker palette, click Track Forward to perform the track analysis.

**16** After tracking is completed, deselect Keep Original Detail to bring back the target

patch cover-up.


**Lesson 8 Adjusting Image Properties** **354**


**17** If necessary, turn off the viewer onscreen controls to hide the tracking point and

patch overlays.


**18** Play the clip to check the accuracy of the cover-up. Make further adjustments to the

size and placement of the source and target patches, if necessary.


The result is a clean cover-up of the wall that is ready for further editing and grading.


Node-based cover-ups are frequently employed to address a scene’s aesthetic needs or

resolve issues that were not noticed during the shoot (for example, removal of visible set

equipment). The workflows covered in these exercises tend to work best on footage with

limited movement and good sample areas. For more complex cover-ups, you can use the

Fusion page.
## **Using Keyframes to** **Animate Grades**


To understand keyframing, you need only grasp the concept that just _two keyframes_ are

required to create animation. Those keyframes must communicate just two things: their

position in time and their values. By placing the keyframes at different points in the

timeline, you indicate the duration of time through which the change occurs, and by giving

those keyframes individual values, you specify the nature of the change. Using this

principle, you can triple the zoom in a shot over 10 seconds or turn all the oranges in a

scene blue over 20 frames.


**Lesson 8 Adjusting Image Properties** **355**


##### **Animating Position Values with** **Dynamic Keyframes**

Dynamic keyframes animate parameter values across frames, creating the effect of

smooth, consistent change over time. Over the next few exercises, you will animate the

transform values and color grade of a clip to imitate a camera move and sunrise effect.

**1** Select clip 01.


This video was captured late in the evening and appears very dark. Before you begin

grading it creatively, you should expand its luminance range to take advantage of the

available visual information. You will use a similar process to the mountain range

exercise in Lesson 1, where you combined color and log wheels to target and expand a

dark section of the waveform.

**2** Create a new node after INPUT CST and label it **Lum** .

**3** Drag the Gamma master wheel right (0.25) to increase the waveform spread, and then

drag the Shadow master wheel right (0.20) to further brighten the dark foreground.

These steps reveal substantial digital noise in the image, which will be addressed after

the grade is completed.


The clip is a locked establishing shot. However, even though it was captured in real

time, it has a timelapse feel. Your goal is to use animation to imitate the fast

passage of time.


Your first task is to create a pan-and-zoom motion starting from the original wide shot

and ending with a close-up of the city skyline.


**Lesson 8 Adjusting Image Properties** **356**


**4** To the right of the palettes in the color page, open the Keyframes Editor.


The palette features two animation categories: the individual Corrector controls for

each node and the Sizing parameters of the overall clip. The Master header at the top

displays a keyframe summary of all the changes made in the clip.

**5** Create a new serial node and label it **Sunrise** . A new corrector will appear in the

Keyframes sidebar matching the number of the new node.


NOTE The exact number of the node and corrector will depend on whether

you chose to preserve node numbers in the Preferences. If you did, Sunrise

will be node 04. If not, the Sunrise node would have renumbered itself

as node 03.


Each new node you create will be accompanied by a corrector header and controls in

the Keyframes Editor.


TIP Clicking the disclosure arrow next to the Corrector and Sizing headers

expands the list of keyframeable categories. These enable you to specify

which color page feature you wish to target and allow for multiple distinct

animations within a single node. However, in most cases, you will animate just

one element per node, so it will not be necessary to expand and search for the

category you need every time you animate.


**6** Click the diamond-shaped keyframe symbol next to Sizing to activate animation in

that parameter.


From now on, any changes you make to the clip’s Input Sizing controls will be logged

as dynamic keyframes.


**Lesson 8 Adjusting Image Properties** **357**


**7** While on the first frame of the clip, right-click the circular keyframe next to Sizing and

choose “Change to Dynamic Keyframe” to convert the default static keyframe to a

dynamic one.


The circular keyframe becomes diamond shaped.

**8** Drag the playhead to the last frame in the Keyframes timeline.

**9** With the Sizing palette in Input Sizing mode, change the Zoom to 1.500, the Pan to

-400.000, and the Tilt to -200.000.


A new dynamic keyframe is automatically added to the Keyframes timeline. Dimmed

triangles extending from the keyframes indicate that a dynamic animation has

been generated.

**10** Play the clip to review the pan-and-zoom motion. The shot begins with a wide view of

the city and then zooms in on the skyline in the distance.


TIP There is no limit to how many keyframes you can use in a parameter. If

needed, you can move the playhead and make further changes to create more

complex positions or color animations.

You can also drag the keyframes in the Keyframes palette timeline to retime

an animation. Placing keyframes farther apart will result in slower change,

while dragging them closer together will force the animation to speed up.

##### **Modifying Dynamic Attributes**


The animation in this exercise was created successfully, but the zooming motion appears a

little artificial due to its linear nature. In this exercise, you will simulate a more realistic

camera zoom by altering the animation speed and style using dynamic attributes.


**Lesson 8 Adjusting Image Properties** **358**


**1** In the Keyframes palette, select the first keyframe of the Sizing parameter.

**2** Right-click the keyframe and choose Change Dynamic Attributes.


The Dissolve Type interface controls animation behavior between the keyframe you

selected and the keyframe that follows it.

**3** Set the Start Dissolve value to 2. The almost-horizontal shape of the line at the start

indicates that the animation will begin slowly and then gradually accelerate to a

constant (linear) speed toward the end.


**Lesson 8 Adjusting Image Properties** **359**


**4** Click OK to confirm.

**5** Play the clip and note the slow start to the animation. This small change helps make

the zooming effect more realistic, mimicking the motion of a camera operator

physically rotating the lens zoom.


**Using Static Keyframes**

When creating a new keyframe in the editor, the alternative to dynamic keyframes

is static keyframes. Static keyframes don’t animate the change between values;

instead, they abruptly change the value when the playhead reaches the keyframe.


You can combine static and dynamic keyframes within a single animation to

achieve specific results—for example, a lightbulb that turns on abruptly (static) and

then gradually increases in brightness and temperature (dynamic).

##### **Changing Color Values Over Time**


Next, to animate the color values of the clip, you’ll target the node’s corrector controls.

**1** Drag the playhead to the first frame of clip 01.


TIP Press the [ (left bracket) and ] (right bracket) keys to navigate between

keyframes in the Keyframes palette. This shortcut can save you time when

reviewing the start and end positions of an animation or when synchronizing

the animation of other parameters and nodes.


**2** Select the Sunrise node.

**3** In the Keyframes palette, click the keyframe symbol in the Sunrise node’s corrector

header to activate keyframing.


To imitate the look of the sun rising, you will first need to create a pre-dawn look.

**4** Drag the Gamma master wheel left to darken the midtones and then drag the Gamma

color wheel toward blue to imitate a cool night color temperature.


**Lesson 8 Adjusting Image Properties** **360**


**5** Reduce Saturation to 35.00 to imitate the limited perception of color in dark

environments.


**6** Go to the last frame of clip 01.


TIP You can click the Expand button (“Split Primary and Secondary Views”) in

the upper right corner of the Keyframes palette to increase the interface size.

Doing so will move all the central palettes to the left of the color page, giving

you more room to focus on keyframing.


You will now create the post-sunrise look in the same node.

**7** Return the Saturation to 50.0 to bring back the original colors to the scene.

**8** In the Primaries palette, click the reset arrow in the upper right of the Gamma wheel to

remove the dark blue look.

**9** Increase the Contrast (1.300) to create a silhouette effect on the skyline.

**10** Drag the Gain color wheel toward yellow to warm the image.


**Lesson 8 Adjusting Image Properties** **361**


**11** Increase the Highlights (50.00) in the adjustment controls to brighten the sunlight on

the horizon.


**12** Play the clip to see the colors animate from the dark blue look to the light warm look.


With two frames, you have created a new narrative in this clip. Keyframing has wide

applications that range from the practical to the creative. One common reason for

keyframing color grades is to address color temperature fluctuation. Shoots in which the

camera operator might maneuver from indoor to outdoor locations (documentaries,

wedding videography, and so on) benefit greatly from these types of animated-grade

workflows. Creatively, animated grades can help communicate a character’s change in

emotional state or location.


If you are new to keyframing, it can take some getting used to, but in time, and with

consistent practice, generating keyframes and animating changes can become a common

part of your grading workflow.
## **Applying Noise Reduction**


DaVinci Resolve’s noise reduction feature runs on a powerful video engine that can

distinguish noise from environmental data by performing a temporal analysis of the

video frames. This feature allows for a strong reduction of noise while preserving a high

level of detail in the subjects of an image. Applying the additional spatial method of noise

reduction further cleans up the image by analyzing and removing repeating

noise patterns.


**Lesson 8 Adjusting Image Properties** **362**


NOTE DaVinci Resolve Studio is required to complete the following exercise.


**1** Continue to work on clip 01 in the Project 03 - The Long Workday SCD timeline.

**2** Go to the last frame of the clip to work on the scene at its brightest.


Because of the low-light conditions in which this footage was captured, the

brightening of the gamma (in the Lum node) has revealed digital noise in the shadows

and midtones.

**3** For a better view of the noise detail, increase the viewer Zoom (between 100%–150%).


**4** Create a new serial node after Sunrise and label it **Denoise** .

**5** Open the Motion Effects palette.


**Lesson 8 Adjusting Image Properties** **363**


This palette is divided into three control areas:


 - **Temporal NR** analyzes the video across several frames to detect moving subjects

and backgrounds. It excludes moving elements from the most aggressive noise

reduction to prevent unwanted blurring of vital information.

 - **Spatial NR** softens high-frequency noise while retaining data in areas of high

detail. This tool is extremely effective for reducing fine-grain noise that Temporal

NR might miss.

 - **Motion Blur** does not perform noise reduction but uses the same analytical

engine as Temporal NR. This tool helps make action shots more dynamic by adding

artificial motion blur to moving subjects.


Under Temporal NR, you will first need to choose the number of frames that will be

averaged to separate the subject detail from the noise.

**6** For this shot, which features no camera movement or moving subjects, selecting

Frames > 2 for analysis is sufficient. The higher the number, the more accurate the

analysis, but at the expense of extra processing time. A higher analysis rate could also

produce artifacts in shots with overlapping moving subjects.


The Mo. Est. Type (motion estimation type) indicates which method is used to detect

motion in the image. A setting of Faster prioritizes speed of output over quality,

whereas Better produces a finer result at the expense of extra processing. When there

is no movement in a shot, choose None to exclude motion analysis from the result and

apply noise reduction to the entire image.

**7** For clip 01, choose Better. This will prevent the ripples in the water from being too

aggressively denoised and account for the Input Sizing animation.


Motion Range allows you to specify the speed at which the subjects are moving to

exclude areas with motion blur from the noise reduction effect.

**8** Clip 01 has almost no motion, so Small is a good choice.


The Temporal Threshold controls how aggressively noise is reduced in the luma and

chroma channels. These are linked by default, but if the image has monochromatic

noise (or vice versa), it’s advisable to unlink the two parameters and target the luma/

chroma noise separately.


This adjustment will activate noise reduction in the image, so you can begin by

entering any number and then dragging left or right to refine the result.


**Lesson 8 Adjusting Image Properties** **364**


**9** Enter **40.0** as the starting Threshold for the linked channels.


To see how much the Temporal NR is affecting the image, you can use the Highlight

tool to assess the pixel difference.

**10** In the viewer, enable Highlight mode.

**11** In the upper left of the viewer, click the A/B icon to activate Difference mode.


The grainy texture you see in the viewer shows the amount of noise that has been

removed from the original image. When you start to recognize distinct outlines of

objects in the noise pattern, it’s an indication that the noise reduction has become so

aggressive that it is now removing legitimate visual information.

**12** Drag the Threshold left (12.0) until only noise remains.


Overly aggressive noise reduction Good noise reduction


The Motion value acts as a pivot for the point at which moving objects are excluded

from noise reduction. A lower value excludes larger areas of the image, whereas a

higher value assumes less motion and targets more of the image.

**13** Leave the Motion parameter as it is.


The Blend value allows you to mix the original image back into the noise-reduced

output. This adjustment can be helpful when noise reduction gets too aggressive and

areas of the image take on a plastic appearance.

**14** Leave the Blend parameter as it is.

**15** Turn off the Highlight mode in the viewer.

**16** Disable and enable the Denoise node to compare the image before and after

Temporal NR.


The noise reduction is targeted but subtle. To further improve the result, you will use

Spatial NR to analyze and remove the generic noise pattern in the frame.


**Lesson 8 Adjusting Image Properties** **365**


At the top of the controls, you can select which noise reduction mode you wish to use.


 - **Faster**, **Better**, and **Enhanced** modes will all run their pattern analysis within a

given radius size and configure their output based on the set threshold. They are

listed in order of processing complexity.

 - **AI UltraNR** is an AI-driven noise pattern identifier that will extract the noise

pattern from the signal by locating and analyzing the “flattest’’ section of the

frame for pure noise.


**17** Under Spatial NR, set the reduction mode to AI UltraNR.

**18** Click Analyze.


A bounding box appears in the frame, identifying the “emptiest” area of pixel data in

the given frame. With no tangible visual content, the data within the square is ideal for

extracting the digital noise produced by the camera sensor.


You can reposition and resize the bounding box in the viewer if you wish, but it is

generally not advised—AI UltraNR is better at detecting optimal analysis regions

than our eyes.


**Lesson 8 Adjusting Image Properties** **366**


You can also manually adjust the Noise Profile Luma and Chroma Threshold settings,

but again, AI UltraNR tends to automatically achieve the ideal mix of thresholds for

clean noise reduction.


TIP Noise Reduction is available in the Effects Library under the Resolve FX

Revival category and features all the same settings. You can use it to apply

noise reduction to clips directly in the edit or cut page timelines.


**19** Press Command-D (macOS) or Ctrl-D (Windows) to bypass the Denoise node and

compare the image before and after noise reduction. Pay particular attention to the

preservation of the fine detail in the image—like the Ferris wheel spokes and the

windows of the buildings in the skyline.


Before noise reduction After noise reduction


Before moving on, it is also worth checking at what point in the node tree noise

reduction is optimal.

**20** Create a new local grade version (version 2).

**21** Select the Denoise node and press E to extract it from the node tree.

**22** Drag the Denoise node over the link between the INPUT CST and the Lum node. Doing

so will reduce noise on the clip before any grading or animation occurs.


In this instance, the change softens the impact of the noise reduction and produces a

better visual output.


You can also check how noise reduction works when applied to the signal prior to

color management.


**Lesson 8 Adjusting Image Properties** **367**


**23** Create a new local grade version (version 3).

**24** Hold Command (macOS) or Ctrl (Windows) and drag the Denoise node over the INPUT

CST to swap their order. Noise reduction is now applied to the original RGB

camera signal.


Without color mapping, AI UltraNR is forced to analyze log-encoded media, making the

noise pattern harder to detect. This results in more aggressive noise reduction and a

smearing effect in the frame.

**25** Label the versions ( **node 4**, **node 2**, and **node 1** ) for easier reference when you

compare the different Denoise node position results in the viewer.

**26** Press Command-N (macOS) or Ctrl-N (Windows) repeatedly to cycle between the

three versions.

**27** Leave the clip on version 2 (node 2), in which the Denoise node is placed after the

INPUT CST.


**Where Is the Best Place for the Noise Reduction Node?**

Applying NR at (or near) the start of the node tree is advisable because it analyzes

and treats the original RGB data. However, this placement may potentially result in

softer edge detail that will affect every downstream node in the grading process.


Applying NR toward the end of the node tree will usually result in sharper edge

detail but may struggle to accurately identify and completely remove noise after it

has been graded and contrasted. When unsure, experiment with the placement of

the NR node in the Node Editor until you find the optimal position.


It’s always advisable to use a dedicated node for noise reduction. After the noise is

reduced to a satisfactory level, you can opt to disable the NR node to reduce the amount of

processing and caching that takes place as you grade. Keep in mind, however, that a

substantially noise-reduced signal might have an observable impact on downstream

nodes, especially chroma and luma key-based nodes like the qualifier. In such cases, it is

recommended to keep the NR node active to get a more accurate representation of your

final look. If this impacts processing and real-time playback on your workstation, you can

enable render caching to ensure smooth system performance.


**Lesson 8 Adjusting Image Properties** **368**


## **Optimizing Performance** **with Render Cache**

Almost anyone who has worked with raw footage or done graphic-intensive work on a

computer will be familiar with the frustration of experiencing lag when the workstation

cannot process the data in real time.


DaVinci Resolve offers various methods for improving workstation performance, such as

reducing the playback resolution, changing debayer quality, generating proxy media, or

using a transcoded media workflow.


Another powerful method for increasing playback speed is allowing DaVinci Resolve to

render your footage while the application is otherwise inactive. You can then play the

cached media without the need to render effects-heavy clips in real time. The caching

mechanism in DaVinci Resolve is made up of four independent stages that prompt a

render based on various criteria. This allows DaVinci Resolve to monitor each clip and

timeline and only generate renders when they meet one or more of the cache-level

requirements. In order, these levels are:


- Fusion Output Caching

- Node Caching

- Color Output Caching (optional)

- Sequence Caching

##### **Enabling Smart Cache**


Caching in DaVinci Resolve can occur on the timeline, clip, or even the node level.

Additionally, cache rendering can occur automatically, if meeting the criteria determined by

the Smart Cache feature, or manually, as determined by the user. You will experience most

of these cache levels in the next few exercises.

**1** Enter the edit page.

**2** If you did not do so in Lesson 7, enable caching by choosing Playback > Render

Cache > Smart.


**Lesson 8 Adjusting Image Properties** **369**


A red bar appears above the edit page timeline and gradually turns blue as frames are

successfully cached. Rendering is prioritized to the playhead position so that the clips

you are actively working on are the first to be processed.


NOTE If you do not observe this caching process in the timeline, it’s possible that

the project does not have a cache location. To fix this, enter the Project Settings,

and in the Master Settings, scroll down to the Working Folders. Ensure that the

Cache files location is set and has write access.


The first level at which caching occurs is Fusion Output Caching (previously known as

source caching). Its name refers to the position in the video signal’s order of operations.

After media is imported and added to a timeline, its signal flows from the edit page to the

Fusion page and is then routed back to the edit page, which prompts this first cache. When

in Smart Cache mode, Fusion Output Caches are generated for processor-intensive video

media codecs such as H.265/HEVC and most raw camera formats, as well as for any

compositing performed in the Fusion page.


The Project 03 - The Long Workday SCD timeline uses media compressed with an

intermediary codec (DNxHR) already optimized for editing; therefore, the program can play

it in real time without triggering the Fusion Output Cache. You’ll have a chance to observe

this level of caching in Lesson 9, “Setting Up Raw Projects,” where you work with raw

media. Fusion is also not triggering the cache because you have not done any work in the

Fusion page in this lesson.


The timeline turned red when you activated Render Cache because of the work you did on

the node cache level in the color page.

##### **Generating a Node Cache**


Node caching occurs in the Node Editor of the color page after grades and effects are

applied. As with Fusion Output Caching, when Smart Cache is enabled, rendering occurs

only when DaVinci Resolve deems the node processes to be intensive.

**1** Enter the color page.


You will continue to work on clip 01.

**2** In the interface toolbar, ensure that the Timeline button is enabled. This will display the

mini-timeline, in which you can observe the video tracks and their cache processes.

**3** Create a serial node before the Denoise node and label it **BW** .


**Lesson 8 Adjusting Image Properties** **370**


**4** In the adjustment controls, drag the Saturation value to 0.


The image retains its sunrise animation but now plays it in black and white. The

timecode above the clip thumbnail turns red to indicate that it is being re-cached. In

the Node Editor, the Denoise and OUTPUT CST node names and numbers turn red for

the same reason.


The INPUT CST remains blue because the BW addition has not affected its incoming

signal. The BW node also does not turn red because the standard color grading tools

in the color page are not classified as intensive enough to trigger a cache.


The cache line in the mini-timeline will eventually turn blue as the render is completed.


You will now observe how changes in node order impact cached nodes.

**5** Click the BW node and press E to extract it.

**6** Drag the BW node over the connection line between the Sunrise and OUTPUT

CST nodes.


The Denoise and OUTPUT CST nodes turn red again as they process their respective

new incoming RGB signals. The Denoise node is no longer processing a black-and
white signal, and the OUTPUT CST is processing the video under a different order

of operations.


**Lesson 8 Adjusting Image Properties** **371**


**7** After the nodes turn blue, click the BW node and raise the contrast to 1.100.


The OUTPUT CST node turns red as it forces a re-cache. The change does not impact

the Denoise node this time because nodes are not affected by downstream changes

in the node tree. If you follow the path of the RGB signal, it is denoised before it is

desaturated, so the program continues to use the same denoised version of the

cached render.

**8** Delete the BW node.

##### **Observing Sequence Caching**


After the Fusion Output and Node Caches, a Sequence Cache is prompted in the edit page

when effects such as transitions, titles, or generators are applied to the timeline.

**1** Enter the edit page.

**2** Open the Effects Library panel.

**3** In the Toolbox > Titles folder, locate the Text title generator.


**4** Drag the title generator onto video track 2 and extend its length to cover the first five

clips of the timeline.

**5** In the upper right of the edit page, open the Inspector palette.


**Lesson 8 Adjusting Image Properties** **372**


**6** Under Rich Text, enter the project name **The Long Workday** .


A red line appears over the timeline to indicate that a render cache is being generated

for all the media under the title tool.


**7** Enter the color page.


Note that the sequence cache for the title generator is still visible in the mini-timeline.

If you don’t want to see or cache edit page effects on higher tracks during grading,

you can opt to disable them.

**8** Click V2 on the mini-timeline to hide the project name text and prevent it from

prompting the sequence cache render.

##### **Utilizing User Cache Modes**


As you’ve seen, the decision to render clips and nodes on every level of the workflow is

made by DaVinci Resolve’s background processes. This allows you to continue focusing on

your project while Smart Cache detects if and when rendering is necessary.


However, at times, you might want to control which clips or nodes are rendered. For that,

you can enable User Cache, which will not perform any media rendering until you

specifically tell it to do so.

**1** Choose Playback > Render Cache > User.


The blue highlights on the clip timecodes and nodes disappear. From now on, all

render caching will occur only on your command.


**Lesson 8 Adjusting Image Properties** **373**


Some colorists prefer to work in this mode when they don’t want an entire timeline to

get cached as soon as they launch a project. One reason might be that they’re using

raw media and want to cache only the clips they are actively working on.

**2** Select clip 01.

**3** Right-click the Denoise node and choose Node Cache > On. Once again, caching is

prompted, and the node name (and clip timecode) eventually turns blue.


TIP When working on a larger project, you could use the Clips filter to isolate

clips with noise reduction and manually cache them to avoid enabling

Smart Cache.


In addition to selecting individual nodes, you can manually render a clip’s entire

node tree.

**4** Select clip 05.

**5** Right-click clip 05 and choose Render Cache Color Output.


The clip’s timecode turns red in the timeline while the nodes remain white. In this

scenario, the entire node tree is cached, which results in even faster processing when

compared to individually rendered nodes. However, it also means that making changes

to _any_ of the nodes in the tree will require the entire clip to be re-cached.

**6** In the Node Editor, add a new serial node called **Magenta Look** .

**7** Drag the Offset color wheel toward magenta to add color to the clip.


Although simply adding color to a clip is not processor intensive, the clip’s timecode

immediately turns red because in User Cache mode, any change will prompt

a re-cache.


**Lesson 8 Adjusting Image Properties** **374**


**8** Remove the Magenta Look node.


The clip caches again, even though you recently had this exact configuration of nodes.

This is because the program does not keep a record of which specific changes

triggered a cache render. Even if you return to previous settings, the clip will treat the

change as new and will re-cache.


You can still manually override the cache status of nodes and clips in Smart Cache mode by

right-clicking and choosing On or Off in the Cache submenu. In User Cache mode, you use

these same controls to activate caching, but there will be no background “Auto” processes,

like the ones in Smart Cache mode.

##### **Configuring Cache Quality**


When you play media in the viewers of the edit and color pages, you can see the playback

frame rate in the GPU status indicator in the upper left of the viewer.


A green light indicates that the media is playing in real time. A red light indicates lag, with

the numerical value displaying the actual playback frame rate. Caching should result in the

GPU status indicator always displaying a green light during playback. If it does not, you

should consider lowering the Timeline Proxy Resolution in the Playback menu or reducing

the quality of the cache.

**1** Open Project Settings and click the Master Settings tab.

**2** Scroll down until you see the Optimized Media and Render Cache section.


**Lesson 8 Adjusting Image Properties** **375**


The “Render cache format” field allows you to choose the codec used to encode your

cached media.


Lowering the cache quality will reduce the file size and prevent your storage from

running out of space too quickly. However, this setting will also lower the visual quality

of the rendered media in your viewer. You should avoid reducing cache quality if

precision of color and key data is important.


Inversely, raising the cache quality will result in a faithful reproduction of your image at

the expense of very large render files.

**3** Set the “Render cache format” to one of the full quantization formats (444 or 4444).


Beneath the “Render cache format” menu are a few checkbox options.


You can specify the amount of time that must pass before background caching begins

in Smart Cache mode. By default, the interval is 5 seconds, but you can increase the

duration if you prefer to tweak your settings at a leisurely pace when grading.


Additionally, you can enable automated transition and composite rendering when in

User mode, which will mimic the behavior of Smart Cache mode.

**4** Click Save to exit the Project Settings.


Another reason why cached media may not play back in real time is that the cache working

folder location might have insufficient read/write speed. Check that the folder is not

located on an old drive or a cloud account (if you have a poor internet connection).


NOTE By default, the Cache files location of the Working Folders is assigned to

the topmost media storage location (Preferences > System) of your project library.

To optimize playback, you might want to redirect the cache location to a drive

other than the one that contains the DaVinci Resolve application and your

project files.


**Lesson 8 Adjusting Image Properties** **376**


##### **Clearing a Cache**

Although caching is triggered on multiple levels, only one cached file is ever active for each

clip or transition. For example, if you apply noise reduction to a clip and then place text

over it on the edit page, the active cache will be a rendered video with reduced noise and

baked-in text. Any further changes will prompt a new cache, which will replace the previous

iteration on the timeline. All the previous renders will be retained in your storage location

until you choose to clear your cache. You’ll want to clear your cache periodically to make

room for more renders or to delete unnecessary materials from older projects.

**1** Choose Playback > Delete Render Cache > Unused.


A prompt will ask you to confirm that you want to delete the unused cache associated

with this project.

**2** Click Delete. The media in the timeline remains rendered, while all previous cached

versions of the clips are removed from your storage.


Other options for deleting the render cache allow you to delete all cached media or

only the renders associated with selected clips on the timeline. It’s important to

remember that no actual media is affected when clearing a cache, and even if you

accidentally delete the renders currently being used in your project, they will be

regenerated the next time caching is triggered.


TIP Occasionally, you might come across a graphic anomaly in which the

viewer in the color page is outputting visual data that does not match the

changes you made to a clip. For example, a Media Offline placeholder might

appear when you are certain the media is connected. Clearing the active

render cache (All) will remove the program’s memory of the clip render and

force it to re-cache the clip correctly.


You can also opt to clear the render cache of specific projects in your libraries.


**Lesson 8 Adjusting Image Properties** **377**


**3** Choose Playback > Manage Render Cache.


The Manage Render Cache window allows you to filter your projects based on storage

location and library. The columns underneath list all your projects and the sizes of the

render cache associated with each one.


To free up storage space, select the checkboxes of older projects and click Clear

Selected Cache in the lower left corner.

**4** Click Close when done.


TIP You can automate the deletion of cached files after a certain period of time.

Go to Preferences > User > Cache Management and indicate (in days) how

frequently you wish to clear the cache.


Proxies and offline media formats are vital for a clean editing workflow, but their use is

discouraged for compositing and grading because they are often of lower visual quality

than the camera originals, which impacts grade clarity and secondary selections. Using

Smart Cache with a high-quality render format will allow you to work faster with higher

image fidelity.
## **Self-Guided Exercises**


Complete the following exercises in the unfiltered Project 03 - The Long Workday SCD

timeline to test your understanding of the tools and workflows covered in this lesson.


**Clip 02** —Use node sizing to cover up the speed limit signs at the top of the frame.


**Clips 03–05** —Apply noise reduction to each clip in the Office group. If you use AI UltraNR,

make sure you re-run the Noise Profile analysis for each clip.


**Clip 08** —Use dynamic and static keyframes to flicker the lights in the garage.


**Clip 16** - Use Patch Replacer to remove all the clouds from the sky using the fewest nodes

possible. Compound the cloud cover-up nodes when finished.


When you’ve completed these exercises, open the **Project 03 - The Long Workday**

**Commercial COMPLETED.drp** and review Lesson 08 Timeline COMPLETED to compare

your work with this “solved” timeline. If the media appears offline, click the red Relink

Media button in the upper left corner of the media pool and specify the location of the

Project 03 media on your workstation.


**Lesson 8 Adjusting Image Properties** **378**


## **Lesson Review**

**1** True or False? If you change a project’s timeline resolution, you will need to review your

secondary grade nodes and manually resize all the Power Windows to fit the

new resolution.

**2** Where can you animate the sizing properties of a clip?

**3** What are dynamic keyframes?

**4** True or False? Noise reduction should be applied only to node 01 of any clip.

**5** Would adding a vignette to a clip cause Smart Cache to render the clip?


**Lesson 8 Adjusting Image Properties** **379**


##### **Answers**

**1** False. DaVinci Resolve is resolution-independent, meaning all secondary tools

automatically resize to fit a new project resolution and aspect ratio.

**2** You can animate the sizing properties of a clip in the Keyframes Editor by changing

transform values in the Input Sizing mode of the Sizing palette.

**3** Dynamic keyframes gradually change a value between two points in time.

**4** False. Noise reduction can be applied to any position in the node tree, based on

effectiveness.

**5** Maybe. Primary and most secondary grading tools are not considered processor
intensive enough to prompt a Smart Cache render, so adding a vignette on its own

would not trigger a cache. However, if the vignette was placed upstream from a Smart

Cached node, it would trigger a re-cache.


**Lesson 8 Adjusting Image Properties** **380**


### Lesson 9
# Setting Up Raw Projects



Raw media refers to various still and

video image formats in which visual

data is captured as an unprocessed

digital signal. In its initial state, raw

media does not have any visual

properties. It is only through a

processing method called _debayering_

that you can assign a monitoring

color space to the video signal and

view it on a display. Raw media has

far greater grading potential due to

its high dynamic range, wide gamut,

and uncompressed approach to pixel

data encoding.


In this lesson, you will work with

Blackmagic RAW (.braw) clips.

Blackmagic RAW offers the same

grading latitude as other raw

standards with the additional

benefit of GPU acceleration and

partial debayering, which results in

dramatically smaller file sizes and

faster playback.



Time

This lesson takes approximately
2 hours to complete.

Goals

Adjusting Raw Settings
at the Project Level 382

Adjusting Raw Settings
at the Clip Level 389

Grading High Dynamic
Range Media 393

Setting Up a Render Cache
for Raw Media Projects 406

Self-Guided Exercises 408

Lesson Review 409


## **Adjusting Raw Settings** **at the Project Level**

The color management exercises you completed in Lessons 4 and 7 demonstrated how to

configure a project’s color space (gamut) and gamma (transfer function) to set up the

starting point of a grade. Debayering raw footage works on a similar premise, although it’s

a far more essential part of the grading process. Without it, the raw media cannot be

displayed in the viewer.


Raw format sensors are defined by their ability to record the photometric properties of

light. Rather than presenting as a set of pixels with hard color data, raw formats record the

light intensity of a scene within the geometry of the sensor’s individual photoreceptive

elements, or _photo sites_ .


To reach a photo site, light must pass through a filter that isolates just one channel of

color—red, green, or blue. Together, the filtered signals make up the Bayer mosaic that

contains all the data necessary to re-create the image digitally. In the Bayer mosaic, green

is captured at double the frequency of red and blue, mimicking the standard observer’s

perception of color.


For this reason, raw files are sometimes called _digital negatives_ : visual information

containing a wide dynamic range of light that remains unviewable until processed.

Debayering (also known as _demosaicing_ ) allows you to appoint values to the photometric

signals and produce a visible image in a designated color space and resolution.


**Determining Whether Clips Are Raw**

You can sometimes recognize whether a video file is raw by its format name

(ArriRaw, Nikon RAW, Canon Raw, etc.) or extension (.braw), which you can see in

the Metadata panel. However, many formats do not provide these clues, and you

need to know that they are raw before you start working with them (like RED or

Phantom CINE).


A quick way to verify whether footage is raw (and supported by DaVinci Resolve 20)

is to place it on a timeline and open the Camera Raw palette in the color page. If

the selected clip is in a raw format, the palette becomes active and displays

options for the Decode Quality and Decode Using fields. If the clip is not raw, the

Camera Raw palette will remain inactive.


**Lesson 9 Setting Up Raw Projects** **382**


In this lesson, you will work with Blackmagic RAW media. This raw format is unique in that it

undergoes partial debayering in the camera hardware, which results in much smaller file

sizes and storage as a single video clip (as opposed to an image sequence). This format

allows for much faster playback, media management, and file transfer compared to

traditional raw formats.

**1** Open DaVinci Resolve 20.

**2** Create a new project and name it **Blackmagic RAW Project** .

**3** Go to the media page.

**4** In the media pool, create two bins: **Video** and **Timelines** .

**5** In the media storage browser, locate the BMD 20 CC - Project 03 folder and enter the

Blackmagic RAW subfolder.

**6** Open the Media folder and drag the four .braw clips into the Video bin.


If a dialog appears informing you that your clips’ frame rates don’t match the project’s

frame rates, click Change to adjust the project frame rate to accommodate the media.

**7** Go to the edit page.

**8** Set the media pool to List view and make sure the clips are sorted alphabetically in the

Clip Name column.

**9** Select the four Blackmagic RAW clips. Right-click one of them and choose Create New

Timeline Using Selected Clips.

**10** Name the timeline **Blackmagic RAW Timeline** and place it in the Timelines bin.

**11** Choose Playback > Render Cache > Smart.


The Fusion Output Caching process will begin immediately on the Blackmagic RAW

clips. Unlike the media you’ve used in previous lessons, raw formats are not

intermediaries and need constant debayering and caching.


**Lesson 9 Setting Up Raw Projects** **383**


When reviewing the clips in the timeline viewer, you will see that two of them have

black bars at the top and bottom of the image. This is known as letterboxing and

occurs when clips have a different aspect ratio to the timeline viewer. By default,

DaVinci Resolve will scale media with mismatched resolutions to preserve maximum

video data. However, if you want all the clips to have the same framing, you can change

your scaling options in the Project Settings.

**12** Open Project Settings and click the Image Scaling tab.

**13** In the Input Scaling category, set “Mismatched resolution files” to “Scale full frame

with crop.”

**14** Click Save to close the Project Settings.


Before


After


All imported media will now be scaled to fill the viewer frame. This happens at the

expense of some cropping on the edges of the clips, but this data can still be retrieved

using the Input sizing palette if needed.


Next, you will set up the project color management.


**Lesson 9 Setting Up Raw Projects** **384**


##### **Color Managing with ACES**

The Academy Color Encoding System (ACES) is a scene-referred, display-independent color

management framework developed to standardize digital cinema and broadcast

post‑production workflows. Its cross-platform support and operational consistency have

led it to be adopted as an industry standard in major post-production houses and

streaming services. As well as being a color management system, it defines its own set of

primaries and transfer functions for various workflows:


**ACES gamuts:**


- **AP0** primaries are photometrically linear and encompass a future-proof wide color

gamut. AP0 is recommended for long-term archival encoding and media storage.

- **AP1** primaries are typically encoded with logarithmic transfer characteristics

(listed below). Their gamut is not as wide as AP0’s but is still wider than any

current deliverable standard. AP1 primaries are recommended for color grading

and compositing.


**ACES transfer functions:**


- **ACEScc** is the AP1 primaries with logarithmic transfer characteristics. It is

recommended for color grading.


ACEScc


**Lesson 9 Setting Up Raw Projects** **385**


- **ACEScct** is a ACEScc variant with a higher toe that results in “milkier” shadows in lift

operations. Some colorists prefer it for its film-like appearance, and it is also used for

color grading.


ACEScct


- **ACEScg** has AP1 primaries with a linear transfer function. It was designed for visual

effects compositing workflows.


In terms of setup, ACES operates similarly to Resolve Color Management. It requires an

input and output to perform color mapping. In ACES, these are called input display

transform (IDT) and output display transform (ODT). Since ACES itself is the working space,

there is no timeline color space. ACES can be enabled project-wide from the Project

Settings or applied to individual nodes using the ACES Transform effect.

**1** In the Project Settings window, click the Color Management tab.

**2** Set the Color Science to ACEScc.


**3** Leave ACES version set to the latest, ACES 2.0.

**4** DaVinci Resolve supports ACES AMF 2.0 sidecar files that define a clip’s input and

output transforms in XML. You can leave this setting set to None.


**Lesson 9 Setting Up Raw Projects** **386**


DaVinci Resolve automatically detects all supported raw formats. Thus, when color

managing on a project level (via ACES or RCM), you do _not_ need to indicate the input

color space of the media. Raw formats are automatically mapped to your working color

space and then transformed to the deliverable standard in the Project Settings. In

such cases, the input parameters will only impact non-raw media.

**5** Leave ACES Input Transform set to No Input Transform.


Unlike with Resolve Color Management, there is no Timeline color space parameter in

the Project Settings. The project will operate within the fixed, log-encoded AP1 ACES

color space.

**6** Set the ACES Output Transform to Rec.709 BT.1886 or your preferred monitoring

standard.

**7** “Process node LUTs in” applies only to CLF LUTs. You can use standard LUTs as usual or

use the ACES Transform to map the starting point of a LUT to an anticipated standard.

You can leave this setting as it is.

**8** Select “Use color space aware grading tools” to ensure tools like the qualifier and

curves operate consistently in the wide ACES gamut.


Several other parameters in the Project Settings can be left to their default values.

DaVinci Resolve settings are generally optimized for the average workflow, with the

option to override those defaults scattered throughout the Project Settings and

Preferences. You will usually know when (and why) you need to change the defaults

when working with specialized workflows or formats.

**9** Click Save to exit the Project Settings.


The images in the viewer shift to display the color-managed raw signal.

**10** In the interface toolbar, open the Metadata panel.

**11** Change the Group filter to Camera.


One of the benefits of working with raw media is that it retains the maximum amount

of camera metadata associated with the footage. In the panel, you can see the camera

type and manufacturer used to capture the footage, and even the shutter angle and

lens model.


**Lesson 9 Setting Up Raw Projects** **387**


##### **Reviewing Raw Settings on the Project Level**

With the project color management set up, you can also review the raw project settings to

control how the raw signal is debayered.

**1** Open the Project Settings and click the Camera Raw tab.


These settings affect how raw footage is debayered on a project-wide basis.

**2** Set RAW Profile to Blackmagic RAW to access the parameters of the clips in

your timeline.


The “Decode quality” is set to the default “Full res.” (full resolution), which means that

raw media is debayered at its native resolution and resized to the timeline resolution

set in the Master Settings. Changing the quality to Half or Quarter will substantially

reduce the processing required to play the footage (at the expense of the visual quality

in the viewer/monitor) and is a viable option for slower systems. You can opt to work

on a lower debayer resolution and later select “Force debayer to highest quality” in the

Advanced Render Settings of the Deliver page before rendering to ensure the image

quality is optimized for export.


NOTE No matter which “Decode quality” you choose, Fusion will always

debayer raw media in its full native resolution.


**3** Leave the “Decode quality” set to “Full res.,” which will be 4K, 4.6K, and 6K for the clips

in this project.


The “Decode using” field allows you to specify how the raw signal is debayered relative

to common in-camera settings such as color science, color space, white balance,

exposure, and so on. By default, it is set to “Camera metadata,” which will incorporate

the settings made by the camera operator during media capture. Changing it to

“Blackmagic RAW default” will reset the camera metadata and prompt it to use any


**Lesson 9 Setting Up Raw Projects** **388**


associated sidecar file metadata. Setting the decode method to Project will reveal the

fully customizable project and camera metadata settings in the lower half of the

Camera Raw window.


NOTE A sidecar file contains descriptive metadata that can be associated

with raw media for look management in-camera and during post-production.

You can generate a sidecar file to back up or share debayer settings and to

preview rushes in a dedicated raw player (such as the Blackmagic RAW player).

As a rule, sidecar files always take precedence over the embedded metadata.

If the sidecar is deleted or moved, the decoding of the raw file will fall back on

the embedded raw file metadata.


**4** Leave “Decode using” set to the default “Camera metadata.”

**5** Click Save to exit the Project Settings.


In Part I of this book, you began working on media without any special color treatment in

what is known as a display-referred workflow. In Part II, you enabled color management to

automatically map log-encoded source clips to the Rec.709 color space. In the final part,

you took advantage of the DaVinci Wide Gamut to future-proof your deliverables using

node-based CSTs, and now you will use the industry-standard ACES framework to explore

other approaches to the display-referred workflow.


There is no single “correct” choice for the treatment of media before the start of the

grading process. The decision to use one color approach over another can be based on

several factors: source media, delivery format, monitoring setup, LUT structure,

collaborators’ software, and personal preference. In this lesson, you will continue to work

with ACES color management, with additional consideration given to the treatment of the

raw signal on the color page via the Camera Raw palette.
## **Adjusting Raw Settings** **at the Clip Level**


When preparing raw media for grading, you will often want to address the individual

debayering needs of clips. The Camera Raw palette in the color page allows you to make

adjustments on a clip-by-clip basis.

**1** Go to the color page.

**2** Select clip 01 (C001).


**Lesson 9 Setting Up Raw Projects** **389**


**3** In the left palettes of the color page, open the Camera Raw palette.

**4** Set Decode Using to Clip. Doing so will disassociate it from the Project Settings and

allow you to work on the clip independently.


The Camera Raw palette gives you access to various color, exposure, and gamma

controls that will affect how the image is debayered on the timeline. In terms of the

signal pipeline, debayering occurs before the video signal enters the source input of

the Node Editor.

**5** Color Science refers to the version of the color science (or color profile) in the camera

at the time the footage was captured. Leave Color Science set to Gen 4.

**6** Change the ISO to 200.


Although the image has already been captured, you can still adjust the sensor

sensitivity to better accommodate your grade’s starting point to the scene’s

luminance. ISO (along with most visual parameters) is ordinarily baked into digital

footage after encoding, so this feature is unique to raw media workflows.


NOTE Dual Native ISO is a feature in some cameras that regulates the optimal

dynamic range for a given exposure to improve image clarity and reduce

noise. Depending on the ISO set during capture, you will see one of two native

ISO ranges available in the Camera RAW palette.


**7** Change the ISO back to 100.


Another method of adjusting signal brightness is to use the Exposure parameter in the

central column of the Camera Raw palette. Decimal values allow you to adjust

exposure in smaller amounts than the whole values featured in the ISO dropdown.


**Lesson 9 Setting Up Raw Projects** **390**


However, looking at the waveform, it is clear that the overexposure in the sky cannot

be resolved with just ISO or Exposure adjustments.


Blackmagic RAW performs partial debayering to reduce processing and speed up

playback. This function is visually imperceptible in most cases, but it may result in the

upper limits of the dynamic range appearing clipped in the waveform. To fully debayer

the raw signal, you will activate Highlight Recovery.

**8** Click the Highlight Recovery checkbox under the ISO parameter.


Highlight Recovery will debayer highlight sensor data that is usually clipped in the

standard decoding matrix. In raw clips with extreme waveform peaks, this option will

often reveal additional information in the highlights.


Without Highlight Recovery With Highlight Recovery


Temperature is another property of light that can be adjusted during the

debayer stage.

**9** Drag the Color Temp slider right (6000) to warm up the image.

**10** To reset the Color Temp to the original setting used during filming, click the White

Balance dropdown menu on the left and choose As Shot.


**Lesson 9 Setting Up Raw Projects** **391**


When working on a raw timeline, you will often want to reuse the Camera Raw controls

across multiple clips. Two buttons at the bottom of the Camera Raw palette allow you

to copy the palette data: Use Settings and Use Changes.


 - **Use Settings** will apply all the Camera Raw settings from a selected clip to all

highlighted clips on the timeline. This option is best used when working with

media from the same source and with similar exposures.

 - **Use Changes** will ripple only the altered parameters, preserving the selected clips’

individual settings. This is ideal when working with visually diverse media that

must retain its unique ISO and Color Temp settings.


**11** With clip 01 still selected, Shift-click clip 04 to highlight all the clips in the timeline.

**12** Click Use Changes in the Camera Raw palette. Because the only available parameters

in clips 2–4 are the decode settings, all three clips switch from Project to Clip decoding

while keeping all other clip settings unchanged.


TIP When saving and applying stills to raw clips, Camera Raw settings are

included in the grade transfer. To prevent Camera Raw data from being

overwritten during still application, right-click in the gallery and choose Copy

Grade: Preserve Camera Raw settings.


**13** Select clip 02 (C003).

**14** To better prepare this clip for primary grading, raise the ISO (1250) so that the

subjects’ faces land in the middle gray region of the waveform.

**15** Select clip 03 (D007).


Reviewing the scopes tells you that a substantial amount of highlight data is crushed at

the top of the waveform graph. The overall scene exposure is satisfactory, so you will

address that highlight region when grading. Leave the ISO at 400.

**16** To ensure that you can retrieve the visual data outside the window, select

Highlight Recovery.


**Lesson 9 Setting Up Raw Projects** **392**


**17** Select clip 04 (E004).


This clip features a dark environment with unique lighting conditions. Although it

might be tempting to address the shadows using the Camera Raw controls, dragging

the Exposure value quickly reveals that it’s not possible to do so without severely

distorting the image. This clip is already at its ideal starting point, and you will further

optimize it using the primary grading tools. Leave the ISO at 5000.


With the raw clips successfully set up, you can proceed to grading in the Node Editor

as usual.


NOTE The Color Space and Gamma parameters in the Camera Raw palette are

disabled when working in a color-managed project. This allows for consistent color

output when changing deliverable formats in the Project Settings.


If you want to assign unique input color spaces to your raw clips and adjust the

Gamma Controls to the right of the Camera Raw palette, you will need to disable

project color management and instead perform node-based color management or

work in a display-referred environment with no color management at all.


The Camera Raw palette is best used to address raw media’s unique ISO and exposure

needs prior to grading. It is highly advisable to avoid balancing, adjusting contrast, or

creating looks at this stage because the Camera Raw palette leaves no evidence of such

changes in the Node Editor. The standard grading tools in the color page impact raw

media just as effectively and are far easier to keep track of in the node tree, which is

important for minimizing destructive grading.
## **Grading High Dynamic** **Range Media**


One of the unique challenges of grading high dynamic range (HDR) footage is targeting

the wide tonal latitude of the available data. In a previous lesson, an overexposed sky was

selected using secondary grading methods to make an isolated luminance adjustment.

Such targeted tonal adjustments can be more frequent when shooting HDR and ordinarily

require extensive secondary grading to achieve a clean look.


The High Dynamic Range (HDR) palette is a primary grading tool featuring color wheels

mapped to customizable tonal ranges that can be used to grade the entire dynamic range

of a raw image within a single interface.


**Lesson 9 Setting Up Raw Projects** **393**


##### **Targeting Individual Tonal Ranges**

As established, a major benefit of the HDR palette is its advanced tonal range control.

Instead of relying on just three wheels to determine the placement of the shadows,

midtones, and highlights, you can construct dynamic looks by adjusting each tonal step of

the image independently. The gentle rolloff between the tonal ranges ensures that grades

appear smooth and natural.


In this lesson, you will color grade a raw clip to gain an understanding of the HDR palette’s

unique global and tonal range parameters.

**1** Select clip 01 (C001).

**2** Label node 01 **HDR balance** .

**3** In the left palettes, open the High Dynamic Range (HDR) palette.


At first glance, this palette resembles the Primaries color wheels. In fact, much of the

operation remains the same—the control point in the center of the wheels adds color

to a tonal range, while controls underneath determine exposure and saturation.


One of the first major differences is the number of wheels you control. A row of

buttons under the palette header allows you to navigate between the different tonal

zone wheels. This action is called _banking_ .


You can click the arrows on either side to bank wheels or click the wheel icons to jump

one or more wheels at a time.


**Lesson 9 Setting Up Raw Projects** **394**


Another major difference is in the way the global wheel impacts the image. Whereas

the Primaries offset wheel affects the image uniformly, the global wheel pinches the

black and white points of the signal, rolling the shadows and highlights in order to

compress, but never clip, either extreme of the waveform. As a result, adjustments to

the exposure and saturation of a video signal have less impact in the shadows and

highlights, which produces more natural-looking changes.


TIP The High Dynamic Range palette is designed for optimal performance in

Resolve Color Management or ACES managed projects. When RCM or ACES is

enabled, the HDR palette is permanently “color space aware,” meaning it

automatically maps its own operational color space to the source image,

producing perceptually uniform results while maintaining careful control of

image saturation. Despite the name, you can use the HDR palette with both

SDR and HDR media, whether or not you enable color management.


The Temp and Tint sliders on either side of the global color wheel are also uniquely

mapped. They are designed to travel the image trace across the _Planckian locus_, which

represents the natural path of light temperature in the CIE 1931 chromaticity graph.

This results in more natural temperature changes in the image.


**Lesson 9 Setting Up Raw Projects** **395**


Although you will be familiar with the adjustment controls across the bottom of the

palette, some controls also exhibit behaviors unique to the HDR palette:


 - **Temp** and **Tint** are numeric representations of the global wheel sliders and can be

used when you need more accuracy or to reset the values.

 - **Contrast** and **Pivot** keep perceptually constant saturation when adjusted. This is

advantageous for HDR grading, where high contrast can lead to oversaturation in

the highlights.

 - **Black Offset** determines the minimum value of the video signal (i.e., the black

point) while gently compressing the data above it.


**4** Begin the grading process by reviewing the waveform scope.


Overall, the waveform looks good; there is no obvious clipping in the highlights or

shadows. However, much of the trace representing the foreground appears bunched

near the bottom of the graph, resulting in flat, dark midtones. Also, the top of the trace

appears compressed along a narrow range, limiting the detail you can see in the

clouds. You will address both of these issues using the HDR palette.


The global wheel is a good starting point for establishing the overall exposure of a clip.

Due to the even distribution of the waveform, you can leave the Global Exp (0.00)

parameter as is.

**5** To establish the overall image saturation, drag Sat (1.40) under the global wheel. Note

that due to the unique global luminance mapping, saturation is not increased as

aggressively in the shadows or in the clouds.


**Lesson 9 Setting Up Raw Projects** **396**


With the global values set, you can proceed to the individual tonal zones. The six

default zone wheels are divided into two categories: dark zones and light zones.


The preceding graph represents the order of the default zones in the palette and their

respective tonal ranges. The closer to the edges you travel, the more dedicated the

tonal zones become.


The Shadow and Light wheels have the broadest impact and overlap each other by a

factor of two stops. They each have narrower tonal ranges within them that allow you

to create contrast in the dark and light zones.


You will address the dark zones first.

**6** Bank the HDR palette wheels until you see the three dark tonal range color wheels:

Black, Dark, and Shadow.

**7** Drag the Dark wheel Exp (-0.40) to accentuate the shadows in the foreground bushes.

This range is narrow enough not to impact most of the foreground midtones.

**8** To enhance the foreground saturation, increase Sat (1.20) in the wider Shadow zone.


Next, you will work on the light zones to reveal the cloud details in the sky.

**9** Bank the HDR palette wheels until you see the three light zone color wheels: Light,

Highlight, and Specular.


To create room for expansion in the highlights, you must lower the top section of

the waveform.


**Lesson 9 Setting Up Raw Projects** **397**


**10** Drag the Highlight Exp (-0.80) left until the top of the waveform sits just under the

third horizontal line from the top.


You now have room to expand the very top of the highlights.

**11** Drag the Specular Exp (1.50) right to lift the top of the waveform trace, revealing fine

cloud details in the viewer.


The default tonal range graph seen in step 6 shows that the Highlight and Specular

zones both overlap the broad Light tonal range. This means you can use the Light zone

to make broader exposure changes while maintaining the established contrast in the

narrower zones.

**12** Drag the Light Exp (0.40) right to lighten the sky while keeping the cloud detail intact.

**13** Drag the Light color wheel control point slightly toward blue to add more color

to the sky.


TIP In the HDR palette options menu, you can change the numeric

representation of the control point position under the Exp and Sat

parameters. Display X and Y allows you to adjust the control point horizontally

and vertically. Display Angle and Strength will move the control point in a

circular motion to determine hue and on a radius to determine saturation.

These controls can be useful when making very fine adjustments using the

numeric fields instead of the color wheel control point.


Several options allow you to review and modify how the tonal zones affect the image.


**Lesson 9 Setting Up Raw Projects** **398**


**14** Click and hold the symbol to the left of the Light zone name.


This allows you to preview which areas of the image are impacted and determine

whether the zone needs adjustment.


In this case, the Light zone affects too much of the foreground and should be reduced.

**15** For a permanent view of the tonal zone selection, click the Highlight button in the

upper left of the viewer. Highlight mode will display the selection of the tonal zone you

are working on, leaving you free to make range and falloff adjustments.


NOTE When using the viewer’s Highlight mode with other tools, such as the

qualifier, Power Windows, or Color Warper, ensure that the HDR palette is not

active in the left palettes to avoid seeing a tonal zone selection instead.


Every zone color wheel is surrounded by two sliders: Min/Max Range and Falloff. The

Min/Max Range slider determines the zone limit, while the Falloff gently fades the

selection to avoid harsh edges when grading.


Let’s review the HDR Zone panel to better understand how the tonal zones were

distributed across this image.


**Lesson 9 Setting Up Raw Projects** **399**


**16** In the HDR palette header, click the Zones Graph button.


The Zones Graph is an additional panel in the HDR palette that allows you to further

customize the tonal zones.


On the left is a sidebar featuring the names of the zones, which you can click to

highlight their range indicator on the graph. Drag the indicator by the handle to

change the minimum or maximum range of a zone. The range will impact the entire

section in the direction of the handle arrow, with a falloff indicated by the soft red

transition. You can also use the sliders below to adjust and reset the range and falloff

values. These parameters are mapped to the sliders on either side of the zone color

wheels in the Controls panel.


Projected on the graph behind the indicators is a histogram of the frame in the viewer.

This histogram can help determine where range indicators should be placed and how

soft the falloff should be. Note that if a histogram signal ends before the start of a range

indicator, that zone will have no impact on the image when adjusted in the HDR palette.

In this instance, there’s nothing to the left of the Black zone, meaning that changes to

the Black zone color wheel, exposure, and saturation will not impact the image.


TIP If you cannot see a histogram in the Zones Graph, adjust one of the HDR

palette parameters or move the playhead slightly in the viewer. This will force

the histogram data to cache.


**Lesson 9 Setting Up Raw Projects** **400**


**17** In the Zones Graph, drag the Light range indicator to +0.10. The selection in the viewer

contracts, resulting in better separation of the branches and mountaintops from the sky.


This adjustment may feel similar to using the Low and High Range parameters in the

log wheels palette. The range slider allows you to refine the tonal range that a given

wheel impacts.

**18** Disable Highlight mode in the viewer.


Before After


**Lesson 9 Setting Up Raw Projects** **401**


##### **Correcting Scenes with a Wide Dynamic Range**

Scenes captured with HDR cameras sometimes feature dramatic shifts in exposure in

different areas of the same frame. Common examples include windows in interior scenes

or when shooting someone against a bright sky outdoors. With standard correction tools,

you would need to use a combination of secondary grading techniques for optimal results.

The HDR grading palette allows you to address a range of exposure levels using just one

primary tool.

**1** In the HDR palette header, return to the Controls panel (color wheels).

**2** Select clip 03 (D007).


The scene is split between two different lighting environments: the underlit interior of

the store and the overexposed windows.

**3** Label node 01 **HDR balance** .


First, you will review how the HDR palette tonal ranges are distributed across

this image.


**Lesson 9 Setting Up Raw Projects** **402**


**4** To open the Zones Graph panel without hiding the HDR color wheels, click the Expand

button in the HDR palette header.


This action opens the Zones Graph in the central palettes of the color page, allowing

you to grade and modify the tonal ranges simultaneously.


Overall, the tonal range layout and distribution appear appropriate for the scene’s

histogram, which is evenly spread through the graph. Because the window and the

light spill in the room compose a smaller portion of the image than the interior, you will

likely need to adjust the Light range at some point. However, it’s too early to determine

how the Light zone should be defined, so you’ll return to it later.


TIP You can create a custom zone in the HDR palette by clicking Create New

Zone at the bottom of the Zones Graph sidebar. Like the preset zones, a

custom zone can be defined as either light or dark and will appear as a color

wheel with unique range and falloff parameters in the Controls panel.


Since you will not be focusing on the global wheel as much for this clip, you have the

option of banking it together with the other wheels so that the HDR palette can

represent four unique tonal zones at once.

**5** Click the options menu and select Bank Global with Color Wheels. If needed, you can

still access the global wheel by banking to the rightmost wheel.


First, you will prioritize restoring the scene’s interior, which is where the audience will

predominantly be looking.

**6** Increase the Shadow Exp (1.00) to brighten the shop interior.


**Lesson 9 Setting Up Raw Projects** **403**


**7** Increase the Shadow Sat (1.10) to make the colors in the shop more vibrant.

**8** Increase the Shadow Range (+3.00) to spread the adjustment throughout the room.

**9** Increase the Shadow Falloff (0.30) to soften the spread, returning shadows to the walls.

**10** Increase the Dark Exp (0.30) to lighten the darkest elements in the room.


Next, you will use the light zones to fix the overexposed window.

**11** Decrease the Highlight Exp (-0.70) until the waveform’s flat top sits just under the top

of the waveform graph.

**12** Raise the Light Range (+2.20) to limit the adjustment to the window area.

**13** Decrease the Specular Exp (-0.90) to add contrast to the darker elements outside

the window.


TIP You can save a custom zone layout by opening the HDR palette options

menu and selecting Save As New Preset. Zone presets can be helpful if you

regularly process footage from the same camera with similar lighting

compositions (such as interviews or set shoots).


Finally, you will address the scene balance.

**14** Reduce the Temp (-2000) and Tint (-7.00) to balance the color cast on the walls.


Before


**Lesson 9 Setting Up Raw Projects** **404**


After


When outputting to an SDR standard, grading raw media is almost no different from

grading non-raw media. The wide dynamic range demands increased attention and

handling, but the creative primary and secondary workflows remain mostly the same.


When outputting to an HDR standard, special care must be given to the waveform

distribution. Although there is some variety in industry approaches and individual colorist

preferences, it’s generally considered a good idea not to overwhelm your audience with

superbright elements. Aim to place the majority of midtone environments in the 100-nit

range, allowing for some fluctuation to emphasize shadows and upper midtone detail.

Reserve the areas above the 100-nit line for light sources and surfaces hit by direct sunlight.


**Mapping the HDR Palette to Color Panels**

The HDR palette is designed to be mapped to the DaVinci Resolve Advanced and

Mini Panels, even when incorporating custom tonal zones and presets.


Advanced Panel: Press SHIFT + AUTO COLOR. All HDR palette controls will be

mapped to the center panel soft buttons and rotaries, while the zones will be

mapped to the trackballs and rings. Press the < and > soft keys to navigate all

available zones.


Mini Panel: Press USER and then press the HDR soft key above the left display. All

HDR palette controls will be mapped to the soft keys and knobs, while the zones

will be mapped to the trackballs and rings. Press the PREV ZONE and NEXT ZONE

soft keys to navigate all available zones.


**Lesson 9 Setting Up Raw Projects** **405**


## **Setting Up a Render Cache** **for Raw Media Projects**

In Lesson 8, you set up your project render cache to a full-quantization (444 or 4444),

12-bit depth codec, but the exercise did not detail the effect this had on the grading

process. In this exercise, you will change the render cache quality to observe its impact on

the image in the viewer and gain an understanding of why the render cache format

matters when working with raw video.

**1** Select clip 01 (C001).

**2** Open Project Settings and click the Master Settings tab.

**3** Scroll down to the Optimized Media and Render Cache section and set the “Render

cache format” to a lower-quality codec such as ProRes 422 Proxy (macOS) or DNxHR

LB (Windows).

**4** Click Save to close the Project Settings.

**5** If caching is not enabled in your project, choose Playback > Render Cache > Smart.

Wait until clip 01 is re-cached.

**6** If you do not see a change in the viewer, drag the playhead slightly to refresh the

active frame in the viewer.


Caching the raw video in a lower-quality format produces a posterized image with

pronounced banding in the sky.


**Lesson 9 Setting Up Raw Projects** **406**


Instead of a smooth blue gradient, the sky now appears to be made up of blue, purple,

and gray stripes. This is the result of using a render cache format that can only

represent a limited amount of luminance and color values. The impact is so severe that

it is even visible in the waveform.


In addition to being a poor representation of your grade, a low-quality render cache

format can also interfere with your ability to accurately make qualifier selections or

view the results of analytical tools, such as noise reduction or the Magic Mask. If you

use a slightly higher-quality render cache format, you might experience reduced

artifacting in the viewer, but the image grading potential will still be compromised.

**7** Open Project Settings and click the Master settings tab.

**8** Set the Render cache format to one of the full-quantization (444 or 4444) or HDR formats.

**9** Click Save to close the Project Settings.


When setting a render cache format, remember that it affects only what you see in the

viewer. If you were to render a clip from the deliver page while caching in a low-quality

codec, the exported image would not have banded gradients or compression artifacts.

This is why it is advisable to use high-quality render caching when grading HDR and

high-bit depth footage. If you don’t, your final project could end up looking different from

what you saw in the viewer.


The Render Settings of the deliver page include an option to “Use render cached images”

in the final deliverable. This option saves you time when exporting a project. Since 12-bit

depth codecs (such as DNxHR 444 and ProRes 4444) are HDR compliant, you can use

these render-cached materials to generate cinema and streaming deliverables.


**Lesson 9 Setting Up Raw Projects** **407**


## **Self-Guided Exercises**

Complete the following self-guided exercises in the Blackmagic RAW Timeline to get more

practice using the HDR palette.


**Clip 02 (C003)** Use the HDR palette to produce a well-lit image with warm, saturated skin

tones. Increase the color separation by saturating the orange clouds against the blue sky.


**Clip 04 (E004)** Use the HDR palette to illuminate the cable car against the dark

background. In a new node, make the car stand out by turning the interior a cool blue. Use

a Power Window if necessary. Create a final node to denoise the clip and find its optimal

placement in the node tree.


After completing these exercises, open **Blackmagic RAW Project COMPLETED.drp** and

review Blackmagic RAW Timeline COMPLETED to compare your work with this “solved”

timeline. If the media appears offline, click the red Relink Media button in the upper left

corner of the media pool and specify the location of the Project 03 Blackmagic RAW media

on your workstation.


**Lesson 9 Setting Up Raw Projects** **408**


## **Lesson Review**

**1** When color managing raw media, where do you set the input camera format?

**2** True or False? You can change the ISO and white balance of raw media at any time.

**3** What does banking accomplish in the HDR palette?

**4** Which tonal range is wider, Shadow or Highlight?

**5** True or False? Caching should always be disabled when grading.


**Lesson 9 Setting Up Raw Projects** **409**


##### **Answers**

**1** Trick question! DaVinci Resolve automatically detects the camera format of imported

raw media, so there is no need to “set” it. To access the raw debayer parameters of a

specific camera, open the Camera RAW project settings and select the RAW profile you

wish to adjust.

**2** True. Because of the unique photometric encoding of raw media, it’s possible to adjust

the ISO and white balance at any stage of the grading process.

**3** Banking refers to navigating between the tonal zone wheels in the HDR palette.

**4** In the default preset layout, the Shadow wheel has a wider tonal range than the

Highlight. However, both zones can be modified as needed.

**5** False. When using a lower-quality render cache format, you might want to disable it

when reviewing your final grade before delivery, but enabling cache rendering during

grading will help substantially with real-time playback. If using a higher-quality render

cache format (12-bit depth with full quantization), it’s acceptable to leave caching on at

all times and even include the cached files in the final project render.


**Lesson 9 Setting Up Raw Projects** **410**


### Lesson 10
# Delivering Projects



When you’re ready to export a

project—whether at the end of a

workflow, at an intermediate point, or

when generating dailies—its render

settings are configured in the deliver

page of DaVinci Resolve.


In this lesson, you will review a project

with clients, explore existing presets,

output for digital cinema, and set up

your own custom renders.



Time

This lesson takes approximately
2.5 hours to complete.

Goals

Using Lightbox to Check
Timelines Before Delivery 412

Reviewing Projects with Clients 416

Understanding the Render
Workflow and Presets 423

Creating Custom Renders 429

Configuring a Timeline
for Digital Cinema 431

Exploring Advanced
Render Settings 438

Lesson Review 447


## **Using Lightbox to Check** **Timelines Before Delivery**

The Lightbox feature of the color page gives you an alternative, expanded representation

of the timeline. It provides a general overview of clips in the edit rather than the default

viewer-focused layout of the color page. It is particularly powerful when combined with

filters and can be used to quickly assess the grade status of timeline clips.

**1** Launch DaVinci Resolve 20.

**2** Import and open **Project 03 - The Long Workday Commercial COMPLETED.drp** .

If necessary, relink the media by clicking the red Relink Media button in the upper

left corner of the media pool and specifying the location of the Project 03 media on

your workstation.

**3** Enable caching by choosing Playback > Render Cache > Smart.

**4** In the Project Settings, set the Render cache format to one of the full quantization

formats (444 or 4444).

**5** Enter the color page.

**6** Use the dropdown menu at the top of the viewer to open Lesson 10 Timeline.

**7** In the upper right of the color page, click the Lightbox button.


**Lesson 10 Delivering Projects** **412**


The Lightbox is a full-screen representation of your project timeline from left to right,

top to bottom. A ruler to the right of the window indicates the timecode of the clips

and turns into a scroll bar when a timeline has more clips than can be displayed in a

single panel.


This expanded overview of the timeline’s thumbnails can be helpful for colorists who

find the Thumbnail timeline in the color page too restrictive. With a glance at the

Lightbox, you can determine which clips are graded and which aren’t.

**8** Click the Information button in the upper left corner of the Lightbox panel to display

clip numbers, timecodes, and video track numbers above the clip thumbnail and

double-click to view a rotation of codecs, source names, and version information

underneath.


**9** Next to the Information button, click the Clip Filter button to expand the

filtering options.

**10** In the Clip Filter list, click Ungraded Clips.


The Lightbox panel is reduced to just three clips. The first two clips clearly belong in

the Garage group but must have been overlooked during grading.


**Lesson 10 Delivering Projects** **413**


**11** Select both clips and choose Groups > Garage > Assign to Group.


Most of the grading in the Garage group was carried out in the post-clip stage, so the

two clips will immediately adopt the look of the rest of the group. They will remain in

the Lightbox panel until the next time you change the filter, after which their new

status as graded clips will be acknowledged.

**12** In the upper left of the page, click the Color Controls button to open the grading

palettes in the lower half of the screen.


If you’re working with an external monitor, you will see a full-screen output of the

selected clip in the Lightbox. This allows you to continue grading and tweaking your

media in Lightbox mode.

**13** With clip 01 still selected, in the Primaries log wheels, raise the Shadow master wheel

to lighten the dark suit and hair.

**14** Select clip 03.


The last filtered clip is the solid white matte at the end of the sequence, which doesn’t

require grading. However, due to the CST-node based color management of this

timeline, if you want the luminance of the final node to be consistent with the rest of

the media (especially in high dynamic range deliverables), you will want to apply the

same color management.

**15** In the Clip Filter list, select All Clips to return the full contents of the timeline to the

Lightbox panel.

**16** Middle-click clip 26 to transfer the INPUT CST and OUTPUT CST nodes to the white

matte clip 27.


**Lesson 10 Delivering Projects** **414**


Next, you’ll review the status of the denoise nodes in the timeline.

**17** In the Clip Filter list, select Noise Reduction.


When performing noise reduction in Lesson 8, you learned that disabling the Denoise

node would facilitate faster playback during the grading process. If you use this

performance optimization method, you must remember to re-enable noise reduction

nodes before exporting a project.

**18** Click the Lightbox button in the upper right corner to close the Lightbox interface.


The Noise Reduction filter is still active in the timeline on the color page.

**19** Navigate the four clips one by one and ensure their Denoise nodes are all enabled.

**20** Select Clips > All Clips to remove the timeline filter.


TIP Changing the timeline thumbnail mode is another great option for visually

assessing the status of clips in the Lightbox panel. Choose View > Timeline

Thumbnail Mode > Source (C Mode) to switch the order of the clips in the

timeline from their edit order to the order in which the media was created.

When working with original camera footage, this will display the order in which

the footage was recorded. C Mode places clips captured on the same day/

location next to each other, making for faster matching, grade copying, and

visual assessment. When done, remember to set the Timeline Thumbnail

Mode back to Record (A Mode).


The timeline has now been checked to verify that all clips are graded and all necessary

nodes are active. When working on your own projects, think about the types of workflows

you use and what is important to verify before delivering a project.


**Lesson 10 Delivering Projects** **415**


In addition to the default filters already present in the Clip Filter panel, you can also use the

Smart Filters option at the bottom of the list to design filters based on the metadata of the

clips in the timeline.
## **Reviewing Projects with Clients**


Before rendering a finished project, you will usually also go through a review process with

your clients or collaborators to ensure everyone is satisfied with the final edit. Ideally, this

would occur in your editing or grading suite, but that is not always possible in remote or

international productions. DaVinci Resolve offers several tools that simplify the

reviewing process.

##### **Remote Monitoring**


Remote monitoring allows you to transmit the image in your viewer to a client’s monitor or

viewing device for real-time collaborative feedback. To use this feature, you and your client

must both have:


- DaVinci Resolve Studio, which includes the DaVinci Remote Monitor app upon

installation

- [A Blackmagic Cloud account, available at https://www.blackmagicdesign.com/](https://www.blackmagicdesign.com/)

- For Linux and Windows users, an RTX series NVIDIA GPU


NOTE The DaVinci Remote Monitor app is available in the App Store, which means

Apple iPhone and iPad devices can be used as client monitors. This setup does not

require the client to have DaVinci Resolve Studio.


With these conditions met, setting up Remote Monitoring as a host takes only a

few moments.


NOTE DaVinci Resolve Studio is required to complete the following exercise.


**1** Choose Workspace > Remote Monitoring.

**2** If prompted, sign in to your Blackmagic Cloud account.


**Lesson 10 Delivering Projects** **416**


**3** In the Remote Monitor window, select the Video Codec and Bitrate you wish to use for

the session.


Ensure both you and your client support the codec and choose a transfer speed

compatible with your connection bandwidths. A 10-bit depth will give greater image

accuracy, but 8-bit depth is substantially less processor-intensive to transmit.

**4** Select “Automatically accept connections” if you wish your client to connect to your

viewer as soon as they input the session code. Otherwise, leave it unchecked to

manually approve the link request.

**5** Click the Start Session button.


A session code is generated, and a red timer appears above it. Below, a list keeps track

of active session participants.

**6** Click the Copy icon to the right of the session code field and paste the code to your

client using any text-based communication method (email, text message, etc.).


**Lesson 10 Delivering Projects** **417**


Once the client has input the session code, a link will be established between their

monitoring device and your video output signal. You can proceed to playback, pause,

and scrub the footage while communicating with the client. They will not see your

DaVinci Resolve user interface.


TIP If you collapse the Remote Monitor window, you can always retrieve it by

clicking the Remote Monitor icon in the lower left of the DaVinci Resolve

interface.


As a client, a remote monitoring connection also requires just a few steps:

**1** Launch the DaVinci Remote Monitor app on your device.

**2** Sign in to your Blackmagic Cloud account.


TIP If you know the host’s server IP address, you can access the remote

monitoring session without a Blackmagic Cloud account. Click Use Remote

Monitor without Blackmagic Cloud to access the IP login fields.


**3** In the Session Code field, paste the code shared by the host.


**Lesson 10 Delivering Projects** **418**


**4** Select the Output Display you wish to use for monitoring.

**5** Click the Join button.


When a remote monitoring session is completed, the host must open the Remote Monitor

window and choose End Session.


TIP In DaVinci Resolve Studio, you can opt to share your viewer overlays with the

client monitor. When a remote session is running, go to the viewer options menu

and choose “Show Viewer Overlays on Remote Monitor.” This option is popular

among field colorists who might use a system in a remote location while grading

on a local monitor

##### **Uploading Presentations**


Blackmagic Presentations is an online service that hosts timelines in Blackmagic Cloud for

more in-depth review and collaboration. The Presentations page features video

conferencing tools that allow teams to remotely review and comment on edits in real time.

Contributors can even add time-based notes and annotations, which will appear as

markers on the host’s timeline in DaVinci Resolve.


Timelines can be uploaded to Presentations via the deliver page or the Quick Export

button in the cut, edit, and color pages.

**1** [In your web browser, go to the Blackmagic Cloud webpage (https://apps.cloud.](https://apps.cloud.blackmagicdesign.com/)

[blackmagicdesign.com/) and log in to your account.](https://apps.cloud.blackmagicdesign.com/)

**2** Click the Presentations icon.


Presentations can be thought of as projects or folders that can contain multiple

timeline renders (called “clips” in Presentations). You must create at least one

Presentation in your account before uploading a timeline.


**Lesson 10 Delivering Projects** **419**


**3** On the left side of the page, click Add Presentation at the bottom of the Presentations

sidebar and give it a name.

**4** Open DaVinci Resolve 20.

**5** In the color page interface toolbar, click Quick Export.

**6** In the Quick Export window, select the Presentations preset.


TIP Quick Export is one of the fastest ways to render videos for review or

upload them to social media and collaboration sites. The render settings

mirror those found in the default settings of the deliver page render presets.


**7** If necessary, sign in to your Blackmagic Cloud account.

**8** In the “Upload to” dropdown menu, select the Presentation to which you wish to

upload the timeline.


**Lesson 10 Delivering Projects** **420**


**9** Click Export.


Once the render and upload are complete, the timeline will be available as a “clip” in

the Presentations interface. Use the info symbol next to the presentation name to add

members and/or choose “Allow Guest access to presentation” to give access to

collaborators who don’t have a Blackmagic Cloud account.


Use the panel on the right to launch clips, navigate markers, and chat with other

members of the project.


**Multi-User Collaboration on Blackmagic Cloud**

Every project in this training manual was launched using a unique method—

restoring a DaVinci Resolve archive, conforming an XML timeline, cutting a self
contained video file with scene cut detection, and importing a DaVinci Resolve

project file. These projects were purposefully designed to demonstrate the variety

of ways that colorists launch timelines for grading. One option we have yet to

explore is using a collaborative workflow on Blackmagic Cloud.

_continues_


**Lesson 10 Delivering Projects** **421**


**Lesson 10 Delivering Projects** **422**


## **Understanding the Render** **Workflow and Presets**

The deliver page is designed to help you quickly set up one or more render jobs. Before

you dive into the intricacies of individual render parameters, it’s helpful to understand that

it takes only four steps to export a project from DaVinci Resolve:

**A** In the Render Settings panel, set up the compression parameters. These include the

file type, codec, and audio specifications, the filename and location on your

workstation, and various advanced controls to optimize render speed and file size.

**B** Define the timeline range you want to export. By default, each job is set to render the

entire timeline, but you can use In and Out points to define a custom range.

**C** Click Add to Render Queue to list the job(s) for exporting.

**D** Select the job(s) in the Render Queue and click the Render button.


In the following exercise, you will create a render job based on a preset in the

Render Settings.

**1** Enter the deliver page.


At the top of the Render Settings panel, you will find a horizontal list of render presets.


**Lesson 10 Delivering Projects** **423**


**Custom Export** opens the full range of render settings in the panel below.


**ProRes**, **H.264 Master**, **H264. HyperDeck**, and **H.265 Master** produce everything

from high-end exports appropriate for broadcast (ProRes) to compressed HD/UHD

files for client review and online upload (H.264 and H.265). Note that the ProRes

Master preset is available only on macOS systems.


**YouTube**, **Vimeo**, and **TikTok** optimize the Render Settings panel based on video

configurations recommended by user-generated content and social media websites.

Enter your login details in Preferences > Internet Accounts to upload videos directly to

your account upon render.


**Presentations**, **Dropbox**, and **Replay** render and automatically upload rendered

timelines to Presentations and Dropbox file-hosting services.


**Lesson 10 Delivering Projects** **424**


**IMF** features a set of SMPTE ST.2067-compliant resolutions and codecs for tapeless

network deliverables. In DaVinci Resolve Studio, this option does not require a license

and supports multiple media streams for video, audio, and subtitle tracks.


NOTE The Interoperable Mastering Format (IMF) is used for broadcast

distribution and online streaming services such as Disney+, Netflix, and

Sony Pictures.


**Final Cut Pro 7/X**, **Premiere XML**, and **AVID AAF** accommodate return trips to their

respective NLE software. This assumes a workflow in which media is edited in a

third-party NLE, migrated to DaVinci Resolve for grading or VFX, and then returned to

the same NLE for final delivery.


**Audio Only** disables video output and delivers a single audio-only file. You can specify

the audio file format in the Audio tab of the Render Settings.


**Pro Tools** renders three files: a self-contained video for reference, individual exports

of all audio clips and their channels, and an AAF file for Avid Pro Tools migration. This

preset accommodates workflows in which the final audio mix is mastered by an

external audio engineer in Pro Tools.


**Lesson 10 Delivering Projects** **425**


**2** Click the disclosure arrow next to the YouTube preset and choose 2160p to load the 4K

UHD version of the preset.


The Render Settings panel displays a limited set of parameters for the selected

YouTube preset.


**Lesson 10 Delivering Projects** **426**


To name the video file, you will use the File Name and Location fields under the

horizontal preset list.

**3** Click the empty text field next to File Name and enter **Workday_YouTube** .


The Location field identifies where the video file will be rendered. A job cannot be sent

to the Render Queue without an assigned location.

**4** Click the Browse button next to the Location text field.

**5** In the File Destination window, navigate to your Desktop, create a new folder called

**Exports**, and assign it as the render destination.


**6** In the Timeline panel, ensure that the render range is set to Entire Timeline.


**7** With the render settings configured and the timeline range defined, click Add to

Render Queue at the bottom of the Render Settings panel.


A pop-up dialog asks whether you want to export the project at a higher resolution

than your timeline. For the purpose of this exercise, you will confirm that this is

intentional.


**Lesson 10 Delivering Projects** **427**


TIP If you’re rendering a video project at a higher resolution than the original

footage, it is best practice to upscale the timeline in the Timeline or Project

Settings. This method will improve the rendered result, give you a more

faithful representation of the final image in the viewer, and allow you to apply

your grades and effects directly to the upscaled clips.


**8** Click Add to close the dialog.

**9** In the Render Queue panel, click the Job 1 title and rename it **YouTube** .


**Supporting Multiple Resolution Options**
**for User-Generated Content Websites**

Video players on user-generated content (UGC) websites such as YouTube or

Vimeo often offer the option to choose a playback video resolution. A lower
resolution video allows for smoother playback on a low-bandwidth internet

connection, whereas a higher resolution results in a better-quality image.


This change in resolution does not occur in real time within the UGC player.

Instead, every resolution of every video is generated at the time of the video’s

upload, which is why there is usually a wait period before an uploaded video goes

live. When switching between resolution options, the user is actually switching

between separate renders of the video as pre-generated by the host website.


For this reason, it is advisable to render and upload your video in the highest

possible quality and leave it up to the UGC website and the end user to determine

which resolution is best suited for playback.


**Lesson 10 Delivering Projects** **428**


## **Creating Custom Renders**

Presets are an efficient method of exporting projects quickly with the confidence that the

settings are appropriate for the intended destination. However, it’s valuable to understand

how and why certain settings are used and to be able to configure them to meet specific

needs, especially when your project deliverables extend beyond the destinations featured

in the presets list.


Most post-production professionals, from editors and compositors to audio engineers and

colorists, will configure render settings based on a wide range of factors. For deliverables,

it will be the industry or technical standards of a broadcast, transmission, or display

format; for collaborative workflows, it may be the software and hardware specifications

of the receiving department.


In this exercise, you will set up a render job to deliver dailies to an editor working on a PC.

**1** At the top of the Render Settings, click the Custom Export button.

**2** Under the File Name and Location fields, choose to render Individual Clips. Doing so

will export every clip in the timeline as its own video file. In the case of dailies, you’ll

want to place untrimmed clips on the timeline to ensure that the editor receives all the

media for every take.

**3** In the Video tab, set the Format to MXF OP-Atom.

**4** Set the Codec to DNxHD and the Type to 1080p 145/120/115 8-bit.


TIP Click the Expand button to the left of the Render Settings button in the

interface toolbar to expand the panel to the height of the deliver page. Click

the button again to collapse the Render Settings panel, extending the timeline

across the full width of the deliver page.


**Lesson 10 Delivering Projects** **429**


**5** The lessons throughout this training manual did not focus on audio syncing or editing;

however, in a dailies workflow, it is assumed that the audio from an external recorder

would have been sync’d to the video files before being assembled in a master timeline.

For this export, under the Audio tab, leave the Codec set to the high-quality Linear

PCM codec.


TIP Under Audio Normalization, the Normalize Audio checkbox allows you to

adjust the gain of your audio tracks to the loudness or peak (whichever

exceeds thresholds first) upon render. This ensures that the audio volume is

optimized for the listener. When choosing “Optimize to standard,” you can

customize the normalization standard, target level, and loudness values.


**6** Click the File tab to the right of the Audio tab to configure the dailies naming convention.


By default, “Filename uses” is set to “Custom name.” When working with dailies, it’s

advisable to preserve the original filenames (“Source name” in the Render Settings).

Doing so will enable you to quickly switch between offline and online media and

maintain consistency between post-production departments.

**7** In this case, you don’t want to use the source name because all the clips came from the

same video file (Project 3 - The Long Workday SCD.mov) and will overwrite one

another. Leave “Custom name” selected.

**8** Enter the Custom name underneath as **Workday Dailies** .

**9** To prevent them from overwriting each other upon export, select “Use unique filenames.”

**10** Choose Suffix as the method for distinguishing the files. This will append a string of

numbers to the render filenames.

**11** Uncheck “Add source frame count to filename” to simplify the naming convention.


The default filename suffix will be eight digits long, which is excessive for a timeline

with only 27 clips.

**12** Choose to “Use **2** digits in the filename.”

**13** At the top of the panel, click Browse to change the Location file path.

**14** In the Exports folder on the Desktop, create a subfolder called **Dailies** and select it as

the location.


**Lesson 10 Delivering Projects** **430**


**15** In the Timeline panel, ensure that the render range is set to Entire Timeline.

**16** Click Add to Render Queue.

**17** In the Render Queue panel, change the Job 2 title to **Workday_Dailies** .
## **Configuring a Timeline** **for Digital Cinema**


A digital cinema package (DCP) is a collection of media and metadata files used to project

digital movie files in a theatrical venue. DaVinci Resolve makes it possible to create a digital

cinema package with its integration of the DCP plug-in. The next few exercises combine

some practical information about DCPs with the configuration steps necessary to generate

a DCP in the deliver page.


**When creating a DCP, the timeline must be set to one of three 2K resolutions:**


- 2K Native (1.90:1) 2048 × 1080 @ 24, 25, 30, 48, 50, or 60 fps

- 2K Flat (1.85:1) 1998 × 1080 @ 24, 25, 30, 48, 50, or 60 fps

- 2K CinemaScope (2.39:1) 2048 × 858 @ 24, 25, 30, 48, 50, or 60 fps


**Or one of three 4K resolutions:**


- 4K Native (1.90:1) 4096 × 2160 @ 24, 25, 30, 48, 50, or 60 fps

- 4K Flat (1.85:1) 3996 × 2160 @ 24, 25, 30, 48, 50, or 60 fps

- 4K CinemaScope (2.39:1) 4096 × 1716 @ 24, 25, 30, 48, 50, or 60 fps


To avoid making major changes to the original timeline, you will make a duplicate and set it

up for DCP delivery.

**1** Go to the edit page.

**2** Right-click Lesson 10 Timeline and choose Duplicate Timeline.

**3** Change the new timeline name to **Lesson 10 Timeline DCP** .

**4** Right-click the new timeline and choose Timelines > Timeline Settings.

**5** Deselect Use Project Settings in the lower left corner.


**Lesson 10 Delivering Projects** **431**


The resolution for your DCP will be 2K Flat because it’s the closest resolution option

when starting from full HD. You’ll need to scale up the project slightly and crop the top

and bottom of the frame.


16 x 9 frame 1.78:1


Native 1.9:1


Flat 1.85:1


Scope 2.39:1


TIP 4K DCPs use a lower bit rate than 2K DCPs when played on 2K projectors.

For that reason, when your target projector is 2K, always make a 2K DCP, even

when working with higher-resolution content.


**6** Set the Timeline Resolution to 1998 x 1080 DCI Flat 1.85.


**7** Set Mismatched Resolution to “Scale full frame with crop.”

**8** At the top of the Timeline Settings window, select the Color tab.

**9** Change the Output color space to P3-DCI.


**Lesson 10 Delivering Projects** **432**


NOTE You will not be able to see the correct colors for this deliverable if you

do not output the video signal to a P3-DCI display.


**10** Click OK to close the Timeline Settings.


The project resolution and aspect ratio are now DCP-compliant. The timeline frame rate is

24 fps, which is also appropriate for DCP delivery. If you were working on a 23.976 fps

project, during DCP creation, it would be interpreted as 24 fps and audio playback would

be pulled up to match. Still, to ensure playback quality, it is advisable to record video and

audio for a standardized frame rate (24, 25, 30, 48, 50, or 60 fps) if you know you will be

delivering a DCP.


**What About the Output CSTs?**

When working with node-based color management, you must always be aware of

the two factors that affect the appearance and color space of your final project file.

The node CSTs map the pixel values of the image from one standard to another

(affecting appearance). The project (or timeline) color management settings are

responsible for the metadata embedded in the rendered file (designating the color

space). In this scenario, the Output CSTs would still need to be updated to output

to P3-DCI Gamma 2.6 (instead of Rec.709). This is easy to do when working with

template node trees (and using the rippling action) or by placing the Output CST

onto the Timeline Node Editor.

##### **Setting Up a DCP Render**


With the resolution and frame rate appropriately set up, all further output parameters can

be configured in the Render Settings panel.


The DCP format in DaVinci Resolve 20 Studio features two codec options. The Kakadu
based JPEG 2000 standard needs no license and delivers unencrypted digital cinema

packages. The easyDCP format encrypts digital media but requires the purchase of a

licensing package.

**1** Go to the deliver page.

**2** In the Render Settings panel, click Custom Export.

**3** Near the top of the panel, select Single Clip. Unlike the dailies, you want this timeline to

be rendered as a single self-contained video file.


**Lesson 10 Delivering Projects** **433**


**4** In the Video tab, set the Format to DCP.

**5** Set the Codec to Kakadu JPEG 2000.

**6** Set the Type to 2K DCI Flat.


TIP DCP uses the XYZ color space. The output color space set in the Projects

Settings > Color Management menu is automatically converted to XYZ during

the creation of the DCP file, even when project-wide color management (RCM

or ACES) is not enabled.


The “Use interop packaging” checkbox determines whether you are generating the

DCP based on the older but more widely supported Interop standard or the more

current and feature-rich SMPTE standard. One of the benefits of using the SMPTE

standard is that it supports a wider range of frame rates. The major benefit of using

the older Interop standard is that it is compatible with more theater projection

systems, though it is limited to either 24 fps or 48 fps.

**7** Ensure that “Use interop packaging” is selected.


“Clean” versions of deliverables are often required for localization. This is a version of

the edit without onscreen titles, lower-thirds, or baked-in subtitles for the benefit of

international distributors who will want to place translated text in the edit. The same is

often done for audio—dialogue is removed while music and sound effects are retained

for a clean deliverable that allows for international dubbing.


An easy way to prepare edits for clean video renders is to keep text elements on

separate tracks and disable them prior to rendering.

**8** Click the disclosure arrow to expand the Advanced Settings.

**9** Near the bottom, deselect Render All Video Tracks.


**Lesson 10 Delivering Projects** **434**


**10** Leave the default Disable set to Video 2 to remove “The Long Workday” text from the

final export.


If you had more video tracks in the timeline, you could use the + (plus) and – (minus)

signs to the right of the dropdown menu to disable as many tracks as needed.

**11** Leave all other settings as they are.


TIP Unencrypted DCPs can be played back on any DCP player/encoder without

restriction. The alternative DCP codec option, easyDCP, features an “Encrypt

package” checkbox for additional file security. This option will set the encoder to

generate a Digest containing the keys used during file encryption. With the Digest,

you can play the resulting DCP on your system and generate Key Delivery

Messages (KDMs) to allow the DCP to be played on other servers.

##### **Naming and Outputting a DCP**


DCPs follow a somewhat specific, yet voluntary, Digital Cinema Naming Convention for the

content title. For each version of a movie you create (such as the English 5.1 version, the

Spanish stereo version, the in-flight version, and so on), a composition playlist (CPL) is

created containing the appropriate content name. DaVinci Resolve’s DCP preset creates

this CPL for you and includes a straightforward way of generating a name that follows the

naming convention.

**1** Continue in the Video tab of the Render Settings.

**2** Scroll down and expand the Composition Settings.

**3** Click the Edit button next to the “Composition name” field.


This launches the Composition Name Generator window. Here, you can enter the

metadata that will be used to create a content title compatible with DCP servers and

theater management systems.


**Lesson 10 Delivering Projects** **435**


**4** Enter the Film Title as **TheLongWorkday**, leave the Content Type as ADV

(Advertisement), and set the Audio Language to EN (English).


TIP Separate the words in your project title using initial capitals—not spaces,

hyphens, or underscores.


The selected metadata is added to the composition name at the top. The F-185 in the

title refers to the projector aspect ratio based on the DCI Flat resolution you set in the

timeline settings.


**Lesson 10 Delivering Projects** **436**


**5** Click OK to close the window.


The composition name should not be confused with the package name that contains

the DCP. The package name is managed in the File tab of the Render Settings panel.

**6** Click the File tab and enter the Custom name as **Long Workday DCP test** .


Lastly, you need to select a destination for this DCP.

**7** Click the Browse button and select the Exports folder on your Desktop as the

render location.


When delivering a real film project, you can output the DCP to a hard drive in a Cru

Dataport DX-115 enclosure that will load directly onto many digital cinema servers and

is often required by film festivals. More conveniently, you can output to a USB 2 or

USB 3 hard drive or even a USB stick if it accommodates the film’s file size. Whatever

storage device you choose must be formatted as a Linux Ext2 or Ext3 drive. You can

use online resources to find various ways of accomplishing this on macOS and

Windows workstations.


TIP Some projection servers don’t provide enough power to mount USB
powered drives. To guarantee playback, use USB drives with an external

power source.


**8** In the Timeline panel, ensure that the render range is set to Entire Timeline.

**9** Click Add to Render Queue.

**10** A pop-up dialog will inform you of an Invalid Audio Track Count. This is due to the DCP

job anticipating a 5.1 audio mix, which is common with digital cinema deliverables.

Your project has a stereo output and will play without issue on most projection

systems. Click Add Anyway.

**11** In the Render Queue, change the Job 3 title to **DCP** .


When rendering a real film project, you will want to test it after generating the DCP file.

The only definite way to test your DCP is to rent a theater and run the projection just as

you would for an audience. That is the only way you can absolutely verify that the color

conversion (from your output color space to XYZ) worked correctly. DCPs can also be

tested by importing them back into a new DaVinci Resolve project file and managing the

color space from DCI X′Y′Z′ to your monitoring standard. It’s a quick way to verify that the

colors have not been corrupted due to incorrect color conversion, but a computer screen

will never be able to truly represent how a film will appear when projected.


**Lesson 10 Delivering Projects** **437**


## **Exploring Advanced** **Render Settings**

In addition to choosing how your footage is compressed, you have additional control over

more nuanced aspects of the rendering process. This exercise is designed to familiarize

you with these settings and empower you to set up your future custom renders more

purposefully.

**1** Return to Lesson 10 Timeline.

**2** In the Render Settings panel, select the Vimeo preset at the default 1080p resolution.


Presets are convenient as a quick starting point for renders, but they can be further

customized if unpacked in the Custom Export controls. In this exercise, you’ll produce

a video with a lower data rate than the default.

**3** At the top of the panel, scroll to the left of the presets list and click the Custom

Export button.


The panel reverts to its expanded custom layout but has adopted the Vimeo

preset settings.

**4** Ensure that the Video Format is QuickTime and the Codec is H.264.


For certain codecs, encoder acceleration options will appear under the Codec

parameter. If you’re using a workstation with an Nvidia NVENC GPU, you will see a

dropdown menu with options to accelerate your Native and GPU encoders.

Workstations offering QuickSync hardware encoding will display an option to use

hardware acceleration.

**5** Select Auto from the Encoder dropdown menu or select “Use hardware acceleration if

available” if you see either of these encoder options.

**6** Leave the Resolution at 1920 x 1080 HD and Frame Rate at Timeline Frame Rate (24

frames per second).


The Quality parameter in the Render Settings panel specifically refers to the data

rate—the amount of data per second required to transmit the audiovisual stream. A

higher data rate contains more visual information, which results in better motion

representation and detail quality, whereas a lower data rate selectively discards some

data to generate a smaller file size.


**Lesson 10 Delivering Projects** **438**


**7** Restrict the Quality setting to 7500 Kb/s. This will reduce the file’s data rate,

significantly lowering the file size while still maintaining a good level of visual quality.


TIP As counterintuitive as it seems, the resolution of a video has no impact on

its file size. Only the data rate determines the file size of a rendered video. If

you export 720p and 1080p versions of the same video at 8000 Kb/s, they will

have the same file size, although the 720p will likely look a little crisper, while

the 1080p video will have more macroblock artifacting as a result of using the

same amount of data to reproduce the image in a larger frame.

This is not true when using an Automatic Quality setting (such as Best), which

configures the data rate based on the timeline’s resolution.


The Encoding Profile determines the level of complexity involved with encoding an

H.264/H.265 file. They are listed from lowest (Base) to highest quality (High 4:4:4), with

Auto determining the optimal profile based on the timeline’s resolution and bit depth.

**8** Leave the Encoding Profile set to Auto.

Key Frames are full-data, intra-coded frames (also known as _i-frames)_ inserted into a

lossy video stream at regular intervals, such as every 30 frames. These i-frames are

reference points for re-creating the temporally compressed p- (predicted) and b- (bi
directionally predicted) frames that make up the majority of the moving image in a

distribution codec (such as H.264). The default Key Frames setting is ideal for most

project types. If you have very fast-moving imagery and see glitch effects in your

rendered video, increase the Key Frames frequency.

**9** Set the Key Frames to be grabbed every 24 frames to ensure slightly less distortion

during the video’s temporal compression and playback.


Frame reordering allows for the encoding of b-frames to improve the quality of the

resulting video file. It can be disabled for faster encoding at the expense of

visual quality.


**Lesson 10 Delivering Projects** **439**


**10** Leave “Frame reordering” enabled.


Many of the more specific parameters found under the Quality and Key Frames

controls are tailored to finishing artists with very specific deliverable needs. As a rule,

these controls are optimized to produce the best temporal compression results in your

operating system and do not need adjustment.

**11** Scroll down and click the disclosure arrow to see the Advanced Settings.


The “Pixel aspect ratio” allows you to indicate whether the video pixels are Square or

Cinemascope (rectangular). This option pertains to older workflows in which digital

footage recorded for analog television (at a rectangular 1.33:1 aspect ratio) was

converted for computer displays (with a square 1:1 aspect ratio). If your video looks

horizontally distorted (too squashed or stretched out), change the pixel aspect ratio.

**12** Leave the “Pixel aspect ratio” set to Square.


Data Levels specify the video signal range of the nonlinear luma Y’ component. The

default Auto setting renders the media at the data level appropriate for the selected

codec. Video refers to Y’CbCr formats that constrain the pixel data values between

64–940 in a 10-bit system in formats using a Rec.709 video standard. Full expands the

range to the film standard of 4–1023 values utilized in high-end digital film formats.


NOTE Data levels are automatically assigned based on the source footage

codec (upon import) and the codec you are rendering to (upon export). The

majority of codecs use video levels (also known as _legal levels_ ), while some

higher-end formats (like scanned DPX image sequences) use data levels (also

known as _full levels_ ).


If your final video looks substantially darker or lighter than it appears in the

viewer of the color page, the data levels may be incorrectly assigned. This can

sometimes happen when offline media is transcoded with a different codec

from the original media. To fix this, make test exports with the Data Levels set

to Video and/or Full until you find the correct data level.


**Lesson 10 Delivering Projects** **440**


**13** Leave the Data Levels set to Auto.


Color Space and Gamma tags allow you to embed colorimetry metadata into the video

file to be read and interpreted by operating systems and applications. These tags allow

you to overcome the color shift that can occur between the DaVinci Resolve viewer and

video players/browsers with an internal color profile.


**14** Leave the tags set to “Same as Project.” The resulting video file will be tagged with the

project’s output color space, regardless of whether project-wide color management

(RCM or ACES) is enabled.


NOTE When exporting from a Mac, you can change the Gamma Tag to

Rec.709-A to leave the transfer function metadata in the video file unspecified.

Apple’s applications will correctly identify and map the gamma based on

Apple’s internal color management system, while external devices will map the

signal to the universal BT.709 transfer function.


For a solution that transcends operating systems and browsers, you can opt to

bake in the Rec.709-A gamma into your video. This is not recommended for

professional broadcast and projection deliverables, but if you are uploading

videos to the web and want your audience to see the video the same way it

appeared to you in DaVinci Resolve’s viewers, make a duplicate of your timeline

and change the output color space to Rec.709-A. This will embed the gamma

into the video signal, meaning the contrast will appear consistent even if

uploaded to a UGC website that does not read/interpret gamma tags.


**Lesson 10 Delivering Projects** **441**


**15** Set the “Data burn-in” to None to ensure that the viewer’s data burn-ins will not appear

in the rendered video.


Selecting “Bypass re-encode when possible” will render a direct copy of the original

media file when possible. This option will have no effect if you have graded or

composited your media or if you’re exporting to a format different from the source.

For example, this setting could be beneficial if you were editing a project using ProRes

422 media, with the intention of delivering in ProRes 422. Bypassing re-encode will

deliver such a project at the highest possible quality.


**16** Leave “Bypass re-encode when possible” selected.


The next set of options, “Use optimized media,” “Use proxy media,” and “Use render

cached images,” allow you to include previously generated renders of the footage in

the final export. It makes sense to select these options when your optimized or proxy

media and render cache are set to a high or lossless quality codec.


The current project is set to cache renders at a high-quality 12-bit depth codec with full

quantization, so it makes sense to use the cached files in the final render to save time.

**17** Select “Use render cached images.”


The “Force sizing to highest quality” and “Force debayer to highest quality” options

bypass the quality settings for resizing and debayering in the Project Settings.

Selecting these is convenient when working on a processor-intensive timeline with raw

footage. You can initially adjust the Project Settings for lower-quality visual output

during editing but bypass these settings for the highest possible quality output upon

final render.

**18** Select “Force sizing to highest quality” to ensure that the optimal resize filter is used

during rendering.


**Lesson 10 Delivering Projects** **442**


**19** Selecting the debayer option is unnecessary because this project does not contain

any raw media.


“Enable Flat Pass” allows you to bypass grades as indicated in the version settings of

clips in the Thumbnail timeline. The default choice is Off, which means all grades will

remain intact. Choosing “With clip settings” means the render will consider the bypass

status of each version (as set in the Versions contextual submenu in the color page).

Choosing Always On will disable all the clip grades in the timeline, providing a quick

way to export an edited timeline or a set of dailies without clip grades.

**20** Leave Enable Flat Pass set to Off.

**21** Selecting “Disable sizing and blanking output” removes any transform changes and

blanking that were applied to the clips in the edit or color pages. Leave it unselected.

**22** In the File tab, at the top of the panel, set “Filename uses” to “Timeline name.” The File

Name field at the top will adopt “Lesson 10 Timeline” as the filename.

**23** In the Timeline panel, navigate to the last frame of clip 05 and press O to place an out

point (01:00:26:09). The dropdown menu at the top of the panel will show that you will

be rendering a custom In/Out Range.


**24** Click Add to Render Queue.

**25** In the Render Queue, change the Job 4 title to **Workday_HD_Preview** .

**26** In the options menu of the Render Queue, choose Show All Projects.


You should now see all the jobs that were added to the Render Queue in any project

associated with the project library you’re currently using. If you split longer projects

into reels, or if you’re working on timelines with different frame rates, you might want

to create all your render jobs first and then access and render them from a single

project Render Queue. That way, you won’t have to wait for a project to finish

rendering before launching the next render.


**Lesson 10 Delivering Projects** **443**


**27** In the options menu, deselect Show All Projects to return to the current project’s

Render Queue.


**Remote Rendering**

DaVinci Resolve Studio allows you to offload job rendering to a different

workstation. This feature requires that all workstations have a copy of

DaVinci Resolve 20 Studio installed, a shared Postgres project library, and access

to all necessary media files using the same filename paths. With one computer

acting as a render station, all other DaVinci Resolve workstations can continue

editing, grading, compositing, and mixing.

##### **Saving Presets**


When frequently outputting to the same standard, or working consistently with the same

collaborators, you may want to generate a preset of your settings so you can set up future

renders more quickly.

**1** In the options menu of the Render Settings panel, choose Save As New Preset.

**2** Name the preset **Client Preview** and choose a preset icon.


The custom preset appears on the left of the horizontal menu at the top of the Render

Settings panel.

**3** In the Render Settings options menu, choose Client Preview > Add to Quick Export.

**4** Go to the edit page to verify that your new custom preset has appeared in the Quick

Export panel.

**5** Return to the deliver page.


**Lesson 10 Delivering Projects** **444**


##### **Editing Render Jobs**

A job can be removed or modified even after it has already been added to the

Render Queue.

**1** Find the DCP job in the Render Queue and click the X in the upper right corner of the

job to delete it from the queue.

**2** Find the YouTube job and click the pencil icon at the top right corner to edit it.


The Render Settings panel changes to reflect the YouTube job settings. Additional

buttons (Cancel, Update Job, and Add New Job) at the bottom of the panel indicate that

a job is currently being edited.

**3** Change the Resolution to 1920 x 1080 HD.

**4** Change the Format to QuickTime.

**5** Click Update Job at the bottom of the panel to exit the Edit mode.


The change overwrites the original YouTube job settings.

**6** Click the YouTube job in the Render Queue panel.

**7** At the bottom of the panel, click Render 1.


Note that the remaining unselected jobs are not rendered. When delivering multiple

timelines or formats, ensure that you select all necessary jobs in the queue before

clicking the Render button. When no jobs are selected, the Render button is set

to Render All.


**Lesson 10 Delivering Projects** **445**


Using the correct render settings is vital for delivering technically correct, visually

optimized video project files. Understanding these settings has even greater benefits; it

elevates your skillset as a colorist and imbues confidence that your projects are delivered

at optimal quality while adhering to industry standards.


**Why Does My Deliverable Look Different?**

When you render a video, it may sometimes not look the same as it did in

DaVinci Resolve. Perhaps the saturation decreases, the hues shift, or there is a

change in contrast. There are many reasons why these things may happen:


 - Your operating system’s internal color management may display your video

differently in native applications than how it appears in DaVinci Resolve.

Ensure DaVinci Resolve is set up to use this display color management in the

General System Preferences.

 - Your main display may have a color profile that affects how the image looks

during grading. When viewed on an external device without the same color

profile, the final video will appear different. This can also be caused by an

uncalibrated monitor. In both cases, having a dedicated grading monitor

should help keep output consistent.

 - A third-party application (such as an NLE or a compositing software) may

incorrectly map the footage based on an assumed color space. Check the

input color space settings in the application and correct them to match that of

the footage.

 - The video file’s color space metadata might be incorrectly read by a video

player or online video host. Check whether tagging or embedding the color

space helps address the issue.

 - The wrong Data Level setting may result in a luminance shift. Try exporting at

a different data level.


Developing a workflow that produces consistent visual results is a necessary step for every

colorist, although it can be a frustrating one because there are so many variables that can

cause a color or gamma shift. Continue to experiment with your project and output

settings until you reach the consistency you need to deliver your projects with confidence.


**Lesson 10 Delivering Projects** **446**


## **Lesson Review**

**1** True or False? You cannot grade media while using the Lightbox panel.

**2** Which Blackmagic Cloud monitoring option allows your clients to leave comments on

your timeline?

**3** True or False? The deliver page supports roundtrip workflows with other

NLE programs.

**4** How would you ensure that the highest-quality debayer settings are used for the final

render of a raw project?

**5** How do you save a custom render preset?


**Lesson 10 Delivering Projects** **447**


##### **Answers**

**1** False. You can view and grade media in the Lightbox if you enable color controls and

have an external monitor.

**2** Clients can review and comment on timelines in Presentations.

**3** True. The presets at the top of the Render Settings panel allow you to select an NLE

program for a roundtrip delivery of individual video clips and an XML timeline.

**4** Select “Force debayer to highest quality” in the Advanced settings when exporting a

raw project.

**5** In the Render Settings options menu, choose Save As New Preset.

##### **Congratulations!**


You have completed **The Colorist Guide to DaVinci Resolve 20** and are now ready to

explore more editing, visual effects, and audio mixing workflows using the additional

certified books in this series.


Completing all the lessons in this book will have prepared you to become a certified

DaVinci Resolve color page end user. You can take the free online exam by following this

link: [bit.ly/R20color](http://bit.ly/R20color) or by visiting the DaVinci Resolve training page (link below) and clicking

the Complete Online Exam button under the Colorist Guide lesson files. When registering,

please select the Blackmagic Design Training Partner Country as ONLINE and the Training

Partner Name as BMD Training Page.


[www.blackmagicdesign.com/products/davinciresolve/training](http://www.blackmagicdesign.com/products/davinciresolve/training)


The exam is made up of 50 multiple-choice questions that must be answered within

a 1-hour limit. A passing score requires 85% accuracy or better. Every user has three

attempts at the exam, with a 24-hour wait period between attempts. If you are

unsuccessful after the third attempt, please wait 6 months before contacting

[learning@blackmagicdesign.com to request that three more attempts be added to your](mailto:learning%40blackmagicdesign.com?subject=)

account. The exam is open book and open software to encourage you to research

the questions as you answer them. Upon passing, your certificate will be emailed to

you automatically.


We also invite you to become part of the DaVinci Resolve community by joining the web

[forum on the Blackmagic Design website (https://forum.blackmagicdesign.com/). There,](https://forum.blackmagicdesign.com/)

you can ask questions about the creative aspects of filmmaking and connect with industry

editors, colorists, compositors, and audio engineers.


We hope that you have found DaVinci Resolve 20’s professional nonlinear editing and world
class color correction tools to be intuitive to learn and a perfect fit for your creative workflow!


**Lesson 10 Delivering Projects** **448**


### Appendix A
# Using the DaVinci Resolve Panels

Blackmagic Design manufactures a variety of control surfaces for use with

DaVinci Resolve 20. The DaVinci Resolve panels allow you to make faster, more

nuanced changes to your images without taking your eyes off the grading

monitor. Instead of being limited to color grading one click or drag at a time,

you can use the panels to adjust multiple controls simultaneously. This intuitive

approach can be the difference between taking 5 minutes to complete a shot and

taking just 30 seconds. Three control panels are available for DaVinci Resolve’s

color page: Micro, Mini, and Advanced.


DaVinci Resolve
Micro Color Panel


**Appendix A Using the DaVinci Resolve Panels** **449**


##### **DaVinci Resolve Micro Color Panel**

The DaVinci Resolve Micro Color Panel is a high-quality, portable wireless panel that

features three high-resolution trackballs and 12 precision-machined control knobs for

accessing essential primary correction tools. Soft keys throughout the panel reset grades,

grab and play stills, navigate the timeline and nodes, and feature many commonly used

grading actions and playback controls. Two shift keys triple the functionality of most of the

available controls, turning the trackballs into transform and Power Window controls when

needed. A horizontal slot across the top of the panel allows for the mounting of tablets,

such as the Apple iPad, for truly remote workflows. The DaVinci Resolve Micro Color Panel

is perfect for use on set to quickly evaluate colors and create looks for broadcast trucks,

for education, and for anyone who grades while traveling.

##### **DaVinci Resolve Mini Panel**


The DaVinci Resolve Mini Panel is a compact device packed with a massive number of

features and controls. You get three professional trackballs along with various buttons for

switching tools, adding color correctors, and navigating your node tree. The Mini Panel

also includes two 5-inch color LCD screens that display menus, controls, and parameter

settings for the active tool. Eight soft buttons and eight soft knobs give you direct access

to the menus of most of the palettes in the color page. The Mini Panel is ideal for users

who balance editing and color grading, users who wish to access both primary and

secondary color correction tools from their panel, and freelance colorists who need to

carry a panel with them when moving between facilities. It’s also great for colorists

working on location shoots, for corporate and event videographers, for houses of worship,

and many more.


**Appendix A Using the DaVinci Resolve Panels** **450**


##### **DaVinci Resolve Advanced Panel**

For the ultimate in speed, power, and control, Blackmagic Design offers the DaVinci Resolve

Advanced Panel. The Advanced Panel has been designed in collaboration with professional

colorists to work in total harmony with the software. This large panel consists of left, center,

and right consoles that give you quick, one-touch access to virtually every parameter and

control in the color page. The DaVinci Resolve Advanced Panel lets colorists instinctively

reach out and touch every part of the image, adjusting multiple parameters simultaneously

with complete responsiveness for a smooth grading experience. While the Mini Panel gives

you access to nearly all the color correction tools in Davinci Resolve, the Advanced Panel

gives you even more flexibility with physical buttons and knobs to control Memories, Open

FX tools, Dolby Vision, and many other speed- and workflow-based tools that further

increase your efficiency. The Advanced Panel also features a unique T-bar for playing back

gallery stills, shuttle controls for cycling through frames and speeding through your timeline,

and a slide-out keyboard. Used in many of the top color grading facilities around the world,

the Davinci Resolve Advanced Panel is the ultimate control surface for Davinci Resolve.


**Appendix A Using the DaVinci Resolve Panels** **451**


##### **DaVinci Resolve Mini Panel Overview**

The Mini Panel is mapped to virtually every tool and parameter in the color page while

sporting a compact design and an accessible price point. This makes it incredibly popular

among both professional colorists and industry newcomers. The following overview will

introduce you to its layout and key functions.























































**Appendix A Using the DaVinci Resolve Panels** **452**


To the right of the Gain trackball are useful playback and shuttle controls to help you

quickly navigate between clips, nodes, and frames. Some additional playback options

include Loop, which will repeat the playback of the currently selected clip; Bypass, which


will temporarily disable the selected node of a clip.









**Appendix A Using the DaVinci Resolve Panels** **453**


**This page is intentionally left blank** **454**


### Appendix B
# Setup and Delivery on Macs

This guide featured multiple tips for best practices when working on Mac

workstations. All these suggestions are consolidated in this sidebar for easy

reference when setting up and delivering projects on Macs.

## **Setting the Output Color Space**


If you’re using a Mac display, you’ll need to choose an output color space based on your

ICC display profile. To find the display profile in your macOS, go to System Preferences >

Displays > Color tab. On newer displays, the profile will usually be Display P3. To set the

correct output color space for Display P3 in the Project Settings, select “Use separate color

space and gamma” under “Color processing mode,” and in the “Output color space” field,

set the left parameter as P3-D65 and the right parameter as sRGB.
## **Using DaVinci Resolve** **with Mac Displays**


The macOS internal color management utility, ColorSync, uses metadata to match colors

between its applications. As a third-party software, DaVinci Resolve is not impacted by

ColorSync, which is why the videos rendered out of DaVinci Resolve might look different

when viewed in Safari or QuickTime. To avoid this, you can include DaVinci Resolve in

ColorSync’s internal mapping. Go to DaVinci Resolve > Preferences > System, and in the

General category, select Use Mac Display Color Profile for Viewers. This will enable

DaVinci Resolve to use whichever color profile you have selected in the macOS Color

preferences, including custom color profiles and calibration software profiles. Please

note that this will only affect the appearance of the footage in the viewers.


**Appendix B Setup and Delivery on Macs** **455**


## **Gamma Tags**

When exporting from a Mac, you can change the Gamma Tag to Rec.709-A to leave the

transfer function metadata in the video file unspecified. Apple’s applications will correctly

identify and map the gamma based on Apple’s internal color management system, while

external devices will map the signal to the universal BT.709 transfer function.
## **Rec.709-A as an** **Output Color Space**


For a solution that transcends operating systems and browsers, you can opt to bake the

Rec.709-A gamma into your video. This is not recommended for professional broadcast

and projection deliverables, but if you are uploading videos to the web and want your

audience to see the video the same way it appeared to you in DaVinci Resolve’s viewers,

make a duplicate of your timeline and change the output color space to Rec.709-A. This will

embed the gamma into the video signal, meaning the contrast will appear consistent even

if uploaded to a UGC website that does not read/interpret gamma tags.


**Appendix B Setup and Delivery on Macs** **456**


## **Index**

**NUMBERS**

2× Zoom, enabling, _132_

4K resolutions, _431_ . _See also_ _resolution_

4K to 1080p to 4K workflow, _349_

**A**

A/B Highlight Difference button, _85_

ACES (Academy Color Encoding System)
color management, _385–387_

Advanced Panel, _449_, _451_

mapping HDR palette to color
panels, _405_

advanced Render settings,
exploring, _438–446_

Advanced Settings, displaying, _440_

AI Depth Map effect, _38–42_

AI IntelliTrack, _353_

AI Magic Mask 2 palette, areas of, _296–304_ .
_See also_ _Magic Mask_

Alt key. _See_ _keyboard shortcuts_

analog video look, creating on
timeline, _336–337_

Anchor Point parameters, _158_

animating

grades using keyframes, _355–362_

position values with dynamic
keyframes, _356–358_

Aperture Diffraction settings, Output
category, _318_

archive, exporting, _164_

archive, opening, _4–5_

Artificial Sky, _105_

aspect ratios

changing, _162_

and resolutions, _347_

atmosphere, adding, _99–102_

attention

drawing, _74–78_

drawing by blurring background,

_308–309_



focusing with vignettes, _81–82_

attributes. _See_ _dynamic attributes_

Audio Normalization, _430_

Audio Only setting, _425_

AVID AAF setting, _425_

**B**

backed up files, opening, _7_

backgrounds, blurring, _308–309_

backups, setting up, _6–7_

Balance node, labeling, _304_

balancing and shot matching, _8_

balancing footage

comparing color and log wheels, _28–42_

grading workflow, _8–10_

opening DaVinci Resolve archive, _4–5_

precision grading with curves, _20–27_

primary grading with color
wheels, _11–20_

setting up project backups, _6–7_

base grades, applying at pre-clip group
level, _277–287_ . _See also_ _grades_

Beauty Resolve FX, _128_

Bézier-based contrast, _330_

BG node, labeling, _207_, _295_

bins. _See also_ _smart bins_

creating, _264_

organizing files into, _148–151_

bit rates, 4K DCPs, _432_

Blackmagic Cloud, collaboration
on, _421–422_

Blackmagic Cloud Store, media
sync with, _xx_

Blackmagic Design Training and
Certification Program, _xi_

Blackmagic RAW Timeline, creating, _383_

blanking, defined, _161_

Bleach bypass version, naming, _229_

blue dot, removing from viewer, _304_

Blue look serial node, creating, _195_


**Index** **457**


blurring backgrounds, _308–309_

Blush Retouching section, _127_

Breech Detail window, creating, _87_

brightening images, _36_

brightness, adjusting, _16_

broadcast versus grading monitor, _173_

BW serial node, labeling, _370_

BW still, labeling, _247_

**C**

cache, clearing, _377–378_

Cache files, location, Working Folders, _376_

cache quality, configuring, _375–376_

cached files, automating deletion of, _378_

caching process, _273_, _370_ . _See also_ _Fusion_
_Output Caching process_ ; _node cache_ ;
_sequence caching_ ; _Smart Cache_

Camera Raw palette, _393_ . _See also_ _raw_
_settings_

Car node, labeling, _305_

certification, getting, _xii_

chroma warping in viewer, _108–113_

Chyron.png graphic, _149_, _154–155_

Cinema Viewer mode, accessing, _233_

Client Preview preset, creating, _444_

clients, reviewing projects with, _416–422_

Clip Attributes, _152–153_

clip group level, making clip-specific
adjustments at, _288–292_ .
_See also_ _groups_

clip thumbnails, changing metadata on
display, _230_

clips. _See also_ _matching clips_ ; _media pool_
_clips_ ; _post-clip grade_ ; _raw clips_

adjusting after post-clip grades, _318–320_

comparing using split-screen
views, _68–69_

cycling through in viewer, _234_

intermediary matching
between, _293–294_

linking to active timeline, _153_

matching using waveforms, _292_

reframing individually, _347–349_



replaying, _91_

Select All option, _173_

Clips filter, resetting, _51_

clip-specific adjustments, making at Clip
group level, _288–294_

Cloud Opacity, increasing, _106_

Cloud Scale, reducing, _106_

Cloud Time, adjusting, _106_

Cloud Tracker option, _354_

codecs, _164_, _339_

collaboration on Blackmagic
Cloud, _421–422_

color adjustments, disabling, _26_

color and log wheels, comparing, _28–42_

color bar graphics and gradients, _34_

Color Bars compound clip, _188_

Color Bars mode, _58_

color charts, using to balance
groups, _285–287_

color coding tracks, _148–151_

color continuity

applying shot matches, _52–54_

comparing and matching shots, _61–69_

matching shots, _54–61_

organizing shots, _48–51_

shot-matching strategy, _46–48_

color correcting with curves, _24–26_

color correction, _8_

color data, including, _348_

color effects, compositing with layer mixer
node, _205–216_

color management. _See also_ _display-_
_referred color management_

with ACES, _385–387_

node-based, _277–287_

setting up, _170–176_

setting up for dynamic range, _170–176_

color monitoring, accuracy of, _177_

color page

entering, _5_

layout, _xxi–xxii_

color ranges, warping, _108_


**Index** **458**


color space finding middle gray of, _330_ .
_See also_ _output color space_

color values, changing over time, _360–362_

Color Warper versus HSL curves, _134_

color wheels, primary grading with, _11–20_

Colorist Guide subfolder, creating, _322_ .
_See also_ _project housekeeping_

Colorize option, _13_

colors. _See also_ _memory colors_

balancing with master wheels, _16–20_

neutralizing, _17_

ColorSlice palette, _331_

ColorTrace, using to migrate timeline
grades, _251–256_

Command key. _See_ _keyboard shortcuts_

comparing. _See also_ _matching shots_ ;

_Shot Match_

clips using split-screen views, _68–69_

and matching shots manually, _61–69_

parades side by side, _64_

results, _100_

work to source footage, _53_

complimentary
hue, adding, _17_ . _See also_ _Hue_

content, delivering in multiple
standards, _178_

contrast, setting, _21–24_

contrast balance, redefining, _34_

Contrast node

labeling, _217_, _326_

selecting, _60_

Contrast serial node, labeling, _228_

control menu, _xxiii_

control panels, _4_

control points

creating, _23_

moving with precision, _131_

copying

grades or stills, _348_

grades using Timelines album, _256–258_

nodes, _237–238_

Corrector header, _357_



corrector nodes

blend modes, _204_

disabling and re-enabling, _42_

operations within, _186_

Coverup node, labeling, _219_

Coverup serial node, creating, _350_, _352_

cover-ups, creating with Patch Replacer
effect, _352–355_

CSTs (Color Space Transforms), _277_ .
_See also_ _monitoring LUT_

node-based color management, _277–282_

using in groups, _282–284_

Ctrl key. _See_ _keyboard shortcuts_

Curve palette, HSL curves, _129_

curves

color correcting with, _24–27_

in color page layout, _xxi–xxii_

isolating, _65_

setting contrast, _21–24_

Curves palette

black point, _193_

Low Soft slider, _315_

opening, _65_

Curves palette histogram, setting, _192_

custom renders, creating, _429–431_ .
_See also_ _Render Cache_

custom windows, creating, _101_ .
_See also_ _windows_

cuts

checking “confidence line” for, _266_

nudging one frame at a time, _161_

**D**

Dark Blue serial node, labeling, _314_

data burn-in, adding to viewer and final
video, _338–340_

Data Levels, setting, _440–441_

DaVinci Remote Monitor app, 416

DaVinci Resolve 20 quick setup, _xiii–xix_

DaVinci Resolve archive, opening, _4–5_

DaVinci Resolve, downloading, _xii_

DaVinci Resolve panels, _449–453_


**Index** **459**


DaVinci Wide Gamut, _280_ . _See also_ _gamut_
_sizes_

DaVinci YRGB color management, _175–176_

DCP (digital cinema package)

defined, _431_

naming and outputting, _435–437_

unencrypted, _435_

DCP render, setting up, _433–435_

“Decode quality,” choosing with raw
settings, _384_

Defocus BG node, labeling, _309_

deletion of cached files, automating, _378_

deliverables, appearance of, _446_

delivering content, _178_

delivering projects

uploading presentations, _419–422_

using Lightbox to check
timelines, _412–416_

delivery and setup on Macs, _455–456_

Denoise serial node, labeling, _363_

depth of field, mimicking, _79–80_

depth plane, isolating grade to, _38–42_

Design Training and Certification
Program, _xi_

destructive grades, potential for, _193_ .
_See also_ _grades_

difficult tracks, fixing, _309–312_ .
_See also_ _tracks_

display profile, finding for macOS, _172_

Display Qualifier Focus, _18_

display-referred color management, _169_ .
_See also_ _color management_

DN×HD 115 1080p codec, _164_

downloading

DaVinci Resolve, _xii_

and installing DaVinci Resolve lesson
files, _xix_

downstream nodes, _185_

.dra folder, creating, _4_

.dra format, _164_

Dropbox setting, _424_

.drp files, _7_, _164_

.drt format, _164_



Dual Native ISO feature, _390_

dynamic attributes, modifying, _358–360_

dynamic keyframes, animating position
values with, _356–358_ .
_See also_ _keyframes_

dynamic range, _168–178_ . _See also_ _wide_
_dynamic range_

**E**

EBU Color Bar, locating, _187_

editing, offline and online, _164_

Editing Sizing mode, _349_

EDLs, importing, _271–273_

Effects and Definitions panel, _253_

emulation LUT, applying, _333–335_ . _See also_

_LUTs (Lookup tables)_

exporting. _See also_ _Quick Export_

and importing stills, _249–251_

from Mac, _441_

project archive, _164_

external mattes, using, _216–222_

Eyes category, _127_

Eyeshadow category, _126_

**F**

Face node, labeling, _300_

face refinement

combining windows with, _123–124_

enhancing skin tones with, _118–128_

Face Window circle window, creating, _131_

files, organizing into bins, _148–151_ .
_See also_ _project files_

Film Look Creator

designing grades with, _231–234_

generating looks in, _331_

filters and flags, organizing shots
with, _48–51_ .
_See also_ _Post Filter_ ; _Pre-Filter parameter_

Final Cut Pro 7/X setting, _425_

fixing

difficult tracks, _309–312_

translation errors, _155–160_


**Index** **460**


flags and filters, organizing shots
with, _48–51_

footage. _See_ _balancing footage_

Foreground, labeling, _100–101_

Foreground Appearance, _107_

Frame mode, switching from Tracker
to, _89_, _91_

frame rates, matching, _268_

full levels, 440

Fusion Output Caching process, _383_ .
_See also_ _caching process_

**G**

Gain color wheel, _xxiv_, _17_, _19_, _28_, _98_

Gain master wheel, _15_, _29_, _35_

Gain Y bar, _59_

gallery, _xxi–xxii_

Gallery View button, _247_

gamma, remapping, _335_

Gamma color wheel, _xxiv_, _28_

Gamma master wheel, _15_

gamma tags, _456_

Gamma Y, _59_

gamut sizes. _See also_ _DaVinci Wide Gamut_

considering for delivering content, _178_

mapping between, _173_

Generators, accessing, _187_

Global Blend parameter, _107_

Global wheel, _327_

grade compositing. _See_ _node-based grade_
_compositing_

grades. _See also_ _base grades_ ; _destructive_
_grades_ ; _post-clip grade_ ; _timeline grades_

animating, _355–362_

copying, _348_

copying using Timelines album, _256–258_

designing with Film Look
Creator, _231–234_

isolating to depth planes, _38–42_

toggling on and off, _19_

grades and nodes, appending, _235–239_

gradients and color bar graphics, _34_

grading versus broadcast monitor, _173_



grading workflow

balancing and shot matching, _8_, _10_

creating looks, _9_

primary and secondary, _10_

secondary grading, _9_

visualizing in Node Editor, _10_

graphic anomaly, encountering, _377_

Grey Scale compound clip, naming, _202_

grid interfaces, using, _113–118_

groups. _See also_ _clip group level_ ; _post-clip_
_group level_ ; _pre-clip group level_ ;
_self-guided exercises_

adopting in color grading
workflow, _276–277_

creating, _273–277_

reviewing contents of, _294_

using color charts to balance, _285–287_

using CSTs in, _282–284_

**H**

H.264 Master setting, _424_

H264.Hyperdeck setting, _424_

H.265 Master setting, _424_

hand, appearance under tracked
window, _92_

HDR (high dynamic range) media,
grading, _393–405_

HDR balance node, labeling, _403_

HDR palette

control point position, _398_

custom zones, _403–404_

Highlight mode, _399_, _401_

mapping to color panels, _405_

saving custom zones, _404_

Zones graph, _400–402_

Headlights node, labeling, _318_

hero shot, choosing, _47_

High Dynamic Range palette, _395_

Highlight, _xxiii_

Highlight button, _76–77_, _86_, _94_

Highlight B/W button, _95_

Highlight master wheel, _31_


**Index** **461**


Highlight Recovery, using with raw
projects, _391_

Highlights and Shadows parameters, _229_

Highway Group self-guided exercise, _340_

Home Group self-guided exercise, _340_

Hotspot Brightness, _106_

HSL curves

versus Color Warper, _134_

using with skin tones, _129_

working with, _137_

HSL Qualifier palette, _94_

HSL selection, refining, _94_

Hue, disabling, _94_ .
_See also_ _complimentary hue_

hue curves, naming convention, _129_

Hue Rotate field, _131_, _190_

Hue Vs Hue palette, _130_

Hue Vs Sat, _129_

**I**

Image Scaling tab, Project Settings, _384_

image sequence mattes, _218–222_

image uniformity. _See_ _Offset color wheel_

image watermark, applying over
video, _339_

Image wipe, _xxiii_

images, brightening, _36_

IMF setting, _425_

importing

and exporting stills, _249–251_

pre-conformed EDLs, _271–273_

XML timelines, _144–151_

Input and Output DRT parameters, _173_

Input Hue field, _131_

Input Sizing mode, _349_

installing DaVinci Resolve lesson files, _xix_

interface

Color page layout, _xxi–xxii_

palette panel, _xxv_

Primaries color wheels, _xxiv_

viewer, _xxiii_

ISO, changing for raw projects, _390–391_



**J**

jacket node, labeling, _207_

**K**

key elements, sharpening, _84–91_

Key Frame Editor, in color page layout,

_xxi–xxii_

key mixer, seeing results of, _97_

keyboard shortcuts

bypassing node trees, _53_, _317_

bypassing nodes, _86_

Cinema Viewer mode, _232_

collapsing viewer, _26_

comparing results, _100_

comparing work to source footage, _53_

Contrast node, _60_

cycling through versions, _234_

disabling color adjustments, _26_

entering color pages, _5_

inverting wipes, _57_

Keyframes palette, _360_

layer mixers, _207_

moving in viewer, _75_

ripple commands, _242_

Select All clips, _173_

serial nodes, _217_

Shot Match, _53_

toggling grades, _19_

toggling Primaries color and log
wheels, _37_

toggling wipes, _62_

Undo, _17_

versions, _230_

Keyframe Editor, _xxv_

Keyframe Timeline Mode, _348_

keyframeable categories, expanding
list of, _357_

keyframes, using to animate grades,

_355–362_ . _See also_ _dynamic keyframes_ ;
_static keyframes_


**Index** **462**


Keyframes palette

increasing interface size, _361_

navigating, _360_

keys between nodes, reusing
and refining, _212–216_

KODAK LUT compound node, creating, _335_

**L**

LAB color space, setting, _210_

layer mixer node, compositing color
effects with, _205–216_ . _See also_ _nodes_

layers, naming, _243_

Left sign curve window, labeling, _350_

legal levels, _440_

lesson files, getting, _xix_

Lift color wheel, _xxiv_, _28_ . _See also_ _shadows_

Lift master wheel, _14_, _29_

Lightbox, using to check timelines, _412–416_

linear VFX clips, _174_ . _See also_ _VFX clips_

Live Preview behavior, changing, _199_

Live Save, _6_ . _See also_ _saving_

local versions, creating, _229–230_

log adjustment controls, _32_

log wheels and color, comparing, _28–42_

log wheels and Primaries color, toggling
between, _37_

The Long Workday project, naming, _373_

look, creating, _9_

LOOK layer, naming, _243_

LOOK serial node, labeling, _322_

Look serial node, labeling, _330_

looks, generating in Film Look Creator, _331_

Loop button, _91_

Lum Mix, setting, _65_

Lum node, labeling, _356_

Lum Vs Sat HSL curve, _315_

luma waveform, _35_

luminance

altering, _26_

displaying, _13_

impact of Offset wheel on, _33_

Luminance selection, _95_



LUTs (Lookup tables).
_See also_ _emulation LUT_

3D LUT Compatible option, _232_

applying to clips in media pool, _333_

working with, _321–333_

**M**

Mac displays, using DaVinci Resolve
with, _175_, _456_

macOS

finding display profile in, _172_

quick setup, _xiii–xix_

Macs, setup and delivery on, _455–456_

Magenta Look serial node, adding, _374_

Magic Mask. _See also_ _AI Magic Mask 2_
_palette_

fixing difficult tracks with, _309–312_

matte selection, _134_

Magic Mask overlay, _308_

Magic Mask palette, _9_

markers, using for filtering purposes, _51_

Mask Overlay, toggling, _301_, _304_, _306_

masking

physical features, _300–304_

secondary grading, _9_

Masks node, labeling, _310_

master wheels. _See also_ _YRGB color_
_management_

balancing colors with, _16–20_

identifying, _xxiv_

setting tonal range with, _11–16_

Match node, labeling, _290_, _320_

matching clips. _See also_ _clips_

hiding, _254_

using waveforms, _292_

matching frame rates, _268_

matching shots. _See also_ _comparing_ ; _shot_
_match_

at clip group level, _288–292_

using stills, _54–61_

matte data, reusing, _214_

Matte Finesse tools, _96_, _99_, _306_

matte preview, disabling, _98_


**Index** **463**


mattes. _See_ _external mattes_ ; _image_
_sequence mattes_

media

preparing using Scene Cut
Detection, _264–273_

trimming, _160–164_

media pool clips, creating timelines from,

_269–271_ . _See also_ _clips_

Memories button, _246_

memory colors, _137_ . _See also_ _colors_

Micro Color Panel, _449–450_

midtones. _See_ _Gamma color wheel_

Mini Panel

curves, _27_

features, _450_

Hue Curves, _137_

illustration, _449_

mapping HDR palette to color
panels, _405_

Offset mode, _20_

operations, _4_

overview, _452–453_

Power Windows, _83_

Qualifiers, _96_

tracking, _91_

mini-timeline in color page layout, _xxi–xxii_ .
_See also_ _timelines_

mixer nodes. _See also_ _nodes_

morphing, _200–201_

visualizing, _202–205_

monitoring LUT, developing, _325–333_ .
_See also_ _CSTs (Color Space Transforms)_
monitors, grading versus
broadcast, _173_

Morning Group self-guided exercise, _341_

Motion Blur, _364_

Motion Effects palette, _363–364_

**N**

node cache, generating, _370–372_ . _See also_

_caching process_

Node Editor

in color page layout, _xxi_



decluttering, _216_

panning and adjusting slider in, _99_

visualizing grading workflow in, _10_

node grades, disabling and enabling, _19_

node order, importance of, _183–198_

node processing, visualizing, _187–190_

Node Sizing mode, _349_

node sizing, sampling visual data
with, _350–351_

node stacks, activating, _243–246_

node tree templates, saving, _239–246_

node trees, bypassing, _53_, _317_

node-based grade compositing, _182–183_

nodes. _See also_ _layer mixer node_ ; _mixer_
_nodes_ ; _parallel mixer node_ ; _serial node_ ;
_Tilt Shift serial node_

anatomy of, _182–183_

appending, _236_

bypassing, _86_

color and saturation, _183–186_

contrast and luminance, _191–193_

copying, _237–238_

downstream, _185_

impact of dominant color grades
on, _194–198_

labeling, _58_

making adjustments in, _186_

reusing and refining keys
between, _212–216_

sharing, _239_

swapping, _185_

nodes and grades, appending, _235–239_

noise reduction

applying, _362–368_

isolating clips with, _374_

normalization, _8_, _13–14_

NS TEMPLATE still, labeling, _245_

**O**

objects, tracking, _304–307_

objects and people, tracking
automatically, _295–312_

obscured objects, tracking, _87–91_


**Index** **464**


Office Group self-guided exercise, _341_

offline and online workflows, _164_

offline reference, syncing, _151–153_

Offset color wheel, _xxiv_, _100_

Offset wheel

accessing, _20_

impact on luminance, _33_

onscreen control menu, _xxiii_

onscreen window controls, toggling, _77_ .
_See also_ _windows_

Option key. _See_ _keyboard shortcuts_

OTIO (Open Timeline IO), _163_

output color space. _See also_ _color space_

changing for dynamic range, _176–178_

setting, _455_

OUTPUT CST, _329_

Output CSTs, _433_

Output sizing, _348–349_

Outside node, labeling, _77_, _99_

overcast skies, fixing, _92–108_

**P**

pages, resetting, _11_

Palette panel, _xxv_

panels, _449–453_

Parade scope, _36_, _56_, _61–62_

parades, comparing side by side, _64_

parallel mixer node, creating processing
branches with, _198–205_ . _See also_ _nodes_

Patch Replacer effect, creating cover-ups
with, _352–355_

people and objects, tracking
automatically, _295–312_

performance, optimizing with Render
Cache, _369–378_

photo sites, reaching, _382_

physical features, masking, _300–304_

Pink ticket circular window, labeling, _212_

Pivot parameter, _34_

_Planckian locus_, _395_

plug-ins, removing from nodes, _128_

Point Tracker, _353_



position values, animating with dynamic
keyframes, _356–358_

Post Filter, increasing, _306_ .
_See also_ _filters and flags_

post-clip grade, applying with external
reference, _313–317_ .
_See also_ _clips_ ; _grades_

post-clip group level, using to create
unifying look, _313–320_ . _See also_ _groups_

Power Windows, _76_, _83_ . _See also_ _windows_

PowerGrade still, appending, _246_

pre-clip group level, _277–282_ .
_See also_ _groups_

pre-conformed EDLs, importing, _271–273_

Pre-Filter parameter, _96_ .
_See also_ _filters and flags_

Premiere XML setting, _425_

presentations, uploading, _419–421_

Presentations setting, _424_

presets, saving, _444_

presets and render workflow,
understanding, _423–428_

Primaries color and log wheels, toggling
between, _37_

Primaries color bars, adjusting, _58–59_

primaries color wheels, _xxi–xxii_, _xxiv_, _28_

primary grading with color wheels, setting
tonal range, _11–16_

PRIMARY layer, naming, _243_

Pro Tools setting, _425_

processing branches, creating, _198–205_

project backups, setting up, _6–7_

project files, locating, _1_ . _See also_ _files_

project housekeeping, _148–151_ . _See also_

_Colorist Guide subfolder_

Project Server, _422_

Project Settings, opening, _170_, _173_

projects

checking timelines before
delivery, _412–416_

remote monitoring, _416–419_

reviewing with clients, _416–422_

ProRes setting, _424_

proxy workflows, exploring, _166–167_


**Index** **465**


**Q**

Qualifier onscreen control, _18_

Qualifier palette, _99_

qualifier selection, removing, _94_

Qualifier tool, _93_

qualifier values, refining, _93_

qualifiers

as “color space aware” tools, _190_

limiting, _97–99_

Quick Export, _420_ . _See also_ _exporting_

**R**

Radius control, Sharpen palette, _85_

Rainbows node, labeling, _217_

raw clips, determining, _382_ . _See also_ _clips_

raw media projects

setting up Render Cache for, _406–407_

sidecar file, _389_

raw settings. _See also_ _Camera Raw palette_ ;

_tonal ranges_

adjusting at clip level, _389–393_

adjusting at project level, _382–389_

reviewing on project level, _388–389_

RCM (Resolve Color Management).
_See_ _color management_

Rec.709-A, using as output
color space, _456_

Rec.709-A Gamma 2.4 output
color space, _173_

RED IPP2 tone mapping option, _173_

Red Pipes corrector node, labeling, _316_

Reds layer node, creating, _213_

Reference Sizing mode, _349_

Reference Sizing tool, _64_

reframing clips, _347–349_

reframing individual clips, _347–349_

Remote Monitor app, _416–419_

remote rendering, _444_

Remove OFX Plugin option, _128_

Render Cache. _See also_ _custom renders_

clearing, _377–378_

optimizing performance with, _369–378_



setting up for Raw media
projects, _406–407_

render jobs, editing, _445–446_

Render settings, exploring, _438–446_

Render Settings (Advanced), _438–444_

Render Settings panel, _426_

render workflow and presets,
understanding, _423–428_

renders, customizing, _429–431_

Replay setting, _424_

Reset UI Layout, _11_

resolution. _See also_ _4K resolutions_

and aspect ratio, _347_

rescaling media to, _345_, _428_

standards, _162_

resolution options, supporting, _428_

Resolve FX plug-ins, removing from
nodes, _128_

Restore node, labeling, _191_

reviewing projects with clients, _416–422_

Revival category, Resolve FX, _367_

RGB channel button, _16_

RGB channels, _xxiv_

RGB output, connecting to RGB input, _103_

RGB selection, fine-tuning, _94_

Right sign curve window, labeling, _351_

ripple commands, assigning
shortcuts to, _242_

**S**

Sat Vs Lum, _129_

saturation and windows, using to draw
attention, _74–78_

Saturation range, _94_

saving. _See also_ _Live Save_

advanced Render settings, _438–444_

and applying stills to raw clips, _392_

custom zone layout for HDR, _404_

node tree templates, _239–246_

presets, _444_

stills for other projects, _246–251_

Scene Cut Detection, using to prepare
media, _264–273_


**Index** **466**


scene-referred color management, _169_ .
_See also_ _color management_

scopes, turning into floating windows, _135_

Scopes palette, _12_, _35–36_, _56_, _132_

s-curve, _330_

SDR (standard dynamic range), _170–173_,

_246_, _280_, _395_, _405_

secondary grading, _9–10_

SECONDARY layer, naming, _243_

Select All command, _173_

self-guided exercises, _340–341_ .
_See also_ _groups_

sequence caching, observing, _372–373_ .
_See also_ _caching process_

serial node, creating, _52_ . _See also_ _nodes_

setup and delivery on Macs, _455–456_

Shadow color indicator, _33_

Shadow master wheel, _31_

shadows. _See also_ _Lift color wheel_

matching, _58_

restoring using log wheels, _35–38_

Shadows and Highlights parameters, _229_

shallow depth of field, mimicking, _79–80_

sharing nodes, _239_

sharing timelines, _164_

Sharp node, bypassing, _86_

Sharpen palette, _85_

sharpening key elements, _84–91_

Shift key. _See_ _keyboard shortcuts_

shot match, applying, _52–54_ . _See also_

_comparing_ ; _matching shots_

shot matching and balancing, _8_

shot-matching strategy, building, _46–48_

shots

comparing and matching
manually, _61–69_

matching at clip group level, _288–292_

matching using stills, _54–61_

organizing using flags and filters, _48–51_

Show Skin Tone Indicator, _133_ .
_See also_ _skin tones_

Sitcom version, naming, _230_

sizing data, including, _348_



Sizing header, _357_

sizing modes, _349_

Sizing palette, opening, _67_, _348_, _350–351_

skies. _See_ _overcast skies_

skin, color grading, _135_

skin quality, improving, _124–128_

Skin serial node, creating, _196_

skin tone saturation, setting, _136–137_

skin tones. _See also_ _Show Skin Tone_
_Indicator_

adjusting manually, _129–137_

enhancing manually, _118–128_

skin-smoothing options, displaying, _125_

Sky corrector node, creating, _93_

Sky Integration, _107_

Sky Mask Adjustments, _104_

Sky Position, _106_

sky replacement, performing, _102–108_

Sky Window Linear window button,
activating, _97_

Skyline Linear window, labeling, _309_

slider, panning and adjusting in Node
Editor, _99_

smart bins, using to filter clips, _174_ .
_See also_ _bins_

Smart Cache. _See also_ _caching process_

alternative to, _374_

enabling, _273_, _369–370_

source footage, comparing work to, _53_

Source Sky Appearance, _104_

Spatial NR, _364_

Split screen, _xxiii_

Split Screen mode, using with groups, _294_

Split tone node, labeling, _227_

Split_tone.dpx export, naming, _249_

split-screen views, using to compare
clips, _68–69_

static keyframes, using, _360_ .
_See also_ _keyframes_

stills

appending to nodes, _236_

copying, _348_

exporting and importing, _249–251_


**Index** **467**


saving and applying to raw clips, _392_

saving for other projects, _246–251_

using to match shots, _54–61_

Sunlight node, creating, _75_

Sunrise serial node, labeling, _357_

Super Scale feature, _345_

system requirements, _xii_

**T**

Teeth section, _127_

TEMPLATE still, labeling, _240_

Temporal NR, _364_

thumbnail timeline, _xxi–xxii_

TikTok setting, 424

Tilt Shift serial node, creating, _79_ .
_See also_ _nodes_

Tilt-Shift Blur effect controls, _79_

timecode, starting, _152_

timeline grades, migrating, _251–256_ .
_See also_ _grades_

Timeline level, using, _333–340_

Timeline Resolution, setting, _432_

timeline resolutions, changing,

_344–347_, _349_

timelines. _See also_ _mini-timeline in color_
_page layout_ ; _XML timeline_

checking before delivery, _412–416_

configuring for digital cinema, _431–437_

conforming, _153–167_

creating from media pool clips, _269–271_

linking clips to, _153_

preparing for XML export, _163_

sharing, _164_

upscaling, _428_

Timelines album, using to copy
grades, _256–258_

Timelines bin, creating, _264_, _383_

tonal ranges. _See also_ _raw settings_

and log wheels, _30_

setting with master wheels, _11–16_

targeting for HDR media, _394–401_

Track Forward button, _90_

Tracker button, _87_



Tracker palette, _88–89_, _213_, _353–355_

tracking

objects, _304–307_

obscured objects, _87–91_

people, _295–299_

people and objects, _295–312_

tracks. _See also_ _difficult tracks_

color coding, _148–151_

fixing, _309–312_

transcoded media, swapping for camera
originals, _165–166_

transcoding, defined, _164_

transform changes, applying, _64_

translation errors, fixing, _155–160_

“translation” report, _156_

trim control, refining, _161_

trimming media, _160–164_

**U**

UGC (user-generated content)
websites, _428_

undoing actions, _17_

Upper reds gradient window, labeling, _214_

upscaling feature, _345_

user cache modes, utilizing, _373–375_

**V**

Vectorscope option, choosing, _132_

versions, working with, _226–234_

VFX clips, filtering, _150_ . _See also_ _linear VFX_
_clips_

VHS node, labeling, _336_

video, applying image watermark over, _339_

Video bin, creating, _264_, _383_

Video Codec, selecting, _339_

video signal, preserving, _194_

viewer

collapsing, _26_

in color page layout, _xxi–xxii_

controls, _xxiii_

moving in, _75_

removing blue dot from, _304_


**Index** **468**


viewer’s eye, controlling, _74–83_

Vignette node, creating, _344_

vignettes, focusing attention with, _81–82_

Vimeo setting, _424_

visual data, sampling with node
sizing, _350–351_

**W**

warping color ranges, _108–118_

watermark, applying over video, _339_

waveform, raising top of, _23_

Waveform brightness slider, _13_

waveform scope, _12_

waveforms, using to match clips, _292_

wide dynamic range, correcting scenes
with, _402–405_ . _See also_ _dynamic range_

Wielage, Marc, _xxi_

window outline, hiding, _82_

Window palette, _100_

windows. _See also_ _custom windows_ ;

_onscreen window controls_ ; _Power_
_Windows_

combining with face refinement, _123–124_

tracking data, _236_

using to limit qualifiers, _97–99_

windows and saturation, using to draw
attention, _74–78_

Windows quick setup, _xiii–xix_

Wipe Timeline Clip, _320_



wipes

inverting, _57_

toggling on and off, _62_

Workday Dailies, Custom name, _430_

Workday_HD_Preview, creating in Render
Queue, _443_

workflows. _See_ _grading workflow_ ;

_offline and online workflows_ ; _proxy_
_workflows_ ; _render workflow and presets_

**X**

XML (eXtensible Markup Language), _143_

XML export, preparing timelines for, _163_

XML
timeline, importing, _144–151_ .
_See also_ _timelines_

XYZ color space, _434_

**Y**

Y (luma) channel, _13_

Y (luminance) bar, Primaries color bars, _61_

YouTube setting, _424_, _428_

YRGB color management, _175–176_ . _See also_

_master wheels_

**Z**

zone layouts, saving for HDR, _404_

zooming

in and out of viewer, _75_

into reference image, _64_


**Index** **469**


DaVinci Resolve 20 is Hollywood’s most popular color correction
software and is used to color grade more feature films, television
shows and commercials than any other application. This official
Blackmagic Design hands on training guide takes you through
a series of practical exercises that teach you how to use
DaVinci Resolve’s color correction tools in detail. You’ll learn
a wide variety of workflows, effects and the tools necessary to
perform Hollywood caliber grades.


**What You’ll Learn**

- Launching DaVinci Resolve project files and restoring archives

- Balancing and matching footage using primary grading tools

- Analyzing and color correcting images with the help of scopes

- Tracking people and objects with windows and magic masks

- Migrating XML timelines and roundtrip workflows

- Preparing projects for film and television with color management

- Working with nodes to create sophisticated grades

- Managing grades with stills, LUTs, versions and color trace

- Creating groups to streamline your workflow

- Color grading high dynamic range raw footage

- Rendering cache and delivery settings for optimal quality

- Dozens of tips and tricks that will transform how you work!


**Who This Book Is For**

This book is designed for video editors who want more control
over the final appearance of their projects and colorists who want
a more advanced understanding of industry workflows and best
practices. It contains clear and concise lessons, along with
hundreds of tips and tricks from professional colorists to help you
create cinematic images that stand out! You’ll learn about the
primary grading tools used for balancing and matching images,
secondary tools for isolating parts of an image, how to read
scopes, create unique looks and much more!



**Color Page Workflows**


**Reading Scopes**


**Secondary Grading**


**Node Editor Pipeline**


