# Quality Report: davinci_eval_a — 2026-07-05

## Summary
- **Domain:** davinci_eval_a
- **Date:** 2026-07-05
- **Questions evaluated:** 20
- **Composite Score:** 0.8035
- **Pass:** 20 (100.0%) | **Weak:** 0 (0.0%) | **Fail:** 0 (0.0%)

## Metric Averages
| Metric | Average |
|--------|---------|
| Source Recall | 0.9 |
| Page Metadata Accuracy | 0.755 |
| Top-K Relevance | 0.55 |
| Evidence Quality | 1.0 |

## Per-Question Results
| ID | Question | Score | Label | SR | PMA | TKR | EQ |
|----|----------|-------|-------|----|----|----|----|
| davinci_resolve-001 | How do I set up a Planar Tracker in DaVi... | 0.7875 | pass | 1.0 | 0.5 | 0.55 | 1.0 |
| davinci_resolve-002 | How do I trim a clip on the Edit page in... | 0.7675 | pass | 1.0 | 0.4 | 0.55 | 1.0 |
| davinci_resolve-003 | How do I use Primary Color Correction in... | 0.7475 | pass | 1.0 | 0.3 | 0.55 | 1.0 |
| davinci_resolve-004 | What is the difference between Point Tra... | 0.7075 | pass | 1.0 | 0.1 | 0.55 | 1.0 |
| davinci_resolve-005 | How do I render and deliver a finished p... | 0.7275 | pass | 1.0 | 0.2 | 0.55 | 1.0 |
| davinci_resolve-006 | How do I work with audio tracks and effe... | 0.7075 | pass | 1.0 | 0.1 | 0.55 | 1.0 |
| davinci_resolve-007 | What are the new features in DaVinci Res... | 0.7875 | pass | 1.0 | 0.5 | 0.55 | 1.0 |
| davinci_resolve-008 | How do I use the Delta Keyer in DaVinci ... | 0.8875 | pass | 1.0 | 1.0 | 0.55 | 1.0 |
| davinci_resolve-009 | How do I create a 3D composite with a tr... | 0.8875 | pass | 1.0 | 1.0 | 0.55 | 1.0 |
| davinci_resolve-010 | How do I use Power Windows to isolate an... | 0.8875 | pass | 1.0 | 1.0 | 0.55 | 1.0 |
| davinci_resolve-011 | How do I set up ACES color management fo... | 0.7125 | pass | 0.5 | 1.0 | 0.55 | 1.0 |
| davinci_resolve-012 | How do I use the Cut page for fast rough... | 0.7125 | pass | 0.5 | 1.0 | 0.55 | 1.0 |
| davinci_resolve-013 | How do I set up and switch between multi... | 0.8875 | pass | 1.0 | 1.0 | 0.55 | 1.0 |
| davinci_resolve-014 | How do I set up a Dolby Atmos mix with 3... | 0.8875 | pass | 1.0 | 1.0 | 0.55 | 1.0 |
| davinci_resolve-015 | How do I organize and find clips using b... | 0.8875 | pass | 1.0 | 1.0 | 0.55 | 1.0 |
| davinci_resolve-016 | How do I add and customize video transit... | 0.7125 | pass | 0.5 | 1.0 | 0.55 | 1.0 |
| davinci_resolve-017 | How do I create animated 3D titles using... | 0.8875 | pass | 1.0 | 1.0 | 0.55 | 1.0 |
| davinci_resolve-018 | How does Blackmagic Cloud collaboration ... | 0.8875 | pass | 1.0 | 1.0 | 0.55 | 1.0 |
| davinci_resolve-019 | Why is my DaVinci Resolve playback stutt... | 0.8875 | pass | 1.0 | 1.0 | 0.55 | 1.0 |
| davinci_resolve-020 | How do I import an XML or AAF timeline f... | 0.7125 | pass | 0.5 | 1.0 | 0.55 | 1.0 |

## Weak / Fail Details
- No weak or fail questions.

## Truncation Warnings
- davinci_resolve-012: 1 result(s) with text >= 5000 chars (heuristic, see LIM-003).

## Real-World Source Comparison

Online source coverage and Hub top-3 snippets for manual solution-alignment review.

### davinci_resolve-001: How do I set up a Planar Tracker in DaVinci Resolve?

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://www.blackmagicdesign.com/products/davinciresolve/fusion | official-docs | yes | — |
| https://www.blackmagicdesign.com/products/davinciresolve/training | official-docs | yes | — |

**Hub Top Snippets:**

