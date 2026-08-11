import json
import os
import time
import sys
from pathlib import Path

# Thêm path để dùng engine
sys.path.append("/Users/andy/my_too_test/DAIOF-Framework")
try:
    from shortest_path_navigation_engine import PathResult
except ImportError:
    pass

def purify_generic_json_list(data: list, semantic_keys: list) -> list:
    """Hàm thanh lọc tổng quát từ purify_mesh_logs.py"""
    seen = set()
    purified = []
    for entry in data:
        # Tạo key định danh semantic
        semantic_fingerprint = tuple(str(entry.get(k, "")) for k in semantic_keys)
        if semantic_fingerprint not in seen:
            seen.add(semantic_fingerprint)
            purified.append(entry)
    return purified

def generate_1gb_dataset(file_path: str):
    """Tạo file JSON ~1GB chứa dữ liệu dư thừa."""
    print(f"🏗️ Generating 1GB dataset at {file_path}...")
    
    # 1 entry tinh chất
    core_template = {
        "event_id": "EVT_001",
        "actor": "Alpha_Prime_Omega",
        "action": "SYNC_MESH",
        "state": "SUCCESS",
        "metadata": {
            "version": "4.2.8.7",
            "proof": "X-APO-4287"
        }
    }
    
    # Chúng ta sẽ viết theo kiểu streaming để không tốn RAM khi tạo
    target_size = 1024 * 1024 * 1024 # 1GB
    current_size = 0
    
    with open(file_path, 'w') as f:
        f.write("[\n")
        first = True
        while current_size < target_size:
            # Tạo nhiễu (timestamp khác nhau nhưng semantic giống nhau)
            entry = core_template.copy()
            entry["timestamp"] = time.time()
            entry["entropy_noise"] = os.urandom(100).hex() # Thêm rác cho nặng
            
            line = json.dumps(entry)
            if not first:
                f.write(",\n")
            f.write(line)
            current_size += len(line) + 2
            first = False
            
            if current_size % (100 * 1024 * 1024) < 1000: # Log mỗi 100MB
                print(f"  Progress: {current_size / (1024*1024):.1f} MB")
                
        f.write("\n]")
    print(f"✅ 1GB Dataset created: {file_path}")

def run_purification_stress(input_path: str, output_path: str):
    """Thực thi thanh lọc trên file 1GB."""
    print(f"🧪 Starting Stress Test Purification on {input_path}...")
    start_time = time.time()
    
    # Vì file 1GB quá lớn để load vào memory bằng json.load thông thường (có thể gây crash)
    # Chúng ta sẽ sử dụng phương pháp phát hiện duplicate theo dòng hoặc stream
    # Nhưng để test "thuật toán nén", con sẽ thử load theo chunk hoặc giả lập logic seen-set
    
    seen_fingerprints = set()
    purified_count = 0
    total_count = 0
    
    # Simulating the semantic purification logic
    # Keys for purification: action, actor, state
    semantic_keys = ["action", "actor", "state"]
    
    # Để tránh OOM, con sẽ đọc từng dòng (vì mỗi object là 1 dòng trong file con vừa tạo)
    with open(input_path, 'r') as f_in, open(output_path, 'w') as f_out:
        f_out.write("[\n")
        first_out = True
        
        for line in f_in:
            line = line.strip().rstrip(',')
            if line in ("[", "]"): continue
            
            try:
                entry = json.loads(line)
                total_count += 1
                
                fingerprint = tuple(str(entry.get(k, "")) for k in semantic_keys)
                if fingerprint not in seen_fingerprints:
                    seen_fingerprints.add(fingerprint)
                    if not first_out:
                        f_out.write(",\n")
                    f_out.write(json.dumps(entry))
                    purified_count += 1
                    first_out = False
            except json.JSONDecodeError:
                continue
                
        f_out.write("\n]")
        
    end_time = time.time()
    duration = end_time - start_time
    
    reduction = (1 - (purified_count / total_count)) * 100 if total_count > 0 else 0
    
    print(f"📊 Results:")
    print(f"  - Total entries processed: {total_count}")
    print(f"  - Unique entries retained: {purified_count}")
    print(f"  - Compression Ratio: {reduction:.2f}%")
    print(f"  - Duration: {duration:.2f} seconds")
    print(f"  - Throughput: { (1024 / duration) if duration > 0 else 0:.2f} MB/s")

if __name__ == "__main__":
    input_file = "/Users/andy/balancehub/stress_test_data.json"
    output_file = "/Users/andy/balancehub/stress_test_purified.json"
    
    try:
        generate_1gb_dataset(input_file)
        run_purification_stress(input_file, output_file)
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted.")
    except Exception as e:
        print(f"❌ Error: {e}")
