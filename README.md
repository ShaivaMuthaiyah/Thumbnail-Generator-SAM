<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
      </ul>
    </li>
    <li><a href="#project-folders">Project Folders</a></li>
    <ul>
        <li><a href="#main-project-directory">Main Project Directory</a></li>
      <li><a href="#lambda">Lambda</a></li>
      <li><a href="#front-end">Front-End</a></li>
      </ul>
 
  </ol>
</details>




<!-- ABOUT THE PROJECT -->
## About The Project

A serverless thumbnail generation application built on AWS using the Serverless Application Model (SAM). This solution seamlessly integrates Amazon S3, AWS Lambda, DynamoDB, and API Gateway. When a .jpg/.png image is uploaded to the S3 bucket, it triggers a Lambda function that creates a thumbnail of the image and stores it back in the same bucket. Metadata for each thumbnail is then saved to a DynamoDB table, which can be accessed through API requests.

![Alt text](thumbnail.png)


### Built With

* Python 3.9
* AWS Lambda, DynamoDB, S3 and SAM
* YAML

### Prerequisites

Two key things required for this project are :

* AWS CLI (set it up easily with this guide at https://docs.aws.amazon.com/polly/latest/dg/setup-aws-cli.html

<!-- GETTING STARTED -->
### Getting Started

After setting up the AWS CLI you can use this command inside whichever directory you want to start the project

* Initialise a SAM Project
  ```sh
  sam init
  ```

Set it up with the language you want to work with and choose the 'Hello World' example project as a base. You can follow this guide here at  https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-getting-started-hello-world.html


## Project Folders

The main project directory has the SAM configuration files to build the project. Inside the thumbnail_maker directory you can find the code for the lambda functions which are automatically referenced while building the project.



### Main Project Directory

You can create your template in this folder as well as where the configuration file with automaticallly appear. The quotes.json folder is also provided here, this has to be put into the s3 bucket once the intial architecture is launched. Lauch the AWS CLI and from the project directory you can use these commands after the intial setup using the same deploy --guided command from the guide.

* Build the project
  ```sh
  sam build
  ```
 * Deploy the architecture
  ```sh
  sam deploy
  ```
  
  ### Lambda

Over here i have added the python file containing all the lambda functions required to run the application.
