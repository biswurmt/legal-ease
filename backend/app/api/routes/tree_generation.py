import concurrent.futures
from typing import Any

from fastapi import APIRouter, HTTPException
from openai import OpenAI
from sqlmodel import Session

from app.core.clients import get_boson_client
from app.models import Message
from app.schemas import ScenariosTreeResponse

router = APIRouter()

def _create_tree_single(_case_background: str, _previous_statements: str, _simulation_goal: str, _last_message: str = None, client: OpenAI = None, system_message: str = None) -> dict[str, Any]:
    """
    Helper function to create a tree with a single API call.
    Returns the parsed result or None if parsing fails.
    """
    if client is None:
        client = get_boson_client()

    # Create the conversation with the AI model
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": "Generate the legal negotiation dialogue tree now."}
    ]

    try:
        # Make API call to Qwen3-32B-thinking-Hackathon model
        response = client.chat.completions.create(
            model="Qwen3-32B-thinking-Hackathon",
            messages=messages,
            temperature=0.7,
            max_tokens=4000,
            response_format={"type": "json_object"}
        )

        # Extract the response content
        tree_content = response.choices[0].message.content

        # Try to parse as JSON
        import json
        tree_data = json.loads(tree_content)
        # Validate the response structure
        scenarios_response = ScenariosTreeResponse(**tree_data)
        return scenarios_response.model_dump()
    except Exception as e:
        # Return None if parsing fails
        return None

