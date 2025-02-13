PS5 Crash Error Decoder

This Python script is designed to extract crash error codes from a PS5 NOR dump or any other compatible .BIN file located within the same directory as the script. The script processes the binary dump and outputs two text files:

EMC Error Log: A raw log containing the error codes and associated details.
Decoded EMC Error Log: A human-readable log with decoded details about the errors.
Features

Extracts crash error codes from PS5 NOR dump or .BIN files.
Outputs two text files:
EMC Error Log: Contains raw crash data.
Decoded EMC Error Log: Provides a decoded version of the error codes, including meaningful descriptions and associated parameters such as:
Error Code (e.g., 80000009)
Error Description (e.g., AC In Detect(12v))
Sequence Number
SoC Temperature
Environmental Temperature
Power State
and more.
Example Output

Code: 80000009 (AC In Detect(12v)), SeqNo: 0016 (Unknown SeqNo), 
T(SoC): 24.83°C, T(Env): 35.25°C, PowState: Unknown PowState, 
UPCAUSE: EAP (EAP's order), devpm: HDMI(5V), BD DRIVE, WLAN
Requirements

Python 3.x
Necessary libraries: (list any libraries if required, e.g., struct, os, etc.)
Installation

Clone or download this repository.
Ensure the .BIN file (PS5 NOR Dump or any compatible file) is placed in the same directory as the script.
Run the script with Python 3.x.
python3 get_ps5_error_data.py
This will generate two text files:

EMC_Error_Log.txt
Decoded_EMC_Error_Log.txt
Usage

Place the .BIN file (PS5 NOR Dump or any other compatible file) in the same folder as the script.
Run the script, and it will automatically extract the crash error codes, generating the logs.
Support

For any issues, please open an issue on GitHub or contact the author.

Donations
https://PayPal.me/Dannyjohn08

Thank you for your support!

Let me know if you'd like to modify anything or add more information!

Contributing
Feel free to open issues or submit pull requests if you find any bugs or have suggestions for improvements.
