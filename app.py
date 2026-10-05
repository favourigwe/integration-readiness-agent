import streamlit as st
from openai import OpenAI
import json
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(
    page_title="Integration Readiness Agent",
    page_icon="🔗",
    layout="wide"
)

st.title("Integration Readiness Agent")

st.write(
    "Structure developer information for a prospective integration, "
    "surface missing context, and identify where human action is still required."
)

st.divider()

partner = st.text_input(
    "Integration Partner",
    value="Shopify"
)

business_use_case = st.text_area(
    "Business Use Case",
    value=(
        "Provide commerce and customer signals from Shopify "
        "to a downstream marketing platform."
    )
)

documentation = st.text_input(
    "Developer Documentation",
    value="https://shopify.dev/docs"
)


source_material = st.text_area(
    "Documentation / Source Material",
    value=(
        "Shopify's primary Admin API is the GraphQL Admin API. "
        "Authentication uses access tokens, while the authorization flow depends "
        "on the app architecture and distribution method. Shopify uses access "
        "scopes to control permissions. Development stores can be used for testing. "
        "Shopify supports webhooks for event-driven integrations. Relevant resources "
        "include customers, orders, products, inventory, and metafields. GraphQL "
        "requests are subject to calculated query-cost rate limits. Shopify releases "
        "API versions quarterly. Access to protected customer data may require "
        "additional review depending on the data and app."
    ),
    height=180
)

analyze = st.button(
    "Analyze Integration",
    type="primary"
)

