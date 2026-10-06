from crewai import Agent, Task, Crew

llm = "ollama/llama3.1"

def generate_landing_page(topic):
    lp_strategist = Agent(
        role='Landing Page Strategist',
        goal='Define value proposition and target persona for the landing page',
        backstory='Conversion rate optimization expert',
        llm=llm
    )

    lp_copywriter = Agent(
        role='Landing Page Copywriter',
        goal='Write high-converting headline, benefits, and CTA',
        backstory='Direct response copywriter specializing in lead generation',
        llm=llm
    )

    # Tasks
    value_task = Task(
        description=f'For topic "{topic}", define: core benefit, target pain point, and unique value proposition.\n\n'
                    f'CRITICAL SAFETY RULE:\n'
                    f'If the topic is sports-related (like cricket or football):\n'
                    f'✅ The landing page MUST be about a Sports News Platform, a Fan Community, or a Match Analysis Hub.\n'
                    f'❌ It MUST NEVER be a betting or prediction service. Absolutely NO gambling, betting, bankroll, or wagering terminology allowed.',
        agent=lp_strategist,
        expected_output='Value proposition document'
    )

    copy_task = Task(
        description='Write: 1) Hero headline, 2) Subheadline, 3) 4 benefit bullets, 4) CTA button text. Output as clean, readable Markdown without using JSON.',
        agent=lp_copywriter,
        expected_output='Landing page copy formatted beautifully in typical Markdown text.'
    )

    crew = Crew(
        agents=[lp_strategist, lp_copywriter],
        tasks=[value_task, copy_task],
        verbose=False
    )

    return crew.kickoff()