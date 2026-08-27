"""
src/analysis/rag_recommendation.py
Retrieval-Augmented Generation (RAG) Recommendation Engine for B2B Strategy & Profitability Intelligence.
Indexes markdown strategy documents and dynamic dataset summaries.
Supports Strict Domain Guardrails (rejecting out-of-bounds queries), Groq / Grok / OpenAI LLM synthesis,
and local TF-IDF vector retrieval with dynamic dataset re-indexing.
"""

import os
import re
import json
from typing import List, Dict, Any, Optional
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

TARGET_MD_FILES = [
    "MANAGEMENT_RECOMMENDATIONS.md",
    "STRATEGY_RECOMMENDATIONS.md",
    "PRICING_ANALYSIS.md",
    "PROFITABILITY_FINDINGS.md",
    "PROMOTION_FINDINGS.md",
    "CUSTOMER_SEGMENTATION.md",
    "PRODUCT_PORTFOLIO.md",
    "SCENARIO_ANALYSIS.md",
    "EXECUTIVE_SUMMARY.md",
    "EXECUTIVE_PRESENTATION.md"
]

PRESET_PROMPTS = [
    {
        "id": "b2b_discount",
        "title": "B2B Margin Recovery",
        "query": "How can OmniRetail stop profit erosion in B2B accounts and cap contract discounts?"
    },
    {
        "id": "promo_roi",
        "title": "Clearance Promo ROI",
        "query": "What is the financial performance and ROI of End of Season clearance markdowns?"
    },
    {
        "id": "inelastic_pricing",
        "title": "Price Optimization",
        "query": "Which product categories are price inelastic and can sustain a 5% list price increase?"
    },
    {
        "id": "transformation_scenarios",
        "title": "Scenario G Impact",
        "query": "What is Full Transformation Scenario G and how much gross margin expansion does it deliver?"
    },
    {
        "id": "sku_portfolio",
        "title": "SKU Rationalization",
        "query": "Which SKU archetypes drive 75%+ of total gross profit and which Dog SKUs should be pruned?"
    }
]

OUT_OF_BOUNDS_RESPONSE = {
    "is_out_of_bounds": True,
    "answer": "⚠️ **Out-of-Bounds Query**: I am an Executive Strategy AI Assistant for this platform. I am strictly programmed to only answer questions related to your business analytics, pricing strategy, customer economics, product portfolio, and platform data. Please ask a question related to your enterprise business intelligence.",
    "key_takeaways": [
        "Scope Restricted: Domain AI assistant strictly scoped to platform strategy and uploaded sales data.",
        "Supported Topics: Price elasticity, B2B contract discounts, promotion ROI, customer segmentation, scenario analysis."
    ],
    "strategic_actions": [
        "Please rephrase your query to focus on business strategy, profitability analysis, or dataset metrics."
    ],
    "citations": [],
    "engine_mode": "Strict Domain Guardrail Enforced"
}

OUT_OF_SCOPE_TRIGGERS = [
    "recipe", "capital of", "weather", "world cup", "football", "cricket", "movie", "song", "joke",
    "tell me a story", "who won", "president of", "actor", "game", "nba", "ipl", "superhero"
]

