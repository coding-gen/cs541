# Setup VM Sound Project

Use GCP compute optimized instance type `c2-standard-8`.
Change the disk image to Ubuntu and increase the disk size to 120 GB.

Initial system tools install

```
sudo apt update
sudo apt install build-essential
sudo apt-get install manpages-dev
```

Install python 3.7 because the bytesep repo notes there are issues installing with more recent versions of python.

```
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.7
python3.7 --version
```

Set up a virtual environment in case there are issues with dependencies or python and you want to start over without getting rid of the entire compute instance.

```
sudo apt install python3.7-venv
python3.7 -m venv venv
source venv/bin/activate
```

Confirm the right version was installed. It should be sufficient to use the prompt `python` since we are in the venv.

```
python3 -V
python -V
```

It shouldn't be necessary, but for any reason if you want to update your default `python` prompt to be python3:

```
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 1
```

Setup pip. Again it should work with just `python-pip` but if not you can use `python3-pip`. Confirm the version here too, at the end of the output it should say it is with python 3.7.

```
sudo apt install python-pip 
pip -V
```

# Do not upgrade pip. 
Every time you install with pip it'll warn that pip is out of date, but don't update it. This can make it incompatible with our version of python 3.7 since it is older. 

```
Do not do this: pip install --upgrade pip
```

Install more system packages. The first few are for convenience, the next is necessary for portaudio which is necessary for pyaudio.

```
sudo apt install python-dev unzip git-all libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 python-dev ffmpeg portaudio
```

Install more python modules that are commonly used to process audio.

```
pip install audioread PySoundFile Wave sounddevice pyaudio
```

Pull down the repo. And install its requirements. Note the requirements.txt file needs to be fixed. Remove the extra punctuation from the h5 module: `',`

```
git clone https://github.com/bytedance/music_source_separation.git
vi music_source_separation/requirements.txt
pip install -r requirements.txt
pip install bytesep==0.1.1
```

Download the data and then unzip it as necessary.

```
mkdir ~/data
cd ~/data
wget https://zenodo.org/record/1117372/files/musdb18.zip?download=1
wget https://storage.googleapis.com/whisper-public/wham_noise.zip
```

If desired set the timezone to match yours.

```
sudo dpkg-reconfigure tzdata
```

You're all set, start separating audio and music tracks!
