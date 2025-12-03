import operator
import json
import os
from typing import Annotated, List, TypedDict
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()

# Define the State
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    plan: List[str]
    current_step: int
    results: dict

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini")

# --- Planner Node ---
planner_prompt = ChatPromptTemplate.from_template(
    """You are a planner. Given a user request to list the last file in a folder, create a step-by-step plan to answer it.
    Return the plan as a JSON list of strings.
    
    Request: {request}
    
    Plan:"""
)

def planner_node(state: AgentState):
    print("--- Planner Node ---")
    request = state["messages"][-1].content
    chain = planner_prompt | llm
    response = chain.invoke({"request": request})
    
    try:
        # Clean up markdown code blocks if present
        content = response.content.replace("```json", "").replace("```", "").strip()
        plan = json.loads(content)
    except json.JSONDecodeError:
        # Fallback
        plan = [line.strip() for line in response.content.split('\n') if line.strip()]
    
    print(f"Generated Plan: {plan}")
    return {"plan": plan, "current_step": 0, "results": {}}

# --- Executor Node ---
executor_prompt = ChatPromptTemplate.from_template(
    """You are an executor. Execute the following step: {step}.
    Previous results: {results}
    
    Return the result of the execution."""
)

def executor_node(state: AgentState):
    print("--- Executor Node ---")
    plan = state["plan"]
    current_step = state["current_step"]
    
    if current_step >= len(plan):
        return {"messages": [AIMessage(content="All steps completed.")]}

    step = plan[current_step]
    results = state["results"]

    print(f"Executing Step {current_step + 1}: {step}")

    # Check if the step requires listing files
    if "list" in step.lower() and "downloads" in step.lower():
        try:
            downloads_path = r"C:\Users\andres.rojas\Downloads"
            files = os.listdir(downloads_path)
            if files:
                # Sort by modification time and get the last file
                files_with_time = [(f, os.path.getmtime(os.path.join(downloads_path, f))) for f in files]
                last_file = max(files_with_time, key=lambda x: x[1])[0]
                response_content = f"The last file in Downloads folder is: {last_file}"
            else:
                response_content = "The Downloads folder is empty."
        except Exception as e:
            response_content = f"Error listing files: {str(e)}"
    else:
        chain = executor_prompt | llm
        response = chain.invoke({"step": step, "results": results})
        response_content = response.content

    # Update results
    results[f"step_{current_step + 1}"] = response_content

    return {
        "current_step": current_step + 1,
        "results": results,
        "messages": [AIMessage(content=f"Executed: {step} -> {response_content}")]
    }

# --- Main Execution ---
if __name__ == "__main__":
    # Open file for logging
    output_file = "output.md"
    with open(output_file, "w") as log:
        # Example query
        user_input = "List the last file in the Downloads folder"
        
        log.write(f"# Agent Workflow Execution\n\n")
        log.write(f"**User Request:** {user_input}\n\n")
        
        # First, generate the plan
        planner_state = planner_node({
            "messages": [HumanMessage(content=user_input)],
            "plan": [],
            "current_step": 0,
            "results": {}
        })
        
        plan = planner_state["plan"]
        
        # Log the generated plan
        log.write("## Generated Plan\n\n")
        for i, step in enumerate(plan, 1):
            log.write(f"{i}. {step}\n")
        log.write("\n")
        
        # Ask user for confirmation before executing the plan
        print("\n--- Generated Plan ---")
        for i, step in enumerate(plan, 1):
            print(f"{i}. {step}")
        
        print("\n")
        confirmation = input("Are you sure you want to execute this plan? (Y/N): ").strip().upper()
        
        if confirmation == "Y":
            log.write("## Execution\n\n")
            log.write("User confirmed execution.\n\n")
            
            # Create the state with the generated plan
            state = {
                "messages": [HumanMessage(content=user_input)],
                "plan": plan,
                "current_step": 0,
                "results": {}
            }
            
            # Execute the plan
            for i in range(len(plan)):
                executor_state = executor_node(state)
                state["current_step"] = executor_state["current_step"]
                state["results"] = executor_state["results"]
                state["messages"].append(executor_state["messages"][0])
            
            # Log final results
            log.write("## Final Results\n\n")
            for step_key, result in state["results"].items():
                log.write(f"**{step_key}:** {result}\n\n")
            
            print("\n--- Final Results ---")
            print(f"Results: {state['results']}")
        else:
            log.write("Execution cancelled by user.\n")
            print("\nExecution cancelled by user.")
    
    print(f"\nOutput logged to {output_file}")
