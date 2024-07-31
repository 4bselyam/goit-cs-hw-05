import asyncio
import aiofiles
import aiopath
import argparse
import logging
from pathlib import Path
from aiofiles.os import makedirs

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


async def read_folder(source_folder, output_folder):
    async for file_path in aiopath.AsyncPath(source_folder).rglob("*"):
        if file_path.is_file():
            await copy_file(file_path, output_folder)


async def copy_file(file_path, output_folder):
    ext = file_path.suffix.lower().strip(".")
    target_folder = aiopath.AsyncPath(output_folder) / ext
    await makedirs(target_folder, exist_ok=True)
    target_path = target_folder / file_path.name

    try:
        async with aiofiles.open(file_path, "rb") as src_file:
            async with aiofiles.open(target_path, "wb") as dst_file:
                while True:
                    chunk = await src_file.read(1024)
                    if not chunk:
                        break
                    await dst_file.write(chunk)
        logging.info(f"Copied {file_path} to {target_path}")
    except Exception as e:
        logging.error(f"Failed to copy {file_path} to {target_path}: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Async file sorter based on file extensions."
    )
    parser.add_argument("source_folder", type=str, help="Path to the source folder.")
    parser.add_argument("output_folder", type=str, help="Path to the output folder.")
    args = parser.parse_args()

    source_folder = aiopath.AsyncPath(args.source_folder)
    output_folder = aiopath.AsyncPath(args.output_folder)

    asyncio.run(read_folder(source_folder, output_folder))


if __name__ == "__main__":
    main()