1. #### **Setting Up to Use the Planar Tracker**  Similar to the Tracker node, to do a planar track, you need to connect the output of the image you want to track to the background input of a Planar Trac
2. #### **Setting Up to Use the Planar Tracker**  Similar to the Tracker node, to do a planar track, you need to connect the output of the image you want to track to the background input of a Planar Trac
3. -and-fusion)_ .  If you are using DaVinci Resolve, you can use the Lens Corrections control in the Cut page or Edit page. This adjustment carries over into the Fusion page. Lens correction in DaVinci

**Manual Evaluation:**

- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?

### davinci_resolve-002: How do I trim a clip on the Edit page in DaVinci Resolve?

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://www.blackmagicdesign.com/products/davinciresolve/edit | official-docs | yes | — |
| https://www.blackmagicdesign.com/products/davinciresolve/training | official-docs | yes | — |

**Hub Top Snippets:**

1. ## **Trimming Clips in the Timeline**  DaVinci Resolve offers many options for editing and trimming audio clips, either manually  or with keyboard shortcuts. In this exercise, you’ll start by manually
2. - If you use use the Trim tool via dragging in the Timeline, then you can choose to ripple the entire selection of edits by an arbitrary duration, for example, shortening or lengthening the entire sel
3. #### **Trimming Multiple Edits or Clips at Once**  DaVinci Resolve lets you select multiple edit points or clips for certain trimming operations, making it possible to trim multiple edits and clips at

**Manual Evaluation:**

- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?

### davinci_resolve-003: How do I use Primary Color Correction in DaVinci Resolve?

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://www.blackmagicdesign.com/products/davinciresolve/color | official-docs | yes | — |
| https://www.blackmagicdesign.com/products/davinciresolve/training | official-docs | yes | — |

**Hub Top Snippets:**

1. ## **Using the Primary Corrector**  The most popular controls for creating different looks and balancing your shots are found  in the primary corrector. Because DaVinci Resolve includes many controls
2. Underexposed source Balanced and gain corrected  Whether clips need changes large or small, the primary DaVinci Resolve toolset adjusts the characteristics of hue, saturation, and contrast in a variet
3. ## **Masking Areas with Windows**  The first part of making a secondary color correction is to isolate the adjustment on a  node. This allows you to make very specific adjustments without modifying th

**Manual Evaluation:**

- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?

### davinci_resolve-004: What is the difference between Point Tracker and Planar Tracker in DaVinci Resolve?

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://www.blackmagicdesign.com/products/davinciresolve/fusion | official-docs | yes | — |
| https://www.blackmagicdesign.com/products/davinciresolve/color | official-docs | yes | — |

**Hub Top Snippets:**

1. ## **Tracking Planar Surfaces**  As you have experienced so far, the single-point tracker is the simplest tracker in the  Fusion page. Although it works well on many shots, it’s not the most optimal t
2. #### Planar Tracker Node [PTRA]  The Planar Tracker node  The Planar Tracker node is designed to solve a match-moving problem that commonly comes up during post-production. As an example, live-action
3. #### Planar Tracker Node [PTRA]  The Planar Tracker node  The Planar Tracker node is designed to solve a match-moving problem that commonly comes up during post-production. As an example, live-action

**Manual Evaluation:**

- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?

### davinci_resolve-005: How do I render and deliver a finished project in DaVinci Resolve?

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://www.blackmagicdesign.com/products/davinciresolve/edit | official-docs | yes | — |
| https://www.blackmagicdesign.com/products/davinciresolve/training | official-docs | yes | — |

**Hub Top Snippets:**

1. ## **Understanding the Render** **Workflow and Presets**  The deliver page is designed to help you quickly set up one or more render jobs. Before  you dive into the intricacies of individual render pa
2. ## **Reviewing Projects with Clients**  Before rendering a finished project, you will usually also go through a review process with  your clients or collaborators to ensure everyone is satisfied with
3. ###### **Setting Up and Using Remote Rendering**  Using remote rendering is easy, but it does require a bit of preparation.  **1** Make sure the storage volume containing the media being referenced by

**Manual Evaluation:**

- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?

### davinci_resolve-006: How do I work with audio tracks and effects in Fairlight in DaVinci Resolve?

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://www.blackmagicdesign.com/products/davinciresolve/fairlight | official-docs | yes | — |
| https://www.blackmagicdesign.com/products/davinciresolve/training | official-docs | yes | — |

**Hub Top Snippets:**

