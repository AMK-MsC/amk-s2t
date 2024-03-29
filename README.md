# AMK Speech-to-Text
 
This mono-repo consist of the code we have developed during our master thesis, a full-stack application developed to streamline the process of transcribing Norwegian emergency calls. The front-end is developed using React, TypeScript and Chakra UI. The back-end is developed using Hugging Face's Transformer library, and Python's Flask.   

## Front-end

The front-end consist of a simple page where the user is able to upload a single audio clip to get the audio automatically transcribed. The transcription is displayed in an editable window, with the option to download the transcription as either a DOC file or as a SRT file. The SRT format makes it possible to listen to the audio together with the transcription as subtitles. 

## Back-end

The back-end is designed to receive a POST request from the front-end, with the audio clip in the request body. The back-end automatically transcribes the audio using our fine-tuned model, and returns the transcription.

## Notebooks

This folder contains the Jupyter notebooks for training and evaluating the model.


| Notebooks    |
|:----------|
|  [Finetuning.ipynb](https://github.com/AMK-MsC/amk-s2t/blob/master/notebooks/Finetuning.ipynb)  |
|  [Evaluation.ipynb](https://github.com/AMK-MsC/amk-s2t/blob/master/notebooks/Evaluation.ipynb)  |
---

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Frontend](#frontend)
  - [Backend](#backend)
- [Contact](#contact)

## Getting Started

Follow these instructions to set up the monorepo project on your local machine for development and testing purposes.

### Prerequisites

Before you start, make sure you have the following software installed on your system:

- Node.js (v12.0.0 or later)
- Yarn (v1.22.0 or later)
- Python (v3.8 or later)
- pip (Python package manager)
- virtualenv (Python virtual environment)

To check if you have Node.js, Yarn, Python, and pip installed, run the following commands:

```sh
node --version
yarn --version
python --version
pip --version
```

### Installation

1. Clone the repo:

```sh
git clone https://github.com/your-username/monorepo-project-name.git
```

2. Change into the amk-s2t:

```sh
cd amk-s2t
```

#### Frontend

3. Change into the frontend directory:

```sh
cd frontend
```

4. Install the required frontend dependencies using Yarn:

```sh
yarn
```
 
#### Backend

5. Change back to the root of the amk-s2t and then into the backend directory:

```sh
cd ../backend
```

6. Set up a virtual environment:

```sh
python -m venv venv
```

7. Activate the virtual environment:

- On Linux and macOS:

```sh
source venv/bin/activate
```

- On Windows:

```sh
venv\Scripts\activate
```

8. Install the required backend dependencies using pip:

```sh
pip install -r requirements.txt
```

## Usage

### Frontend

To start the frontend development server, run the following commands:

```sh
cd ../frontend
yarn start
```

This will open your default web browser and load the application at `http://localhost:3000`. As you make changes to the source code, the app will automatically reload, reflecting the updates.

### Backend

To start the backend development server, run the following commands:

```sh
cd ../backend
flask run
```

This will start the backend server at `http://localhost:5000`. As you make changes to the source code, the server will automatically reload, reflecting the updates.

## Contact

Øyvind Grutle - oyvindgru@gmail.com

Jens A. Thuestad - jens.andreas@live.no

Project Link: https://github.com/oyvindgrutle/amk-s2t
