# Data18-Phoenix metadata agent

This metadata agent will receive data from [Data18.com's Store](https://data18.empirestores.co) for full length movie releases.

To get the best results, follow the [standard plex naming convention for movies](http://wiki.plexapp.com/index.php/Media_Naming_and_Organization_Guide#Movie_Content).


Features
============
Currently the features of this metadata agent are:
- Grabs Metadata
- Title
- Studio
- Release Data
- Porn Stars stored in Actors with photo
- Categories stored as Genres
- DVD/Movie cover stored as Movie Poster
- Video Preview stored as video background

Future Plans are:
- Automatically grab scene photos for additional background artwork

Installation
============
Here is how to find the plug-in folder location:
https://support.plex.tv/hc/en-us/articles/201106098-How-do-I-find-the-Plug-Ins-folder-

Plex main folder location:

    * '%LOCALAPPDATA%\Plex Media Server\'                                        # Windows Vista/7/8
    * '%USERPROFILE%\Local Settings\Application Data\Plex Media Server\'         # Windows XP, 2003, Home Server
    * '$HOME/Library/Application Support/Plex Media Server/'                     # Mac OS
    * '$PLEX_HOME/Library/Application Support/Plex Media Server/',               # Linux
    * '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/', # Debian,Fedora,CentOS,Ubuntu
    * '/usr/local/plexdata/Plex Media Server/',                                  # FreeBSD
    * '/usr/pbi/plexmediaserver-amd64/plexdata/Plex Media Server/',              # FreeNAS
    * '${JAIL_ROOT}/var/db/plexdata/Plex Media Server/',                         # FreeNAS
    * '/c/.plex/Library/Application Support/Plex Media Server/',                 # ReadyNAS
    * '/share/MD0_DATA/.qpkg/PlexMediaServer/Library/Plex Media Server/',        # QNAP
    * '/volume1/Plex/Library/Application Support/Plex Media Server/',            # Synology, Asustor
    * '/raid0/data/module/Plex/sys/Plex Media Server/',                          # Thecus
    * '/raid0/data/PLEX_CONFIG/Plex Media Server/'                               # Thecus Plex community    

Get the latest source zip in github release at https://github.com/PhoenixPlexCode/Data18-Phoenix.bundle > "Clone or download > Download Zip
- Open Data18-Phoenix.bundle-master.zip and copy the folder inside (Data18-Phoenix.bundle-master) to the plug-ins folders
- Rename folder to "Data18-Phoenix.bundle" (remove -master) :

Notice
============
This was created quickly because I couldn't fall asleep. No real error checking is implemented. It was quickly tested on ~100 titles before the initial publishing.