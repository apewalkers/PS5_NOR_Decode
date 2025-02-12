import os
import re

# Get the folder where the script is located
folder_path = os.path.dirname(os.path.abspath(__file__))

# Start and end offsets
start_offset = 0x1CE100
end_offset = 0x1CEC70

# Function to extract and convert data from binary file between specific offsets
def extract_hex_data(file_path, start_offset, end_offset):
    with open(file_path, "rb") as file:
        file.seek(start_offset)
        data = file.read(end_offset - start_offset)
        if len(data) % 4 != 0:
            raise ValueError("Data length is not a multiple of 4 bytes, check the offsets.")
        hex_data = [f"{int.from_bytes(data[i:i+4], 'little'):08X}" for i in range(0, len(data), 4)]
        return hex_data

# Function to format extracted data with descriptions and line numbers
def format_data_with_line_numbers(hex_data, file_path):
    formatted_data = f"{file_path}""\n== Emc Error Log ==\n"
    formatted_data += "# No  Code       Rtc        PowState   UpCause    SeqNo   DevPm  T(SoC)  T(Env) Padding(0) Padding(1)\n"
    
    for index in range(0, len(hex_data), 8):
        row = hex_data[index:index+8]
        if len(row) == 8:
            formatted_row = f" {index//8:02d} "
            formatted_row += f"{row[0]} {row[1]} {row[2]} {row[3]} "
            formatted_row += f"{row[4][:4]} {row[4][4:]} "
            formatted_row += f"{row[5][:4]} {row[5][4:]} "
            formatted_row += f"{row[6][:4]} {row[6][4:]} "
            formatted_row += f"{row[7][:4]} {row[7][4:]} "
            formatted_row += "FFFF FFFF"
            formatted_data += formatted_row + "\n"
    
    return formatted_data

# List all .bin files in the folder where the script is located
bin_files = [f for f in os.listdir(folder_path) if f.endswith('.bin')]

# Loop through all .bin files and process each one
for bin_file in bin_files:
    file_path = os.path.join(folder_path, bin_file)
    hex_data = extract_hex_data(file_path, start_offset, end_offset)
    formatted_data = format_data_with_line_numbers(hex_data, file_path)
    
    # Output file path with the .bin filename as a prefix
    bin_file_name = os.path.splitext(bin_file)[0]
    output_file_path = os.path.join(folder_path, f"{bin_file_name}_EMC_LOG.txt")

    # Open the output file
    with open(output_file_path, "w") as output_file:
        output_file.write(formatted_data + "\n\n")

    print(f"Formatted data from {bin_file} has been written to {output_file_path}")

