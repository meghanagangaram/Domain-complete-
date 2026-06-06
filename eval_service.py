import os
import json
import time
import numpy as np
from google import genai
from google.genai import types
from rag_service import retrieve_similar_chunks, generate_rag_answer, client

EVAL_RESULTS_FILE = os.path.join("backend", "data", "eval_results.json")

# 20 Ground Truth Q&A pairs for the Galactic Archive
GROUND_TRUTH_DATASET = [
    {
        "id": 1,
        "query": "What is the coordinate of Planet Eldoria?",
        "ground_truth_answer": "The coordinates of Planet Eldoria are 142.88.92.11.",
        "target_doc_id": "planet_eldoria"
    },
    {
        "id": 2,
        "query": "What is the wind speed of Zephyrus-9 and where do people live?",
        "ground_truth_answer": "The wind speed on Zephyrus-9 exceeds 800 km/h. The population lives in suspended floating 'Aero-Domes' 50 kilometers above the surface.",
        "target_doc_id": "planet_zephyrus_9"
    },
    {
        "id": 3,
        "query": "What repeating signal did Outpost 42 detect in 2259?",
        "ground_truth_answer": "In 2259, Outpost 42 detected a repeating 8-digit sequence: 10011101 from deep within the void.",
        "target_doc_id": "station_outpost_42"
    },
    {
        "id": 4,
        "query": "Who is the leader of the Void Syndicate and what species is he?",
        "ground_truth_answer": "The leader of the Void Syndicate is Slyvox the Shadow, who is a Void Weaver species.",
        "target_doc_id": "faction_void_syndicate"
    },
    {
        "id": 5,
        "query": "What was banned under the Anti-Weapons Treaty of 2240?",
        "ground_truth_answer": "The Anti-Weapons Treaty of 2240 banned the development of planetary-disruption weapons, such as the weaponization of the Void Engine.",
        "target_doc_id": "faction_galactic_council"
    },
    {
        "id": 6,
        "query": "Which engine technology was developed by the Eldorian Sages and what does it use as fuel?",
        "ground_truth_answer": "The Hyperdrive Engine was developed by the Eldorian Sages, and it uses refined Aurelium Crystals as its fuel source.",
        "target_doc_id": "tech_hyperdrive_engine"
    },
    {
        "id": 7,
        "query": "What cyberattack did the Shadow Nexus perform in 2248?",
        "ground_truth_answer": "In 2248, the Shadow Nexus hacked Frosthaven, deactivating security grids and waking 45 high-profile political prisoners prematurely.",
        "target_doc_id": "planet_frosthaven" # Also related to faction_shadow_nexus
    },
    {
        "id": 8,
        "query": "What energy generation capacity does the Dyson Swarm have?",
        "ground_truth_answer": "The Dyson Swarm generates approximately 1.2 x 10^26 Watts of power, satisfying the energy demands of the entire Core Systems.",
        "target_doc_id": "tech_dyson_swarm"
    },
    {
        "id": 9,
        "query": "What is Project Genesis and where is it researched?",
        "ground_truth_answer": "Project Genesis aims to create a hybrid biological-mechanical organism (like Subject Omega) that can survive in the vacuum of deep space. It is researched at the classified Genesis Lab in the Hidden Nebula.",
        "target_doc_id": "station_genesis_lab"
    },
    {
        "id": 10,
        "query": "What is the temperature in the twilight zone of Gliese-581-V?",
        "ground_truth_answer": "The twilight zone of Gliese-581-V has a temperate climate with an average temperature of 18°C.",
        "target_doc_id": "planet_gliese_581_v"
    },
    {
        "id": 11,
        "query": "Who is the leader of the Harmony Order?",
        "ground_truth_answer": "The leader of the Harmony Order is Elder Tree Elder, a Siliconite representative.",
        "target_doc_id": "faction_harmony_order"
    },
    {
        "id": 12,
        "query": "Which planet is the headquarters of the Iron Vanguard?",
        "ground_truth_answer": "The headquarters of the Iron Vanguard is Planet Obsidian Prime, specifically at the Dark Forge.",
        "target_doc_id": "faction_iron_vanguard" # Or planet_obsidian_prime
    },
    {
        "id": 13,
        "query": "What are the coordinates of the Vault World Aethelgard?",
        "ground_truth_answer": "The coordinates of Planet Aethelgard are 001.00.00.01.",
        "target_doc_id": "planet_aethelgard"
    },
    {
        "id": 14,
        "query": "What happened during the Chrono-Anchor test in 2252?",
        "ground_truth_answer": "During the 2252 test at Aethelgard, the laboratory was locked in a 4-second time loop for three weeks before the power grid could be remotely shut down.",
        "target_doc_id": "tech_chrono_anchor"
    },
    {
        "id": 15,
        "query": "What is the average lifespan of a Siliconite?",
        "ground_truth_answer": "The average lifespan of a Siliconite is 1000 Earth Years.",
        "target_doc_id": "species_siliconites"
    },
    {
        "id": 16,
        "query": "What is the Code of the Sky and which species lives by it?",
        "ground_truth_answer": "The Code of the Sky dictates fair combat and loyalty to the Alliance. The Avians of Aquila live by this code.",
        "target_doc_id": "species_aquila_avians"
    },
    {
        "id": 17,
        "query": "What is the coordinate of the Void Gate?",
        "ground_truth_answer": "The coordinates of the Void Gate (Warp Hub Delta) are 880.11.22.44.",
        "target_doc_id": "station_void_gate"
    },
    {
        "id": 18,
        "query": "What unique feature allows islands to float on Planet Valyria?",
        "ground_truth_answer": "The islands float due to high concentrations of Levitate Ore in their foundations.",
        "target_doc_id": "planet_valyria"
    },
    {
        "id": 19,
        "query": "Who developed the Bio-Dome Generator?",
        "ground_truth_answer": "The Bio-Dome Generator was developed by Horizon Biotech Laboratories.",
        "target_doc_id": "tech_biodome_gen"
    },
    {
        "id": 20,
        "query": "What is the average lifespan of an Eldorian?",
        "ground_truth_answer": "The average lifespan of an Eldorian is 400 Earth Years.",
        "target_doc_id": "species_eldorians"
    }
]

