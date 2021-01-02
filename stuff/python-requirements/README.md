# Create a folder named 'python'
mkdir python
cd python

# Download the PyJWT library in current folder (inside 'python' folder)
pip3 install PyJWT -t .

# Make a zip of the current folder excluding the .DS_Store files
# zip -vr folder.zip folder/ -x "*.DS_Store"
cd ../
zip -vr requirements.zip python/ -x "*.DS_Store"
