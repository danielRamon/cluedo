## Cluedo

### Detective Game with Streamlit and Ollama: Solve the Crime

**Description:**

Dive into an exciting world of mystery and crime-solving! This interactive game puts you in the shoes of a clever detective who must unravel a case. Interrogate suspects and witnesses, analyze clues, and use all your intelligence to discover the culprit.

**Technologies:**

* **Streamlit:** Streamlit's intuitive and user-friendly interface allows for a smooth and engaging gameplay experience.
* **Ollama:** The large language model service Ollama, using the "Gemma2" model, generates cases and provides intelligent and realistic responses to the player's questions, creating an immersive interrogation experience.

**Requirements:**

* **Ollama:** The Ollama large language model service must be installed and running on its default port `11434`, and the `Gemma2` model should be downloaded.

**How to Play:**
1. Clone the repository:
```bash
git clone https://github.com/danielRamon/cluedo.git
```
2. Install the dependencies:
```bash
cd cluedo
pip install -r requirements.txt
```
3. Start the game:
```bash
streamlit run streamlit_app.py
```

4. Play

![Intro](./resources/intro_readme.gif)
![Game](./resources/game_readme.gif)

**Contributions:**

Contributions are welcome! You can help improve the game in the following ways:

* **AI Enhancement:** Explore ways to improve Ollama's ability to generate more natural and convincing responses, as well as using other LLM services.
* **New Features:** Implement new features such as a scoring system, multiple difficulty levels, or the ability to save and load games.
* **Create a Cloud Service:** You can deploy the game on a server so that others without technical knowledge can use it.

**Project Structure:**

* `streamlit_app.py`: The main file containing the game logic and the Streamlit user interface.
* `generate_players.py`: Auxiliary code for creating stories and characters at the start of the game.
* `resources`: Folder containing images for the end of the game.
* `requirements.txt`: File listing the project's dependencies.

**Notes:**

This project is intended for self-learning purposes, so any constructive feedback is welcome.

**Have fun solving crimes!**

**Daniel Ramón Gallardo**

**[LinkedIn](https://www.linkedin.com/in/daniel-ramon-gallardo/)**
