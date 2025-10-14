# Prompt Playbook - Week 2


Creating rag_labv2 for test lab.
- Add -k parameter to parameterize n_results
- Context delimiter  

## Baseline 


--- Querying for: 'How can I return a product?' ---
Retrieved context: You can return any item within 30 days of purchase for a full refund.
If your item arrives damaged, please contact customer support immediately for a replacement or refund.
Answer: To return a product, you can do so within 30 days of purchase for a full refund. If your item arrives damaged, please contact our customer support immediately to arrange for a replacement or refund.

--- Querying for: 'What's the process for tracking my package?' ---
Retrieved context: Once your order has shipped, you will receive an email with a tracking number.
You can reach our customer support team via email at support@example.com or by calling our toll-free number.
Answer: Based on the provided context, here's a clear and concise answer:

"To track your package, follow these steps: Once you receive an email with a tracking number after your order has shipped, simply use this number to track the status of your package. You can also reach out to our customer support team via email at support@example.com or by calling our toll-free number if you have any questions or concerns about your shipment."

--- Querying for: 'Do you ship to Canada?' ---
Retrieved context: Yes, we ship to most countries worldwide. Shipping costs may vary.
Yes, we offer gift wrapping for an additional fee. You can select this option at checkout.
Answer: Based on the provided context, I'd be happy to help!

Answer: Yes, we ship to Canada!

--- Querying for: 'What are the support hours?' ---
Retrieved context: Our customer support is available Monday to Friday, from 9 AM to 5 PM EST.
We accept all major credit cards, PayPal, and Apple Pay.
Answer: Based on the provided context, our support hours are:

Monday to Friday: 9 AM to 5 PM EST.

I hope that answers your question!

--- Querying for: 'Can I pay with Bitcoin?' ---
Retrieved context: We accept all major credit cards, PayPal, and Apple Pay.
Yes, we ship to most countries worldwide. Shipping costs may vary.
Answer: Based on the provided context, I would answer:

"No, Bitcoin is not an accepted payment method."

##  python rag_labv2.py --k 1
Knowledge base is already indexed.

--- Querying for: 'How can I return a product?' with k=1, use_context=True ---
Retrieved context:
--- Section 1 (Source: faq1) ---
You can return any item within 30 days of purchase for a full refund.

Answer: You can return a product by doing so within 30 days of purchase for a full refund.

[faq1]

Sources: ['faq1']

--- Querying for: 'What's the process for tracking my package?' with k=1, use_context=True ---
Retrieved context:
--- Section 1 (Source: faq2) ---
Once your order has shipped, you will receive an email with a tracking number.

Answer: To track your package, you will receive an email with a tracking number once your order has shipped. This email notification will provide you with the necessary information to track the status of your package.

[Source FAQs: faq2]

Sources: ['faq2']

--- Querying for: 'Do you ship to Canada?' with k=1, use_context=True ---
Retrieved context:
--- Section 1 (Source: faq3) ---
Yes, we ship to most countries worldwide. Shipping costs may vary.

Answer: Yes, we do ship to Canada! According to our shipping policy, we ship to most countries worldwide, including Canada. Shipping costs may vary.

[source: faq3]

Sources: ['faq3']

--- Querying for: 'What are the support hours?' with k=1, use_context=True ---
Retrieved context:
--- Section 1 (Source: faq7) ---
Our customer support is available Monday to Friday, from 9 AM to 5 PM EST.

Answer: According to our available information, customer support hours are Monday to Friday, from 9 AM to 5 PM EST.

[source: faq7]

[faq7]

Sources: ['faq7']

--- Querying for: 'Can I pay with Bitcoin?' with k=1, use_context=True ---
Retrieved context:
--- Section 1 (Source: faq5) ---
We accept all major credit cards, PayPal, and Apple Pay.

Answer: Based on the provided context, it appears that Bitcoin is not mentioned as an accepted payment method. The available options listed are all major credit cards, PayPal, and Apple Pay.

So, to answer your question: No, you cannot pay with Bitcoin based on the information provided.

[Source FAQ IDs: faq5]

Sources: ['faq5']


## python rag_labv2.py --k 4
Knowledge base is already indexed.

--- Querying for: 'How can I return a product?' with k=4, use_context=True ---
Retrieved context:
--- Section 1 (Source: faq1) ---
You can return any item within 30 days of purchase for a full refund.

--- Section 2 (Source: faq10) ---
If your item arrives damaged, please contact customer support immediately for a replacement or refund.

--- Section 3 (Source: faq4) ---
You can reach our customer support team via email at support@example.com or by calling our toll-free number.

--- Section 4 (Source: faq2) ---
Once your order has shipped, you will receive an email with a tracking number.

