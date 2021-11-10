import docker
from io import StringIO
from typing import Dict
import json
from tempfile import SpooledTemporaryFile
from pathlib import Path
import io



pull_repo = "itisfoundation/sleeper"
pull_tag = "2.1.1"
owner_email = "me@me.com"

client = docker.from_env()

print(f"Pulling {pull_repo}:{pull_tag} ...")
image = client.images.pull(pull_repo, tag=pull_tag)
assert image, f"image {pull_repo}:{pull_tag} could NOT be pulled!"

print(json.dumps(image.labels, indent=2))
image_labels: Dict = dict(image.labels)

# will override owner to gain FULL access rights
if owner_email:
    image_labels.update({"io.simcore.contact": f'{{"contact": "{owner_email}"}}'})


    # with io.BytesIO()
    #     fh.write(f"FROM {pull_repo}:{pull_tag}")
    #     fh.seek(0)
    #     image2, build_logs_iter = client.images.build(
    #     fileobj=fh._file, labels=image_labels, tag=f"{pull_tag}-owned2"
    #     )
    #     for line in build_logs_iter:
    #         print(line)
    df_path = Path("Dockerfile").resolve()
    df_path.write_text(f"FROM {pull_repo}:{pull_tag}")
    image2, build_logs_iter = client.images.build(
       path=str(df_path.parent), labels=image_labels, tag=f"{pull_tag}-owned"
    )
    for log in build_logs_iter:
        print("", log["stream"])
    df_path.unlink()



    print(json.dumps(image2.labels, indent=2))


def extract_labels(img):
    return {
        key[len("io.simcore.") :]: json.loads(value)[key[len("io.simcore.") :]]
        for key, value in img.labels.items()
        if key.startswith("io.simcore.")
    }


print(json.dumps(extract_labels(image2), indent=2))