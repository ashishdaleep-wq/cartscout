# 🛒 CartScout — AI Shopping Assistant

CartScout is a Streamlit shopping app with a built-in AI assistant. Browse a catalog of 100 products, filter by category, price and rating, read automatically summarized pros & cons for each product, manage a cart, and ask the chatbot for product info or shopping advice.

Built as a college capstone project by a team of four. Project lead: [Ashish](https://github.com/ashishdaleep-wq).

## Features

- **Search & filters** — text search across name, brand, category and tags; filter by category, max price and minimum rating.
- **Review summaries** — each product shows pros, cons and an overall verdict (e.g. "Highly Recommended"), generated from its reviews by a keyword-based sentiment scorer.
- **Cart** — add items, change quantities, remove items, see running totals.
- **AI chat assistant** — a layered chatbot:
  1. Greeting handler
  2. Off-topic guardrail (politics, news, religion, cricket, weather and similar topics are refused)
  3. Direct product lookup by name, brand or tag, with price, rating, stock status and sample reviews
  4. Fallback to an LLM (Groq, `llama-3.1-8b-instant`) for advice, comparisons and out-of-inventory requests
- **Bilingual replies** — answers in English by default and switches to Roman Urdu when the user writes in it.

## Tech stack

Python · Streamlit · Groq API (Llama 3.1) · python-dotenv

## Getting started

```bash
git clone https://github.com/ashishdaleep-wq/cartscout.git
cd cartscout

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env             # Windows: copy .env.example .env
# then open .env and paste your Groq API key (free at https://console.groq.com)

streamlit run app.py
```

The app opens at http://localhost:8501.

**No API key?** The app still runs. Search, filters, review summaries, the cart, and the chatbot's greeting, guardrail and product-lookup layers all work. Only the LLM advice layer is switched off.

## Project structure

```
cartscout/
├── app.py                # Streamlit UI: navbar, store, cart, about page, chat panel
├── chatbot.py            # Chat assistant (rules + Groq LLM fallback)
├── cart.py               # Cart logic on top of Streamlit session state
├── recommender.py        # Product loading, filtering, same-category recommendations
├── review_summarizer.py  # Keyword-based pros/cons and verdict from review text
├── products.json         # Catalog: 100 products, 5 categories, 10 brands
├── legacy/
│   └── recommender_v2.py # Early pandas-based prototype (not used by the app)
├── requirements.txt
└── .env.example
```

## Data

`products.json` holds 100 sample products (Electronics, Fashion, Home, Personal Care, Fitness). Each has a name, brand, category, price, rating, review count, stock status, tags and sample reviews. This is demo data, not live store data. Product images are loaded from Unsplash URLs.

## Known limitations

- Review "AI summaries" are keyword matching, not a language model, so sarcasm and negation are not understood.
- Chat memory lives in the running Streamlit process, so it is shared across browser sessions.
- The cart is kept in session state only and is lost on refresh. There is no checkout or database.

## Ideas for next steps

- Use the LLM for review summarization instead of keyword scoring
- Persist carts and users in a database
- Replace the sample catalog with a real product API

## Configuration

| Variable | Required | Purpose |
|---|---|---|
| `GROQ_API_KEY` | No (needed for LLM advice) | Groq API key for the chatbot fallback |

Never commit your `.env` file. It is already in `.gitignore`.

## License

MIT. See [LICENSE](LICENSE).
