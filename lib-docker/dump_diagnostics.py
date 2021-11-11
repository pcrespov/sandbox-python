from pathlib import Path

import docker
import json
import re

COLOR_ENCODING_RE = re.compile(r"\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[mGK]")


def main():

    client = docker.from_env()
    # Includes stop containers, which might be e.g. failing tasks
    all_containers = client.containers.list(all=True)

    out_dir = Path.cwd() / "ignore"
    out_dir.mkdir(parents=True, exist_ok=True)

    # get the services logs
    for container in all_containers:

        logs = COLOR_ENCODING_RE.sub(
            "",
            container.logs(
                timestamps=True, stdout=True, stderr=True, stream=False
            ).decode(),
        )
        (out_dir / f"{container.name}.log").write_text(logs)

        # with (out_dir / f"{container.name}.log").open("wt") as fh:
        #     for line in container.logs(timestamps=True, stdout=True, stderr=True, stream=True):
        #         fh.write( COLOR_ENCODING_RE.sub("", line.decode()) )

        (out_dir / f"{container.name}.json").write_text(
            json.dumps(container.attrs, indent=2)
        )

    if all_containers:
        print(
            "\n\t",
            f"wrote docker log files for {len(all_containers)} containers in ",
            out_dir,
        )


if __name__ == "__main__":
    main()
