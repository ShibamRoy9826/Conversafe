<img src="static/logo.png" width=40%>

# Conversafe 💬

Conversafe is language learning platform designed to make mastering languages both fun and engaging! This platform is more fun for pre-intermediate to interemediate users at the moment. This platform provides a learning environment through real conversations with other users. Infact, incase other users are not available, they can have a conversation with AI! It has many other amazing features like fun general knowledge quizzes, vocabulary quizzes, a word helper(Somewhat like a dictionary), and many more! This platform is extremely user-friendly and offers a welcoming space for learners to practice, learn, and have fun:) 

> [!NOTE]
> This demo version doesn't have all the features, as the application is quite resource intensive at the moment...

## ✨ Demo - https://conversafe.pythonanywhere.com/

## Features 😎

-  Conversation with real peole (other learners)
-  Conversation with AI in absense of other users
-  Fun general knowledge quizzes, and Vocabulary quizzes
-  A word helper, something like a dictionary, but with more things like synonyms, phonetics etc.
-  Random Quotes, and Fun facts
-  Friends system, so that users can make new friends
-  Sources to more learning material, not exclusive to English, but many other skills too
-  Catppuccin based dark theme by default
-  Extremely user-friendly UI
-  Fully free and open source

## Language support🗣️

As of now, these are the languages which are supported:

- English
- Hindi
- Bengali
- Spanish
- German

## Usage guide 🛠️

1. This is the landing page of the website, click on the signup button at the top-right to create a new account.( Press on login if you already have an account)

![App Screenshot](/screenshots/image-1.png)

2. Once you get into the signup page, enter the details its asking for inorder to create an account. Next, click on the Submit button to send a verification email to the provided email.

![App Screenshot](/screenshots/image-2.png)
![App Screenshot](/screenshots/image-3.png)

3. Go to your email providers website , and check for an email. Make sure to check the Spam folder incase you don't find the email

![App Screenshot](/screenshots/image-4.png)
![App Screenshot](/screenshots/image-5.png)

 4. Email Verification is now successful

![App Screenshot](/screenshots/image-6.png)

 5. Go to the login page, and login with the same details that you used to create the account 

![App Screenshot](/screenshots/image-7.png)

 6. Done! Now you're logged in and you can explore the rest of the website, its pretty user-friendly.
 If you don't understand the language, Click `Settings icon > Language learning medium > Change to any language you want(Out of the ones that are supported)`

## How is it made?

Its a [Django](https://www.djangoproject.com/) web app, and I used [TailwindCSS](https://tailwindcss.com/), and some vanilla CSS to design the frontend.
The chat system is built using websockets, there are different chat rooms which are created if there are no free active user pairs, if there already exists any active user waiting in an empty chatroom, the user is automatically paired with them. There's also a custom keyboard which is used so that users are easily type even when in a larger screen without having to worry about the system keyboard layout. This keyboard is made using [simple-keyboard](https://github.com/hodgef/simple-keyboard).

Each time the user logs in and gets to the dashboard, there's a random quote and a fact in the language that the user wants to learn. The quotes are fetched from a local database, while the facts are fetched using an api called the [Useless facts API](https://uselessfacts.jsph.pl/). The support for other languages is actually made by translating sentences, which is made possible by [LibreTranslate](https://github.com/LibreTranslate/LibreTranslate)

The AI feature uses [Blenderbot 400M Distill](https://huggingface.co/facebook/blenderbot-400M-distill) , an open-source project developed by Meta, its not too accurate as of now, but accurate enough for basic conversation. I am using it because its pretty lightweight.

There's also a word finder functionailty which uses a local database and the [Datamuse API](https://www.datamuse.com/api/) for phonetics and similar words.


## Installation/Running Locally 🛠️

Running this project locally is very easy.

1. Start by cloning this repository

```bash
  git clone https://github.com/ShibamRoy9826/Conversafe.git
```
2. Get inside the Conversafe directory

```bash
  cd Conversafe
```

3. Install necessary dependencies (Its suggested to make a virtual environment to run the project. Recommended Python Version : 3.10.5 )
 You should also have npm installed.
```bash
  pip install -r requirements.txt
```
4. Install TailwindCss

```bash
npm init -y
npm install -D tailwindcss
npx tailwindcss init
```

5. To Run the server

```bash
python manage.py runserver
```

6. To Run Tailwind CSS
```bash
npm run dev
```

7. To run the language server
```bash
libretranslate --load-only en,es,de,bn,hi
```
This step will require a huge amount of time when run for the first time, as it will download all the translation models for these languages

8. Now you can visit https://127.0.0.1:8000 to view the application :)

## FAQ ❔

### 1. Why Conversafe? There are other language learning apps too!

Yes, there are indeed many other applications which offer language learning for free, but Conversafe is an open-source alternative to that! and along with that it provides more practical interaction between the users so that they can learn better! 

### 2. What's the point of using the AI feature? I can just have a conversation with ChatGPT or Gemini, they are far more accurate!

While they may be far more accurate, they also collect your data. Your responses are used to train the model itself, but incase of Conversafe, it uses [Blenderbot 400M Distill](https://huggingface.co/facebook/blenderbot-400M-distill) which is another open-source project made by Meta. Its a little lightweight, and that's why its being used in this application, but If I find any better open-source alternative I would definitely shift to that. You can suggest any model either by raising an issue in this github repository.

## Contributing 🤝

Everyone is welcome to contribute to the code!
You can also raise an issue, or suggest any features that you think would be great :)

> ✨ Please star this repository if you liked this project 😁
