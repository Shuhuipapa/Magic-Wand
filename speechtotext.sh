#!/bin/bash
#while true;do
	echo "Recording your Speech (Ctrl+C to Transcribe)" # Tell user to start
	arecord -D plughw:1,0 -f S16_LE -t wav -d 3  -r 16000  file.wav #Store a 3 second recording with a 16000 sampling rate
	wget -q -U "Mozilla/5.0" --post-file file.wav --header "Content-Type: audio/l16; rate=16000" -O - "http://www.google.com/speech-api/v2/recognize?lang=en-us&client=chromium&key=AIzaSyCLmrUtDTZJM5rvNlkxvUZyfq7erCpJqFw" | cut -d\" -f8 >stt.txt  #Upload to cloud and get text back
	rm file.wav # remove wav file
	cat stt.txt # Show the retreived txt
#done