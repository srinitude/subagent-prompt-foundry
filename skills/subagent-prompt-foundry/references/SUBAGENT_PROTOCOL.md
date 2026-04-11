# Parent and Subagent Protocol

The subagent runs in an isolated context outside the parent’s main context window.

## Parent -> Subagent
Pass:
- task_summary
- goal
- constraints
- artifacts
- allowed_tools
- required_output
- success_criteria
- exclusions

## Subagent -> Parent
Return:
- task_understanding
- assumptions
- blocking_questions
- output
- evidence
- uncertainty
- confidence
- next_step

## Go here when
- the request mentions delegation
- the subagent is not supposed to inherit full parent context
- you need a message structure

## Do not go here when
- you are only deciding whether to ask clarifying questions
