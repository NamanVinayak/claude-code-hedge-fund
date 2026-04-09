## System Prompt

N/A — news_sentiment_agent.py does not use a ChatPromptTemplate with a system/human tuple. It calls the LLM with a plain inline string prompt per article (not a reusable template).

## Human Template

Please analyze the sentiment of the following news headline with the following context: The stock is {ticker}. Determine if sentiment is 'positive', 'negative', or 'neutral' for the stock {ticker} only. Also provide a confidence score for your prediction from 0 to 100. Respond in JSON format.

Headline: {headline}
