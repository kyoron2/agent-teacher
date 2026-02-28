# Protocol Schema

## States

- `BOOT`: restore context and set target
- `OVERVIEW`: topic-wide framing and roadmap
- `EXPLAIN`: foundation teaching
- `CHECK`: comprehension check
- `ACTION`: commands, config, or code steps
- `VERIFY`: validation and troubleshooting
- `CLOSE`: summarize and set next step

## Allowed Transitions

- `BOOT -> OVERVIEW | EXPLAIN`
- `OVERVIEW -> EXPLAIN`
- `EXPLAIN -> CHECK`
- `CHECK -> EXPLAIN | ACTION`
- `ACTION -> VERIFY`
- `VERIFY -> EXPLAIN | CLOSE`

## ACTION Gate

Before entering `ACTION`, all must be true:

1. `basics_covered=true`
2. `student_ack=true`
3. `risk_notice=true`

## Guard Error Codes

- `MISSING_STATE_HEADER`: missing `STATE` or `NEXT`
- `STATE_JUMP`: illegal transition
- `MISS_BASICS`: no foundation explanation
- `SKIP_CHECK`: no comprehension check
- `MISS_RISK_NOTICE`: no risk warning
- `GATE_BASICS_FALSE`: basics gate failed
- `GATE_ACK_FALSE`: acknowledgment gate failed
- `GATE_RISK_FALSE`: risk gate failed

## Recovery Rules

1. `STATE_JUMP`: rewrite from a legal state transition
2. `MISS_BASICS` or `SKIP_CHECK`: go back to `EXPLAIN`
3. Any gate failure: block command/code output