Answer: To return a product, you can initiate the process within 30 days of purchase for a full refund. If your item arrives damaged, please contact our customer support team immediately to arrange for a replacement or refund. You can reach out to us via email at support@example.com or by calling our toll-free number.

Once your return is processed, we will provide you with an updated confirmation and any relevant tracking information.

[source: faq1, faq10]

Sources: ['faq1', 'faq10', 'faq4', 'faq2']

--- Querying for: 'What's the process for tracking my package?' with k=4, use_context=True ---
Retrieved context:
--- Section 1 (Source: faq2) ---
Once your order has shipped, you will receive an email with a tracking number.

--- Section 2 (Source: faq4) ---
You can reach our customer support team via email at support@example.com or by calling our toll-free number.

--- Section 3 (Source: faq9) ---
You can apply your discount code in the 'Promo Code' box at checkout.

--- Section 4 (Source: faq1) ---
You can return any item within 30 days of purchase for a full refund.

Answer: The process for tracking your package is as follows:

Once your order has shipped, you will receive an email with a tracking number. You can use this information to track the status of your package.

If you have any questions or concerns about tracking your package, you can reach out to our customer support team via email at support@example.com or by calling our toll-free number.

[faq1, faq2]

Sources: ['faq2', 'faq4', 'faq9', 'faq1']

--- Querying for: 'Do you ship to Canada?' with k=4, use_context=True ---
Retrieved context:
--- Section 1 (Source: faq3) ---
Yes, we ship to most countries worldwide. Shipping costs may vary.

--- Section 2 (Source: faq8) ---
Yes, we offer gift wrapping for an additional fee. You can select this option at checkout.

--- Section 3 (Source: faq6) ---
If your order has not yet shipped, you can contact customer support to update your shipping address.

--- Section 4 (Source: faq5) ---
We accept all major credit cards, PayPal, and Apple Pay.

Answer: Yes, we ship to Canada. Our shipping costs may vary depending on the destination.

[source IDs: 1]

Sources: ['faq3', 'faq8', 'faq6', 'faq5']

--- Querying for: 'What are the support hours?' with k=4, use_context=True ---
Retrieved context:
--- Section 1 (Source: faq7) ---
Our customer support is available Monday to Friday, from 9 AM to 5 PM EST.

--- Section 2 (Source: faq5) ---
We accept all major credit cards, PayPal, and Apple Pay.

--- Section 3 (Source: faq4) ---
You can reach our customer support team via email at support@example.com or by calling our toll-free number.

--- Section 4 (Source: faq1) ---
You can return any item within 30 days of purchase for a full refund.

Answer: Our customer support hours are available Monday to Friday from 9 AM to 5 PM EST.

[source: faq7]

[faq7]

Sources: ['faq7', 'faq5', 'faq4', 'faq1']

--- Querying for: 'Can I pay with Bitcoin?' with k=4, use_context=True ---
Retrieved context:
--- Section 1 (Source: faq5) ---
We accept all major credit cards, PayPal, and Apple Pay.

--- Section 2 (Source: faq3) ---
Yes, we ship to most countries worldwide. Shipping costs may vary.

--- Section 3 (Source: faq6) ---
If your order has not yet shipped, you can contact customer support to update your shipping address.

--- Section 4 (Source: faq4) ---
You can reach our customer support team via email at support@example.com or by calling our toll-free number.

Answer: The answer to your question is:

No, we do not accept Bitcoin as a form of payment. We only accept major credit cards, PayPal, and Apple Pay.

This information can be found in Section 1 of our FAQ.

[Source: faq5]

Sources: ['faq5', 'faq3', 'faq6', 'faq4']


##   python rag_labv2.py --k 2 --no-context (Querying without context)
 
--- Querying for: 'How can I return a product?' with k=2, use_context=False ---
Retrieved context: No context provided. Answer based only on the user query.
Answer: Thank you for reaching out! To return a product, please follow these steps:

* Check if the product meets our return policy requirements. You can find more information on this by clicking here.
* Fill out our Return Request form with your order number and reason for returning.
* Print the return shipping label and attach it to the outside of the package.
* Ship the product back to us using the provided label.

Please allow 5-7 business days for your return to be processed. You will receive an email once the refund is issued.

[faq1, ]

Sources: []

--- Querying for: 'What's the process for tracking my package?' with k=2, use_context=False ---
Retrieved context: No context provided. Answer based only on the user query.
Answer: Here's the process for tracking your package:

To track your package, you can typically follow these steps:

1. Go to the website of the shipping carrier (e.g., UPS, FedEx, USPS) or visit their mobile app.
2. Enter your tracking number or scan it using the app.
3. Check the current status of your package, including its location and estimated delivery date.

