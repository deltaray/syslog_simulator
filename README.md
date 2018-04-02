
# Summary

syslog_simulator is software to generate fake syslog data using a
configuration file that you configure. The primary use case for
this software is for information security education. Too often
security educators will leave realistic logs out of their
courses and presentations because including them requires
sanitizing the data, which can take a lot of time and you can
never be 100% sure you got everything.

This software was mostly written to explore the idea of simulating
logs and what is required in terms of configuration and algorithmic
structure to generate a realistic looking log sequentially. It is
part of a bigger project to help generate a variety of log formats.
Also see Kay Avila's apache_log_simulator.

# Beta Warning

This software is beta quality and is likely to not work completely
and subject to change. In fact this software is likely to be later
merged into a larger project involving different types of log
formats. The configuration file format is likely to change heavily
to be more user friendly. The python code format for the config
file is more of a temporary measure.

# License

Copyright 2018 Mark Krenz (mark@suso.com) This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.

# Configuration

The file *config.py* holds configuration data.  It is written as python
code that is imported by the main program.  The sample *config.py* file
that comes with this software contains all the possible values and
includes some comments to help you get started.

NOTE: At this point some of the configuration values are for
placeholding/ideas and aren't completely implemented.

# Generating a log

After you have setup the *config.py* file in the previous section,
you can simply run the gen_sshdlogs.py file. By default, it will
created a file called *syslog* in the current directory.

./gen_syslog.py

# How do I do X?

While the eventual goal is to make programs such as this one simulate
different types of attacks, for now you can also use the program
to generate the majority of the log file and then manually insert
a line or two where the attack becomes successful and so on.

# Contact
If you have a suggestion for this software or other similar software,
I'd love to hear it. Please feel free to open an issue or contact me.
Thanks.


