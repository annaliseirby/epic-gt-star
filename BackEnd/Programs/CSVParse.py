import sys, csv, getopt, os

# Script that parses APD data and generates MVC Array
# Running this script will parse all of the files currently in the RawCSV folder

inFile = sys.argv
locations = {}
outfile = '../Database/latLong.js'

def main(argv):
	for file in argv:
		inf = open('../RawCSV/' + file,'r')
		next(inf)
		line_words = (line.split(',') for line in inf)
		for words in line_words:
			if words[7].strip() + ', ' + words[8].strip() in locations:
				locations[words[7].strip() + ', ' + words[8].strip()] += 1
			else:
				locations.update({words[7].strip() + ', ' + words[8]: 1})
			
	outf = open(outfile,'w')
	outf.writelines("var heatMapData = [ \n")
	for k, v in sorted(locations.items()):
		if (v == 1):
			outf.writelines('\t new google.maps.LatLng(' + k + '), \n')
		else:
			outf.writelines('\t {location: new google.maps.LatLng(' + k + '), weight: ' +  str(v) + '}, \n')
	outf.writelines(']; \n')

if __name__ == "__main__":
	files = []
	for f in os.listdir('../RawCSV'):
		files.append(f)
	main(files)