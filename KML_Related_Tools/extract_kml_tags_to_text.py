# This file is part of Abdullah Alafari's GitHub PythonTools repository (AlafarAbdullah/PythonTools).
# It serves as a collection of Python scripts created for personal use and to share 
# knowledge and resources with the community.

# Most tools in this repository were originally developed for specific purposes 
# and later generalized for broader applications. The original use case of a script 
# may or may not be disclosed, depending on the specific context and the permission
# of any associated individuals or entities.

# Disclaimer:
# - All explanations and notes are based on personal understanding and are subject to improvement.
# - The author is not responsible for any misuse or data loss resulting from the use of this script.


# Done Adding notes and generalizing the code for the Github upload 21/Jan/2025

# Prerequisites:
# - Ensure the `.kml` file has proper XML structure and uses namespaced tags.
# - File permissions:
#   - Read access to the `.kml` file.
#   - Write access to the directory specified in `output_path`.
# - XML structure:
#   - The `.kml` file must include the specified `tag_name`. 
#   - Tags must be correctly nested as specified in queries (e.g., `"Placemark/kml:coordinates"`).

# --- Script Overview ---
# This script extracts the text of specified XML tags from a `.kml` file and saves the output as plain text.
# - `.kml` files are XML-based and store geographic data for use in mapping applications (e.g., Google Earth).
# - The script can extract specific tags (e.g., "name" or "coordinates") for summaries, reports, or further analysis.
# - Assumes the `.kml` file adheres to standard formats with correctly structured tags.

# --- Warnings ---
# - The output file will overwrite any existing file at the specified path with the same name.
# - Test the script with a small `.kml` file to verify the output before processing large datasets.

# --- Mock Data (.kml) ---
# Input file example (tag_name = "name"): 
# <?xml version='1.0' encoding='utf-8'?>
# <kml xmlns="http://www.opengis.net/kml/2.2"><Document><Placemark><name>Al Murooj (المروج)</name><description>Route Color: #00ade5
# Hub: No
# Park &amp; Ride: No
# </description><Point><coordinates>46.6544534448838,24.7545287735283,0</coordinates></Point></Placemark><Placemark><name>King Fahad District (حي الملك فهد)</name><description>Route Color: #00ade5
# Hub: No
# Park &amp; Ride: No

# Example Output (.txt):
# Al Murooj (المروج)
# King Fahad District (حي الملك فهد)



# Future Plans : 
# - Add Command-Line Argument Parsing
# - Expand Functionality to get more than tag at a time

#--___---___---___---___---___---___---___---___---___---___---___---___---___---___---___---___---

import xml.etree.ElementTree as ET      # To interact with XML as an ElementTree
import os

# Variables to configure before running the script :
# Enclose values in double quotes ("")
# Be careful though,  Don't repeat the quotes, "PATH" not "'PATH'"
# On macOS and some Linux distributions, copying and pasting file paths may enclose them in single quotes (''). Remove these extra quotes

kml_file_path =  "Users/User/Documents/file.kml"                   
# Replace With the path of the original .kml file, read permission needed

tag_name = "name"
# Replace with the specific tag to extract (e.g., "Placemark/kml:coordinates" for coordinates)
# Supports nested tags with the format: "Parent/kml:Child/kml:ChildChild"

output_path = "Users/User/Documents/file.txt"     
# Ensure this is a writable path; the file will be created or overwritten                   
# The output TXT file doesn't have to exist, you have to provide a valid PATH while {file} could be any name you want the output file to be (this will overwrite any existing file with the same name)
# Check Save Output as Text Section

# Open and read kml file and read text file as string
# try for error handling
try :
    with open(kml_file_path) as file:
        kml_data = file.read()
except FileNotFoundError:
    print(f"Error: The file {kml_file_path} was not found.")
    exit(1)
except Exception as e:
    print(f"Error reading the file: {e}")
    exit(1)

# Convert the string (text) to an ElementTree using the standards of .kml
# try for error handling
try :
    root = ET.fromstring(kml_data)
except ET.ParseError as e:
    print(f"Error parsing the XML file: {e}")
    exit(1)

# Ensures compatibility with namespaced elements in the XML file
# Splits the namespace URI from the tag name and removes curly braces
namespace = {'kml': root.tag.split('}')[0].strip('{')}


# Uses the kml namespace to correctly query prefixed elements
# .// allows searching at any depth in the XML hierarchy
placemark_names = root.findall(f'.//kml:{tag_name}', namespace)
ExtractedText = []
number_of_no_namespaces_found = 0       # Counter for missing data (tag not found)
# Useful to make sure no data entry of the original text was missed

# Append extracted names to a list {ExtractedText}
if placemark_names:
    for name in placemark_names:
        ExtractedText.append(name.text)
else:                                    # If there's no name
    number_of_no_namespaces_found += 1    # Add to missing data counter

ExtractedText = "\n".join(ExtractedText)  # Make all the items in the list one String variable with an \n (new line) separating each


# Save Output as text, w stands for overwrite
# For options, check https://docs.python.org/3/library/functions.html#open 
# or check the latest https://docs.python.org 's functions section
with open(output_path, "w", encoding="utf-8") as outputfile:
    outputfile.write(ExtractedText)


if not os.path.isdir(os.path.dirname(output_path)):
    print(f"Error: Directory {os.path.dirname(output_path)} does not exist.")
    exit(1)


print(f"Successfully saved all '{tag_name}' tags to '{output_path}'.")
if number_of_no_namespaces_found > 0:
    print(f"Warning: {number_of_no_namespaces_found} tags were missing or empty.")
