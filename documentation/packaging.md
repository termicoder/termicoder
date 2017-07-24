# How to generate a new release
This file is created to serve as a guide to me for updating this package on PyPI

## 1. Update readme.rst
Do care to update features and changelogs also see if the html is rendered properly using utilities such as http://rst.ninjs.org/

## 2. Update setup.py
Updating version is important else PyPI won't accept the release  
also update tags etc in setup.py  

## 3. Update MANIFEST.in
This is the file that tells what all files are to be included in the package 

## 4. Generating source distribution(sdist)
Currently termicoder is only availible as source distribution as there are issues in packaging data using wheels 
To generate source distribution run `python setup.py sdist`  
this will create a folder named dist which contains an archive (format may vary on platform is tar.gz on linux can use --formats flag also) of the distribution.  
Check the contents of the archive properly if not satisfied go back to step 2  

## 5. Upload
check dist folder, remove older versions run  
`twine upload dist/*`
