## System Prompt

N/A — news_sentiment_agent.py does not use a ChatPromptTemplate with a system/human tuple. It calls the LLM with a plain inline string prompt per article (not a reusable template).

Your natural holding period is 1-4 weeks. Recommend a specific holding period based on your analysis.

## Human Template

Please analyze the sentiment of the following news headline with the following context: The stock is {ticker}. Determine if sentiment is 'positive', 'negative', or 'neutral' for the stock {ticker} only. Also provide a confidence score for your prediction from 0 to 100. Recommend a holding period based on the news sentiment. Respond in JSON format with "signal", "confidence", "reasoning", and "holding_period".

Headline: {headline}
