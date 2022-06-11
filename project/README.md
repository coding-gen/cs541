# Final Project

Genevieve LaLonde
CS510-Computers, Sound and Music
Spring term 2022
Portland State University 
Prof. Dr. Bart Massey
6 June 2022

# Informational links:

* Kong et al's paper: https://arxiv.org/pdf/2109.05418v1.pdf
* Kong et al's repo: https://github.com/bytedance/music_source_separation
* Kong et al's data MUSDB18 which they trained on: https://zenodo.org/record/1117372
* My gitlab repo: https://gitlab.cecs.pdx.edu/music-source-separation/music-source-separation
* My separated musical vocals included at: https://gitlab.cecs.pdx.edu/music-source-separation/music-source-separation/separated-vocals
* The audio dataset with background noise: WHAM!: http://wham.whisper.ai/
* My separated audio included at: https://gitlab.cecs.pdx.edu/music-source-separation/music-source-separation/separated_audio
* Performance evaluation: museval (Signal-to-Distortion Ratio SDR)
 * https://github.com/sigsep/sigsep-mus-eval
 * https://sigsep.github.io/sigsep-mus-eval/
 * https://museval.readthedocs.io/en/latest/

# Usage: 

To use the pretrained model, you can run Kong et al's bytesep as below:

```
$ python -m bytesep separate \
  --cpu  \
  --source_type="vocals" \
  --audio_path="../data/own/IFeelTheEarthMove.m4a" \
  --output_path="separated_results/test-output.mp3" 
Using cpu for separating ..
/home/gen/venv/lib/python3.7/site-packages/librosa/core/audio.py:162: UserWarning: PySoundFile failed. Trying audioread instead.
  warnings.warn("PySoundFile failed. Trying audioread instead.")
Separate time: 746.715 s
```
As can be seen, it is necessary to use the --cpu param if your system does not have any GPU, disabling the default CUDA option. Additionally the default module PySoundFile fails, though I have not been able to find details as to why. The backup option audioread works though. 

# What I did

I set up the implementation and ran it over various types of music from my own library to determine any weaknesses. This required setting up the system a few times, since I kept hitting issues. See the end resulting setup instructions in sound_project_vm_setup.md. See my resulting separated vocals in the dirs: separated-vocals, jazz, ska, and acapella. For any particulary interesting effects, I noted the results in the commit message on the file. The separated_audio dir is empty, as I was not able to test on separating speech out from noisy backgrounds due to dataset issues, detailed below.

## Problems encountered in the setup

I will be documenting these issues below, and filing bug reports on the issues section of the original repo so future reproductions of the bytesep work can be accomplished more easily.

At first I had set up on Debian, but had better success on Ubuntu, since it is easier to install older versions of python on it manually using the dead snakes PPA as per the guide: https://linuxize.com/post/how-to-install-python-3-7-on-ubuntu-18-04/. The code repo states that newer versions of python can prevent installation of their bytesep tool. When doing the initial setup, I ran into a few issues. For example, the requirements.txt file has a typo. It was evidently copied from the setup.py file, and maintains the syntax on this line: `h5py==2.10.0',`. After that, it is recommended to download the checkpoints with bytesep itself, but there was a typo in the readme:

```
$ python -m bytesep download_checkpoints
usage: __main__.py [-h] {download-checkpoints,separate} ...
__main__.py: error: argument mode: invalid choice: 'download_checkpoints' (choose from 'download-checkpoints', 'separate')
```
Luckily upon close inspection I realized there was a dash instead of an underscore as from their own documentation and `python -m bytesep download-checkpoints` would work instead. Once it could run though, it failed on a missing system requirement for protobuf:

```
$ python -m bytesep download_checkpoints
Traceback (most recent call last):
... <redacted>
TypeError: Descriptors cannot not be created directly.
If this call came from a _pb2.py file, your generated code is out of date and must be regenerated with protoc >= 3.19.0.
If you cannot immediately regenerate your protos, some other possible workarounds are:
 1. Downgrade the protobuf package to 3.20.x or lower.
 2. Set PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python (but this will use pure-Python parsing and will be much slower).
```
After manually installing protobuf, the checkpoints were able to be downloaded. However the actual separation could not be run.