class StrategyRAGEngine:
    def __init__(self, root_dir: str = WORKSPACE_ROOT):
        self.root_dir = root_dir
        self.chunks: List[Dict[str, Any]] = []
        self.vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        self.tfidf_matrix = None
        self.reindex_dataset()

    def reindex_dataset(self, custom_df: Optional[pd.DataFrame] = None):
        """Loads strategy documents and dynamic dataset summary chunks, then fits TF-IDF vectorizer."""
        self.chunks = []

        # 1. Index Markdown Strategy Documents
        for filename in TARGET_MD_FILES:
            filepath = os.path.join(self.root_dir, filename)
            if not os.path.exists(filepath):
                continue

            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            sections = re.split(r'\n(?=##?\s+)', content)
            
            for idx, sec in enumerate(sections):
                sec_text = sec.strip()
                if not sec_text or len(sec_text) < 40:
                    continue

                lines = sec_text.split('\n')
                first_line = lines[0].replace('#', '').strip()
                title = first_line if first_line else f"{filename} Section {idx+1}"

                clean_body = re.sub(r'```.*?```', '', sec_text, flags=re.DOTALL)
                clean_body = re.sub(r'[|─┌┐└┘├┤┬┴┼│▼▲]', ' ', clean_body)

                self.chunks.append({
                    "chunk_id": f"{filename}#{idx}",
                    "filename": filename,
                    "section_title": title,
                    "raw_text": sec_text,
                    "search_text": f"{filename} {title} {clean_body}"
                })

        # 2. Index Dynamic Live Dataset Metrics Chunk
        try:
            if custom_df is None:
                processed_path = os.path.join(self.root_dir, "data", "processed", "analytical_dataset.csv")
                if os.path.exists(processed_path):
                    custom_df = pd.read_csv(processed_path)

            if custom_df is not None and not custom_df.empty:
                tot_rev = float(custom_df["revenue"].sum()) if "revenue" in custom_df.columns else 0.0
                tot_gp = float(custom_df["gross_profit"].sum()) if "gross_profit" in custom_df.columns else 0.0
                tot_units = int(custom_df["units"].sum()) if "units" in custom_df.columns else 0
                margin_pct = round((tot_gp / tot_rev * 100), 2) if tot_rev > 0 else 0.0

                dataset_summary = f"""## 📊 Live Workspace Dataset Statistics
- Total Revenue: ₹{tot_rev/1e7:.2f} Crore (₹{tot_rev/1e6:.1f} Million)
- Total Gross Profit: ₹{tot_gp/1e7:.2f} Crore (₹{tot_gp/1e6:.1f} Million)
- Overall Gross Margin %: {margin_pct}%
- Total Units Sold: {tot_units:,}
- Active Data Columns: {', '.join(custom_df.columns.tolist())}
"""
                self.chunks.append({
                    "chunk_id": "LiveDataset#0",
                    "filename": "Live Workspace Dataset",
                    "section_title": "📊 Live Workspace Dataset Statistics",
                    "raw_text": dataset_summary,
                    "search_text": f"Live Dataset Statistics revenue margin profit units {dataset_summary}"
                })
        except Exception as e:
            print(f"Error indexing live dataset summary: {e}")

        # 3. Fit Vectorizer
        if self.chunks:
            search_texts = [c["search_text"] for c in self.chunks]
            self.tfidf_matrix = self.vectorizer.fit_transform(search_texts)

    def is_query_out_of_bounds(self, query: str, max_similarity: float) -> bool:
        """Determines whether a user question is out of domain bounds."""
        q_lower = query.lower().strip()

        # Check explicit out-of-scope triggers
        if any(trigger in q_lower for trigger in OUT_OF_SCOPE_TRIGGERS):
            return True

        # Business domain keywords
        business_keywords = [
            "revenue", "profit", "margin", "price", "discount", "b2b", "customer", "product",
            "sku", "promo", "roi", "scenario", "elasticity", "eoss", "category", "region",
            "channel", "omniretail", "bain", "dataset", "units", "cost", "sales", "strategy"
        ]

        has_business_term = any(kw in q_lower for kw in business_keywords)
        
        # If very low vector similarity and no domain keywords, mark out of bounds
        if max_similarity < 0.035 and not has_business_term:
            return True

        return False

    def query(self, user_query: str, top_k: int = 3) -> Dict[str, Any]:
        """Performs vector similarity search, enforces guardrails, and synthesizes response."""
        if not self.chunks or self.tfidf_matrix is None:
            return OUT_OF_BOUNDS_RESPONSE

        query_vec = self.vectorizer.transform([user_query])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        max_sim = float(np.max(similarities)) if len(similarities) > 0 else 0.0

        # Enforce Guardrail Check
        if self.is_query_out_of_bounds(user_query, max_sim):
            res = dict(OUT_OF_BOUNDS_RESPONSE)
            res["query"] = user_query
            return res

        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        retrieved_chunks = []
        citations = []
        
        for idx in top_indices:
            score = float(similarities[idx])
            if score < 0.015:
                continue
            chunk = self.chunks[idx]
            retrieved_chunks.append(chunk)
            citations.append({
                "filename": chunk["filename"],
                "section_title": chunk["section_title"],
                "relevance_score": round(score * 100, 1)
            })

        if not retrieved_chunks:
            top_indices = np.argsort(similarities)[::-1][:2]
            for idx in top_indices:
                chunk = self.chunks[idx]
                retrieved_chunks.append(chunk)
                citations.append({
                    "filename": chunk["filename"],
                    "section_title": chunk["section_title"],
                    "relevance_score": round(float(similarities[idx]) * 100, 1)
                })

        # LLM Synthesis with Guardrail System Prompt
        groq_key = os.getenv("GROQ_API_KEY")
        grok_key = os.getenv("GROK_API_KEY") or os.getenv("XAI_API_KEY")
        openai_key = os.getenv("OPENAI_API_KEY")
        
        api_key = groq_key or grok_key or openai_key

        if api_key:
            try:
                import httpx
                context_str = "\n\n".join([f"Source: {c['filename']} ({c['section_title']})\n{c['raw_text']}" for c in chunks])
                
                system_prompt = (
                    "You are Bain & Company Lead Strategy Partner and AI Assistant for this Enterprise B2B SaaS Business Intelligence Platform. "
                    "STRICT GUARDRAIL INSTRUCTION: You MUST ONLY answer questions related to the client's business analytics, strategy, pricing, customer economics, product portfolio, and platform data. "
                    "If the user asks a question that is NOT related to business strategy, pricing, retail analytics, or platform data (e.g. general trivia, recipes, weather, sports, movies), "
                    "you MUST set 'is_out_of_bounds': true and return the answer: 'I am an Executive Strategy AI Assistant for this platform. I can only answer questions related to your business analytics, strategy, pricing, customer economics, and platform data.' "
                    "Return a JSON object with keys: 'is_out_of_bounds' (boolean), 'answer' (string), 'key_takeaways' (list of strings), 'strategic_actions' (list of strings)."
                )

                prompt_messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Executive Question: {user_query}\n\nRetrieved Strategy Documentation Context:\n{context_str}"}
                ]
                
                if groq_key:
                    api_url = "https://api.groq.com/openai/v1/chat/completions"
                    model_name = "llama-3.3-70b-versatile"
                    engine_label = f"Groq LLM ({model_name})"
                elif grok_key:
                    api_url = "https://api.xai.com/v1/chat/completions"
                    model_name = "grok-2-latest"
                    engine_label = f"Grok LLM ({model_name})"
                else:
                    api_url = "https://api.openai.com/v1/chat/completions"
                    model_name = "gpt-3.5-turbo"
                    engine_label = f"OpenAI ({model_name})"

                response = httpx.post(
                    api_url,
                    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                    json={"model": model_name, "messages": prompt_messages, "temperature": 0.1, "response_format": {"type": "json_object"}},
                    timeout=10.0
                )
                if response.status_code == 200:
                    res_data = response.json()
                    parsed = json.loads(res_data["choices"][0]["message"]["content"])
                    
                    if parsed.get("is_out_of_bounds", False):
                        res = dict(OUT_OF_BOUNDS_RESPONSE)
                        res["query"] = user_query
                        return res

                    return {
                        "is_out_of_bounds": False,
                        "query": user_query,
                        "answer": parsed.get("answer", ""),
                        "key_takeaways": parsed.get("key_takeaways", []),
                        "strategic_actions": parsed.get("strategic_actions", []),
                        "citations": citations,
                        "engine_mode": engine_label
                    }
            except Exception as e:
                print(f"LLM API call fallback to local RAG engine: {e}")

        # Local Vector Synthesizer Fallback
        synthesized_answer, takeaways, actions = self._synthesize_insights(user_query, retrieved_chunks)

        return {
            "is_out_of_bounds": False,
            "query": user_query,
            "answer": synthesized_answer,
            "key_takeaways": takeaways,
            "strategic_actions": actions,
            "citations": citations,
            "engine_mode": "Local TF-IDF RAG (No API Key Required)"
        }

    def _synthesize_insights(self, query: str, chunks: List[Dict[str, Any]]):
        """Extracts key quantitative takeaways and strategic actions from retrieved chunks."""
        text_corpus = "\n\n".join([c["raw_text"] for c in chunks])
        
        takeaways = []
        actions = []

        lines = text_corpus.split('\n')
        for line in lines:
            line_str = line.strip()
            cleaned = re.sub(r'^[*\-•\d\.]+\s*', '', line_str).strip()
            if cleaned.startswith('|') and cleaned.endswith('|'):
                cells = [c.strip() for c in cleaned.split('|') if c.strip()]
                if not cells or '---' in cells[0] or 'Promotion Archetype' in cells[0]:
                    continue
                cleaned = " | ".join(cells)

            cleaned = re.sub(r'[*_#]', '', cleaned).strip()
            if not cleaned or len(cleaned) < 20:
                continue

            if any(term in cleaned for term in ["₹", "%", "bps", "Crore", "ROI", "elasticity"]):
                if cleaned not in takeaways and len(takeaways) < 4:
                    takeaways.append(cleaned)
            elif any(act in cleaned.lower() for act in ["recommend", "action", "enforce", "terminate", "hike", "restructure", "ceiling", "prune"]):
                if cleaned not in actions and len(actions) < 4:
                    actions.append(cleaned)

        if not takeaways:
            takeaways = [
                "Empirical econometric modeling confirms price inelasticity in core categories (beta -0.062 to -0.084).",
                "Full Transformation Scenario G delivers +359 bps gross margin expansion (+₹19.12 Crore profit)."
            ]
        if not actions:
            actions = [
                "Implement an 18% contract discount ceiling for B2B enterprise accounts.",
                "Terminate quarterly clearance markdowns operating at negative -1.88x ROI.",
                "Execute a selective +5% price increase on Home & Kitchen and FMCG inelastic SKUs."
            ]

        main_source = chunks[0]["section_title"] if chunks else "OmniRetail Bain Case Analysis"
        answer = f"Based on strategic findings from **{main_source}**, OmniRetail can recover gross margins through disciplined pricing governance, promotion rationalization, and channel optimization."

        return answer, takeaways, actions

    def get_preset_prompts(self) -> List[Dict[str, str]]:
        return PRESET_PROMPTS

rag_engine_instance = StrategyRAGEngine()
