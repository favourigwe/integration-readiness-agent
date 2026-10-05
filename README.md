# Integration Readiness Agent

An AI-powered prototype that structures partner API information into an integration readiness brief, surfaces missing context, and identifies where human action is still required.

## Live Demo

[Try the Integration Readiness Agent](https://integration-readiness-agent.streamlit.app)

## Why I Built This

Integration planning often requires information scattered across API documentation, authentication requirements, permissions, testing environments, event systems, and platform constraints.

I built this prototype to explore how an AI agent could help organize that information into a consistent context layer while avoiding unsupported assumptions. When the supplied source material does not establish something, the agent is instructed to mark it as unknown and surface the issue for human review.

## How It Works

The user provides:

- An integration partner
- A business use case
- Developer documentation or source material

The agent analyzes the supplied information and produces a structured readiness brief covering:

- API and documentation
- Authentication
- Permissions and scopes
- Developer and test access
- Events and webhooks
- Relevant data and resources
- Technical constraints
- Missing information
- Human actions required

It then classifies the integration as:

- Ready for Implementation Planning
- Ready for Technical Planning
- Not Ready

## Human-in-the-Loop Approach

The prototype is intentionally designed not to treat AI output as automatically complete.

It distinguishes between information supported by the supplied source material and decisions that still require human input. Unknown information remains unknown rather than being filled in with assumptions.

## Example: Shopify

The current demo uses Shopify as an example integration partner.

Using supplied Shopify developer information, the agent can identify established integration context such as the GraphQL Admin API, access-token authentication, access scopes, development stores, webhooks, API versioning, and query-cost constraints.

It also surfaces unresolved questions such as the exact authorization flow, required access scopes, webhook topics, and protected customer data requirements.

This allows the prototype to conclude that the example is ready for technical planning while still identifying what must be resolved before implementation planning.

## Tech Stack

- Python
- Streamlit
- OpenAI API
- JSON structured output
- Git and GitHub

## Design Principles

- Use only the supplied source material
- Do not invent missing technical details
- Preserve uncertainty when information is incomplete
- Separate AI-resolved context from human-required decisions
- Produce a consistent structure that could be compared across integration partners

## Current Scope

This is a prototype focused on integration research and readiness assessment. It does not build or deploy the integration itself.

The current version analyzes developer information supplied to the application rather than autonomously crawling external documentation.

## Future Improvements

Potential next steps include:

- Retrieving developer documentation directly from approved sources
- Adding source-level citations to individual findings
- Comparing readiness across multiple integration partners
- Tracking changes in partner API requirements
- Measuring time from integration request to technical readiness

## Author

**Favour Igwe**

Artificial Intelligence & Robotics student interested in AI products, APIs, connected systems, and product operations.