## Health Records on BlockChain
The goal of this project is to store medical reports of a user on a Blockchain to manage authentication, anonymity, security, accountability and effective sharing of data.
Further, the data from the reports is used to predict the user's health.
Also, dependencies on hospitals/doctors for maintainenance and retrieval of records is eliminated.

## Implementation
- A python blockchain in django is built.
- A user can retrieve his/her blockchain of records.
- Users login to the application and can then either add a new block by uploading their medical report either as an image or pdf.
- A new block can also be added via Android application that sends data directly to the application.
- The information in the form of text is extracted by ocrAPI.
- Prediction on the existing reports is done and a summary of the user's health can be viewed by the user.

## Live Demo
https://api.cohabitation95.hasura-app.io/