def create_tree(case_background: str, previous_statements: str, simulation_goal: str, last_message: str = None, _refresh: bool = False) -> dict[str, Any]:
    """
    Create a tree of messages based on the case background and previous statements.
    Makes 3 parallel API calls and keeps the first valid response.
    Uses the Qwen3-32B-thinking-Hackathon model to generate a structured 3-level dialogue tree.
    """
    try:
        # Get Boson AI client
        client = get_boson_client()

        # Prepare the complete system message for legal simulation tree generation
        if last_message:
            # If continuing from a previous message, use that as Level 1
            level1_instruction = f"Level 1: Use the provided last message as the Level 1 statement: \"{last_message}\"\n"
            special_note = f"\nIMPORTANT: The Level 1 node must use exactly this text: \"{last_message}\"\n"
            # Determine the speaker based on the last message pattern
            # If last message was from one side, the next level should be from the other
            if "A" in last_message or last_message.startswith("Your client"):
                next_speaker = "B"
                follow_up_speaker = "A"
            else:
                next_speaker = "A"
                follow_up_speaker = "B"
            level2_instruction = f"Level 2: Three possible responses from \"{next_speaker}\".\n"
            level3_instruction = f"Level 3: For each Level 2 response, provide exactly three follow-up replies from \"{follow_up_speaker}\".\n"
        else:
            # New conversation - determine who should speak first based on context
            level1_instruction = "Level 1: An opening statement. Based on the [CASE_BACKGROUND], determine who should initiate the negotiation:\n"
            level1_instruction += "- If your client (Player) should initiate (e.g., making a demand, presenting evidence, proposing settlement): speaker = \"A\"\n"
            level1_instruction += "- If the opposing side should initiate (e.g., they approach your client first, they have the burden, they sent an initial offer): speaker = \"B\"\n"
            level1_instruction += "The decision should be realistic based on negotiation dynamics and who is most likely to reach out first given the context.\n"
            special_note = ""

            # For new conversations, alternate based on who speaks first
            # This will be determined dynamically by the model
            level2_instruction = "Level 2: Three possible responses. If Level 1 speaker is \"A\", Level 2 should be responses from \"B\". If Level 1 is \"B\", Level 2 should be responses from \"A\".\n"
            level3_instruction = "Level 3: For each Level 2 response, provide exactly three follow-up replies. The speaker should alternate: if Level 2 is from \"B\", Level 3 is from \"A\"; if Level 2 is from \"A\", Level 3 is from \"B\".\n"

        system_message = (
            "You are an expert legal simulation generator. Your task is to create a realistic, branching dialogue tree for a legal negotiation scenario. You will be given a detailed case background and a specific simulation goal. Your output MUST be a single, valid JSON object and nothing else.\n\n"
            "[TASK_DEFINITION]\n"
            "Generate a dialogue tree exactly three (3) levels deep.\n"
            f"{level1_instruction}"
            f"{level2_instruction}"
            f"{level3_instruction}"
            "The dialogue must directly reflect the facts, disputed issues, and (most importantly) the personalities described in the [CASE_BACKGROUND]. The entire negotiation must be focused on achieving the [SIMULATION_GOAL].\n\n"
            "[INPUT_CONTEXT]\n\n"
            f"[CASE_BACKGROUND]\n{case_background}\n\n"
            f"[PREVIOUS STATEMENTS]\n{previous_statements}\n\n"
            f"[SIMULATION_GOAL] {simulation_goal}\n\n"
            f"{special_note}"
            "[OUTPUT_FORMAT_AND_CONSTRAINTS]\n"
            "Output format MUST be a single, valid JSON object.\n"
            "Do not include any text, explanations, or markdown formatting before or after the JSON object.\n"
            "The root of the JSON object must be scenarios_tree.\n"
            "Follow the schema precisely:\n"
            "speaker: (string) \"A\" or \"B\".\n"
            "line: (string) The text of the dialogue.\n"
            "level: (number) The depth of the node (1, 2, or 3).\n"
            "reflects_personality: (string) A brief justification of how this line reflects the facts or personality from the [CASE_BACKGROUND].\n"
            "responses: (array) An array of nested node objects. Level 3 nodes must have an empty [] responses array.\n\n"
            "[SCHEMA_DEFINITION]\n"
            "The speaker at Level 1 can be either \"A\" or \"B\" based on the context.\n"
            "Level 2 speaker must be the opposite of Level 1.\n"
            "Level 3 speaker must be the opposite of Level 2.\n"
            "Example where Player starts:\n"
            "{\n"
            '  "scenarios_tree": {\n'
            '    "speaker": "A",\n'
            '    "line": "...",\n'
            '    "level": 1,\n'
            '    "reflects_personality": "...",\n'
            '    "responses": [\n'
            '      {"speaker": "B", "line": "...", "level": 2, ...},\n'
            '      {"speaker": "B", "line": "...", "level": 2, ...},\n'
            '      {"speaker": "B", "line": "...", "level": 2, ...}\n'
            '    ]\n'
            '  }\n'
            "}\n\n"
            "Example where B starts:\n"
            "{\n"
            '  "scenarios_tree": {\n'
            '    "speaker": "B",\n'
            '    "line": "...",\n'
            '    "level": 1,\n'
            '    "reflects_personality": "...",\n'
            '    "responses": [\n'
            '      {"speaker": "A", "line": "...", "level": 2, ...},\n'
            '      {"speaker": "A", "line": "...", "level": 2, ...},\n'
            '      {"speaker": "A", "line": "...", "level": 2, ...}\n'
            '    ]\n'
            '  }\n'
            "}\n"
            "Each Level 2 response contains 3 Level 3 responses in its \"responses\" array."
        )

        # Make 3 parallel API calls using ThreadPoolExecutor
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [
                executor.submit(_create_tree_single, case_background, previous_statements, simulation_goal, last_message, client, system_message)
                for _ in range(3)
            ]

            # Wait for the first valid result
            results = []
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result is not None:
                    # Cancel remaining futures
                    for f in futures:
                        f.cancel()
                    return result
                results.append(result)

        # If all 3 attempts failed, return error response
        return {
            "error": "All 3 parallel attempts failed to generate valid response",
            "raw_response": "Failed to parse JSON from all 3 API calls",
            "scenarios_tree": {
                "speaker": "A",
                "line": "Error: Could not generate proper dialogue tree",
                "level": 1,
                "reflects_personality": "System error occurred",
                "responses": []
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating tree: {str(e)}")

def save_messages_to_tree(session: Session, _case_id: int, tree_data: dict[str, Any], existing_tree_id: int = None, last_message_id: int = None) -> bool:
    """
    Save messages from tree generation to database.
    If no last_message_id, creates a new tree with level1 as root.
    If existing_tree_id provided, appends new messages to the existing tree as children of last_message_id.
    Returns True if successful, False otherwise.
    """
    try:
        # Get the scenarios_tree from the response
        scenarios_tree = tree_data.get("scenarios_tree", {})

        if last_message_id is None:
            # No last_message_id - create new tree with level1 as root
            # Save Level 1 message as root (parent_id=None)
            level1_msg = Message(
                content=scenarios_tree.get("line", ""),
                role=scenarios_tree.get("speaker", "A"),
                simulation_id=existing_tree_id,
                parent_id=None,  # Root message
                selected=True
            )
            session.add(level1_msg)
            session.commit()
            session.refresh(level1_msg)

            # Save Level 2 messages (B responses)
            level2_messages = []
            level2_responses = scenarios_tree.get("responses", [])

            for level2_response in level2_responses:
                level2_msg = Message(
                    content=level2_response.get("line", ""),
                    role=level2_response.get("speaker", "B"),
                    simulation_id=existing_tree_id,
                    parent_id=level1_msg.id,
                    selected=False  # Not selected by default
                )
                session.add(level2_msg)
                session.commit()
                session.refresh(level2_msg)
                level2_messages.append(level2_msg)

            # Save Level 3 messages (player follow-ups)
            for i, level2_response in enumerate(level2_responses):
                if i < len(level2_messages):
                    level2_msg = level2_messages[i]
                    level3_responses = level2_response.get("responses", [])

                    for level3_response in level3_responses:
                        level3_msg = Message(
                            content=level3_response.get("line", ""),
                            role=level3_response.get("speaker", "A"),
                            simulation_id=existing_tree_id,
                            parent_id=level2_msg.id,
                            selected=False  # Not selected by default
                        )
                        session.add(level3_msg)

        else:
            # Existing history - append new messages as children of last_message_id
            last_message = session.get(Message, last_message_id)
            if not last_message:
                raise HTTPException(status_code=404, detail=f"Message with id {last_message_id} not found")

            level1_msg = last_message

            # Save Level 2 messages (B responses)
            level2_messages = []
            level2_responses = scenarios_tree.get("responses", [])

            for level2_response in level2_responses:
                level2_msg = Message(
                    content=level2_response.get("line", ""),
                    role=level2_response.get("speaker", "B"),
                    simulation_id=existing_tree_id,
                    parent_id=level1_msg.id,
                    selected=False  # Not selected by default
                )
                session.add(level2_msg)
                session.commit()
                session.refresh(level2_msg)
                level2_messages.append(level2_msg)

            # Save Level 3 messages (player follow-ups)
            for i, level2_response in enumerate(level2_responses):
                if i < len(level2_messages):
                    level2_msg = level2_messages[i]
                    level3_responses = level2_response.get("responses", [])

                    for level3_response in level3_responses:
                        level3_msg = Message(
                            content=level3_response.get("line", ""),
                            role=level3_response.get("speaker", "A"),
                            simulation_id=existing_tree_id,
                            parent_id=level2_msg.id,
                            selected=False  # Not selected by default
                        )
                        session.add(level3_msg)

        session.commit()
        return True

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error saving messages to tree: {str(e)}")
