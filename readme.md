PetTrackr/
├── frontend/
│ ├── gui.py # Main UI window and navigation
│ ├── views/ # Individual views: Profile, Logs, etc.
│ │ ├── profile_tab.py
│ │ ├── logs_tab.py
│ │ └── feeding_tab.py
│ ├── components/ # Reusable widgets (buttons, dialogs)
│ └── assets/ # Images, icons, themes
│
├── backend/
│ ├── models/ # Pet, LogEntry, etc.
│ │ ├── pet.py
│ │ └── log.py
│ ├── controllers/ # Business logic, PetManager, validators
│ │ ├── pet_controller.py
│ │ └── health_checker.py
│ ├── services/ # File I/O, notifier, client/server stuff
│ │ ├── file_service.py
│ │ ├── notifier.py
│ │ └── network_service.py
│ └── data/ # Local JSON files or sqlite DB
│
├── tests/ # (Optional) Testing modules
├── main.py # Entry point that wires front and back
└── README.md
