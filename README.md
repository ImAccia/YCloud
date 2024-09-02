# YCloud
YCloud is a service that allows you to convert your files into videos, which can then be stored on youtube for free, allowing you to have an infinite cloud storage.
The service provides functionality for both **encoding and decoding data**. 

## Features

-   **Data to Video Conversion**:
    -   Converts a data file into a video with each pixel or block representing data.
    -   Zips files from a source directory before encoding them into video frames.


-   **Video to Data Extraction**:    
    -   Extracts data from a video by decoding pixel values.
    -   Saves extracted data into a zip file.

-   **YouTube Video Downloading**: 
    - Download videos directly from YouTube, given the video ID.

-   **YouTube Video Uploading**: 
	- Upload videos directly to your YouTube channel. (this option requires setting up the credentials.json file, which has to be downloaded from the Google Cloud Console of your project)
-   **Configuration Editing**: 
	- Modify configuration settings directly from the program.


## Requirements

-   Python 3.x
-   OpenCV (`cv2`)
-   NumPy
-   `curses` (usually included with Python standard library on Unix-based systems)

## Installation

1.  **Clone the Repository**:
    `git clone https://github.com/ImAccia/YCloud.git` 
    
2.  **Install Python Dependencies**:     
    `pip install opencv-python-headless numpy`
    *If you are running this on windows you also have to install windows-curses*

## Configurable Variables

The `config.py` file contains several parameters that you can adjust to fit your needs. 
-   **`block_size`**:
    -   **Type**: Integer
    -   **Description**: Size of each block in pixels for encoding and decoding. Both width and height should be divisible by this value.
    -   **Example**: `16`

-   **`width`**:    
    -   **Type**: Integer
    -   **Description**: Width of the video frames in pixels.
    -   **Example**: `640`

-   **`height`**:    
    -   **Type**: Integer
    -   **Description**: Height of the video frames in pixels.
    -   **Example**: `480`

-   **`fps`**:    
    -   **Type**: Integer
    -   **Description**: Frames per second for the output video.
    -   **Example**: `30`

-   **`rgb`**:    
    -   **Type**: Integer (0/1)
    -   **Description**: Set to `1` if the video should use RGB color mode, otherwise `0` for B&W.
    -   **Example**: `0`

-   **`src`**:    
    -   **Type**: String
    -   **Description**: Path to the source folder containing files to be converted into video.
    -   **Example**: `'source_folder'`

-   **`out`**:    
    -   **Type**: String
    -   **Description**: Path to the output zip file where the files from the source folder will be stored.
    -   **Example**: `'output.zip'`

-   **`video_out`**:    
    -   **Type**: String
    -   **Description**: Path to the output video file where data will be encoded into video frames.
    -   **Example**: `'output_video.mp4'`

-   **`video_in`**:    
    -   **Type**: String
    -   **Description**: Path to the input video file from which data will be extracted.
    -   **Example**: `'input_video.mp4'`

-   **`zip_out`**:    
    -   **Type**: String
    -   **Description**: Path to the output zip file where extracted data will be saved.
    -   **Example**: `'extracted_data.zip'`

## Usage

1.  **Run the Main Script**:
    `python main.py` 
    
2.  **Menu Options**:
    -   **Data -> Video**: Converts data files into a video. (Requires correct configuration)
    -   **Video -> Data**: Extracts data from a video and saves it into a zip file. (Requires a video file and correct configuration)
    -   **Download YT Video**: Prompts for a YouTube video ID and downloads the video.
    -   **Upload YT Video**: Prompts for a video title and uploads the video  to the channel specified in the configuration file.
    -   **Edit Config**: Opens a configuration editor to modify the settings in `config.py`.

## Notes on RGB Functionality

The RGB functionality is currently under development. The program is designed to support both RGB and grayscale video modes, but the RGB mode may not be fully operational at this time. Future updates will aim to complete and test this feature. For now, using RGB mode may lead to incomplete or incorrect results.

## Obtaining the `credentials.json` File for YouTube

To use the YouTube video upload functionality, you need to set up access to the YouTube Data API and obtain the `credentials.json` file. Follow these steps to get your `credentials.json` file:

### Steps to Obtain the `credentials.json` File

1.  **Access Google Cloud Console**:
    -   Go to the Google Cloud Console.
    -   If you don't have a Google Cloud account yet, you will be prompted to create one and set up a project.

2.  **Create a New Project**:    
    -   Select or create a project. You can do this by clicking the dropdown menu in the top left corner and then clicking "New Project".
    -   Give your project a name and click "Create".

3.  **Enable YouTube Data API**:    
    -   In the Google Cloud Console search bar, search for "YouTube Data API v3".
    -   Select "YouTube Data API v3" and click "Enable" to enable the API for your project.

4.  **Configure OAuth Consent Screen**:    
    -   Go to "APIs & Services" > "OAuth consent screen".
    -   Choose the user type (Internal or External) and fill in the required information, such as the product name and support email.
    -   Save your changes.

5.  **Create Credentials**:    
    -   Go to "APIs & Services" > "Credentials".
    -   Click "Create Credentials" and select "OAuth Client ID".
    -   Choose "Desktop app" as the application type and enter a name for your client ID.
    -   Click "Create". You will be provided with a client ID and client secret.

6.  **Download the `credentials.json` File**:    
    -   After creating the credentials, click the download icon next to your OAuth Client ID to download the `credentials.json` file.
    -   Save this file in your project directory or a location accessible by your script.

7.  **Configure Authentication**:    
    -   Ensure that the `credentials.json` file is accessible by your script and that your code properly handles the OAuth2 authentication process for uploading videos to YouTube.

### Additional Notes

-   **Protect Your `credentials.json` File**: This file contains sensitive information. Do not share it publicly and avoid including it in version control (e.g., in a Git repository).
-   **Expiration and Updates**: OAuth credentials may expire or change. If you encounter authentication issues, check your settings in the Google Cloud Console and update the `credentials.json` file as needed.

### Useful Resources

-   [Google Cloud Documentation - Creating Credentials](https://developers.google.com/workspace/guides/create-credentials)
-   [YouTube Data API Documentation](https://developers.google.com/youtube/v3)

## Troubleshooting

-   **Invalid Block Size Error**:
    -   Ensure that both width and height in your `config.py` are divisible by the block size.

-   **No Files Found**:    
    -   Verify that the source folder contains files before running the `dataToVideo` method.

-   **File Paths and Names**:    
    -   Double-check the paths and filenames specified in `config.py`.

-   **YouTube Handling**:    
    -   Ensure that you have appropriate credentials and access for YouTube operations.
