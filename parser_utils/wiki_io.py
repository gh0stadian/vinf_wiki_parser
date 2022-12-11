class WikiIO:
    def __init__(self, filepath):
        self.xml_fd = None
        self.path = filepath
        self._offset = 0
        self.residual = ""

        self.open_file()

    def open_file(self):
        """Opens the xml file."""
        try:
            self.xml_fd = open(self.path, "r", encoding="utf8")

        except Exception as e:
            print(f"Could not open file.\n{e}")

    def get_chunk(self, chunk=262144):
        """Returns a chunk of the xml file."""
        try:
            out = self.residual + self.xml_fd.read(chunk)
            last_page_end = out.rfind("</page>")
            end = last_page_end + 7 if last_page_end != -1 else 0
            self.residual = out[end:]
            return out[:end]

        except Exception as e:
            print(f"Could not read xml file.\n{e}")
