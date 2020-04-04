# Vernier Alignment
A set of Python functions to facilitate a psycho-physical alignment procedure making use of [Vernier hyperacuity](https://en.wikipedia.org/wiki/Vernier_acuity). The code makes extensive use of [PsychoPy.](https://github.com/psychopy/psychopy)

The code was written with a specific example in mind, but could be easily modified. Example is as follows:
* Two displays are combined by a beam-splitter and imaged onto a subject's retina. 
* Each display is optically filtered - one at 510nm, the other at 630nm. 
* To account for chromatic defocus in the subject's eye, the two displays are position at different distances from the first lens, creating a difference in scale.
* Chromatic aberration in the subject's eye will also cause the images to be offset on the subject's retina.
* To account for these differences in position and scale, a vernier acuity test is performed at four different orientations.

## Getting started 
You will need to have installed the following programs.

### Prerequisites
* [Anaconda for Python 3](https://www.anaconda.com/distribution/)
* [PsychoPy](https://github.com/psychopy/psychopy)
* [Git](https://git-scm.com/download/win)

### Installation 
Clone the git repository: `git clone https://github.com/tomjsmart/psychopy_vernier`

### Test
To run a test on a single monitor set `run_type = 'test'`
