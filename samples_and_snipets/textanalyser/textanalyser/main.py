from modules.TextExtractorModule import File

def main():
	import sys, os
	filename=os.path.join('paper', 'La Porte - 1996 - High reliability organizations Unlikely, demandin.pdf')
	file = File(filename)
	text = file.extract_text()
	print(text)


if __name__ == "__main__":
	main()
