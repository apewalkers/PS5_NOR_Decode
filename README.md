# PS5 Crash Error Decoder

This Python script extracts crash error codes from a **PS5 NOR dump** or any other compatible `.BIN` file within the same directory as the script. The extracted data is saved in two text files for easier debugging and analysis.

---

## 🛠 Features

- Extracts **crash error codes** from PS5 NOR dump or `.BIN` files.
- Generates two log files:
  - **EMC Error Log**: Contains raw crash data.
  - **Decoded EMC Error Log**: A human-readable version with detailed error descriptions.
- Decodes important parameters, including:
  - **Error Code** (e.g., `80000009`)
  - **Error Description** (e.g., `AC In Detect(12v)`)
  - **Sequence Number**
  - **SoC Temperature**
  - **Environmental Temperature**
  - **Power State**
  - **UPCAUSE Details**
  - **Connected Devices** (HDMI, BD DRIVE, WLAN, etc.)

---

## :open_file_folder: Example Output

Code: 80000009 (AC In Detect(12v)),__
SeqNo: 0016 (Unknown SeqNo),__
T(SoC): 24.83°C,__
T(Env): 35.25°C,__
PowState: Unknown PowState,__
UPCAUSE: EAP (EAP's order),__
devpm: HDMI(5V), BD DRIVE, WLAN

---

## :pushpin: Requirements

- **Python 3.x**
- Necessary Python libraries (e.g., `struct`, `os`, etc.)

---

## :inbox_tray: Installation

1. **Clone or Download** this repository:
   ```sh
   git clone https://github.com/apewalkers/PS5_NOR_Decode.git
   cd PS5_NOR_Decode