```
$ python -m bytesep separate  --cpu   --source_type="vocals"     --audio_path="../data/own/MyHero.mp3"     --output_path="separated_results/test-output.mp3" 
Using cpu for separating ..
/home/gen/venv/lib/python3.7/site-packages/librosa/core/audio.py:162: UserWarning: PySoundFile failed. Trying audioread instead.
  warnings.warn("PySoundFile failed. Trying audioread instead.")
Traceback (most recent call last):
  File "/home/gen/venv/lib/python3.7/site-packages/librosa/core/audio.py", line 146, in load
    with sf.SoundFile(path) as sf_desc:
  File "/home/gen/venv/lib/python3.7/site-packages/soundfile.py", line 740, in __init__
    self._file = self._open(file, mode_int, closefd)
  File "/home/gen/venv/lib/python3.7/site-packages/soundfile.py", line 1265, in _open
    "Error opening {0!r}: ".format(self.name))
  File "/home/gen/venv/lib/python3.7/site-packages/soundfile.py", line 1455, in _error_check
    raise RuntimeError(prefix + _ffi.string(err_str).decode('utf-8', 'replace'))
RuntimeError: Error opening '../data/own/MyHero.mp3': File contains data in an unknown format.
```

While that error message in itself was not terribly helpful, it seemed to indicate some system incompatibility or missing library. I installed recommended libraries we had discussed early in class, and with some additional googling installed a few more system level things as well.

```
sudo apt-get install build-essential libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 ffmpeg python-dev

pip install audioread PySoundFile Wave sounddevice pyaudio

```

Pyaudio was actually very difficult to get installed. I ended up having to install it specifically outside of my python virtual environment, and it required me to first install the portaudio libraries `libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0` as it was failing on issing C header files before that, like:

```
      src/_portaudiomodule.c:28:10: fatal error: Python.h: No such file or directory
         28 | #include "Python.h"
            |          ^~~~~~~~~~
      compilation terminated.
      error: command 'x86_64-linux-gnu-gcc' failed with exit status 1
      [end of output]

```

```
src/_portaudiomodule.c:29:10: fatal error: portaudio.h: No such file or directory
       29 | #include "portaudio.h"
          |          ^~~~~~~~~~~~~
    compilation terminated.
```

When converting some audio files, I made the mistake of uploading them from a MAC which added internal files like `'._05 Cry me a river.m4a'`. These prevented running bytesep on an entire directory, erroring on unknown format in string decoding. It took me a while to figure out the issue was caused by these internal files.

```
    raise RuntimeError(prefix + _ffi.string(err_str).decode('utf-8', 'replace'))
RuntimeError: Error opening '../data/own/jazz/._05 Cry me a river.m4a': File contains data in an unknown format.
```

It was after installing `ffmpeg` finally that the code was able to run. This had been mentioned in a github issues post as something that they tried because it was generally recommended, but had not worked for them: https://github.com/librosa/librosa/issues/1037 I tried it anyway just in case. 