# Code database with patterns
code_database = {
    r'80000001': 'Thermal Sensor Fail - NaN SOC',
    r'80000004': 'AC/DC Power Fail',
    r'80000005': 'Main SoC CPU Power Fail',
    r'80000006': 'Main SoC GFX Power Fail',
    r'80000007': 'Main SoC Thrm High Temperature Abnormality',
    r'80000008': 'Drive Dead Notify Timeout',
    r'80000009': 'AC In Detect(12v)',
    r'8000000A': 'VRM HOT Fatal',
    r'8000000B': 'Unexpected Thermal Shutdown in state that Fatal OFF is not allowed',
    r'8000000C': 'MSoC Temperature Alert',
    r'80000024': 'MEMIO(2) Init FAIL(SoC) (?)',
    r'80800024': 'MEMIO(2) Init FAIL(SoC) (?)',
    r'80850000': 'VRM CPU (2)',
    r'8085[0-9A-Fa-f]{4}': 'VRM CPU (2) (?)',
    r'80860000': 'VRM GPU(6)',
    r'8086[0-9A-Fa-f]{4}': 'VRM GPU(6) (?)',
    r'8080[0-9A-Fa-f]{4}': 'Fatal Shutdown by OS request',
    r'80810001': 'FORCE_Fatal_Off - PSQ Error',
    r'80810002': 'PSQ NVS Access Error',
    r'80810013': 'PSQ ScCmd DRAM Init Error',
    r'80810014': 'PSQ ScCmd Link Up Failure',
    r'80830000': 'Power Group 2 Init Fail (?)',
    r'8084[0-9A-Fa-f]{4}': 'PCIe Link Down',
    r'80870001': 'Titania RAM Protect Error',
    r'80870002': 'Titania RAM Parity Error',
    r'80870003': 'Titania Boot Failed : Couldn\'t read Chip Revision.',
    r'80870004': 'Titania Boot Failed : Couldn\'t read error information.',
    r'80870005': 'Titania Boot Failed : State Error',
    r'808710[0-9A-Fa-f]{2}': 'Titania ScCmd Response Error',
    r'8088[0-9A-Fa-f]{1}[A-Z]{3}': 'Titania Boot EAP Error',
    r'8089[0-9A-Fa-f]{1}[A-Z]{3}': 'Titania Boot EFC Error',
    r'808A[0-9A-Fa-f]{4}': 'Titania Temperature Error',
    r'808B[0-9A-Fa-f]{3}[A-Z]{1}': 'Titania Watch Dog Timer',
    r'808C[0-9A-Fa-f]{4}': 'USB Type-C Error',
    r'808D0000': 'Thermal Shutdown : Main SoC',
    r'808D0001': 'Thermal Shutdown : Local Sensor 1',
    r'808D0002': 'Thermal Shutdown : Local Sensor 2',
    r'808D0003': 'Thermal Shutdown : Local Sensor 3',
    r'808E0000': 'EAP_Fail (SSD_CON)',
    r'808E0001': 'EAP_Fail (SSD_CON)',
    r'808E0002': 'EAP_Fail (SSD_CON)',
    r'808E0003': 'EAP_Fail (SSD_CON)',
    r'808E0004': 'EAP_Fail (SSD_CON)',
    r'808E0005': 'EAP_Fail (SSD_CON) - Sig 1',
    r'808E0006': 'EAP_Fail (SSD_CON)',
    r'808E0007': 'EAP_Fail (SSD_CON)',
    r'808F0001': 'SMCU (SSD_CON > EMC) (?)',
    r'808F0002': 'SMCU (SSD_CON > EMC) (?)',
    r'808F0003': 'SMCU (SSD_CON > EMC) (?)',
    r'808F00FF': 'SMCU (SSD_CON > EMC) (?)',
    r'8090[0-9A-Fa-f]{4}': 'Fatal Shutdown - OS CRASH',
    r'8091[0-9A-Fa-f]{4}': 'SSD PMIC Error',
    r'80C00114': 'WatchDog For SoC',
    r'80C00115': 'WatchDog For EAP',
    r'80C0012C': 'BD Drive Detached',
    r'80C0012D': 'EMC Watch Dog Timer Error',
    r'80C0012E': 'ADC Error (Button)',
    r'80C0012F': 'ADC Error (BD Drive)',
    r'80C00130': 'ADC Error (AC In Det)',
    r'80C00131': 'USB Over Current',
    r'80C00132': 'FAN Storage Access Failed',
    r'80C00133': 'USB-BT FW Header Invalid Header',
    r'80C00134': 'USB-BT BT Command Error',
    r'80C00135': 'USB-BT Memory Malloc Failed',
    r'80C00136': 'USB-BT Device Not Found',
    r'80C00137': 'USB-BT MISC Error',
    r'80C00138': 'Titania Interrupt HW Error',
    r'80C00139': 'BD Drive Eject Assert Delayed',
    r'80801101': 'RAM GDDR6 1',
    r'80801102': 'RAM GDDR6 2',
    r'80801103': 'RAM GDDR6 1 2',
    r'80801104': 'RAM GDDR6 3',
    r'80801105': 'RAM GDDR6 1 3',
    r'80801106': 'RAM GDDR6 2 3',
    r'80801107': 'RAM GDDR6 1 2 3',
    r'80801108': 'RAM GDDR6 4',
    r'80801109': 'RAM GDDR6 1 4',
    r'8080110A': 'RAM GDDR6 2 4',
    r'8080110B': 'RAM GDDR6 1 2 4',
    r'8080110C': 'RAM GDDR6 3 4',
    r'8080110D': 'RAM GDDR6 1 3 4',
    r'8080110E': 'RAM GDDR6 2 3 4',
    r'8080110F': 'RAM GDDR6 1 2 3 4',
    r'80801110': 'RAM GDDR6 5',
    r'80801111': 'RAM GDDR6 1 5',
    r'80801112': 'RAM GDDR6 2 5',
    r'80801113': 'RAM GDDR6 1 2 5',
    r'80801114': 'RAM GDDR6 3 5',
    r'80801115': 'RAM GDDR6 1 3 5',
    r'80801116': 'RAM GDDR6 2 3 5',
    r'80801117': 'RAM GDDR6 1 2 3 5',
    r'80801118': 'RAM GDDR6 4 5',
    r'80801119': 'RAM GDDR6 1 4 5',
    r'8080111A': 'RAM GDDR6 2 4 5',
    r'8080111B': 'RAM GDDR6 1 2 4 5',
    r'8080111C': 'RAM GDDR6 3 4 5',
    r'8080111D': 'RAM GDDR6 1 3 4 5',
    r'8080111E': 'RAM GDDR6 2 3 4 5',
    r'8080111F': 'RAM GDDR6 1 2 3 4 5',
    r'8080[0-9A-Fa-f]{4}': 'Fatal_OFF by BigOs - Failed to Start OS Kernel',
    r'FFFFFFFF': 'No Error',  # Added the missing comma here
    r'C001[0-9A-Fa-f]{4}': 'Main SoC Access Error (I2C)',
    r'C002[0-9A-Fa-f]{4}': 'Main SoC Access Error (SB-TSI I2C)',
    r'C003[0-9A-Fa-f]{4}': 'Main SoC Access Error (SB-RMI)',
    r'C00B[0-9A-Fa-f]{4}': 'Serial Flash Access Error',
    r'C00C[0-9A-Fa-f]{4}': 'VRM Controller Access Error',
    r'C00D[0-9A-Fa-f]{4}': 'PMIC (Subsystem) Access Error',
    r'C010[0-9A-Fa-f]{4}': 'Flash Controller Access Error',
    r'C011[0-9A-Fa-f]{4}': 'Potentiometer Access Error',
    r'C015[0-9A-Fa-f]{4}': 'PCIe Access Error',
    r'C016[0-9A-Fa-f]{4}': 'PMIC (SSD) Access Error',
    r'C081[0-9A-Fa-f]{4}': 'HDMI Tx Access Error',
    r'C090[0-9A-Fa-f]{4}': 'USB Type-C PD Controller Access Error',
    r'C091[0-9A-Fa-f]{4}': 'USB Type-C USB/DP Mux Access Error',
    r'C092[0-9A-Fa-f]{4}': 'USB Type-C Redriver Access Error',
    r'C0FE[0-9A-Fa-f]{4}': 'Dummy'


}


