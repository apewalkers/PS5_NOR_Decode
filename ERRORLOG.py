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
    "2002": "EmcBootup",
    "2067": "EmcBootup",
    "2064": "EmcBootup",
    "218E": "EmcBootup",
    "2003": "Subsystem Peripheral Initialize",
    "2005": "Subsystem Peripheral Initialize",
    "2004": "Subsystem Peripheral Initialize",
    "2008": "aEmcTimerIniti",
    "2009": "aEmcTimerIniti",
    "200A": "aEmcTimerIniti",
    "200B": "aEmcTimerIniti",
    "200C": "aPowerGroup2On 1",
    "2109": "aPowerGroup2On 1",
    "200D": "aPowerGroup2On 1",
    "2011": "aPowerGroup2On 1",
    "200E": "aPowerGroup2On 1",
    "200F": "aPowerGroup2On 1",
    "2010": "aPowerGroup2On 1",
    "202E": "aPowerGroup2On 1",
    "2006": "aPowerGroup2On 1",
    "21AF": "aPowerGroup2On 1",
    "21B1": "aPowerGroup2On 1",
    "2014": "aPowerGroup2Off",
    "202F": "aPowerGroup2Off",
    "2015": "aPowerGroup2Off",
    "2016": "aPowerGroup2Off",
    "202B": "aPowerGroup2Off",
    "2017": "aPowerGroup2Off",
    "210A": "aPowerGroup2Off",
    "2018": "aPowerGroup2Off",
    "2019": "aPowerGroup2Off",
    "201A": "aSbPcieInitiali",
    "2030": "aSbPcieInitiali",
    "2031": "aSbPcieInitiali",
    "2066": "aSbPcieInitiali 1",
    "2030": "aSbPcieInitiali 1",
    "2031": "aSbPcieInitiali 1",
    "208D": "aEfcBootModeSet",
    "210B": "aEfcBootModeSet",
    "210C": "aEfcBootModeSet",
    "210D": "aEfcBootModeSet",
    "201D": "Flash Controller ON EFC",
    "2027": "Flash Controller ON EFC",
    "2110": "Flash Controller ON EFC",
    "2033": "Flash Controller ON EFC",
    "2089": "Flash Controller ON EFC",
    "2035": "Flash Controller ON EFC",
    "201D": "Flash Controller ON EAP",
    "2027": "Flash Controller ON EAP",
    "2110": "Flash Controller ON EAP",
    "2033": "Flash Controller ON EAP",
    "2089": "Flash Controller ON EAP",
    "2035": "Flash Controller ON EAP",
    "2027": "Flash Controller Soft reset",
    "2032": "Flash Controller Soft reset",
    "2033": "Flash Controller Soft reset",
    "2089": "Flash Controller Soft reset",
    "2035": "Flash Controller Soft reset",
    "201C": "Subsystem PCIe USP Enable",
    "2029": "Subsystem PCIe DSP Enable",
    "2107": "Subsystem PCIe DSP Enable",
    "2159": "Flash Controller Initialization EFC",
    "2045": "Flash Controller Initialization EFC",
    "2038": "Flash Controller Initialization EFC",
    "2043": "Flash Controller Initialization EFC",
    "2041": "Flash Controller Initialization EFC",
    "2159": "Flash Controller Initialization EAP",
    "2045": "Flash Controller Initialization EAP",
    "2043": "Flash Controller Initialization EAP",
    "2041": "Flash Controller Initialization EAP",
    "2047": "Flash Controller Initialization EAP",
    "204C": "Flash Controller OFF EFC",
    "2108": "Flash Controller OFF EFC",
    "206D": "Flash Controller OFF EFC",
    "2014": "Flash Controller OFF EFC",
    "2034": "Flash Controller OFF EFC",
    "208A": "Flash Controller OFF EFC",
    "210F": "Flash Controller OFF EFC",
    "2028": "Flash Controller OFF EFC",
    "201E": "Flash Controller OFF EFC",
    "2046": "Flash Controller OFF EAP",
    "2108": "Flash Controller OFF EAP",
    "206D": "Flash Controller OFF EAP",
    "2014": "Flash Controller OFF EAP",
    "2034": "Flash Controller OFF EAP",
    "208A": "Flash Controller OFF EAP",
    "210F": "Flash Controller OFF EAP",
    "2028": "Flash Controller OFF EAP",
    "201E": "Flash Controller OFF EAP",
    "204C": "Flash Controller STOP EFC",
    "2046": "Flash Controller STOP EFC",
    "2108": "Flash Controller STOP EFC",
    "206D": "Flash Controller STOP EFC",
    "2014": "Flash Controller STOP EFC",
    "2028": "Flash Controller STOP EFC",
    "2048": "Flash Controller STOP EFC",
    "204D": "Flash Controller STOP EAP",
    "2046": "Flash Controller STOP EAP",
    "2108": "Flash Controller STOP EAP",
    "206D": "Flash Controller STOP EAP",
    "2014": "Flash Controller STOP EAP",
    "2028": "Flash Controller STOP EAP",
    "2048": "Flash Controller STOP EAP",
    "2049": "Flash Controller SRAM Keep Enable",
    "2016": "Subsystem PG2 reset",
    "200E": "Subsystem PG2 reset",
    "2010": "Subsystem PG2 reset",
    "202E": "Subsystem PG2 reset",
    "2006": "Subsystem PG2 reset",
    "2111": "ACDC 12V ON",
    "2113": "ACDC 12V ON",
    "2052": "ACDC 12V ON",
    "2085": "ACDC 12V ON",
    "2054": "ACDC 12V ON",
    "2087": "ACDC 12V ON",
    "216F": "USB VBUS On",
    "211B": "USB VBUS On",
    "211D": "BD Drive Power On",
    "203A": "Main SoC Power ON Cold Boot",
    "203D": "Main SoC Power ON Cold Boot",
    "2126": "Main SoC Power ON Cold Boot",
    "2128": "Main SoC Power ON Cold Boot",
    "212A": "Main SoC Power ON Cold Boot",
    "2135": "Main SoC Power ON Cold Boot",
    "211F": "Main SoC Power ON Cold Boot",
    "2189": "Main SoC Power ON Cold Boot",
    "218B": "Main SoC Power ON Cold Boot",
    "21B6": "Main SoC Power ON Cold Boot",
    "21B8": "Main SoC Power ON Cold Boot",
    "21BA": "Main SoC Power ON Cold Boot",
    "2023": "Main SoC Power ON Cold Boot",
    "2125": "Main SoC Power ON Cold Boot",
    "2167": "Main SoC Power ON Cold Boot",
    "21C1": "Main SoC Power ON Cold Boot",
    "21C3": "Main SoC Power ON Cold Boot",
    "2121": "Main SoC Power ON Cold Boot",
    "21C5": "Main SoC Power ON Cold Boot",
    "2175": "Main SoC Power ON Cold Boot",
    "2133": "Main SoC Power ON Cold Boot",
    "2141": "Main SoC Power ON Cold Boot",
    "205F": "Main SoC Power ON Cold Boot",
    "218D": "Main SoC Power ON Cold Boot",
    "21BE": "Main SoC Power ON Cold Boot",
    "21C0": "Main SoC Power ON Cold Boot",
    "21C4": "Main SoC Power ON Cold Boot",
    "2123": "Main SoC Power ON Cold Boot",
    "2136": "Main SoC Power ON Cold Boot",
    "2137": "Main SoC Power ON Cold Boot",
    "216D": "Main SoC Power ON Cold Boot",
    "2060": "Main SoC Power ON Cold Boot",
    "2061": "Main SoC Power ON Cold Boot",
    "2025": "Main SoC Power ON Cold Boot",
    "203A": "Main SoC Power ON S3 Exit",
    "203D": "Main SoC Power ON S3 Exit",
    "2128": "Main SoC Power ON S3 Exit",
    "212A": "Main SoC Power ON S3 Exit",
    "2135": "Main SoC Power ON S3 Exit",
    "2023": "Main SoC Power ON S3 Exit",
    "2167": "Main SoC Power ON S3 Exit",
    "21C1": "Main SoC Power ON S3 Exit",
    "2175": "Main SoC Power ON S3 Exit",
    "2133": "Main SoC Power ON S3 Exit",
    "2141": "Main SoC Power ON S3 Exit",
    "205F": "Main SoC Power ON S3 Exit",
    "218D": "Main SoC Power ON S3 Exit",
    "21BE": "Main SoC Power ON S3 Exit",
    "21C0": "Main SoC Power ON S3 Exit",
    "21C4": "Main SoC Power ON S3 Exit",
    "2123": "Main SoC Power ON S3 Exit",
    "2136": "Main SoC Power ON S3 Exit",
    "2137": "Main SoC Power ON S3 Exit",
    "216D": "Main SoC Power ON S3 Exit",
    "2060": "Main SoC Power ON S3 Exit",
    "2061": "Main SoC Power ON S3 Exit",
    "2025": "Main SoC Power ON S3 Exit",
    "2127": "Main SoC Reset Release",
    "204A": "Main SoC Reset Release",
    "2129": "Main SoC Reset Release",
    "21A3": "Main SoC Reset Release",
    "21A5": "Main SoC Reset Release",
    "21A7": "Main SoC Reset Release",
    "21A9": "Main SoC Reset Release",
    "21AB": "Main SoC Reset Release",
    "21AD": "Main SoC Reset Release",
    "212F": "Main SoC Reset Release",
    "2169": "Main SoC Reset Release",
    "2161": "Main SoC Reset Release",
    "21B3": "Main SoC Reset Release",
    "21B5": "Main SoC Reset Release",
    "213C": "Main SoC Reset Release",
    "213D": "Main SoC Reset Release",
    "213F": "Main SoC Reset Release",
    "2050": "Main SoC Reset Release",
    "2083": "Main SoC Reset Release",
    "2187": "Main SoC Reset Release",
    "2195": "Main SoC Reset Release",
    "2197": "Main SoC Reset Release",
    "2155": "Main SoC Reset Release",
    "205C": "Main SoC Reset Release",
    "217F": "Main SoC Reset Release",
    "212B": "MSOC Reset Moni High",
    "2157": "MSOC Reset Moni High",
    "208F": "Main SoC Power Off",
    "2040": "Main SoC Power Off",
    "2156": "Main SoC Power Off",
    "2196": "Main SoC Power Off",
    "2198": "Main SoC Power Off",
    "2188": "Main SoC Power Off",
    "2084": "Main SoC Power Off",
    "2051": "Main SoC Power Off",
    "213E": "Main SoC Power Off",
    "2140": "Main SoC Power Off",
    "2162": "Main SoC Power Off",
    "216A": "Main SoC Power Off",
    "21B4": "Main SoC Power Off",
    "2130": "Main SoC Power Off",
    "217D": "Main SoC Power Off",
    "206C": "Main SoC Power Off",
    "215E": "Main SoC Power Off",
    "2026": "Main SoC Power Off",
    "2138": "Main SoC Power Off",
    "2139": "Main SoC Power Off",
    "2142": "Main SoC Power Off",
    "21BF": "Main SoC Power Off",
    "21C2": "Main SoC Power Off",
    "2168": "Main SoC Power Off",
    "2135": "Main SoC Power Off",
    "2124": "Main SoC Power Off",
    "2176": "Main SoC Power Off",
    "212C": "Main SoC Power Off",
    "2158": "Main SoC Power Off",
    "205D": "Main SoC Power Off",
    "213B": "Main SoC Power Off",
    "211E": "BD Drive Power Off",
    "211C": "USB VBUS Off",
    "216F": "USB VBUS Off",
    "2114": "ACDC 12V Off",
    "2112": "ACDC 12V Off",
    "207A": "ACDC 12V Off",
    "2086": "ACDC 12V Off",
    "2053": "ACDC 12V Off",
    "2088": "ACDC 12V Off",
    "2055": "ACDC 12V Off",
    "204B": "FC NAND Close Not urgent",
    "2035": "FC NAND Close Not urgent",
    "2040": "FC NAND Close Not urgent",
    "2042": "FC NAND Close Not urgent",
    "2044": "FC NAND Close Not urgent",
    "204B": "FC NAND Close Urgent",
    "2035": "FC NAND Close Urgent",
    "2042": "FC NAND Close Urgent",
    "2044": "FC NAND Close Urgent",
    "204B": "FATAL OFF",
    "208F": "FATAL OFF",
    "212C": "FATAL OFF",
    "2158": "FATAL OFF",
    "212E": "FATAL OFF",
    "2156": "FATAL OFF",
    "213E": "FATAL OFF",
    "2140": "FATAL OFF",
    "2162": "FATAL OFF",
    "216A": "FATAL OFF",
    "21B4": "FATAL OFF",
    "2130": "FATAL OFF",
    "217D": "FATAL OFF",
    "206C": "FATAL OFF",
    "215E": "FATAL OFF",
    "2026": "FATAL OFF",
    "2138": "FATAL OFF",
    "2139": "FATAL OFF",
    "2142": "FATAL OFF",
    "21BF": "FATAL OFF",
    "21C2": "FATAL OFF",
    "2168": "FATAL OFF",
    "2135": "FATAL OFF",
    "2124": "FATAL OFF",
    "2176": "FATAL OFF",
    "2024": "FATAL OFF",
    "2152": "FATAL OFF",
    "2122": "FATAL OFF",
    "2064": "FATAL OFF",
    "21AA": "FATAL OFF",
    "21AC": "FATAL OFF",
    "21AE": "FATAL OFF",
    "21A4": "FATAL OFF",
    "21A6": "FATAL OFF",
    "21A8": "FATAL OFF",
    "2126": "FATAL OFF",
    "21B7": "FATAL OFF",
    "21B9": "FATAL OFF",
    "21BB": "FATAL OFF",
    "218C": "FATAL OFF",
    "218A": "FATAL OFF",
    "2120": "FATAL OFF",
    "211E": "FATAL OFF",
    "211C": "FATAL OFF",
    "2118": "FATAL OFF",
    "2073": "FATAL OFF",
    "2075": "FATAL OFF",
    "2079": "FATAL OFF",
    "2071": "FATAL OFF",
    "204F": "FATAL OFF",
    "2022": "FATAL OFF",
    "2116": "FATAL OFF",
    "2108": "FATAL OFF",
    "208C": "FATAL OFF",
    "2034": "FATAL OFF",
    "208A": "FATAL OFF",
    "2165": "FATAL OFF",
    "210F": "FATAL OFF",
    "2028": "FATAL OFF",
    "201E": "FATAL OFF",
    "201B": "FATAL OFF",
    "208E": "FATAL OFF",
    "2174": "FATAL OFF",
    "2164": "FATAL OFF",
    "216C": "FATAL OFF",
    "21B2": "FATAL OFF",
    "21B0": "FATAL OFF",
    "2012": "FATAL OFF",
    "206D": "FATAL OFF",
    "2014": "FATAL OFF",
    "202F": "FATAL OFF",
    "2015": "FATAL OFF",
    "2016": "FATAL OFF",
    "202B": "FATAL OFF",
    "2017": "FATAL OFF",
    "210A": "FATAL OFF",
    "2018": "FATAL OFF",
    "2114": "FATAL OFF",
    "2112": "FATAL OFF",
    "2086": "FATAL OFF",
    "2053": "FATAL OFF",
    "2088": "FATAL OFF",
    "2055": "FATAL OFF",
    "2091": "FATAL OFF",
    "2057": "FATAL OFF",
    "2192": "FATAL OFF",
    "2190": "FATAL OFF",
    "217E": "FATAL OFF",
    "2105": "FATAL OFF",
    "2092": "FATAL OFF",
    "208D": "EAP Boot Mode Set",
    "210B": "EAP Boot Mode Set",
    "210C": "EAP Boot Mode Set",
    "210E": "EAP Boot Mode Set",
    "212D": "EAP Reset Moni de assert",
    "212E": "EAP Reset Moni Assert",
    "205D": "EAP Reset Moni Assert",
    "213B": "EAP Reset Moni Assert",
    "205E": "FAN CONTROL Parameter Reset",
    "2065": "EMC SoC Handshake ST",
    "2152": "USB OC Moni de assert",
    "211F": "GDDR6 USB Power On",
    "2189": "GDDR6 USB Power On",
    "218B": "GDDR6 USB Power On",
    "21B6": "GDDR6 USB Power On",
    "21B8": "GDDR6 USB Power On",
    "21BA": "GDDR6 USB Power On",
    "2125": "GDDR6 USB Power On",
    "2151": "USB OC Moni Assert",
    "2068": "HDMI Standby",
    "2106": "WLAN Module USB Enable",
    "2196": "Main SoC Thermal Moni Stop",
    "2198": "Main SoC Thermal Moni Stop",
    "2188": "Main SoC Thermal Moni Stop",
    "2084": "Main SoC Thermal Moni Stop",
    "2051": "Main SoC Thermal Moni Stop",
    "217B": "WLAN Module Reset",
    "2105": "WLAN Module Reset",
    "2069": "WLAN Module Reset",
    "2106": "WLAN Module Reset",
    "215A": "1GbE NIC Reset de assert",
    "215B": "1GbE NIC Reset assert",
    "2115": "HDMI CECStart",
    "2021": "HDMI CECStart",
    "204E": "HDMI CECStart",
    "2070": "HDMI CECStart",
    "2078": "HDMI CECStart",
    "206E": "HDMI CECStart",
    "2074": "HDMI CECStart",
    "2072": "HDMI CECStart",
    "206E": "HDMI CECStart",
    "2074": "HDMI CECStart",
    "2073": "HDMI CECStop",
    "2075": "HDMI CECStop",
    "2079": "HDMI CECStop",
    "2071": "HDMI CECStop",
    "204F": "HDMI CECStop",
    "2022": "HDMI CECStop",
    "2116": "HDMI CECStop",
    "2077": "HDMIStop",
    "2075": "HDMIStop",
    "2068": "HDMIStop",
    "2115": "CECStart",
    "206E": "CECStart",
    "2077": "CECStop",
    "206C": "CECStop",
    "2070": "CECStop",
    "2078": "CECStop",
    "215F": "MDCDC ON",
    "2160": "MDCDC Off",
    "208E": "Titania2 GPIO Glitch Issue WA",
    "216E": "Check AC IN DETECT",
    "2170": "Check BD DETECT",
    "2173": "GPI SW Open",
    "2174": "GPI SW Close",
    "2102": "Devkit IO Expander Initialize",
    "2177": "Salina PMIC Register Initialize",
    "2178": "Disable AC IN DETECT",
    "2179": "BT WAKE Enabled",
    "217B": "BT WAKE Disabled",
    "2094": "Stop PCIePLL NoSS part",
    "217A": "Titania PMIC Register Initialize",
    "203B": "Setup FC for BTFW DL",
    "2039": "Setup FC for BTFW DL",
    "217C": "BTFW Download",
    "217B": "WM Reset",
    "2105": "WM Reset",
    "2069": "WM Reset",
    "2106": "WM Reset",
    "2095": "Telstar ROM Boot Wait",
    "201B": "Stop PCIePLL SS NOSS part",
    "2082": "Stop PCIePLL SS part",
    "2013": "Stop Subsystem PG2 Bus Error Detection(DDR4 BufferOverflow)",
    "2012": "Stop SFlash DMA",
    "2056": "Local Temp.3 ON",
    "2090": "Local Temp.3 ON",
    "2091": "Local Temp.3 OFF",
    "2057": "Local Temp.3 OFF",
    "217E": "Fan Servo Parameter Reset",
    "2051": "Cold reset WA",
    "213E": "Cold reset WA",
    "2140": "Cold reset WA",
    "217D": "Cold reset WA",
    "2127": "Cold reset WA",
    "2129": "Cold reset WA",
    "213C": "Cold reset WA",
    "213D": "Cold reset WA",
    "213F": "Cold reset WA",
    "2050": "Cold reset WA",
    "205C": "Cold reset WA",
    "217F": "Cold reset WA",
    "2180": "FAN Control Start at Restmode during US",
    "2181": "FAN Control Start at Restmode during US",
    "2182": "FAN Control Start at Restmode during US",
    "2193": "FAN Control Start at Restmode during US",
    "2183": "FAN Control Stop at Restmode during USB",
    "2184": "FAN Control Stop at Restmode during USB",
    "2185": "FAN Control Stop at Restmode during USB",
    "2194": "FAN Control Stop at Restmode during USB",
    "2186": "Read Titania PMIC Registe",
    "2029": "Subsystem PCIe DSP Enable BT DL",
    "219B": "I2C Open",
    "219C": "I2C Open",
    "219D": "I2C Open",
    "219E": "I2C Open",
    "2199": "I2C Open",
    "219A": "I2C Open",
    "21A0": "Drive FAN Control Stop",
    "219F": "Drive FAN Control Stop",
    "21A1": "Drive FAN Control Start",
    "21A2": "Drive FAN Control Start",
    "21AA": "USB OC Moni de assert 2",
    "21AC": "USB OC Moni de assert 2",
    "21AE": "USB OC Moni de assert 2",
    "21A4": "USB VBUS Off 2",
    "21A6": "USB VBUS Off 2",
    "21A8": "USB VBUS Off 2",
    "21A3": "USB VBUS On 2",
    "21A5": "USB VBUS On 2",
    "21A7": "USB VBUS On 2",
    "21A9": "USB VBUS On 2",
    "21AB": "USB VBUS On 2",
    "21AD": "USB VBUS On 2",
    "211D": "Dev BD Drive Power On",
    "211E": "Dev BD Drive Power Off",
    "216F": "Dev USB VBUS On",
    "211B": "Dev USB VBUS On",
    "2106": "Dev WLAN BT RESET NEGATE",
    "217B": "Dev WLAN BT RESET ASSERT",
    "2105": "Dev WLAN BT RESET ASSERT",
    "2069": "Dev WLAN BT RESET ASSERT",
    "217B": "Dev WLAN BT RESET ASSERT NEGATE",
    "2105": "Dev WLAN BT RESET ASSERT NEGATE",
    "2069": "Dev WLAN BT RESET ASSERT NEGATE",
    "2106": "Dev WLAN BT RESET ASSERT NEGATE",
    "2117": "Dev HDMI 5V Power On",
    "2118": "Dev HDMI 5V Power Off",
    "2134": "Dev VBURN ON",
    "2135": "Dev VBURN OFF",
    "2107": "Dev WLAN BT PCIE RESET NEGATE",
    "2108": "Dev WLAN BT PCIE RESET ASSERT",
    "2069": "Dev WLAN BT PCIE RESET ASSERT",
    "2108": "Dev WLAN BT PCIE RESET ASSERT NEGATE",
    "2069": "Dev WLAN BT PCIE RESET ASSERT NEGATE",
    "2107": "Dev WLAN BT PCIE RESET ASSERT NEGATE",
    "21A3": "Dev USBA1 VBUS On",
    "21A9": "Dev USBA1 VBUS On",
    "21AA": "Dev USBA1 VBUS Off",
    "21A4": "Dev USBA1 VBUS Off",
    "21A5": "Dev USBA2 VBUS On",
    "21AB": "Dev USBA2 VBUS On",
    "21AC": "Dev USBA2 VBUS Off",
    "21A6": "Dev USBA2 VBUS Off",
    "21A7": "Dev USBA3 VBUS On",
    "21AD": "Dev USBA3 VBUS On",
    "21AE": "Dev USBA3 VBUS Off",
    "21A8": "Dev USBA3 VBUS Off"
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
    0x07: "FATAL_ERRO",
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
    return devices if devices else ["No Device Powe"]  # Return devices or a fallback message

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
    return devices if devices else ["No Device Powe"]  # Return devices or a fallback message

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
