🎮 Familiada (Python + Flet)


A simple Family Feud–style game built with Python and Flet.
The project focuses on game logic, UI state management, and event-driven programming.

✨ Features

- Two teams with custom names
- Random questions loaded from questions.json
- Multiple rounds (default: 3)
- Correct / wrong answer handling
- Mistake system with visual “X” indicators
- Sound effects (intro, correct, wrong)
- Final screen with winner or draw
- Dark mode UI

🛠 Tech Stack

- Python 3
- Flet (GUI)
- playsound3
- JSON
- asyncio / threading

📁 Project Structure
.
├── main.py
├── questions.json
├── intro.mp3
├── correct.mp3
├── wrong.mp3
└── README.md

▶️ Run the App

Install dependencies:
pip install flet playsound3


Run:
python main.py

📄 questions.json Format
{
  "Question?": {
    "answer 1": 30,
    "answer 2": 25,
    "answer 3": 20,
    "answer 4": 15,
    "answer 5": 10
  }
}

🚀 Status

- Working prototype, open for improvements:
- animations
- score display
- AI-assisted answer matching

👩‍💻 Author

Created as a learning project for:
- game logic
- UI state handling
- event-based GUI programming
  
Feel free to fork or extend 🙂
