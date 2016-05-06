import os
import zipfile

def run(outputDir, fileName):
	zipf = zipfile.ZipFile(fileName, 'w', zipfile.ZIP_DEFLATED)
	# ziph is zipfile handle
	for root, dirs, files in os.walk(outputDir):
		for file in files:
			zipf.write(os.path.join(root, file))
			os.remove(os.path.join(root, file))
	zipf.close()