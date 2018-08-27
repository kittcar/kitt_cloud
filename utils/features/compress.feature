Feature: Creating and writing with a Compress object

	Scenario: Initializing a Compress object with a valid extension
		Given we want to compress some files
		When we create the object with the extension .tgz
		Then a new tarfile should open for writing
		And the Compress object can be removed

	Scenario: Initializing a Compress object with an invalid extension
		Given we want to compress some files
		When we create the object with the extension .png
		Then a ValueError exception should occur

	Scenario: Archiving a folder
		Given we want to compress some files
		When we have an open file for writing
		And we add the folder testfiles to the archive
		Then the archive should contain fake_file.txt
		And the Compress object can be removed

	Scenario: Archiving a folder that does not exist
		Given we want to compress some files
		When we have an open file for writing
		And we add the folder doesntexist to the archive
		Then a IOError exception should occur
		And the Compress object can be removed