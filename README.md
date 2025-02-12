PS5 NOR Decode
Overview
This Python script extracts the DBI contents from specified offsets, formats the extracted data into an EMC_LOG.txt file, and decodes it into human-readable text. The script uses wildcards and is useful for debugging a PlayStation 5, especially when UART access is unavailable.

Features
Extracts DBI contents from specified start and end offsets.

Formats extracted data into EMC_LOG.txt.

Decodes data into human-readable text.

Utilizes wildcards for data extraction.

Supports PlayStation 5 debugging without UART access.

Getting Started
Prerequisites
Python 3.x

Required Python libraries (install using requirements.txt if provided)

Installation
Clone the repository:

git clone https://github.com/apewalkers/PS5_NOR_Decode.git
cd PS5_NOR_Decode

Run the script:

The extracted and formatted data will be saved in EMC_LOG.txt.

Script Details
The script performs the following steps:

Reads the binary data from the specified offsets.

Extracts the DBI contents using wildcards.

Formats the extracted data into EMC_LOG.txt.

Decodes the data into human-readable text.

Example output 
Code: 80000009 (AC In Detect(12v)),
 SeqNo: 0016 (Unknown SeqNo),
 T(SoC): 24.83°C,
 T(Env): 35.25°C,
 PowState: Unknown PowState,
 UPCAUSE: EAP (EAP's order),
 devpm: HDMI(5V), BD DRIVE, WLAN
 
Code: C0020303 (Main SoC Access Error (SB-TSI I2C)),
 SeqNo: 0016 (Unknown SeqNo),
 T(SoC): 24.83°C,
 T(Env): 35.25°C,
 PowState: Unknown PowState,
 UPCAUSE: EAP (EAP's order),
 devpm: HDMI(5V), BD DRIVE, WLAN
Donations
If you find this project helpful and would like to support its development, consider making a donation. Donations are not required but greatly appreciated. Thank you!

PayPal.me/Dannyjohn08

Contributing
Feel free to open issues or submit pull requests if you find any bugs or have suggestions for improvements.
