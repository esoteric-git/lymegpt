# LymeGPT

LymeGPT is a Retrieval-Augmented Generation (RAG) application that uses AWS Bedrock and Streamlit to provide information about Lyme disease treatment. The app uses a Streamlit frontend to interact with users, triggering an AWS Lambda function that communicates with a knowledge base in AWS Bedrock. The LLM used for the chat is Claude-3-Sonnet.

This project can be used to create any RAG app with AWS Bedrock. You can follow the instructions below to quickly get a RAG app up and running with your own knowledge base.

## Live Demo

A running version of the application is available at [lymegpt.streamlit.app](https://lymegpt.streamlit.app). 

**Note:** To prevent casual or accidental use and control AWS costs, the app requires authentication. Use the following credentials:

- Username: lyme
- Password: lyme

## Features

- LLM chatbot UI for asking complex questions about Lyme disease and treatments that are obscured or not found in the foundation model's training data
- Uses AWS Bedrock for LLM inference and RAG functionality
- Knowledge base is stored in S3 and is easily updated with new info
- RAG will provide citation source text of the chunked sources for the LLM's response

## Architecture

The application consists of four main components:

1. **AWS Bedrock Knowledge Base**: Stores and retrieves relevant information about Lyme disease
2. **AWS Bedrock LLM Inference**: Uses Claude3-Sonnet for LLM inference
3. **AWS Lambda**: Processes user queries and communicates with AWS Bedrock
4. **Streamlit Frontend**: Handles user interaction and display of results

## Setup and Deployment

### Prerequisites

- Python 3.7+
- AWS account with access to Lambda and Bedrock services
- Streamlit account (for cloud deployment)

### 1. Setting up the Knowledge Base on AWS Bedrock

First, setup an S3 bucket for the project:

1. Make 2 folders, name them Dataset and Lambdalayer
2. Put your knowledge base documents into Dataset folder
3. Put the Lambda zip file called `knowledgebase_lambdalayer.zip` in the Lambdalayer folder. Cloudfoundation will look here later when it creates the lambda function.

To set up the knowledge base on AWS Bedrock:

1. Navigate to the AWS Bedrock console.
2. In the left navigation pane, choose **Knowledge bases**[1].
3. Choose **Create knowledge base**[2].
4. Configure your knowledge base:
   - Choose a name and optional description
   - Select the data source as the S3 bucket dataset folder you created earlier
   - Choose the embeddings model Titan Text Embeddingsv2 (you may have to request access)
   - Create the system and user prompts. These are important because it tells the LLM to use the knowledge base as context for its chat response.
5. Review and create the knowledge base.
6. Click sync, this chunks the data and vectorizes into AWS OpenSearch Vector Store
7. Once synced, the knowledge base will be available for use. Test it with an available model.

For more detailed instructions, refer to the AWS Bedrock documentation on creating a knowledge base.

### 2. Setting up the Lambda Function

To set up the Lambda function use AWS CloudFormation to deploy it:

1. In the AWS Console, create a new stack, in specify template select Upload a Template File

2. Upload `DeployKnowledgeBase.yaml` as the template.

3. Enter your parameters KnowledgeBaseID and LambdaLayerS3BucketName.

3. The CloudFormation template will create the following resources:
   - IAM role for the Lambda function
   - Lambda function with the necessary permissions
   - Lambda layer containing required dependencies


The `DeployKnowledgeBase.yaml` file includes:
- Lambda function configuration
- IAM role with permissions for Bedrock, S3, and CloudWatch Logs
- Lambda layer for dependencies

This setup simplifies the deployment process, eliminating the need to manually configure these resources through the AWS console.

### 3. Local Streamlit Development

1. Clone the repository if you have not already:
   ```
   git clone https://github.com/esoteric-git/lymegpt.git
   cd lymegpt
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create or use an AWS user with the following permissions. Note that you must enter the ARN of your new Lambda and S3 bucket:
    ```
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "lambda:InvokeFunction"
                ],
                "Resource": [
                    "arn:aws:lambda:your-region:your-account-id:function:InvokeKnowledgeBase"
                ]
            },
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject"
                ],
                "Resource": [
                    "arn:aws:s3:::your-bucket-name/*"
                ]
            }
        ]
    }
    ```

3. Set up environment variables:
   Create a `.env` file in the root directory with the following content:
   ```
   AWS_ACCESS_KEY_ID=your_access_key
   AWS_SECRET_ACCESS_KEY=your_secret_key
   AWS_DEFAULT_REGION=your_aws_region
   ```

4. Your App.py uses Boto3 to authenticate the AWS session with the access keys stored in `.env`.  Make sure you have a `.gitignore` file that excludes `.env` to prevent leaking the keys to github in the next step.

5. Run the Streamlit app locally:
   ```
   streamlit run app.py
   ```

6. Change the hardcoded username and password in the app.py to your desired credentials:
    ```
    if username == "lyme" and password == "lyme":  # Hardcoded credentials
    ```

### 4. Streamlit Cloud Deployment

1. Push your code to a GitHub repository.

2. Log in to [Streamlit Cloud](https://streamlit.io/cloud).

3. Create a new app and connect it to your GitHub repository.

4. In the app settings, add the following secrets:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_DEFAULT_REGION`

   Make sure to copy these values from your local `.env` file and use the TOML config format.

5. Deploy the app.

## Usage

1. Open the app in a web browser.
2. Log in using the provided credentials.
3. Type your question about Lyme disease treatment in the chat input.
4. View the LLM response generated using RAG (Retrieval-Augmented Generation) and explore the cited chunks of the sources.

## Disclaimer

This application is for informational purposes only and should not be considered medical advice. Always consult with a qualified healthcare professional for medical diagnosis and treatment.