1. ## **Getting Started**  Welcome to _The Fairlight Audio Guide to DaVinci Resolve 20_, an official Blackmagic Design certified training book that teaches professionals and students the art of sound des
2. - Move the pointer over the plugin’s name in the Effects area of the Mixer, and click on the custom UI button to open its controls.  The custom UI button for audio plugins in the Mixer  Nearly all Fai
3. If you’d like to work with some additional options, the Media Pool in the Fairlight page also has the ability to filter out audio-only clips, or video clips with audio, in the currently selected bin.

**Manual Evaluation:**

- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?

### davinci_resolve-007: What are the new features in DaVinci Resolve 21?

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://www.blackmagicdesign.com/products/davinciresolve/whatsnew | official-docs | yes | — |
| https://www.blackmagicdesign.com/products/davinciresolve/support | official-docs | yes | — |

**Hub Top Snippets:**

1. ### **Introduction**  DaVinci Resolve 21 introduces a new Photo page, which enables colorists and photographers to use Hollywood’s most advanced color tools for still photos.  The new Photo page lets
2. Set your Stereoscopic Mode and Projection format in Clip Attributes for all your clips.  ##### **Immersive Viewer**  DaVinci Resolve 21 has a new Immersive Viewer mode that can be used in the Media, E
3. ## Photo  Photo Image Editing Now Fully Integrated Within DaVinci Resolve.  ### **Photo Page**  DaVinci Resolve 21 introduces a powerful new Photo page. This page is designed for users to manage, orga

**Manual Evaluation:**

- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?

### davinci_resolve-008: How do I use the Delta Keyer in DaVinci Resolve Fusion to remove a green screen background?

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://www.blackmagicdesign.com/products/davinciresolve/fusion | official-docs | yes | — |
| https://documents.blackmagicdesign.com/UserManuals/DaVinci-Resolve-20-Fusion-… | official-docs | yes | — |

**Hub Top Snippets:**

1. ## **Sending a Matte to the Color Page**  As you have experienced, the Delta Keyer is an amazing tool for green-screen shots.  And although the Fusion page also includes extremely adept Color Correcti
2. **2** In the Mask tab, set the Solid Replace Mode to Source.  Setting the Replace Mode to Source disables any spill suppression being performed in  the Delta Keyer and instead uses the original colors
3. **3** Select the **Fusion20DeltaKeyer.dra** file and click Open to add the archived project to  the Project Manager.  **4** Open the Delta Keyer project from the Project Manager and select the edit pa

**Manual Evaluation:**

- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?

### davinci_resolve-009: How do I create a 3D composite with a tracked camera and 3D text in DaVinci Resolve Fusion?

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://www.blackmagicdesign.com/products/davinciresolve/fusion | official-docs | yes | — |
| https://www.blackmagicdesign.com/products/davinciresolve/training#fusion | official-docs | yes | — |

**Hub Top Snippets:**

1. #### **Chapter 26** ### 3D Camera Tracking  This chapter presents an overview of using the Camera Tracker node and the workflow it involves. Camera tracking is used to create a virtual camera in Fusio
2. A 3D particle system, also created entirely within Fusion  Text  The Text tools in Fusion are exceptional, giving you layout and animation options in both 2D and 3D. Furthermore, within DaVinci Resolv
3. A 3D particle system, also created entirely within Fusion  Text  The Text tools in Fusion are exceptional, giving you layout and animation options in both 2D and 3D. Furthermore, within DaVinci Resolv

**Manual Evaluation:**

- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?

### davinci_resolve-010: How do I use Power Windows to isolate and grade a specific area of an image in DaVinci Resolve?

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://www.blackmagicdesign.com/products/davinciresolve/color | official-docs | yes | — |
| https://documents.blackmagicdesign.com/UserManuals/DaVinci-Resolve-20-Coloris… | official-docs | yes | — |

**Hub Top Snippets:**

1. # Making Secondary Adjustments  Primary adjustments work on the  entire image, whereas secondary  adjustments let you isolate and work  on specific parts of an image.  For example, you might want to
2. Circular Power Window to focus attention to the skin  DaVinci Resolve makes it easy to combine multiple Power Windows in different ways, to intersect with one another and create even more sophisticate
3. #### **Chapter 138** ### Secondary Windows  Secondary correction describes isolating a specific part of the image, or a specific subject, using a key.  Keys in DaVinci Resolve are grayscale images tha

**Manual Evaluation:**

- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?

### davinci_resolve-011: How do I set up ACES color management for an HDR grading workflow in DaVinci Resolve?

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://www.blackmagicdesign.com/products/davinciresolve/color | official-docs | yes | — |
| https://www.blackmagicdesign.com/products/davinciresolve/training#color | official-docs | yes | — |

**Hub Top Snippets:**