seq_database = {
    "EmcBootup": [0x2002, 0x2067, 0x2064, 0x218E],
    "Subsystem Peripheral Initialize": [0x2003, 0x2005, 0x2004],
    "aEmcTimerIniti": [0x2008, 0x2009, 0x200A, 0x200B],
    "aPowerGroup2On 1": [0x200C, 0x2109, 0x200D, 0x2011, 0x200E, 0x200F, 0x2010, 0x202E, 0x2006, 0x21AF, 0x21B1],
    "aPowerGroup2Off": [0x2014, 0x202F, 0x2015, 0x2016, 0x202B, 0x2017, 0x210A, 0x2018, 0x2019],
    "aSbPcieInitiali": [0x201A, 0x2030, 0x2031],
    "aSbPcieInitiali 1": [0x2066, 0x2030, 0x2031],
    "aEfcBootModeSet": [0x208D, 0x210B, 0x210C, 0x210D],
    "Flash Controller ON EFC": [0x201D, 0x2027, 0x2110, 0x2033, 0x2089, 0x2035],
    "Flash Controller ON EAP": [0x201D, 0x2027, 0x2110, 0x2033, 0x2089, 0x2035],
    "Flash Controller Soft reset": [0x2027, 0x2032, 0x2033, 0x2089, 0x2035],
    "Subsystem PCIe USP Enable": [0x201C],
    "Subsystem PCIe DSP Enable": [0x2029, 0x2107],
    "Flash Controller Initialization EFC": [0x2159, 0x2045, 0x2038, 0x2043, 0x2041],
    "Flash Controller Initialization EAP": [0x2159, 0x2045, 0x2043, 0x2041, 0x2047],
    "Flash Controller OFF EFC": [0x204C, 0x2108, 0x206D, 0x2014, 0x2034, 0x208A, 0x210F, 0x2028, 0x201E],
    "Flash Controller OFF EAP": [0x2046, 0x2108, 0x206D, 0x2014, 0x2034, 0x208A, 0x210F, 0x2028, 0x201E],
    "Flash Controller STOP EFC": [0x204C, 0x2046, 0x2108, 0x206D, 0x2014, 0x2028, 0x2048],
    "Flash Controller STOP EAP": [0x204D, 0x2046, 0x2108, 0x206D, 0x2014, 0x2028, 0x2048],
    "Flash Controller SRAM Keep Enable": [0x2049],
    "Subsystem PG2 reset": [0x2016, 0x200E, 0x2010, 0x202E, 0x2006],
    "ACDC 12V ON": [0x2111, 0x2113, 0x2052, 0x2085, 0x2054, 0x2087],
    "USB VBUS On": [0x216F, 0x211B],
    "BD Drive Power On": [0x211D],
    "Main SoC Power ON Cold Boot": [0x203A, 0x203D, 0x2126, 0x2128, 0x212A, 0x2135, 0x211F, 0x2189, 0x218B, 0x21B6, 0x21B8, 0x21BA, 0x2023, 0x2125, 0x2167, 0x21C1, 0x21C3, 0x2121, 0x21C5, 0x2175, 0x2133, 0x2141, 0x205F, 0x218D, 0x21BE, 0x21C0, 0x21C4, 0x2123, 0x2136, 0x2137, 0x216D, 0x2060, 0x2061, 0x2025],
    "Main SoC Power ON S3 Exit": [0x203A, 0x203D, 0x2128, 0x212A, 0x2135, 0x2023, 0x2167, 0x21C1, 0x2175, 0x2133, 0x2141, 0x205F, 0x218D, 0x21BE, 0x21C0, 0x21C4, 0x2123, 0x2136, 0x2137, 0x216D, 0x2060, 0x2061, 0x2025],
    "Main SoC Reset Release": [0x2127, 0x204A, 0x2129, 0x21A3, 0x21A5, 0x21A7, 0x21A9, 0x21AB, 0x21AD, 0x212F, 0x2169, 0x2161, 0x21B3, 0x21B5, 0x213C, 0x213D, 0x213F, 0x2050, 0x2083, 0x2187, 0x2195, 0x2197, 0x2155, 0x205C, 0x217F],
    "MSOC Reset Moni High": [0x212B, 0x2157],
    "Main SoC Power Off": [0x208F, 0x2040, 0x2156, 0x2196, 0x2198, 0x2188, 0x2084, 0x2051, 0x213E, 0x2140, 0x2162, 0x216A, 0x21B4, 0x2130, 0x217D, 0x206C, 0x215E, 0x2026, 0x2138, 0x2139, 0x2142, 0x21BF, 0x21C2, 0x2168, 0x2135, 0x2124, 0x2176, 0x212C, 0x2158, 0x205D, 0x213B],
    "BD Drive Power Off": [0x211E],
    "USB VBUS Off": [0x211C, 0x216F],
    "ACDC 12V Off": [0x2114, 0x2112, 0x207A, 0x2086, 0x2053, 0x2088, 0x2055],
    "FC NAND Close Not urgent": [0x204B, 0x2035, 0x2040, 0x2042, 0x2044],
    "FC NAND Close Urgent": [0x204B, 0x2035, 0x2042, 0x2044],
    "FATAL OFF": [0x204B, 0x208F, 0x212C, 0x2158, 0x212E, 0x2156, 0x213E, 0x2140, 0x2162, 0x216A, 0x21B4, 0x2130, 0x217D, 0x206C, 0x215E, 0x2026, 0x2138, 0x2139, 0x2142, 0x21BF, 0x21C2, 0x2168, 0x2135, 0x2124, 0x2176, 0x2024, 0x2152, 0x2122, 0x2064, 0x21AA, 0x21AC, 0x21AE, 0x21A4, 0x21A6, 0x21A8, 0x2126, 0x21B7, 0x21B9, 0x21BB, 0x218C, 0x218A, 0x2120, 0x211E, 0x211C, 0x2118, 0x2073, 0x2075, 0x2079, 0x2071, 0x204F, 0x2022, 0x2116, 0x2108, 0x208C, 0x2034, 0x208A, 0x2165, 0x210F, 0x2028, 0x201E, 0x201B, 0x208E, 0x2174, 0x2164, 0x216C, 0x21B2, 0x21B0, 0x2012, 0x206D, 0x2014, 0x202F, 0x2015, 0x2016, 0x202B, 0x2017, 0x210A, 0x2018, 0x2114, 0x2112, 0x2086, 0x2053, 0x2088, 0x2055, 0x2091, 0x2057, 0x2192, 0x2190, 0x217E, 0x2105, 0x2092],
    "EAP Boot Mode Set": [0x208D, 0x210B, 0x210C, 0x210E],
    "EAP Reset Moni de assert": [0x212D],
    "EAP Reset Moni Assert": [0x212E, 0x205D, 0x213B],
    "FAN CONTROL Parameter Reset": [0x205E],
    "EMC SoC Handshake STR": [0x2065],
    "USB OC Moni de assert": [0x2152],
    "GDDR6 USB Power On": [0x211F, 0x2189, 0x218B, 0x21B6, 0x21B8, 0x21BA, 0x2125],
    "USB OC Moni Assert": [0x2151],
    "HDMI Standby": [0x2068],
    "WLAN Module USB Enable": [0x2106],
    "Main SoC Thermal Moni Stop": [0x2196, 0x2198, 0x2188, 0x2084, 0x2051],
    "WLAN Module Reset": [0x217B, 0x2105, 0x2069, 0x2106],
    "1GbE NIC Reset de assert": [0x215A],
    "1GbE NIC Reset assert": [0x215B],
    "HDMI CECStart": [0x2115, 0x2021, 0x204E, 0x2070, 0x2078, 0x206E, 0x2074, 0x2072, 0x206E, 0x2074],
    "HDMI CECStop": [0x2073, 0x2075, 0x2079, 0x2071, 0x204F, 0x2022, 0x2116],
    "HDMIStop": [0x2077, 0x2075, 0x2068],
    "CECStart": [0x2115, 0x206E],
    "CECStop": [0x2077, 0x206C, 0x2070, 0x2078],
    "MDCDC ON": [0x215F],
    "MDCDC Off": [0x2160],
    "Titania2 GPIO Glitch Issue WA": [0x208E],
    "Check AC IN DETECT": [0x216E],
    "Check BD DETECT": [0x2170],
    "GPI SW Open": [0x2173],
    "GPI SW Close": [0x2174],
    "Devkit IO Expander Initialize": [0x2102],
    "Salina PMIC Register Initialize": [0x2177],
    "Disable AC IN DETECT": [0x2178],
    "BT WAKE Enabled": [0x2179],
    "BT WAKE Disabled": [0x217B],
    "Stop PCIePLL NoSS part": [0x2094],
    "Titania PMIC Register Initialize": [0x217A],
    "Setup FC for BTFW DL": [0x203B, 0x2039],
    "BTFW Download": [0x217C],
    "WM Reset": [0x217B, 0x2105, 0x2069, 0x2106],
    "Telstar ROM Boot Wait": [0x2095],
    "Stop PCIePLL SS NOSS part": [0x201B],
    "Stop PCIePLL SS part": [0x2082],
    "Stop Subsystem PG2 Bus Error Detection(DDR4 BufferOverflow)": [0x2013],
    "Stop SFlash DMA": [0x2012],
    "Local Temp.3 ON": [0x2056, 0x2090],
    "Local Temp.3 OFF": [0x2091, 0x2057],
    "Fan Servo Parameter Reset": [0x217E],
    "Cold reset WA": [0x2051, 0x213E, 0x2140, 0x217D, 0x2127, 0x2129, 0x213C, 0x213D, 0x213F, 0x2050, 0x205C, 0x217F],
    "FAN Control Start at Restmode during US": [0x2180, 0x2181, 0x2182, 0x2193],
    "FAN Control Stop at Restmode during USB": [0x2183, 0x2184, 0x2185, 0x2194],
    "Read Titania PMIC Register": [0x2186],
    "Subsystem PCIe DSP Enable BT DL": [0x2029],
    "I2C Open": [0x219B, 0x219C, 0x219D, 0x219E, 0x2199, 0x219A],
    "Drive FAN Control Stop": [0x21A0, 0x219F],
    "Drive FAN Control Start": [0x21A1, 0x21A2],
    "USB OC Moni de assert 2": [0x21AA, 0x21AC, 0x21AE],
    "USB VBUS Off 2": [0x21A4, 0x21A6, 0x21A8],
    "USB VBUS On 2": [0x21A3, 0x21A5, 0x21A7, 0x21A9, 0x21AB, 0x21AD],
    "Dev BD Drive Power On": [0x211D],
    "Dev BD Drive Power Off": [0x211E],
    "Dev USB VBUS On": [0x216F, 0x211B],
    "Dev WLAN BT RESET NEGATE": [0x2106],
    "Dev WLAN BT RESET ASSERT": [0x217B, 0x2105, 0x2069],
    "Dev WLAN BT RESET ASSERT NEGATE": [0x217B, 0x2105, 0x2069, 0x2106],
    "Dev HDMI 5V Power On": [0x2117],
    "Dev HDMI 5V Power Off": [0x2118],
    "Dev VBURN ON": [0x2134],
    "Dev VBURN OFF": [0x2135],
    "Dev WLAN BT PCIE RESET NEGATE": [0x2107],
    "Dev WLAN BT PCIE RESET ASSERT": [0x2108, 0x2069],
    "Dev WLAN BT PCIE RESET ASSERT NEGATE": [0x2108, 0x2069, 0x2107],
    "Dev USBA1 VBUS On": [0x21A3, 0x21A9],
    "Dev USBA1 VBUS Off": [0x21AA, 0x21A4],
    "Dev USBA2 VBUS On": [0x21A5, 0x21AB],
    "Dev USBA2 VBUS Off": [0x21AC, 0x21A6],
    "Dev USBA3 VBUS On": [0x21A7, 0x21AD],
    "Dev USBA3 VBUS Off": [0x21AE, 0x21A8],
}


