from pathlib import Path

import docker


def main():

    client = docker.from_env()
    # Includes stop containers, which might be e.g. failing tasks
    all_containers = client.containers.list(all=True)

    out_dir = Path.cwd() / "ignore"
    out_dir.mkdir(parents=True, exist_ok=True)

    # get the services logs
    for container in all_containers:
        service_file = out_dir / f"{container.name}.log"
        service_file.write_text(
            container.logs(
                timestamps=True, stdout=True, stderr=True, stream=False
            ).decode()
        )

    if all_containers:
        print(
            "\n\t",
            f"wrote docker log files for {len(all_containers)} containers in ",
            out_dir,
        )


if __name__ == "__main__":
    main()