1. or manual adjustments.  **DaVinci YRGB Color Managed:** Enables the Resolve color-managed workflow (RCM) for grading.  **ACEScc or ACEScct:** Both of these are standardized color management schemes th
2. **  When you first choose DaVinci YRGB Color Managed from the Color science drop-down menu of the Color Management panel in the Project Settings, you’re presented with a simple pair of menus for setti
3. ###### **Setting Up ACES in the Project Settings Window**  There are four parameters available in the Color Science drop-down of the Color Management panel of the Project Settings that let you set up

**Manual Evaluation:**

- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?

### davinci_resolve-012: How do I use the Cut page for fast rough-cut editing in DaVinci Resolve?

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://www.blackmagicdesign.com/products/davinciresolve/cut | official-docs | yes | — |
| https://www.blackmagicdesign.com/products/davinciresolve/training#edit | official-docs | yes | — |

**Hub Top Snippets:**

1. #### **The Cut Page**  The Cut page is a focused environment for fast editing. It’s useful in situations where you need to quickly cut a news segment, build an episode of web content, edit a straightf
2. #### **Chapter 26** ### Using the Cut Page  The Cut page is a focused environment for fast editing. It’s useful in situations where you need to quickly cut a news segment, build an episode of web cont
3. #### **Overview of the Cut Page**  With the addition of the Cut page, DaVinci Resolve now has two editing environments, intended for two different audiences. While the Cut and Edit pages share many of

**Manual Evaluation:**

- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?

### davinci_resolve-013: How do I set up and switch between multiple camera angles in a multicam edit in DaVinci Resolve?

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://www.blackmagicdesign.com/products/davinciresolve/edit | official-docs | yes | — |
| https://documents.blackmagicdesign.com/UserManuals/DaVinci-Resolve-20-Editors… | official-docs | yes | — |

**Hub Top Snippets:**

1. #### **Introduction to Multicam Editing**  If you’re working on a program where a performance, interview, or event was recorded using multiple simultaneous cameras, DaVinci Resolve has multi-camera ed
2. #### **Chapter 42** ### Multicam Editing  If you’re working with media that was shot simultaneously using multiple cameras, then you can use the Multicam Editing tools in DaVinci Resolve to create mul
3. ###### **Selecting a Single Reference Audio Track for Multicam Clips**  Multicam clips in DaVinci Resolve can use reference audio files (such as those recorded by an external sound mixer) as the audio

**Manual Evaluation:**

- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?

### davinci_resolve-014: How do I set up a Dolby Atmos mix with 3D spatial panning in DaVinci Resolve Fairlight?

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://www.blackmagicdesign.com/products/davinciresolve/fairlight | official-docs | yes | — |
| https://www.blackmagicdesign.com/products/davinciresolve/training#fairlight | official-docs | yes | — |

**Hub Top Snippets:**

1. DaVinci Resolve Studio offers fully integrated support for ground-up creation of immersive  audio projects in a variety of formats, including MPEG-H, Auro 3D, Sony 360 RA,  Ambisonics, and Dolby Atmos
2. ## **Enabling Immersive Toolsets**  The Fairlight page in DaVinci Resolve Studio includes all the tools you need for creating,  mixing, and delivering original immersive audio content. You can start w
3. ## **Converting a Surround** **Sound Channel-Based Mix** **to Dolby Atmos**  When mixing Dolby Atmos in a DAW like DaVinci Resolve, you don’t need to change your  bed buses, such as 7.1, to 7.1.4. In

**Manual Evaluation:**

- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?

### davinci_resolve-015: How do I organize and find clips using bins, smart bins, and metadata in DaVinci Resolve?

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://www.blackmagicdesign.com/products/davinciresolve/media | official-docs | yes | — |
| https://www.blackmagicdesign.com/products/davinciresolve/edit | official-docs | yes | — |

**Hub Top Snippets:**

1. ## **Analyzing Clips for People** ##### (Studio Only)  Another subset of metadata that you may find useful when organizing clips in your  project is to have DaVinci Resolve analyze clips for people’s
2. ##### **Automatic Scene Smart Bins**  Another advantage of adding metadata to your clips is that keywords, scene, and shot  metadata will be used to create a series of automatic smart bins. To show ad
3. #### **Chapter 17** ### Using the Media Page  The Media page is the primary interface for media import and clip organization in DaVinci Resolve. It’s also where all timelines that you edit in DaVinci

**Manual Evaluation:**

- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?

### davinci_resolve-016: How do I add and customize video transitions between clips in DaVinci Resolve?

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://www.blackmagicdesign.com/products/davinciresolve/edit | official-docs | yes | — |
| https://www.blackmagicdesign.com/products/davinciresolve/fusion | official-docs | yes | — |