# Map of power states, describing what each state means in the system
pow_state_map = {
    0x00: "ACIN_L Before Standby",
    0x01: "STANDBY",
    0x02: "PG2_ON",
    0x03: "EFC_ON",
    0x04: "EAP_ON",
    0x05: "SOC_ON",
    0x06: "ERROR_DET",
    0x07: "FATAL_ERROR",
    0x08: "NEVER_BOOT",
    0x09: "FORCE_OFF",
    0x0A: "FORCE_OFF BT Firmware Download",
    # Feel free to add more states here as you encounter them
}

# This is where we map boot-up causes (what triggered the device to start up)
upcause_map = {
    26: "DEV UART",
    19: "BT (Bluetooth)",
    18: "CEC (HDMI-CEC)",
    17: "EAP (EAP's order)",
    16: "Main SoC",
    10: "Eject Button",
    9: "Disc Loaded",
    8: "Power Button",
    0: "Boot-Up at power-on"
}

# Here we list what devices are responsible for triggering power management actions
devpm_map = {
    4: "HDMI(5V)",
    3: "BD DRIVE",
    2: "HDMI(CEC)",
    1: "USB",
    0: "WLAN"
}

def parse_log_files(file_pattern):
    # Get the path of the current directory where this script is located
    current_directory = os.path.dirname(os.path.realpath(__file__))
    
    # Find files matching the pattern
    matching_files = [f for f in os.listdir(current_directory) if re.match(file_pattern, f)]
    
    if not matching_files:
        print(f"No files matching pattern '{file_pattern}' found in the current directory.")
        return []
    
    return matching_files