I also had difficulty getting access to gitlab. I am more familiar with github and that is what is configured on my machine. Though I had set up API access tokens and SSH keys with gitlab at the start of the course, I could not clone the repository. I set up new ones, and was able to ssh with the rsa key like `git -i ~/path/to/rsa_id sgl@gitlab.cecs.pdx.edu/`. However I could not for the life of me figure out how to simply clone the repo, despite a thorough read through the GitLab SSH documentation (https://docs.gitlab.com/ee/user/ssh.html and https://docs.gitlab.com/ee/gitlab-basics/start-using-git.html#clone-a-repository and https://docs.gitlab.com/ee/security/two_factor_authentication.html#2fa-for-git-over-ssh-operations etc.) and stackoverflow. In the end I realized I could upload files directly in the web app and did it that way instead. 


# How it went

I had a lot of difficulty in implementing the pre-trained model from Kong et al, as described above. Luckily once I got it working, I was astounded with the results. I made the mistake of first separating the vocals out of the Foo Fighters' "My Hero". This track is mostly instrumental to begin with, though since it is a live recording there is some cheering. I was very confused when I first listened to the separated vocals! I am also impressed that the algorithm was able to pick up that the cheers were human audio. 

In all the system setup, I recreated the virtual machine several times, and ended up needing to download the audio data for VCTK again. This takes several hours. In the meantime, I started separating the vocals out of several music files from my own collection, in a variety of genres: rock, classic rock, classic jazz, modern jazz, male and female singers, operatic vocals over metal back, acapella. I found that bytesep did very poorly on classical jazz. It included a lot of instrumental sounds in the separated vocals. A lot of the songs include hints of cymbols or tiny bits of swelling music in the vocals. I suspect the cymbols are included, since as a pure noise source they are difficult to distinguish, and indeed could represent fricatives which are common in human audio like "f" and "s". However, in Louis Armstrong's "A Kiss to Build a Dream On", the rhythm section and trumpet are also featured heavily in the audio. I had to go back and listen to the original before I could identify that the piano and most of the clarinets at least were filtered out. I dug into this further to attempt to determine what it is about horns in classical jazz that bytesep is having trouble with. I ran other similar types of music through the separator, including more classical jazz, big band swing (which prominently features trumet, trombone, saxophone and clarinet), modern jazz, ska, and acapella. Bytesep appears to consider horns to be a part of the vocals when they carry the melody line, especially if they are old recordings. Thus, the saxophone at 4:40 in the modern Jazz piece "Cry me a river" performed by Natalie Cole was included in the vocals. However the prominent horns in the ska album "Borders & Boundaries" from Less than Jake were nearly always removed. The closer they were to following the melody line, the more likely they were to be included in the vocals, and the louder they were preserved. Thus in many tracks on the album, they almost sound like a backup singer, reflecting the actual vocals. This can be heard in the intro to "Gainesville Rock City" where the horn section plays the melody to start the song off, and is almost fully preserved in the byteseparated vocals. 

I included the acapella album to see how bytesep would handle vocalized approximations of a rhythm section and supporting instruments. It performed quite well in the first track, removing background noises like the piano keys, tuner, and claps, while preserving the chaotic collection of voices. In "Billie Jean / Smooth Criminal" most of the beat boxing was removed, especially the bass parts, while fricatives like "sh", "k" and "ts" were preserved in the vocals. These fricatives are meant to approximate the sound of cymbals, which are a pure noise sound. The bytesep algorithm had difficulty separating cymbals out from the vocals in all the other tracks I tested, so I suspect that is why these parts of the beat boxing were preserved as well. See tracks 01 Joh Eh Ba Dop and 07 The District Sleeps Alone Tonight which contain beat boxing. This pattern was repeated in the other songs. The bass parts of the beat boxing, as well as any base lines were nearly fully removed. Remaining vocal lines and vocal sounds were preserved. 


# What is still to be done

My original intention had been to take these models that are pretrained on music, and determine if they could be used to separate speech out from noisy backgrounds. Unfortunately I had a lot of issues with my datasets. In addition to being so large as to be unwieldy and take hours to download, I had problems finding an already composed dataset for speech with noisy backgrounds. I pulled down and worked with the VCTK dataset from https://datashare.ed.ac.uk/handle/10283/3443. However it turned out to be recordings of human readings, with no background noise. I also worked with the WHAM! dataset from http://wham.whisper.ai/. However this turned out to be only background noises without speech. It appears there is a way to generate speech over background noise from the WHAM! dataset, however I ran out of time.

After working with bytesep, I suspect it would perform quite poorly on the task of audio separation from a noisy background and would require further fine tuning. I suspect this because pure noises like cymbals, brushes on a snare, and fricatives were often preserved in the vocals track that bytesep produces. Additionally most background noises like claps were often still at least partially present. Also, a lot of background noise recordings represent cafes or bars, where the noise is other voices. In the acapella recordings as well as recordings with more than one vocalist, all the vocal parts were usually maintained, including backup singers, and including horns that fulfilled the role of backup singers if they also followed the melody. The only vocal parts that were removed from the acapella recordings were base lines, which would have qualified as bass or accompaniment. Since only the model was only trained to detect four tracks (vocals, bass, accompaniment, and other), it does not appear to be able to separate between the primary vocals, and supporting vocals. While it would feed quite well into the downstream task of melody detection, I believe it would need to be trained to detect horns like trumpets and saxophones as another track, and primary versus secondary audio, before it could be used in separating audio tracks from backgrounds which contain voices. 

I would also like to continue to look into why horns were almost completely preserved in the old classic jazz recordings, but at least partially removed from more modern recordings. I originally assumed this was due to differences in audio equipment. On the one hand, horns were mostly able to be removed from the ska tracks, which supports the idea that older recording techniques lead to the confusion. However, when the horns more closely followed the melody line for a longer period of time, they were more often included. Additionally, the saxophone in the modern rendition of "I'm beginning to see the light" was also included in the vocals, which seems to rule out older recording techniques as the culprit. Therefore I suspect it is a fault of training. Since bytesep was not intended to detect horns in particular - only "accompaniment" - it was weak in separating out horns. More often, accompaniment is performed by the rhythm section like piano, guitar, or bass guitar. I would like to investigate the training set further to determine what kinds of accompaniment it was trained on, and whether simply adding more data with horn sections would resolve the issue. Likely the original MUSDB18 dataset is a good starting point for training, and further fine tuning on more specific data would improve performance in both of the areas discussed. 
