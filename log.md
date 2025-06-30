# Work Log – 2025-06-27

## 1. Core Logic Restructuring & Pipeline Implementation
- **Refined analysis workflow**: Successfully restructured the entire program logic to follow the intended flow: detect significant price movements first, then fetch associated news, and finally use LLM to analyze the correlation between anomalies and news events.
- **End-to-end pipeline testing**: Validated the complete workflow from signal detection through news association to final analysis output.
- **Logic optimization**: Streamlined the process to ensure efficient data flow and accurate signal-to-news mapping.

## 2. LLM Integration & Modularization
- **Integrated large language model**: Successfully incorporated LLM capabilities to analyze news headlines and summaries, providing intelligent insights into potential causes of stock price movements.
- **Modular design**: Implemented the LLM analyzer as a separate, configurable module that can process news content and generate contextual explanations for market anomalies.
- **Content analysis**: Enhanced the system's ability to correlate news sentiment and content with detected price signals.

## 3. Local File Integration & Mock Data Testing
- **Mock data implementation**: Successfully switched from live API calls to local JSON file processing, enabling offline development and testing.
- **File-based workflow**: Created `DummySession` and `DummyResponse` classes to simulate API responses using local TSLA data files.
- **Development mode**: Established a seamless way to test the entire pipeline using pre-downloaded data, making development more efficient and independent of API limitations.

## 4. User Interface Enhancements
- **Dynamic stock symbol input**: Added user input functionality allowing analysis of any stock symbol (not just TSLA).
- **Improved sidebar controls**: Enhanced the UI to accept user-specified stock symbols with automatic file name generation.
- **Code organization**: Refactored mock classes into separate modules (`fetcher/mock.py`) for better code structure and maintainability.

## Key Insights & Observations
1. **Complexity increases with depth**: The deeper we dive into the project, the more complex challenges emerge - from handling edge cases in anomaly detection to managing API rate limits.
2. **API limitations are restrictive**: The 25 requests/day limit on Alpha Vantage API is quite constraining for development and testing purposes.
3. **Mock data proves valuable**: Local file testing significantly improves development velocity and reduces dependency on external APIs.

## Current Challenges & Next Steps
1. **Anomaly detection refinement**: Some edge cases in signal detection still need debugging and improvement.
2. **API rate limit management**: Need to implement better strategies to work within the 25 requests/day constraint.
3. **Deep content analysis**: Explore having the LLM analyze full article content rather than just headlines and summaries for more comprehensive insights.
4. **Frontend redesign**: The user interface needs a complete overhaul to better present analysis results and improve user experience.
5. **Multilingual support**: Consider adding Chinese language support for both UI and content analysis.

## Technical Debt
- Error handling for missing data files needs improvement
- Need better validation for user input (stock symbols)
- Consider implementing caching mechanisms for API responses
- Frontend styling and layout require significant enhancement

---

# Work Log – 2025-06-26

## 1. Bug Fixes & UI Improvements
- **Fixed relevance-score display**: Resolved yesterday’s issue where the nested `relevance_score` wasn’t showing correctly.  
- **Re-sorted news by timestamp**: Ensured that all news items now appear in strict chronological order.  
- **Polished the UI**: Tweaked layout and controls (dropdowns, “Confirm” button) so the sidebar and main view render as expected.

## 2. Project Proposal & Design Discussion
- **Revisited high-level architecture**: Collaborated with GPT to explore new approaches and clarified the core flow (“fetch → parse → analyze → render”).  
- **Rewrote the project proposal**: Updated scope, goals and removed outdated milestones, in line with today’s refined vision.

## 3. Codebase Refactoring
- **Introduced OOP design**: Modularized fetchers, parsers, analyzers, and renderers into distinct classes/interfaces.  
- **Dependency injection**: Centralized configuration and made the core `run(...)` function test-friendly.  
- **Separated concerns**: Moved all Streamlit UI code into `ui.py`, with `app.py` focusing solely on orchestration.

## Lessons Learned
1. **Use version control**  
   Without Git or similar, it’s hard to trace or revert past code—this was a major headache today.  
2. **Don’t over-rely on AI for refactoring**  
   While Copilot/GPT can accelerate boilerplate, it sometimes generates buggy or misaligned code. Always understand the underlying logic before applying automated suggestions.

---
# Work Log – 2025-06-25

## 1. Environment Configuration

* Installed and configured Homebrew, pyenv, and Python 3.13.5 within a VS Code virtual environment (`.venv`).
* Verified `python` CLI availability and activated the virtual environment in the integrated terminal.

## 2. API Integration & Data Fetching

* Integrated Alpha Vantage **TIME\_SERIES\_DAILY** endpoint to download historical TSLA price data (JSON → DataFrame).
* Integrated Alpha Vantage **NEWS\_SENTIMENT** endpoint to fetch TSLA‐related news (JSON → DataFrame), defaulting missing `relevance_score` values to 1.0.
* Encapsulated data pipelines in `data_loader.py` with robust error checking and date parsing.

## 3. Analyzer Module

* Developed `detect_significant_moves()` to identify dates where |daily pct\_change| ≥ configurable threshold.
* Developed `associate_news()` to link each signal date with all news items in the preceding N days above a relevance threshold.

## 4. Interactive Front‑end (Streamlit)

* Built `app.py` featuring:

  * Sidebar controls for price threshold, news relevance threshold, “days before” window, and analysis period (7 days, 1 month, 6 months, 1 year, or full history).
  * Plotly chart rendering closing prices and marking signal dates with hover‐enabled red markers.
  * Markdown news cards listing associated headlines under each signal date.

## 5. Testing

* Experimented with pytest for `fetch_news_sentiment`, then opted for end‑to‑end UI testing as more effective for this pipeline.

---

## Known Issues

1. **News–Event Mismatch**: Robotaxi press releases are often omitted because the API filters on ticker “TSLA” rather than “Tesla.”
2. **Relevance Score Handling**: Defaulting missing scores to 1.0 masks true API scoring nuances.
3. **UI Confirmation Button**: Streamlit’s immediate application of sidebar changes calls for a dedicated “Apply” button to batch‐submit parameters.
4. **Data Flow Validation**: Need end‑to‑end checks to ensure front‑end selections propagate correctly to back‑end filters.

## Next Steps

* Enhance news queries to include both ticker and company name or topic filters.
* Refine relevance filtering via keyword matching (e.g., “Robotaxi”).
* Add a Streamlit “Apply” button to prevent partial state updates.
* Implement UI integration tests to verify parameter propagation and data consistency.
* Evaluate LLM‑based text analysis for automated sentiment and keyword extraction in upcoming sprints.