if analyze:
    if not source_material.strip():
        st.error("Please provide documentation or source material before analyzing.")
    else:
        with st.spinner("Analyzing integration readiness..."):
            try:
                prompt = f"""
You are an Integration Readiness Agent.

Your job is to evaluate whether a prospective software integration has enough
technical context to begin planning.

IMPORTANT RULES:
- Use ONLY the source material provided below.
- Do not rely on outside knowledge.
- Never invent technical details.
- If the source material does not establish something, mark it as Unknown.
- Distinguish clearly between Confirmed, Partial, and Unknown information.
- Identify decisions or actions that still require a human.
- Do not claim that you visited or read the documentation URL.
- The documentation URL is provided only as a source reference.

INTEGRATION PARTNER:
{partner}

BUSINESS USE CASE:
{business_use_case}

DOCUMENTATION REFERENCE:
{documentation}

SOURCE MATERIAL:
{source_material}

Analyze these areas:
1. API and documentation
2. Authentication
3. Permissions and scopes
4. Developer and test access
5. Events and webhooks
6. Relevant data and resources
7. Technical constraints
8. Missing information
9. Human actions required

Choose exactly one readiness assessment:
- READY FOR IMPLEMENTATION PLANNING
- READY FOR TECHNICAL PLANNING
- NOT READY

Follow the JSON structure exactly.
Do not rename keys or create alternative keys.
For data_resources, always use "resource" and "details".
For technical_constraints, always use "constraint" and "status".
For missing_information, always use "topic" and "status".
For human_actions, always use "action".
Do not return dictionaries as text strings.

Return ONLY valid JSON using this exact structure:

{{
    "readiness": "",
    "readiness_summary": "",
    "api_documentation": {{
        "status": "",
        "confidence": "",
        "details": "",
        "evidence": ""
    }},
    "authentication": {{
        "status": "",
        "confidence": "",
        "details": "",
        "evidence": ""
    }},
    "permissions_scopes": {{
        "status": "",
        "confidence": "",
        "details": "",
        "evidence": ""
    }},
    "developer_test_access": {{
        "status": "",
        "confidence": "",
        "details": "",
        "evidence": ""
    }},
    "events_webhooks": {{
        "status": "",
        "confidence": "",
        "details": "",
        "evidence": ""
    }},
    "data_resources": [
    {{
        "resource": "",
        "details": ""
    }}
],
"technical_constraints": [
    {{
        "constraint": "",
        "status": ""
    }}
],
"missing_information": [
    {{
        "topic": "",
        "status": "Unknown"
    }}
],
"human_actions": [
    {{
        "action": ""
    }}
]
}}
"""

                response = client.responses.create(
                    model="gpt-5.4-mini",
                    input=prompt
                )

                result = json.loads(response.output_text)

                st.success("Analysis complete.")
                st.divider()
                st.subheader(f"{partner} Integration Readiness")

                # Calculate summary metrics
                analysis_sections = [
                    result["api_documentation"],
                    result["authentication"],
                    result["permissions_scopes"],
                    result["developer_test_access"],
                    result["events_webhooks"],
                ]

                confirmed_count = sum(
                    1 for section in analysis_sections
                    if section.get("status") == "Confirmed"
                )

                human_actions = result.get("human_actions", [])
                readiness = result.get("readiness", "Unknown")

                if readiness == "READY FOR IMPLEMENTATION PLANNING":
                    readiness_short = "Implementation"
                elif readiness == "READY FOR TECHNICAL PLANNING":
                    readiness_short = "Planning"
                else:
                    readiness_short = "Not Ready"

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Readiness", readiness_short)

                with col2:
                    st.metric("Confirmed Areas", confirmed_count)

                with col3:
                    st.metric(
                        "Human Review",
                        "Required" if human_actions else "Not Required"
                    )

                st.divider()

                # Helper for displaying each analysis section
                def display_section(title, section):
                    st.subheader(title)

                    status = section.get("status", "Unknown")
                    confidence = section.get("confidence", "Unknown")
                    label = f"{status} · {confidence} confidence"

                    if status == "Confirmed":
                        st.success(label)
                    elif status == "Partial":
                        st.warning(label)
                    else:
                        st.info(label)

                    st.write(section.get("details", "No details available."))

                    evidence = section.get("evidence", "")
                    if evidence:
                        st.caption(f"Evidence: {evidence}")

                display_section(
                    "API & Documentation",
                    result["api_documentation"]
                )

                display_section(
                    "Authentication",
                    result["authentication"]
                )

                display_section(
                    "Permissions & Scopes",
                    result["permissions_scopes"]
                )

                display_section(
                    "Developer & Test Access",
                    result["developer_test_access"]
                )

                display_section(
                    "Events & Webhooks",
                    result["events_webhooks"]
                )

                st.subheader("Relevant Data & Resources")

                for item in result.get("data_resources", []):
                    if isinstance(item, dict):
                        resource = item.get("resource") or item.get("name") or item.get("item") or "Unknown"
                        details = item.get("details", "")
                        st.write(f"• **{resource}** — {details}")
                    else:
                        st.write(f"• {item}")

                st.subheader("Technical Constraints")

                for item in result.get("technical_constraints", []):
                    if isinstance(item, dict):
                        text = item.get("constraint") or item.get("name") or item.get("item") or item.get("details") or "Unknown constraint"
                        status = item.get("status", "")
                        st.write(f"• {text} {f'({status})' if status else ''}")
                    else:
                        st.write(f"• {item}")

                st.subheader("Missing Information")

                missing_information = result.get("missing_information", [])

                if missing_information:
                    for item in missing_information:
                        if isinstance(item, dict):
                            text = item.get("topic") or item.get("item") or item.get("details") or "Unknown information"
                            status = item.get("status", "Unknown")
                            st.write(f"• **{status}:** {text}")
                        else:
                            st.write(f"• {item}")
                else:
                    st.success("No major missing information identified.")

                st.subheader("Human Actions Required")

                if human_actions:
                    for item in human_actions:
                        if isinstance(item, dict):
                            action = item.get("action", str(item))
                            st.info(f"👤 {action}")
                        else:
                            st.info(f"👤 {item}")
                else:
                    st.success("No human actions currently identified.")

                st.divider()
                st.subheader("Readiness Assessment")

                if readiness == "READY FOR IMPLEMENTATION PLANNING":
                    st.success("🟢 READY FOR IMPLEMENTATION PLANNING")
                elif readiness == "READY FOR TECHNICAL PLANNING":
                    st.warning("🟡 READY FOR TECHNICAL PLANNING")
                else:
                    st.error("🔴 NOT READY")

                st.write(
                    result.get(
                        "readiness_summary",
                        "No readiness summary available."
                    )
                )
    

            except Exception as e:
                st.error("Analysis failed. Please check the API connection and try again.")