# Convert the temperature from hex format to Celsius
def convert_to_celsius(hex_value):
    try:
        # Convert hex to integer, then to Celsius
        temp_value = int(hex_value, 16)
        temp_celsius = temp_value / 256.0
        return round(temp_celsius, 2)  # Return the temperature rounded to 2 decimal places
    except ValueError:
        # If the hex value isn't valid, just return None
        return None

def get_seq_description(seq_no):
    """This function looks up the description for a given sequence number."""
    for pattern, description in seq_database.items():
        if re.match(pattern, seq_no):
            return description
    return "Unknown SeqNo"  # If no match is found, return a fallback message

def get_code_description(code):
    """This function returns a description for a given error code."""
    for pattern, description in code_database.items():
        if re.match(pattern, code):
            return description
    return "Unknown Code"  # In case the code is not recognized

# Get the human-readable description for the PowState
def get_pow_state_description(pow_state_value):
    return pow_state_map.get(pow_state_value, "Unknown PowState")

# Get the flags for boot-up causes based on the given value
def get_upcause_flags(upcause_value):
    causes = []
    for bit, description in upcause_map.items():
        if upcause_value & (1 << bit):
            causes.append(description)
    return causes if causes else ["No Boot Cause"]  # Return a list of causes, or a fallback message

# Get the flags for device power management based on the given value
def get_devpm_flags(devpm_value):
    devices = []
    for bit, description in devpm_map.items():
        if devpm_value & (1 << bit):
            devices.append(description)
    return devices if devices else ["No Device Power"]  # Return devices or a fallback message

