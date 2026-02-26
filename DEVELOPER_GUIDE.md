# Quick Start Guide for Developers

## First-Time Setup (5 minutes)

### 1. Clone and Setup
```bash
git clone <repo-url>
cd performx
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
cp .env.example .env
```

### 2. Run Application
```bash
python run.py
```
Visit: `http://localhost:5000`

## Project Structure Quick Guide

**Working on Authentication?** → Edit `app/routes/auth.py` and `app/services/user_service.py`

**Working on Tasks?** → Edit `app/routes/tasks.py` and `app/services/task_service.py`

**Working on Goals?** → Edit `app/routes/goals.py` and `app/services/goal_service.py`

**Working on Database?** → Edit files in `app/models/`

**Working on UI?** → Edit files in `app/templates/`

## Key Files to Know

| File | Purpose |
|------|---------|
| `run.py` | Application entry point |
| `config.py` | Configuration management |
| `app/__init__.py` | Flask app factory |
| `app/models/` | Database models |
| `app/routes/` | URL routes (blueprints) |
| `app/services/` | Business logic |
| `app/utils/` | Helpers & validators |

## Common Tasks

### Add a New Route
1. Create function in appropriate `app/routes/` file
2. Add `@blueprint.route()` decorator
3. Import blueprint in `app/routes/__init__.py` (if needed)
4. Update templates with correct `url_for()` calls

Example:
```python
# In app/routes/tasks.py
@tasks_bp.route('/status/<int:task_id>')
@login_required
def get_status(task_id):
    task = TaskService.get_task(task_id)
    return f"Task: {task.title}"
```

### Add Database Validation
```python
# In app/utils/validators.py
def validate_task_priority(priority):
    valid = ['Low', 'Medium', 'High']
    return priority in valid
```

### Add Business Logic
```python
# In app/services/task_service.py
@staticmethod
def get_overdue_tasks(user_id):
    from datetime import datetime
    return Task.query.filter(
        Task.user_id == user_id,
        Task.completed == False,
        Task.due_date < datetime.now()
    ).all()
```

## Code Style

Follow **PEP 8**:
```python
# ✅ Good
user = User.query.filter_by(email=email).first()

# ❌ Bad
u=User.query.filter_by(e=email).first()
```

## Testing Changes

```bash
# Install test dependencies (optional)
pip install pytest pytest-flask

# Run tests
pytest
```

## Debugging

Add breakpoint:
```python
breakpoint()  # Will pause execution
```

Or use Flask debugger (automatically enabled in development):
- Visit the error page in browser
- Click debugger icon to open interactive shell

## Environment Variables

Required in `.env`:
```
FLASK_ENV=development
SECRET_KEY=dev-key-change-for-production
```

## Database Reset

**Delete database file to start fresh:**
```bash
rm instance/database.db
# App will recreate on next run
```

## Common Issues

**`ImportError: cannot import name...`**
- Check blueprint is registered in `app/__init__.py`
- Verify model is imported correctly

**`404 on form submit`**
- Check `url_for()` function in template
- Verify route name matches blueprint

**`AttributeError: 'NoneType' object...`**
- Check if object exists before using (use `or 404`)
- Verify object ID is correct

## Git Workflow

```bash
# Create feature branch
git checkout -b feature/task-priority

# Make changes, test, then commit
git add .
git commit -m "feat: Add task priority filter"

# Push and create pull request
git push origin feature/task-priority
```

## Tips for Team Development

✅ **Do:**
- Write descriptive commit messages
- Test your changes before committing
- Keep functions small and focused
- Document complex logic

❌ **Don't:**
- Commit without testing
- Use hardcoded values
- Modify config.py directly (use .env)
- Leave debug print statements

## Need Help?

1. Check `README.md` for overview
2. Check `MIGRATION_GUIDE.md` for routing changes
3. Look at similar existing code for patterns
4. Check logs: `python run.py`

---

**Happy coding! 🚀**
