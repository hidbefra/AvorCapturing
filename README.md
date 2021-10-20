# AvorCapturing
Extracts barcode information from PDFs and searches for the associated folder in a directory and copies the PDF there.


DirectoryIndex digs through a folder structure. If the folder name corresponds to a regex pattern, the path to this folder is saved in a dictionary.

AvorCapturing searches a directory for PDFs. The PDFs are either searched for a barcode or a text excerpt which leads to a regex pattern.
If a corresponding text pattern has been found, the PDF is pushed into the corresponding directory which was determined using the "DirectoryIndex"