# Main function to process the log data and output it to a readable file
import os
import re

def parse_log_file(file_name):
    # Get the path of the current directory where this script is located
    current_directory = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_directory, file_name)
    
    try:
        # Open and read the log file
        with open(file_path, 'r') as file:
            log_data = file.readlines()
        return log_data
    except FileNotFoundError:
        # If the file is not found, let the user know
        print(f"File {file_name} not found in the current directory.")
        return []

# Convert the temperature from hex format to Celsius
def convert_to_celsius(hex_value):
    try:
        # Convert hex to integer, then to Celsius
        temp_value = int(hex_value, 16)
        temp_celsius = temp_value / 256.0
        return round(temp_celsius, 2)  # Return the temperature rounded to 2 decimal places
    except ValueError:
        # If the hex value isn't valid, just return None
        return None

def get_seq_description(seq_no):
    """This function looks up the description for a given sequence number."""
    for pattern, description in seq_database.items():
        if re.match(pattern, seq_no):
            return description
    return "Unknown SeqNo"  # If no match is found, return a fallback message

def get_code_description(code):
    """This function returns a description for a given error code."""
    for pattern, description in code_database.items():
        if re.match(pattern, code):
            return description
    return "Unknown Code"  # In case the code is not recognized

# Get the human-readable description for the PowState
def get_pow_state_description(pow_state_value):
    return pow_state_map.get(pow_state_value, "Unknown PowState")

