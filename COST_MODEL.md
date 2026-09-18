# Cost Model

## AI Learning Agent

The application tracks:

- Model calls
- Tool calls
- Input tokens
- Output tokens
- Total tokens
- Estimated model cost

## Model Call Limit

Maximum model calls per workflow:

5

## Tool Call Limit

Maximum external tool calls per workflow:

3

## Current Development Configuration

The application currently uses the Gemini API.

The development environment may use a free-tier API quota.

The application does not assume that the free tier has unlimited usage.

## Cost Calculation

Estimated cost:

input token cost + output token cost

The pricing values should be configured according to the
currently selected model and provider pricing.

## Cost Control

The system uses:

1. Model call limits
2. Tool call limits
3. Retry limits
4. Fallback model
5. RAG retrieval
6. Structured responses
7. LangSmith tracing

These controls help prevent unnecessary model usage.

## Production Recommendation

Before production deployment:

- Configure current provider pricing.
- Monitor token usage.
- Set provider spending limits where available.
- Monitor repeated failures.
- Monitor tool-call frequency.
- Review LangSmith traces regularly.