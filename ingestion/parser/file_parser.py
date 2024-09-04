from ingestion.parser.base import Parser
from ingestion.parser.model import File, Section


class FileParser(Parser):
    def __init__(self) -> None:
        pass

    def parse(self, text: str) -> File:
        return File(name=self.parse_title(text), sections=self.parse_sections(text))

    def parse_title(self, text: str) -> str:
        markdown_lines = text.split("\n")

        for line in markdown_lines:
            line = line.strip()

            if line.startswith("## "):
                return line[3:].strip()

        raise ValueError("file doesn't have a title")

    def parse_sections(self, text: str) -> list[Section]:
        sections = {}
        current_section = None
        current_content = []

        markdown_lines = text.split("\n")

        for line in markdown_lines:
            line = line.strip()

            if line.startswith("### "):
                if current_section:
                    sections[current_section] = "\n".join(current_content).strip()

                current_section = line[3:].strip()
                current_content = []

            elif current_section:
                current_content.append(line)

        if current_section:
            sections[current_section] = "\n".join(current_content).strip()

        return [Section(name=key, content=value) for key, value in sections.items()]
