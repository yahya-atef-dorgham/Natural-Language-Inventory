# SQLite Migration Complete

## Overview

The Natural Language Inventory Dashboard has been successfully migrated from PostgreSQL to SQLite using `sql.js`. This change simplifies local development and eliminates native dependency issues on Windows.

## What Changed

### Database System
- **Before**: PostgreSQL with `pg` driver
- **After**: SQLite with `sql.js` (pure JavaScript implementation)

### Benefits
1. **No Native Dependencies**: `sql.js` is pure JavaScript, eliminating `node-gyp` build issues
2. **Simpler Setup**: No separate database server required
3. **File-Based**: Database stored in a single `inventory.db` file
4. **Cross-Platform**: Works consistently across Windows, macOS, and Linux
5. **Automatic Initialization**: Schema and sample data created automatically on first run

## Files Updated

### Backend Code
- `backend/src/services/db/connection.ts` - Complete rewrite for SQLite
- `backend/src/services/inventoryQueryExecutor.ts` - SQL syntax conversion
- `backend/src/config/index.ts` - Updated config for SQLite
- `backend/package.json` - Replaced `pg` with `sql.js`

### Deployment
- `docker-compose.yml` - Removed PostgreSQL service, added volume for SQLite
- `backend/Dockerfile` - No changes needed (works with new dependencies)
- `backend/init.sql` - Deleted (schema now in code)

### Documentation
- `README.md` - Updated setup instructions
- `DEPLOYMENT.md` - Updated deployment and troubleshooting sections

## Database File Location

### Local Development
- **Path**: `backend/inventory.db`
- **Auto-created**: Yes, on first run
- **Sample Data**: Automatically inserted

### Docker Deployment
- **Path**: `/app/data/inventory.db` (inside container)
- **Volume**: `backend_data` (persistent storage)
- **Backup**: Use `docker cp` to backup/restore

## Testing Results

✅ **Backend Build**: Successful
✅ **Database Connection**: Successful
✅ **Schema Initialization**: Successful
✅ **Sample Data**: Inserted correctly
✅ **API Endpoint**: Working (tested with mock auth)
✅ **Query Execution**: Returning correct results

### Test Query
```bash
# Request
POST /api/nl-queries
Authorization: Bearer mock-token
Body: { "query": "Show me all products in electronics" }

# Response
{
  "sessionId": "ce0eecde-383a-49ee-a2eb-2f177ce9239b",
  "status": "executed",
  "message": "Query accepted and executing"
}

# Results retrieved successfully with 10 inventory items
```

## Running the Application

### Local Development

```bash
# Backend
cd backend
npm install
npm run build
npm start

# Frontend (in separate terminal)
cd frontend
npm install
npm run dev
```

The backend will automatically create `inventory.db` with sample data on first run.

### Docker Deployment

```powershell
# Windows
.\deploy.ps1

# Or manually
docker-compose up -d
```

## Configuration

### Environment Variables (Optional)

Create `backend/.env`:
```env
PORT=3001
NODE_ENV=development
DB_PATH=inventory.db
CORS_ORIGIN=http://localhost:3000
LOG_LEVEL=info
```

### Docker Environment

In `docker-compose.yml`:
```yaml
backend:
  environment:
    DB_PATH: /app/data/inventory.db
  volumes:
    - backend_data:/app/data
```

## Backup & Restore

### Local
```bash
# Backup
cp backend/inventory.db backup.db

# Restore
cp backup.db backend/inventory.db
```

### Docker
```bash
# Backup
docker cp nl-inventory-backend:/app/data/inventory.db ./backup.db

# Restore
docker cp ./backup.db nl-inventory-backend:/app/data/inventory.db
docker-compose restart backend
```

## Troubleshooting

### Database Not Created
- Check write permissions in `backend/` directory
- Check logs for WASM loading errors
- Verify `sql.js` is installed: `npm list sql.js`

### Query Errors
- SQLite syntax differs slightly from PostgreSQL
- Check `backend/src/services/db/connection.ts` for SQL conversion logic
- Review logs for specific SQL errors

### Performance
- SQLite is optimized for single-user/low-concurrency scenarios
- For production with high concurrency, consider PostgreSQL or other RDBMS
- Current setup is ideal for development and small deployments

## Next Steps

The application is now ready for:
1. ✅ Local development
2. ✅ Docker deployment
3. ⏳ User Story 2 - Self-review and safety checks
4. ⏳ User Story 3 - Results exploration (sorting, filtering)
5. ⏳ Polish - Documentation, performance, security, edge case tests

## Notes

- The `.gitignore` file excludes `inventory.db` to prevent committing database files
- Sample data includes 10 inventory items across 3 categories and 3 locations
- Authentication uses mock token `mock-token` for development
- Frontend needs to be updated to use correct API field names (`query` not `naturalLanguageQuery`)

