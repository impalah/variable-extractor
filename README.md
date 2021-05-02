# variable-extractor
Testing how to extract data from text documents.

This project is just a code showcase that contains two components:

* A PDF to Text converter.
* A field extractor from a text file (uses regex).


## Convert a PDF into plain text

    - Command line program.
    - Simple webservice

### Project folder and files organization

    src - source code, including tests
    deployment - kubernetes deployment files (does not apply)

### Requirements

    apt-get install -y build-essential libpoppler-cpp-dev pkg-config python-dev

### Execution

#### Shell Command

The container needs to read the pdf file and to store the txt file somewhere so we need to mount a volume when launching the command line process.

    docker container run -v /home/impalah/data:/data pdfprocessor:latest python /var/pdfprocessor/pdf2txt.py -i /data/Report1.pdf -o /data/report1.txt

Arguments

    i: input pdf file
    o: output txt file

    h: shows command help

#### Webservice

Docker launch. For this example we will use the Flask development server. In a production environment something like wsgi should be used.

    docker container run -p5000:5000 pdf-converter:latest python /var/pdfprocessor/pdf2txt_server.py

### Test Webservice

Send a POST to http://localhost:5000/pdf with the PDF as the body content

### Run tests in container

    docker container run pdf-converter:latest python -m unittest tests/pdfmanager_test.py



## Analyzes text and return free text and patient Id rehashed

    - Data persisted in database (simulated).
    - Webservice and shell command.

### Project folder and files organization

    src - source code, including tests
    deployment - kubernetes deployment files (does not apply)

### Build

From root directory execute:

    docker build -t TAGNAME -f DockerfileAnalyzer .

### Execution

#### Shell Command

The container needs to read the text file so we need to mount a volume when launching the command line process.

    docker container run -v /home/impalah/data:/data analyzer:latest python /var/analyzer/analyze_mr.py -i /data/Report1.txt

Arguments

    i: input txt file
    o: output json file

    h: shows command help

#### Webservice

Docker launch. For this example we will use the Flask development server. In a production environment something like wsgi should be used.

    docker container run -p5001:5001 analyzer:latest python /var/analyzer/analyze_mr_server.py

### Test Webservice

Send a POST to http://localhost:5001/medical-report with the text file as the body content

Will return json result.

### Run tests in container

    docker container run text-analyzer:latest python -m unittest tests/medical_report_analyzer_test.py


