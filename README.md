# Team Planner Tool 🧑‍💻📋

A lightweight task and project management backend system built using **Django REST Framework**, **local file-based persistence (JSON)**, and a clean RESTful architecture.

This application allows users to:
- Create & manage teams
- Manage boards under teams
- Create & assign tasks to team members
- Authenticate using token-based login

---

## 📁 Project Structure

```bash
TeamPlannerProject/
│
├── base_interface/             # Base classes for Users, Teams, Boards, Tasks
├── projectplannertool/         # Main Django project
├── db/                         # JSON files for data persistence (created on the fly and utilises lock to avoid any race-around condition)
│   ├── user.json
│   ├── team.json
│   ├── board.json
│   ├── task.json
│   └── auth.json
├── out/                        # used in export board api
├── manage.py
└── requirements.txt            # Contains all the dependency
└── factwise.postman_collection.json            # All the endpoint sample requests

```
---

## ⚙️ Design Considerations

- 📁 **Flat JSON files** used for data persistence (`user.json`, `team.json`, etc.)
- 🔐 Utilising Locks to avoid any race around conditions
- ♻️ Custom **indexing utilities** handle ID generation and uniqueness constraints
- 🔐 Single-token system per user (old tokens are replaced)
- 🧩 Modular service layer based on base_interface inheritance
- 🔍 Minimal external dependencies; no DB setup needed
- 🛠️ Implemented strict access control to prevent unauthorized users from accessing data beyond their scope, ensuring that only administrators have unrestricted visibility where applicable.

---

## 🚀 Getting Started

### ✅ Prerequisites

- Python 3.8 or later
- Django
- Django REST Framework
- Filelock

Install dependencies:
```bash
cd TeamPlannerProject/
pip install -r requirements.txt
```

Run the server:
```bash
python manage.py runserver
```

---

## 🛠️ Features Overview

| Module | Capabilities |
|--------|--------------|
| **User** | Admin/Manager/User creation, Login, Describe/Update/Delete |
| **Teams** | Create teams, Add/remove users, List users per team |
| **Boards** | Create boards under teams, List/update/delete boards |
| **Tasks** | Create tasks under boards, Assign users, List/update/delete tasks |
| **Auth** | Token-based authentication via `auth.json` |

---

## 🔒 Authentication

- Users authenticate via a **login API**.
- A **token** is generated and stored in `auth.json`.
- All protected endpoints require this token to be sent in headers.

Example:
```http
Authorization: Token <your_token>
```

---

## 🔄 Relationships

- **Users ↔ Teams**: Many-to-Many  
- **Teams → Boards**: One-to-Many  
- **Boards → Tasks**: One-to-Many  
- **Tasks ↔ Users**: Many-to-Many (optional, Future Scope)

---

## 📌 API Endpoints (Summary)

### 👤 Users

| Endpoint | Method | Description |
|---------|--------|-------------|
| `/api/v1/users/create/` | `POST` | Create a new user |
| `/api/v1/auth/login/` | `POST` | User login and token generation |
| `/api/v1/users/describe/?id=<user_id>` | `GET` | Get user details |
| `/api/v1/users/update/` | `PUT` | Update user info |
| `/api/v1/users/delete/?id=<user_id>` | `DELETE` | Delete a user |
| `/api/v1/users/teams/?id=<user_id>` | `GET` | Get all teams of a user |

---

### 👥 Teams

| Endpoint | Method | Description |
|---------|--------|-------------|
| `/api/v1/teams/create/` | `POST` | Create a new team (admin only once for 'admin' team) |
| `/api/v1/teams/add-users/` | `PUT` | Add users to a team |
| `/api/v1/teams/update/` | `PUT` | Update team info |
| `/api/v1/teams/remove-users/` | `POST` | Remove users from a team |
| `/api/v1/teams/describe/?id=<team_id>` | `GET` | Get team details |
| `/api/v1/teams/list/` | `GET` | List all teams |
| `/api/v1/teams/list-users/?id=<team_id>` | `GET` | List users in a team |

---

### 📋 Boards

| Endpoint | Method | Description |
|---------|--------|-------------|
| `/api/v1/boards/create/` | `POST` | Create a board under a team |
| `/api/v1/boards/list/?id=<team_id>` | `GET` | List boards under a team |
| `/api/v1/boards/close/` | `POST` | Close a board |
| `/api/v1/boards/export/` | `POST` | Exports boards info in a presentable txt file |

---

### ✅ Tasks

| Endpoint | Method | Description |
|---------|--------|-------------|
| `/api/v1/boards/tasks/create/` | `POST` | Create a task under a board |
| `/api/v1/boards/tasks/update-status/` | `PUT` | Update task status |

---

## 🧪 Testing via tools like Postman
> The complete postman collection with all the relevant endpoint can be found inside TeamPlannerProject

Sample curl for creating new admin user

```bash
curl --location 'http://localhost:8000/api/v1/users/create/' \
--header 'Content-Type: application/json' \
--data '{
  "name": "admin_user",
  "display_name": "Admin",
  "password": "supersecure",
  "is_admin": true
}'
```
---

## 🌟 Future Enhancements

- Token expiry and refresh tokens
- Admin dashboards and metrics
- Full test suite using `pytest` or `unittest`
- Integrate more fetch api, like listing task, listing boards based on status, listing board based on users, listing task based on users.
- Implementing swagger
- Role-based access controls

---

## 🧑‍💻 Author

**Shadab Shaikh**  
Senior Software Engineer | Python & Django Expert | Led cross-functional builds for Fintech, Sales, Fashion, EdTech, E-commerce & Scholarly Publishing. <br>
• [LinkedIn](https://www.linkedin.com/in/shadabsk)

---

## 🙏 Acknowledgements

- DRF Docs: https://www.django-rest-framework.org/
- Problem Statement & Test: FactWise
- Thanks to the open-source community for providing invaluable documentation and tools
- Assistance from LLMs (gpt-4o) for architectural guidance, design suggestions, and code validation

---
