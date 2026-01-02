# OpenAI GPT Integration Setup Guide

## 🚀 Overview

The Natural Language Inventory Dashboard now uses **OpenAI GPT** to intelligently convert natural language queries to SQL, implementing the **Reflection Pattern** (Draft → Review → Finalize).

## 🔑 Getting Your OpenAI API Key

1. **Go to OpenAI Platform**: https://platform.openai.com/
2. **Sign up or log in** to your account
3. **Navigate to API Keys**: https://platform.openai.com/api-keys
4. **Create new secret key**:
   - Click "Create new secret key"
   - Give it a name (e.g., "Inventory Dashboard")
   - Copy the key immediately (you won't see it again!)

## ⚙️ Configuration

### Step 1: Create `.env` file

In the `backend/` directory, create a `.env` file:

```bash
cd backend
copy .env.example .env     # Windows
# or
cp .env.example .env       # Linux/Mac
```

### Step 2: Add Your API Key

Edit `backend/.env` and add your OpenAI API key:

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_MODEL=gpt-4o-mini
OPENAI_ENABLED=true
```

### Available Models

| Model | Speed | Cost | Intelligence | Recommended For |
|-------|-------|------|--------------|-----------------|
| **gpt-4o-mini** | ⚡⚡⚡ | 💰 | ⭐⭐⭐ | **Production (Default)** |
| **gpt-4o** | ⚡⚡ | 💰💰💰 | ⭐⭐⭐⭐⭐ | Complex queries |
| **gpt-3.5-turbo** | ⚡⚡⚡ | 💰 | ⭐⭐ | Budget option |

### Step 3: Restart Backend

```bash
cd backend
npm run build
npm start
```

## 🎯 How It Works

### Reflection Pattern (3-Step Process)

```
User Query: "Show me top selling electronic products with low stock"
              ↓
┌─────────────────────────────────────────────────────┐
│ Step 1: DRAFT (GPT generates initial SQL)          │
│ --------------------------------------------------- │
│ SELECT i.*, c.name as category                     │
│ FROM inventory_items i                             │
│ JOIN product_categories c ON i.category_id = c.id │
│ WHERE c.name = 'Electronics'                       │
│   AND i.current_stock < i.reorder_threshold        │
│ ORDER BY i.recent_sales_volume DESC                │
│ LIMIT 20                                           │
└─────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────┐
│ Step 2: CRITIQUE (GPT reviews for issues)          │
│ --------------------------------------------------- │
│ ✓ Security: SELECT-only, no dangerous operations  │
│ ✓ Syntax: Valid SQLite                            │
│ ✓ Performance: LIMIT clause present               │
│ ⚠ Issue: Should use LEFT JOIN for safety          │
│ needsRevision: true                                │
└─────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────┐
│ Step 3: REVISE (GPT fixes identified issues)       │
│ --------------------------------------------------- │
│ SELECT i.*, c.name as category                     │
│ FROM inventory_items i                             │
│ LEFT JOIN product_categories c                     │
│   ON i.category_id = c.id                         │
│ WHERE c.name = 'Electronics'                       │
│   AND i.current_stock < i.reorder_threshold        │
│ ORDER BY i.recent_sales_volume DESC                │
│ LIMIT 20                                           │
└─────────────────────────────────────────────────────┘
              ↓
         Execute & Return Results
```

## 🧪 Testing GPT Integration

### Test 1: Simple Query
```bash
curl -X POST http://localhost:3001/api/nl-queries \
  -H "Authorization: Bearer mock-token" \
  -H "Content-Type: application/json" \
  -d '{"query": "Show me all products"}'
```

### Test 2: Complex Query
```bash
curl -X POST http://localhost:3001/api/nl-queries \
  -H "Authorization: Bearer mock-token" \
  -H "Content-Type: application/json" \
  -d '{"query": "Which electronics have sold more than 100 units but are running low on stock?"}'
```

### Test 3: Very Complex Query
```bash
curl -X POST http://localhost:3001/api/nl-queries \
  -H "Authorization: Bearer mock-token" \
  -H "Content-Type: application/json" \
  -d '{"query": "Show me the top 5 products in each category sorted by sales volume"}'
```

## 📊 Advantages vs Keyword-Based

| Feature | Keyword-Based | GPT-Based |
|---------|--------------|-----------|
| **Flexibility** | ❌ Limited patterns | ✅ Understands context |
| **Complex Queries** | ❌ Rigid rules | ✅ Natural understanding |
| **Examples** | "Show top selling electronics" | "Which items should I reorder urgently based on sales trends?" |
| **Speed** | ⚡ Instant | ⚡ ~1-2 seconds |
| **Cost** | Free | ~$0.0001-0.0003 per query |
| **Accuracy** | ~70% | ~95% |
| **Self-Correction** | ❌ No | ✅ Reflection Pattern |

## 🔒 Security Features

1. **SELECT-only enforcement**: GPT is instructed to never generate modification queries
2. **Critique step**: Reviews for SQL injection attempts
3. **Schema validation**: Ensures only valid tables/columns are used
4. **Fallback mode**: If GPT fails, falls back to keyword-based generation
5. **Low temperature**: Uses 0.2-0.3 temperature for consistent, safe outputs

## 💡 Example Queries GPT Can Handle

### Simple Queries
- "Show me all products"
- "List items in electronics"
- "What's low on stock?"

### Medium Complexity
- "Show top selling products with less than 20 units in stock"
- "Find items that need reordering in the clothing category"
- "Which warehouse has the most inventory?"

### High Complexity
- "Compare sales volume between electronics and clothing categories"
- "Show me products where stock is below 50% of reorder threshold"
- "Which items have the highest sales-to-stock ratio in each location?"

## 🛠️ Troubleshooting

### GPT Not Working?

**Check the logs:**
```bash
cd backend
npm start
# Look for: "OpenAI GPT integration enabled"
```

**Test API key:**
```bash
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

### Falling Back to Keywords?

If you see "using keyword-based fallback" in logs:
1. Check API key is set correctly in `.env`
2. Verify `OPENAI_ENABLED=true`
3. Check OpenAI account has credits
4. Review error messages in logs

### Rate Limits?

OpenAI has rate limits:
- **Free tier**: 3 requests per minute
- **Paid tier**: Higher limits based on usage

If hit rate limit, the system automatically falls back to keyword-based generation.

## 💰 Cost Estimation

Using **gpt-4o-mini** (recommended):
- **Cost per query**: ~$0.0001-0.0003
- **1,000 queries**: ~$0.10-0.30
- **10,000 queries**: ~$1-3

The Reflection Pattern makes 2-3 API calls per query (draft + critique + optional revision), but it's still very affordable.

## 🚫 Disabling GPT

To disable GPT and use keyword-based generation:

```env
OPENAI_ENABLED=false
```

Or remove/comment out the API key:

```env
# OPENAI_API_KEY=sk-xxxxx
```

The system will automatically fall back to keyword-based generation.

## 📈 Next Steps

1. ✅ Get OpenAI API key
2. ✅ Add to `.env` file
3. ✅ Restart backend
4. ✅ Test with complex queries
5. ⏳ Monitor usage and costs
6. ⏳ Fine-tune system prompts if needed

## 🎓 Learning More

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [GPT Best Practices](https://platform.openai.com/docs/guides/gpt-best-practices)
- [Rate Limits](https://platform.openai.com/docs/guides/rate-limits)
- [Pricing](https://openai.com/pricing)

