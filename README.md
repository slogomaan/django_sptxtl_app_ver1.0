In this project, we input an audio file which is converted to a text file by using ‘SpeechRecognition’ python library, which involves splitting the audio file into smaller portions, also called ‘chunks’, making it easier to transcribe them. These transcribed chunks are then concatenated to generate a whole transcribed paragraph.

This generated paragraph at the moment is unreadable as it has no punctuation, so we use another python library called ‘deepmultilingualpunctuation’ which uses a method called ‘PunctuationModel()’ that is used to add punctuation to the generated paragraph.

On the web page we give users the option to choose the language which they want this transcribed text to be translated to, and according to their choice, the transcribed text is translated to the desired language. The language options (Indian) include; Hindi, Bengali, Telugu, Marathi, Tamil, Urdu, Gujarati, Kannada, Malayalam, Odia, Punjabi, Assamase, Maithili, Santali.

After the translation, the user has the option to send the output as an email to multiple recipients, with the help of emailing function which is already included in Django. This Django project is made on Microsoft’s source code editor ‘Visual Studio Code’

Use cases for this system:

1. This system could be used in the company for sending emails across multiple departments without the need of writing an email, we just have to input an audio file from the web page and the email will be sent automatically to the employees. This reduces the time to send an email and it makes it more convenient for easier communication.
2. Another use case could be for the field employees, who cannot have access to the hardware all the time, to write important information via an email, so with the help of this system they just have to record an audio file, upload it to the web and it will be automatically transcribed and emailed to the Head of  Department. This way the field employees will not have to leave or be side tracked while working, just for sending emails.
