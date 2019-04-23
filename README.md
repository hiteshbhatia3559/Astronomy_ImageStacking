**What is this program**
It takes low ISO .fit files and stacks them to output a clearer image.

How to use
```
0. Install Python 3.5 or higher, ensure that Python dir is added to PATH environment variable
1. Install astropy library by doing 'pip install astropy' in the command prompt
1.1 Install pytest by doing 'pip install pytest' in the command prompt
1.2 Install image_registration by doing 'pip install image_registration'
2. Download the program from here, and unzip anywhere (say at ./Project/)
2.5 IMPORTANT : Ensure that you edit the directory that has the files (or leave it default and it will use the current dataset, 
alternatively simply delete old .fit files and copy new ones in to './Project./Iota Cancri - Binary System-20190405T043457Z-001'
3. At ./Project/, open command prompt and type 'python main.py'. Note
4. If there were no errors, the program will print out the QF of each file. Please note that some Warnings may occur but those are not relevant.
5. It will then merge the top 20% by QF of these files, and output the merged file at 'stacked.fit'
6. Done!
```

Links
``` 
https://drive.google.com/drive/u/1/folders/1YBeRzOybVH_ngwzdh_1ZIOHcPXfbkxiV
^ Link to images
```