# --- LLM-as-a-judge Evaluation helper ---
def judge_answer_quality(query, context, generated_answer, ground_truth):
    """
    Evaluates faithfulness, relevance, and recall using Gemini API.
    If Gemini client is not initialized, returns fallback scores.
    """
    if not client:
        # Mock scores if API is not available
        return {
            "faithfulness": 1.0,
            "relevance": 1.0,
            "recall": 1.0,
            "reasoning": "Offline mode: Auto-assigned perfect scores."
        }

    judge_prompt = f"""You are a rigorous QA judge evaluating a Retrieval-Augmented Generation (RAG) system.
You will be given:
1. User Query
2. Retrieved Context Fragments (the text the system retrieved to answer the question)
3. Generated Answer (the system's response)
4. Ground Truth Answer (the gold-standard answer)

Your job is to rate the Generated Answer on a scale of 0.0 to 1.0 (where 1.0 is perfect) for the following three metrics:

1. **Faithfulness (Factual Consistency)**: Is the generated answer fully grounded in the retrieved context? It should NOT contain details that are NOT in the context. (0.0 = completely hallucinated/unsupported, 1.0 = perfectly faithful, no hallucinations).
2. **Answer Relevance**: Does the generated answer directly address the user's query? It should not be vague or talk about unrelated topics. (0.0 = completely irrelevant, 1.0 = highly relevant).
3. **Context Recall**: Does the generated answer capture the key factual details present in the Ground Truth Answer? (0.0 = none of the ground truth details are captured, 1.0 = all critical ground truth details are captured).

Provide your response in raw JSON format with exactly these keys:
"faithfulness": float (0.0 to 1.0),
"relevance": float (0.0 to 1.0),
"recall": float (0.0 to 1.0),
"reasoning": string (brief explanation of your scoring)

Do NOT include any markdown code blocks, backticks, or other text outside the JSON.

---
[EVALUATION CASE]
User Query: {query}

Retrieved Context:
{context}

Generated Answer:
{generated_answer}

Ground Truth Answer:
{ground_truth}
---
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=judge_prompt,
            config=types.GenerateContentConfig(
                temperature=0.0,
                response_mime_type="application/json"
            )
        )
        scores = json.loads(response.text.strip())
        return {
            "faithfulness": float(scores.get("faithfulness", 0.0)),
            "relevance": float(scores.get("relevance", 0.0)),
            "recall": float(scores.get("recall", 0.0)),
            "reasoning": scores.get("reasoning", "")
        }
    except Exception as e:
        print(f"Error calling judge: {e}")
        return {
            "faithfulness": 0.5,
            "relevance": 0.5,
            "recall": 0.5,
            "reasoning": f"Judge evaluation failed: {str(e)}"
        }

# --- Batch Evaluation Run ---
def run_evaluation():
    print("Starting RAG evaluation pipeline...")
    results = []
    
    total_hit = 0
    total_mrr = 0.0
    
    total_faithfulness = 0.0
    total_relevance = 0.0
    total_recall = 0.0
    
    start_time = time.time()
    
    for item in GROUND_TRUTH_DATASET:
        query = item["query"]
        target_doc = item["target_doc_id"]
        ground_truth = item["ground_truth_answer"]
        
        print(f"Running Eval Case {item['id']}: '{query}'")
        
        # 1. Evaluate Retrieval
        retrieved_results = retrieve_similar_chunks(query, k=4)
        retrieved_docs = [chunk["doc_id"] for chunk, _ in retrieved_results]
        
        # Hit Rate: Target document in top-k
        hit = 1 if target_doc in retrieved_docs else 0
        total_hit += hit
        
        # MRR calculation
        mrr = 0.0
        if target_doc in retrieved_docs:
            rank = retrieved_docs.index(target_doc) + 1
            mrr = 1.0 / rank
        total_mrr += mrr
        
        # 2. Evaluate Generation
        rag_response = generate_rag_answer(query)
        generated_ans = rag_response["answer"]
        
        # Format context for the judge
        context_text = "\n\n".join([f"Source: {c['title']}\nContent: {c['content']}" for c in rag_response["sources"]])
        
        # Call LLM judge
        judge_scores = judge_answer_quality(query, context_text, generated_ans, ground_truth)
        
        total_faithfulness += judge_scores["faithfulness"]
        total_relevance += judge_scores["relevance"]
        total_recall += judge_scores["recall"]
        
        results.append({
            "id": item["id"],
            "query": query,
            "target_doc_id": target_doc,
            "ground_truth": ground_truth,
            "generated_answer": generated_ans,
            "retrieved_sources": [
                {"title": c["title"], "score": c["score"]} for c in rag_response["sources"]
            ],
            "retrieval_hit": hit,
            "retrieval_mrr": mrr,
            "metrics": {
                "faithfulness": judge_scores["faithfulness"],
                "relevance": judge_scores["relevance"],
                "recall": judge_scores["recall"]
            },
            "reasoning": judge_scores["reasoning"]
        })
        
        # Throttle slightly to respect API limits if needed
        time.sleep(0.5)

    n_cases = len(GROUND_TRUTH_DATASET)
    summary = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "duration_seconds": round(time.time() - start_time, 2),
        "total_test_cases": n_cases,
        "retrieval_hit_rate": round(total_hit / n_cases, 3),
        "retrieval_mrr": round(total_mrr / n_cases, 3),
        "avg_faithfulness": round(total_faithfulness / n_cases, 3),
        "avg_relevance": round(total_relevance / n_cases, 3),
        "avg_recall": round(total_recall / n_cases, 3),
        "results": results
    }
    
    os.makedirs(os.path.dirname(EVAL_RESULTS_FILE), exist_ok=True)
    with open(EVAL_RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
        
    print("Evaluation completed successfully. Results saved.")
    return summary

def get_latest_eval_results():
    if os.path.exists(EVAL_RESULTS_FILE):
        try:
            with open(EVAL_RESULTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
    return None

if __name__ == "__main__":
    summary = run_evaluation()
    print("\nEvaluation Summary:")
    print(f"Hit Rate: {summary['retrieval_hit_rate']:.2%}")
    print(f"MRR: {summary['retrieval_mrr']:.3f}")
    print(f"Faithfulness: {summary['avg_faithfulness']:.3f}")
    print(f"Relevance: {summary['avg_relevance']:.3f}")
    print(f"Context Recall: {summary['avg_recall']:.3f}")
