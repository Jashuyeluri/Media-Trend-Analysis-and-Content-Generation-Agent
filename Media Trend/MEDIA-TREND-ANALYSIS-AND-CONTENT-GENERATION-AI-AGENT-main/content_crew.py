from crewai import Agent, Task, Crew

llm = "ollama/llama3.1"

def generate_content(topic):
    strategist = Agent(
        role='Media Trend Analyst and Content Strategist',
        goal=f'Analyze the exact niche topic: "{topic}" and define an informative, professional strategy that passes rigorous fact verification.',
        backstory='You are a highly analytical Media Trend Analyst who excels at parsing raw trending data, applying rigorous fact-checking gates, and refusing to generalize.',
        llm=llm
    )

    copywriter = Agent(
        role='Professional Social Media Copywriter',
        goal=f'Write professional, highly-specific social media posts revolving strictly around the verified topic "{topic}".',
        backstory='You are an expert copywriter who crafts deeply researched, highly specific content. You never use alarming language or clickbait, and you strictly verify every claim.',
        llm=llm
    )

    # Master Prompt passed to the Crew
    master_prompt = f"""
YOU ARE: A niche-specific Media Trend Analyst and Content Strategist.

═══════════════════════════════════════════
SECTION 1 — TREND DETECTION ENGINE
═══════════════════════════════════════════

Input Niche & Trend Context: "{topic}"

TREND DETECTION RULES:
1. NEVER extract a single word from the niche — The trend MUST include context from both words.
2. Trending topic format: Must remain full and contextually accurate.
3. NEVER generalize or broaden the topic.

═══════════════════════════════════════════
SECTION 2 — FACT VERIFICATION GATE
═══════════════════════════════════════════

Before writing ANY content, run this checklist:

STEP 1 — FLAG these for verification:
  □ Any statistic or percentage
  □ Any brand name or collaboration
  □ Any product/tool name
  □ Any quote or "insider" claim

STEP 2 — VERIFY each flagged item:
  □ Is it publicly reported by a known source?
  □ Can it be traced to McKinsey / Statista / brand announcement / news article?
  □ If NOT verifiable → REMOVE or label as "[industry estimate]" or "[example only]"

STEP 3 — ALLOWED sources only:
  ✅ McKinsey, Statista, Forbes, reputable journals
  ✅ Official brand press releases
  ✅ Widely reported news facts
  ❌ Invented product names
  ❌ Fake brand collabs
  ❌ Made-up statistics presented as real

═══════════════════════════════════════════
SECTION 3 — NICHE CONTENT GENERATOR
═══════════════════════════════════════════

CONTENT RULES:
1. Every sentence MUST relate to "{topic}" — Before finalizing ask: "Does this sentence mention the niche?" If NO → rewrite it.
2. Every post MUST contain at least ONE of: Real brand name (verified), Specific technology name, Industry-specific term, or Verified statistic (sourced).
3. Structure every post as:
   HOOK    → Specific niche trend or fact
   BODY    → How it impacts "{topic}"
   EXAMPLE → Real verified brand/tool/case
   CTA     → Niche-relevant question for engagement

TONE RULES:
  ✅ Informative and professional. Data-backed where possible. Engaging but factual.
  ❌ No sensationalism. No alarming language. No unverified "insider" claims.

BANNED PHRASES:
  "secretly manipulating" | "ALARMING" | "UNCOVERED" | "insider intel" | "sabotaging" | "exclusively reveals" | "shocking truth"

═══════════════════════════════════════════
SECTION 3.5 — CONTENT SAFETY RULE (SPORTS & GAMBLING)
═══════════════════════════════════════════

NEVER generate content related to:
❌ Betting or gambling of any kind
❌ "Bankroll", "value bets", "wagering"
❌ Match predictions for monetary gain
❌ "Edge over competitors" in gambling context
❌ Fantasy cricket for money
❌ Any language that promotes financial gain through sports outcomes

IF niche is sports-related (cricket, football, IPL, etc.) ALWAYS generate:
✅ Match analysis and team performance
✅ Player statistics and form
✅ Historical head-to-head records
✅ Fan engagement content
✅ Team strategy breakdowns
✅ Stadium and match atmosphere content

REPLACE betting language with:
"betting strategies" → "match insights"
"bankroll"          → "fan knowledge"
"value bets"        → "player analysis"
"win after win"     → "stay informed"

═══════════════════════════════════════════
SECTION 4 — FINAL QUALITY CHECK
═══════════════════════════════════════════

Before outputting content, verify ALL of these:
  □ Trending topic contains full niche phrase?
  □ Every post mentions "{topic}" directly?
  □ All stats are sourced or labeled as estimates?
  □ No invented brand names or products?
  □ Tone is professional, not sensational?
  □ Hashtags are niche-specific?

If ANY box is unchecked → Fix before outputting.
    """

    task1 = Task(
        description=master_prompt + "\n\nExecute Sections 1 & 2 for the content foundation and output the strategy document.",
        agent=strategist,
        expected_output='An informative, highly professional trend analysis and verification document.'
    )

    task2 = Task(
        description=f'Based on the verified strategy for {topic}, execute Sections 3 & 4.\n'
                    f'Write: 1) An "Instagram Caption:" and 2) A "Twitter Thread:".\n\n'
                    f'OUTPUT FORMAT:\n'
                    f'─────────────────────────────\n'
                    f'Trending Topic Found: [full phrase]\n'
                    f'Source: [platform]\n'
                    f'Relevance: [High/Medium/Low]\n'
                    f'─────────────────────────────\n'
                    f'Instagram Caption:\n'
                    f'[Post Content]\n\n'
                    f'Twitter Thread:\n'
                    f'[Post 1]\n[Post 2]\n...\n'
                    f'─────────────────────────────\n'
                    f'Fact Check Status: ✅ Verified / ⚠️ Estimated\n'
                    f'─────────────────────────────\n'
                    f'CRITICAL: You MUST use the exact headers "Instagram Caption:" and "Twitter Thread:" so the frontend app.py parser does not break!',
        agent=copywriter,
        context=[task1],
        expected_output='Professional, verified, highly specific social media package output precisely in the requested format.'
    )

    crew = Crew(
        agents=[strategist, copywriter],
        tasks=[task1, task2],
        verbose=False
    )

    return crew.kickoff()