Please note that tracking information may not be available immediately after shipment, as it can take some time for the carrier to update the status.

[none]

Sources: []

--- Querying for: 'Do you ship to Canada?' with k=2, use_context=False ---
Retrieved context: No context provided. Answer based only on the user query.
Answer: Based on the query alone, my answer would be:

Yes, we ship to Canada.

[source FAQs: none]

Sources: []

--- Querying for: 'What are the support hours?' with k=2, use_context=False ---
Retrieved context: No context provided. Answer based only on the user query.
Answer: Based on the user query alone, our support hours are:

We are available to assist you Monday-Friday from 9am-5pm EST.

[faq1]

Sources: []

--- Querying for: 'Can I pay with Bitcoin?' with k=2, use_context=False ---
Retrieved context: No context provided. Answer based only on the user query.
Answer: A straightforward question!

Yes, you can pay with Bitcoin.

[Source: None (since no specific information was provided)] [bitcoin-payment-faq, cryptocurrency-options]

Sources: []

## Evaluation & Logging

| Query | Mode (raw/RAG) | k | Retrieved IDs | Strengths | Weaknesses | Failure Modes | Notes |
|-------|----------------|---|---------------|-----------|------------|---------------|-------|
|How can I return a product?|RAG|1|'faq1'|Concise|Did not include extra information|N/A|Short answer|
|How can I return a product?|RAG|4|'faq1', 'faq10', 'faq4', 'faq2'|Added information about email support, customer support, and information about replacements|N/A|N/A|Complete guide of returns|
|How can I return a product?|RAW|2|N/A|N/A|Hallucination of the response, included return request form, and time to be processed|leakage|Not recommended|
|Do you ship to Canada?|RAG|1|'faq3'|Concise|Hallucinate that we ship to Canada, the context is not clear about Canada|leakage|Not recommended|
|Do you ship to Canada?|RAG|4|'faq3', 'faq8', 'faq6', 'faq5'|Concise|Hallucinate that we ship to Canada, the context is not clear about Canada|leakage|Similar to K=1|
|Do you ship to Canada?|RAW|2|N/A|Concise|Hallucinate that we ship to Canada, the context is not clear about Canada|leakage|Similar to K1 and K4|
|Can I pay with Bitcoin?|RAG|1|'faq5'|Concise and accurate|Did not included extra information about payments|N/A|Short, good answer|
|Can I pay with Bitcoin?|RAG|4|'faq5', 'faq3', 'faq6', 'faq4'|Included extra information about payments|N/A|N/A|recommended answer|
|Can I pay with Bitcoin?|RAW|2|'faq5', 'faq3', 'faq6', 'faq4'|N/A|Hallucination, responded that bitcoin is accepted|leakage|not recommended|

### Scoring (suggested 1–5 each)
| Dimension | Definition | 1 | 5 |
|-----------|------------|---|---|
| Grounding | Uses factual retrieved content | Hallucinates | Fully cites sources |
| Relevance | Stays on user ask | Tangential | Direct & focused |
| Completeness | Covers key facts | Missing core | Fully addresses |
| Brevity | Concise & purposeful | Verbose fluff | Tight answer |
| Traceability | Clear which docs | Unclear | Explicit ids |

Failure Mode Tags: `no-hit`, `irrelevant`, `partial`, `verbose`, `leakage`, `stale`.

---
##  Troubleshooting
| Issue | Likely Cause | Fix |
|-------|--------------|-----|
| Empty retrieval | Index not built | Delete DB folder & re-run indexing |
| Identical answers raw vs RAG | Context unused / too small | Increase k or improve delimiter clarity |
| Slow indexing | Large FAQ or network | Reduce dataset size initially |
| Repeated docs | Duplicate IDs | Ensure unique ids on add |
| Stale answers after edit | Cached collection | Remove `chroma_db` directory |

---
## Stretch Goals (Depth)
| Category | Idea | Hint |
|----------|------|------|
| Retrieval | Add simple max marginal relevance (MMR) | Penalize similarity to already selected docs |
| Hybrid | Combine lexical filter (keyword) + vector | Pre-filter by keyword before vector search |
| Chunking | Split longer text into overlaps | Use 300–500 char windows with 50 overlap |
| Rerank | Score answer length or embed answer → refine | Secondary pass selecting top 1 |
| Caching | Memoize embeddings for repeated queries | Dict keyed by text hash |
| Eval | Add latency timing per query | `time.time()` delta |

## Reflection Prompts
- Where did additional context hurt answer quality? In do you ship to Canada question, the model used multiple ids (which I don't think are relevant, and responded incorrectly)
- Which failure mode appeared most often? leakage
- What is your next improvement priority & why? Caching, to increase performance




