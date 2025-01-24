PORT_RANGES = [
    {"start": 11000, "end": 11010, "download": 1200, "upload": 1200}, # 50 Mbit/s
    {"start": 12001, "end": 12010, "download": 2000, "upload": 2000},   # 130 Mbit/s
    {"start": 13001, "end": 13010, "download": 250, "upload": 250},
    {"start": 14001, "end": 14010, "download": 500, "upload": 500},
    {"start": 15001, "end": 15010, "download": 1000, "upload": 1000},
]

OUTPUT_FILE = "./nginx.conf"
TEMPLATE = """server {{
    listen {port};
    ssl_preread on;
    proxy_pass 127.0.0.1:{backend_port};
    proxy_download_rate {download_rate}k;
    proxy_upload_rate {upload_rate}k;
}}\n\n"""

def convert_mbit_to_mbyte(mbit: int) -> int:
    return max(1, mbit // 8)

def generate_single_config():
    with open(OUTPUT_FILE, "w") as f:
        f.write("# Auto-generated config. Do not edit manually!\n\n")
        
        for config in PORT_RANGES:
            dl_rate = convert_mbit_to_mbyte(config["download"])
            ul_rate = convert_mbit_to_mbyte(config["upload"])
            
            for port in range(config["start"], config["end"] + 1):
                config_block = TEMPLATE.format(
                    port=port,
                    backend_port=port + 10000,
                    download_rate=dl_rate,
                    upload_rate=ul_rate
                )
                f.write(config_block)
    
    total_ports = sum(r["end"] - r["start"] + 1 for r in PORT_RANGES)
    print(f"Сгенерирован 1 файл ({OUTPUT_FILE}) с {total_ports} серверами")

if __name__ == "__main__":
    generate_single_config()