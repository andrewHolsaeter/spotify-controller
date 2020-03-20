# Spotify Control
Hopefully will allow automated spotify playing from pi (for an alarm clock)

# Requirements
Mopidy and mopidy-spotify installed (see below for installation instructions)
Spotify premium account

# Installing Mopidy and mopidy spotify
Taken from wonderful post here:
https://www.ckdsn.com/how-to-a-spotify-alarm-clock-for-raspberry-pi
*Note that these are outdated instructions, and I ran into some problems getting it up in running
Some additional things I ran into and changed:
*  `sudo systemctl status mopidy` showed "* failed to open vchiq instance"  
  *  Cause: mopidy was only member of audio group and not video group as checked by `groups mopidy`
  *  Fix: Add video to mopidy user with: `sudo adduser mopidy video`
  *  Ref: https://discourse.mopidy.com/t/failed-to-open-vchiq-instance/2373/4
*  `mpc add` doesn't work and `sudo systemctl status mopidy` showed: " Failed to lookup : Session must be logged in and online to .."  
  *  Cause: Running mopidy on boot, but Pi not waiting for network on boot
  *  Fix1: Manually restart mopidy using stop/start
  *  Fix2: Edit rasp-conf to wait for network on boot:
	1) sudo raspi-config
 	2) Select **4 Wait for network at boot**
	3) Select **Slow Wait for network connection before completing boot**
	4) Clik **Ok**, then **Finish**
  *  Ref: https://discourse.mopidy.com/t/spotify-authentication-works-only-after-server-restart/3617
* Adding playlists failed
  *  Cause: Wasn't using the hashed? client_id/secret from https://mopidy.com/ext/spotify/#authentication
  *  Cause2: Also possibly due to using old mopidy that used python2. Updated to newest mopidy which uses python3.7
  *  Fix: Make sure to copy the textbox div after the popup closes and use that in `mopidy.conf`

