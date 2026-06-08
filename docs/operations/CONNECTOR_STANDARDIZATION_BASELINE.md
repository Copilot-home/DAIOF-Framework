# CONNECTOR_STANDARDIZATION_BASELINE

## 1. Scope
Áp dụng cho toàn bộ file trong `connectors/*.yaml`.

## 2. Required top-level keys
Mọi connector phải có đủ các khóa:
- `id`
- `type`
- `version`
- `capabilities`
- `mailbox_in`
- `mailbox_out`
- `scheduler`
- `triggers`
- `state`
- `health`
- `policies`
- `guardrails`
- `contracts`

## 3. Required nested contract keys
`contracts` phải có:
- `input_schema`
- `output_schema`
- `error_schema`

## 4. Realtime core contract profiles
Ba connector lõi realtime phải map profile rõ ràng:

### `conductor`
- `contracts.input_schema.profile = search_space_collapse_v1`
- `contracts.output_schema.profile = deny_rule_update_v1`

### `mcp_hub`
- `contracts.input_schema.profile = dead_end_claim_filter_v1`
- `contracts.output_schema.profile = claim_rejection_reason_v1`

### `runtime_observer`
- `contracts.input_schema.profile = denied_path_violation_event_v1`
- `contracts.output_schema.profile = collapse_telemetry_snapshot_v1`

## 5. Naming normalization
- `id`: snake_case
- Queue naming: `queue.<connector>.in|out`
- Profile naming: snake_case + version suffix `_v1`

## 6. Validation command
```bash
python3 scripts/validate_connector_standardization.py
```
