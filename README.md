# Poem Generator from Images 🎨📜

## About the Project

This project is an innovative application that generates poems based on an image uploaded by the user. The application leverages modern Artificial Intelligence and Audio Processing technologies to create an immersive experience, transforming visual features into words and sound.

## Features

- **Poem Generation**: Poems are created by analyzing the person featured in the image.
- **Text-to-Audio Conversion**: The generated poem is transformed into audio using the Google Cloud Text-to-Speech API.
- **Musical Background**: The audio is enhanced with a musical background for a more pleasant presentation.

## Technologies Used

- **Python**: The core programming language of the project.
- **Flask**: Framework used to build the web application.
- **Google AI Studio**: Tool used to generate poems from images.
- **Google Cloud Text-to-Speech**: API to convert poem text into audio.
- **PyDub**: Library used to add a musical background to the audio.

## How to Run the Project

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/your-repository.git
   cd your-repository
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # For Linux/macOS
   venv\Scripts\activate      # For Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**:
   - Create a `.env` file and add your API keys for Google AI Studio and Google Cloud:
     ```
     GOOGLE_AI_KEY=YourAPIKey
     GOOGLE_CLOUD_KEY=YourJSONFile
     ```

5. **Run the application**:
   ```bash
   flask run
   ```

6. **Access it in your browser**:
   - Open [http://localhost:5000](http://localhost:5000).

## Project Structure

```plaintext
.
├── app.py                 # Main Flask application file
├── static/                # Static files (CSS, JS, images)
├── templates/             # HTML templates for the interface
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
```

## Next Steps

- Improve the AI model to generate more creative poems.
- Implement support for multiple languages in poems and audio.
- Add a more interactive graphical user interface.

## Contributions

Feel free to contribute! Follow these steps:

1. **Fork the repository**
2. **Create a branch for your feature**:
   ```bash
   git checkout -b my-feature
   ```
3. **Commit your changes**:
   ```bash
   git commit -m "Add my feature"
   ```
4. **Push to the main branch**:
   ```bash
   git push origin my-feature
   ```
5. **Open a Pull Request**

## License

This project is licensed under the [MIT License](LICENSE).
