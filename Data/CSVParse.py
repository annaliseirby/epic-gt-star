import sys, csv, getopt

inFile = sys.argv
locations = {}

def main(argv):
	for file in argv:
		inf = open(file,'r')
		next(inf)
		line_words = (line.split(',') for line in inf)
		for words in line_words:
			if words[7].strip() + ', ' + words[8].strip() in locations:
				locations[words[7].strip() + ', ' + words[8].strip()] += 1
			else:
				locations.update({words[7].strip() + ', ' + words[8]: 1})
			
	outf = open('latLong.txt','w')
	outf.writelines("var heatMapData = [ \n")
	for k, v in sorted(locations.items()):
		outf.writelines('\t {location: new google.maps.LatLng(' + k + '), weight: ' +  str(v) + '}, \n')
	outf.writelines(']; \n')

if __name__ == "__main__":
	main(sys.argv[1:])