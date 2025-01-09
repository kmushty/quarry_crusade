Welcome to your first Connext DDS example! 

This example was generated for architecture x64Linux3gcc4.8.2, using the
data type Hxgn_MapSurveyUpdate from Hxgn_MapSurveyUpdate.idl.
This example builds two applications, named Hxgn_MapSurveyUpdate_publisher and
Hxgn_MapSurveyUpdate_subscriber.

To Build this example:
======================
 
From your command shell, type:
> make -f makefile_Hxgn_MapSurveyUpdate_x64Linux3gcc4.8.2
This command will build a release executable.
 
To build a debug version instead:
> make -f makefile_Hxgn_MapSurveyUpdate_x64Linux3gcc4.8.2 DEBUG=1

To Modify the Data:
===================
To modify the data being sent, edit the Hxgn_MapSurveyUpdate_publisher.cxx
file where it says:
/* Modify the instance to be written here */

To Run this Example:
====================
Make sure you are in the directory where the USER_QOS_PROFILES.xml file was
generated (the same directory this README file is in).
Run /opt/rti_connext_dds-6.0.1/resource/scripts/rtisetenv_x64Linux3gcc4.8.2.bash
to make sure the Connext libraries are in the path, especially if you opened
a new command prompt window.
Run the publishing or subscribing application by typing:
> objs/x64Linux3gcc4.8.2/Hxgn_MapSurveyUpdate_publisher <domain_id> <sample_count>
> objs/x64Linux3gcc4.8.2/Hxgn_MapSurveyUpdate_subscriber <domain_id> <sample_count>
