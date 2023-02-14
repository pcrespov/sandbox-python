from pathlib import Path

import yaml


def main():
    specs = {
        "services": {
            f"httpbin_{i}": {"image": "kennethreitz/httpbin", "ports": [f"{8000+i}:80"]}
            for i in range(200)
        }
    }
    Path("docker-compose.yml").write_text(yaml.safe_dump(specs, sort_keys=False))


if __name__ == "__main__":
    main()