# Get the flags for boot-up causes based on the given value
def get_upcause_flags(upcause_value):
    causes = []
    for bit, description in upcause_map.items():
        if upcause_value & (1 << bit):
            causes.append(description)
    return causes if causes else ["No Boot Cause"]  # Return a list of causes, or a fallback message

# Get the flags for device power management based on the given value
def get_devpm_flags(devpm_value):
    devices = []
    for bit, description in devpm_map.items():
        if devpm_value & (1 << bit):
            devices.append(description)
    return devices if devices else ["No Device Power"]  # Return devices or a fallback message

def generate_output_filename(input_file_name):
    # Extract the prefix from the input file name
    prefix = os.path.splitext(input_file_name)[0]
    base_output_filename = f"Decoded_{prefix}"

    index = 1
    while os.path.exists(f"{base_output_filename}_{index}.txt"):
        index += 1

    return f"{base_output_filename}_{index}.txt"

def process_log_and_write_output(parsed_data, input_file_name):
    output_lines = []
    
    for line in parsed_data:
        # Skip lines that are either comments or empty
        if line.startswith("#") or not line.strip():
            continue
        
        # Split the line by spaces to extract data
        parts = line.split()
        
        if len(parts) >= 11:  # Check if the line has enough data fields
            try:
                # Extract relevant information from the line
                code = parts[1]
                rtc = parts[2]
                pow_state_value = int(parts[3], 16)
                upcause_value = int(parts[4], 16)
                seq_no = parts[6]
                devpm_value = int(parts[7], 16)
                t_soc = parts[8]
                t_env = parts[9]

                # Get descriptions for each piece of data
                seq_description = get_seq_description(seq_no)
                code_description = get_code_description(code)

                # Convert temperature values to Celsius
                t_soc_celsius = convert_to_celsius(t_soc)
                t_env_celsius = convert_to_celsius(t_env)

                # Get the PowState description
                pow_state_description = get_pow_state_description(pow_state_value)

                # Get boot-up causes and device power management flags
                upcause_flags = get_upcause_flags(upcause_value)
                devpm_flags = get_devpm_flags(devpm_value)

                # Format the output line in a more readable way
                readable_line = (f"Code: {code} ({code_description}),\n "
                                 f"SeqNo: {seq_no} ({seq_description}),\n "
                                 f"T(SoC): {t_soc_celsius}°C,\n "
                                 f"T(Env): {t_env_celsius}°C,\n "
                                 f"PowState: {pow_state_description},\n "
                                 f"UPCAUSE: {', '.join(upcause_flags)},\n "
                                 f"devpm: {', '.join(devpm_flags)}\n \n")
                output_lines.append(readable_line)

            except ValueError as e:
                # If there's an error processing the line, print it out and move to the next
                print(f"Error processing line: {line.strip()} - {e}")
                continue

    # Generate the output file name based on the input file name
    output_file_name = generate_output_filename(input_file_name)

    # Save the parsed log to a new file
    output_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), output_file_name)
    with open(output_file_path, "w") as output_file:
        output_file.writelines(output_lines)

    print(f"Log file '{input_file_name}' parsed successfully.")
    print(f"The parsed log has been saved as '{output_file_name}'.")

log_file_pattern = r'.*EMC_LOG\.txt$'
matching_files = parse_log_files(log_file_pattern)

for file_name in matching_files:
    parsed_data = parse_log_file(file_name)
    process_log_and_write_output(parsed_data, file_name)
