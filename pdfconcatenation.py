from configparser import SafeConfigParser
import codecs, datetime, glob, os, re, subprocess

# ---------- CONSTANTS ----------
config_filename = "configuration.ini"
# ----------/CONSTANTS ----------

# ---------- FUNCTIONS ----------
# Load the PDF files of today, sorted backwards
# basepath: The base path from config
# filename_pattern: The regEx to find the PDFs
# RETURN: The PDF files of today, sorted backwards.
def load_file_list(basepath, filename_pattern):
	fileslist = glob.glob(basepath + "\\" + filename_pattern)
	fileslist.sort(reverse = True)
	return fileslist;

# Searches the marker in the given filename
# file_name: The file's name
# file_marker: The marker to look for
# RETURN: True, if the marker is found, False otherwise.
def search_marker(file_name, file_marker):
	if file_marker in file_name:
		return True
	else:
		return False

# Writes Numbers smaller 10 with a leading zero
# number: The number
# RETURN: A string with the result
def pad_number(number):
	result = ""
	if number < 10:
		result = "0"
	result = result + str(number)
	return result

# Generates the output filepath
# fileslist: The list of files that are already there
# RETURN: A file name of the format YYYY-MM-DD-##.pdf with ## being the 
#         smallest number that does not overwrite anything. The file name
#         includes the path.
def generate_filepath(basepath, fileslist, filemarker):
	pattern = '.*' + datetime.datetime.now().strftime("%Y-%m-%d-") + "([0-9][0-9]).*"
	lastNumber = pad_number(int(re.sub(pattern, '\\1', fileslist[0]))+1)
	return basepath + "\\" + datetime.datetime.now().strftime("%Y-%m-%d-") + str(lastNumber) + "-" + filemarker + ".pdf"

# Appends a file name to the PDFSAM command line (at its beginning)
# command: The command before the call
# filename: The file name or path
# RETURN: The command with the file PREpended
def append_filename(command, filename):
	print("Adding file " + filename + "...")
	command = "-f " + filename + " " + command
	return command;
# ----------/FUNCTIONS ----------

# ---------- START RUN ----------
# Read configuration
parser = SafeConfigParser()
try:
	with codecs.open(config_filename, 'r', encoding='utf-8') as f:
		parser.readfp(f)
except FileNotFoundError:
	print("Cannot read " + config_filename + ", did you rename the filled template?")
	input("Press Enter to exit...")
	quit()

try:
	config_basepath = parser.get("pdf_settings", "basepath")
	config_filemarker = parser.get("pdf_settings", "filemarker")
	config_pdfsam_jar = parser.get("program_settings", "pdfsam_jar")
	config_pdfsam_dir = parser.get("program_settings", "pdfsam_dir")
	config_pdfvwr_path = parser.get("program_settings", "pdfvwr_executable")
except:
	print("Could not find all needed options in config file. Try to load a new copy.")
	input("Press Enter to exit...")
	quit()

filenamenumber = None
foundFiles = False

# Build regEx pattern for searching
filenamePattern = datetime.datetime.now().strftime("%Y-%m-%d-*.pdf")

# Load files list
fileslist = load_file_list(config_basepath, filenamePattern)

# Iterate over files and add them to the PDFsam command line
pdfsam_command = ""
foundthemarker = False
for filename in fileslist:
	foundthemarker = (foundthemarker or search_marker(filename, config_filemarker))
	if not foundthemarker:
		foundFiles = True
		pdfsam_command = append_filename(pdfsam_command, filename)

if foundFiles:
	# Finalize PDFsam command
	output_file_path = generate_filepath(config_basepath, fileslist, config_filemarker)
	pdfsam_command = "java -jar " + config_pdfsam_jar + " " + pdfsam_command + "-o " + output_file_path + " concat"
	print("\nCreated the following command line:")
	print("\t" + pdfsam_command)
	# Change dir, execute command
	print("\nRunning PDFsam...")
	os.chdir(config_pdfsam_dir)
	os.system(pdfsam_command)
	# Call PDF Viewer
	subprocess.call([config_pdfvwr_path, output_file_path])
else:
	print("No files to concat have been found.")

input("Press Enter to continue...")