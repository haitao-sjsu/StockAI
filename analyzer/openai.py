import pandas as pd
from typing import Optional, Dict, Any
from openai import OpenAI
import config
from config_lang import LANG_CONFIG
import streamlit as st

def analyze_news_with_openai(
    df_news: pd.DataFrame,
    signal_date: pd.Timestamp,
    price_change_pct: float,
    symbol: str,
    lang: str = "zh"
) -> Optional[str]:
    """
    Use OpenAI LLM to analyze daily news and infer reasons for stock price movements.
    """
    config_lang = LANG_CONFIG.get(lang, LANG_CONFIG["en"])
    
    def extract_response_text(response) -> str:
        try:
            return response.output[0].content[0].text.strip()
        except Exception as e:
            return f"[Error extracting response text: {e}]"
    
    if df_news.empty:
        return config_lang["no_news"]

    if not config.OPENAI_API_KEY:
        return config_lang["no_api_key"]

    try:
        client = OpenAI(api_key=config.OPENAI_API_KEY)

        # Build news summaries
        summaries = []
        for _, row in df_news.iterrows():
            ts = row["time_published"]
            summaries.append(
                f"{config_lang['time_label']}: {ts}\n"
                f"{config_lang['title_label']}: {row['title']}\n"
                f"{config_lang['summary_label']}: {row['summary']}\n"
            )
        
        news_text = "\n\n---\n\n".join(summaries)

        # Format date and direction
        date_str = signal_date.strftime(config_lang["date_format"])
        direction_text = config_lang[f"direction_up"] if price_change_pct > 0 else config_lang["direction_down"]
        
        # Format prompts
        user_prompt = config_lang["user_prompt"].format(
            symbol=symbol,
            date_str=date_str,
            direction_text=direction_text,
            price_change=abs(price_change_pct),
            news_text=news_text
        )

        response = client.responses.create(
            model=config.OPENAI_MODEL,
            instructions=config_lang['system_instruction'],
            input=user_prompt,
        )

        return extract_response_text(response)

    except Exception as err:
        err_msg = f"{config_lang['error_prefix']}: {err}"
        st.error(err_msg)
        return err_msg