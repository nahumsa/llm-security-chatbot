import requests

root_path = "https://raw.githubusercontent.com/OWASP/www-project-top-10-for-large-language-model-applications/main/1_1_vulns/"

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
    def __init__(self) -> None:
        pass

    def extract(self) -> list[str]:
        extracted_texts: list[str] = []

        for file_path in rel_file_paths:
            req = requests.get(url=root_path + file_path)
            extracted_texts.append(req.text)

        return extracted_texts
