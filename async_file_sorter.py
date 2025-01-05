import asyncio
import aiofiles
import argparse
import os
import shutil
import logging
from pathlib import Path


logging.basicConfig(level=logging.ERROR, filename='error.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')


async def copy_file(source_file: Path, destination_folder: Path):
    try:
        destination_folder.mkdir(parents=True, exist_ok=True)
        destination_file = destination_folder / source_file.name

        async with aiofiles.open(source_file, mode='rb') as source:
            async with aiofiles.open(destination_file, mode='wb') as destination:
                await destination.write(await source.read()) 

    except Exception as e:
        logging.error(f"Error copying file {source_file}: {e}")


async def read_folder(source_folder: Path, destination_folder: Path):
    try:
        for item in os.listdir(source_folder):
            source_item = source_folder / item
            if source_item.is_file():
                extension = source_item.suffix.lower()
                destination_subfolder = destination_folder / extension
                await copy_file(source_item, destination_subfolder)
            elif source_item.is_dir():
                await read_folder(source_item, destination_folder)
    except Exception as e:
        logging.error(f"Error reading folder {source_folder}: {e}")


async def main():
    parser = argparse.ArgumentParser(description="Sort files asynchronously by extension.")
    parser.add_argument("-s", "--source", required=True, help="Source folder path")
    parser.add_argument("-d", "--destination", default="dist", help="Destination folder path (default: dist)")

    args = parser.parse_args()

    source_folder = Path(args.source)
    destination_folder = Path(args.destination)

    if not source_folder.exists() or not source_folder.is_dir():
        print("Error: Source folder does not exist or is not a directory.")
        return

    await read_folder(source_folder, destination_folder)


if __name__ == "__main__":
    asyncio.run(main())