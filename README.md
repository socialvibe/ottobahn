# ottobahn
Python-based web application for dynamically generating an infinite live stream.

# Running

In order to run the ottobahn server, you need a properly-configured python environment and
a set of video assets to serve up as the stream. A config file is also needed in order to
point the server at the assets and configure some aspects of the generated stream.

## Assets

In order to run the stream, one content assets and 0 or more ad assets are required. If no
ad assets are provided, then the stream will just loop the content forever.

### Existing assets

An archive file containing suitable assets has been uploaded to the wiki for this project. If
those assets are suitable for your use, they can be uncompressed in the `assets` directory
of this repository and you should be all set.

### Acquiring Assets

If you want your stream to have your own assets for content and ads, you can make the assets
yourself. First, get a hold of some mp4 files (how to do this is left as an exercise for the
reader, but there are plenty of services available that will download YouTube videos in this
format.) Once you have your raw content in hand, run the following ffmpeg command (assuming
input video called `x.mp4`):

```
ffmpeg -y x.mp4 -codec copy -bsf:v h264_mp4toannexb -map 0 -f segment -segment_time 10 -segment_format mpegts -segment_list x.m3u8 -segment_list_type m3u8 "frag%d.ts"
```

Now you can point your config file (more on which later) at any assets you've created or downloaded
and you're all set.

## Python Environment

Ottobahn is a python application, an as such needs a properly-configred python environment
to run correctly. Make sure you have the latest version of Python 3 and choose an environment
to configure. I prefer `virtualenv` but you can also do this install using the global python
environment if you like. Install all the packages listed in `requirements.txt` using the
command:

```
pip install -r requirements.txt
```

## Config

Ottobahn requires a config file to control some aspects of how it will render live streams.
This file must be called `config.ini`, and it must be in the current directory when launching
the service. This file uses standard python .ini file syntax.

### Minimal Config

The minimal config file contains the following directives:

```
[content]
window_size=1200
manifest=path/to/content.m3u8
```

Window size is measured in seconds, so this defines a 20-minute window (note that, depending
on the size of your HLS fragments, it might not be possible to provide a window that is
exactly the desired length. The service will use the value provided here as a lower bound on
the window size. The path to the content manifest can be absolute, or relative to the working
directory from which the service was launched.

### Config for Ad Insertion

If you want the service to insert ads, you will need some additional config parameters:

```
[content]
window_size=1200
manifest=path/to/content.m3u8
ad_separation=60
ads_per_pod=3

[ads]
ad1=path/to/ad1/ad1.m3u8
ad2=path/to/ad2/ad2.m3u8
   .
   .
   .
```

Here, `ad_separation` measures the minimum time between ad pods, and `ads_per_pod` determines
how many ads will be in each pod. Each pod will randomly select this number of ads from those
available, and insert them in a random order.

The ads section can list any number of paths to any number of ad manifests. The key names do
not matter; any key in that section will be treated as pointing to a path to an ad manifest.
There must be at least as many entries in this section as the value for `ads_per_pod`.

## Running (Really This Time)

Once everything is set up, to launch the service, just run the `run.sh` script in the project
root directory. This will launch the service on port 9090, and it can be hit at the URL:
http://localhost:9090/m To verify that things are working, enter that link in Safari and the
stream should play back in the browser. It should also play in any other HLS player.
