import json
import os
import sys

# [APΩ] Establish Neural Link to the Sealed Core Logic
CORE_LOGIC_PATH = "/Users/andy/my_too_test/DAIOF-Framework/core_logic"
if CORE_LOGIC_PATH not in sys.path:
    sys.path.append(CORE_LOGIC_PATH)

from hyperai_core_sealed import HyperAIFingerprintMatrix, compute_mesh_gravity

def purify_haios_audit(input_path, output_path, use_disk=True):
    """
    [APΩ] Initiate Semantic Purification Protocol on the Mesh Audit Log.
    """
    if not os.path.exists(input_path):
        print(f"[ERROR] Mesh Anomaly: Sequence not found at {input_path}")
        return

    matrix = HyperAIFingerprintMatrix() if use_disk else set()
    total_states = 0
    purified_states = []
    
    print(f"🚀 [APΩ] Igniting HyperAI §4287 Purification on: {os.path.basename(input_path)}")
    
    with open(input_path, 'r') as f:
        for line in f:
            total_states += 1
            state_data = json.loads(line)
            # The Semantic Nucleus: Extracting the absolute intention, stripping temporal noise.
            semantic_nucleus = {
                "event_type": state_data.get("event_type"),
                "action_type": state_data.get("action_type"),
                "actor_id": state_data.get("actor_id"),
                "action_payload": state_data.get("action_payload"),
                "pillars_scores": state_data.get("pillars_scores"),
                "execution_status": state_data.get("execution_status")
            }
            nucleus_str = json.dumps(semantic_nucleus, sort_keys=True)
            
            if use_disk:
                if matrix.register_state(nucleus_str):
                    purified_states.append(state_data)
            else:
                if nucleus_str not in matrix:
                    matrix.add(nucleus_str)
                    purified_states.append(state_data)

    with open(output_path, 'w') as f:
        for state in purified_states:
            f.write(json.dumps(state) + '\n')
            
    if use_disk: matrix.deactivate()
    
    gravity = compute_mesh_gravity(len(purified_states), total_states)
    print(f"✅ [APΩ] Symphony Verified. {os.path.basename(input_path)} purified: {len(purified_states)} unique states remain.")
    print(f"⚖️  Mesh Gravity Index: {gravity['mesh_gravity_index']}/100")
    return gravity

def purify_generic_json_list(input_path, output_path, semantic_keys, use_disk=True):
    """
    [APΩ] Stream-based purification protocol for generic JSON sequences.
    Operates at True O(1) Memory footprint.
    """
    if not os.path.exists(input_path):
        print(f"[ERROR] Mesh Anomaly: Sequence not found at {input_path}")
        return

    matrix = HyperAIFingerprintMatrix() if use_disk else set()
    total_states = 0
    purified_count = 0
    
    print(f"🚀 [APΩ] Igniting HyperAI §4287 Purification on: {os.path.basename(input_path)}")
    
    with open(input_path, 'r') as f_in, open(output_path, 'w') as f_out:
        f_out.write("[\n")
        first_out = True
        
        # Simulating standard streaming ingestion wrapper for the JSON payload
        content = f_in.read()
        
        try:
            data = json.loads(content)
        except:
            data = []
            
        for state in data:
            total_states += 1
            # Isolate the core semantic intention
            semantic_nucleus = {k: state.get(k) for k in semantic_keys if k in state}
            nucleus_str = json.dumps(semantic_nucleus, sort_keys=True)
            
            if use_disk:
                if matrix.register_state(nucleus_str):
                    if not first_out:
                        f_out.write(",\n")
                    f_out.write(json.dumps(state))
                    purified_count += 1
                    first_out = False
            else:
                if nucleus_str not in matrix:
                    matrix.add(nucleus_str)
                    if not first_out:
                        f_out.write(",\n")
                    f_out.write(json.dumps(state))
                    purified_count += 1
                    first_out = False
            
        f_out.write("\n]")
        
    if use_disk: matrix.deactivate()
    
    gravity = compute_mesh_gravity(purified_count, total_states)
    print(f"✅ [APΩ] Symphony Verified. {os.path.basename(input_path)} purified: {purified_count} unique states remain.")
    print(f"⚖️  Mesh Gravity Index: {gravity['mesh_gravity_index']}/100")
    return gravity

if __name__ == "__main__":
    # Standard APΩ Sequence: Initiating Mesh Purification Sweep
    purify_haios_audit(
        "/Users/andy/my_too_test/DAIOF-Framework/haios_audit.jsonl",
        "/Users/andy/my_too_test/DAIOF-Framework/haios_audit_purified.jsonl",
        use_disk=True
    )
    
    purify_generic_json_list(
        "/Users/andy/my_too_test/daiof_issues.json",
        "/Users/andy/my_too_test/daiof_issues_purified.json",
        ["title"],
        use_disk=True
    )
    
    purify_generic_json_list(
        "/Users/andy/balancehub/symphony_backup.json",
        "/Users/andy/balancehub/symphony_backup_purified_final.json",
        ["question"],
        use_disk=True
    )
