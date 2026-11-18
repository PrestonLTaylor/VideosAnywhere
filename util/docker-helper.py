"""
A helper script for building and running VideosAnywhere inside docker.

See print_usage for more details.
"""

import docker, docker.errors
import sys

# The name of the tag to use within the script for the docker image.
VIDEOSANYWHERE_IMAGE_TAG: str = "videosanywhere:latest"

def print_usage() -> None:
    """
    Prints the usage of the script to stdout.
    """

    print("Usage:")
    print("py docker-helper.py build: Removes the current videosanywhere:latest docker image and containers and rebuilds the image.")
    print("py docker-helper.py run: Runs the videosanywhere:latest docker image with a port binding of 6000:6000.")
    print("py docker-helper.py usage: Prints usage of this script.")

def cleanup_and_build_image() -> None:
    """
    Stops and removes any containers that are using the image we are rebuilding, removes the old image and then builds
    VideosAnywhere using the dockerfile in the root of the project.

    Will report any issues with the removal/build process to the user and exit the script.
    """

    print("Cleaning up old VideosAnywhere containers and images.")

    client = docker.from_env()

    try:
        old_containers = client.containers.list(all=True, filters={"ancestor": VIDEOSANYWHERE_IMAGE_TAG})
        for container in old_containers:
            container.stop()
            container.remove()
    except Exception as e:
        print("Error from the docker server whilst removing old VideosAnywhere containers: ", e)
        return

    try:
        old_image = client.images.get(VIDEOSANYWHERE_IMAGE_TAG)
        old_image.remove()
    except docker.errors.APIError as e:
        # Ignore APIErrors that are Not Found errors.
        if e.status_code != 404:
            print("Error from the docker server whilst removing old VideosAnywhere image: ", e)
            return
    except:
        # Ignore docker.error.ImageNotFound errors.
        pass

    print("Building new VideosAnywhere images.")

    try:
        client.images.build(path="../", tag=VIDEOSANYWHERE_IMAGE_TAG, rm=True)
    except Exception as e:
        print("Error whilst building new VideosAnywhere image: ", e)
        return

    print("Successfully build new VideosAnywhere image.")

def run_image() -> None:
    """
    Runs the vidoesanywhere:latest with a port binding of 6000:6000 and detaches.
    """

    print("Trying to run the videosanywhere:latest docker image.")

    client = docker.from_env()

    try:
        client.containers.run(VIDEOSANYWHERE_IMAGE_TAG, ports={'6000/tcp': 6000}, detach=True)
    except docker.errors.ImageNotFound:
        print(f"Docker could not find {VIDEOSANYWHERE_IMAGE_TAG} image, try running py docker-helper.py build first.")
    except Exception as e:
        print("Error whilst trying to run image: ", e)

def main() -> None:
    if len(sys.argv) < 2:
        print_usage()
        return

    arg = sys.argv[1].lower()

    if arg == "usage":
        print_usage()
    elif arg == "build":
        cleanup_and_build_image()
    elif arg == "run":
        run_image()

if __name__ == "__main__":
    main()