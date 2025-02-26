# **Messaging API**

A Django REST Framework (DRF) based API for managing messaging threads and messages with authentication, pagination, and validation.

## **Features**
- User authentication (Token-based authentication)
- CRUD operations for Threads and Messages
- Mark messages as read
- Get unread message count
- Pagination for messages
- URL validation enforcement

---

## **Installation & Setup**

### **1. Clone the Repository**
```bash
https://github.com/nazarbodak221/django_message_thread.git
cd messaging-api
```

### **2. Create a Virtual Environment & Install Dependencies**
```bash
python -m venv venv
source venv/bin/activate   # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

### **3. Go to django app directory and Apply Migrations**
```bash
cd django_project
python manage.py makemigrations
python manage.py migrate
```

### **4. Load Initial Data**
```bash
python manage.py loaddata db.json
```

### **5. Create a Superuser**
```bash
python manage.py createsuperuser
```

### **6. Run Server**
```bash
python manage.py runserver
```

## **API Endpoints**

### **Authentication**
| Method | Endpoint              | Description                        |
|--------|-----------------------|------------------------------------|
| POST | `/api/token/`         | Login and get authentication token |
| POST | `/api/token/refresh/` | Refresh token                      |
| POST | `/api/token/verify/`  | Verify token                       |

### **Threads**
| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/api/feed/threads/` | Get all threads for the authenticated user |
| POST | `/api/feed/threads/` | Create a new thread |
| GET | `/api/feed/threads/{id}/` | Get a thread by ID |
| DELETE | `/api/feed/threads/{id}/` | Delete a thread (only if the user is a participant) |

### **Messages**
| Method | Endpoint | Description                                                                |
|--------|---------|----------------------------------------------------------------------------|
| GET | `/api/feed/messages/?thread={id}` | Retrieve all messages for the authenticated user. Optionally, filter messages by a specific thread using the `thread` query parameter. |
| POST | `/api/feed/messages/` | Send a message (must specify `thread` and `content`)                       |
| POST | `/api/feed/messages/{id}/mark_as_read/` | Mark a message as read                                                     |
| GET | `/api/feed/messages/unread_messages/` | Get count of unread messages for the authenticated user                    |


## **Contributing**
### **Feel free to fork the repo, create a branch, and submit a pull request. 🚀**

