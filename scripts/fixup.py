#!/usr/bin/python
import json


def patch_image(image: dict) -> dict:
    amd64 = image["Architecture"] == "amd64"

    image["Tags"] = image.pop("RepoTags")
    if amd64:
        image["Tags"].remove("nightly-aarch64")
    else:
        image["Tags"].remove("nightly")
    mediatype = image["LayersData"][0]["MIMEType"]
    image["MediaType"] = mediatype
    return image


with open("index/static") as file:
    static = json.loads(file.read())

image_1 = static["Results"][0]["Images"][0]
image_2 = static["Results"][1]["Images"][0]

image_1 = patch_image(image_1)
image_2 = patch_image(image_2)
static["Results"][0]["Images"][0] = image_1
static["Results"][1]["Images"][0] = image_2

with open("index/static", "w") as file:
    out = json.dumps(static, indent=4)
    file.write(out)
