from ingestion.files import FilesExtractor


if __name__ == "__main__":
    for file in FilesExtractor().extract():
        print(file.name)
        for section in file.sections:
            print()
            print(section.name)
            print(section.content)
