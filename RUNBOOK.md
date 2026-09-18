Document what to do when:

Gemini returns 429
Gemini returns 404
Tavily fails
Chroma fails
SQLite becomes locked
LangSmith tracing fails
User gets blocked
Moderator request is stuck
Backend crashes
Frontend cannot connect
===================================================
For example:

Gemini 429
    ↓
Check quota
    ↓
Do not repeatedly retry
    ↓
Wait for quota reset / configure billing
    ↓
Verify model configuration

================================================