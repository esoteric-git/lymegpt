# LymeGPT

LymeGPT is a Retrieval-Augmented Generation (RAG) application that leverages AWS Bedrock and Streamlit to provide information about Lyme disease treatment. The app uses a Streamlit frontend to interact with users, triggering an AWS Lambda function that communicates with a knowledge base in AWS Bedrock.

## Live Demo

A running version of the application is available at [lymegpt.streamlit.app](https://lymegpt.streamlit.app). 

**Note:** To prevent casual or accidental use and control AWS costs, the app requires authentication. Use the following credentials:

- Username: lyme
- Password: lyme

## Features

- User-friendly chat interface for asking questions about Lyme disease treatment
- Integration with AWS Bedrock for advanced natural language processing
- Citation of sources for provided information
- Expandable chunks of source text for further reading

## Architecture

The application consists of three main components:

1. **AWS Bedrock Knowledge Base**: Stores and retrieves relevant information about Lyme disease
2. **AWS Lambda**: Processes user queries and communicates with AWS Bedrock
3. **Streamlit Frontend**: Handles user interaction and display of results

## Setup and Deployment

### Prerequisites

- Python 3.7+
- AWS account with access to Lambda and Bedrock services
- Streamlit account (for cloud deployment)

### 1. Setting up the Knowledge Base on AWS Bedrock

To set up the knowledge base on AWS Bedrock:

1. Navigate to the AWS Bedrock console.
2. In the left navigation pane, choose **Knowledge bases**[1].
3. Choose **Create knowledge base**[2].
4. Configure your knowledge base:
   - Choose a name and optional description
   - Select the data source (e.g., Amazon S3)
   - Choose the Bedrock model
   - Configure additional settings as needed
5. Upload your Lyme disease-related documents to the specified S3 bucket.
6. Review and create the knowledge base.
7. Once created, the knowledge base will be processed and made available for use.

For more detailed instructions, refer to the AWS Bedrock documentation on creating a knowledge base[2].

### 2. Setting up the Lambda Function

To set up the Lambda function:

1. Ensure you have the `DeployKnowledgeBase.yaml` and `knowledgebase_lambdalayer.zip` files in your project's root directory.

2. Use AWS CloudFormation to deploy the Lambda function:
   ```
   aws cloudformation create-stack --stack-name LymeGPTLambda --template-body file://DeployKnowledgeBase.yaml --capabilities CAPABILITY_IAM
   ```

3. The CloudFormation template will create the following resources:
   - IAM role for the Lambda function
   - Lambda function with the necessary permissions
   - Lambda layer containing required dependencies

4. After the stack creation is complete, note the Lambda function ARN from the CloudFormation outputs.

The `DeployKnowledgeBase.yaml` file includes:
- Lambda function configuration
- IAM role with permissions for Bedrock, S3, and CloudWatch Logs
- Lambda layer for dependencies

This setup simplifies the deployment process, eliminating the need to manually configure these resources through the AWS console.

### 3. Local Streamlit Development

1. Clone the repository:
   ```
   git clone https://github.com/esoteric-git/lymegpt.git
   cd lymegpt
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory with the following content:
   ```
   AWS_ACCESS_KEY_ID=your_access_key
   AWS_SECRET_ACCESS_KEY=your_secret_key
   AWS_DEFAULT_REGION=your_aws_region
   ```

4. Update the Lambda function ARN in your Streamlit app configuration.

5. Run the Streamlit app locally:
   ```
   streamlit run app.py
   ```

### 4. Streamlit Cloud Deployment

1. Push your code to a GitHub repository.

2. Log in to [Streamlit Cloud](https://streamlit.io/cloud).

3. Create a new app and connect it to your GitHub repository.

4. In the app settings, add the following secrets:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_DEFAULT_REGION`

   Make sure to copy these values from your local `.env` file.

5. Deploy the app.

## Usage

1. Open the app in a web browser.
2. Log in using the provided credentials.
3. Type your question about Lyme disease treatment in the chat input.
4. View the LLM-RAG-generated response and explore cited chunks of the sources.

## Disclaimer

This application is for informational purposes only and should not be considered medical advice. Always consult with a qualified healthcare professional for medical diagnosis and treatment.
