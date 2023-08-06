class FileFormat(type):
    ...


class TerraformFile(FileFormat):
    __format_name__ = "terraform"


class DotEnvFile(FileFormat):
    __format_name__ = ".env"
