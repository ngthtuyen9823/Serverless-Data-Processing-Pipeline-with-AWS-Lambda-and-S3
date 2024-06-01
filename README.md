**Serverless Data Processing Pipeline with AWS Lambda and S3**
**Create a serverless pipeline that triggers an AWS Lambda function for processing data (e.g., image resizing, text file sanitization) upon upload to an S3 bucket.**
**Integrate AI text analysis to process and analyze text files, extracting named entities and sentiment.**
**Use CloudWatch to monitor Lambda executions and optimize performance based on metrics.**

### Tổng quan về luồng thực hiện

1. upload file lên s3 (source bucket)
2. kích hoạt lambda function
    1. sử dụng textract để trích xuất văn bản 
    2. sử dụng comprehend để phân tích AI
    3. nếu file ở định dạng image thì thực hiện resize ảnh

---
#### Link video demo: https://youtu.be/Ld2rPlfVYqU?si=p95FS5SqjxcU4Bpn
### Các bước thực hiện

- **Tạo 2 Amazon S3 Buckets: cloudproject, cloudproject-resized**
    
    
- **Upload một  file để hỗ trợ cho việc kiểm thử giả lập hàm lambda sau này**
- **Vào trang: https://us-east-1.console.aws.amazon.com/iamv2/home#/policies để tạo permissions policy**
    
    (This policy gives your function the permissions it needs to access other AWS resources. For this tutorial, the policy gives Lambda read and write permissions for Amazon S3 buckets and allows it to write to Amazon CloudWatch Logs logs) có tên là **LambdaS3Policy**
    
    change the name of bucket
    
    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": [
            "logs:PutLogEvents",
            "logs:CreateLogGroup",
            "logs:CreateLogStream"
          ],
          "Resource": "arn:aws:logs:*:*:*"
        },
        {
          "Effect": "Allow",
          "Action": ["s3:GetObject"],
          "Resource": "arn:aws:s3:::is1cloudproject/*"
        },
        {
          "Effect": "Allow",
          "Action": ["s3:PutObject"],
          "Resource": "arn:aws:s3:::is1cloudproject-resized/*"
        }
      ]
    }
    ```
    
    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": [
            "logs:PutLogEvents",
            "logs:CreateLogGroup",
            "logs:CreateLogStream"
          ],
          "Resource": "arn:aws:logs:*:*:*"
        },
        {
          "Effect": "Allow",
          "Action": ["s3:GetObject"],
          "Resource": "arn:aws:s3:::is1cloudproject/*"
        },
        {
          "Effect": "Allow",
          "Action": ["s3:PutObject"],
          "Resource": "arn:aws:s3:::is1cloudproject-resized/*"
        }
      ]
    }
    ```
    
- **Tạo role cho Lambda function (**S3TextractComprehendCloudWatchLambda**): https://us-east-1.console.aws.amazon.com/iamv2/home?region=us-east-1#/roles**
    - Thay vì dùng AmazonS3FullAccess ta sử dụng **LambdaS3Policy**
    - AWSLambdaExecute
    - AmazonTextractFullAccess
    - ComprehendFullAccess
    - CloudWatchLambdaInsightsExecutionRolePolicy (Turn on to collect system-level metrics including CPU time, memory, disk, and network usage)
- **Tạo AWS Lambda function (cloudproject1)**
    
    Python 3.9
    
    **Use an existing role**
    
- **Install các thư viện cần thiết và tạo cấu trúc của folder lambda_handler**
    
    boto3
    
- **Thêm layer để có thể sử dụng thư viện Pillow**
    
    arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p39-pillow:1 
    
    để có thể sử dụng thư viện Pillow. Để có thể Giảm Kích Thước Deployment Package (thời gian và chi phí triển khai sẽ được giảm)
    
- **Tiến hành cấu hình lambda function để có thể xử lí các file lớn mà không bị timeout**
- **Viết code thực thi lambda function**
    - Code xử lý file từ Textract
    - Code xử lý file từ Comprehend
    - Code xử lý resize ảnh
    - Code xử lý lỗi (tạo một Json File với error messages)
    - Viết hàm lambda_handler
- **Upload file zip lambda function lên S3**
- **Upload file zip từ S3 lên lambda function**
- **Test lambda function với event giả lập**
    
    ```json
    {
      "Records": [
        {
          "eventVersion": "2.0",
          "eventSource": "aws:s3",
          "awsRegion": "us-east-1",
          "eventTime": "1970-01-01T00:00:00.000Z",
          "eventName": "ObjectCreated:Put",
          "userIdentity": {
            "principalId": "EXAMPLE"
          },
          "requestParameters": {
            "sourceIPAddress": "127.0.0.1"
          },
          "responseElements": {
            "x-amz-request-id": "EXAMPLE123456789",
            "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH"
          },
          "s3": {
            "s3SchemaVersion": "1.0",
            "configurationId": "testConfigRule",
            "bucket": {
              "name": "is1cloudproject",
              "ownerIdentity": {
                "principalId": "EXAMPLE"
              },
              "arn": "arn:aws:s3:::is1cloudproject"
            },
            "object": {
              "key": "test.jpg",
              "size": 1024,
              "eTag": "0123456789abcdef0123456789abcdef",
              "sequencer": "0A1B2C3D4E5F678901"
            }
          }
        }
      ]
    }
    ```
    
- **Tạo trigger cho Lambda function**
    
    
- **Test lambda function với trigger thực là upload file lên S3**
    
    
- **Giám sát các metrics va hiệu suất quan trọng**
    - Invocations: Theo dõi số lần hàm Lambda được gọi. Điều này giúp hiểu khối lượng công việc tổng thể trên chức năng của mình.
    - Durations: Theo dõi thời gian cần thiết để hàm Lambda thực thi. Số liệu này rất quan trọng để xác định các tắc nghẽn về hiệu suất.
    - Errors: Theo dõi số lỗi gặp phải trong quá trình thực thi hàm Lambda. Tỷ lệ lỗi cao có thể cho thấy có vấn đề với chức năng hoặc phần phụ thuộc của bạn.
    - Maxmemory Used: Giám sát lượng bộ nhớ tối đa mà hàm Lambda sử dụng trong quá trình thực thi. Điều chỉnh bộ nhớ được phân bổ nếu cần để tối ưu hóa hiệu suất.
- **Thu thập và theo dõi các log, dựa trên info và errors thu thập từ log để hoàn thiện, cải tiến project**
- **Kết nối CloudWatch: vào Configuration của Lambda function để enable CloudWatch Lambda Insights. Sử dụng CloudWatch Logs Insights để truy vấn và phân tích dữ liệu nhật ký nâng cao.**
- **Dựa trên dữ liệu từ CloudWatch, tối ưu hóa cấu hình và tài nguyên của Lambda để cải thiện hiệu suất.**
