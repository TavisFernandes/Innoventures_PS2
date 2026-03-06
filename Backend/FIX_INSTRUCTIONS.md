# Backend API Fix - Domain Detection & Citations

## Issues Found:
1. The `/chat` endpoint was not using the SME Plugin's domain detection
2. Citations were not being extracted from responses
3. Domain was hardcoded to "finance" instead of auto-detecting

## Fix Required in Backend/api_server.py:

The `/chat` endpoint around line 351 needs to be updated to:

1. **Remove** the direct OpenRouter API call code (lines ~386-420)
2. **Keep** the SME Plugin processing code (lines 366-384) which already detects domain and extracts citations
3. **Add** the proper return statement using `result.domain.value` and `result.citations`

##Current Status:
- Domain detection logic is already added (✅)
- Citation extraction from the SME Plugin is in place (✅)  
- Need to remove redundant httpx.AsyncClient code that bypasses the SME Plugin

## What's Happening:
The endpoint currently has TWO code paths:
1. SME Plugin processing (correct - detects domain & extracts citations)
2. Direct API call (incorrect - hardcoded to finance, no citations)

The direct API call code needs to be removed so only the SME Plugin path is used.

## Manual Fix Instructions:
In `Backend/api_server.py`, around line 386, remove everything between:
```python
print(f"📚 Citations: {result.citations}")
```
and
```python
except Exception as e:
```

Then add this single return statement:
```python
        return ChatResponse(
            answer=result.answer,
            confidence=result.confidence,
            sources=result.sources,
            methodology=result.methodology,
            domain=result.domain.value,
            citations=result.citations,
            reasoning_steps=result.reasoning_steps,
            disclaimer=result.disclaimer
        )
```
