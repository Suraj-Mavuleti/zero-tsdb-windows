#!/usr/bin/env python3
import sys, time, struct, os

DB_FILE = "store.ztsdb"

def show_header():
    print("\033[1;34m" + "="*60 + "\033[0m")
    print("\033[1;34m          ZERO-TSDB: V4 NATIVE TIME-SERIES DATABASE\033[0m")
    print("\033[1;34m" + "="*60 + "\033[0m")

def insert(metric, value):
    timestamp = int(time.time())
    # Format: Timestamp (8 bytes), Metric length (1 byte), Metric string, Value (8 bytes float)
    metric_bytes = metric.encode('utf-8')[:255]
    with open(DB_FILE, "ab") as f:
        f.write(struct.pack(f"<QB{len(metric_bytes)}sd", timestamp, len(metric_bytes), metric_bytes, float(value)))
    print(f"\033[1;32m[TSDB] Successfully flushed to disk: {metric} = {value} at T={timestamp}\033[0m")

def query(target_metric):
    if not os.path.exists(DB_FILE):
        return []
    
    results = []
    with open(DB_FILE, "rb") as f:
        while True:
            header = f.read(9)
            if not header: break
            ts, length = struct.unpack("<QB", header)
            metric = f.read(length).decode('utf-8')
            value = struct.unpack("<d", f.read(8))[0]
            if metric == target_metric:
                results.append((ts, value))
    return results

def plot(target_metric):
    results = query(target_metric)
    if not results:
        print(f"\033[1;31m[TSDB] No data found for metric '{target_metric}' in local storage.\033[0m")
        return
    
    print(f"\n\033[1;36m=== TIMESERIES PLOT: {target_metric.upper()} ===\033[0m\n")
    
    max_val = max(r[1] for r in results)
    min_val = min(r[1] for r in results)
    height = 20
    
    for r in results:
        ts, val = r
        if max_val == min_val:
            normalized = height // 2
        else:
            normalized = int((val - min_val) / (max_val - min_val) * height)
        
        bar = "█" * normalized
        time_str = time.strftime('%H:%M:%S', time.localtime(ts))
        print(f"\033[1;33m{time_str}\033[0m [\033[1;37m{val:8.2f}\033[0m] | \033[1;32m{bar}\033[0m")
    print("\n")

def main():
    if len(sys.argv) < 2:
        show_header()
        print("Usage:")
        print("  ./start.sh insert <metric> <value>")
        print("  ./start.sh query <metric>")
        print("  ./start.sh plot <metric>")
        return
        
    cmd = sys.argv[1]
    if cmd == "insert" and len(sys.argv) == 4:
        insert(sys.argv[2], sys.argv[3])
    elif cmd == "query" and len(sys.argv) == 3:
        for ts, val in query(sys.argv[2]):
            time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))
            print(f"[{time_str}] : {val}")
    elif cmd == "plot" and len(sys.argv) == 3:
        plot(sys.argv[2])
    else:
        print("\033[1;31m[Error] Invalid command format.\033[0m")

if __name__ == '__main__': main()
