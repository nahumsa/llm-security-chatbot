from typing import Optional
import requests

from ingestion.parser import FileParser, Parser, File

root_path = (
    "https://raw.githubusercontent.com"
    + "/OWASP"
    + "/www-project-top-10-for-large-language-model-applications"
    + "/main"
    + "/1_1_vulns"
)

rel_file_paths = [
    "LLM01_PromptInjection.md",
    "LLM02_InsecureOutputHandling.md",
    "LLM03_TrainingDataPoisoning.md",
    "LLM04_ModelDoS.md",
    "LLM05_SupplyChainVulnerabilities.md",
    "LLM06_SensitiveInformationDisclosure.md",
    "LLM07_InsecurePluginDesign.md",
    "LLM08_ExcessiveAgency.md",
    "LLM09_Overreliance.md",
    "LLM10_ModelTheft.md",
]


class FilesExtractor:
    def __init__(self, parser: Optional[Parser] = None) -> None:
        if not parser:
            self.parser = FileParser()

        else:
            self.parser = parser

    def extract(self) -> list[File]:
        extracted_texts: list[File] = []

        for file_path in rel_file_paths:
            req = requests.get(url=root_path + "/" + file_path)
            parsed_text = self.parser.parse(req.text)
            extracted_texts.append(parsed_text)

        return extracted_texts
