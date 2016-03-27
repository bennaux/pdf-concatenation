# pdf-concatenation
Small windows / Python hack to concatenate a range of PDF files at the end of the day.

## The problem and solutions
### The problem
You are doing your daily work and have to print different things you want to archive in folders. Printing all those small jobs at once would save power and (important!) **the times you have to walk to the printer, possibly insert paper and wait for the printer to complete**.

### A first attempt for a solution
You print all those single jobs into a PDF printer and use its collate functionality. At the end of the day, you create a PDF file from all the jobs and print it with your printer.

![Schema drawing of first attempt.](https://raw.githubusercontent.com/bennaux/pdf-concatenation/master/readme-graphics/first-attempt.png)

**Problem with this solution**: Sometimes, the creation of the PDF file with the PDF printer crashes. This results into a complete loss of all the input data.

### A second attempt for a solution
(*This is what I did until I wrote this script.*) You print every single jobs into the same PDF printer, but you do not use its collate function. Thus, you get one PDF per job, put them all into the same directory and name them `YYYY-MM-DD-##.pdf`, for example `2016-03-27-01.pdf`, `2016-03-27-02.pdf` and so on. (*When you use the Num pad, this can get really fast doing that.*) At the end of the day, you use **PDF Split & Merge** (PDFsam) to merge all the files into one PDF, that you can print later on.

![Schema drawing of second attempt.](https://raw.githubusercontent.com/bennaux/pdf-concatenation/master/readme-graphics/second-attempt.png)  

**Problem with this solution**: You can create the single PDFs without much hassle and don't have to fear that any older ones will be destroyed if the PDF printer crashes. But to merge all the files, you have to open PDFsam, open the folder containing the PDFs, drop them into the program, enter an output path and open the resulting file manually. This is just annoying.

### The solution this script offers
#### Simple
It takes all the single PDFs from a directory, merges them using PDFsam and opens the result file. Doing this, it takes care not to add files that it has already processed earlier.

#### More detailed example
1. You print single jobs, resulting in `2016-03-27-01.pdf`, `2016-03-27-02.pdf` and `2016-03-27-03.pdf`.
2. You start the script:  
   It finds `-03.pdf`, `-02.pdf` and `-01.pdf`.  
   It merges `-01.pdf`, `-02.pdf` and `-03.pdf` into `2016-03-27-04-CONCATENATED_BY_BENNAUX_SCRIPT.pdf` and opens it in a PDF viewer. 
3. You print the result, are happy and continue working.
4. You find out that you forgot about two tasks, complete them and print the results into the files `2016-03-27-05.pdf` and `2016-03-27-06.pdf`.
5. You start the script again:  
   It finds `-06.pdf`, `-05.pdf` and `-04-CONCATENATED_BY_BENNAUX_SCRIPT.pdf` and stops there because of the marker `CONCATENATED_BY_BENNAUX_SCRIPT`.  
   It merges `-05.pdf` and `-06.pdf` into `2016-03-27-07-CONCATENATED_BY_BENNAUX_SCRIPT.pdf` and opens it in a PDF viewer.

## Additional Features
* You can configure...
	* the path where the PDFs are taken from and the result is put into
	* the file marker, of course (you do not have to use the `CONCATENATED_BY_BENNAUX_SCRIPT` string)
	* the location and executable of PDFsam
	* the executable of the PDF viewer you want to use.      

## System Prerequisites
* Python 3 
* A PDF printer
* PDF Split & Merge (Basic version is enough)  
  [http://www.pdfsam.org](http://www.pdfsam.org)
* A PDF viewer 

## Setup and Workflow
### Setup
1. Read the code to make sure I do not want to harm you and did not make a mistake (yes, this script is written for those who know what they are doing). 
2. Make sure you meet all the Prerequisites.
3. Clone this script.
4. Rename the `configuration-template.ini` to `configuration.ini`.
5. Edit the `configuration.ini` and specify all the paths, names and the marker. The comments will help you.
6. Make a link to call the script. **Make sure the working dir of the link is the directory where the script lies, so that it can find the configuration file.** You do not need to drop anything onto the link. This step is optional.

### Workflow
1. Work and create the first result, then the second, and so forth, name them after the current date, in the format `YYYY-MM-DD-##.pdf`, with `##` being numbers, counting upwards.  
   If you do not want to have a PDF added to the merge, just name it differently ;-)
2. Start the script. It will merge the files and open the result.

## Notes / Caution
* The script is made for daily use, so it supports only two-digit numbers. Thus, if you have more than 99 files for a day, expect all bad things to happen you can think of. =)
* Although it is commented quite well, this script is a quick-and-dirty solution that has been written in a very short period of time to be used by myself. It has not been tested in-depth to confirm that it wouldn't destroy valuable data. You have been warned.
