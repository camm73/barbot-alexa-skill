#!/bin/bash

rm skill.zip
echo "Packing files..."
zip -r9 skill.zip *.py

aws lambda update-function-code --function-name barbot-alexa --zip-file fileb://skill.zip

echo "Successfully uploaded to lambda"
exit 0