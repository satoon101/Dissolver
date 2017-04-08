# Dissolver

## Introduction
Dissolver is a plugin created for [Source.Python](https://github.com/Source-Python-Dev-Team/Source.Python).  As such, it requires [Source.Python](https://github.com/Source-Python-Dev-Team/Source.Python) to be installed on your Source-engine server.  It currently only supports CS:GO, CS:S, BMS, and TF2.  Further support will be added to more games in the future.

This plugin removes or dissolves player ragdolls when they die.

<br>
## Installation
To install, simply download the current release from its [release thread](https://forums.sourcepython.com/viewtopic.php?t=1101) and install it into the main directory for your server.

Once you have installed Dissolver on your server, simply add the following to your autoexec.cfg file:
```
sp plugin load dissolver
```

<br>
## Configuration
After having loaded the plugin once, a configuration file will have been created on your server at **../cfg/source-python/dissolver.cfg**

Edit that file to your liking.  The current default configuration file looks like:
```
// Options
//   * 0 = NORMAL
//   * 1 = ELECTRICAL
//   * 2 = ELECTRICAL_LIGHT
//   * 3 = CORE
//   * 4 = RANDOM
//   * 5 = REMOVE
// Default Value: 0
// The type of dissolver to use.
   dissolver_type 0


// Default Value: 2
// The magnitude to use when dissolving.
   dissolver_magnitude 2


// Default Value: 0
// The amount of time (in seconds) to wait before dissolving.
   dissolver_delay 0
```
