# OC Project 12: Epicevents CRM

This project is carried out as part of the OpenClassrooms training program.
Epicevents is a role-based command-line CRM application used to manage clients, contracts and events.

Some actions require the authenticated user to have a specific role.

---

## Table of Contents

- [Tech Stack](#tech-stack)
- [Features](#features)
- [Installation](#installation)
- [Available Commands](#available-commands)
- [Logs & Monitoring](#logs--monitoring)
- [Testing](#testing)
- [Notes](#notes)
- [Author](#author)

---

## Tech Stack

- Python 3.10+
- SQLite
- SQLAlchemy
- JWT Authentication
- Click
- Rich
- Sentry


## Features
- User registration and authentication (JWT)
- User, client, contract and event management
- Role-based permissions (management/sales/support)
- All authenticated users can list clients, contracts and events
- Management team can:
    - Create/list/update/delete users
    - Create/update contracts
    - Filter events not assigned to a support contact
    - Assign a support contact to an event
- Sales team can:
    - Create clients
    - Update clients they are responsible for
    - Update contracts for the clients they are responsible for
    - Filter unsigned or unpaid contracts
    - Create an event for one of their clients who has signed a contract
- Support team can:
    - Filter events assigned to them
    - Update events assigned to them


## Installation

1. Clone the repository:
```
git clone https://github.com/anselmlys/OC_P12_CRM.git
cd OC_P12_CRM
```

2. Create/Activate virtual environment:
```
python -m venv env

# On Windows:
.\env\Scripts\activate

# On macOS / Linux:
source env/bin/activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Create ".env" file at project root with:   
```
DATABASE_URL=sqlite:///database/crm.db   
JWT_SECRET_KEY=*your_secret_key*     
SENTRY_DSN=*your_sentry_dsn* or ''     
APP_ENV=development
```

5. Initialize database:
```
python epicevents.py db init
```

6. Create first management user:
```
python epicevents.py db create-admin --email "your@email.com" --last-name "your name" --first-name "your name"
```


## Available Commands

The CLI is organised by modules:
- auth
- users
- clients
- contracts
- events

Command syntax:
```
python epicevents.py [module] [action] [options]
```

To get more information add '--help' to your command:
```
python epicevents.py --help
python epicevents.py [module] --help
python epicevents.py [module] [action] --help
```

### Auth
#### Login
After the command, user will be prompted for their password.
```
python epicevents.py auth login --email "your@email.com"
```
#### Logout
```
python epicevents.py auth logout
```
#### Change password
User will be asked to enter their old password and new password after the command.
```
python epicevents.py auth change-password
```

### Users
#### Create new user
All options are mandatory here. Role can be "management"/"sales"/"support".
```
python epicevents.py users create --email "user@email.com" --last-name "Doe" --first-name "John" --role "sales"
```
#### List all users
```
python epicevents.py users list
```
#### Update a user by id
Only the ID option is mandatory here: it expects the ID of the user you wish to update. If you do not want to update a field, just do not enter the field option name.
```
python epicevents.py users update --id 1 --email "user@email.com" --last-name "Doe" --first-name "John" --role "sales"
```
#### Delete a user by id
The ID option expects the ID of the user you wish to delete.
```
python epicevents.py users delete --id 1
```

### Clients
#### Create new client
Only the options "last name", "first name" and "email" are mandatory here.
```
python epicevents.py clients create --last-name "Doe" --first-name "John" --email "client@email.com" --phone-number "0202020202" --company-name "Random company"
```
#### List all clients
```
python epicevents.py clients list
```
#### Client detail by id
The ID option expects the ID of the client you wish to see the details.
```
python epicevents.py clients detail --id 1
```
#### Update a client by id
Only the options ID is mandatory here: it expects the ID of the client you wish to update. If you do not want to update a field, just do not enter the field option name.
```
python epicevents.py clients update --id 1 --last-name "doe" --first-name "John" --email "client@email.com" --phone-number "0202020202" --company-name "Random company"
```

### Contracts
#### Create new contract
Only the option "client id" is mandatory here. The "signed" option expects "yes" or "no" answer.
```
python epicevents.py contracts create --client-id 1 --total-amount 1000 --remaining-amount 500 --signed "no"
```
#### List all contracts
```
python epicevents.py contracts list
```
#### List unsigned contracts
```
python epicevents.py contracts list --unsigned
```
#### List unpaid contracts
```
python epicevents.py contracts list --unpaid
```
#### Contract detail by id
Only the option ID is mandatory here: it expects the ID of the contract you wish to see the details of.
```
python epicevents.py contracts detail --id 1
```
#### Update contract by id
Only the option ID is mandatory here: it expects the ID of the contract you wish to update. 
```
python epicevents.py contracts update --id 1 --client-id 1 --total-amount 2000 --remaining-amount 1000 --signed "yes"
```

### Events
#### Create new event
Only the option "contract id" is mandatory here. "Start date" and "End date" options expect the format DD/MM/YYYY.
```
python epicevents.py events create --contract-id 1 --start-date "02/02/2026" --end-date "03/02/2026" --support-contact-id 2 --location "berlin" --number-of-attendees 50 --notes "Enter text here."
```
#### List all events
```
python epicevents.py events list
```
#### List all events to assign
```
python epicevents.py events list --to-assign
```
#### List all events assigned to the authenticated user
```
python epicevents.py events list --assigned
```
#### Event details by id
The option ID is mandatory here: it expects the ID of the event you wish to see the details of. 
```
python epicevents.py events detail --id 1
```
#### Update an event by id
Only the option ID is mandatory here: it expects the ID of the event you wish to update. "Start date" and "End date" options expect the format DD/MM/YYYY.
```
python epicevents.py events update --id 1 --start-date "02/02/2026" --end-date "03/02/2026" --location "berlin" --number-of-attendees 50 --notes "Enter text here."
```
#### Assign an event to a support contact
The ID option expects the ID of the event you wish to update.
```
python epicevents.py events assign --id 1 --support-id 2
```


## Logs & Monitoring
This project uses Sentry to centralize important actions and unexpected errors.

Logged information:
- Unhandled errors
- User creation
- User updates
- Newly signed contracts


## Testing
### Testing dependencies
- pytest
- coverage
### Pytest
```
pytest
pytest -v       # verbose mode: shows each test name and result
pytest -q       # quiet mode: displays minimal output`
```
### Coverage
To measure how much of the code is covered by tests:
```
pytest --cov=.
```
To generate an HTML report:
```
pytest --cov=. --cov-report html
```

## Notes

This app is designed for educational purposes only.


## Author

Anselmlys