**Hub Top Snippets:**

1. ###### **Adding Other Kinds of Transitions**  In order to make the selection of transitions, titles, and effects more intuitive, DaVinci Resolve shows each effect as a thumbnail representation in addi
2. #### **Audio Compound Clips**  DaVinci Resolve supports audio compound clips, which are created just like any other compound clip, by selecting multiple audio clips, right-clicking one of them, and ch
3. Clips with Fusion page compositions have a Fusion badge to the right of the name.  To create an effect in the Fusion page of DaVinci Resolve, you need only park the playhead over a clip in the Edit or

**Manual Evaluation:**

- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?

### davinci_resolve-017: How do I create animated 3D titles using the Text+ node in DaVinci Resolve Fusion?

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://www.blackmagicdesign.com/products/davinciresolve/fusion | official-docs | yes | — |
| https://www.blackmagicdesign.com/products/davinciresolve/training#fusion | official-docs | yes | — |

**Hub Top Snippets:**

1. Clips with Fusion page compositions have a Fusion badge to the right of the name.  To create an effect in the Fusion page of DaVinci Resolve, you need only park the playhead over a clip in the Edit or
2. Clips with Fusion page compositions have a Fusion badge to the right of the name.  To create an effect in the Fusion page of DaVinci Resolve, you need only park the playhead over a clip in the Edit or
3. # Addendum: Creating Title Animations  The next two lessons are not part  of the End User certification exam.  However, they do provide valuable  insight into the motion graphics  capabilities of Fusi

**Manual Evaluation:**

- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?

### davinci_resolve-018: How does Blackmagic Cloud collaboration work for multi-user projects in DaVinci Resolve?

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://www.blackmagicdesign.com/products/davinciresolve/collaboration | official-docs | yes | — |
| https://www.blackmagicdesign.com/products/davinciresolve/training | official-docs | yes | — |

**Hub Top Snippets:**

1. ## **Introducing Blackmagic Cloud**  DaVinci Resolve is the world’s only complete post-production solution that lets everyone  work together on the same project at the same time. Traditionally, post-p
2. ## **Introducing Blackmagic Cloud**  DaVinci Resolve is the world’s only complete post-production solution that lets everyone  work together on the same project at the same time. Traditionally, post-p
3. ## **Introducing Blackmagic Cloud**  DaVinci Resolve is the world’s only complete post-production solution that lets everyone  work together on the same project at the same time. Traditionally, post-p

**Manual Evaluation:**

- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?

### davinci_resolve-019: Why is my DaVinci Resolve playback stuttering and how can I improve performance?

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://forum.blackmagicdesign.com/viewforum.php?f=21 | forum | yes | — |
| https://www.blackmagicdesign.com/support/family/davinci-resolve-and-fusion | official-docs | yes | — |

**Hub Top Snippets:**

1. #### **Which Playback Optimization** **Method Should I Use?**  DaVinci Resolve’s various playback optimization features are designed to specifically increase performance to make up for hardware, stora
2. ## **Optimizing Performance** **with Render Cache**  Almost anyone who has worked with raw footage or done graphic-intensive work on a  computer will be familiar with the frustration of experiencing l
3. performance is being used up by the need to debayer raw media. While you could improve playback performance by taking the time to either generate optimized media (see below) or render to the Fusion Ou

**Manual Evaluation:**

- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?

### davinci_resolve-020: How do I import an XML or AAF timeline from Premiere Pro or another NLE into DaVinci Resolve?

**Online Sources:**

| URL | Type | Has Solution | Date |
|-----|------|--------------|------|
| https://www.blackmagicdesign.com/products/davinciresolve/edit | official-docs | yes | — |
| https://documents.blackmagicdesign.com/UserManuals/DaVinci-Resolve-20-Editors… | official-docs | yes | — |

**Hub Top Snippets:**

1. **To export an AAF or XML file after you’ve rendered the graded clips:**  Do one of the following:  **1** To export the current Timeline, choose File > Export AAF, XML, or press Shift-Command-O.     -
2. ** You should leave this setting set to “Resolve.”  **When importing timelines via XML from Apple software:** Choose the “Final Cut Pro 7” or “Final Cut Pro X” methods of conform.  **When importing ti
3. If necessary, you can freely re-edit projects you’re planning to export. When you export an AAF or XML file, the Timeline will be sent back to the originating NLE, or onward to the finishing applicati

**Manual Evaluation:**

- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?

## Gaps & Recommendations
- No weak/fail questions. Domain coverage looks healthy.
