import sys
import csv

inFile, outFile = sys.argv[1], sys.argv[2]
locations = {}

with open(inFile) as inf:
	next(inf)
	line_words = (line.split(',') for line in inf)
	for words in line_words:
		if words[7].strip() + ' ' + words[8].strip() not in locations:
			locations.update({words[7].strip() + ', ' + words[8]: 1})
		else:
			locations[words[7].strip() + ', ' + words[8]] += 1

with open(outFile,'a') as outf:
	outf.writelines("var heatMapData = [ \n")
	for k, v in locations.items():
		outf.writelines('\t {location: new google.maps.LatLng(' + k + '), weight: ' +  str(v) + '}, \n')
	outf.writelines('];')